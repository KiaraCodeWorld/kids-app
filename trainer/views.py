import re
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from datetime import date
from .content import (
    LEVELS,
    get_categories,
    get_challenge,
    get_lesson,
    get_lessons_by_category,
    get_lessons_by_level,
    AGE_RANGES,
    get_lessons_by_age,
    generate_speed_problems,
)
from .spelling_content import get_spelling_words, SPELLING_LEVELS, get_word_metadata, get_vocabulary_words, VOCABULARY_WORDS
from .quiz_content import generate_quiz, GRADE_LABELS
from .llm_service import get_llm_helper
from .models import SavedVocabularyWord, SavedFlashcard
from .word_explorer_content import (
    WORD_TIERS, TIER_LABELS, IDIOMS, BADGES,
    get_daily_words, get_daily_idiom, compute_new_badges,
)
from .daily_discovery_content import (
    CATEGORY_META, ORDERED_CATEGORIES, CATEGORY_POOLS,
    get_daily_item, get_item_by_id,
)
from .news_fetcher import get_live_news_cached, pick_news_item
from .math_challenge_content import (
    get_all_questions, filter_questions, get_topics, get_quiz_session,
)


def home(request):
    level_groups = [
        {
            'level': level,
            'lessons': get_lessons_by_level(level),
        }
        for level in LEVELS
    ]
    category_groups = [
        {
            'category': category,
            'lessons': get_lessons_by_category(category),
        }
        for category in get_categories()
    ]
    age_groups = [
        {
            'age_range': age_range,
            'lessons': get_lessons_by_age(age_range),
        }
        for age_range in AGE_RANGES
    ]
    from . import mission_service
    player = mission_service.get_player(request)
    dash = mission_service.player_dashboard(player)

    return render(request, 'trainer/home.html', {
        'levels': LEVELS,
        'level_groups': level_groups,
        'category_groups': category_groups,
        'age_groups': age_groups,
        'dash': dash,
    })


def lesson_detail(request, slug):
    lesson = get_lesson(slug)
    if lesson is None:
        return render(request, 'trainer/home.html', {'levels': LEVELS, 'lessons_by_level': {level: get_lessons_by_level(level) for level in LEVELS}})

    feedback = ''
    feedback_class = ''
    show_hint = False
    explanation = ''
    submitted_answer = ''

    if request.method == 'POST':
        submitted_answer = request.POST.get('answer', '').strip()
        correct_answer = lesson['challenge']['answer']
        if submitted_answer == correct_answer:
            feedback = 'Nice work! That answer is correct.'
            feedback_class = 'success'
            explanation = lesson['challenge']['explanation']
        else:
            feedback = 'That is not quite right yet. Keep trying!' 
            feedback_class = 'error'
            show_hint = True
            explanation = lesson['challenge']['explanation']

    return render(request, 'trainer/concept_detail.html', {
        'lesson': lesson,
        'feedback': feedback,
        'feedback_class': feedback_class,
        'show_hint': show_hint,
        'explanation': explanation,
        'submitted_answer': submitted_answer,
    })


def challenge(request, slug=None):
    challenge_item = get_challenge(slug)
    if challenge_item is None:
        challenge_item = get_challenge()

    feedback = ''
    feedback_class = ''
    show_hint = False
    explanation = ''
    user_answer = ''

    if request.method == 'POST':
        user_answer = request.POST.get('answer', '').strip()
        if user_answer == challenge_item['answer']:
            feedback = 'Great job! You solved it correctly.'
            feedback_class = 'success'
            explanation = challenge_item['explanation']
        else:
            feedback = 'Not quite yet. Try the hint and think it through again.'
            feedback_class = 'error'
            show_hint = True
            explanation = challenge_item['explanation']

    return render(request, 'trainer/challenge.html', {
        'challenge': challenge_item,
        'feedback': feedback,
        'feedback_class': feedback_class,
        'show_hint': show_hint,
        'explanation': explanation,
        'user_answer': user_answer,
    })


def speed_test(request, slug):
    lesson = get_lesson(slug)
    if lesson is None:
        raise Http404('Lesson not found')

    problems = generate_speed_problems(slug, 30)
    if not problems:
        raise Http404('No problems available for this trick')

    return render(request, 'trainer/speed_test.html', {
        'lesson': lesson,
        'problems_json': json.dumps(problems),
    })


def spelling_home(request):
    return render(request, 'trainer/spelling_home.html', {
        'levels': SPELLING_LEVELS,
    })


def spelling_test(request, level):
    if level not in SPELLING_LEVELS:
        raise Http404('Invalid spelling level')

    words = get_spelling_words(level, count=10)
    words_json = json.dumps([
        {
            'word': w['word'],
            'level': w['level'],
            'hint': w['hint'],
        }
        for w in words
    ])

    return render(request, 'trainer/spelling_test.html', {
        'level': level,
        'words_json': words_json,
        'word_count': len(words),
    })


@csrf_exempt
def api_explain_word(request, word):
    if not word or len(word) < 2:
        return JsonResponse({'error': 'Invalid word'}, status=400)

    llm = get_llm_helper()
    if not llm:
        return JsonResponse({
            'explanation': f'Tips for spelling "{word}": Break it into syllables and say each one slowly.',
            'cached': False,
        })

    explanation = llm.get_explanation_safe(word, 'general')
    return JsonResponse({
        'explanation': explanation,
        'word': word,
    })


@csrf_exempt
def api_math_hint(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    try:
        data = json.loads(request.body)
        question = data.get('question', '')
        trick = data.get('trick', '')
        answer = data.get('answer', '')
        prompt = data.get('prompt', '')

        if not question:
            return JsonResponse({'hint': 'Think carefully about each step!'}, status=200)

        llm = get_llm_helper()
        if not llm:
            return JsonResponse({'hint': '💡 Break it into smaller parts!'}, status=200)

        # Use cache to speed up repeated requests
        cache_key = f"math_hint:{question}"
        cached_hint = cache.get(cache_key)
        if cached_hint:
            return JsonResponse({'hint': cached_hint, 'cached': True}, status=200)

        try:
            response = llm.client.chat.completions.create(
                model="google/gemma-4-31b-it:free",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
            )

            hint = response.choices[0].message.content.strip()
            cache.set(cache_key, hint, 60 * 60)  # Cache for 1 hour

            return JsonResponse({'hint': hint, 'cached': False}, status=200)
        except Exception as e:
            return JsonResponse({'hint': f'⚡ Smart tip: {answer} is your goal!'}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)


def vocabulary_home(request):
    return render(request, 'trainer/vocabulary_home.html', {
        'levels': list(VOCABULARY_WORDS.keys()),
    })


def vocabulary_lesson(request, level):
    if level not in VOCABULARY_WORDS:
        raise Http404('Invalid vocabulary level')

    words = get_vocabulary_words(level, count=3)
    words_json = json.dumps([
        {
            'word': w['word'],
            'definition': w['definition'],
            'usage': w['usage'],
        }
        for w in words
    ])

    return render(request, 'trainer/vocabulary_lesson.html', {
        'level': level,
        'words_json': words_json,
        'word_count': len(words),
    })


@csrf_exempt
def api_word_explanation(request, word):
    """Get detailed explanation of a word from LLM"""
    if not word or len(word) < 2:
        return JsonResponse({'error': 'Invalid word'}, status=400)

    llm = get_llm_helper()
    cache_key = f"word_explain:{word.lower()}"

    # Check cache first
    cached = cache.get(cache_key)
    if cached:
        return JsonResponse(cached)

    if not llm:
        return JsonResponse({
            'explanation': f'Check a dictionary for "{word}"',
            'examples': [],
        })

    prompt = f"""Explain the word "{word}" in this exact format, using plain markdown (no ### headers):

**Meaning:** One clear sentence.
**Origin:** One sentence on where the word comes from.
**Synonyms:** word1, word2, word3
**Examples:**
* First real-life example sentence.
* Second real-life example sentence.
**Memory Trick:** One catchy way to remember it.

Be concise. No extra commentary."""

    try:
        response = llm.client.chat.completions.create(
            model="google/gemma-4-31b-it:free",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=250,
        )

        explanation = response.choices[0].message.content
        result = {
            'word': word,
            'explanation': explanation,
        }
        cache.set(cache_key, result, 60 * 60 * 24)  # Cache for 24 hours
        return JsonResponse(result)

    except Exception as e:
        return JsonResponse({
            'explanation': f'"{word}" is an interesting word. Look it up in a dictionary for more details.',
        })


def mental_quiz_home(request):
    return render(request, 'trainer/mental_quiz_home.html', {'grade_labels': GRADE_LABELS})


def mental_quiz(request, grade):
    if grade not in GRADE_LABELS:
        raise Http404('Invalid grade')
    questions = generate_quiz(grade, count=16)
    return render(request, 'trainer/mental_quiz.html', {
        'grade': grade,
        'grade_label': GRADE_LABELS[grade],
        'questions_json': json.dumps(questions),
        'question_count': len(questions),
    })


def saved_vocabulary(request):
    """View all saved vocabulary words"""
    saved_words = SavedVocabularyWord.objects.all()
    return render(request, 'trainer/saved_vocabulary.html', {
        'saved_words': saved_words,
        'word_count': saved_words.count(),
    })


@csrf_exempt
def api_save_word(request):
    """Save a vocabulary word to personal list"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    try:
        data = json.loads(request.body)
        word = data.get('word', '').strip()
        definition = data.get('definition', '')
        usage = data.get('usage', '')
        level = data.get('level', 'Beginner')

        if not word:
            return JsonResponse({'error': 'Word required'}, status=400)

        # Save or update word
        saved, created = SavedVocabularyWord.objects.update_or_create(
            word=word,
            defaults={
                'definition': definition,
                'usage': usage,
                'level': level,
            }
        )

        return JsonResponse({
            'success': True,
            'message': 'Word saved!' if created else 'Word updated!',
            'word': word,
            'is_new': created,
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_check_saved_word(request, word):
    """Check if a word is already saved"""
    try:
        saved = SavedVocabularyWord.objects.filter(word=word.lower()).exists()
        return JsonResponse({
            'word': word,
            'is_saved': saved,
        })
    except Exception as e:
        return JsonResponse({'is_saved': False})


@csrf_exempt
def api_get_saved_words(request):
    """Get all saved words as JSON"""
    try:
        saved_words = SavedVocabularyWord.objects.values('word', 'definition', 'usage', 'level', 'saved_at')
        words_list = list(saved_words)

        # Generate CSV format
        csv_content = "Word,Definition,Usage,Level,Saved Date\n"
        for word in words_list:
            csv_content += f'"{word["word"]}","{word["definition"]}","{word["usage"]}","{word["level"]}","{word["saved_at"].strftime("%Y-%m-%d %H:%M")}"\n'

        return JsonResponse({
            'words': words_list,
            'count': len(words_list),
            'csv_content': csv_content,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ── Brain Quest: Daily Mission ──────────────────────────────────────────────
from . import mission_service


def mission_home(request):
    """Mission intro: mascot greeting + Start Today's Quest CTA (or done state)."""
    player = mission_service.get_player(request)
    dash = mission_service.player_dashboard(player)
    return render(request, 'trainer/mission_home.html', {'dash': dash})


def profile_me(request):
    """Progress dashboard: mascot, level, streak, badges, subject accuracy, history."""
    from .mission_engine import SUBJECT_META
    player = mission_service.get_player(request)
    dash = mission_service.player_dashboard(player)

    # Subject accuracy bars
    subjects = []
    for subj, meta in SUBJECT_META.items():
        if subj not in ('math', 'vocabulary', 'words', 'spelling'):
            continue
        st = (player.subject_stats or {}).get(subj, {})
        total = st.get('total', 0)
        correct = st.get('correct', 0)
        acc = round(correct / total * 100) if total else 0
        subjects.append({
            'label': meta['label'], 'emoji': meta['emoji'],
            'accuracy': acc, 'total': total, 'has_data': total > 0,
        })
    subjects.sort(key=lambda s: (-s['has_data'], -s['accuracy']))

    # Recent missions
    recent = []
    for m in player.missions.filter(completed=True)[:7]:
        recent.append({
            'date': m.mission_date,
            'score': m.score, 'total': m.total,
            'xp': m.xp_earned,
            'recovery': m.is_recovery,
        })

    return render(request, 'trainer/profile_me.html', {
        'dash': dash,
        'subjects': subjects,
        'recent': recent,
        'accuracy': player.accuracy(),
        'total_missions': player.total_missions,
        'total_correct': player.total_correct,
        'total_items': player.total_items,
        'longest_streak': player.longest_streak,
    })


def daily_mission(request):
    """Full-screen distraction-free mission flow."""
    player = mission_service.get_player(request)
    record, items, state = mission_service.get_or_build_today_mission(player)
    dash = mission_service.player_dashboard(player)

    return render(request, 'trainer/daily_mission.html', {
        'items_json': json.dumps(items),
        'record_id': record.id,
        'is_recovery': state['is_recovery'],
        'already_done': state['completed_today'] and record.completed,
        'mascot_name': dash['mascot_name'],
        'mascot_emoji': dash['mascot_emoji'],
        'dash': dash,
    })


@csrf_exempt
def api_mission_complete(request):
    """Finalize the mission: award XP, update streak, return summary."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    player = mission_service.get_player(request)
    record_id = data.get('record_id')
    results = data.get('results', [])

    record = player.missions.filter(id=record_id).first()
    if not record:
        # rebuild today's record as a fallback
        record, _items, _state = mission_service.get_or_build_today_mission(player)

    summary = mission_service.complete_mission(player, record, results)
    return JsonResponse(summary)


@csrf_exempt
def api_mascot_react(request):
    """Per-item mascot reaction during the mission (stateless)."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    from . import mascot as mascot_mod
    reaction = mascot_mod.react_to_answer(
        bool(data.get('correct')), int(data.get('streak_in_mission', 0)))
    return JsonResponse(reaction)


@csrf_exempt
def api_save_mascot(request):
    """Set/rename the mascot and species, plus grade."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    try:
        data = json.loads(request.body or '{}')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    player = mission_service.get_player(request)
    name = (data.get('mascot_name') or '').strip()[:40]
    species = (data.get('mascot_species') or '').strip()[:20]
    grade = data.get('grade_level')
    if name:
        player.mascot_name = name
    if species:
        player.mascot_species = species
    if grade is not None:
        try:
            player.grade_level = max(1, min(8, int(grade)))
        except (ValueError, TypeError):
            pass
    player.save()
    return JsonResponse({'success': True, 'mascot_name': player.mascot_name,
                         'mascot_species': player.mascot_species,
                         'grade_level': player.grade_level})


def flashcard_review(request):
    """Flashcard review page for saved words and idioms."""
    cards = SavedFlashcard.objects.all()
    return render(request, 'trainer/flashcard_review.html', {
        'cards_json': json.dumps([
            {
                'id': c.id,
                'card_type': c.card_type,
                'front_text': c.front_text,
                'back_text': c.back_text,
                'example': c.example,
                'emoji': c.emoji,
                'extra_json': c.extra_json,
            }
            for c in cards
        ]),
        'total': cards.count(),
    })


@csrf_exempt
def api_save_flashcard(request):
    """Save or toggle a flashcard (word or idiom)."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    try:
        data = json.loads(request.body)
        card_type = data.get('card_type', 'word')
        front_text = data.get('front_text', '').strip()
        back_text = data.get('back_text', '')
        example = data.get('example', '')
        emoji = data.get('emoji', '')
        extra_json = data.get('extra_json', {})

        if not front_text:
            return JsonResponse({'error': 'front_text required'}, status=400)
        if card_type not in ('word', 'idiom'):
            return JsonResponse({'error': 'Invalid card_type'}, status=400)

        card, created = SavedFlashcard.objects.update_or_create(
            card_type=card_type,
            front_text=front_text,
            defaults={
                'back_text': back_text,
                'example': example,
                'emoji': emoji,
                'extra_json': extra_json,
            }
        )

        return JsonResponse({
            'success': True,
            'saved': True,
            'is_new': created,
            'message': 'Saved to flashcards!' if created else 'Flashcard updated!',
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def api_check_flashcard(request, card_type, front_text):
    """Check if a flashcard is saved."""
    saved = SavedFlashcard.objects.filter(card_type=card_type, front_text=front_text).exists()
    return JsonResponse({'is_saved': saved})


@csrf_exempt
def api_delete_flashcard(request):
    """Delete a saved flashcard by id."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    try:
        data = json.loads(request.body)
        card_id = data.get('id')
        SavedFlashcard.objects.filter(id=card_id).delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# ── Word Explorer Academy ──────────────────────────────────────────────────

def _we_session(request):
    """Return the word explorer session dict, creating it if needed."""
    if 'we' not in request.session:
        request.session['we'] = {
            'seen': {},        # {tier: [word_id, ...]}
            'seen_idioms': [],
            'badges': [],
            'streak': 0,
            'last_date': None,
        }
    return request.session['we']


def word_explorer_home(request):
    return render(request, 'trainer/word_explorer_home.html', {
        'tiers': TIER_LABELS,
    })


def word_explorer_lesson(request, tier):
    if tier not in WORD_TIERS:
        raise Http404('Invalid tier')

    we = _we_session(request)
    seen_ids = we['seen'].get(tier, [])
    words = get_daily_words(tier, seen_ids)

    # Update streak display (not incremented here — happens on session complete)
    streak = we.get('streak', 0)
    last_date = we.get('last_date')
    today = str(date.today())
    already_done_today = (last_date == today)

    return render(request, 'trainer/word_explorer_lesson.html', {
        'tier': tier,
        'tier_info': TIER_LABELS[tier],
        'words_json': json.dumps(words),
        'word_count': len(words),
        'streak': streak,
        'already_done_today': already_done_today,
        'badges_json': json.dumps(we.get('badges', [])),
        'total_seen': sum(len(v) for v in we['seen'].values()),
    })


def idiom_island(request):
    we = _we_session(request)
    idiom = get_daily_idiom(we.get('seen_idioms', []))
    return render(request, 'trainer/idiom_island.html', {
        'idiom': idiom,
        'streak': we.get('streak', 0),
        'total_idioms': len(we.get('seen_idioms', [])),
    })


@csrf_exempt
def api_we_complete_session(request):
    """Mark a Word Explorer session complete: update streak, seen words, badges."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    try:
        data = json.loads(request.body)
        tier = data.get('tier', '')
        completed_ids = data.get('word_ids', [])   # word ids the kid went through
        has_challenge = data.get('has_challenge', False)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    if tier not in WORD_TIERS:
        return JsonResponse({'error': 'Invalid tier'}, status=400)

    we = _we_session(request)
    today = str(date.today())

    # Update streak
    if we.get('last_date') == today:
        streak = we.get('streak', 0)  # already did today — keep streak
    elif we.get('last_date') == str(date.fromordinal(date.today().toordinal() - 1)):
        streak = we.get('streak', 0) + 1  # consecutive day
    else:
        streak = 1  # reset or first time

    we['streak'] = streak
    we['last_date'] = today

    # Update seen words
    seen_tier = we['seen'].get(tier, [])
    for wid in completed_ids:
        if wid not in seen_tier:
            seen_tier.append(wid)
    we['seen'][tier] = seen_tier

    total_seen = sum(len(v) for v in we['seen'].values())
    total_idioms = len(we.get('seen_idioms', []))
    earned = we.get('badges', [])

    new_badges = compute_new_badges(total_seen, streak, total_idioms, earned, has_challenge)
    we['badges'] = earned + new_badges

    request.session['we'] = we
    request.session.modified = True

    badge_details = [BADGES[b] for b in new_badges if b in BADGES]

    return JsonResponse({
        'streak': streak,
        'total_seen': total_seen,
        'new_badges': badge_details,
        'all_badges': we['badges'],
    })


@csrf_exempt
def api_we_complete_idiom(request):
    """Mark an idiom as seen."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=400)

    try:
        data = json.loads(request.body)
        idiom_id = data.get('idiom_id', '')
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    we = _we_session(request)
    seen = we.get('seen_idioms', [])
    if idiom_id and idiom_id not in seen:
        seen.append(idiom_id)
    we['seen_idioms'] = seen

    total_idioms = len(seen)
    earned = we.get('badges', [])
    new_badges = compute_new_badges(
        sum(len(v) for v in we['seen'].values()),
        we.get('streak', 0),
        total_idioms,
        earned,
        False,
    )
    we['badges'] = earned + new_badges
    request.session['we'] = we
    request.session.modified = True

    badge_details = [BADGES[b] for b in new_badges if b in BADGES]
    return JsonResponse({
        'total_idioms': total_idioms,
        'new_badges': badge_details,
    })


@csrf_exempt
def api_we_word_explanation(request, word, tier):
    """Age-adaptive LLM explanation for a Word Explorer word."""
    if not word or tier not in WORD_TIERS:
        return JsonResponse({'error': 'Invalid parameters'}, status=400)

    # Find context for the word in the tier
    context = ''
    for w in WORD_TIERS.get(tier, []):
        if w['word'] == word:
            context = w.get('context', '')
            break

    llm = get_llm_helper()
    if not llm:
        return JsonResponse({'explanation': f'"{word}" is a great word to learn! Try using it in a sentence.'})

    explanation = llm.explain_word_for_tier(word, tier, context)
    return JsonResponse({'word': word, 'tier': tier, 'explanation': explanation})


# ── Daily Discovery ─────────────────────────────────────────────────────────

def _dd_session(request):
    if 'dd' not in request.session:
        request.session['dd'] = {
            'seen': {cat: [] for cat in ORDERED_CATEGORIES},
            'streak': 0,
            'last_date': None,
            'completed_today': [],
        }
    return request.session['dd']


def daily_discovery_home(request):
    sess = _dd_session(request)
    today = str(date.today())

    # Streak logic
    last = sess.get('last_date')
    from datetime import timedelta
    yesterday = str(date.today() - timedelta(days=1))
    if last == today:
        pass  # same day
    elif last == yesterday:
        sess['streak'] = sess.get('streak', 0) + 1
        sess['last_date'] = today
    else:
        sess['streak'] = 1
        sess['last_date'] = today
    request.session.modified = True

    # Pre-fetch live news for the card preview (non-blocking: uses cache or falls back)
    live_news = get_live_news_cached(cache)

    # Build category cards with today's item preview
    cards = []
    for cat in ORDERED_CATEGORIES:
        meta = CATEGORY_META[cat]
        seen = sess['seen'].get(cat, [])
        if cat == 'news':
            item = pick_news_item(live_news, seen) if live_news else get_daily_item('news', seen)
        else:
            item = get_daily_item(cat, seen)
        completed = cat in sess.get('completed_today', [])
        cards.append({
            'category': cat,
            'label': meta['label'],
            'emoji': meta['emoji'],
            'color': meta['color'],
            'bg': meta['bg'],
            'teaser': item['teaser'] if item else '',
            'title': item['title'] if item else meta['label'],
            'completed': completed,
            'count': len(CATEGORY_POOLS.get(cat, [])),
        })

    return render(request, 'trainer/daily_discovery_home.html', {
        'cards': cards,
        'streak': sess.get('streak', 0),
        'completed_today': len(sess.get('completed_today', [])),
        'total_categories': len(ORDERED_CATEGORIES),
    })


def daily_discovery_item(request, category):
    if category not in ORDERED_CATEGORIES:
        raise Http404

    sess = _dd_session(request)
    seen = sess['seen'].get(category, [])
    meta = CATEGORY_META[category]

    if category == 'news':
        live_articles = get_live_news_cached(cache)
        item = pick_news_item(live_articles, seen) if live_articles else get_daily_item('news', seen)
    else:
        item = get_daily_item(category, seen)

    if not item:
        raise Http404

    total = len(live_articles) if category == 'news' and live_articles else len(CATEGORY_POOLS.get(category, []))

    return render(request, 'trainer/daily_discovery_item.html', {
        'item': item,
        'meta': meta,
        'category': category,
        'completed': category in sess.get('completed_today', []),
        'streak': sess.get('streak', 0),
        'seen_count': len(seen),
        'total': total,
        'is_news': category == 'news',
    })


@csrf_exempt
def api_dd_complete(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    data = json.loads(request.body or '{}')
    category = data.get('category', '')
    item_id = data.get('item_id', '')

    if category not in ORDERED_CATEGORIES:
        return JsonResponse({'error': 'Invalid category'}, status=400)

    sess = _dd_session(request)
    today = str(date.today())

    # Add to seen
    if item_id and item_id not in sess['seen'].get(category, []):
        sess['seen'].setdefault(category, []).append(item_id)

    # Track completed today
    completed = sess.setdefault('completed_today', [])
    if category not in completed:
        completed.append(category)

    # Streak
    if sess.get('last_date') != today:
        sess['streak'] = sess.get('streak', 0) + 1
        sess['last_date'] = today

    request.session.modified = True
    return JsonResponse({
        'ok': True,
        'streak': sess['streak'],
        'completed_today': len(sess['completed_today']),
        'total_categories': len(ORDERED_CATEGORIES),
    })


@csrf_exempt
def api_dd_ai_explain(request):
    """Expand a Daily Discovery item with deeper AI context."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    data = json.loads(request.body or '{}')
    title = data.get('title', '')
    category = data.get('category', '')
    item_id = data.get('item_id', '')

    item = get_item_by_id(item_id)
    body_excerpt = item.get('body', '')[:300] if item else ''

    llm = get_llm_helper()
    if not llm:
        return JsonResponse({'explanation': 'AI is offline — try again later.'})

    explanation = llm.explain_discovery_item(title, category, body_excerpt)
    return JsonResponse({'explanation': explanation})


# ── Math Challenge ───────────────────────────────────────────────────────────

def _mc_session(request):
    if 'mc' not in request.session:
        request.session['mc'] = {
            'grade': 4,
            'score': 0,
            'total': 0,
            'streak': 0,
            'session_ids': [],
            'history': [],  # [{id, correct, user_answer}]
        }
    return request.session['mc']


def math_challenge_home(request):
    all_q = get_all_questions()
    topics = get_topics(all_q)
    grade_counts = {}
    for q in all_q:
        g = q.get('grade', 4)
        grade_counts[g] = grade_counts.get(g, 0) + 1

    mc = _mc_session(request)
    return render(request, 'trainer/math_challenge_home.html', {
        'total_questions': len(all_q),
        'topics': topics,
        'grade_counts': sorted(grade_counts.items()),
        'score': mc.get('score', 0),
        'total_answered': mc.get('total', 0),
        'streak': mc.get('streak', 0),
    })


def math_challenge_quiz(request, grade=4):
    try:
        grade = int(grade)
    except (TypeError, ValueError):
        grade = 4

    all_q = get_all_questions()
    pool = filter_questions(all_q, grade=grade)
    if not pool:
        pool = all_q  # fallback: all grades

    mc = _mc_session(request)
    seen_ids = mc.get('session_ids', [])
    unseen = [q for q in pool if q['id'] not in seen_ids]
    if not unseen:
        unseen = pool  # reset when all seen

    quiz = get_quiz_session(unseen, count=10)

    # Store current session ids
    mc['session_ids'] = seen_ids + [q['id'] for q in quiz]
    request.session.modified = True

    return render(request, 'trainer/math_challenge_quiz.html', {
        'questions_json': json.dumps(quiz),
        'grade': grade,
        'question_count': len(quiz),
        'score': mc.get('score', 0),
        'streak': mc.get('streak', 0),
    })


@csrf_exempt
def api_mc_submit(request):
    """Submit an answer for a math challenge question."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    q_id = data.get('question_id', '')
    user_answer = str(data.get('answer', '')).strip()
    correct_answer = str(data.get('correct_answer', '')).strip()
    question_text = data.get('question', '')
    topic = data.get('topic', 'Math')
    grade = int(data.get('grade', 4))

    # Flexible matching: case-insensitive, strip punctuation for open answers
    def normalize(s):
        return re.sub(r'[^a-z0-9.]', '', s.lower().strip())

    is_correct = normalize(user_answer) == normalize(correct_answer)

    mc = _mc_session(request)
    mc['total'] = mc.get('total', 0) + 1
    if is_correct:
        mc['score'] = mc.get('score', 0) + 1
        mc['streak'] = mc.get('streak', 0) + 1
    else:
        mc['streak'] = 0

    history = mc.get('history', [])
    history.append({'id': q_id, 'correct': is_correct, 'user_answer': user_answer})
    mc['history'] = history[-50:]  # keep last 50

    request.session.modified = True

    return JsonResponse({
        'correct': is_correct,
        'correct_answer': correct_answer,
        'score': mc['score'],
        'total': mc['total'],
        'streak': mc['streak'],
    })


@csrf_exempt
def api_mc_hint(request):
    """Get a gentle hint for a math question."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    question = data.get('question', '')
    topic = data.get('topic', 'Math')
    grade = int(data.get('grade', 4))

    if not question:
        return JsonResponse({'hint': 'Read the question carefully — what information is given?'})

    llm = get_llm_helper()
    if not llm:
        return JsonResponse({'hint': f'Think about {topic}. Break the problem into smaller steps!'})

    hint = llm.get_math_hint(question, topic, grade)
    return JsonResponse({'hint': hint})


@csrf_exempt
def api_mc_explain(request):
    """Get full step-by-step explanation for a math question."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    question = data.get('question', '')
    topic = data.get('topic', 'Math')
    grade = int(data.get('grade', 4))
    user_answer = data.get('user_answer', '')

    if not question:
        return JsonResponse({'explanation': 'No question provided.'})

    llm = get_llm_helper()
    if not llm:
        return JsonResponse({'explanation': 'AI is offline — try again later.'})

    explanation = llm.explain_math_question(question, topic, grade, user_answer or None)
    return JsonResponse({'explanation': explanation})


# ── User Profile & Settings ──────────────────────────────────────────────────

@login_required
def profile_settings(request):
    from .models import UserProfile
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.display_name = request.POST.get('display_name', '').strip()[:80]
        grade = request.POST.get('grade_level', '4')
        try:
            profile.grade_level = int(grade)
        except ValueError:
            pass
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        profile.save()
        messages.success(request, 'Profile updated!')
        return redirect('trainer:profile_settings')

    return render(request, 'trainer/profile_settings.html', {'profile': profile})


@login_required
def api_profile_stats(request):
    from .models import UserProfile
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return JsonResponse({
        'display_name': profile.get_display_name(),
        'avatar_url': profile.get_avatar_url(),
        'grade_level': profile.grade_level,
        'total_stars': profile.total_stars,
        'total_correct': profile.total_correct,
        'total_questions': profile.total_questions,
        'accuracy': profile.accuracy(),
    })
