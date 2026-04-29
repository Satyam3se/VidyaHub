import os
import django
import sys

# Set up Django environment
sys.path.append('c:/VidyaHub')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

def seed_maths_questions():
    print("🔢 Seeding 30 Maths Questions for Class 1...")
    
    grade = Grade.objects.get(name='Class 1')
    subject = Subject.objects.get(grade=grade, slug='maths')
    chapter = Chapter.objects.get(subject=subject, slug='basics')

    # Clear existing to avoid duplicates if re-run
    MCQQuestion.objects.filter(chapter=chapter).delete()

    questions = [
        ("What is 1 + 1?", "1", "2", "3", "4", "B", "1+1 is 2."),
        ("What comes after 5?", "4", "6", "7", "8", "B", "The number after 5 is 6."),
        ("Which shape has 3 sides?", "Circle", "Square", "Triangle", "Rectangle", "C", "A triangle has three sides."),
        ("What is 2 + 3?", "4", "5", "6", "1", "B", "2+3 equals 5."),
        ("Counting: 1, 2, _, 4", "3", "5", "0", "6", "A", "The missing number is 3."),
        ("Which is the smallest number?", "10", "5", "8", "2", "D", "2 is the smallest here."),
        ("What is 5 - 1?", "4", "6", "3", "2", "A", "5 minus 1 is 4."),
        ("How many fingers are in one hand?", "4", "5", "10", "6", "B", "A normal hand has 5 fingers."),
        ("What is 0 + 7?", "0", "7", "70", "1", "B", "Anything plus zero is the number itself."),
        ("Which is a big number?", "1", "20", "5", "3", "B", "20 is larger than the others."),
        # Row 11-20
        ("What is 2 + 2?", "3", "5", "4", "6", "C", "2+2 is 4."),
        ("What is 10 - 0?", "0", "1", "10", "100", "C", "Taking nothing away leaves it the same."),
        ("How many corners does a square have?", "3", "4", "5", "0", "B", "A square has 4 corners."),
        ("What is 4 + 1?", "3", "5", "6", "4", "B", "4+1 is 5."),
        ("What comes before 10?", "8", "9", "11", "12", "B", "9 comes just before 10."),
        ("Which is round?", "Square", "Triangle", "Circle", "Cube", "C", "A circle is round."),
        ("What is 3 + 3?", "6", "7", "9", "33", "A", "3+3 is 6."),
        ("What is 8 - 2?", "5", "6", "7", "4", "B", "8 minus 2 is 6."),
        ("How many legs does a dog have?", "2", "4", "6", "1", "B", "Dogs have 4 legs."),
        ("What is half of 2?", "0", "2", "1", "3", "C", "Half of 2 is 1."),
        # Row 21-30
        ("What is 5 + 5?", "10", "15", "55", "20", "A", "5+5 is 10."),
        ("What is 9 - 9?", "9", "18", "0", "1", "C", "Subtracting a number from itself is 0."),
        ("Which is a shape?", "Apple", "Circle", "Banana", "Cat", "B", "A circle is a mathematical shape."),
        ("What is 6 + 1?", "5", "6", "7", "8", "C", "6 plus 1 is 7."),
        ("Counting: 8, 9, _", "10", "11", "7", "12", "A", "10 comes after 9."),
        ("What is 4 - 2?", "1", "2", "3", "4", "B", "4 minus 2 is 2."),
        ("How many eyes do you have?", "1", "2", "3", "4", "B", "Humans usually have 2 eyes."),
        ("What is 7 + 2?", "8", "9", "10", "72", "B", "7+2 is 9."),
        ("What is 1 + 0?", "0", "1", "11", "2", "B", "1 plus nothing is 1."),
        ("What is 3 - 1?", "1", "2", "3", "0", "B", "3 minus 1 is 2.")
    ]

    for i, q in enumerate(questions):
        MCQQuestion.objects.create(
            chapter=chapter,
            question_text=q[0],
            option_a=q[1],
            option_b=q[2],
            option_c=q[3],
            option_d=q[4],
            correct_option=q[5],
            explanation=q[6],
            order=i
        )
    
    print(f"✅ Successfully seeded 30 Maths questions for Class 1!")

if __name__ == '__main__':
    seed_maths_questions()
