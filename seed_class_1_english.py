import os
import django
import sys

# Set up Django environment
sys.path.append('c:/VidyaHub')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

def seed_english_questions():
    print("🔤 Seeding 30 English Questions for Class 1...")
    
    grade = Grade.objects.get(name='Class 1')
    subject = Subject.objects.get(grade=grade, slug='english')
    chapter = Chapter.objects.get(subject=subject, slug='basics')

    MCQQuestion.objects.filter(chapter=chapter).delete()

    questions = [
        ("Which is a vowel?", "B", "C", "A", "D", "C", "vowels are A, E, I, O, U."),
        ("What is the first letter of 'Apple'?", "A", "B", "C", "D", "A", "Apple starts with A."),
        ("Find the small letter for 'E'?", "e", "f", "a", "k", "A", "'e' is the small letter."),
        ("Which animal says 'Moo'?", "Cat", "Dog", "Cow", "Pig", "C", "A cow says moo."),
        ("The color of a leaf is...", "Red", "Blue", "Green", "Yellow", "C", "Leaves are green."),
        ("Opposite of 'Big' is...", "Large", "Small", "Tall", "Short", "B", "Small is the opposite of big."),
        ("Which one is a fruit?", "Carrot", "Potato", "Apple", "Onion", "C", "Apple is a fruit."),
        ("What is the plural of 'Cat'?", "Cats", "Cates", "Caties", "Cata", "A", "Just add 's' to make cats."),
        ("Which letter comes after 'J'?", "I", "K", "L", "M", "B", "K comes after J."),
        ("A ___ fly in the sky.", "Dog", "Bird", "Fish", "Cat", "B", "Birds fly."),
        # 11-20
        ("What is the color of the sky?", "Green", "Red", "Blue", "Pink", "C", "The sky is blue."),
        ("Identify the correctly spelled word:", "Appel", "Apple", "Aple", "Appll", "B", "Apple is correct."),
        ("Which is a naming word (Noun)?", "Run", "Jump", "Rahul", "Fast", "C", "Rahul is a name."),
        ("Small letter for 'G' is...", "q", "g", "p", "j", "B", "'g' is the small form."),
        ("Which is a rhyming word for 'Bat'?", "Ball", "Cat", "Toy", "Bat", "B", "Bat and Cat rhyme."),
        ("I ___ a student.", "is", "am", "are", "be", "B", "I always takes 'am'."),
        ("What do we do with our eyes?", "Hear", "Smell", "See", "Eat", "C", "We see with our eyes."),
        ("The sun rises in the...", "West", "East", "North", "South", "B", "The sun rises in the East."),
        ("Opposite of 'Happy' is...", "Sad", "Glad", "Joy", "Funny", "A", "Sad is the opposite of happy."),
        ("A ___ has seven colors.", "Cloud", "Rainbow", "Sun", "Moon", "B", "A rainbow has 7 colors."),
        # 21-30
        ("Which one is a vegetable?", "Mango", "Potato", "Grapes", "Orange", "B", "Potato is a vegetable."),
        ("What is the last letter of 'Alphabet'?", "A", "Z", "T", "E", "C", "Alphabet ends with 't'."),
        ("Choose the odd one out:", "Apple", "Mango", "Banana", "Rose", "D", "Rose is a flower, others are fruits."),
        ("I have two ___.", "Hands", "Hand", "Handes", "Handy", "A", "Plural of hand is hands."),
        ("The king of the jungle is...", "Tiger", "Lion", "Elephant", "Monkey", "B", "Lion is the king."),
        ("Which letter is missing: B, C, _, E", "D", "F", "A", "G", "A", "D comes between C and E."),
        ("What do we use to cut paper?", "Pen", "Eraser", "Scissors", "Ruler", "C", "Scissors are used for cutting."),
        ("Opposite of 'Night' is...", "Dark", "Evening", "Day", "Morning", "C", "Day is the opposite of night."),
        ("A baby dog is called a...", "Kitten", "Puppy", "Calf", "Kid", "B", "A puppy is a baby dog."),
        ("Which is a magic word?", "Hello", "Bye", "Please", "Hey", "C", "Please is a polite magic word.")
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
    print(f"✅ Successfully seeded 30 English questions!")

if __name__ == '__main__':
    seed_english_questions()
