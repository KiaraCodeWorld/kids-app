"""
LLM-backed content generators for Brain Quest datasets.

Each generator knows how to:
- load existing items from the relevant content module
- build a prompt that asks the LLM for new items in JSON format
- parse and validate the LLM response
- return only validated, non-duplicate items
"""

import json
import re
import time
from abc import ABC, abstractmethod
from typing import Any

from trainer.llm_service import get_llm_helper
from trainer import content_validator as validator


class ContentGenerator(ABC):
    """Base class for section-specific content generators."""

    def __init__(self, target: int = 100):
        self.target = target
        self.llm = get_llm_helper()

    def check_llm_health(self) -> tuple[bool, str]:
        """Make a tiny test call and report whether the LLM is reachable."""
        if not self.llm:
            return False, "OPENROUTER_API_KEY is not set or is empty."
        try:
            result = self.llm._call_llm('Reply with exactly: OK', max_tokens=10)
            if result and 'OK' in result:
                return True, "LLM is responding."
            if not result:
                return False, "LLM returned an empty response. This often means the API key is invalid or the model is unavailable."
            return False, f"LLM returned unexpected text: {result[:200]}"
        except Exception as e:
            return False, f"LLM call failed: {type(e).__name__}: {e}"

    @property
    @abstractmethod
    def section(self) -> str:
        pass

    @abstractmethod
    def current_count(self) -> int:
        """Return how many items already exist in this bucket."""
        pass

    @abstractmethod
    def existing_keys(self) -> set[str]:
        """Return the set of keys used for duplicate detection (words, IDs, etc.)."""
        pass

    @abstractmethod
    def build_prompt(self, batch_size: int, existing_keys: set[str]) -> str:
        """Build the LLM prompt for one batch."""
        pass

    @abstractmethod
    def parse_and_validate(self, raw: str, existing_keys: set[str]) -> tuple[list[dict], list[dict]]:
        """Return (valid_items, rejected_items_with_reasons)."""
        pass

    def gap(self) -> int:
        return max(0, self.target - self.current_count())

    def generate_batch(self, batch_size: int, existing_keys: set[str] | None = None) -> tuple[list[dict], list[dict], str]:
        """Generate one batch. Returns (valid, rejected, raw_response)."""
        if existing_keys is None:
            existing_keys = self.existing_keys()

        if not self.llm:
            raise RuntimeError(
                "OPENROUTER_API_KEY is not set. Cannot generate content via LLM."
            )

        prompt = self.build_prompt(batch_size, existing_keys)
        raw = self.llm._call_llm(prompt, max_tokens=self.max_tokens_for(batch_size))
        if not raw or not raw.strip():
            healthy, message = self.check_llm_health()
            if not healthy:
                raise RuntimeError(f"LLM is not available: {message}")
            return [], [{'error': 'LLM returned empty response for this batch'}], raw

        valid, rejected = self.parse_and_validate(raw, existing_keys)
        return valid, rejected, raw

    def max_tokens_for(self, batch_size: int) -> int:
        # Conservative estimate; increase for larger batches or longer items.
        return min(4000, max(500, batch_size * 250))

    def _extract_json(self, raw: str) -> list[dict]:
        """Extract a JSON array from LLM output, tolerating markdown fences."""
        raw = raw.strip()
        # If wrapped in ```json ... ```, strip it.
        if raw.startswith('```'):
            raw = re.sub(r'^```[a-zA-Z]*\n?', '', raw)
            raw = re.sub(r'\n?```$', '', raw)
            raw = raw.strip()

        # Sometimes the model returns the array directly; sometimes it is inside
        # explanatory text. Try to find the outermost JSON array.
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            pass

        # Find the first '[' and last ']'
        start = raw.find('[')
        end = raw.rfind(']')
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw[start:end + 1])
            except json.JSONDecodeError:
                pass

        # Try to find the first '{' and last '}' for a single object.
        start = raw.find('{')
        end = raw.rfind('}')
        if start != -1 and end != -1 and end > start:
            try:
                return [json.loads(raw[start:end + 1])]
            except json.JSONDecodeError:
                pass

        raise ValueError('Could not extract JSON array from LLM response')


class SpellingGenerator(ContentGenerator):
    """Generate REAL_WORDS entries for one spelling level."""

    def __init__(self, level: str, target: int = 100):
        super().__init__(target)
        if level not in ('Beginner', 'Intermediate', 'Advanced', 'Expert'):
            raise ValueError(f"Invalid spelling level: {level}")
        self.level = level
        from trainer import spelling_content
        self._module = spelling_content

    @property
    def section(self) -> str:
        return f"spelling/{self.level}"

    def current_count(self) -> int:
        return len(self._module.REAL_WORDS[self.level])

    def existing_keys(self) -> set[str]:
        all_words = set()
        for level_words in self._module.REAL_WORDS.values():
            all_words.update(w.lower() for w in level_words)
        return all_words

    def build_prompt(self, batch_size: int, existing_keys: set[str]) -> str:
        level_descriptions = {
            'Beginner': 'simple, common words (1-2 syllables) for ages 6-8',
            'Intermediate': 'tricky, commonly misspelled words (2-3 syllables) for ages 8-10',
            'Advanced': 'harder, less common words (3-4 syllables) for ages 10-12',
            'Expert': 'rare, complex competition-level words for ages 12+',
        }
        existing_sample = sorted(list(existing_keys))[:30]
        return f"""You are helping build a spelling-bee app for kids.

Generate {batch_size} NEW spelling words for the {self.level} level.
Level description: {level_descriptions[self.level]}.

Requirements:
- Return ONLY a JSON array of strings. Example: ["apple", "bread", "cat"]
- Do NOT include words already in use: {existing_sample}
- Words must be age-appropriate, correctly spelled, and free of offensive language.
- Prefer words with interesting phonetic patterns, double letters, silent letters, or common mistakes.

Return exactly {batch_size} words."""

    def parse_and_validate(self, raw: str, existing_keys: set[str]) -> tuple[list[dict], list[dict]]:
        data = self._extract_json(raw)
        valid = []
        rejected = []
        seen_in_batch = set()

        for idx, item in enumerate(data):
            if not isinstance(item, str):
                rejected.append({'index': idx, 'item': item, 'reason': 'not a string'})
                continue
            word = item.strip().lower()
            issues = validator.validate_spelling_word(word, existing_keys | seen_in_batch)
            if issues:
                rejected.append({'index': idx, 'item': item, 'reason': '; '.join(issues)})
            else:
                valid.append({'word': word})
                seen_in_batch.add(word)

        return valid, rejected


class VocabularyGenerator(ContentGenerator):
    """Generate VOCABULARY_WORDS entries for one level."""

    def __init__(self, level: str, target: int = 100):
        super().__init__(target)
        if level not in ('Beginner', 'Intermediate', 'Advanced'):
            raise ValueError(f"Invalid vocabulary level: {level}")
        self.level = level
        from trainer import spelling_content
        self._module = spelling_content

    @property
    def section(self) -> str:
        return f"vocabulary/{self.level}"

    def current_count(self) -> int:
        return len(self._module.VOCABULARY_WORDS[self.level])

    def existing_keys(self) -> set[str]:
        all_words = set()
        for level_words in self._module.VOCABULARY_WORDS.values():
            all_words.update(w['word'].lower() for w in level_words)
        return all_words

    def build_prompt(self, batch_size: int, existing_keys: set[str]) -> str:
        level_descriptions = {
            'Beginner': 'ages 6-8; simple, useful words they can use at school and home',
            'Intermediate': 'ages 8-10; descriptive and academic words for essays and conversations',
            'Advanced': 'ages 11-13; more sophisticated words for debates and deeper reading',
        }
        existing_sample = sorted(list(existing_keys))[:20]
        return f"""You are building a vocabulary app for kids.

Generate {batch_size} NEW vocabulary words for the {self.level} level.
Level description: {level_descriptions[self.level]}.

Requirements per word:
- "word": the vocabulary word (no duplicates with existing words: {existing_sample})
- "definition": a simple, child-friendly definition (1 sentence)
- "usage": a realistic example sentence from a kid's perspective that naturally uses the word

Return ONLY a JSON array of objects. Example:
[
  {{"word": "brave", "definition": "Ready to face danger or pain without fear", "usage": "The brave firefighter rescued the kitten."}}
]

Return exactly {batch_size} words. Do not use words already in use."""

    def parse_and_validate(self, raw: str, existing_keys: set[str]) -> tuple[list[dict], list[dict]]:
        data = self._extract_json(raw)
        valid = []
        rejected = []
        seen_in_batch = set()

        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                rejected.append({'index': idx, 'item': item, 'reason': 'not an object'})
                continue
            # Normalize word casing.
            if 'word' in item and isinstance(item['word'], str):
                item['word'] = item['word'].strip()
            issues = validator.validate_vocabulary_word(item, existing_keys | seen_in_batch)
            if issues:
                rejected.append({'index': idx, 'item': item, 'reason': '; '.join(issues)})
            else:
                valid.append(item)
                seen_in_batch.add(item['word'].lower())

        return valid, rejected


class DailyDiscoveryGenerator(ContentGenerator):
    """Generate Daily Discovery items for one category."""

    CATEGORY_PREFIXES = {
        'space': 'sp',
        'manners': 'mn',
        'funfact': 'ff',
        'hack': 'hk',
        'game': 'gm',
        'trending': 'tr',
        'news': 'nw',
    }

    CATEGORY_DESCRIPTIONS = {
        'space': 'amazing space and astronomy facts for curious kids',
        'manners': 'practical etiquette and social skills kids can use every day',
        'funfact': 'surprising science, animal, and history facts',
        'hack': 'quick 2-minute productivity, health, or study tips',
        'game': 'fun family or classroom games with clear rules',
        'trending': 'current trends in tech, culture, environment, or lifestyle',
        'news': 'kid-friendly news stories with what happened, why it matters, and what is next',
    }

    TAG_SUGGESTIONS = {
        'space': 'Science|Explorer|Mind-Bending|Wow',
        'manners': 'Life Skill|Social Intelligence|Everyday|Communication',
        'funfact': 'Animal Kingdom|History|Physics|Biology|Chemistry',
        'hack': 'Productivity|Health|Study Hack|Mental Health',
        'game': '2 Players|Brain Training|Team Game|Solo',
        'trending': 'Tech|Environment|Culture|Health Trend',
        'news': 'Science|Environment|Tech|Health|Youth Impact',
    }

    def __init__(self, category: str, target: int = 100):
        super().__init__(target)
        if category not in self.CATEGORY_PREFIXES:
            raise ValueError(f"Invalid daily discovery category: {category}")
        self.category = category
        from trainer import daily_discovery_content
        self._module = daily_discovery_content

    @property
    def section(self) -> str:
        return f"daily_discovery/{self.category}"

    def current_count(self) -> int:
        return len(self._module.CATEGORY_POOLS[self.category])

    def existing_keys(self) -> set[str]:
        return {item['id'] for item in self._module.CATEGORY_POOLS[self.category]}

    def _next_id(self, existing_keys: set[str]) -> str:
        prefix = self.CATEGORY_PREFIXES[self.category]
        numbers = []
        for key in existing_keys:
            if key.startswith(prefix):
                try:
                    numbers.append(int(key[len(prefix):]))
                except ValueError:
                    pass
        next_num = max(numbers, default=0) + 1
        return f"{prefix}{next_num:03d}"

    def build_prompt(self, batch_size: int, existing_keys: set[str]) -> str:
        desc = self.CATEGORY_DESCRIPTIONS[self.category]
        tag_examples = self.TAG_SUGGESTIONS[self.category]
        prefix = self.CATEGORY_PREFIXES[self.category]
        next_id = self._next_id(existing_keys)
        return f"""You are writing content for a kids' learning app called Brain Quest.

Generate {batch_size} NEW Daily Discovery items for the '{self.category}' category.
Category description: {desc}.

Requirements per item:
- "id": unique ID starting with '{prefix}' followed by a 3-digit number. Start with {next_id} and increment.
- "emoji": one single, relevant emoji
- "title": catchy, kid-friendly headline (5-8 words)
- "teaser": one intriguing sentence that hooks the reader
- "body": 3-5 sentences explaining the topic. Use simple words, bold key terms with **asterisks**, and make it engaging.
- "challenge": one actionable question or activity for the kid to try
- "tag": one short label like {tag_examples}

Do NOT reuse these existing IDs: {sorted(list(existing_keys))[:30]}

Return ONLY a JSON array of objects. Example:
[
  {{
    "id": "{next_id}",
    "emoji": "🚀",
    "title": "Rockets Use Stages to Save Fuel",
    "teaser": "A rocket drops parts of itself as it climbs higher.",
    "body": "Rockets are heavy because they carry so much fuel. To make climbing easier, they are built in **stages**. Each stage burns its fuel and then falls away, making the rocket lighter. This lets the remaining stages go faster and farther using less fuel.",
    "challenge": "Look up what happens to old rocket stages after they fall away.",
    "tag": "Space Tech"
  }}
]

Return exactly {batch_size} items."""

    def parse_and_validate(self, raw: str, existing_keys: set[str]) -> tuple[list[dict], list[dict]]:
        data = self._extract_json(raw)
        valid = []
        rejected = []
        seen_in_batch = set()

        for idx, item in enumerate(data):
            if not isinstance(item, dict):
                rejected.append({'index': idx, 'item': item, 'reason': 'not an object'})
                continue
            # Ensure category is set correctly.
            item['category'] = self.category
            issues = validator.validate_daily_discovery_item(item, existing_keys | seen_in_batch)
            if issues:
                rejected.append({'index': idx, 'item': item, 'reason': '; '.join(issues)})
            else:
                valid.append(item)
                seen_in_batch.add(item['id'])

        return valid, rejected
