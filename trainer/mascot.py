"""
Brain Quest — Mascot emotional-state system.

The mascot (a fox named by the child) reacts to performance and context.
It never shames mistakes — only encourages. Lines vary by time of day,
streak, and how the child is doing right now.

Pure functions: given context, return a {face, mood, line} payload the
templates/JS render.
"""
import random
from datetime import datetime

DEFAULT_NAME = "Foxy"
SPECIES_EMOJI = {
    "fox": "🦊", "owl": "🦉", "cat": "🐱", "dragon": "🐲",
    "panda": "🐼", "robot": "🤖", "unicorn": "🦄", "bunny": "🐰",
}

# Mood -> facial expression overlay (paired with the species emoji in UI)
MOOD_FACE = {
    "happy": "😊",
    "excited": "🤩",
    "celebrate": "🎉",
    "proud": "🥳",
    "encourage": "🤗",
    "thinking": "🤔",
    "sleepy": "😴",
    "neutral": "🙂",
}


def species_emoji(species: str) -> str:
    return SPECIES_EMOJI.get((species or "fox").lower(), "🦊")


def _time_part(now: datetime | None = None) -> str:
    h = (now or datetime.now()).hour
    if h < 12:
        return "morning"
    if h < 17:
        return "afternoon"
    if h < 21:
        return "evening"
    return "night"


def greet(name: str, streak: int = 0, completed_today: bool = False,
          now: datetime | None = None) -> dict:
    """Homepage / mission-intro greeting."""
    name = name or DEFAULT_NAME
    part = _time_part(now)
    hello = {
        "morning": "Good morning",
        "afternoon": "Good afternoon",
        "evening": "Good evening",
        "night": "Hey there",
    }[part]

    if completed_today:
        mood = "proud"
        lines = [
            f"{hello}! You already crushed today's quest. 🌟",
            f"{hello}! Mission done — you're on fire today! 🔥",
            f"{hello}! Come back tomorrow for a fresh quest. 💪",
        ]
    elif streak >= 3:
        mood = "excited"
        lines = [
            f"{hello}! Your {streak}-day streak is amazing — keep it going! 🔥",
            f"{hello}! {streak} days strong. Ready for today's quest? 🚀",
            f"{hello}! Don't break that {streak}-day streak — let's go! ⚡",
        ]
    elif part == "night":
        mood = "sleepy"
        lines = [
            f"{hello}! A quick quest before bed? You've got this. 🌙",
            f"{hello}! One short quest and you're a champion today. ✨",
        ]
    else:
        mood = "happy"
        lines = [
            f"{hello}! Ready to learn something new this {part}? 🚀",
            f"{hello}! Let's explore something exciting. ✨",
            f"{hello}! Today's quest is waiting for you. 🎯",
        ]
    return {"mood": mood, "face": MOOD_FACE[mood], "line": random.choice(lines)}


def react_to_answer(correct: bool, streak_in_mission: int = 0) -> dict:
    """In-mission reaction after a single item is answered."""
    if correct:
        mood = "celebrate" if streak_in_mission >= 2 else "happy"
        lines = [
            "Yes! Nailed it! 🎉",
            "You thought that through! 🌟",
            "Great strategy! 💡",
            "Correct! High five! 🙌",
        ]
        if streak_in_mission >= 2:
            lines = [
                f"{streak_in_mission} in a row! Your focus is paying off! 🔥",
                "On a roll! Keep going! 🚀",
                "Wow, you're building momentum! ⚡",
            ]
    else:
        mood = "encourage"
        lines = [
            "Close one! Mistakes help us learn. 🤗",
            "No worries — let's see why. You've got this! 💪",
            "Good try! Every quest makes you stronger. 🌱",
            "That's okay! The best learners make mistakes. 💛",
        ]
    return {"mood": mood, "face": MOOD_FACE[mood], "line": random.choice(lines)}


def react_to_summary(score: int, total: int, leveled_up: bool,
                     streak: int, new_milestone: bool) -> dict:
    """Mission-complete reaction on the summary screen."""
    if leveled_up:
        mood = "celebrate"
        line = "LEVEL UP! Your practice is paying off! 🎊"
    elif new_milestone:
        mood = "celebrate"
        line = f"{streak}-day streak milestone! You're a legend! 🏆"
    elif total > 0 and score == total:
        mood = "proud"
        line = "A perfect quest! Your effort really showed! 🥳"
    elif total > 0 and score >= total / 2:
        mood = "happy"
        line = "Great quest today! You're getting stronger! 🌟"
    else:
        mood = "encourage"
        line = "You finished — that's what counts! Tomorrow we get even better. 💪"
    return {"mood": mood, "face": MOOD_FACE[mood], "line": line}
