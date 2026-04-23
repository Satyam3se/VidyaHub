from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import StudentSignUpForm, TeacherSignUpForm, UserLoginForm
from .models import Profile, Grade, Subject, Chapter, Video, ChapterNote, MCQQuestion, UserProgress, SubjectScore
from django.conf import settings
from django.http import JsonResponse
import google.generativeai as genai
import json
import re
from groq import Groq

genai.configure(api_key=settings.GEMINI_API_KEY)

def index(request):
    return render(request, 'main/index.html')

@login_required
def dashboard(request):
    if request.user.profile.role == 'teacher':
        return redirect('teacher_dashboard')
    return redirect('student_dashboard')

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('student_dashboard')
    else:
        form = StudentSignUpForm()
    return render(request, 'main/signup_student.html', {'form': form})

def teacher_signup(request):
    if request.method == 'POST':
        form = TeacherSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('teacher_dashboard')
    else:
        form = TeacherSignUpForm()
    return render(request, 'main/signup_teacher.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Redirect based on role
            if hasattr(user, 'profile'):
                if user.profile.role == 'teacher':
                    return redirect('teacher_dashboard')
                else:
                    return redirect('student_dashboard')
            return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'main/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def student_dashboard(request):
    if request.user.profile.role != 'student':
        return redirect('teacher_dashboard')
    
    from .utils import get_global_leaderboard, get_user_badges, get_achievement_progress, get_daily_reward
    leaderboard = get_global_leaderboard()
    profile = request.user.profile
    
    # Get gamification data
    badges = get_user_badges(request.user)[:6]  # Recent badges
    achievement_progress = get_achievement_progress(profile)[:5]
    daily_reward = get_daily_reward(profile.streak)
    
    return render(request, 'main/student_dashboard.html', {
        'leaderboard': leaderboard,
        'user_badges': badges,
        'achievement_progress': achievement_progress,
        'daily_reward': daily_reward,
    })

@login_required
def teacher_dashboard(request):
    if request.user.profile.role != 'teacher':
        return redirect('student_dashboard')
    return render(request, 'main/teacher_dashboard.html')

# Course System Views
def course_index(request):
    grades = Grade.objects.all()
    return render(request, 'main/classes.html', {'grades': grades})

def grade_detail(request, grade_slug):
    grade = get_object_or_404(Grade, slug=grade_slug)
    subjects = grade.subjects.all()
    return render(request, 'main/subjects.html', {
        'grade': grade,
        'subjects': subjects
    })

def subject_detail(request, grade_slug, subject_slug):
    grade = get_object_or_404(Grade, slug=grade_slug)
    subject = get_object_or_404(Subject, grade=grade, slug=subject_slug)
    chapters = subject.chapters.all()
    return render(request, 'main/chapters.html', {
        'grade': grade,
        'subject': subject,
        'chapters': chapters
    })

def chapter_detail(request, grade_slug, subject_slug, chapter_slug):
    grade = get_object_or_404(Grade, slug=grade_slug)
    subject = get_object_or_404(Subject, grade=grade, slug=subject_slug)
    chapter = get_object_or_404(Chapter, subject=subject, slug=chapter_slug)
    
    # Get the videos for this chapter
    videos = chapter.videos.all()
    
    # Support specific video selection via query param ?v=ID
    video_id = request.GET.get('v')
    if video_id:
        current_video = get_object_or_404(Video, id=video_id, chapter=chapter)
    else:
        current_video = videos.first()
    
    # Get all chapters for sidebar
    all_chapters = subject.chapters.all()
    
    # Calculate Next and Previous chapters
    prev_chapter = subject.chapters.filter(order__lt=chapter.order).order_by('-order').first()
    next_chapter = subject.chapters.filter(order__gt=chapter.order).order_by('order').first()
    
    try:
        note = chapter.notes
    except Exception:
        note = None

    # Check if chapter has quiz questions
    import json
    chapter_quiz_count = chapter.mcqs.count()
    mcq_queryset = chapter.mcqs.all()
    mcq_questions = [
        {
            'id': q.id,
            'question_text': q.question_text,
            'option_a': q.option_a,
            'option_b': q.option_b,
            'option_c': q.option_c,
            'option_d': q.option_d,
            'correct_option': q.correct_option,
            'explanation': q.explanation,
            'order': q.order
        }
        for q in mcq_queryset
    ]

    return render(request, 'main/video_player.html', {
        'grade': grade,
        'subject': subject,
        'chapter': chapter,
        'videos': videos,
        'current_video': current_video,
        'all_chapters': all_chapters,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
        'note': note,
        'chapter_quiz_count': chapter_quiz_count,
        'mcq_questions': json.dumps(mcq_questions),
    })

@login_required
def ai_stuck_explanation(request):
    chapter_id = request.GET.get('chapter_id')
    chapter = get_object_or_404(Chapter, id=chapter_id)
    
    prompt = f"""
    Explain the core concepts of the chapter: '{chapter.name}' from the subject '{chapter.subject.name}'.
    
    Requirements:
    1. Language: Simple, plain language understandable by a {chapter.subject.grade.name} student.
    2. Format: Return a JSON object with:
       - 'explanation': A markdown-formatted explanation (300-500 words).
       - 'quiz': An array of 3 objects, each with 'question', 'options' (array of 4), and 'correct_index' (0-3).
    3. Tone: Encouraging and clear.
    
    Return ONLY valid JSON.
    """
    
    try:
        # Check Simulation Mode
        if getattr(settings, 'AI_SIMULATION_MODE', False):
            raise Exception("Simulation Mode Active")

        # Try OpenAI First
        if settings.OPENAI_API_KEY:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=settings.OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    response_format={ "type": "json_object" }
                )
                data = json.loads(response.choices[0].message.content)
                return JsonResponse(data)
            except Exception as openai_err:
                print(f"OpenAI Failed, falling back to Gemini: {openai_err}")
        
        # Fallback to Gemini Logic
        model_names = [
            'gemini-1.5-flash', 
            'gemini-1.5-flash-latest', 
            'models/gemini-1.5-flash', 
            'gemini-1.5-pro', 
            'gemini-pro'
        ]
        
        for m_name in model_names:
            try:
                model = genai.GenerativeModel(m_name)
                res = model.generate_content(prompt)
                if not res.candidates or not res.candidates[0].content.parts:
                    continue
                text = res.text
                if '```json' in text:
                    text = text.split('```json')[1].split('```')[0].strip()
                elif '```' in text:
                    text = text.split('```')[1].split('```')[0].strip()
                return JsonResponse(json.loads(text))
            except Exception:
                continue
        
        # If we reach here, both AI providers failed
        raise Exception("API Providers unavailable")

    except Exception as e:
        # ZERO-FAILURE LOCAL FALLBACK
        print(f"AI Failed ({e}), using local data simulation.")
        
        # Get Note Content
        note = ChapterNote.objects.filter(chapter=chapter).first()
        explanation = note.content if note else "This concept covers the fundamental principles of study. Please refer to your textbooks for detailed analysis."
        
        # Get 3 random questions
        questions_query = MCQQuestion.objects.filter(chapter=chapter).order_by('?')[:3]
        quiz = []
        for q in questions_query:
            quiz.append({
                'question': q.question_text,
                'options': [q.option_a, q.option_b, q.option_c, q.option_d],
                'correct_index': ord(q.correct_option) - ord('A')
            })
            
        return JsonResponse({
            'explanation': explanation,
            'quiz': quiz if quiz else [{
                'question': 'How ready are you for the hackathon?',
                'options': ['Not ready', 'Getting there', 'Ready', 'Mastered'],
                'correct_index': 2
            }],
            'simulated': True
        })

def ask_vidya_ai(request):
    """Handle general questions from the floating AI Chatbot using Groq."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_question = data.get('question')
            
            if not user_question:
                return JsonResponse({'error': 'No question provided'}, status=400)

            client = Groq(api_key=settings.GROQ_API_KEY)
            
            # System prompt to define the AI's personality
            system_prompt = """
            You are 'Vidya AI', the friendly and expert educational assistant for VidyaHub.
            Your goal is to help students understand complex topics, solve doubts, and stay motivated.
            
            Guidelines:
            1. Be encouraging, patient, and clear.
            2. Use simple language but remain scientifically accurate.
            3. If a student asks about a specific subject, try to relate it to their learning journey.
            4. Keep responses concise (under 200 words) unless requested otherwise.
            5. Use Markdown for formatting (bold, lists, etc.).
            """
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_question}
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=False,
            )
            
            answer = completion.choices[0].message.content
            return JsonResponse({'answer': answer})
            
        except Exception as e:
            print(f"Groq AI Error: {e}")
            return JsonResponse({'error': 'Vidya AI is taking a short break. Please try again in a moment.'}, status=500)
            
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def live_battle(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    return render(request, 'main/live_battle.html', {
        'subject': subject,
        'user': request.user
    })

@login_required
def game_dashboard(request):
    if request.user.profile.role != 'student':
        return redirect('teacher_dashboard')
    
    profile = request.user.profile
    
    # Calculate Course Progress
    # Try to get the last active subject from scores
    subject_score = profile.user.subject_scores.order_by('-last_updated').first()
    if subject_score:
        subject = subject_score.subject
    else:
        # Fallback to the first subject of their grade
        subject = Subject.objects.filter(grade__name=profile.grade).first()

    progress = 0
    clan_name = "Basics Clan"
    clan_slug = "basics"
    milestone_next = 25
    
    if subject:
        total_chapters = subject.chapters.count()
        if total_chapters > 0:
            completed = UserProgress.objects.filter(
                user=request.user, 
                chapter_note__chapter__subject=subject
            ).count()
            progress = (completed / total_chapters) * 100
        
        from .game_utils import get_clan_info
        clan_name, clan_slug, milestone_next = get_clan_info(progress)

    # XP Progress for the level bar
    xp_in_level = profile.xp % 500
    xp_percent = (xp_in_level / 500) * 100
    xp_for_next_level = 500 - xp_in_level

    # Global Rank
    students_above = Profile.objects.filter(role='student', xp__gt=profile.xp).count()
    global_rank = students_above + 1
    total_students = Profile.objects.filter(role='student').count()

    # Subjects for this student's grade (quiz buttons)
    grade_subjects = Subject.objects.filter(grade__name=profile.grade)

    return render(request, 'main/game_dashboard.html', {
        'profile': profile,
        'progress': progress,
        'subject': subject,
        'clan_name': clan_name,
        'clan_slug': clan_slug,
        'milestone_next': milestone_next,
        'xp_percent': xp_percent,
        'xp_in_level': xp_in_level,
        'xp_for_next_level': xp_for_next_level,
        'next_level_xp': profile.level * 500,
        'global_rank': global_rank,
        'total_students': total_students,
        'grade_subjects': grade_subjects,
    })

@login_required
def daily_quiz_init(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    
    from .game_utils import generate_30_questions
    questions = generate_30_questions(subject, request.user.profile.grade)
    
    if not questions:
        return redirect('game_dashboard')
        
    return render(request, 'main/daily_quiz.html', {
        'subject': subject,
        'questions': questions,
    })

@login_required
def daily_quiz_submit(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        subject_id = data.get('subject_id')
        score = data.get('score')
        time_taken = data.get('time_taken')
        
        from .game_utils import calculate_xp_award
        xp_earned = calculate_xp_award(score, time_taken)
        
        profile = request.user.profile
        profile.xp += xp_earned
        
        new_level = (profile.xp // 500) + 1
        level_up = (new_level > profile.level)
        profile.level = new_level
        
        from datetime import date, timedelta
        today = date.today()
        if profile.last_quiz_date == today - timedelta(days=1):
            profile.streak += 1
        elif profile.last_quiz_date != today:
            profile.streak = 1
        
        profile.last_quiz_date = today
        profile.save()
        
        return JsonResponse({
            'success': True,
            'xp_earned': xp_earned,
            'level_up': level_up,
            'streak': profile.streak,
            'new_level': profile.level,
            'total_xp': profile.xp,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def boss_battle_init(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    # Fetch 15 random questions from the ENTIRE subject for the boss battle
    questions = MCQQuestion.objects.filter(chapter__subject=subject).order_by('?')[:15]
    
    if not questions:
        # Fallback if no questions in DB
        from .game_utils import generate_30_questions
        questions = generate_30_questions(subject, request.user.profile.grade)[:10]

    return render(request, 'main/boss_battle.html', {
        'subject': subject,
        'questions': questions,
    })

@login_required
def boss_battle_submit(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        subject_id = data.get('subject_id')
        score = data.get('score')
        
        # Boss Battle gives DOUBLE XP!
        xp_earned = score * 50 # 50 XP per correct answer in Boss Battle
        
        profile = request.user.profile
        profile.xp += xp_earned
        
        new_level = (profile.xp // 500) + 1
        level_up = (new_level > profile.level)
        profile.level = new_level
        profile.save()
        
        return JsonResponse({
            'success': True, 
            'xp_earned': xp_earned, 
            'level_up': level_up,
            'victory_msg': f"The Boss of {Subject.objects.get(id=subject_id).name} has been defeated!"
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def chapter_quiz_init(request, chapter_id):
    """Show a quiz for a specific chapter."""
    chapter = get_object_or_404(Chapter, id=chapter_id)
    questions = list(chapter.mcqs.all())
    
    if not questions:
        # No DB questions for this chapter
        return render(request, 'main/chapter_quiz.html', {
            'chapter': chapter,
            'questions': [],
            'no_questions': True,
        })
    
    import random
    random.shuffle(questions)
    # Take up to 15 questions per chapter quiz
    questions = questions[:15]
    
    return render(request, 'main/chapter_quiz.html', {
        'chapter': chapter,
        'questions': questions,
        'total': len(questions),
    })


@login_required
def generate_ai_notes(request, chapter_id):
    """Generate high-quality HTML study notes for a chapter using Groq AI."""
    chapter = get_object_or_404(Chapter, id=chapter_id)
    
    # Check if notes already exist
    if ChapterNote.objects.filter(chapter=chapter).exists():
        return JsonResponse({'error': 'Notes already exist for this chapter.'}, status=400)

    try:
        from groq import Groq
        client = Groq(api_key=settings.GROQ_API_KEY)
        
        prompt = f"""
        You are 'Vidya AI', an expert educator. Write a high-quality, comprehensive, and engaging study note for the chapter '{chapter.name}' in the subject of '{chapter.subject.name}' (Grade: {chapter.subject.grade.name}).
        
        The output MUST be formatted as clean HTML. Do NOT wrap it in markdown blocks like ```html.
        
        Structure requirements:
        1. Use <div class="chapter-note-container"> as the root.
        2. Include an 'Overview' section with 2-3 paragraphs.
        3. Include a 'Key Concepts' section with a bulleted list. 
        4. CRITICAL: For each item in the 'Key Concepts' list, append a clarify icon at the end of the text like this: 
           `<span class="clarify-icon" onclick="window.openVidyaAI('Tell me more about [Concept Name] in the context of {chapter.name}')"><i data-lucide="help-circle"></i></span>`
        5. Include a 'Detailed Breakdown' section with subheadings (h4).
        6. Include a 'Study Tips' section.
        7. Use premium educational tone.
        """
        
        # Try 70B first
        try:
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a specialized educational content creator. Return ONLY clean HTML."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2048,
            )
        except Exception as e:
            print(f"70B Failed, falling back to 8B: {e}")
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": "You are a specialized educational content creator. Return ONLY clean HTML."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=2048,
            )
        
        html_content = completion.choices[0].message.content.strip()
        
        # Strip potential markdown backticks
        if html_content.startswith("```html"):
            html_content = html_content[7:]
        elif html_content.startswith("```"):
            html_content = html_content[3:]
        if html_content.endswith("```"):
            html_content = html_content[:-3]
            
        # Save to database
        note = ChapterNote.objects.create(
            chapter=chapter,
            content=html_content.strip()
        )
        
        return JsonResponse({
            'success': True,
            'content': note.content
        })
        
    except Exception as e:
        print(f"Notes Generation Error: {e}")
        return JsonResponse({'error': 'Failed to generate notes. Please try again later.'}, status=500)


@login_required
def concept_duel(request, chapter_id):
    """View for the Concept Duel game - Chapter-specific quiz battle against AI."""
    import json
    from django.db.models import Count
    
    chapter = get_object_or_404(Chapter, id=chapter_id)
    
    # Get questions from this specific chapter first
    questions_query = MCQQuestion.objects.filter(chapter=chapter).order_by('?')
    question_count = questions_query.count()
    
    # If chapter doesn't have enough questions, get from same subject
    if question_count < 10:
        # Get additional questions from same subject
        additional = MCQQuestion.objects.filter(
            chapter__subject=chapter.subject
        ).exclude(
            chapter=chapter
        ).order_by('?')[:(10 - question_count)]
        
        questions_query = list(questions_query) + list(additional)
    
    # Take first 10
    questions_query = questions_query[:10]
    
    questions = []
    for q in questions_query:
        questions.append({
            'id': q.id,
            'question': q.question_text,
            'options': [q.option_a, q.option_b, q.option_c, q.option_d],
            'correct': ord(q.correct_option) - ord('A')
        })
    
    # Handle case with no questions at all
    if not questions:
        questions = [{
            'id': 0,
            'question': 'No questions available for this chapter yet.',
            'options': ['Continue anyway', 'Go back', 'Try another chapter', 'Practice more'],
            'correct': 0
        }]
    
    context = {
        'chapter': chapter,
        'questions_json': json.dumps(questions),
        'profile': request.user.profile,
        'question_source': 'chapter' if question_count >= 10 else 'subject'
    }
    return render(request, 'main/concept_duel.html', context)

@login_required
def memory_match(request):
    """View for the Memory Match game."""
    return render(request, 'main/memory_match.html', {
        'profile': request.user.profile
    })

@login_required
def word_scramble(request):
    """View for the Word Scramble game."""
    return render(request, 'main/word_scramble.html', {
        'profile': request.user.profile
    })

@login_required
def space_defender(request):
    """View for the Space Defender game."""
    return render(request, 'main/space_defender.html', {
        'profile': request.user.profile
    })

@login_required
def math_duel(request):
    """View for the Math Duel game."""
    profile = request.user.profile
    grade = profile.grade
    return render(request, 'main/math_duel.html', {
        'profile': profile,
        'grade': grade,
    })

@login_required
def spelling_bee(request):
    """View for the Spelling Bee game."""
    profile = request.user.profile
    grade = profile.grade
    return render(request, 'main/spelling_bee.html', {
        'profile': profile,
        'grade': grade,
    })

@login_required
def science_lab(request):
    """View for the Science Lab game."""
    profile = request.user.profile
    grade = profile.grade
    return render(request, 'main/science_lab.html', {
        'profile': profile,
        'grade': grade,
    })

@login_required
def geography_explorer(request):
    """View for the Geography Explorer game."""
    profile = request.user.profile
    grade = profile.grade
    return render(request, 'main/geography_explorer.html', {
        'profile': profile,
        'grade': grade,
    })

@login_required
def code_cracker(request):
    """View for the Code Cracker game."""
    profile = request.user.profile
    grade = profile.grade
    return render(request, 'main/code_cracker.html', {
        'profile': profile,
        'grade': grade,
    })

@login_required
def geography_explorer(request):
    """View for the Geography Explorer game."""
    return render(request, 'main/geography_explorer.html', {
        'profile': request.user.profile
    })

@login_required
def code_cracker(request):
    """View for the Code Cracker game."""
    profile = request.user.profile
    grade = profile.grade
    target_exam = profile.target_exam
    return render(request, 'main/code_cracker.html', {
        'profile': profile,
        'grade': grade,
    })

# ===================== JEE GAMES =====================
@login_required
def jee_math(request):
    """View for JEE Math game."""
    if request.user.profile.target_exam != 'jee':
        return redirect('game_dashboard')
    return render(request, 'main/jee_math.html', {
        'profile': request.user.profile,
    })

@login_required
def jee_physics(request):
    """View for JEE Physics game."""
    if request.user.profile.target_exam != 'jee':
        return redirect('game_dashboard')
    return render(request, 'main/jee_physics.html', {
        'profile': request.user.profile,
    })

@login_required
def jee_chemistry(request):
    """View for JEE Chemistry game."""
    if request.user.profile.target_exam != 'jee':
        return redirect('game_dashboard')
    return render(request, 'main/jee_chemistry.html', {
        'profile': request.user.profile,
    })

# ===================== NEET GAMES =====================
@login_required
def neet_biology(request):
    """View for NEET Biology game."""
    if request.user.profile.target_exam != 'neet':
        return redirect('game_dashboard')
    return render(request, 'main/neet_biology.html', {
        'profile': request.user.profile,
    })

@login_required
def neet_chemistry(request):
    """View for NEET Chemistry game."""
    if request.user.profile.target_exam != 'neet':
        return redirect('game_dashboard')
    return render(request, 'main/neet_chemistry.html', {
        'profile': request.user.profile,
    })

@login_required
def neet_physics(request):
    """View for NEET Physics game."""
    if request.user.profile.target_exam != 'neet':
        return redirect('game_dashboard')
    return render(request, 'main/neet_physics.html', {
        'profile': request.user.profile,
    })

# ===================== NDA GAMES =====================
@login_required
def nda_math(request):
    """View for NDA Math game."""
    if request.user.profile.target_exam != 'nda':
        return redirect('game_dashboard')
    return render(request, 'main/nda_math.html', {
        'profile': request.user.profile,
    })

@login_required
def nda_physics(request):
    """View for NDA Physics game."""
    if request.user.profile.target_exam != 'nda':
        return redirect('game_dashboard')
    return render(request, 'main/nda_physics.html', {
        'profile': request.user.profile,
    })

@login_required
def nda_ga(request):
    """View for NDA General Ability game."""
    if request.user.profile.target_exam != 'nda':
        return redirect('game_dashboard')
    return render(request, 'main/nda_ga.html', {
        'profile': request.user.profile,
    })

@login_required
def chapter_quiz_submit(request):
    """Handle chapter quiz submission and award XP."""
    if request.method == 'POST':
        import json as json_mod
        from .utils import add_xp, check_achievements
        data = json_mod.loads(request.body)
        chapter_id = data.get('chapter_id')
        score = data.get('score', 0)
        total = data.get('total', 10)
        
        profile = request.user.profile
        
        # Update quiz stats
        profile.total_quizzes += 1
        if score == total:
            profile.perfect_scores += 1
        profile.save()
        
        # XP: 15 XP per correct answer for chapter quizzes (more than daily)
        xp_earned = score * 15
        # Perfect score bonus
        if score == total:
            xp_earned += 30

        # Use gamification utility
        result = add_xp(request.user, xp_earned, activity_type='quiz')
        
        # Check for new badges
        new_badges = check_achievements(profile, 'quiz')

        return JsonResponse({
            'success': True,
            'xp_earned': xp_earned,
            'level_up': result.get('leveled_up', 0),
            'new_level': result['new_level'],
            'total_xp': result['new_xp'],
            'score': score,
            'total': total,
            'new_badges': [{'name': b.name, 'icon': b.icon} for b in new_badges],
            'streak': profile.streak,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def game_results_submit(request):
    """API endpoint to submit game results and award XP."""
    if request.method == 'POST':
        import json as json_mod
        from .utils import add_xp, check_achievements
        data = json_mod.loads(request.body)
        xp_earned = data.get('xp', 0)
        
        profile = request.user.profile
        
        # Update game stats
        profile.games_played += 1
        profile.save()

        # Use gamification utility
        result = add_xp(request.user, xp_earned, activity_type='game')
        
        # Check for new badges
        new_badges = check_achievements(profile, 'game')

        return JsonResponse({
            'success': True,
            'xp_earned': xp_earned,
            'level_up': result.get('leveled_up', 0),
            'new_level': result['new_level'],
            'new_badges': [{'name': b.name, 'icon': b.icon} for b in new_badges],
            'streak': profile.streak,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)

# ============ LEADERBOARD ============

@login_required
def leaderboard_view(request):
    leaderboard_type = request.GET.get('type', 'global')
    
    from django.db.models import Sum
    from django.contrib.auth.models import User
    
    if leaderboard_type == 'streak':
        # Streak leaderboard
        profiles = Profile.objects.filter(role='student').order_by('-streak', '-xp')[:50]
        leaderboard = [{'username': p.user.username, 'score': p.streak} for p in profiles]
    elif leaderboard_type == 'weekly':
        # Weekly - get users who earned XP this week
        from django.utils import timezone
        from datetime import timedelta
        week_ago = timezone.now() - timedelta(days=7)
        
        from .models import XPTransaction
        weekly_xp = XPTransaction.objects.filter(
            created_at__gte=week_ago
        ).values('user__username').annotate(
            total=Sum('amount')
        ).order_by('-total')[:50]
        
        leaderboard = [{'username': e['user__username'], 'score': e['total'] or 0} for e in weekly_xp]
    else:
        # Global - by total XP
        leaderboard = get_global_leaderboard(50)
    
    # Calculate user's rank
    user_rank = 1
    for i, entry in enumerate(leaderboard):
        if entry['username'] == request.user.username:
            user_rank = i + 1
            break
    else:
        # User not in top 50, count their rank
        if leaderboard_type == 'streak':
            higher_users = Profile.objects.filter(role='student', streak__gt=request.user.profile.streak).count()
            user_rank = higher_users + 1
        else:
            higher_users = Profile.objects.filter(role='student', xp__gt=request.user.profile.xp).count()
            user_rank = higher_users + 1
    
    return render(request, 'main/leaderboard.html', {
        'leaderboard': leaderboard,
        'leaderboard_type': leaderboard_type,
        'user_rank': user_rank,
    })

# ============ PROFILE ============

@login_required
def profile_view(request):
    from .utils import get_user_badges
    from .models import XPTransaction, Friend
    
    profile = request.user.profile
    badges = get_user_badges(request.user)
    xp_transactions = XPTransaction.objects.filter(user=request.user)[:20]
    
    # Get friends
    friends = Friend.objects.filter(from_user=request.user).select_related('to_user__profile')[:10]
    
    return render(request, 'main/profile.html', {
        'profile': profile,
        'user_badges': badges,
        'xp_transactions': xp_transactions,
        'friends': friends,
    })

@login_required
def update_avatar(request):
    if request.method == 'POST':
        import json as json_mod
        data = json_mod.loads(request.body)
        avatar = data.get('avatar', 'default')
        
        profile = request.user.profile
        profile.avatar = avatar
        profile.save()
        
        return JsonResponse({'success': True, 'avatar': avatar})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def battle_results_submit(request):
    """Handle battle results and award XP/badges."""
    if request.method == 'POST':
        import json as json_mod
        from .utils import add_xp, check_achievements
        data = json_mod.loads(request.body)
        
        score = data.get('score', 0)
        won = data.get('won', False)
        
        profile = request.user.profile
        profile.battles_played += 1
        
        if won:
            profile.battles_won += 1
            profile.battle_streak += 1
            if profile.battle_streak > profile.highest_battle_streak:
                profile.highest_battle_streak = profile.battle_streak
        else:
            profile.battle_streak = 0
        
        profile.save()
        
        # Award XP based on result
        if won:
            base_xp = 50 + (score * 2)  # Base 50 + 2 per point
            result = add_xp(request.user, base_xp, 'battle_win', f'Battle win - {score} points')
        else:
            base_xp = 10 + score  # Participation
            result = add_xp(request.user, base_xp, 'battle', f'Battle completed - {score} points')
        
        # Check achievements
        new_badges = check_achievements(profile, 'battle_win' if won else 'battle')
        
        return JsonResponse({
            'success': True,
            'xp_earned': result['xp_earned'],
            'won': won,
            'new_badges': [{'name': b.name, 'icon': b.icon} for b in new_badges],
            'battles_won': profile.battles_won,
            'battle_streak': profile.battle_streak,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
