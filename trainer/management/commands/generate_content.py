"""
Management command: generate_content

LLM-backed pipeline for growing Brain Quest content datasets.

Examples:
    # Generate 20 Beginner spelling words, stage only
    python manage.py generate_content --section spelling --level Beginner --batch 20

    # Generate until Advanced vocabulary reaches 100 items
    python manage.py generate_content --section vocabulary --level Advanced --target 100

    # Generate 5 Daily Discovery space items and merge into source file
    python manage.py generate_content --section daily_discovery --category space --batch 5 --merge

    # Preview only
    python manage.py generate_content --section spelling --level Intermediate --target 100 --dry-run
"""

import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from trainer.content_generator import (
    ContentGenerator,
    SpellingGenerator,
    VocabularyGenerator,
    DailyDiscoveryGenerator,
)

def get_project_root() -> Path:
    return Path(settings.BASE_DIR)


def get_data_generated_dir() -> Path:
    return get_project_root() / 'data' / 'generated'

GENERATORS = {
    ('spelling', None): SpellingGenerator,
    ('vocabulary', None): VocabularyGenerator,
    ('daily_discovery', None): DailyDiscoveryGenerator,
}

CATEGORY_TO_LEVEL_ARG = {
    'spelling': 'level',
    'vocabulary': 'level',
    'daily_discovery': 'category',
}

LEVELS = {
    'spelling': ['Beginner', 'Intermediate', 'Advanced', 'Expert'],
    'vocabulary': ['Beginner', 'Intermediate', 'Advanced'],
}

CATEGORIES = [
    'space', 'manners', 'funfact', 'hack', 'game', 'trending', 'news'
]


class Command(BaseCommand):
    help = 'Generate new content for Brain Quest sections using an LLM.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--section',
            required=True,
            choices=['spelling', 'vocabulary', 'daily_discovery'],
            help='Which content section to grow.',
        )
        parser.add_argument(
            '--level',
            choices=LEVELS['spelling'] + LEVELS['vocabulary'],
            help='Spelling or vocabulary level.',
        )
        parser.add_argument(
            '--category',
            choices=CATEGORIES,
            help='Daily Discovery category.',
        )
        parser.add_argument(
            '--target',
            type=int,
            default=100,
            help='Total target number of items in this bucket (default: 100).',
        )
        parser.add_argument(
            '--batch',
            type=int,
            default=20,
            help='Number of items to ask the LLM for per call (default: 20).',
        )
        parser.add_argument(
            '--max-calls',
            type=int,
            default=20,
            help='Maximum LLM calls to make (safety limit, default: 20).',
        )
        parser.add_argument(
            '--merge',
            action='store_true',
            help='Append validated generated items to the source Python file.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show gap and sample prompt but do not call LLM or write files.',
        )
        parser.add_argument(
            '--sleep',
            type=float,
            default=1.0,
            help='Seconds to sleep between LLM calls (default: 1.0).',
        )
        parser.add_argument(
            '--sample',
            action='store_true',
            help='Use deterministic sample data instead of calling the LLM (for testing the pipeline).',
        )

    def handle(self, *args, **options):
        section = options['section']
        target = options['target']
        batch = options['batch']
        merge = options['merge']
        dry_run = options['dry_run']
        max_calls = options['max_calls']
        sleep_seconds = options['sleep']
        use_sample = options['sample']

        # Validate level/category for the chosen section.
        if section in ('spelling', 'vocabulary'):
            level = options['level']
            if not level:
                raise CommandError(f"--level is required for section '{section}'")
            generator = SpellingGenerator(level, target) if section == 'spelling' else VocabularyGenerator(level, target)
        else:
            category = options['category']
            if not category:
                raise CommandError("--category is required for section 'daily_discovery'")
            generator = DailyDiscoveryGenerator(category, target)

        self.stdout.write(self.style.NOTICE(f"Section: {generator.section}"))
        self.stdout.write(f"Current count: {generator.current_count()}")
        self.stdout.write(f"Target: {target}")
        self.stdout.write(f"Gap: {generator.gap()}")

        if generator.gap() == 0:
            self.stdout.write(self.style.SUCCESS("Target already reached. Nothing to do."))
            return

        if dry_run:
            prompt = generator.build_prompt(min(batch, generator.gap()), generator.existing_keys())
            self.stdout.write(self.style.NOTICE("\n--- SAMPLE PROMPT ---"))
            try:
                self.stdout.write(prompt[:2000])
            except UnicodeEncodeError:
                # Some terminals cannot print emojis; show an ASCII-safe version.
                self.stdout.write(prompt[:2000].encode('ascii', 'replace').decode('ascii'))
            self.stdout.write(self.style.NOTICE("--- END SAMPLE ---\n"))
            self.stdout.write(self.style.SUCCESS("Dry run complete. No LLM calls made."))
            return

        if use_sample:
            self.stdout.write(self.style.WARNING("SAMPLE MODE: using deterministic sample data, not LLM."))

        # Collect generated items across batches.
        all_valid = []
        all_rejected = []
        existing_keys = generator.existing_keys()
        calls_made = 0

        while len(all_valid) < generator.gap() and calls_made < max_calls:
            remaining = generator.gap() - len(all_valid)
            current_batch = min(batch, remaining)

            if use_sample:
                self.stdout.write(f"\nSample batch {calls_made + 1}/{max_calls}: generating {current_batch} items...")
                valid, rejected = self._sample_batch(section, generator, current_batch, existing_keys)
                raw = ''
            else:
                self.stdout.write(f"\nLLM call {calls_made + 1}/{max_calls}: requesting {current_batch} items...")
                try:
                    valid, rejected, raw = generator.generate_batch(current_batch, existing_keys)
                except RuntimeError as e:
                    raise CommandError(str(e))

            calls_made += 1
            all_valid.extend(valid)
            all_rejected.extend(rejected)

            # Update keys so later batches avoid duplicates.
            for item in valid:
                if section == 'spelling':
                    existing_keys.add(item['word'].lower())
                elif section == 'vocabulary':
                    existing_keys.add(item['word'].lower())
                else:
                    existing_keys.add(item['id'])

            self.stdout.write(f"  Accepted: {len(valid)} | Rejected: {len(rejected)} | Total accepted: {len(all_valid)}")

            if sleep_seconds and calls_made < max_calls and len(all_valid) < generator.gap():
                import time
                time.sleep(sleep_seconds)

        # We may have generated more than needed because a batch returned extras.
        needed = generator.gap()
        selected = all_valid[:needed]
        overflow = all_valid[needed:]

        # Save staging file.
        DATA_GENERATED_DIR = get_data_generated_dir()
        DATA_GENERATED_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_section = generator.section.replace('/', '_')
        staging_path = DATA_GENERATED_DIR / f"{safe_section}_{timestamp}.json"

        staging_data = {
            'section': generator.section,
            'target': target,
            'current_before': generator.current_count(),
            'generated_valid': len(all_valid),
            'selected_for_merge': len(selected),
            'rejected': len(all_rejected),
            'llm_calls': calls_made,
            'generated_at': datetime.now().isoformat(),
            'valid': all_valid,
            'rejected': all_rejected,
        }
        staging_path.write_text(json.dumps(staging_data, indent=2, ensure_ascii=False), encoding='utf-8')
        self.stdout.write(self.style.NOTICE(f"\nStaging file saved: {staging_path}"))

        if merge:
            self._merge(selected, section, generator)
            self.stdout.write(self.style.SUCCESS(f"Merged {len(selected)} items into source file."))
        else:
            self.stdout.write(self.style.WARNING(
                "Items are staged but NOT merged. Review the staging file, then re-run with --merge."
            ))

        if overflow:
            self.stdout.write(self.style.NOTICE(f"{len(overflow)} extra valid items were generated but not merged (exceeds target)."))

        if all_rejected:
            self.stdout.write(self.style.NOTICE(f"{len(all_rejected)} items were rejected. See staging file for details."))

    def _sample_batch(self, section: str, generator: ContentGenerator, batch_size: int, existing_keys: set) -> tuple[list[dict], list[dict]]:
        """Generate deterministic sample items for pipeline testing."""
        valid = []
        rejected = []
        if section == 'spelling':
            base = ['alpha', 'bliss', 'crisp', 'drift', 'eagle', 'flame', 'grape', 'haste', 'igloo', 'jolly']
            for i in range(batch_size):
                word = f"sample{i+1:02d}"
                # Try to make words look real if possible.
                word = base[i % len(base)] + (f"{i//len(base)}" if i >= len(base) else "")
                issues = []  # validator.validate_spelling_word(word, existing_keys)
                if issues:
                    rejected.append({'item': word, 'reason': '; '.join(issues)})
                else:
                    valid.append({'word': word.lower()})
                    existing_keys.add(word.lower())
        elif section == 'vocabulary':
            for i in range(batch_size):
                word = f"sampleword{i+1}"
                item = {
                    'word': word,
                    'definition': f'A friendly word used for testing pipeline number {i+1}.',
                    'usage': f'The student used the word {word} in a practice sentence.',
                }
                valid.append(item)
                existing_keys.add(word.lower())
        elif section == 'daily_discovery':
            prefix_map = {
                'space': 'sp', 'manners': 'mn', 'funfact': 'ff', 'hack': 'hk',
                'game': 'gm', 'trending': 'tr', 'news': 'nw',
            }
            cat = generator.category
            prefix = prefix_map[cat]
            numbers = [int(k[len(prefix):]) for k in existing_keys if k.startswith(prefix) and k[len(prefix):].isdigit()]
            start = max(numbers, default=0) + 1
            for i in range(batch_size):
                num = start + i
                item = {
                    'id': f"{prefix}{num:03d}",
                    'category': cat,
                    'emoji': '🌟',
                    'title': f'Sample Discovery Item {num}',
                    'teaser': f'This is a sample teaser for {cat} item {num}.',
                    'body': f'This is the body of a sample {cat} item used to test the generation pipeline. **Bold text** is supported.',
                    'challenge': f'Try researching more about {cat} item {num}.',
                    'tag': 'Sample',
                }
                valid.append(item)
                existing_keys.add(item['id'])
        return valid, rejected

    def _merge(self, items: list[dict], section: str, generator: ContentGenerator):
        """Append validated items to the source Python file."""
        if section == 'spelling':
            self._merge_spelling(items, generator.level)
        elif section == 'vocabulary':
            self._merge_vocabulary(items, generator.level)
        elif section == 'daily_discovery':
            self._merge_daily_discovery(items, generator.category)

    def _backup(self, path: Path):
        backup_path = path.with_suffix(path.suffix + '.bak')
        shutil.copy2(path, backup_path)
        self.stdout.write(self.style.NOTICE(f"Backup created: {backup_path}"))

    def _find_assignment_region(self, text: str, name: str) -> tuple[int, int]:
        """Return (start, end) indices of a top-level assignment `name = ...`."""
        import ast
        tree = ast.parse(text)
        for node in tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == name:
                        return node.lineno - 1, node.end_lineno
        raise CommandError(f"Could not find assignment '{name}' in source file")

    def _merge_spelling(self, items: list[dict], level: str):
        path = get_project_root() / 'trainer' / 'spelling_content.py'
        self._backup(path)
        text = path.read_text(encoding='utf-8')

        start_line, end_line = self._find_assignment_region(text, 'REAL_WORDS')
        lines = text.splitlines(keepends=True)
        region = ''.join(lines[start_line:end_line])

        pattern = rf"(    '{re.escape(level)}': \[\n)(.*?)(\n    \],)"
        match = re.search(pattern, region, re.DOTALL)
        if not match:
            raise CommandError(f"Could not find spelling list for level '{level}'")

        existing_body = match.group(2).rstrip()
        if existing_body and not existing_body.endswith(','):
            existing_body += ','

        new_words = ",\n        ".join(f"'{item['word']}'" for item in items)
        insert = f"\n        {new_words}"
        new_region = region[:match.start(2)] + existing_body + insert + region[match.end(2):]

        lines[start_line:end_line] = [new_region]
        path.write_text(''.join(lines), encoding='utf-8')

    def _merge_vocabulary(self, items: list[dict], level: str):
        path = get_project_root() / 'trainer' / 'spelling_content.py'
        self._backup(path)
        text = path.read_text(encoding='utf-8')

        start_line, end_line = self._find_assignment_region(text, 'VOCABULARY_WORDS')
        lines = text.splitlines(keepends=True)
        region = ''.join(lines[start_line:end_line])

        pattern = rf"(    '{re.escape(level)}': \[\n)(.*?)(\n    \],)"
        match = re.search(pattern, region, re.DOTALL)
        if not match:
            raise CommandError(f"Could not find vocabulary list for level '{level}'")

        existing_body = match.group(2).rstrip()
        if existing_body and not existing_body.endswith(','):
            existing_body += ','

        new_entries = []
        for item in items:
            entry = (
                f"{{'word': {repr(item['word'])}, "
                f"'definition': {repr(item['definition'])}, "
                f"'usage': {repr(item['usage'])}}}"
            )
            new_entries.append(entry)

        insert = ",\n        ".join(new_entries)
        new_region = region[:match.start(2)] + existing_body + f"\n        {insert}" + region[match.end(2):]

        lines[start_line:end_line] = [new_region]
        path.write_text(''.join(lines), encoding='utf-8')

    def _merge_daily_discovery(self, items: list[dict], category: str):
        path = get_project_root() / 'trainer' / 'daily_discovery_content.py'
        self._backup(path)
        text = path.read_text(encoding='utf-8')

        list_name = category.upper()
        if category == 'funfact':
            list_name = 'FUNFACTS'
        elif category == 'news':
            list_name = 'NEWS'

        start_line, end_line = self._find_assignment_region(text, list_name)
        lines = text.splitlines(keepends=True)
        region = ''.join(lines[start_line:end_line])

        # The list ends with a top-level `]`.
        pattern = rf"({re.escape(list_name)} = \[\n)(.*?)(\n\])"
        match = re.search(pattern, region, re.DOTALL)
        if not match:
            raise CommandError(f"Could not find daily discovery list '{list_name}'")

        existing_body = match.group(2).rstrip()
        if existing_body and not existing_body.endswith(','):
            existing_body += ','

        new_entries = []
        for item in items:
            entry = (
                f"_d({repr(item['id'])},{repr(item['category'])},{repr(item['emoji'])},"
                f"{repr(item['title'])},\n   {repr(item['teaser'])},\n   {repr(item['body'])},\n   "
                f"{repr(item['challenge'])},{repr(item.get('tag', ''))}),"
            )
            new_entries.append(entry)

        insert = "\n\n".join(new_entries)
        new_region = region[:match.end(2)] + f"\n\n{insert}" + region[match.end(2):]

        lines[start_line:end_line] = [new_region]
        path.write_text(''.join(lines), encoding='utf-8')
