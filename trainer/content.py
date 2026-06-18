from random import choice, randint, shuffle

def generate_speed_problems(slug, count):
    def gen_make_10():
        a, b = randint(7,9), randint(3,8)
        return {'question': f'{a} + {b}', 'answer': str(a+b)}

    def gen_doubles():
        n = randint(4,9)
        return {'question': f'{n} + {n+1}', 'answer': str(2*n+1)}

    def gen_left_to_right():
        a, b = randint(100,999), randint(100,999)
        return {'question': f'{a} + {b}', 'answer': str(a+b)}

    def gen_comp_add():
        n, m = randint(290,398), randint(30,70)
        return {'question': f'{n} + {m}', 'answer': str(n+m)}

    def gen_count_up():
        a, b = randint(60,90), randint(55,88)
        big, small = max(a,b), min(a,b)
        return {'question': f'{big} - {small}', 'answer': str(big-small)}

    def gen_comp_sub():
        n, m = randint(400,600), randint(290,398)
        return {'question': f'{n} - {m}', 'answer': str(n-m)}

    def gen_mult_10():
        n, mult = randint(10,50), choice([10,100,1000])
        return {'question': f'{n} × {mult}', 'answer': str(n*mult)}

    def gen_mult_5():
        n = randint(1,40) * 2
        return {'question': f'{n} × 5', 'answer': str(n*5)}

    def gen_mult_9():
        n = randint(2,12)
        return {'question': f'{n} × 9', 'answer': str(n*9)}

    def gen_mult_11():
        attempts = 0
        while attempts < 10:
            a, b = randint(1,9), randint(1,8)
            if a + b < 10:
                return {'question': f'{a}{b} × 11', 'answer': str((a*10+b)*11)}
            attempts += 1
        # Fallback if can't find valid combo
        a, b = 2, 3
        return {'question': f'{a}{b} × 11', 'answer': str((a*10+b)*11)}

    def gen_squares_5():
        n = randint(3,9)
        return {'question': f'{n}5²', 'answer': str((n*10+5)**2)}

    def gen_magic_9():
        n = randint(2,9)
        return {'question': f'{n} × 9', 'answer': str(n*9)}

    def gen_vedic_eka():
        n = randint(2,8)
        return {'question': f'{n}5 × {n}5', 'answer': str((n*10+5)**2)}

    def gen_vedic_nik():
        n = randint(100,999)
        return {'question': f'1000 - {n}', 'answer': str(1000-n)}

    generators = {
        'make-10-first': gen_make_10,
        'doubles-near-doubles': gen_doubles,
        'left-to-right-addition': gen_left_to_right,
        'compensation-addition': gen_comp_add,
        'count-up-subtraction': gen_count_up,
        'compensation-subtraction': gen_comp_sub,
        'multiply-by-10-100': gen_mult_10,
        'multiply-by-5': gen_mult_5,
        'multiply-by-9': gen_mult_9,
        'multiply-by-11': gen_mult_11,
        'squares-ending-5': gen_squares_5,
        'magic-9': gen_magic_9,
        'vedic-ekaadhikena': gen_vedic_eka,
        'vedic-nikhilam': gen_vedic_nik,
    }

    if slug not in generators:
        return []

    problems = []
    gen = generators[slug]
    seen = set()
    attempts = 0
    max_attempts = count * 10  # Prevent infinite loops

    while len(problems) < count and attempts < max_attempts:
        attempts += 1
        try:
            prob = gen()
            key = prob['question']
            if key not in seen:
                problems.append(prob)
                seen.add(key)
        except:
            pass

    return problems

LESSONS = [
    # ============ ADDITION TRICKS ============
    {
        'slug': 'make-10-first',
        'title': '🎯 Make 10 First',
        'category': 'Addition',
        'level': 'Beginner',
        'age_range': '7-8',
        'emoji': '🎯',
        'summary': 'Break numbers to reach 10, then add remainder.',
        'description': [
            'To add 8 + 5: Break 5 into 2 + 3.',
            '8 + 2 = 10, then 10 + 3 = 13.',
            'This makes any addition easy and super fast!',
        ],
        'example': '8 + 5 = 8 + 2 + 3 = 10 + 3 = 13.',
        'challenge': {
            'question': 'What is 7 + 6 using the make-10 trick?',
            'answer': '13',
            'hint': 'Break 6 into 3 + 3. Add 3 to 7 to get 10, then add 3 more.',
            'explanation': '7 + 3 = 10, then 10 + 3 = 13.',
        },
    },
    {
        'slug': 'doubles-near-doubles',
        'title': '👯 Doubles & Near Doubles',
        'category': 'Addition',
        'level': 'Beginner',
        'age_range': '7-8',
        'emoji': '👯',
        'summary': 'Memorize doubles, then use for numbers close by.',
        'description': [
            'Know: 6 + 6 = 12 (double of 6).',
            'Then 6 + 7 = 6 + 6 + 1 = 12 + 1 = 13.',
            'Near doubles save you from counting on fingers!',
        ],
        'example': '6 + 7 = 6 + 6 + 1 = 13.',
        'challenge': {
            'question': 'What is 8 + 9 using doubles?',
            'answer': '17',
            'hint': 'Start with 8 + 8 = 16, then add 1 more.',
            'explanation': '8 + 8 = 16, so 8 + 9 = 17.',
        },
    },
    {
        'slug': 'left-to-right-addition',
        'title': '⬅️➡️ Left-to-Right Addition',
        'category': 'Addition',
        'level': 'Intermediate',
        'age_range': '8-9',
        'emoji': '⬅️',
        'summary': 'Add hundreds first, then tens, then ones.',
        'description': [
            'For 247 + 536:',
            'Add hundreds: 200 + 500 = 700.',
            'Add tens: 40 + 30 = 70. Then 700 + 70 = 770.',
            'Add ones: 7 + 6 = 13. Then 770 + 13 = 783.',
        ],
        'example': '247 + 536: 700 + 70 + 13 = 783.',
        'challenge': {
            'question': 'What is 324 + 215 using left-to-right?',
            'answer': '539',
            'hint': 'Add: 300+200, then 20+10, then 4+5.',
            'explanation': '500 + 30 + 9 = 539.',
        },
    },
    {
        'slug': 'compensation-addition',
        'title': '⚖️ Compensation Addition',
        'category': 'Addition',
        'level': 'Intermediate',
        'age_range': '8-9',
        'emoji': '⚖️',
        'summary': 'Round up one number, then subtract the extra.',
        'description': [
            'For 498 + 37:',
            'Round 498 up to 500.',
            'Add: 500 + 37 = 537.',
            'Subtract the 2 we added: 537 - 2 = 535.',
        ],
        'example': '498 + 37 = 500 + 37 - 2 = 535.',
        'challenge': {
            'question': 'What is 297 + 45 using compensation?',
            'answer': '342',
            'hint': 'Round 297 to 300, add 45, then subtract 3.',
            'explanation': '300 + 45 - 3 = 342.',
        },
    },
    {
        'slug': 'count-up-subtraction',
        'title': '🔢 Count Up to Subtract',
        'category': 'Subtraction',
        'level': 'Beginner',
        'age_range': '7-8',
        'emoji': '🔢',
        'summary': 'Count forward from the smaller number to the larger.',
        'description': [
            'For 72 - 68:',
            'Count up: 68 → 70 (that\'s +2), then 70 → 72 (that\'s +2).',
            'Total: 2 + 2 = 4.',
        ],
        'example': '72 - 68: 68→70→72 = +2+2 = 4.',
        'challenge': {
            'question': 'What is 85 - 78 by counting up?',
            'answer': '7',
            'hint': 'Count from 78 to 85. 78→80 (+2), then 80→85 (+5).',
            'explanation': '2 + 5 = 7.',
        },
    },
    {
        'slug': 'compensation-subtraction',
        'title': '⚖️ Compensation Subtraction',
        'category': 'Subtraction',
        'level': 'Intermediate',
        'age_range': '8-9',
        'emoji': '⚖️',
        'summary': 'Round the number being subtracted, then adjust.',
        'description': [
            'For 500 - 298:',
            'Round 298 to 300.',
            'Subtract: 500 - 300 = 200.',
            'Add back the 2: 200 + 2 = 202.',
        ],
        'example': '500 - 298 = 500 - 300 + 2 = 202.',
        'challenge': {
            'question': 'What is 600 - 397 using compensation?',
            'answer': '203',
            'hint': 'Round 397 to 400, then adjust.',
            'explanation': '600 - 400 + 3 = 203.',
        },
    },
    {
        'slug': 'multiply-by-10-100',
        'title': '0️⃣ Multiply by 10, 100, 1000',
        'category': 'Multiplication',
        'level': 'Beginner',
        'age_range': '7-8',
        'emoji': '0️⃣',
        'summary': 'Just add zeros to the right!',
        'description': [
            'Multiply by 10: Add one 0 to the right.',
            'Multiply by 100: Add two 0s to the right.',
            'Multiply by 1000: Add three 0s to the right.',
        ],
        'example': '45 × 100 = 4,500.',
        'challenge': {
            'question': 'What is 23 × 1000?',
            'answer': '23000',
            'hint': 'Add three zeros to 23.',
            'explanation': '23 × 1000 = 23,000.',
        },
    },
    {
        'slug': 'multiply-by-5',
        'title': '5️⃣ Multiply by 5 Fast',
        'category': 'Multiplication',
        'level': 'Beginner',
        'age_range': '7-8',
        'emoji': '5️⃣',
        'summary': 'Multiply by 10, then divide by 2.',
        'description': [
            'For 24 × 5:',
            'Multiply by 10: 24 × 10 = 240.',
            'Divide by 2: 240 ÷ 2 = 120.',
        ],
        'example': '24 × 5 = 240 ÷ 2 = 120.',
        'challenge': {
            'question': 'What is 34 × 5 using the trick?',
            'answer': '170',
            'hint': 'Multiply 34 by 10 to get 340, then divide by 2.',
            'explanation': '340 ÷ 2 = 170.',
        },
    },
    {
        'slug': 'multiply-by-9',
        'title': '9️⃣ Multiply by 9 Magic',
        'category': 'Multiplication',
        'level': 'Beginner',
        'age_range': '7-8',
        'emoji': '9️⃣',
        'summary': 'Multiply by 10, then subtract the original number.',
        'description': [
            'For 8 × 9:',
            'Multiply by 10: 8 × 10 = 80.',
            'Subtract the original: 80 - 8 = 72.',
        ],
        'example': '8 × 9 = 80 - 8 = 72.',
        'challenge': {
            'question': 'What is 7 × 9 using the trick?',
            'answer': '63',
            'hint': 'Multiply 7 by 10 to get 70, then subtract 7.',
            'explanation': '70 - 7 = 63.',
        },
    },
    {
        'slug': 'multiply-by-11',
        'title': '1️⃣1️⃣ Multiply by 11',
        'category': 'Multiplication',
        'level': 'Intermediate',
        'age_range': '8-9',
        'emoji': '1️⃣',
        'summary': 'Place digits apart, put their sum in the middle.',
        'description': [
            'For 23 × 11:',
            'Write 2 and 3 apart: 2 _ 3.',
            'Put their sum in the middle: 2 + 3 = 5.',
            'Result: 253.',
        ],
        'example': '23 × 11 = 2(2+3)3 = 253.',
        'challenge': {
            'question': 'What is 34 × 11 using the trick?',
            'answer': '374',
            'hint': 'Put 3 and 4 apart, then put 7 in the middle.',
            'explanation': '3 + 4 = 7, so 374.',
        },
    },
    {
        'slug': 'squares-ending-5',
        'title': '5️⃣² Squares Ending in 5',
        'category': 'Multiplication',
        'level': 'Intermediate',
        'age_range': '8-9',
        'emoji': '5️⃣',
        'summary': 'Vedic trick: multiply front digit by (digit+1), append 25.',
        'description': [
            'For 35²:',
            'Front digit is 3. Multiply: 3 × 4 = 12.',
            'Append 25: 1225.',
        ],
        'example': '35² = (3×4)(25) = 1,225.',
        'challenge': {
            'question': 'What is 65² using the trick?',
            'answer': '4225',
            'hint': 'Multiply 6 × 7 = 42, then append 25.',
            'explanation': '42 | 25 = 4,225.',
        },
    },
    {
        'slug': 'magic-9',
        'title': '🎩 Magic 9',
        'category': 'Fun Games',
        'level': 'Beginner',
        'age_range': '7-8',
        'emoji': '🎩',
        'summary': 'Any number × 9: digits always sum to 9.',
        'description': [
            'Try it: 7 × 9 = 63.',
            '6 + 3 = 9!',
            'Try: 8 × 9 = 72.',
            '7 + 2 = 9!',
        ],
        'example': '7 × 9 = 63 → 6 + 3 = 9.',
        'challenge': {
            'question': 'What is 6 × 9? Check if digits sum to 9.',
            'answer': '54',
            'hint': 'The answer is 54. Check: 5 + 4 = 9.',
            'explanation': 'Magic! All multiples of 9 have digits that sum to 9.',
        },
    },
    {
        'slug': 'vedic-ekaadhikena',
        'title': '🕉️ Ekādhikena Pūrveṇa',
        'category': 'Vedic Sutras',
        'level': 'Intermediate',
        'age_range': '8-9',
        'emoji': '🕉️',
        'summary': 'Vedic: Multiply numbers ending in 5.',
        'description': [
            'For 25 × 25:',
            'Front digit 2: 2 × 3 = 6.',
            'Append 25: 625.',
        ],
        'example': '25 × 25 = (2×3) | 25 = 625.',
        'challenge': {
            'question': 'What is 45 × 45?',
            'answer': '2025',
            'hint': 'Multiply 4 × 5 = 20, then append 25.',
            'explanation': '20 | 25 = 2,025.',
        },
    },
    {
        'slug': 'vedic-nikhilam',
        'title': '🕉️ Nikhilam Navataścaramaṃ',
        'category': 'Vedic Sutras',
        'level': 'Intermediate',
        'age_range': '8-9',
        'emoji': '🕉️',
        'summary': 'Vedic: Subtract from 100 or 1000 easily.',
        'description': [
            'For 1000 - 378:',
            'All from 9: 1000 - 378 → (10-3)(9-7)(10-8).',
            'Result: 622.',
        ],
        'example': '1000 - 378 = 622 using complement method.',
        'challenge': {
            'question': 'What is 1000 - 445?',
            'answer': '555',
            'hint': 'Use: all from 9 (except last from 10).',
            'explanation': '1000 - 445 = 555.',
        },
    },
]

LEVELS = ['Beginner', 'Intermediate', 'Expert']
CATEGORIES = ['Addition', 'Subtraction', 'Multiplication', 'Division', 'Fractions', 'Percentages', 'Fun Games', 'Vedic Sutras']
AGE_RANGES = ['7-8', '8-9', '9-10']

CHALLENGES = [
    {
        'slug': 'speed-challenge-1',
        'title': 'Speed Challenge: Mix & Match',
        'question': 'Quick! What is 34 × 11?',
        'answer': '374',
        'hint': 'Use the multiply by 11 trick: 3 + 4 = 7 in the middle.',
        'explanation': '3(7)4 = 374.',
    },
    {
        'slug': 'speed-challenge-2',
        'title': 'Speed Challenge: Magic 9s',
        'question': 'What is 8 × 9?',
        'answer': '72',
        'hint': 'Use 8 × 10 - 8 = 80 - 8.',
        'explanation': '72.',
    },
    {
        'slug': 'speed-challenge-3',
        'title': 'Speed Challenge: Squares',
        'question': 'What is 85² quickly?',
        'answer': '7225',
        'hint': 'Multiply 8 × 9 = 72, then append 25.',
        'explanation': '72 | 25 = 7,225.',
    },
]


def get_lesson(slug):
    return next((lesson for lesson in LESSONS if lesson['slug'] == slug), None)


def get_lessons_by_level(level):
    return [lesson for lesson in LESSONS if lesson['level'] == level]


def get_lessons_by_category(category):
    return [lesson for lesson in LESSONS if lesson['category'] == category]


def get_lessons_by_age(age_range):
    return [lesson for lesson in LESSONS if lesson['age_range'] == age_range]


def get_categories():
    return CATEGORIES


def get_challenge(slug=None):
    if slug:
        return next((item for item in CHALLENGES if item['slug'] == slug), None)
    return choice(CHALLENGES)
