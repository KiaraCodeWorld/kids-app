"""
Brain Quest — Mission service layer.

Ties the pure engine/leveling/mascot modules to the database models:
player resolution, streak + recovery state, building today's mission, and
processing a completed mission (XP, level-up, streak, badges, history).
"""
from datetime import date, timedelta
from django.utils import timezone

from .models import PlayerProfile, MissionRecord
from . import leveling, mascot
from .mission_engine import build_daily_mission, gradeable_count


# ── player resolution (works logged-in or anonymous) ────────────────────────
def get_player(request) -> PlayerProfile:
    if request.user.is_authenticated:
        player, _ = PlayerProfile.objects.get_or_create(user=request.user)
        # Inherit grade from UserProfile if present
        if player.total_missions == 0 and hasattr(request.user, 'profile'):
            player.grade_level = request.user.profile.grade_level or player.grade_level
            player.save(update_fields=['grade_level'])
        return player

    if not request.session.session_key:
        request.session.save()
    key = request.session.session_key
    player, _ = PlayerProfile.objects.get_or_create(session_key=key, user__isnull=True)
    return player


# ── streak / recovery state ─────────────────────────────────────────────────
def mission_state(player: PlayerProfile, today: date | None = None) -> dict:
    """Describe today's mission status without mutating anything."""
    today = today or date.today()
    last = player.last_mission_date
    gap = (today - last).days if last else None

    completed_today = gap == 0
    is_recovery = gap == 2  # missed exactly one day
    return {
        "completed_today": completed_today,
        "is_recovery": is_recovery,
        "gap": gap,
        "today": today,
    }


def todays_record(player: PlayerProfile, today: date | None = None):
    today = today or date.today()
    return player.missions.filter(mission_date=today).order_by('-created_at').first()


# ── build today's mission ───────────────────────────────────────────────────
def get_or_build_today_mission(player: PlayerProfile, today: date | None = None):
    """Return (record, items, state). Reuses today's record if one exists so the
    same 3 items are shown all day; creates a fresh one otherwise."""
    today = today or date.today()
    state = mission_state(player, today)

    existing = todays_record(player, today)
    if existing and existing.items_json:
        return existing, existing.items_json, state

    seed = f"{player.id}-{today.isoformat()}"
    items = build_daily_mission(
        grade=player.grade_level,
        weak_subject=player.weak_subject(),
        strong_subject=player.strong_subject(),
        seen_uids=player.recent_seen_uids(14),
        seed=seed,
    )

    record = MissionRecord.objects.create(
        player=player,
        mission_date=today,
        items_json=items,
        is_recovery=state["is_recovery"],
        total=gradeable_count(items),
    )
    return record, items, state


# ── complete a mission ──────────────────────────────────────────────────────
def complete_mission(player: PlayerProfile, record: MissionRecord, results: list,
                     today: date | None = None) -> dict:
    """results: [{uid, subject, correct(bool), gradeable(bool)}]. Idempotent
    for a given day — completing again won't double-count streak/XP."""
    today = today or date.today()

    if record.completed:
        # Already finalized today — return a summary without re-awarding.
        return _summary_payload(player, record, leveled_up=False,
                                new_milestone=False, prev_level=player.level)

    prev_level = player.level
    prev_streak = player.current_streak

    # ── streak update ──
    last = player.last_mission_date
    gap = (today - last).days if last else None
    is_recovery = record.is_recovery or (gap == 2)
    if gap == 0:
        pass  # already counted today (shouldn't happen — record not completed)
    elif gap == 1 or gap == 2:
        player.current_streak = prev_streak + 1   # consecutive OR recovery (preserved)
    else:
        player.current_streak = 1                 # first mission or streak broken
    player.last_mission_date = today
    player.longest_streak = max(player.longest_streak, player.current_streak)

    # ── scoring & subject stats ──
    correct = sum(1 for r in results if r.get("gradeable") and r.get("correct"))
    gradeable = sum(1 for r in results if r.get("gradeable"))
    stats = dict(player.subject_stats or {})
    for r in results:
        if not r.get("gradeable"):
            continue
        subj = r.get("subject", "math")
        s = dict(stats.get(subj, {"correct": 0, "total": 0}))
        s["total"] += 1
        if r.get("correct"):
            s["correct"] += 1
        stats[subj] = s
    player.subject_stats = stats

    # ── seen items (for 14-day no-repeat) ──
    seen = dict(player.seen_items or {})
    for it in record.items_json:
        uid = it.get("uid")
        if uid:
            seen[uid] = today.isoformat()
    # prune anything older than 30 days to keep it small
    cutoff = (today - timedelta(days=30)).isoformat()
    seen = {u: d for u, d in seen.items() if d >= cutoff}
    player.seen_items = seen

    # ── XP & level ──
    xp_info = leveling.compute_mission_xp(correct, gradeable,
                                          player.current_streak, is_recovery)
    player.xp += xp_info["total"]
    player.level = leveling.level_from_xp(player.xp)
    leveled_up = player.level > prev_level

    # ── totals ──
    player.total_missions += 1
    player.total_correct += correct
    player.total_items += gradeable

    # ── badges ──
    new_badges = _award_badges(player)

    player.save()

    # ── record ──
    record.score = correct
    record.total = gradeable
    record.xp_earned = xp_info["total"]
    record.completed = True
    record.completed_at = timezone.now()
    record.save()

    new_milestone = leveling.streak_milestone_bonus(player.current_streak) > 0

    payload = _summary_payload(player, record, leveled_up, new_milestone, prev_level)
    payload["xp_breakdown"] = xp_info["breakdown"]
    payload["xp_earned"] = xp_info["total"]
    payload["new_badges"] = new_badges
    payload["is_recovery"] = is_recovery
    return payload


BADGE_DEFS = {
    "first_mission": {"emoji": "🎯", "name": "First Quest!", "desc": "Completed your first mission"},
    "streak_3":      {"emoji": "🔥", "name": "On Fire!", "desc": "3-day streak"},
    "streak_7":      {"emoji": "🏆", "name": "Week Warrior", "desc": "7-day streak"},
    "streak_14":     {"emoji": "⭐", "name": "Two-Week Star", "desc": "14-day streak"},
    "streak_30":     {"emoji": "👑", "name": "Quest Royalty", "desc": "30-day streak"},
    "level_5":       {"emoji": "🚀", "name": "Rising Star", "desc": "Reached Level 5"},
    "level_10":      {"emoji": "🧠", "name": "Big Brain", "desc": "Reached Level 10"},
    "missions_10":   {"emoji": "💪", "name": "Dedicated", "desc": "Completed 10 missions"},
}


def _award_badges(player: PlayerProfile) -> list:
    earned = set(player.badges or [])
    checks = {
        "first_mission": player.total_missions + 1 >= 1,
        "streak_3": player.current_streak >= 3,
        "streak_7": player.current_streak >= 7,
        "streak_14": player.current_streak >= 14,
        "streak_30": player.current_streak >= 30,
        "level_5": player.level >= 5,
        "level_10": player.level >= 10,
        "missions_10": player.total_missions + 1 >= 10,
    }
    new = []
    for key, ok in checks.items():
        if ok and key not in earned:
            earned.add(key)
            new.append(BADGE_DEFS[key])
    player.badges = list(earned)
    return new


def _summary_payload(player, record, leveled_up, new_milestone, prev_level):
    prog = leveling.level_progress(player.xp)
    reaction = mascot.react_to_summary(
        record.score, record.total, leveled_up,
        player.current_streak, new_milestone,
    )
    return {
        "score": record.score,
        "total": record.total,
        "streak": player.current_streak,
        "longest_streak": player.longest_streak,
        "level": prog["level"],
        "level_title": prog["title"],
        "leveled_up": leveled_up,
        "prev_level": prev_level,
        "xp": player.xp,
        "level_percent": prog["percent"],
        "xp_to_next": prog["xp_to_next"],
        "mascot": reaction,
        "mascot_name": player.mascot_name,
        "mascot_emoji": mascot.species_emoji(player.mascot_species),
    }


def player_dashboard(player: PlayerProfile) -> dict:
    """Snapshot for the home/mission-intro card."""
    prog = leveling.level_progress(player.xp)
    state = mission_state(player)
    greeting = mascot.greet(
        player.mascot_name,
        streak=player.current_streak,
        completed_today=state["completed_today"],
    )
    return {
        "mascot_name": player.mascot_name,
        "mascot_emoji": mascot.species_emoji(player.mascot_species),
        "mascot_species": player.mascot_species,
        "greeting": greeting,
        "level": prog["level"],
        "level_title": prog["title"],
        "level_percent": prog["percent"],
        "xp": player.xp,
        "xp_to_next": prog["xp_to_next"],
        "streak": player.current_streak,
        "longest_streak": player.longest_streak,
        "completed_today": state["completed_today"],
        "is_recovery": state["is_recovery"],
        "total_missions": player.total_missions,
        "accuracy": player.accuracy(),
        "badges": [BADGE_DEFS[b] for b in (player.badges or []) if b in BADGE_DEFS],
        "grade_level": player.grade_level,
    }
