"""
Validation utilities for LLM-generated content.

Each validator returns a list of issue strings; an empty list means the item is valid.
"""

import re
from typing import Any


# Very basic blocklist for obviously inappropriate content.
# Expand as needed; this is a safety net, not a full content filter.
BLOCKLIST = {
    'damn', 'hell', 'crap', 'stupid', 'idiot', 'hate', 'kill', 'dead', 'sex',
    'drugs', 'alcohol', 'beer', 'wine', 'vodka', 'gun', 'violence', 'suicide',
}


def _has_blocklist(text: str) -> bool:
    if not text:
        return False
    words = re.findall(r"[a-zA-Z']+", text.lower())
    return any(word in BLOCKLIST for word in words)


def _is_single_emoji(value: str) -> bool:
    """Best-effort check that value is one emoji/grapheme cluster."""
    if not isinstance(value, str):
        return False
    # Strip variation selectors and zero-width joiners, then count graphemes.
    cleaned = value.replace('\u200d', '').replace('\ufe0f', '').replace('\u200c', '')
    return len(cleaned) == 1 and cleaned.strip()


def validate_spelling_word(word: str, existing_words: set[str]) -> list[str]:
    issues = []
    if not isinstance(word, str) or not word.strip():
        issues.append('word is empty')
        return issues
    word = word.strip().lower()
    if not re.fullmatch(r"[a-zA-Z'\-]+", word):
        issues.append(f'word contains invalid characters: {word!r}')
    if word in existing_words:
        issues.append(f'duplicate word: {word}')
    if len(word) < 2:
        issues.append(f'word too short: {word}')
    if _has_blocklist(word):
        issues.append(f'word blocked: {word}')
    return issues


def validate_vocabulary_word(item: dict[str, Any], existing_words: set[str]) -> list[str]:
    issues = []
    required = {'word', 'definition', 'usage'}
    missing = required - set(item.keys())
    if missing:
        issues.append(f'missing keys: {sorted(missing)}')
        return issues

    word = str(item['word']).strip()
    definition = str(item['definition']).strip()
    usage = str(item['usage']).strip()

    if not word:
        issues.append('word is empty')
    elif word.lower() in existing_words:
        issues.append(f'duplicate word: {word}')

    if not definition:
        issues.append('definition is empty')
    elif len(definition) > 300:
        issues.append('definition is too long (>300 chars)')

    if not usage:
        issues.append('usage is empty')
    elif word.lower() not in usage.lower():
        issues.append(f'usage sentence does not contain the word: {word}')

    for text in (word, definition, usage):
        if _has_blocklist(text):
            issues.append('content contains blocked words')
            break

    return issues


def validate_daily_discovery_item(item: dict[str, Any], existing_ids: set[str]) -> list[str]:
    issues = []
    required = {'id', 'category', 'emoji', 'title', 'teaser', 'body', 'challenge'}
    missing = required - set(item.keys())
    if missing:
        issues.append(f'missing keys: {sorted(missing)}')
        return issues

    item_id = str(item['id']).strip()
    category = str(item['category']).strip()
    emoji = str(item['emoji']).strip()
    title = str(item['title']).strip()
    teaser = str(item['teaser']).strip()
    body = str(item['body']).strip()
    challenge = str(item['challenge']).strip()

    if not item_id:
        issues.append('id is empty')
    elif item_id in existing_ids:
        issues.append(f'duplicate id: {item_id}')

    prefix_map = {
        'space': 'sp',
        'manners': 'mn',
        'funfact': 'ff',
        'hack': 'hk',
        'game': 'gm',
        'trending': 'tr',
        'news': 'nw',
    }
    expected_prefix = prefix_map.get(category)
    if expected_prefix and item_id and not item_id.startswith(expected_prefix):
        issues.append(f'id {item_id!r} does not match category prefix {expected_prefix}')

    if not category:
        issues.append('category is empty')

    if not emoji:
        issues.append('emoji is empty')
    elif not _is_single_emoji(emoji):
        issues.append(f'emoji should be a single emoji: {emoji!r}')

    for field, value in [('title', title), ('teaser', teaser), ('body', body), ('challenge', challenge)]:
        if not value.strip():
            issues.append(f'{field} is empty')

    for text in (title, teaser, body, challenge):
        if _has_blocklist(text):
            issues.append('content contains blocked words')
            break

    return issues
