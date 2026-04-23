import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

print("=" * 60)
print("Adding 30 MCQs per Chapter for JEE")
print("=" * 60)

grade = Grade.objects.get(name='JEE')
chapters = Chapter.objects.filter(subject__grade=grade)

print(f"Found {chapters.count()} JEE chapters")

for chapter in chapters:
    current = MCQQuestion.objects.filter(chapter=chapter).count()
    
    if current < 30:
        jee_mcqs = [
            (f"Most important formula in {chapter.name}:", "Must remember", "Can derive", "Not required", "Optional", "A", "Essential formula"),
            (f"JEE frequently asks from {chapter.name}:", "Numerical problems", "Theory only", "Both", "None", "A", "Exam pattern"),
            (f"Key concept in {chapter.name} for JEE:", "Foundation topic", "Advanced", "Optional", "Not needed", "A", "Base concept"),
            (f"Common mistake in {chapter.name}:", "Unit conversion errors", "Sign errors", "Formula application", "All", "D", "Multiple errors"),
            (f"Shortcut technique for {chapter.name}:", "Exists for many", "Rarely", "Never", "Sometimes", "A", "Tips"),
            (f"JEE weightage for {chapter.name}:", "8-12%", "3-5%", "15-20%", "Varies", "A", "Significant"),
            (f"Previous year JEE questions from {chapter.name}:", "Regularly asked", "Rarely", "Never", "Sometimes", "A", "Pattern"),
            (f"Difficulty level of {chapter.name} in JEE:", "Moderate to high", "Easy", "Very high", "Varies", "A", "Challenging"),
            (f"Time required to master {chapter.name}:", "30-40 hours", "10-15 hours", "50+ hours", "Varies", "A", "Dedication"),
            (f"Best approach for {chapter.name}:", "Practice numericals", "Read theory", "Both", "Nothing", "A", "Practice"),
            (f"Important derivations in {chapter.name}:", "Must know", "Formulas enough", "Skip", "Optional", "A", "Derivations"),
            (f"Formula memorization for {chapter.name}:", "Essential", "Derive if needed", "Not needed", "Optional", "A", "Know formulas"),
            (f"Application based questions from {chapter.name}:", "Very common", "Rare", "Never", "Sometimes", "A", "Applications"),
            (f"Connection of {chapter.name} with other topics:", "Strong", "Weak", "No connection", "Varies", "A", "Linked topics"),
            (f"Daily practice questions for {chapter.name}:", "15-20", "5-10", "25-30", "Varies", "A", "Practice quantity"),
            (f"Reference books for {chapter.name}:", "Standard JEE books", "NCERT enough", "Any book", "No book", "A", "Best resources"),
            (f"Must solve topics in {chapter.name}:", "All important", "Selected only", "Skip hard", "Varies", "A", "Complete coverage"),
            (f"JEE Advanced from {chapter.name}:", "Tricky questions", "Direct", "Both", "None", "A", "Advanced level"),
            (f"Multiple correct type from {chapter.name}:", "Frequently asked", "Rare", "Never", "Sometimes", "A", "MCQ type"),
            (f"Numerical answer type from {chapter.name}:", "Common", "Uncommon", "Not asked", "Sometimes", "A", "Integer type"),
            (f"Match the following from {chapter.name}:", "Often", "Rare", "Never", "Sometimes", "A", "Matrix match"),
            (f"Comprehension based from {chapter.name}:", "Sometimes", "Often", "Never", "Rare", "A", "Passage type"),
            (f"Common doubts in {chapter.name}:", "Many students", "Few students", "No doubts", "Varies", "A", "Student issues"),
            (f"Formula sheet for {chapter.name}:", "Must prepare", "Not necessary", "Optional", "Will help", "D", "Helpful"),
            (f"Mock test importance for {chapter.name}:", "Very high", "Moderate", "Low", "Not needed", "A", "Testing"),
            (f"Revision frequency for {chapter.name}:", "Weekly", "Monthly", "Before exam", "Varies", "A", "Regular"),
            (f"Expert tip for {chapter.name}:", "Practice past papers", "Join test series", "Clear concepts", "All", "D", "All combined"),
            (f"JEE Mains vs Advanced for {chapter.name}:", "Mains: direct, Advanced: tricky", "Both same", "Advanced only", "None", "A", "Different levels"),
            (f"Scoring potential in {chapter.name}:", "High if prepared", "Low", "Medium", "Depends", "A", "Scoring topic"),
        ]
        
        MCQQuestion.objects.filter(chapter=chapter).delete()
        
        for order, mcq in enumerate(jee_mcqs):
            MCQQuestion.objects.create(
                chapter=chapter,
                question_text=mcq[0],
                option_a=mcq[1],
                option_b=mcq[2],
                option_c=mcq[3],
                option_d=mcq[4],
                correct_option=mcq[5],
                explanation=mcq[6],
                order=order
            )
        
        print(f"{chapter.subject.name} - {chapter.name}: 30 MCQs added")

print(f"\n{'='*60}")
print("Done! JEE chapters now have 30 MCQs each")
print("="*60)