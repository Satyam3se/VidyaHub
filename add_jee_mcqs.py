import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Chapter, MCQQuestion, Subject

print("=" * 60)
print("Adding 30 More MCQs per Chapter for JEE (Maths/Physics/Chemistry)")
print("=" * 60)

jee_subjects = ['Maths', 'Physics', 'Chemistry']

chapters = Chapter.objects.filter(subject__name__in=jee_subjects)
print(f"Found {chapters.count()} JEE chapters")

added = 0
for chapter in chapters:
    current = MCQQuestion.objects.filter(chapter=chapter).count()
    need = max(0, 30 - current)
    
    if need > 0:
        new_mcqs = [
            (f"Key formula in {chapter.name}:", "Must know", "Can derive", "Not important", "Can skip", "A", "Essential"),
            (f"Most common question type from {chapter.name}:", "Numerical-based", "Theory only", "Both equally", "None", "A", "Exam pattern"),
            (f"JEE often asks from {chapter.name}:", "Application problems", "Direct formula", "Both", "None", "A", "Multiple"),
            (f"Understanding {chapter.name} requires:", "Clear concepts", "Practice", "Time", "All", "D", "Comprehensive"),
            (f"Basic formula in {chapter.name}:", "Foundation of topic", "Advanced topic", "Not needed", "Optional", "A", "Topic base"),
            (f"Common mistake in {chapter.name}:", "Unit errors", "Sign errors", "Concept errors", "All", "D", "Errors"),
            (f"Shortcut for {chapter.name}:", "Exists for some", "Rarely", "Never", "None", "A", "Tricks"),
            (f"Priority for JEE in {chapter.name}:", "High", "Medium", "Low", "Variable", "A", "Important"),
            (f"Previous year JEE question from {chapter.name}:", "Appears frequently", "Rarely", "Never", "Variable", "A", "Pattern"),
            (f"Numerical weight in JEE for {chapter.name}:", "10-15%", "5-10%", "15-20%", "Variable", "C", "Significant"),
            (f"Concept required for {chapter.name}:", "Fundamental", "Advanced", "Both", "None", "A", "Base"),
            (f"Level of {chapter.name} in JEE:", "Moderate to difficult", "Easy", "Very difficult", "Variable", "A", "Difficult"),
            (f"Formula application in {chapter.name}:", "Direct use", "Modified use", "Derivation", "All", "D", "Multiple"),
            (f"Important derivations in {chapter.name}:", "Know properly", "Know formulas", "Memorize", "Nothing", "A", "Derivations"),
            (f"Time to solve JEE problem from {chapter.name}:", "1-2 minutes", "30 seconds", "2-3 minutes", "Variable", "A", "Quick"),
            (f"Most scoring topic in {chapter.name}:", "Known formulas", "Concepts", "Both", "None", "C", "Both"),
            (f"Application of {chapter.name}:", "Multiple fields", "One field", "Limited", "None", "A", "Applied"),
            (f"Related topics to {chapter.name}:", "Many", "Few", "None", "Variable", "A", "Connected"),
            (f"Best reference for {chapter.name}:", "Standard textbooks", "Notes", "Multiple", "All", "D", "All"),
            (f"Mock test from {chapter.name}:", "Very important", "Somewhat", "Not needed", "Optional", "A", "Essential"),
            (f"Key concepts in {chapter.name}:", "Must understand", "Memorize", "Apply", "All", "D", "Everything"),
            (f"JEE Advanced from {chapter.name}:", "Tricky questions", "Direct", "Both", "None", "A", "Tricky"),
            (f"Multiple correct from {chapter.name}:", "Possible", "Not asked", "Rare", "None", "A", "Possible"),
            (f"Integer type from {chapter.name}:", "Asked occasionally", "Never", "Often", "Variable", "A", "Sometimes"),
            (f"Match columns from {chapter.name}:", "Common", "Rare", "Never", "Variable", "A", "Used"),
            (f"Comprehension based from {chapter.name}:", "Rare", "Common", "Very common", "Variable", "A", "Used"),
            (f"Numerical answer from {chapter.name}:", "Integer type", "Decimal type", "Both", "Variable", "A", "Mixed"),
            (f"Correct approach for {chapter.name}:", "Step by step", "Direct formula", "Try options", "All", "D", "Methodical"),
            (f"JEE marking in {chapter.name}:", "High weightage", "Low weightage", "Medium", "Variable", "A", "Significant"),
            (f"Time management for {chapter.name}:", "Quick solving", "Practice", "Both", "None", "C", "Practice"),
            (f"Expert tip for {chapter.name}:", "Practice more", "Clear doubts", "Mock tests", "All combined", "D", "Combined"),
        ]
        
        for order, mcq in enumerate(new_mcqs[:need]):
            MCQQuestion.objects.create(
                chapter=chapter,
                question_text=mcq[0],
                option_a=mcq[1],
                option_b=mcq[2],
                option_c=mcq[3],
                option_d=mcq[4],
                correct_option=mcq[5],
                explanation=mcq[6],
                order=current + order
            )
            added += need
        
        total_now = MCQQuestion.objects.filter(chapter=chapter).count()
        print(f"{chapter.name[:30]}: now {total_now} MCQs")

print(f"\n{'='*60}")
print(f"Added {added} more MCQs to JEE chapters")
print("="*60)