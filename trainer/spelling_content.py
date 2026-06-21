from random import shuffle, choice, sample

SPELLING_LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Expert']

# Real competition words (Scripps Spelling Bee style)
REAL_WORDS = {
    'Beginner': [
        'apple', 'bread', 'cat', 'dog', 'elephant', 'friend', 'garden', 'hello',
        'important', 'jacket', 'kitchen', 'lemon', 'monkey', 'number', 'orange',
        'pencil', 'quiet', 'rabbit', 'school', 'table', 'umbrella', 'violin', 'water',
        'family', 'happy', 'summer', 'winter', 'spring', 'yellow', 'purple', 'green',
        'window', 'doctor', 'bottle', 'button', 'cookie', 'dinner', 'flower', 'guitar',
        'honest', 'island', 'laughter', 'market', 'picnic', 'planet', 'puzzle', 'rocket',
        'shadow', 'soccer', 'theater', 'vacation', 'weather', 'whisper'
    ],
    'Intermediate': [
        'accommodate', 'believe', 'calendar', 'debris', 'excellent', 'february',
        'grateful', 'happened', 'independent', 'jewelry', 'knowledge', 'library',
        'miscellaneous', 'neighbor', 'occurred', 'parliament', 'questionnaire',
        'receive', 'separate', 'tomorrow', 'unnecessary', 'vegetables', 'wednesday',
        'absence', 'achievement', 'appreciate', 'assignment', 'atmosphere', 'bicycle',
        'brilliant', 'cafeteria', 'courageous', 'curiosity', 'definitely', 'dictionary',
        'embarrass', 'environment', 'exercise', 'experience', 'frequently', 'generous',
        'government', 'hospital', 'imagine', 'incredible', 'invitation',
        'laboratory', 'maintain', 'mortgage', 'necessary', 'occasion', 'paragraph',
        'particularly', 'possible', 'preparation', 'pronunciation', 'remember', 'restaurant',
        'schedule', 'situation', 'successful', 'surprise', 'technology', 'temperature',
        'throughout', 'university', 'village', 'volunteer'
    ],
    'Advanced': [
        'abjure', 'bourgeois', 'chrysalis', 'deluge', 'equipment', 'fiasco',
        'gymnasium', 'hierarchy', 'iridescent', 'jonquil', 'kaleidoscope',
        'lieutenant', 'mischievous', 'onomatopoeia', 'poignant', 'queue',
        'reconnaissance', 'syllable', 'tyranny', 'ubiquitous', 'vengeance',
        'worcester', 'xeric', 'yacht', 'zealous',
        'algorithm', 'amateur', 'analyze', 'apparatus', 'arithmetic', 'asterisk',
        'barometer', 'camouflage', 'catastrophe', 'chronicle', 'committee', 'conscience',
        'controversy', 'deduction', 'dilemma', 'discipline', 'ecosystem', 'eloquent',
        'entrepreneur', 'evolution', 'extraordinary', 'flabbergasted', 'fluorescent',
        'formidable', 'guarantee', 'hieroglyph', 'hypothesis', 'illuminate', 'influenza',
        'infrastructure', 'jurisdiction', 'laboratory', 'labyrinth', 'metamorphosis',
        'nauseous', 'necessary', 'nuisance', 'occurrence', 'parachute', 'parliament',
        'phenomenon', 'photosynthesis', 'pneumonia', 'prejudice', 'pronunciation',
        'renaissance', 'reservoir', 'rhinoceros', 'rhythm', 'sacrifice', 'statistics',
        'subterranean', 'suffrage', 'symphony', 'temperature', 'vocabulary', 'vulnerable'
    ],
    'Expert': [
        'aegis', 'antediluvian', 'bourgeoisie', 'camaraderie', 'discombobulate',
        'ecclesiastical', 'floccinaucinilicilification', 'gnathic', 'hutzpah',
        'inconsequential', 'juxtaposition', 'kinesiology', 'laissez-faire',
        'mahogany', 'naphtha', 'obsequious', 'perspicacious', 'qiviut', 'rambunctious',
        'serendipitous', 'tintinnabulation', 'uxorial', 'vicissitude', 'whilom',
        'xiphoid', 'yodeling', 'zephyr',
        'abecedarian', 'absquatulate', 'alfresco', 'antebellum', 'argosy', 'badinage',
        'braggadocio', 'callipygian', 'canoodle', 'catercorner', 'collywobbles', 'concupiscence',
        'defenestration', 'doppelganger', 'effervescent', 'epistemology', 'equinox', 'euonym',
        'floccinaucinihilipilification', 'gobbledygook', 'hagiography', 'harrumph', 'heliolatry',
        'hippopotomonstrosesquippedaliophobia', 'ichthyology', 'jackanapes', 'juggernaut',
        'kakistocracy', 'kerfuffle', 'lackadaisical', 'lollygag', 'magniloquent', 'maverick',
        'mnemonic', 'nudiustertian', 'obfuscate', 'peregrination', 'pulchritude', 'quixotic',
        'rapscallion', 'schadenfreude', 'sesquipedalian', 'skedaddle', 'snollygoster',
        'spaghettification', 'stultify', 'supercilious', 'tatterdemalion', 'triskaidekaphobia',
        'ulculation', 'umbrage', 'verisimilitude', 'whippersnapper', 'widdershins', 'xenolith'
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
        {'word': 'brave', 'definition': 'Ready to face danger or pain without fear', 'usage': 'The brave firefighter rescued the kitten from the tall tree.'},
        {'word': 'curious', 'definition': 'Eager to learn or know more', 'usage': 'The curious child asked why the sky looks blue.'},
        {'word': 'grateful', 'definition': 'Feeling thankful and appreciative', 'usage': 'I am grateful for my family and a warm dinner every night.'},
        {'word': 'honest', 'definition': 'Telling the truth and not cheating', 'usage': 'She was honest about breaking the cup and apologized right away.'},
        {'word': 'patient', 'definition': 'Able to wait calmly without getting annoyed', 'usage': 'The patient teacher explained the problem three times.'},
        {'word': 'responsible', 'definition': 'Reliable and able to be trusted to do the right thing', 'usage': 'He is responsible enough to feed the dog every morning.'},
        {'word': 'generous', 'definition': 'Happy to give more than is usual or expected', 'usage': 'My generous neighbor shared cookies with everyone on the street.'},
        {'word': 'thoughtful', 'definition': 'Showing care and consideration for others', 'usage': 'It was thoughtful of you to bring me water after the game.'},
        {'word': 'determined', 'definition': 'Having made a firm decision and not giving up', 'usage': 'The determined runner finished the race even after falling down.'},
        {'word': 'creative', 'definition': 'Using imagination to make or think of new things', 'usage': 'She found a creative way to organize her bookshelf.'},
        {'word': 'confident', 'definition': 'Feeling sure about yourself and your abilities', 'usage': 'He felt confident speaking in front of the class after practicing.'},
        {'word': 'encourage', 'definition': 'To give support, confidence, or hope to someone', 'usage': 'My coach encouraged me to keep trying even when I missed the goal.'},
        {'word': 'include', 'definition': 'To make someone part of a group or activity', 'usage': 'Please include the new student in your group project.'},
        {'word': 'observe', 'definition': 'To watch carefully and notice details', 'usage': 'Scientists observe plants to learn how they grow.'},
        {'word': 'predict', 'definition': 'To say what you think will happen in the future', 'usage': 'I predict it will rain because the sky is dark and gray.'},
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
        {'word': 'brainstorm', 'definition': 'To think of many ideas quickly as a group', 'usage': 'Let us brainstorm ideas for the school science fair project.'},
        {'word': 'compromise', 'definition': 'To settle a disagreement by each side giving up something', 'usage': 'They compromised by choosing pizza one night and tacos the next.'},
        {'word': 'evaluate', 'definition': 'To judge the value or quality of something', 'usage': 'Teachers evaluate student work to give helpful feedback.'},
        {'word': 'illustrate', 'definition': 'To explain or make clear by using examples or pictures', 'usage': 'She used a diagram to illustrate how the water cycle works.'},
        {'word': 'summarize', 'definition': 'To give a brief statement of the main points', 'usage': 'Please summarize the story in three sentences.'},
        {'word': 'elaborate', 'definition': 'To add more detail or information', 'usage': 'Can you elaborate on why you chose that answer?'},
        {'word': 'hesitate', 'definition': 'To pause before doing or saying something', 'usage': 'Do not hesitate to ask for help if you are stuck.'},
        {'word': 'contribute', 'definition': 'To give something to help a person or cause', 'usage': 'Everyone contributed snacks for the class party.'},
        {'word': 'demonstrate', 'definition': 'To show clearly how something works or is done', 'usage': 'The chef will demonstrate how to make sushi rolls.'},
        {'word': 'maintain', 'definition': 'To keep something in good condition', 'usage': 'It is important to maintain your bicycle by oiling the chain.'},
        {'word': 'negotiate', 'definition': 'To discuss something to reach an agreement', 'usage': 'The kids negotiated who would choose the movie.'},
        {'word': 'prioritize', 'definition': 'To decide which tasks are most important and do those first', 'usage': 'I prioritize homework before playing video games.'},
        {'word': 'recommend', 'definition': 'To suggest that someone do or use something', 'usage': 'I recommend this book because the mystery is exciting.'},
        {'word': 'reinforce', 'definition': 'To strengthen or support an idea or behavior', 'usage': 'Practicing every day reinforces good piano skills.'},
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
        {'word': 'altruistic', 'definition': 'Showing unselfish concern for the well-being of others', 'usage': 'Her altruistic volunteer work helped hundreds of families.'},
        {'word': 'benevolent', 'definition': 'Well meaning and kindly; showing goodwill', 'usage': 'The benevolent donor gave books to every classroom.'},
        {'word': 'candid', 'definition': 'Honest and straightforward in speaking or writing', 'usage': 'His candid feedback helped me improve my essay.'},
        {'word': 'comprehensive', 'definition': 'Covering all or nearly all aspects of something', 'usage': 'The guide provided a comprehensive overview of local birds.'},
        {'word': 'diligent', 'definition': 'Having or showing care and effort in work', 'usage': 'The diligent student reviewed notes every evening.'},
        {'word': 'empathy', 'definition': 'The ability to understand and share the feelings of others', 'usage': 'Reading fiction can increase empathy by letting you see other perspectives.'},
        {'word': 'formidable', 'definition': 'Inspiring fear or respect through being powerful or capable', 'usage': 'The chess champion was a formidable opponent.'},
        {'word': 'genuine', 'definition': 'Truly what something is said to be; authentic', 'usage': 'A genuine apology can repair a damaged friendship.'},
        {'word': 'hypothetical', 'definition': 'Based on an idea or possibility rather than fact', 'usage': 'Let us consider a hypothetical situation where schools start at noon.'},
        {'word': 'innovative', 'definition': 'Introducing new ideas or methods', 'usage': 'The innovative app helps students learn math through games.'},
        {'word': 'juxtapose', 'definition': 'To place different things side by side for comparison', 'usage': 'The artist chose to juxtapose bright colors with dark shadows.'},
        {'word': 'labyrinthine', 'definition': 'Like a labyrinth; intricate and confusing', 'usage': 'The old library had a labyrinthine layout of hidden rooms.'},
        {'word': 'magnanimous', 'definition': 'Generous or forgiving, especially toward a rival', 'usage': 'The magnanimous winner congratulated every opponent.'},
        {'word': 'nurture', 'definition': 'To care for and encourage growth or development', 'usage': 'Parents and teachers work together to nurture young minds.'},
        {'word': 'perceptive', 'definition': 'Having or showing sensitive insight or understanding', 'usage': 'The perceptive detective noticed the tiny clue everyone else missed.'},
    ],
}


def get_vocabulary_words(level, count=3):
    """Get random vocabulary words for a level"""
    if level not in VOCABULARY_WORDS:
        level = 'Beginner'

    words = VOCABULARY_WORDS[level]
    selected = sample(words, min(count, len(words)))

    return selected
