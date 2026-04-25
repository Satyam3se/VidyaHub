from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/student/', views.student_signup, name='student_signup'),
    path('signup/teacher/', views.teacher_signup, name='teacher_signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    
    # Course System
    path('courses/', views.course_index, name='course_index'),
    path('courses/<slug:grade_slug>/', views.grade_detail, name='grade_detail'),
    path('courses/<slug:grade_slug>/<slug:subject_slug>/', views.subject_detail, name='subject_detail'),
    path('courses/<slug:grade_slug>/<slug:subject_slug>/<slug:chapter_slug>/', views.chapter_detail, name='chapter_detail'),
    
    # AI Logic
    path('api/ai/stuck/', views.ai_stuck_explanation, name='ai_stuck'),
    path('api/ai/ask/', views.ask_vidya_ai, name='ask_vidya_ai'),
    path('generate-ai-notes/<int:chapter_id>/', views.generate_ai_notes, name='generate_ai_notes'),
    path('games/duel/<int:chapter_id>/', views.concept_duel, name='concept_duel'),
    path('games/memory-match/', views.memory_match, name='memory_match'),
    path('games/word-scramble/', views.word_scramble, name='word_scramble'),
    path('games/space-defender/', views.space_defender, name='space_defender'),
    path('games/gravity-drop/', views.gravity_drop, name='gravity_drop'),
    path('games/quiz-dash/', views.quiz_dash, name='quiz_dash'),
    path('games/knowledge-ninja/', views.knowledge_ninja, name='knowledge_ninja'),
    path('games/astro-jump/', views.astro_jump, name='astro_jump'),
    path('games/scholar-snake/', views.scholar_snake, name='scholar_snake'),
    path('games/hover-dash/', views.hover_dash, name='hover_dash'),
    path('games/brain-breaker/', views.brain_breaker, name='brain_breaker'),
    path('games/whack-a-fact/', views.whack_a_fact, name='whack_a_fact'),
    path('games/knowledge-toss/', views.knowledge_toss, name='knowledge_toss'),
    path('games/math-duel/', views.math_duel, name='math_duel'),
    path('games/spelling-bee/', views.spelling_bee, name='spelling_bee'),
    path('games/science-lab/', views.science_lab, name='science_lab'),
    path('games/geography-explorer/', views.geography_explorer, name='geography_explorer'),
    path('games/code-cracker/', views.code_cracker, name='code_cracker'),
    
    # JEE Games
    path('games/jee-math/', views.jee_math, name='jee_math'),
    path('games/jee-physics/', views.jee_physics, name='jee_physics'),
    path('games/jee-chemistry/', views.jee_chemistry, name='jee_chemistry'),
    
    # NEET Games
    path('games/neet-biology/', views.neet_biology, name='neet_biology'),
    path('games/neet-chemistry/', views.neet_chemistry, name='neet_chemistry'),
    path('games/neet-physics/', views.neet_physics, name='neet_physics'),
    
    # NDA Games
    path('games/nda-math/', views.nda_math, name='nda_math'),
    path('games/nda-physics/', views.nda_physics, name='nda_physics'),
    path('games/nda-ga/', views.nda_ga, name='nda_ga'),
    
    path('api/game/results/', views.game_results_submit, name='game_results_submit'),
    path('api/battle/results/', views.battle_results_submit, name='battle_results_submit'),

    # Real-time Battles
    path('battle/<int:subject_id>/', views.live_battle, name='live_battle'),

    # Gamification
    path('game/', views.game_dashboard, name='game_dashboard'),
    path('game/quiz/<int:subject_id>/', views.daily_quiz_init, name='daily_quiz'),
    path('game/quiz/submit/', views.daily_quiz_submit, name='daily_quiz_submit'),
    path('game/boss/<int:subject_id>/', views.boss_battle_init, name='boss_battle_init'),
    path('game/boss/submit/', views.boss_battle_submit, name='boss_battle_submit'),

    # Chapter Quizzes
    path('game/chapter-quiz/<int:chapter_id>/', views.chapter_quiz_init, name='chapter_quiz'),
    path('game/chapter-quiz/submit/', views.chapter_quiz_submit, name='chapter_quiz_submit'),
    
    # Leaderboard
    path('leaderboard/', views.leaderboard_view, name='leaderboard'),
    path('profile/', views.profile_view, name='profile'),
    path('api/profile/avatar/', views.update_avatar, name='update_avatar'),
    
    # Teacher PDF Features
    path('teacher/upload-note/', views.upload_teacher_note, name='upload_teacher_note'),
    path('teacher/note-analysis/<int:upload_id>/', views.view_note_analysis, name='view_note_analysis'),
    
    # Student AI Mastery
    path('dashboard/mastery/', views.mastery_dashboard, name='mastery_dashboard'),
]
