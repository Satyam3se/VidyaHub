import re

with open('c:/VidyaHub/main/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_func = '''@login_required
def game_dashboard(request):
    if request.user.profile.role != 'student':
        return redirect('teacher_dashboard')
    
    profile = request.user.profile
    
    # Calculate Course Progress
    # Find active subject (based on last score or just pick one for demo)
    subject_score = profile.user.subject_scores.order_by('-last_updated').first()
    if subject_score:
        subject = subject_score.subject
    else:
        # Fallback to first subject in their grade
        from .models import Subject
        subject = Subject.objects.filter(grade__name=profile.grade).first()

    progress = 0
    clan_name = "Newbie"
    milestone_next = 25
    
    if subject:
        total_chapters = subject.chapters.count()
        if total_chapters > 0:
            completed = profile.user.progress.filter(chapter_note__chapter__subject=subject).count()
            progress = (completed / total_chapters) * 100
        
        from .game_utils import get_clan_info
        clan_name, clan_slug, milestone_next = get_clan_info(progress)

    # Calculate XP Progress for the bar
    xp_in_level = profile.xp % 500
    xp_percent = (xp_in_level / 500) * 100

    return render(request, 'main/game_dashboard.html', {
        'profile': profile,
        'progress': progress,
        'subject': subject,
        'clan_name': clan_name,
        'milestone_next': milestone_next,
        'xp_percent': xp_percent,
        'next_level_xp': (profile.level) * 500
    })'''

new_func = '''@login_required
def game_dashboard(request):
    if request.user.profile.role != 'student':
        return redirect('teacher_dashboard')
    
    profile = request.user.profile
    
    # Calculate Course Progress
    subject_score = profile.user.subject_scores.order_by('-last_updated').first()
    if subject_score:
        subject = subject_score.subject
    else:
        from .models import Subject
        subject = Subject.objects.filter(grade__name=profile.grade).first()

    progress = 0
    clan_name = "Newbie"
    milestone_next = 25
    
    if subject:
        total_chapters = subject.chapters.count()
        if total_chapters > 0:
            completed = profile.user.progress.filter(chapter_note__chapter__subject=subject).count()
            progress = (completed / total_chapters) * 100
        
        from .game_utils import get_clan_info
        clan_name, clan_slug, milestone_next = get_clan_info(progress)

    # XP Progress for the level bar
    xp_in_level = profile.xp % 500
    xp_percent = (xp_in_level / 500) * 100
    xp_for_next_level = 500 - xp_in_level

    # Global Rank: count students with MORE XP
    from .models import Profile as ProfileModel
    students_above = ProfileModel.objects.filter(role='student', xp__gt=profile.xp).count()
    global_rank = students_above + 1
    total_students = ProfileModel.objects.filter(role='student').count()

    # Subjects for this student's grade (quiz buttons)
    from .models import Subject as SubjectModel
    grade_subjects = SubjectModel.objects.filter(grade__name=profile.grade)

    return render(request, 'main/game_dashboard.html', {
        'profile': profile,
        'progress': progress,
        'subject': subject,
        'clan_name': clan_name,
        'milestone_next': milestone_next,
        'xp_percent': xp_percent,
        'xp_in_level': xp_in_level,
        'xp_for_next_level': xp_for_next_level,
        'next_level_xp': profile.level * 500,
        'global_rank': global_rank,
        'total_students': total_students,
        'grade_subjects': grade_subjects,
    })'''

if old_func in content:
    content = content.replace(old_func, new_func)
    with open('c:/VidyaHub/main/views.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: game_dashboard view updated!")
else:
    print("ERROR: Could not find old function. Trying normalized search...")
    # Normalize line endings and try again
    content_normalized = content.replace('\r\n', '\n')
    old_normalized = old_func.replace('\r\n', '\n')
    if old_normalized in content_normalized:
        content_normalized = content_normalized.replace(old_normalized, new_func)
        with open('c:/VidyaHub/main/views.py', 'w', encoding='utf-8') as f:
            f.write(content_normalized)
        print("SUCCESS: Updated after normalizing line endings!")
    else:
        print("FAILED: Function not found even after normalization.")
        # Print what we found around line 242
        lines = content.split('\n')
        for i, line in enumerate(lines[240:290], start=241):
            print(f"{i}: {repr(line)}")
