from random import shuffle, choice, sample

SPELLING_LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Expert']

# Real competition words (Scripps Spelling Bee style)
REAL_WORDS = {
    'Beginner': [
        'apple', 'bread', 'cat', 'dog', 'elephant', 'friend', 'garden', 'hello',
        'important', 'jacket', 'kitchen', 'lemon', 'monkey', 'number', 'orange',
        'pencil', 'quiet', 'rabbit', 'school', 'table', 'umbrella', 'violin', 'water'
    ],
    'Intermediate': [
        'accommodate', 'believe', 'calendar', 'debris', 'excellent', 'february',
        'grateful', 'happened', 'independent', 'jewelry', 'knowledge', 'library',
        'miscellaneous', 'neighbor', 'occurred', 'parliament', 'questionnaire',
        'receive', 'separate', 'tomorrow', 'unnecessary', 'vegetables', 'wednesday'
    ],
    'Advanced': [
        'abjure', 'bourgeois', 'chrysalis', 'deluge', 'equipment', 'fiasco',
        'gymnasium', 'hierarchy', 'iridescent', 'jonquil', 'kaleidoscope',
        'lieutenant', 'mischievous', 'onomatopoeia', 'poignant', 'queue',
        'reconnaissance', 'syllable', 'tyranny', 'ubiquitous', 'vengeance',
        'worcester', 'xeric', 'yacht', 'zealous'
    ],
    'Expert': [
        'aegis', 'antediluvian', 'bourgeoisie', 'camaraderie', 'discombobulate',
        'ecclesiastical', 'floccinaucinilicilification', 'gnathic', 'hutzpah',
        'inconsequential', 'juxtaposition', 'kinesiology', 'laissez-faire',
        'mahogany', 'naphtha', 'obsequious', 'perspicacious', 'qiviut', 'rambunctious',
        'serendipitous', 'tintinnabulation', 'uxorial', 'vicissitude', 'whilom',
        'xiphoid', 'yodeling', 'zephyr'
    ]
}

SPELLING_RULES = {
    'silent_letters': {
        'description': 'Letters that are spelled but not pronounced',
        'examples': ['knife', 'psychology', 'island', 'knight', 'wreck'],
        'explanation': 'These words have letters that appear in the spelling but are not heard when spoken.',
    },
    'double_consonants': {
        'description': 'When to use double consonants',
        'examples': ['rabbit', 'happy', 'letter', 'summer', 'beginning'],
        'explanation': 'Double consonants often appear after short vowels in one-syllable words or when doubling before adding suffixes.',
    },
    'silent_e': {
        'description': 'The silent e rule changes vowel sounds',
        'examples': ['home', 'make', 'use', 'hope', 'bike'],
        'explanation': 'A silent e at the end makes the vowel say its long sound.',
    },
    'ie_vs_ei': {
        'description': 'I before E except after C',
        'examples': ['believe', 'receive', 'ceiling', 'chief', 'weight'],
        'explanation': 'Usually use "ie" except after "c" or when "ei" sounds like "ay".',
    },
    'homophones': {
        'description': 'Words that sound the same but have different meanings',
        'examples': ['their/there/they\'re', 'to/too/two', 'right/write'],
        'explanation': 'Homophones sound identical but have different spellings and meanings.',
    },
    'suffix_y': {
        'description': 'Y to I conversion when adding suffixes',
        'examples': ['happy→happier', 'baby→babies', 'study→studied'],
        'explanation': 'When adding suffixes to words ending in consonant+y, change y to i.',
    },
    'etymology': {
        'description': 'Understanding word origins helps with spelling',
        'examples': ['psychology', 'orchestra', 'February', 'colonel'],
        'explanation': 'Many English words come from other languages, and knowing their origin helps explain their unusual spellings.',
    },
}

def get_spelling_words(level, count=10, rule_filter=None):
    """
    Get a random selection of words for a spelling level.

    Args:
        level: 'Beginner', 'Intermediate', 'Advanced', or 'Expert'
        count: Number of words to return
        rule_filter: Optional rule to filter words (advanced feature)

    Returns:
        List of words with metadata
    """
    if level not in REAL_WORDS:
        level = 'Beginner'

    words = REAL_WORDS[level]
    selected = sample(words, min(count, len(words)))

    return [
        {
            'word': w,
            'level': level,
            'hint': f'The word is "{w}". Try to spell it correctly.',
        }
        for w in selected
    ]

def get_word_metadata(word):
    """Get metadata about a word"""
    word_lower = word.lower()

    metadata = {
        'word': word,
        'length': len(word),
        'syllables': estimate_syllables(word),
    }

    # Determine difficulty level
    for level in SPELLING_LEVELS:
        if word_lower in [w.lower() for w in REAL_WORDS[level]]:
            metadata['level'] = level
            break

    return metadata

def estimate_syllables(word):
    """Rough estimate of syllable count"""
    vowels = 'aeiouy'
    syllable_count = 0
    previous_was_vowel = False

    for char in word.lower():
        is_vowel = char in vowels
        if is_vowel and not previous_was_vowel:
            syllable_count += 1
        previous_was_vowel = is_vowel

    if word.lower().endswith('e'):
        syllable_count -= 1
    if word.lower().endswith('le'):
        syllable_count += 1

    return max(1, syllable_count)


# Vocabulary words - everyday usage
VOCABULARY_WORDS = {
    'Beginner': [
        {'word': 'persevere', 'definition': 'To continue doing something despite difficulty', 'usage': 'She persevered through the difficult exam to achieve her goals.'},
        {'word': 'meticulous', 'definition': 'Very careful and precise about details', 'usage': 'The architect was meticulous in designing every aspect of the building.'},
        {'word': 'pragmatic', 'definition': 'Dealing with things in a practical way based on actual circumstances', 'usage': 'A pragmatic approach to solving problems is often the most effective.'},
        {'word': 'ephemeral', 'definition': 'Lasting for a very short time; temporary', 'usage': 'The beauty of cherry blossoms is ephemeral, lasting only a few weeks.'},
        {'word': 'nostalgia', 'definition': 'A sentimental longing for the past', 'usage': 'Listening to old songs fills me with nostalgia for my childhood.'},
        {'word': 'benign', 'definition': 'Gentle and kind; harmless', 'usage': 'The doctor assured us that the tumor was benign and not dangerous.'},
        {'word': 'vindicate', 'definition': 'To prove right or justify; to clear from blame', 'usage': 'The evidence helped vindicate the wrongly accused man.'},
        {'word': 'candid', 'definition': 'Honest and straightforward; frank', 'usage': 'She gave a candid opinion about the project without holding back.'},
        {'word': 'ubiquitous', 'definition': 'Present everywhere; widespread', 'usage': 'Smartphones have become ubiquitous in modern society.'},
        {'word': 'serendipity', 'definition': 'Finding something good by chance', 'usage': 'Meeting my best friend was pure serendipity at that coffee shop.'},
    ],
    'Intermediate': [
        {'word': 'eloquent', 'definition': 'Fluent and expressive in speech or writing', 'usage': 'The speaker delivered an eloquent speech that moved the audience.'},
        {'word': 'procrastinate', 'definition': 'To delay or postpone action unnecessarily', 'usage': 'Don\'t procrastinate on your assignments; start them early.'},
        {'word': 'resilient', 'definition': 'Able to recover quickly from difficulties', 'usage': 'Despite setbacks, she remained resilient and kept moving forward.'},
        {'word': 'meager', 'definition': 'Small in quantity and not enough; scanty', 'usage': 'The refugee camp had only meager supplies to distribute.'},
        {'word': 'pragmatism', 'definition': 'Dealing with things in a realistic, sensible way', 'usage': 'Her pragmatism helped her make sound business decisions.'},
        {'word': 'ambiguous', 'definition': 'Having more than one possible meaning or interpretation', 'usage': 'The instructions were ambiguous, causing confusion among the team.'},
        {'word': 'diligent', 'definition': 'Showing careful and persistent effort in work', 'usage': 'His diligent study habits earned him top grades in class.'},
        {'word': 'facilitate', 'definition': 'To make something easier or help it happen', 'usage': 'Technology helps facilitate communication across distances.'},
        {'word': 'meticulous', 'definition': 'Very careful and precise; paying attention to details', 'usage': 'A surgeon must be meticulous when performing delicate operations.'},
        {'word': 'tenacious', 'definition': 'Holding firmly to something; determined and persistent', 'usage': 'His tenacious attitude helped him achieve his dreams.'},
    ],
    'Advanced': [
        {'word': 'pragmatic', 'definition': 'Concerned with practical consequences; dealing realistically with things', 'usage': 'The government took a pragmatic approach to environmental policy.'},
        {'word': 'ephemeral', 'definition': 'Lasting for a very short time; transitory', 'usage': 'Internet fame is often ephemeral, lasting only days or weeks.'},
        {'word': 'obfuscate', 'definition': 'To deliberately make something unclear or confusing', 'usage': 'The company tried to obfuscate the facts about the scandal.'},
        {'word': 'perspicacious', 'definition': 'Having keen insight and understanding; perceptive', 'usage': 'Her perspicacious analysis of the market trends proved valuable.'},
        {'word': 'sycophant', 'definition': 'A person who acts obsequiously to gain favor', 'usage': 'The office sycophant constantly flattered the manager.'},
        {'word': 'ameliorate', 'definition': 'To make better or improve a bad situation', 'usage': 'New policies aim to ameliorate poverty in the region.'},
        {'word': 'contentious', 'definition': 'Causing or likely to cause heated debate; quarrelsome', 'usage': 'Healthcare policy remains a contentious issue in politics.'},
        {'word': 'sagacious', 'definition': 'Having sound judgment; wise and discerning', 'usage': 'His sagacious advice proved invaluable during the crisis.'},
        {'word': 'obsequious', 'definition': 'Obedient and excessively eager to please', 'usage': 'The waiter\'s obsequious manner made some customers uncomfortable.'},
        {'word': 'capricious', 'definition': 'Sudden and unaccountable changes of mood or behavior', 'usage': 'The capricious weather made outdoor planning difficult.'},
    ],
}


def get_vocabulary_words(level, count=3):
    """Get random vocabulary words for a level"""
    if level not in VOCABULARY_WORDS:
        level = 'Beginner'

    words = VOCABULARY_WORDS[level]
    selected = sample(words, min(count, len(words)))

    return selected
