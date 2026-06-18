from django.urls import path
from . import views

app_name = 'trainer'

urlpatterns = [
    path('', views.home, name='home'),
    path('lesson/<slug:slug>/', views.lesson_detail, name='lesson_detail'),
    path('speed/<slug:slug>/', views.speed_test, name='speed_test'),
    path('challenge/', views.challenge, name='challenge'),
    path('challenge/<slug:slug>/', views.challenge, name='challenge_specific'),
    path('spelling/', views.spelling_home, name='spelling_home'),
    path('spelling/<str:level>/', views.spelling_test, name='spelling_test'),
    path('vocabulary/', views.vocabulary_home, name='vocabulary_home'),
    path('vocabulary/<str:level>/', views.vocabulary_lesson, name='vocabulary_lesson'),
    path('mental-quiz/', views.mental_quiz_home, name='mental_quiz_home'),
    path('mental-quiz/<str:grade>/', views.mental_quiz, name='mental_quiz'),
    path('api/explain-word/<str:word>/', views.api_explain_word, name='api_explain_word'),
    path('api/math-hint/', views.api_math_hint, name='api_math_hint'),
    path('api/word-explanation/<str:word>/', views.api_word_explanation, name='api_word_explanation'),
    path('saved-vocabulary/', views.saved_vocabulary, name='saved_vocabulary'),
    path('api/save-word/', views.api_save_word, name='api_save_word'),
    path('api/check-saved-word/<str:word>/', views.api_check_saved_word, name='api_check_saved_word'),
    path('api/get-saved-words/', views.api_get_saved_words, name='api_get_saved_words'),
    # Brain Quest — Daily Mission
    path('me/', views.profile_me, name='profile_me'),
    path('mission/', views.mission_home, name='mission_home'),
    path('mission/play/', views.daily_mission, name='daily_mission'),
    path('api/mission/complete/', views.api_mission_complete, name='api_mission_complete'),
    path('api/mascot/react/', views.api_mascot_react, name='api_mascot_react'),
    path('api/mascot/save/', views.api_save_mascot, name='api_save_mascot'),
    # Flashcards
    path('flashcards/', views.flashcard_review, name='flashcard_review'),
    path('api/flashcard/save/', views.api_save_flashcard, name='api_save_flashcard'),
    path('api/flashcard/check/<str:card_type>/<str:front_text>/', views.api_check_flashcard, name='api_check_flashcard'),
    path('api/flashcard/delete/', views.api_delete_flashcard, name='api_delete_flashcard'),
    # Word Explorer Academy
    path('word-explorer/', views.word_explorer_home, name='word_explorer_home'),
    path('word-explorer/<str:tier>/', views.word_explorer_lesson, name='word_explorer_lesson'),
    path('idiom-island/', views.idiom_island, name='idiom_island'),
    path('api/we/complete/', views.api_we_complete_session, name='api_we_complete'),
    path('api/we/idiom-complete/', views.api_we_complete_idiom, name='api_we_idiom_complete'),
    path('api/we/explain/<str:word>/<str:tier>/', views.api_we_word_explanation, name='api_we_explain'),
    # Daily Discovery
    path('daily-discovery/', views.daily_discovery_home, name='daily_discovery_home'),
    path('daily-discovery/<str:category>/', views.daily_discovery_item, name='daily_discovery_item'),
    path('api/dd/complete/', views.api_dd_complete, name='api_dd_complete'),
    path('api/dd/ai-explain/', views.api_dd_ai_explain, name='api_dd_ai_explain'),
    # Math Challenge
    path('math-challenge/', views.math_challenge_home, name='math_challenge_home'),
    path('math-challenge/quiz/', views.math_challenge_quiz, name='math_challenge_quiz'),
    path('math-challenge/quiz/<int:grade>/', views.math_challenge_quiz, name='math_challenge_quiz_grade'),
    path('api/mc/submit/', views.api_mc_submit, name='api_mc_submit'),
    path('api/mc/hint/', views.api_mc_hint, name='api_mc_hint'),
    path('api/mc/explain/', views.api_mc_explain, name='api_mc_explain'),
    # Profile
    path('profile/', views.profile_settings, name='profile_settings'),
    path('api/profile/stats/', views.api_profile_stats, name='api_profile_stats'),
]
