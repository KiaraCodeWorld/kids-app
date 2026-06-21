from django.test import TestCase

from trainer import content_validator as validator


class ContentValidatorTests(TestCase):
    def test_validate_spelling_word_accepts_valid_word(self):
        issues = validator.validate_spelling_word('brave', {'apple'})
        self.assertEqual(issues, [])

    def test_validate_spelling_word_rejects_duplicate(self):
        issues = validator.validate_spelling_word('apple', {'apple'})
        self.assertIn('duplicate word: apple', issues)

    def test_validate_spelling_word_rejects_blocked_word(self):
        issues = validator.validate_spelling_word('stupid', set())
        self.assertIn('word blocked: stupid', issues)

    def test_validate_vocabulary_word_accepts_valid_item(self):
        item = {
            'word': 'brave',
            'definition': 'Ready to face danger',
            'usage': 'The brave child helped her friend.',
        }
        issues = validator.validate_vocabulary_word(item, set())
        self.assertEqual(issues, [])

    def test_validate_vocabulary_word_rejects_missing_usage(self):
        item = {'word': 'brave', 'definition': 'Ready to face danger'}
        issues = validator.validate_vocabulary_word(item, set())
        self.assertIn('missing keys: [\'usage\']', issues)

    def test_validate_daily_discovery_item_accepts_valid_item(self):
        item = {
            'id': 'sp021',
            'category': 'space',
            'emoji': '🚀',
            'title': 'Rockets Use Stages',
            'teaser': 'A hook sentence.',
            'body': 'Some engaging body text.',
            'challenge': 'Look this up.',
            'tag': 'Science',
        }
        issues = validator.validate_daily_discovery_item(item, set())
        self.assertEqual(issues, [])

    def test_validate_daily_discovery_item_rejects_wrong_prefix(self):
        item = {
            'id': 'mn021',
            'category': 'space',
            'emoji': '🚀',
            'title': 'Rockets Use Stages',
            'teaser': 'A hook sentence.',
            'body': 'Some engaging body text.',
            'challenge': 'Look this up.',
        }
        issues = validator.validate_daily_discovery_item(item, set())
        self.assertIn("id 'mn021' does not match category prefix sp", issues)
