"""
Brain Quest — Daily Mission engine.

Builds one mission per day: exactly 3 items across >=2 subjects.
  • Item 1 — reinforcement from the child's weak area (gradeable)
  • Item 2 — confidence builder from a strong area (gradeable)
  • Item 3 — fun item (a surprising fact or an idiom; learn-only)

Rules:
  • No item seen in the last 14 days repeats (caller passes seen_uids).
  • Difficulty adapts to the child's grade band.
  • The engine NEVER raises — build_daily_mission() always returns a valid
    3-item mission, falling back to a safe default if anything goes wrong.

Every item is normalized to a common shape:
  {
    uid, subject, subject_label, emoji, role, kind ('mcq'|'reveal'),
    title, prompt,
    choices: [{key, text}]   # mcq only
    answer_key,              # mcq only
    hint, explanation,       # mcq only
    body, fun_extra,         # reveal only
  }
"""
import random

from .math_challenge_content import get_all_questions, filter_questions
from .spelling_content import get_spelling_words, VOCABULARY_WORDS
from .word_explorer_content import WORD_TIERS, IDIOMS
from .daily_discovery_content import CATEGORY_POOLS

SUBJECT_META = {
    "math":       {"label": "Math",       "emoji": "🧮"},
    "vocabulary": {"label": "Vocabulary", "emoji": "📖"},
    "words":      {"label": "Words",      "emoji": "🗺️"},
    "spelling":   {"label": "Spelling",   "emoji": "🐝"},
    "idiom":      {"label": "Idiom",      "emoji": "🏝️"},
    "fact":       {"label": "Fun Fact",   "emoji": "🌟"},
}

GRADEABLE_SUBJECTS = ["math", "vocabulary", "words", "spelling"]


# ── grade → content-level bands ─────────────────────────────────────────────
def _band(grade: int) -> dict:
    if grade <= 2:
        return {"vocab": "Beginner", "spelling": "Beginner", "tier": "5-7"}
    if grade <= 4:
        return {"vocab": "Intermediate", "spelling": "Intermediate", "tier": "8-10"}
    return {"vocab": "Advanced", "spelling": "Advanced", "tier": "11-13"}


def _shuffled_choices(correct_text, distractor_texts, rng):
    """Build a 4-option MCQ; return (choices, answer_key)."""
    opts = [correct_text] + list(distractor_texts)
    rng.shuffle(opts)
    keys = ["A", "B", "C", "D", "E"]
    choices = [{"key": keys[i], "text": t} for i, t in enumerate(opts)]
    answer_key = next(c["key"] for c in choices if c["text"] == correct_text)
    return choices, answer_key


# ── per-subject item builders (each returns an item dict or None) ────────────
def _build_math(grade, seen, rng):
    pool = filter_questions(get_all_questions(), grade=grade) or get_all_questions()
    pool = [q for q in pool if q.get("type") == "mcq" and q.get("options")]
    rng.shuffle(pool)
    for q in pool:
        uid = f"math:{q['id']}"
        if uid in seen:
            continue
        opts = q["options"]
        choices = [{"key": k, "text": v} for k, v in opts.items()]
        return {
            "uid": uid, "subject": "math", "role": "",
            "subject_label": "Math", "emoji": "🧮", "kind": "mcq",
            "title": q.get("topic", "Math Challenge"),
            "prompt": q["question"],
            "choices": choices,
            "answer_key": q["answer"],
            "hint": q.get("hint", "Take it one step at a time!"),
            "explanation": " ".join(q.get("steps", [])) or q.get("key_concept", ""),
        }
    return None


def _build_vocabulary(grade, seen, rng):
    level = _band(grade)["vocab"]
    pool = VOCABULARY_WORDS.get(level) or VOCABULARY_WORDS.get("Beginner", [])
    all_words = [w for lst in VOCABULARY_WORDS.values() for w in lst]
    items = list(pool)
    rng.shuffle(items)
    for w in items:
        uid = f"vocab:{w['word']}"
        if uid in seen:
            continue
        distractors = rng.sample(
            [d["definition"] for d in all_words if d["word"] != w["word"]],
            k=min(3, max(1, len(all_words) - 1)),
        )
        choices, answer_key = _shuffled_choices(w["definition"], distractors, rng)
        return {
            "uid": uid, "subject": "vocabulary", "role": "",
            "subject_label": "Vocabulary", "emoji": "📖", "kind": "mcq",
            "title": f"What does “{w['word']}” mean?",
            "prompt": f"Choose the best meaning of the word **{w['word']}**.",
            "choices": choices,
            "answer_key": answer_key,
            "hint": "Think about how you'd use it in a sentence.",
            "explanation": f"**{w['word']}** means: {w['definition']} "
                           f"Example: {w.get('usage', '')}",
        }
    return None


def _build_words(grade, seen, rng):
    tier = _band(grade)["tier"]
    pool = WORD_TIERS.get(tier) or WORD_TIERS.get("8-10", [])
    all_words = [w for lst in WORD_TIERS.values() for w in lst]
    items = list(pool)
    rng.shuffle(items)
    for w in items:
        uid = f"word:{w['id']}"
        if uid in seen:
            continue
        distractors = rng.sample(
            [d["definition"] for d in all_words if d["id"] != w["id"]],
            k=min(3, max(1, len(all_words) - 1)),
        )
        choices, answer_key = _shuffled_choices(w["definition"], distractors, rng)
        return {
            "uid": uid, "subject": "words", "role": "",
            "subject_label": "Word Explorer", "emoji": "🗺️", "kind": "mcq",
            "title": f"{w['emoji']} What does “{w['word']}” mean?",
            "prompt": f"Pick the best meaning of **{w['word']}**.",
            "choices": choices,
            "answer_key": answer_key,
            "hint": f"You'll often hear it here: {w.get('context', '')}",
            "explanation": f"**{w['word']}** — {w['definition']} "
                           f"Example: “{w.get('example', '')}”",
        }
    return None


def _misspellings(word, rng):
    """Generate up to 3 plausible wrong spellings of a word."""
    word = word.lower()
    variants = set()
    vowels = "aeiou"
    swaps = {"ie": "ei", "ei": "ie", "c": "s", "s": "c", "ph": "f",
             "ous": "us", "able": "ible", "ible": "able", "tion": "shun"}
    # double a consonant
    for i, ch in enumerate(word):
        if ch not in vowels and 1 <= i < len(word) - 1:
            variants.add(word[:i] + ch + word[i:])
            break
    # drop a letter (not first)
    if len(word) > 4:
        i = rng.randint(2, len(word) - 2)
        variants.add(word[:i] + word[i + 1:])
    # rule swaps
    for a, b in swaps.items():
        if a in word:
            variants.add(word.replace(a, b, 1))
    # vowel swap
    for i, ch in enumerate(word):
        if ch in vowels:
            other = rng.choice([v for v in vowels if v != ch])
            variants.add(word[:i] + other + word[i + 1:])
            break
    variants.discard(word)
    out = [v for v in variants if v != word]
    rng.shuffle(out)
    return out[:3]


def _build_spelling(grade, seen, rng):
    level = _band(grade)["spelling"]
    words = get_spelling_words(level, count=20)
    rng.shuffle(words)
    for w in words:
        word = w["word"]
        uid = f"spelling:{word.lower()}"
        if uid in seen:
            continue
        wrong = _misspellings(word, rng)
        if len(wrong) < 3:
            continue
        choices, answer_key = _shuffled_choices(word, wrong[:3], rng)
        return {
            "uid": uid, "subject": "spelling", "role": "",
            "subject_label": "Spelling", "emoji": "🐝", "kind": "mcq",
            "title": "Pick the correct spelling",
            "prompt": "Which one is spelled correctly?",
            "choices": choices,
            "answer_key": answer_key,
            "hint": "Say it slowly, syllable by syllable.",
            "explanation": f"The correct spelling is **{word}**.",
        }
    return None


_BUILDERS = {
    "math": _build_math,
    "vocabulary": _build_vocabulary,
    "words": _build_words,
    "spelling": _build_spelling,
}


def _build_gradeable(subject, grade, seen, rng):
    """Try the requested subject, then fall back to any other gradeable one."""
    order = [subject] + [s for s in GRADEABLE_SUBJECTS if s != subject]
    for s in order:
        builder = _BUILDERS.get(s)
        if not builder:
            continue
        item = builder(grade, seen, rng)
        if item:
            return item
    return None


# ── fun item (idiom or fact) ────────────────────────────────────────────────
def _build_idiom(seen, rng):
    items = list(IDIOMS)
    rng.shuffle(items)
    for idi in items:
        uid = f"idiom:{idi['id']}"
        if uid in seen:
            continue
        return {
            "uid": uid, "subject": "idiom", "role": "fun",
            "subject_label": "Idiom Island", "emoji": "🏝️", "kind": "reveal",
            "title": f"{idi['emoji']} “{idi['phrase']}”",
            "prompt": f"People say **“{idi['phrase']}”** — but it doesn't "
                      f"mean what it sounds like!",
            "body": f"🖼️ Literally: {idi['literal']}\n\n"
                    f"✅ It really means: {idi['meaning']}\n\n"
                    f"💬 Example: “{idi['example']}”",
            "fun_extra": f"Challenge: try using “{idi['phrase']}” in a "
                         f"real conversation today!",
        }
    return None


def _build_fact(seen, rng):
    pool = [it for lst in CATEGORY_POOLS.values() for it in lst]
    rng.shuffle(pool)
    for it in pool:
        uid = f"fact:{it['id']}"
        if uid in seen:
            continue
        return {
            "uid": uid, "subject": "fact", "role": "fun",
            "subject_label": "Fun Fact", "emoji": it.get("emoji", "🌟"),
            "kind": "reveal",
            "title": f"{it.get('emoji', '🌟')} {it['title']}",
            "prompt": it.get("teaser", ""),
            "body": it.get("body", ""),
            "fun_extra": it.get("challenge", ""),
        }
    return None


def _build_fun(seen, rng):
    # alternate idiom / fact, but fall back to the other if exhausted
    first, second = ("idiom", "fact") if rng.random() < 0.5 else ("fact", "idiom")
    builders = {"idiom": _build_idiom, "fact": _build_fact}
    return builders[first](seen, rng) or builders[second](seen, rng)


# ── default / fallback mission ──────────────────────────────────────────────
def _default_mission(grade, rng):
    """A guaranteed-safe mission ignoring seen-history (used as last resort)."""
    items = []
    m = _build_math(grade, set(), rng)
    if m:
        items.append(m)
    v = _build_vocabulary(grade, set(), rng)
    if v:
        items.append(v)
    f = _build_fun(set(), rng)
    if f:
        items.append(f)
    return items


# ── public entry point ──────────────────────────────────────────────────────
def build_daily_mission(grade=4, weak_subject="math", strong_subject="vocabulary",
                        seen_uids=None, seed=None):
    """Build today's 3-item mission. Never raises."""
    rng = random.Random(seed)
    seen = set(seen_uids or [])
    grade = max(1, min(8, int(grade or 4)))

    try:
        used = set()
        items = []

        # Item 1 — reinforcement (weak area)
        i1 = _build_gradeable(weak_subject, grade, seen | used, rng)
        if i1:
            i1["role"] = "reinforce"
            items.append(i1)
            used.add(i1["uid"])

        # Item 2 — confidence builder (strong area, different subject if possible)
        strong = strong_subject if strong_subject != (i1 or {}).get("subject") else None
        if not strong:
            strong = next((s for s in GRADEABLE_SUBJECTS
                           if s != (i1 or {}).get("subject")), "vocabulary")
        i2 = _build_gradeable(strong, grade, seen | used, rng)
        if i2:
            i2["role"] = "confidence"
            items.append(i2)
            used.add(i2["uid"])

        # Item 3 — fun (fact or idiom)
        i3 = _build_fun(seen | used, rng)
        if i3:
            items.append(i3)
            used.add(i3["uid"])

        # Ensure exactly 3 items & >=2 subjects; backfill if needed
        if len(items) < 3:
            for s in GRADEABLE_SUBJECTS:
                if len(items) >= 3:
                    break
                extra = _build_gradeable(s, grade, seen | used, rng)
                if extra and extra["uid"] not in used:
                    extra["role"] = extra["role"] or "confidence"
                    items.append(extra)
                    used.add(extra["uid"])

        if len(items) < 3:
            # history exhausted — fall back to a default (allows repeats)
            items = _default_mission(grade, rng)

        return items[:3]
    except Exception:
        # absolute last resort
        try:
            return _default_mission(grade, rng)
        except Exception:
            return []


def gradeable_count(items) -> int:
    return sum(1 for it in items if it.get("kind") == "mcq")
