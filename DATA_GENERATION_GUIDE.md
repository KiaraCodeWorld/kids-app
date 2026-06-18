# Brain Quest Data Generation Guide

This guide explains how to create and structure data for all sections of the Brain Quest app. Each section has a specific JSON/Python format, sample generation prompts, and integration instructions.

---

## Table of Contents

1. [Spelling Bee](#spelling-bee)
2. [Vocabulary](#vocabulary)
3. [Mental Math](#mental-math)
4. [Word Explorer (by Tier)](#word-explorer)
5. [Idiom Island](#idiom-island)
6. [Daily Discovery](#daily-discovery)
7. [Math Challenge](#math-challenge)
8. [Flashcard System](#flashcard-system)

---

## Spelling Bee

**File:** `trainer/spelling_content.py`

### Data Structure

```python
SPELLING_LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Expert']

REAL_WORDS = {
    'Beginner': [
        'apple', 'bread', 'cat', 'dog', 'elephant',
        # ... more words
    ],
    'Intermediate': [
        'accommodate', 'believe', 'calendar', 'debris',
        # ... more words
    ],
    'Advanced': [
        'abjure', 'bourgeois', 'chrysalis', 'deluge',
        # ... more words
    ],
    'Expert': [
        'aegis', 'antediluvian', 'bourgeoisie', 'camaraderie',
        # ... more words
    ]
}
```

### Generation Prompt for Claude

```
You are a spelling bee expert for elementary and middle school students (ages 7-13).
Create spelling word lists organized by difficulty level for our educational app.

For each level, provide 25-30 words that:
- Are age-appropriate and from real spelling bee competitions
- Progress in difficulty (Beginner → Intermediate → Advanced → Expert)
- Include phonetically tricky words with silent letters, odd patterns
- Include common student mistakes (like accommodate, necessary, etc.)

Format as a Python dictionary with structure:
REAL_WORDS = {
    'Beginner': ['word1', 'word2', ...],
    'Intermediate': [...],
    'Advanced': [...],
    'Expert': [...]
}

Include explanation for why each word is tricky (silent letters, double consonants, etc.)
```

### Usage Notes
- Returns 10 random words per quiz
- Uses `get_spelling_words(level, count=10)` function
- Words can include accent hints via `get_word_metadata()`

---

## Vocabulary

**File:** `trainer/spelling_content.py`

### Data Structure

```python
VOCABULARY_WORDS = {
    'Beginner': [
        {
            'word': 'persevere',
            'definition': 'To continue doing something despite difficulty',
            'usage': 'She persevered through the difficult exam to achieve her goals.',
        },
        # ... more words
    ],
    'Intermediate': [
        {
            'word': 'eloquent',
            'definition': 'Fluent and expressive in speech or writing',
            'usage': 'The speaker delivered an eloquent speech that moved the audience.',
        },
        # ... more words
    ],
    'Advanced': [
        {
            'word': 'pragmatic',
            'definition': 'Concerned with practical consequences; dealing realistically with things',
            'usage': 'The government took a pragmatic approach to environmental policy.',
        },
        # ... more words
    ],
}
```

### Generation Prompt for Claude

```
You are a vocabulary curriculum expert for elementary and middle school students (ages 7-13).
Create vocabulary word lists organized by proficiency level for our daily lesson system.

For each level (Beginner/Intermediate/Advanced), provide 10 words that:
- Build reading and communication skills
- Are engaging for kids 7-13 years old
- Progress in complexity and abstraction
- Include real-world, relatable usage contexts
- Include positive, actionable definitions (no boring textbook language)

Format as Python dict:
VOCABULARY_WORDS = {
    'Beginner': [
        {
            'word': 'persevere',
            'definition': 'To continue doing something despite difficulty',
            'usage': 'She persevered through the difficult exam to achieve her goals.',
        },
        # ... 9 more
    ],
    # Intermediate and Advanced sections...
}

Make definitions child-friendly, usage examples relatable to kids' lives.
```

### Usage Notes
- Returns 3 random words per lesson
- Kids can save words as flashcards
- Supports all grade levels K-7th

---

## Mental Math

**File:** `trainer/quiz_content.py`

### Data Structure

```python
MENTAL_MATH_QUESTIONS = {
    1: [  # Grade 1
        {
            'question': '2 + 3 = ?',
            'answer': '5',
            'choices': ['4', '5', '6', '7'],
            'explanation': 'Start at 2 and count up 3 more: 2 → 3 → 4 → 5',
            'trick': 'Count on your fingers'
        },
        # ... more questions
    ],
    2: [  # Grade 2
        {
            'question': 'What is 12 - 5?',
            'answer': '7',
            'choices': ['6', '7', '8', '9'],
            'explanation': 'Count backward from 12: 12 → 11 → 10 → 9 → 8 → 7',
            'trick': 'Use a number line or count back'
        },
        # ... more questions
    ],
    # Grades 3-8 similarly
}
```

### Generation Prompt for Claude

```
You are a mental math educator for elementary and middle school students (grades 1-8).
Create age-appropriate mental math questions for each grade level.

For each grade (1-8), provide 20-25 questions that:
- Are appropriate for the grade level
- Mix addition, subtraction, multiplication, division (as grade-appropriate)
- Include realistic word problems
- Have clear 4-choice multiple choice answers
- Include a simple explanation for the correct answer
- Include a mental math "trick" to solve it faster

Format as Python dict:
MENTAL_MATH_QUESTIONS = {
    1: [
        {
            'question': 'What is 2 + 3?',
            'answer': '5',
            'choices': ['4', '5', '6', '7'],
            'explanation': 'Start at 2 and count up 3...',
            'trick': 'Count on your fingers'
        },
        # ... 19-24 more
    ],
    2: [...],  # Grades 2-8
}

Grade 1: Addition/subtraction to 20
Grade 2: Addition/subtraction to 50, intro to multiplication
Grade 3: Multiplication/division to 12x12
Grade 4: Multi-digit multiplication, division
Grade 5: Fractions, decimals, percentages
Grade 6: Ratios, proportions, early algebra
Grade 7: Expressions, equations, pre-algebra
Grade 8: Linear equations, exponents, basic algebra
```

### Usage Notes
- Pulled dynamically by `generate_quiz(grade, count=5)`
- Returns random subset of questions per session
- Tracks accuracy per grade level

---

## Word Explorer

**File:** `trainer/word_explorer_content.py`

### Data Structure

```python
# Helper function
def _w(id, word, emoji, ctx, dfn, ex, prompt):
    return {
        'id': id,
        'word': word,
        'emoji': emoji,
        'context': ctx,           # Where kids see this word
        'definition': dfn,         # Child-friendly definition
        'example': ex,             # Real usage example
        'use_prompt': prompt       # Engagement question
    }

# Organized by age tier
WORD_TIERS = {
    '5-7': [
        _w('t1_001', 'gigantic', '🦕', 'Cartoons, toys', 
           'Super-duper huge — way bigger than normal!',
           'That stuffed bear is gigantic!',
           'Name something gigantic outside.'),
        # ... 199 more words (200 total)
    ],
    '8-10': [
        # ... 200 words of intermediate vocabulary
    ],
    '11-13': [
        # ... 200 words of advanced vocabulary
    ]
}

TIER_LABELS = {
    '5-7':  {'label':'Ages 5–7',  'grade':'K–1st Grade',  'emoji':'🟢','color':'#10b981','desc':'Fun action words, feelings, and everyday things'},
    '8-10': {'label':'Ages 8–10','grade':'2nd–4th Grade','emoji':'🟡','color':'#f59e0b','desc':'News words, social words, and descriptive power'},
    '11-13':{'label':'Ages 11–13','grade':'5th–7th Grade','emoji':'🔴','color':'#ef4444','desc':'Article words, debate words, and emotional intelligence'},
}
```

### Generation Prompt for Claude

```
You are a creative vocabulary expert for children ages 5-13. We are building a "Word Explorer" 
academy where kids discover new words organized by age tier, with visual descriptions and 
engagement activities.

For EACH age tier below, create exactly 200 words with these properties:

**Ages 5-7 (Tier 1):**
- Action words (gigantic, shiver, leap, sprint)
- Descriptive words (shiny, bumpy, sour, soft)
- Emotion words (happy, scared, brave, grumpy)
- Nature words (sparkle, breeze, rainbow, muddy)
- Sound words (crunch, whisper, buzz, creak)
- Total: ~200 words split across categories

**Ages 8-10 (Tier 2):**
- News/current event vocabulary
- Social and group words
- More complex emotions and motivations
- Academic subject words
- Total: ~200 words

**Ages 11-13 (Tier 3):**
- Debate and persuasion words
- Abstract concepts
- Advanced emotional intelligence
- Technical and specialized terms
- Total: ~200 words

For EACH word, provide:
1. **Word**: The vocabulary word itself
2. **Emoji**: A relevant visual emoji (single emoji only)
3. **Context**: Where kids encounter this word (e.g., "Movies, bedtime, cozy spots")
4. **Definition**: Simple, engaging, child-appropriate (avoid textbook language)
5. **Example**: Real usage sentence kids can relate to
6. **Prompt**: An interactive question to engage the child ("What makes you gigantic?", "Where have you seen drift?")

Format as a Python list where each word is created by calling:
_w(id, word, emoji, context, definition, example, prompt)

Use IDs like: t1_001, t1_002 (tier 1) through t3_200 (tier 3)

Make the definitions vivid and playful, not boring. Include actions, emotions, nature, 
sensations — things kids actually experience and care about.
```

### Usage Notes
- 200 words per tier → total 600 words
- Daily system shows 3 words: 1 new, 1 review, 1 challenge
- Words can be saved as flashcards
- Tier progression is built into the UI

---

## Idiom Island

**File:** `trainer/word_explorer_content.py`

### Data Structure

```python
# Helper function
def _i(id, phrase, emoji, literal, meaning, example):
    return {
        'id': id,
        'phrase': phrase,           # The idiom (e.g., "piece of cake")
        'emoji': emoji,             # Visual representation
        'literal': literal,         # Silly literal interpretation (visual story)
        'meaning': meaning,         # What it actually means
        'example': example          # Real usage by a kid
    }

_IDIOMS = [
    _i('i001', 'break a leg', '🎭', 
       'Someone literally snapping their leg in half before walking on stage',
       'Good luck — especially before a performance or difficult task',
       'Tomorrow is my spelling test. Break a leg!'),
    # ... 199 more idioms (200 total)
]

IDIOMS = _IDIOMS
```

### Generation Prompt for Claude

```
You are an idiom expert creating engaging idioms for kids ages 7-13. We are building "Idiom Island"
where kids learn expressions they hear in movies, books, and real conversations.

Create 200 idioms organized by category. For EACH idiom, include:

1. **Phrase**: The actual idiom kids will learn (e.g., "piece of cake", "raining cats and dogs")
2. **Emoji**: A single fun emoji representing it
3. **Literal**: A humorous/silly visual interpretation of the literal meaning 
   (e.g., "A baker literally tossing cakes into a mouth" for "piece of cake")
4. **Meaning**: Clear explanation of what it ACTUALLY means
5. **Example**: A sentence from a kid's perspective using the idiom naturally

Categories to include (40 idioms each):
1. School & Learning (study, test, pay attention themed)
2. Friendship & Feelings (happy, sad, trust themed)
3. Sports & Competition (win, try, practice themed)
4. Family & Home (household, care, responsibility themed)
5. Nature & Outdoors (weather, animals, movement themed)
6. Modern Slang & Gen-Z (fire, vibe, main character, etc.)

Format as Python:
_IDIOMS = [
    _i('i001', 'break a leg', '🎭',
       'Someone literally snapping their leg in half before walking on stage',
       'Good luck — especially before a performance or difficult task',
       'Tomorrow is my spelling test. Break a leg!'),
    # ... 199 more
]

Make the literal interpretations silly and visual so kids can create mental pictures.
Make examples relatable to kids' actual lives (school, friends, sports, home).
```

### Usage Notes
- 200 total idioms
- Daily rotation via `get_daily_idiom()`
- Kids can save as flashcards
- Literal descriptions help memory retention

---

## Daily Discovery

**File:** `trainer/daily_discovery_content.py`

### Data Structure

```python
DISCOVERY_CATEGORIES = {
    'history': [
        {
            'id': 'hist_001',
            'title': 'The Great Pyramid of Giza',
            'emoji': '🔺',
            'category': 'Ancient Wonders',
            'description': 'Built over 4,500 years ago, the pyramids still amaze us today.',
            'facts': [
                'Took 20 years and 100,000 workers to build',
                'Originally covered in white limestone that shined in the sun',
                'The only surviving wonder of the ancient world'
            ],
            'fun_fact': 'If you stacked $1 bills from here to the moon, you could build another pyramid!',
            'video_url': 'https://example.com/pyramid.mp4',  # Optional
            'sources': ['Wikipedia: Great Pyramid', 'National Geographic']
        },
        # ... more history items
    ],
    'science': [
        {
            'id': 'sci_001',
            'title': 'Why Do Octopuses Have Blue Blood?',
            'emoji': '🐙',
            'category': 'Marine Life',
            'description': 'Unlike humans with iron-based red blood...',
            'facts': [
                'Octopuses use copper-based hemocyanin instead of iron',
                'This makes their blood better for cold, deep ocean water',
                'Blue blood is visible through their transparent skin'
            ],
            'fun_fact': 'An octopus has THREE hearts — two pump blood to the gills, one to the body!',
            'video_url': None,
            'sources': []
        },
        # ... more science items
    ],
    'nature': [
        # ... nature discoveries
    ],
    'technology': [
        # ... tech discoveries
    ],
    'culture': [
        # ... cultural discoveries
    ]
}
```

### Generation Prompt for Claude

```
You are a science communicator creating daily discovery content for curious kids ages 7-13.
We are building a "Daily Discovery" section where kids learn one fascinating fact per day
about history, science, nature, technology, and culture.

For EACH category below, create 15-20 discovery items. Each item should:

1. **Title**: Catchy, question-based or intriguing headline
2. **Emoji**: Single relevant emoji
3. **Category**: Subcategory (e.g., "Ancient Wonders", "Marine Life")
4. **Description**: 1-2 sentence hook that makes kids want to learn
5. **Facts**: 3-5 bullet points of interesting, verifiable facts
6. **Fun Fact**: ONE wow moment or mind-bending connection
7. **Sources**: At least 1 credible source (Wikipedia, National Geographic, etc.)

Categories to cover:
- **History** (15 items): Ancient Egypt, Rome, inventions, famous leaders
- **Science** (20 items): Space, biology, physics, amazing animals
- **Nature** (15 items): Ecosystems, weather, plants, insects
- **Technology** (15 items): How things work, inventions, AI, robots
- **Culture** (15 items): Languages, holidays, traditions, art

Format as Python dict:
DISCOVERY_CATEGORIES = {
    'history': [
        {
            'id': 'hist_001',
            'title': 'The Great Pyramid of Giza',
            'emoji': '🔺',
            'category': 'Ancient Wonders',
            'description': 'Built over 4,500 years ago...',
            'facts': [
                'Took 20 years and 100,000 workers',
                'Originally covered in white limestone',
                'The only surviving wonder of the ancient world'
            ],
            'fun_fact': 'Something that connects to their world or blows their mind!',
            'sources': ['Wikipedia: Great Pyramid', 'National Geographic']
        },
        # ... 14-19 more
    ],
    # Other categories...
}

Make facts verified and age-appropriate. Focus on "wow" moments and connections.
```

### Usage Notes
- 60-80 total discoveries across 5 categories
- One random item shown per day
- Rotates through all items before repeating
- Supports optional video URLs (for future expansion)

---

## Math Challenge

**File:** `trainer/math_challenge_content.py`

### Data Structure

```python
MATH_CHALLENGES = {
    1: [  # Grade 1
        {
            'id': 'g1_001',
            'problem': 'Sarah has 3 apples. Her friend gives her 2 more. How many apples does she have now?',
            'answer': '5',
            'choices': ['4', '5', '6', '7'],
            'difficulty': 'easy',
            'trick': 'Squishing Numbers - Use a tens frame',
            'explanation': 'We start with 3 apples and add 2 more: 3 + 2 = 5',
            'hint': 'Count on your fingers or use objects',
            'category': 'addition'
        },
        # ... more problems
    ],
    # Grades 2-8 similarly
}
```

### Generation Prompt for Claude

```
You are a math curriculum expert creating engaging math word problems for grades 1-8.
Create problems that build mental math skills and include teaching "tricks" or strategies.

For EACH grade level (1-8), create 25-30 problems that:
- Use relatable, real-world scenarios
- Mix operation types (addition, subtraction, multiplication, division)
- Include a "math trick" or strategy name (e.g., "Squishing Numbers", "Fact Families")
- Have 4 multiple choice answers with 1 correct answer
- Include a clear explanation and helpful hint

Format as Python dict:
MATH_CHALLENGES = {
    1: [
        {
            'id': 'g1_001',
            'problem': 'Sarah has 3 apples. Her friend gives her 2 more. How many apples does she have now?',
            'answer': '5',
            'choices': ['4', '5', '6', '7'],
            'difficulty': 'easy',
            'trick': 'Squishing Numbers - Count on your fingers',
            'explanation': 'We start with 3 apples and add 2 more: 3 + 2 = 5',
            'hint': 'Try counting on from 3',
            'category': 'addition'
        },
        # ... 24-29 more
    ],
    # Grades 2-8...
}

Grade 1: Simple addition/subtraction to 20
Grade 2: Two-digit addition/subtraction, intro multiplication
Grade 3: Multiplication tables, division basics
Grade 4: Multi-digit multiplication, long division
Grade 5: Fractions, decimals, percentages
Grade 6: Ratios, proportions, rates
Grade 7: Expressions, equations, negative numbers
Grade 8: Linear equations, exponents, pre-algebra

Include real-world contexts kids relate to (allowance, sports, games, shopping).
```

### Usage Notes
- 25-30 problems per grade level
- Randomly selected per quiz session
- Tracks performance by category and difficulty
- "Tricks" are taught mental math strategies

---

## Flashcard System

**File:** `trainer/models.py` - `SavedFlashcard` model

### Data Structure

```python
class SavedFlashcard(models.Model):
    CARD_TYPES = [('word', 'Word'), ('idiom', 'Idiom')]
    
    card_type = models.CharField(max_length=10, choices=CARD_TYPES)
    front_text = models.CharField(max_length=200)      # The word/idiom
    back_text = models.TextField()                      # Definition/meaning
    example = models.TextField(blank=True)              # Usage example
    emoji = models.CharField(max_length=10, blank=True) # Visual aid
    extra_json = models.JSONField(default=dict)         # Extra data
    saved_at = models.DateTimeField(auto_now_add=True)
```

### JSON Structure for `extra_json`

```json
{
  "word_type": "vocabulary",
  "tier": "5-7",
  "pronunciation": "jig-an-tik",
  "synonyms": ["huge", "enormous", "massive"],
  "context": "Cartoons, toys",
  "memory_aid": "Think of a GIANT + TIC (like a nervous tic) = GIGANTIC!"
}
```

### Usage Notes
- Kids save words/idioms for later review
- Supports flip-card animation
- Supports pronunciation audio (optional)
- Can export/import full deck
- Syncs with learning progress

---

## Integration Steps

### 1. Add Data to Respective Files

- **Spelling:** Update `REAL_WORDS` dict in `spelling_content.py`
- **Vocabulary:** Update `VOCABULARY_WORDS` dict in `spelling_content.py`
- **Mental Math:** Create/update `quiz_content.py` with `MENTAL_MATH_QUESTIONS`
- **Word Explorer:** Update `WORD_TIERS` dict in `word_explorer_content.py`
- **Idioms:** Update `_IDIOMS` list in `word_explorer_content.py`
- **Daily Discovery:** Create/update `daily_discovery_content.py`
- **Math Challenge:** Create/update `math_challenge_content.py`

### 2. Test Data Loading

```python
# From Django shell
python manage.py shell

from trainer.spelling_content import get_spelling_words
words = get_spelling_words('Beginner', count=5)
print(words)

from trainer.word_explorer_content import WORD_TIERS
print(len(WORD_TIERS['5-7']))  # Should be 200
```

### 3. Run Migrations (if adding new models)

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Verify in Browser

- Visit `/` → Spelling, Vocabulary, Word Explorer
- Visit `/mental-quiz/` → Mental Math
- Visit `/idiom-island/` → Idioms
- Visit `/daily-discovery/` → Daily Discovery
- Visit `/math-challenge/` → Math Challenge

---

## Data Quality Checklist

- [ ] All definitions are child-friendly (no jargon)
- [ ] Examples are relatable to kids' lives
- [ ] Emoji choices are accurate and recognizable
- [ ] No copyright issues with content
- [ ] Facts are verified and credible
- [ ] No inappropriate language or themes
- [ ] Content progression is smooth (easy → hard)
- [ ] Each section has at least 15-20 items per difficulty level
- [ ] IDs are unique and follow naming convention
- [ ] Formatting is consistent across all entries

---

## Helpful Resources

- **Spelling Words:** Scripps Spelling Bee word lists
- **Vocabulary:** Merriam-Webster Learning, Vocabulary.com
- **Math:** Common Core standards, Khan Academy
- **Idioms:** Dictionary.com Idioms, Idioms Online
- **Science Facts:** National Geographic Kids, Smithsonian

---

## Questions?

For issues or questions about data structure:
1. Check the relevant content file for examples
2. Review the model definitions in `trainer/models.py`
3. Test with `python manage.py shell` before adding to live app
4. Verify on a development server first
