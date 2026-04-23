import os
import django
import sys

sys.path.append('c:/VidyaHub')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

def seed():
    print("Seeding Class 1 Fundamentals...")

    # 1. Create Grade
    grade, _ = Grade.objects.get_or_create(name='Class 1', slug='class-1', defaults={'order': 1})

    # 2. Create Subjects
    subjects_data = [
        {'name': 'Maths', 'slug': 'maths', 'icon': 'plus-circle'},
        {'name': 'English', 'slug': 'english', 'icon': 'languages'},
        {'name': 'Hindi', 'slug': 'hindi', 'icon': 'book-open'},
        {'name': 'EVS', 'slug': 'evs', 'icon': 'leaf'},
    ]

    for s_data in subjects_data:
        s, _ = Subject.objects.get_or_create(
            grade=grade, slug=s_data['slug'],
            defaults={'name': s_data['name'], 'icon': s_data['icon']}
        )
        Chapter.objects.get_or_create(
            subject=s, slug='basics',
            defaults={'name': 'The Basics', 'order': 1}
        )
        print(f"  Subject ready: {s_data['name']}")

    print("Grade and subjects ready.")


    # -- MATHS --
    maths_subject = Subject.objects.get(grade=grade, slug='maths')
    maths_chapter = Chapter.objects.get(subject=maths_subject, slug='basics')
    MCQQuestion.objects.filter(chapter=maths_chapter).delete()

    maths_qs = [
        ("What is 1 + 1?", "1", "2", "3", "4", "B", "1+1 is 2."),
        ("What comes after 5?", "4", "6", "7", "8", "B", "The number after 5 is 6."),
        ("Which shape has 3 sides?", "Circle", "Square", "Triangle", "Rectangle", "C", "A triangle has 3 sides."),
        ("What is 2 + 3?", "4", "5", "6", "1", "B", "2+3 equals 5."),
        ("Counting: 1, 2, _, 4", "3", "5", "0", "6", "A", "The missing number is 3."),
        ("Which is the smallest number?", "10", "5", "8", "2", "D", "2 is the smallest."),
        ("What is 5 - 1?", "4", "6", "3", "2", "A", "5 minus 1 is 4."),
        ("How many fingers in one hand?", "4", "5", "10", "6", "B", "One hand has 5 fingers."),
        ("What is 0 + 7?", "0", "7", "70", "1", "B", "Anything plus zero is itself."),
        ("Which is a big number?", "1", "20", "5", "3", "B", "20 is larger than the others."),
        ("What is 2 + 2?", "3", "5", "4", "6", "C", "2+2 is 4."),
        ("What is 10 - 0?", "0", "1", "10", "100", "C", "Taking nothing away leaves it the same."),
        ("How many corners does a square have?", "3", "4", "5", "0", "B", "A square has 4 corners."),
        ("What is 4 + 1?", "3", "5", "6", "4", "B", "4+1 is 5."),
        ("What comes before 10?", "8", "9", "11", "12", "B", "9 comes before 10."),
        ("Which is round?", "Square", "Triangle", "Circle", "Cube", "C", "A circle is round."),
        ("What is 3 + 3?", "6", "7", "9", "33", "A", "3+3 is 6."),
        ("What is 8 - 2?", "5", "6", "7", "4", "B", "8 minus 2 is 6."),
        ("How many legs does a dog have?", "2", "4", "6", "1", "B", "Dogs have 4 legs."),
        ("What is half of 2?", "0", "2", "1", "3", "C", "Half of 2 is 1."),
        ("What is 5 + 5?", "10", "15", "55", "20", "A", "5+5 is 10."),
        ("What is 9 - 9?", "9", "18", "0", "1", "C", "A number minus itself is 0."),
        ("Which is a shape?", "Apple", "Circle", "Banana", "Cat", "B", "A circle is a shape."),
        ("What is 6 + 1?", "5", "6", "7", "8", "C", "6 plus 1 is 7."),
        ("Counting: 8, 9, _", "10", "11", "7", "12", "A", "10 comes after 9."),
        ("What is 4 - 2?", "1", "2", "3", "4", "B", "4 minus 2 is 2."),
        ("How many eyes do you have?", "1", "2", "3", "4", "B", "Humans have 2 eyes."),
        ("What is 7 + 2?", "8", "9", "10", "72", "B", "7+2 is 9."),
        ("What is 1 + 0?", "0", "1", "11", "2", "B", "1 plus nothing is 1."),
        ("What is 3 - 1?", "1", "2", "3", "0", "B", "3 minus 1 is 2."),
    ]
    for i, q in enumerate(maths_qs):
        MCQQuestion.objects.create(chapter=maths_chapter,question_text=q[0],option_a=q[1],option_b=q[2],option_c=q[3],option_d=q[4],correct_option=q[5],explanation=q[6],order=i)
    print(f"  Seeded 30 Maths questions.")


    # -- ENGLISH --
    en_subject = Subject.objects.get(grade=grade, slug='english')
    en_chapter = Chapter.objects.get(subject=en_subject, slug='basics')
    MCQQuestion.objects.filter(chapter=en_chapter).delete()

    en_qs = [
        ("Which is a vowel?", "B", "C", "A", "D", "C", "Vowels are A, E, I, O, U."),
        ("What is the first letter of 'Apple'?", "A", "B", "C", "D", "A", "Apple starts with A."),
        ("Find the small letter for 'E'.", "e", "f", "a", "k", "A", "'e' is the small letter of E."),
        ("Which animal says 'Moo'?", "Cat", "Dog", "Cow", "Pig", "C", "A cow says moo."),
        ("The color of a leaf is:", "Red", "Blue", "Green", "Yellow", "C", "Leaves are green."),
        ("Opposite of 'Big' is:", "Large", "Small", "Tall", "Short", "B", "Small is the opposite of big."),
        ("Which one is a fruit?", "Carrot", "Potato", "Apple", "Onion", "C", "Apple is a fruit."),
        ("Plural of 'Cat' is:", "Cats", "Cates", "Caties", "Cata", "A", "Add 's' to make Cats."),
        ("Which letter comes after 'J'?", "I", "K", "L", "M", "B", "K comes after J."),
        ("A ___ fly in the sky.", "Dog", "Bird", "Fish", "Cat", "B", "Birds fly."),
        ("What is the color of the sky?", "Green", "Red", "Blue", "Pink", "C", "The sky is blue."),
        ("Correctly spelled word:", "Appel", "Apple", "Aple", "Appll", "B", "Apple is correct."),
        ("Which is a naming word (Noun)?", "Run", "Jump", "Rahul", "Fast", "C", "Rahul is a name."),
        ("Small letter for 'G' is:", "q", "g", "p", "j", "B", "'g' is the small form."),
        ("Rhyming word for 'Bat':", "Ball", "Cat", "Toy", "Bat", "B", "Bat and Cat rhyme."),
        ("I ___ a student.", "is", "am", "are", "be", "B", "'I' always takes 'am'."),
        ("What do we do with our eyes?", "Hear", "Smell", "See", "Eat", "C", "We see with our eyes."),
        ("The sun rises in the:", "West", "East", "North", "South", "B", "Sun rises in the East."),
        ("Opposite of 'Happy' is:", "Sad", "Glad", "Joy", "Funny", "A", "Sad is the opposite of happy."),
        ("A ___ has seven colors.", "Cloud", "Rainbow", "Sun", "Moon", "B", "A rainbow has 7 colors."),
        ("Which one is a vegetable?", "Mango", "Potato", "Grapes", "Orange", "B", "Potato is a vegetable."),
        ("Last letter of 'Alphabet'?", "A", "Z", "T", "E", "C", "Alphabet ends with 't'."),
        ("Odd one out:", "Apple", "Mango", "Banana", "Rose", "D", "Rose is a flower."),
        ("I have two ___.", "Hands", "Hand", "Handes", "Handy", "A", "Plural of hand is hands."),
        ("King of the jungle is:", "Tiger", "Lion", "Elephant", "Monkey", "B", "Lion is the king."),
        ("Missing: B, C, _, E", "D", "F", "A", "G", "A", "D comes between C and E."),
        ("We use ___ to cut paper.", "Pen", "Eraser", "Scissors", "Ruler", "C", "Scissors cut paper."),
        ("Opposite of 'Night' is:", "Dark", "Evening", "Day", "Morning", "C", "Day is opposite of night."),
        ("A baby dog is called a:", "Kitten", "Puppy", "Calf", "Kid", "B", "A puppy is a baby dog."),
        ("Which is a magic word?", "Hello", "Bye", "Please", "Hey", "C", "Please is a polite word."),
    ]
    for i, q in enumerate(en_qs):
        MCQQuestion.objects.create(chapter=en_chapter,question_text=q[0],option_a=q[1],option_b=q[2],option_c=q[3],option_d=q[4],correct_option=q[5],explanation=q[6],order=i)
    print(f"  Seeded 30 English questions.")


    # -- HINDI --
    hi_subject = Subject.objects.get(grade=grade, slug='hindi')
    hi_chapter = Chapter.objects.get(subject=hi_subject, slug='basics')
    MCQQuestion.objects.filter(chapter=hi_chapter).delete()

    hi_qs = [
        ("Swar varn kaun sa hai?", "ka", "kha", "a", "ga", "C", "'a' ek swar hai."),
        ("'Aam' ka pehla akshar kya hai?", "aa", "m", "n", "p", "A", "Aam 'aa' se shuru hota hai."),
        ("Inmein se kaun sa ek phal hai?", "Gajar", "Aam", "Mooli", "Aloo", "B", "Aam ek phal hai."),
        ("Aakaash ka rang kaisa hota hai?", "Laal", "Hara", "Neela", "Peela", "C", "Aakaash neela hota hai."),
        ("'Chhota' ka vilom kya hai?", "Bada", "Nanha", "Kam", "Jyada", "A", "Bada, chhota ka ulta hai."),
        ("Jungle ka raja kaun hai?", "Haathi", "Sher", "Lomdi", "Bhalu", "B", "Sher jungle ka raja hai."),
        ("Hamare paas kitni aankhein hain?", "Ek", "Do", "Teen", "Chaar", "B", "Hamari do aankhein hoti hain."),
        ("Suraj kis disha mein ugta hai?", "Paschim", "Purv", "Uttar", "Dakshin", "B", "Suraj purv mein ugta hai."),
        ("'Kitaab' ka bahuvachan kya hai?", "Kitabein", "Kitabo", "Kitabi", "Kitaben", "A", "Kitab ka kitabein hota hai."),
        ("Patang kahan udti hai?", "Paani mein", "Aasmaan mein", "Zameen par", "Ghar mein", "B", "Patang aasmaan mein udti hai."),
        ("Seb ka rang kaisa hota hai?", "Peela", "Neela", "Laal", "Kaala", "C", "Seb laal hota hai."),
        ("'Ka' ke baad kya aata hai?", "Kha", "Ga", "Gha", "Cha", "A", "Ka ke baad kha aata hai."),
        ("Gaay hamein kya deti hai?", "Anda", "Doodh", "Phal", "Sabji", "B", "Gaay doodh deti hai."),
        ("Ek paltu janwar kaun sa hai?", "Sher", "Kutta", "Haathi", "Cheeta", "B", "Kutta ek paltu janwar hai."),
        ("Mor hamara ___ pakshi hai.", "Paltu", "Rashtriya", "Jangli", "Chhota", "B", "Mor hamara rashtriya pakshi hai."),
        ("Paani ka rang kaisa hota hai?", "Safed", "Neela", "Rangheen nahi hota", "Laal", "C", "Shuddh paani rangeen nahi hota."),
        ("Ek saptah mein kitne din hote hain?", "5", "6", "7", "8", "C", "Ek saptah mein 7 din hote hain."),
        ("Haathi ki naak ko kya kahte hain?", "Poonchh", "Soondh", "Kaan", "Haath", "B", "Haathi ki naak soondh kahlati hai."),
        ("'A' se kya hota hai?", "Aam", "Imli", "Anaar", "Un", "C", "A se Anaar hota hai."),
        ("Machhli kahan rehti hai?", "Ped par", "Zameen par", "Paani mein", "Aasmaan mein", "C", "Machhli paani mein rehti hai."),
        ("Traffic light mein rukne ke liye kaun sa rang hota hai?", "Hara", "Peela", "Laal", "Neela", "C", "Laal rang rukne ka sanket hai."),
        ("Bharat ki rajdhani kya hai?", "Mumbai", "Delhi", "Kolkata", "Chennai", "B", "Bharat ki rajdhani Delhi hai."),
        ("'Raat' ka vilom kya hai?", "Subah", "Din", "Shaam", "Andhera", "B", "Raat ka ulta din hai."),
        ("Ped se hamein kya milta hai?", "Chhaya", "Phal", "Oxygen", "Sab kuch", "D", "Ped hamein sab kuch dete hain."),
        ("Ghar ki rakhwali kaun karta hai?", "Billi", "Sher", "Kutta", "Chuha", "C", "Kutta ghar ki rakhwali karta hai."),
        ("Sabjiyon ka raja kaun hai?", "Tamatar", "Aloo", "Bhindi", "Baingan", "B", "Aloo ko sabziyon ka raja kaha jata hai."),
        ("Tiranga mein kitne rang hain?", "Do", "Teen", "Chaar", "Paanch", "B", "Tiranga mein teen rang hote hain."),
        ("Khatta phal kaun sa hai?", "Kela", "Angur", "Nimbu", "Seb", "C", "Nimbu khatta hota hai."),
        ("Mithai kaun banata hai?", "Dhobi", "Halwai", "Mochi", "Naai", "B", "Halwai mithai banata hai."),
        ("Kauve ka rang kaisa hota hai?", "Safed", "Hara", "Kaala", "Neela", "C", "Kauva kaala hota hai."),
    ]
    for i, q in enumerate(hi_qs):
        MCQQuestion.objects.create(chapter=hi_chapter,question_text=q[0],option_a=q[1],option_b=q[2],option_c=q[3],option_d=q[4],correct_option=q[5],explanation=q[6],order=i)
    print(f"  Seeded 30 Hindi questions.")


    # -- EVS --
    evs_subject = Subject.objects.get(grade=grade, slug='evs')
    evs_chapter = Chapter.objects.get(subject=evs_subject, slug='basics')
    MCQQuestion.objects.filter(chapter=evs_chapter).delete()

    evs_qs = [
        ("What do plants need to make food?", "Water only", "Sunlight only", "Sunlight, water and air", "Soil only", "C", "Plants need sunlight, water and air."),
        ("Which animal gives us wool?", "Cow", "Sheep", "Goat", "Dog", "B", "Sheep gives us wool."),
        ("Water falling from clouds is called:", "Evaporation", "Rain", "Dew", "Snow", "B", "Rain falls from clouds."),
        ("Which part of a plant makes food?", "Root", "Stem", "Leaf", "Flower", "C", "Leaves make food using sunlight."),
        ("Air is:", "Visible", "Invisible", "Yellow", "Solid", "B", "We cannot see air."),
        ("Which is a source of light?", "Moon", "Mirror", "Sun", "Cloud", "C", "The Sun is a natural light source."),
        ("We breathe in:", "Carbon Dioxide", "Oxygen", "Nitrogen", "Smoke", "B", "Humans breathe in oxygen."),
        ("Which sense organ do we use to smell?", "Eyes", "Ears", "Nose", "Tongue", "C", "We smell with our nose."),
        ("A cactus stores water in its:", "Leaves", "Roots", "Stem", "Flowers", "C", "Cactus stores water in its stem."),
        ("Which season is cold?", "Summer", "Monsoon", "Winter", "Spring", "C", "Winter is the cold season."),
        ("Young one of a cat is called:", "Puppy", "Calf", "Kitten", "Foal", "C", "A baby cat is a kitten."),
        ("Which is a natural resource?", "Plastic", "Glass", "Water", "Paper", "C", "Water is a natural resource."),
        ("Trees give us:", "Rain", "Oxygen", "Rocks", "Sand", "B", "Trees give us oxygen."),
        ("What protects us from sun's heat?", "Clouds", "Stars", "Moon", "Wind", "A", "Clouds block the sun."),
        ("A tadpole grows into a:", "Fish", "Snake", "Frog", "Turtle", "C", "Tadpole becomes a frog."),
        ("We get milk from:", "Hen", "Cow", "Both cow and goat", "Fish", "C", "We get milk from cow and goat."),
        ("Which is a water animal?", "Lion", "Tiger", "Fish", "Camel", "C", "Fish live in water."),
        ("Which part of the plant is underground?", "Flower", "Root", "Leaf", "Fruit", "B", "Roots are underground."),
        ("We should throw garbage in:", "River", "Road", "Dustbin", "Garden", "C", "Always use a dustbin."),
        ("Caterpillar becomes a:", "Ant", "Bee", "Butterfly", "Spider", "C", "Caterpillar turns into a butterfly."),
        ("Which animal can live on land and water?", "Dog", "Frog", "Parrot", "Horse", "B", "Frog is an amphibian."),
        ("We use raincoat during:", "Summer", "Winter", "Rain", "Night", "C", "Raincoats protect us from rain."),
        ("To save water we should:", "Bathe 3 times", "Leave taps open", "Close taps when not in use", "Wash in rivers", "C", "Close taps to save water."),
        ("Which of these gives us fruits?", "Clouds", "Trees", "Rocks", "Rivers", "B", "Trees give us fruits."),
        ("The organ we use to taste is:", "Nose", "Tongue", "Skin", "Eyes", "B", "We taste with our tongue."),
        ("Where do birds live?", "Underground", "In the sea", "On trees and nests", "In deserts", "C", "Most birds live in nests."),
        ("Which food gives us energy?", "Rice", "Stone", "Sand", "Air", "A", "Rice gives us energy."),
        ("Honey is made by:", "Ants", "Butterflies", "Bees", "Spiders", "C", "Bees make honey."),
        ("Sunlight, air and water are:", "Man-made", "Natural gifts", "Harmful", "Artificial", "B", "They are gifts of nature."),
        ("Earthworm helps the soil by:", "Polluting it", "Making it loose and fertile", "Drying it", "Hardening it", "B", "Earthworms loosen soil."),
    ]
    for i, q in enumerate(evs_qs):
        MCQQuestion.objects.create(chapter=evs_chapter,question_text=q[0],option_a=q[1],option_b=q[2],option_c=q[3],option_d=q[4],correct_option=q[5],explanation=q[6],order=i)
    print(f"  Seeded 30 EVS questions.")

    total = MCQQuestion.objects.filter(chapter__subject__grade=grade).count()
    print(f"\nDone! Total MCQ questions for Class 1: {total}")


if __name__ == '__main__':
    seed()
