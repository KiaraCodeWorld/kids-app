# Quick Data Generation Prompts

You can now generate data automatically with the `generate_content` management command. See the **Automated Pipeline** section at the top of `DATA_GENERATION_GUIDE.md` for details.

Quick examples:

```bash
# Generate spelling words
python manage.py generate_content --section spelling --level Beginner --batch 20

# Generate vocabulary words
python manage.py generate_content --section vocabulary --level Intermediate --target 100

# Generate Daily Discovery items
python manage.py generate_content --section daily_discovery --category funfact --batch 10 --merge
```

You can still copy and paste the prompts below into Claude or ChatGPT if you prefer manual generation.

---

Copy and paste these prompts directly into Claude or ChatGPT to generate datasets.

---

## 🎯 Spelling Bee Dataset (30 words per level)

```
Create 4 spelling word lists for an elementary app. Format as Python dict:

SPELLING_LEVELS = ['Beginner', 'Intermediate', 'Advanced', 'Expert']

REAL_WORDS = {
    'Beginner': [
        # 30 words: simple, common, 1-2 syllables
        'apple', 'bread', 'cat', 'dog', 'elephant', ...
    ],
    'Intermediate': [
        # 30 words: compound/tricky, 2-3 syllables, common mistakes
        'accommodate', 'believe', 'calendar', 'debris', ...
    ],
    'Advanced': [
        # 30 words: harder, 3-4 syllables, less common
        'abjure', 'bourgeois', 'chrysalis', 'deluge', ...
    ],
    'Expert': [
        # 30 words: competition level, rare, complex
        'aegis', 'antediluvian', 'bourgeoisie', 'camaraderie', ...
    ]
}

Include words that are:
- From real spelling bee competitions (Scripps)
- Progressive in difficulty
- Include phonetically tricky patterns
- Age-appropriate for elementary/middle school

Return ONLY the Python dict with 30 words per level (120 total).
```

---

## 📚 Vocabulary Dataset (15 words per level)

```
Create vocabulary word lists for 3 grade levels. Format as Python dict:

VOCABULARY_WORDS = {
    'Beginner': [
        {
            'word': 'persevere',
            'definition': 'To continue doing something despite difficulty',
            'usage': 'She persevered through the difficult exam to achieve her goals.'
        },
        # ... 14 more words
    ],
    'Intermediate': [
        # 15 words with more complex meanings
    ],
    'Advanced': [
        # 15 words, abstract, advanced concepts
    ]
}

Requirements per word:
- Definition: simple, child-friendly (no textbook language)
- Usage: realistic example from a kid's perspective
- No slang or inappropriate terms

Each level should have exactly 15 words (45 total).
```

---

## 🧮 Mental Math Dataset (20 problems per grade)

```
Create mental math word problems for grades 1-3. Format as Python dict:

MENTAL_MATH_QUESTIONS = {
    1: [
        {
            'question': '2 + 3 = ?',
            'answer': '5',
            'choices': ['4', '5', '6', '7'],
            'explanation': 'Count from 2: 2 → 3 → 4 → 5',
            'trick': 'Count on your fingers'
        },
        # ... 19 more for grade 1
    ],
    2: [
        # 20 problems for grade 2 (subtraction, harder addition)
    ],
    3: [
        # 20 problems for grade 3 (multiplication intro)
    ]
}

Requirements:
- Grade 1: Addition/subtraction to 20
- Grade 2: Addition/subtraction to 100, intro multiplication
- Grade 3: Multiplication 1-12 facts, basic division

Each problem needs:
- question: Clear word problem
- answer: Correct answer as string
- choices: 4 options (correct answer in random position)
- explanation: Step-by-step solution
- trick: Mental math strategy name

Return 20 problems per grade (60 total for grades 1-3).
```

---

## 🌟 Word Explorer Dataset (50 words per tier)

**Tier 1: Ages 5-7 (50 words)**

```
Create 50 action and descriptive words for young kids. Format:

TIER_1_WORDS = [
    {
        'id': 't1_001',
        'word': 'gigantic',
        'emoji': '🦕',
        'context': 'Cartoons, toys',
        'definition': 'Super-duper huge — way bigger than normal!',
        'example': 'That stuffed bear is gigantic!',
        'use_prompt': 'Name something gigantic outside.'
    },
    # ... 49 more words
]

Categories (10 words each):
1. Movement words (jump, hop, skip, leap, dance, etc.)
2. Feeling words (happy, scared, brave, sad, angry, etc.)
3. Touch/texture words (soft, rough, bumpy, smooth, sticky, etc.)
4. Sound words (crunch, whisper, buzz, bang, etc.)
5. Weather/nature words (sparkle, breeze, sunny, rainy, etc.)

Requirements:
- Emoji: Single, relevant emoji only
- Definition: 1-2 sentences, simple words, exciting tone
- Example: Real sentence using the word naturally
- Prompt: Question that engages the child

Return exactly 50 words (5 categories × 10 words).
```

**Tier 2: Ages 8-10 (50 words)**

```
Create 50 intermediate vocabulary words. Same format as above but:

Categories:
1. Academic words (analyze, organize, investigate, discover, etc.)
2. Social/friendship words (collaborate, discuss, debate, negotiate, etc.)
3. Emotion/motivation words (determined, curious, focused, anxious, etc.)
4. News/current event words (climate, technology, culture, community, etc.)
5. Descriptive/advanced (elaborate, mysterious, brilliant, humble, etc.)

Make definitions age-appropriate for 8-10 year olds. Include relatable contexts.
```

**Tier 3: Ages 11-13 (50 words)**

```
Create 50 advanced vocabulary words. Same format but:

Categories:
1. Debate/persuasion words (convince, argue, evidence, thesis, etc.)
2. Abstract concept words (perspective, impact, influence, legacy, etc.)
3. Advanced emotion words (contemplate, resilient, conflicted, enlightened, etc.)
4. Technical/specialized words (algorithm, data, evolution, photosynthesis, etc.)
5. Complex descriptive words (ambiguous, meticulous, pragmatic, austere, etc.)

Definitions should be clear but intellectually challenging. Prompts should encourage deeper thinking.
```

---

## 🎭 Idioms Dataset (30 idioms)

```
Create 30 idioms that kids (7-13) actually hear and use. Format:

IDIOMS = [
    {
        'id': 'i001',
        'phrase': 'break a leg',
        'emoji': '🎭',
        'literal': 'Someone literally snapping their leg in half before a performance',
        'meaning': 'Good luck — especially before a performance or difficult task',
        'example': 'Tomorrow is my spelling test. Break a leg!'
    },
    # ... 29 more idioms
]

Categories (6 idioms each):
1. School/Learning idioms (piece of cake, break a leg, etc.)
2. Friendship/Emotion idioms (break the ice, wear your heart on your sleeve, etc.)
3. Sports/Competition idioms (play ball, move the goal posts, etc.)
4. Family/Home idioms (home stretch, knock it out of the park, etc.)
5. Modern slang (that's fire, bet, no cap, vibe check, etc.)
6. Nature/Weather idioms (raining cats and dogs, storm is coming, etc.)

Requirements:
- Literal: Silly, visual interpretation (kids should laugh)
- Meaning: Simple, direct explanation
- Example: Kid's perspective, natural usage

Return 30 idioms total.
```

---

## 🔬 Daily Discovery Dataset (15 items per category)

```
Create 15 fascinating discovery items for 3 categories. Format:

DISCOVERIES = {
    'science': [
        {
            'id': 'sci_001',
            'title': 'Why Do Octopuses Have Blue Blood?',
            'emoji': '🐙',
            'category': 'Marine Life',
            'description': 'Unlike humans with iron-based red blood, octopuses use copper-based hemocyanin instead.',
            'facts': [
                'Octopuses use copper-based hemocyanin instead of iron',
                'This makes their blood better for cold, deep ocean water',
                'Blue blood is visible through their transparent skin'
            ],
            'fun_fact': 'An octopus has THREE hearts — two pump blood to the gills, one to the body!',
            'sources': ['National Geographic Kids', 'Wikipedia: Octopus']
        },
        # ... 14 more for science
    ],
    'history': [
        # 15 historical discoveries
    ],
    'nature': [
        # 15 nature discoveries
    ]
}

Categories (15 items each):
1. SCIENCE: Animals, space, human body, technology
2. HISTORY: Ancient civilizations, inventions, famous people
3. NATURE: Ecosystems, weather patterns, plants, insects

Requirements per item:
- Title: Question-based or intriguing headline
- Description: 1-2 sentences that hook interest
- Facts: 3-5 bullet points, verified and credible
- Fun fact: ONE "wow" moment (connections, surprising stat, etc.)
- Sources: At least 1 credible source

Return 45 items total (15 per category).
```

---

## 🎲 Math Challenge Dataset (20 problems per grade)

**Grades 1-2:**

```
Create 20 word problems for Grade 1 & 2. Format:

MATH_CHALLENGES = {
    1: [
        {
            'id': 'g1_001',
            'problem': 'Sarah has 3 apples. Her friend gives her 2 more. How many apples does she have now?',
            'answer': '5',
            'choices': ['4', '5', '6', '7'],
            'difficulty': 'easy',
            'trick': 'Count on your fingers',
            'explanation': 'Start with 3 and count 2 more: 3 + 2 = 5',
            'hint': 'Use your fingers to count',
            'category': 'addition'
        },
        # ... 19 more for grade 1
    ],
    2: [
        # 20 problems for grade 2
    ]
}

Grade 1:
- Focus: Addition/subtraction to 20
- 10 addition problems, 10 subtraction problems

Grade 2:
- Focus: Addition/subtraction to 100, intro multiplication
- 8 addition, 8 subtraction, 4 with 2-digit numbers

Requirements:
- problem: Real-world scenario (toys, allowance, sports, etc.)
- answer: Correct answer as string
- choices: 4 options with correct answer random
- trick: A strategy name (e.g., "Counting on", "Using tens frames")
- explanation: Clear step-by-step solution
- hint: A helpful clue
- category: The math type

Return 40 problems total (20 per grade for grades 1-2).
```

---

## How to Use These Prompts

1. **Copy the prompt** for the dataset you need
2. **Paste into Claude/ChatGPT**
3. **Request modifications** if needed (e.g., "Make it themed around space" or "Include more challenging vocab")
4. **Copy the returned code** and paste into the appropriate file
5. **Test** by running `python manage.py shell` and importing the data
6. **Refresh** your browser to see the new content

---

## Example: Complete Workflow

### Step 1: Get Spelling Data
Paste the Spelling Bee prompt into Claude → Get dict with 120 words

### Step 2: Add to `trainer/spelling_content.py`
```python
# Replace existing REAL_WORDS with Claude's output
REAL_WORDS = {
    'Beginner': [...],
    'Intermediate': [...],
    'Advanced': [...],
    'Expert': [...]
}
```

### Step 3: Test
```bash
python manage.py shell
from trainer.spelling_content import get_spelling_words
words = get_spelling_words('Beginner')
print(words)
```

### Step 4: Verify in Browser
Visit `http://localhost:8000/spelling/Beginner/` → Should show new words

---

## Dataset Size Summary

**Recommended dataset sizes:**

| Section | Items | Notes |
|---------|-------|-------|
| Spelling | 120 (30/level) | 4 levels |
| Vocabulary | 45 (15/level) | 3 levels |
| Mental Math | 100+ (20+/grade) | Grades 1-8 |
| Word Explorer | 600 (200/tier) | 3 tiers |
| Idioms | 200 | Mixed categories |
| Daily Discovery | 60-80 | 5 categories |
| Math Challenge | 150+ (25+/grade) | Grades 1-8 |

**Total: ~1,300+ items** for a complete app

---

## Need More Help?

- **For individual sections:** See `DATA_GENERATION_GUIDE.md`
- **For Claude prompts:** Use these templates as-is or modify for your needs
- **For format questions:** Check the example code in each prompt
- **For testing:** Use `python manage.py shell` and import functions

Good luck! 🚀
