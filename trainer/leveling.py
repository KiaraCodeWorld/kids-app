"""
Brain Quest — XP & Leveling system.

Pure functions (no DB) so they're easy to test and reuse.

XP is awarded for completing missions, getting items correct, perfect
missions, and hitting streak milestones. Levels are derived from cumulative
XP via a gently rising curve, each with a kid-friendly title.
"""

# Each level has a title. Beyond the list, titles cycle on the last few.
LEVEL_TITLES = [
    "Sprout",       # 1
    "Spark",        # 2
    "Explorer",     # 3
    "Adventurer",   # 4
    "Pathfinder",   # 5
    "Champion",     # 6
    "Master Mind",  # 7
    "Genius",       # 8
    "Legend",       # 9
    "Brainiac",     # 10
    "Quest Hero",   # 11
    "Grand Sage",   # 12
]

# XP awards
XP_MISSION_COMPLETE = 20      # base for finishing a mission
XP_PER_CORRECT = 5            # each correct gradeable item
XP_PERFECT_BONUS = 15        # all gradeable items correct
XP_RECOVERY_BONUS = 10       # completing a recovery mission

# Streak milestone bonuses (day -> bonus XP)
STREAK_MILESTONE_XP = {3: 25, 7: 50, 14: 100, 30: 200}


def xp_threshold(level: int) -> int:
    """Cumulative XP required to *reach* the start of a given level.

    Level 1 starts at 0 XP. Each successive level needs a bit more than the
    last (quadratic-ish curve): threshold(n) = 50 * (n-1) * n / ... kept simple.
    """
    if level <= 1:
        return 0
    # Sum of (75 * k) for k in 1..(level-1) => gentle ramp.
    n = level - 1
    return 75 * n * (n + 1) // 2


def level_from_xp(total_xp: int) -> int:
    """Highest level whose threshold is <= total_xp."""
    level = 1
    while xp_threshold(level + 1) <= total_xp:
        level += 1
        if level > 999:  # safety
            break
    return level


def level_title(level: int) -> str:
    if level <= 0:
        return LEVEL_TITLES[0]
    if level <= len(LEVEL_TITLES):
        return LEVEL_TITLES[level - 1]
    return LEVEL_TITLES[-1]


def level_progress(total_xp: int) -> dict:
    """Return a dict describing progress within the current level."""
    level = level_from_xp(total_xp)
    cur_floor = xp_threshold(level)
    next_floor = xp_threshold(level + 1)
    span = max(1, next_floor - cur_floor)
    into = total_xp - cur_floor
    return {
        "level": level,
        "title": level_title(level),
        "xp": total_xp,
        "level_floor": cur_floor,
        "next_level_xp": next_floor,
        "xp_into_level": into,
        "xp_needed_for_level": span,
        "percent": min(100, round(into / span * 100)),
        "xp_to_next": max(0, next_floor - total_xp),
    }


def streak_milestone_bonus(streak: int) -> int:
    """XP bonus if this streak value is a milestone, else 0."""
    return STREAK_MILESTONE_XP.get(streak, 0)


def compute_mission_xp(correct_count: int, gradeable_count: int,
                       streak: int, is_recovery: bool) -> dict:
    """Break down the XP earned for a completed mission."""
    breakdown = []
    total = XP_MISSION_COMPLETE
    breakdown.append({"label": "Mission complete", "xp": XP_MISSION_COMPLETE})

    correct_xp = correct_count * XP_PER_CORRECT
    if correct_xp:
        breakdown.append({"label": f"{correct_count} correct", "xp": correct_xp})
        total += correct_xp

    perfect = gradeable_count > 0 and correct_count == gradeable_count
    if perfect:
        breakdown.append({"label": "Perfect mission!", "xp": XP_PERFECT_BONUS})
        total += XP_PERFECT_BONUS

    if is_recovery:
        breakdown.append({"label": "Recovery bonus", "xp": XP_RECOVERY_BONUS})
        total += XP_RECOVERY_BONUS

    milestone_xp = streak_milestone_bonus(streak)
    if milestone_xp:
        breakdown.append({"label": f"{streak}-day streak!", "xp": milestone_xp})
        total += milestone_xp

    return {
        "total": total,
        "breakdown": breakdown,
        "perfect": perfect,
        "milestone": milestone_xp > 0,
    }
