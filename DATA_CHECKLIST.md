# Data Integration Checklist ✅

Use this checklist to track your progress adding datasets to Brain Quest.

---

## 📋 Quick Overview

- [ ] Spelling Bee (4 levels × 100 words = 400 items)
- [ ] Vocabulary (3 levels × 100 words = 300 items)
- [ ] Mental Math (8 grades × 20+ problems = 160+ items)
- [ ] Word Explorer (3 tiers × 200 words = 600 items)
- [ ] Idiom Island (200 items)
- [ ] Daily Discovery (7 categories × 100 items = 700 items)
- [ ] Math Challenge (8 grades × 25+ problems = 200+ items)
- [ ] Flashcards (Auto-populated from vocab/idioms)

**Total: ~2,500+ items**

You can grow Spelling, Vocabulary, and Daily Discovery automatically with the `generate_content` management command. See the *Automated Pipeline* section in `DATA_GENERATION_GUIDE.md`.

---

## 🎯 Section-by-Section Checklist

### ✅ Spelling Bee
**File:** `trainer/spelling_content.py`

- [ ] Use prompt from `GENERATE_DATA_PROMPTS.md` or run `python manage.py generate_content --section spelling --level <Level> --target 100`
- [ ] Generate 4 levels: Beginner, Intermediate, Advanced, Expert
- [ ] 100 words per level (400 total)
- [ ] Copy output into `REAL_WORDS` dict
- [ ] Test: `python manage.py shell`
  ```python
  from trainer.spelling_content import get_spelling_words
  words = get_spelling_words('Beginner', count=10)
  print(len(words))  # Should be 10
  ```
- [ ] Verify in browser: `localhost:8000/spelling/`
- [ ] All 4 levels showing ✓

### ✅ Vocabulary
**File:** `trainer/spelling_content.py`

- [ ] Use prompt from `GENERATE_DATA_PROMPTS.md` or run `python manage.py generate_content --section vocabulary --level <Level> --target 100`
- [ ] Generate 3 levels: Beginner, Intermediate, Advanced
- [ ] 100 words per level (300 total)
- [ ] Each word has: word, definition, usage
- [ ] Copy output into `VOCABULARY_WORDS` dict
- [ ] Test: `python manage.py shell`
  ```python
  from trainer.spelling_content import get_vocabulary_words
  words = get_vocabulary_words('Beginner', count=3)
  print(words[0])  # Check structure
  ```
- [ ] Verify in browser: `localhost:8000/vocabulary/`
- [ ] Can save words as flashcards ✓

### ✅ Mental Math
**File:** `trainer/quiz_content.py`

- [ ] Create file if doesn't exist: `trainer/quiz_content.py`
- [ ] Use prompt from `GENERATE_DATA_PROMPTS.md`
- [ ] Generate for grades 1-3 (or 1-8 for full coverage)
- [ ] 20+ problems per grade
- [ ] Each problem has: question, answer, choices, explanation, trick, hint
- [ ] Create dict: `MENTAL_MATH_QUESTIONS`
- [ ] Test: `python manage.py shell`
  ```python
  from trainer.quiz_content import generate_quiz
  quiz = generate_quiz(grade=1, count=5)
  print(quiz)  # Check structure
  ```
- [ ] Verify in browser: `localhost:8000/mental-quiz/`
- [ ] Can select grades and see problems ✓

### ✅ Word Explorer (Ages 5-7)
**File:** `trainer/word_explorer_content.py`

- [ ] Use prompt from `GENERATE_DATA_PROMPTS.md` (Tier 1)
- [ ] Generate 200 words (or start with 50-100)
- [ ] Organize by category: Movement, Feelings, Textures, Sounds, Nature
- [ ] Each word: id, word, emoji, context, definition, example, use_prompt
- [ ] Use helper: `_w(id, word, emoji, context, dfn, ex, prompt)`
- [ ] Create list: `_T1 = [...]`
- [ ] Add to: `WORD_TIERS = {'5-7': _T1}`
- [ ] Test: `python manage.py shell`
  ```python
  from trainer.word_explorer_content import WORD_TIERS
  print(len(WORD_TIERS['5-7']))  # Should be 200+
  ```
- [ ] Verify in browser: `localhost:8000/word-explorer/`
- [ ] 5-7 age tier appears ✓

### ✅ Word Explorer (Ages 8-10)
**File:** `trainer/word_explorer_content.py`

- [ ] Use prompt from `GENERATE_DATA_PROMPTS.md` (Tier 2)
- [ ] Generate 200 words (or start with 50-100)
- [ ] Categories: Academic, Social, Emotion/Motivation, News/Current, Descriptive
- [ ] Each word: id, word, emoji, context, definition, example, use_prompt
- [ ] Use helper: `_w(id, word, emoji, context, dfn, ex, prompt)`
- [ ] Create list: `_T2 = [...]`
- [ ] Add to: `WORD_TIERS = {'8-10': _T2, ...}`
- [ ] Test: `python manage.py shell`
  ```python
  from trainer.word_explorer_content import WORD_TIERS
  print(len(WORD_TIERS['8-10']))  # Should be 200+
  ```
- [ ] Verify in browser: `localhost:8000/word-explorer/`
- [ ] 8-10 age tier appears ✓

### ✅ Word Explorer (Ages 11-13)
**File:** `trainer/word_explorer_content.py`

- [ ] Use prompt from `GENERATE_DATA_PROMPTS.md` (Tier 3)
- [ ] Generate 200 words (or start with 50-100)
- [ ] Categories: Debate/Persuasion, Abstract, Advanced Emotion, Technical, Complex Descriptive
- [ ] Each word: id, word, emoji, context, definition, example, use_prompt
- [ ] Use helper: `_w(id, word, emoji, context, dfn, ex, prompt)`
- [ ] Create list: `_T3 = [...]`
- [ ] Add to: `WORD_TIERS = {'11-13': _T3, ...}`
- [ ] Test: `python manage.py shell`
  ```python
  from trainer.word_explorer_content import WORD_TIERS
  print(len(WORD_TIERS['11-13']))  # Should be 200+
  ```
- [ ] Verify in browser: `localhost:8000/word-explorer/`
- [ ] 11-13 age tier appears ✓

### ✅ Idiom Island
**File:** `trainer/word_explorer_content.py`

- [ ] Use prompt from `GENERATE_DATA_PROMPTS.md`
- [ ] Generate 200 idioms (or start with 30-50)
- [ ] Categories: School/Learning, Friendship/Emotion, Sports, Family, Modern Slang, Nature/Weather
- [ ] Each idiom: id, phrase, emoji, literal, meaning, example
- [ ] Use helper: `_i(id, phrase, emoji, literal, meaning, example)`
- [ ] Create list: `_IDIOMS = [...]`
- [ ] Add to: `IDIOMS = _IDIOMS`
- [ ] Test: `python manage.py shell`
  ```python
  from trainer.word_explorer_content import IDIOMS
  print(len(IDIOMS))  # Should be 200+
  ```
- [ ] Verify in browser: `localhost:8000/idiom-island/`
- [ ] Idiom displays correctly with all fields ✓
- [ ] Can save as flashcard ✓

### ✅ Daily Discovery
**File:** `trainer/daily_discovery_content.py`

- [ ] Create file: `trainer/daily_discovery_content.py`
- [ ] Use prompt from `GENERATE_DATA_PROMPTS.md` or run `python manage.py generate_content --section daily_discovery --category <category> --target 100`
- [ ] Generate 100 items per category (700 items)
- [ ] Categories: space, manners, funfact, hack, game, trending, news
- [ ] Each item: id, title, emoji, category, description, facts (list), fun_fact, sources (list)
- [ ] Create dict: `DISCOVERY_CATEGORIES`
- [ ] Test: `python manage.py shell`
  ```python
  from trainer.daily_discovery_content import DISCOVERY_CATEGORIES
  print(DISCOVERY_CATEGORIES['science'][0])  # Check structure
  ```
- [ ] Verify in browser: `localhost:8000/daily-discovery/`
- [ ] Random item displays daily ✓
- [ ] Categories work ✓

### ✅ Math Challenge
**File:** `trainer/math_challenge_content.py`

- [ ] Create file: `trainer/math_challenge_content.py`
- [ ] Use prompt from `GENERATE_DATA_PROMPTS.md`
- [ ] Generate for grades 1-3 (or 1-8 for full coverage)
- [ ] 20+ problems per grade
- [ ] Each problem: id, problem, answer, choices, difficulty, trick, explanation, hint, category
- [ ] Create dict: `MATH_CHALLENGES`
- [ ] Test: `python manage.py shell`
  ```python
  from trainer.math_challenge_content import MATH_CHALLENGES
  print(MATH_CHALLENGES[1][0])  # Check structure
  ```
- [ ] Verify in browser: `localhost:8000/math-challenge/`
- [ ] Can select grade and see problems ✓
- [ ] Tricks and explanations display ✓

---

## 🔍 Quality Checks

For **each** dataset before committing:

### Spelling & Vocabulary
- [ ] No duplicate words
- [ ] Definitions are child-friendly
- [ ] Examples are grammatically correct
- [ ] Spelling is correct (ironic for Spelling Bee!)

### Mental Math & Math Challenge
- [ ] Math is correct (answers verified)
- [ ] 4 choices with correct answer in random position
- [ ] Explanations are clear
- [ ] Grade progression makes sense

### Word Explorer
- [ ] IDs are unique (no duplicates)
- [ ] Emojis are single characters only
- [ ] Definitions avoid jargon
- [ ] Examples are relatable to kids
- [ ] Prompts engage the child

### Idioms
- [ ] Literal interpretations are silly/visual
- [ ] Meanings are accurate
- [ ] Examples use natural kid language
- [ ] All 200 (or target count) present

### Daily Discovery
- [ ] Facts are verified (check sources)
- [ ] Facts are age-appropriate
- [ ] Fun fact is genuinely interesting
- [ ] No inappropriate content

---

## 📊 Progress Tracker

| Section | Items | Status | Notes |
|---------|-------|--------|-------|
| Spelling | 400 | 🟨 | 4 levels, 100 each (53-82/level so far) |
| Vocabulary | 300 | 🟨 | 3 levels, 100 each (~25/level so far) |
| Mental Math | 160+ | ⬜ | 8 grades, 20+ each |
| Word Explorer | 600 | 🟩 | 3 tiers, 200 each |
| Idioms | 200 | 🟩 | Mixed categories |
| Daily Discovery | 700 | 🟨 | 7 categories, 100 each (20/level so far) |
| Math Challenge | 200+ | 🟨 | 8 grades, 25+ each |

**Key:** ⬜ = Not Started | 🟨 = In Progress | 🟩 = Complete

---

## 🧪 Testing Commands

```bash
# Start Django shell
python manage.py shell

# Test Spelling
from trainer.spelling_content import get_spelling_words
print(get_spelling_words('Beginner', count=5))

# Test Vocabulary
from trainer.spelling_content import get_vocabulary_words
print(get_vocabulary_words('Beginner', count=3))

# Test Mental Math
from trainer.quiz_content import generate_quiz
print(generate_quiz(grade=2, count=5))

# Test Word Explorer
from trainer.word_explorer_content import WORD_TIERS, get_daily_words
print(f"Tier 5-7: {len(WORD_TIERS['5-7'])} words")
print(get_daily_words('5-7'))

# Test Idioms
from trainer.word_explorer_content import IDIOMS, get_daily_idiom
print(f"Total idioms: {len(IDIOMS)}")
print(get_daily_idiom())

# Test Daily Discovery
from trainer.daily_discovery_content import DISCOVERY_CATEGORIES
print(list(DISCOVERY_CATEGORIES.keys()))
print(DISCOVERY_CATEGORIES['science'][0])

# Test Math Challenge
from trainer.math_challenge_content import MATH_CHALLENGES
print(f"Grade 1: {len(MATH_CHALLENGES[1])} problems")
print(MATH_CHALLENGES[1][0])
```

---

## 🚀 Final Verification

Before marking complete:

1. **Browser Testing**
   - [ ] All pages load without errors
   - [ ] Data displays correctly
   - [ ] No console errors (F12)
   - [ ] Mobile responsiveness works

2. **Functionality Testing**
   - [ ] Can save flashcards
   - [ ] Can take quizzes
   - [ ] Can view explanations
   - [ ] Streak tracking works

3. **Data Verification**
   - [ ] No offensive content
   - [ ] No copyright issues
   - [ ] Facts are accurate
   - [ ] No duplicate IDs

---

## 📝 Notes

- Start small! You don't need all 1,400+ items at launch. Start with 200-300 high-quality items.
- Gradually expand each section as the app grows.
- Kids learn better with diverse, varied content.
- Quality > Quantity — 100 excellent items beat 1000 mediocre ones.

---

## Next Steps

1. **Pick one section** to start with
2. **Use the corresponding prompt** from `GENERATE_DATA_PROMPTS.md`
3. **Generate data** with Claude/ChatGPT
4. **Add to the file** in the format shown
5. **Test with** `python manage.py shell`
6. **Verify in browser** at the URL provided
7. **Check this box** ✓ when complete
8. **Move to next section**

Good luck! 🎉
