from random import randint, choice, shuffle, sample

# ── helpers ───────────────────────────────────────────────────────────────────

def _time_str(h, m):
    suffix = 'am' if h < 12 else 'pm'
    h12 = h if h <= 12 else h - 12
    return f"{h12}:{m:02d}{suffix}"

def _add_minutes(h, m, delta):
    total = h * 60 + m + delta
    return total // 60 % 24, total % 60

# ── Grade 2 generators ────────────────────────────────────────────────────────

def _g2_times_table():
    a = randint(2, 9)
    b = randint(2, 9)
    return {'q': f'{a} × {b}', 'a': str(a * b), 'cat': 'Multiplication'}

def _g2_division_fact():
    b = randint(2, 9)
    ans = randint(2, 9)
    return {'q': f'{b * ans} ÷ {b}', 'a': str(ans), 'cat': 'Division'}

def _g2_missing_sub():
    ans = randint(2, 9)
    total = randint(ans + 3, 20)
    return {'q': f'{total} − ___ = {total - ans}', 'a': str(ans), 'cat': 'Missing Number'}

def _g2_change_cents():
    spend = randint(10, 48)
    return {'q': f'Change from 50¢ if I spend {spend}¢?', 'a': f'{50 - spend}¢', 'cat': 'Money'}

def _g2_number_pattern():
    start = randint(10, 200)
    step = choice([-2, -3, -5, 2, 3, 5])
    seq = [start + step * i for i in range(5)]
    next_val = start + step * 5
    return {'q': f'Next number: {", ".join(map(str, seq))}, ___', 'a': str(next_val), 'cat': 'Patterns'}

def _g2_time_add():
    h = randint(8, 21)
    m = choice([0, 15, 30, 45])
    delta_h = randint(1, 3)
    nh, nm = _add_minutes(h, m, delta_h * 60)
    return {'q': f'Time is {_time_str(h, m)}. What will it be in {delta_h} hour{"s" if delta_h>1 else ""}?',
            'a': _time_str(nh, nm), 'cat': 'Time'}

def _g2_missing_addend():
    a1 = randint(5, 15)
    b1 = randint(2, 10)
    total = a1 + b1
    a2 = randint(3, total - 1)
    return {'q': f'{a1} + {b1} = {a2} + ___', 'a': str(total - a2), 'cat': 'Missing Number'}

def _g2_subtraction():
    a = randint(200, 900)
    b = choice([100, 200, 300, 400, 500])
    if b >= a:
        b = 100
    return {'q': f'{a} subtract {b}', 'a': str(a - b), 'cat': 'Subtraction'}

def _g2_combined_total():
    a = randint(10, 40)
    b = randint(10, 40)
    names = choice([('Sally', 'Frazer'), ('Kim', 'Jordan'), ('Max', 'Lily')])
    item = choice(['stickers', 'coins', 'marbles', 'cards'])
    return {'q': f'{names[0]} has {a} {item}. {names[1]} has {b}. How many altogether?',
            'a': str(a + b), 'cat': 'Word Problem'}

def _g2_share_equally():
    divisor = choice([2, 3, 4, 5, 6, 8, 10])
    ans = randint(2, 8)
    total = divisor * ans
    item = choice(['candies', 'stickers', 'cookies', 'cards'])
    return {'q': f'Share {total} {item} equally between {divisor} friends. How many each?',
            'a': str(ans), 'cat': 'Division'}

def _g2_weight_division():
    unit_w = choice([2, 4, 5])
    total_w = choice([8, 12, 16, 20, 24])
    ans = total_w // unit_w
    return {'q': f'Each ball weighs {unit_w} oz. How many balls weigh {total_w} oz?',
            'a': str(ans), 'cat': 'Word Problem'}

def _g2_measure_convert():
    cm = randint(2, 12)
    return {'q': f'How many mm in {cm}cm?', 'a': str(cm * 10), 'cat': 'Measurement'}

def _g2_halve_number():
    n = randint(2, 20) * 2
    return {'q': f'Half of a number is {n // 2}. What is the number?', 'a': str(n), 'cat': 'Number Sense'}

def _g2_wheels():
    n = randint(2, 8)
    wheels = choice([2, 3, 4])
    vehicle = {2: 'bicycles', 3: 'tricycles', 4: 'cars'}[wheels]
    return {'q': f'How many wheels do {n} {vehicle} have?', 'a': str(n * wheels), 'cat': 'Word Problem'}

def _g2_time_bake():
    h = randint(9, 14)
    m = choice([0, 10, 20, 30, 40, 50])
    delta = choice([15, 20, 25, 30])
    nh, nm = _add_minutes(h, m, delta)
    return {'q': f'Put cake in oven for {delta} min at {_time_str(h, m)}. When ready?',
            'a': _time_str(nh, nm), 'cat': 'Time'}

# ── Grade 4 generators ────────────────────────────────────────────────────────

def _g4_decimal_add():
    a = randint(1, 9)
    b = randint(1, 9)
    ans = (a + b) / 10
    return {'q': f'Work out 0.{a} + 0.{b}', 'a': str(round(ans, 1)), 'cat': 'Decimals'}

def _g4_decimal_mul():
    a = randint(1, 9)
    b = randint(2, 9)
    return {'q': f'0.{a} × {b}', 'a': str(round(a * b / 10, 1)), 'cat': 'Decimals'}

def _g4_place_value_add():
    thousands = randint(1, 9) * 1000
    hundreds = randint(1, 9) * 100
    ones = randint(1, 9)
    return {'q': f'What is {thousands} + {hundreds} + {ones}?',
            'a': str(thousands + hundreds + ones), 'cat': 'Place Value'}

def _g4_place_value_missing():
    a = randint(1000, 9000)
    b_digit = randint(1, 9)
    b = b_digit * 10
    a_adj = (a // 100) * 100 + b + randint(1, 9)
    base = (a_adj // 1000) * 1000 + (a_adj % 10)
    return {'q': f'Fill in the missing number: {a_adj} = {base} + ___', 'a': str(b), 'cat': 'Place Value'}

def _g4_equiv_fraction():
    pairs = [('3/6', '1/2'), ('2/4', '1/2'), ('4/8', '1/2'), ('5/10', '1/2'),
             ('2/6', '1/3'), ('3/9', '1/3'), ('4/12', '1/3'),
             ('2/8', '1/4'), ('3/12', '1/4')]
    eq, simple = choice(pairs)
    distractors = ['1/3', '2/5', '4/9', '5/8', '3/7', '2/7', '3/8']
    options = [eq] + sample([d for d in distractors if d != simple], 3)
    shuffle(options)
    return {'q': f'Which fraction equals {simple}?  ' + '   '.join(options),
            'a': eq, 'cat': 'Fractions'}

def _g4_fraction_of():
    denoms = [(2, 3), (3, 4), (4, 5), (5, 6)]
    d, _ = choice(denoms)
    ans = randint(2, 8)
    total = d * ans
    return {'q': f'What is 1/{d} of {total}?', 'a': str(ans), 'cat': 'Fractions'}

def _g4_fraction_add_tenths():
    a = randint(1, 4)
    b = randint(1, 4)
    c = randint(1, 4)
    if a + b + c > 9:
        c = 1
    return {'q': f'Add together {a}/10, {b}/10 and {c}/10', 'a': f'{a+b+c}/10', 'cat': 'Fractions'}

def _g4_factors():
    nums = {12: '1, 2, 3, 4, 6, 12', 15: '1, 3, 5, 15', 16: '1, 2, 4, 8, 16',
            18: '1, 2, 3, 6, 9, 18', 20: '1, 2, 4, 5, 10, 20', 24: '1, 2, 3, 4, 6, 8, 12, 24'}
    n = choice(list(nums.keys()))
    return {'q': f'Write all the factors of {n}', 'a': nums[n], 'cat': 'Number Theory'}

def _g4_prime_identify():
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    non_primes = [4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21, 22, 24, 25]
    p1, p2 = sample(primes, 2)
    others = sample([n for n in non_primes if n not in (p1, p2)], 4)
    all_nums = sorted([p1, p2] + others)
    return {'q': f'Which two are prime?  {" ".join(map(str, all_nums))}',
            'a': f'{min(p1,p2)} and {max(p1,p2)}', 'cat': 'Number Theory'}

def _g4_divisible_by():
    divisor = choice([2, 3, 5, 10])
    pool = list(range(11, 99))
    yes = [n for n in pool if n % divisor == 0]
    no  = [n for n in pool if n % divisor != 0]
    chosen_yes = sample(yes, 2)
    chosen_no  = sample(no, 3)
    all_n = sorted(chosen_yes + chosen_no)
    return {'q': f'Which numbers are divisible by {divisor}?  {" ".join(map(str, all_n))}',
            'a': ' and '.join(map(str, sorted(chosen_yes))), 'cat': 'Divisibility'}

def _g4_round_ten():
    n = randint(101, 999)
    rounded = round(n / 10) * 10
    return {'q': f'Round {n} to the nearest ten', 'a': str(rounded), 'cat': 'Rounding'}

def _g4_large_compare():
    nums = [randint(100000, 999999) for _ in range(4)]
    return {'q': f'Largest of: {", ".join(map(str, nums))}', 'a': str(max(nums)), 'cat': 'Number Sense'}

def _g4_money_change():
    from_amt = choice([5, 10, 20])
    spend_d = randint(1, from_amt - 1)
    spend_c = choice([0, 10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90])
    spend = spend_d + spend_c / 100
    change = from_amt - spend
    return {'q': f'I have ${from_amt}. I spend ${spend:.2f}. Change?',
            'a': f'${change:.2f}', 'cat': 'Money'}

def _g4_unit_price():
    price = choice([1.50, 2.50, 3.50, 4.60, 5.00, 0.75, 1.25])
    qty = randint(2, 5)
    total = price * qty
    return {'q': f'One costs ${price:.2f}. How much for {qty}?',
            'a': f'${total:.2f}', 'cat': 'Money'}

def _g4_quarters():
    dollars = randint(1, 5)
    return {'q': f'How many quarters make ${dollars}?', 'a': str(dollars * 4), 'cat': 'Money'}

def _g4_mixed_number_add():
    whole = randint(2, 8)
    a = randint(1, 5)
    b = whole - a
    half1 = choice([True, False])
    half2 = not half1
    def fmt(n, half): return f'{n}½' if half else str(n)
    total = whole + (0.5 if half1 else 0) + (0.5 if half2 else 0)
    return {'q': f'Add {fmt(a, half1)}, {randint(1,4)} and {fmt(b, half2)}',
            'a': str(int(total) if total == int(total) else total), 'cat': 'Fractions'}

def _g4_journey_time():
    h = randint(7, 11)
    m = choice([0, 10, 20, 30, 40])
    dur_h = choice([1, 2, 3])
    dur_m = choice([0, 15, 20, 30, 45])
    nh, nm = _add_minutes(h, m, dur_h * 60 + dur_m)
    dur_str = f'{dur_h}h {dur_m}min' if dur_m else f'{dur_h} hours'
    return {'q': f'Set off at {_time_str(h, m)}. Journey takes {dur_str}. Arrive?',
            'a': _time_str(nh, nm), 'cat': 'Time'}

def _g4_perimeter_square():
    side = randint(3, 12)
    return {'q': f'Perimeter of a square with sides {side} inches?',
            'a': f'{side * 4} inches', 'cat': 'Geometry'}

def _g4_geometry_fact():
    facts = [
        ('How many vertices in a triangular pyramid?', '4'),
        ('How many faces on a cube?', '6'),
        ('How many edges on a triangular prism?', '9'),
        ('How many sides does a hexagon have?', '6'),
        ('How many sides does an octagon have?', '8'),
        ('How many sides does a pentagon have?', '5'),
        ('How many vertices does a square have?', '4'),
        ('How many right angles in a rectangle?', '4'),
    ]
    q, a = choice(facts)
    return {'q': q, 'a': a, 'cat': 'Geometry'}

def _g4_fraction_complement():
    num = randint(1, 4)
    den = randint(num + 1, 8)
    comp = den - num
    return {'q': f'{num}/{den} of children are boys. What fraction are girls?',
            'a': f'{comp}/{den}', 'cat': 'Fractions'}

def _g4_length_divide():
    total = choice([2, 3, 4, 5, 6])
    pieces = choice([2, 4, 5, 8, 10])
    cm = (total * 100) // pieces
    return {'q': f'{total}m rope cut into {pieces} equal pieces. Length each?',
            'a': f'{cm}cm', 'cat': 'Measurement'}

def _g4_sum_diff_puzzle():
    diff = choice([1, 2, 3, 4])
    for s in range(5, 20):
        if (s + diff) % 2 == 0:
            b = (s + diff) // 2
            a = s - b
            return {'q': f'Two numbers with sum {s} and difference {diff}.',
                    'a': f'{a} and {b}', 'cat': 'Number Sense'}
    return _g4_sum_diff_puzzle()

def _g4_change_multi_item():
    from_amt = 10
    p1 = choice([1.50, 2.00, 2.50, 3.00, 3.50, 4.00, 4.30])
    p2 = choice([0.50, 1.00, 1.50, 2.00, 2.50])
    total_spend = p1 + p2
    if total_spend >= from_amt:
        p1, p2 = 2.50, 1.50
        total_spend = 4.00
    change = from_amt - total_spend
    return {'q': f'Spend ${p1:.2f} and ${p2:.2f}. Change from $10?',
            'a': f'${change:.2f}', 'cat': 'Money'}

# ── Public API ────────────────────────────────────────────────────────────────

GRADE_GENERATORS = {
    'grade2': [
        _g2_times_table, _g2_division_fact, _g2_missing_sub, _g2_change_cents,
        _g2_number_pattern, _g2_time_add, _g2_missing_addend, _g2_subtraction,
        _g2_combined_total, _g2_share_equally, _g2_weight_division,
        _g2_measure_convert, _g2_halve_number, _g2_wheels, _g2_time_bake,
    ],
    'grade4': [
        _g4_decimal_add, _g4_decimal_mul, _g4_place_value_add, _g4_place_value_missing,
        _g4_equiv_fraction, _g4_fraction_of, _g4_fraction_add_tenths, _g4_factors,
        _g4_prime_identify, _g4_divisible_by, _g4_round_ten, _g4_large_compare,
        _g4_money_change, _g4_unit_price, _g4_quarters, _g4_journey_time,
        _g4_perimeter_square, _g4_geometry_fact, _g4_fraction_complement,
        _g4_length_divide, _g4_sum_diff_puzzle, _g4_change_multi_item,
        _g4_mixed_number_add,
    ],
    'mixed': None,  # handled below
}

GRADE_LABELS = {
    'grade2': '2nd Grade',
    'grade4': '4th Grade',
    'mixed':  'Mixed Challenge',
}

def generate_quiz(grade, count=16):
    if grade == 'mixed':
        gens = GRADE_GENERATORS['grade2'] + GRADE_GENERATORS['grade4']
    else:
        gens = GRADE_GENERATORS.get(grade, GRADE_GENERATORS['grade4'])

    questions = []
    seen = set()
    attempts = 0
    while len(questions) < count and attempts < count * 15:
        attempts += 1
        try:
            item = choice(gens)()
            key = item['q']
            if key not in seen:
                seen.add(key)
                questions.append({'question': item['q'], 'answer': item['a'], 'category': item['cat']})
        except Exception:
            pass
    return questions
