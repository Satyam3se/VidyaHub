import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

print("=" * 60)
print("Adding 30 MCQs per Chapter for NEET")
print("=" * 60)

grade = Grade.objects.get(name='NEET')
chapters = Chapter.objects.filter(subject__grade=grade)

print(f"Found {chapters.count()} NEET chapters")

for chapter in chapters:
    neet_mcqs = [
        (f"Most asked topic in NEET from {chapter.name}:", "Frequently appears", "Rarely asked", "Never asked", "Sometimes", "A", "Important topic"),
        (f"NEET weightage for {chapter.name}:", "8-12%", "3-5%", "15-20%", "Varies", "A", "High weightage"),
        (f" NCERT importance for {chapter.name}:", "Must read NCERT", "NCERT not needed", "Optional", "Will help", "A", "NCERT based"),
        (f"Previous year NEET questions from {chapter.name}:", "5-8 questions", "1-2", "None", "Varies", "A", "Direct from NCERT"),
        (f"Concept clarity for {chapter.name}:", "Very important", "Somewhat", "Not needed", "Optional", "A", "Foundation"),
        (f"Formula memorization for {chapter.name}:", "Essential", "Derive if needed", "Not needed", "Optional", "A", "Know formulas"),
        (f"Diagram based questions in {chapter.name}:", "Very common", "Rare", "Never", "Sometimes", "A", "Visual questions"),
        (f"Numerical problems in {chapter.name}:", "Common", "Uncommon", "Not asked", "Sometimes", "A", "Calculations"),
        (f"Assertion-Reason type from {chapter.name}:", "Frequently asked", "Rare", "Never", "Sometimes", "A", "A-R type"),
        (f"Match the following from {chapter.name}:", "Often", "Rare", "Never", "Sometimes", "A", "Matrix type"),
        (f"Common mistakes in {chapter.name}:", "Units and signs", "Formula application", "Both", "None", "C", "Error-prone"),
        (f"Best books for {chapter.name}:", "NCERT + reference", "Any book", "Only reference", "No book", "A", "Standard books"),
        (f"Time management for {chapter.name}:", "Allocate more time", "Less time", "No change", "Varies", "A", "Time sensitive"),
        (f"Difficulty level in NEET for {chapter.name}:", "Moderate", "Easy", "Very difficult", "Varies", "A", "Balanced"),
        (f"Revision frequency for {chapter.name}:", "Weekly", "Monthly", "Before exam", "Varies", "A", "Regular"),
        (f"Must know topics in {chapter.name}:", "All important", "Selected only", "Skip hard", "Varies", "A", "Complete coverage"),
        (f"Practice questions needed for {chapter.name}:", "20-30", "5-10", "40+", "Varies", "A", "Practice quantity"),
        (f"Board vs NEET for {chapter.name}:", "NEET more detailed", "Both same", "Board detailed", "None", "A", "NEET focused"),
        (f"Definition based questions in {chapter.name}:", "Very common", "Rare", "Never", "Sometimes", "A", "Definitions"),
        (f"Example based questions in {chapter.name}:", "Common", "Uncommon", "Not asked", "Sometimes", "A", "Examples"),
        (f"Application based in {chapter.name}:", "Very common", "Rare", "Never", "Sometimes", "A", "Real life"),
        (f"MCQ difficulty in {chapter.name}:", "Tricky options", "Straight forward", "Both", "None", "A", "Tricky"),
        (f"Scoring potential in {chapter.name}:", "High if prepared", "Low", "Medium", "Depends", "A", "Scoring topic"),
        (f"Formula sheet for {chapter.name}:", "Must prepare", "Not necessary", "Optional", "Will help", "D", "Helpful"),
        (f"Mock test importance for {chapter.name}:", "Very high", "Moderate", "Low", "Not needed", "A", "Testing"),
        (f"Expert tip for {chapter.name}:", "Master NCERT", "Solve past papers", "Clear concepts", "All", "D", "All combined"),
        (f"Connection with other topics in {chapter.name}:", "Strong", "Weak", "No connection", "Varies", "A", "Linked topics"),
        (f"Daily practice for {chapter.name}:", "15-20 questions", "5-10", "25-30", "Varies", "A", "Daily practice"),
        (f"Key concept in {chapter.name} for NEET:", "Must understand", "Memorize only", "Skip", "Optional", "A", "Core concept"),
    ]
    
    MCQQuestion.objects.filter(chapter=chapter).delete()
    
    for order, mcq in enumerate(neet_mcqs):
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
print("Done! NEET chapters now have 30 MCQs each")
print("="*60)