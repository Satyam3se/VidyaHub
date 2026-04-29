"""
Patch views.py to:
1. Update chapter_detail to pass chapter_quiz_count
2. Append chapter_quiz_init and chapter_quiz_submit views
"""

with open('c:/VidyaHub/main/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Normalize line endings for matching
content = content.replace('\r\n', '\n')

# ===== PATCH 1: Update chapter_detail return to pass quiz count =====
old_return = """    return render(request, 'main/video_player.html', {
        'grade': grade,
        'subject': subject,
        'chapter': chapter,
        'videos': videos,
        'current_video': current_video,
        'all_chapters': all_chapters,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
        'note': note
    })"""

new_return = """    # Check if chapter has quiz questions
    chapter_quiz_count = chapter.mcqs.count()

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
    })"""

if old_return in content:
    content = content.replace(old_return, new_return)
    print("PATCH 1 applied: chapter_detail updated.")
else:
    print("ERROR: Could not find chapter_detail return block.")

# ===== PATCH 2: Append new chapter quiz views =====
new_views = '''

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
    # Take up to 10 questions per chapter quiz
    questions = questions[:10]
    
    return render(request, 'main/chapter_quiz.html', {
        'chapter': chapter,
        'questions': questions,
        'total': len(questions),
    })


@login_required
def chapter_quiz_submit(request):
    """Handle chapter quiz submission and award XP."""
    if request.method == 'POST':
        import json as json_mod
        data = json_mod.loads(request.body)
        chapter_id = data.get('chapter_id')
        score = data.get('score', 0)
        total = data.get('total', 10)
        
        # XP: 15 XP per correct answer for chapter quizzes (more than daily)
        xp_earned = score * 15
        # Perfect score bonus
        if score == total:
            xp_earned += 30

        profile = request.user.profile
        profile.xp += xp_earned
        new_level = (profile.xp // 500) + 1
        level_up = new_level > profile.level
        profile.level = new_level
        profile.save()

        return JsonResponse({
            'success': True,
            'xp_earned': xp_earned,
            'level_up': level_up,
            'new_level': profile.level,
            'total_xp': profile.xp,
            'score': score,
            'total': total,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
'''

content += new_views
print("PATCH 2 applied: New chapter quiz views appended.")

with open('c:/VidyaHub/main/views.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("views.py saved successfully.")
