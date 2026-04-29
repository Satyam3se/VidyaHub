import os
import django
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion


def seed():
    print("Seeding Class 2 Fundamentals...")

    # 1. Grade
    grade, _ = Grade.objects.get_or_create(
        name='Class 2', slug='class-2', defaults={'order': 2}
    )

    # 2. Subjects + Basic Chapters
    subjects_data = [
        {'name': 'Maths',   'slug': 'maths',   'icon': 'plus-circle'},
        {'name': 'English', 'slug': 'english',  'icon': 'languages'},
        {'name': 'Hindi',   'slug': 'hindi',    'icon': 'book-open'},
        {'name': 'EVS',     'slug': 'evs',      'icon': 'leaf'},
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


    # ================================================================
    # MATHS  (Class 2 level – two-digit arithmetic, shapes, time, etc.)
    # ================================================================
    maths_subject = Subject.objects.get(grade=grade, slug='maths')
    maths_chapter = Chapter.objects.get(subject=maths_subject, slug='basics')
    MCQQuestion.objects.filter(chapter=maths_chapter).delete()

    maths_qs = [
        ("What is 15 + 10?",       "24", "25", "26", "20",  "B", "15 + 10 = 25."),
        ("What is 30 - 12?",       "17", "18", "19", "16",  "B", "30 - 12 = 18."),
        ("What is 4 x 3?",         "10", "11", "12", "13",  "C", "4 multiplied by 3 = 12."),
        ("Which is the largest?",  "45", "54", "44", "50",  "B", "54 is the largest."),
        ("What is 20 + 35?",       "55", "50", "45", "60",  "A", "20 + 35 = 55."),
        ("Count by 2s: 2, 4, _, 8","5",  "6",  "7",  "3",  "B", "The pattern is +2, so next is 6."),
        ("What is 50 - 20?",       "20", "25", "30", "35",  "C", "50 - 20 = 30."),
        ("How many sides has a rectangle?", "3", "4", "5", "6", "B", "A rectangle has 4 sides."),
        ("What is 11 + 11?",       "21", "22", "23", "20",  "B", "11 + 11 = 22."),
        ("Which number is even?",  "3",  "7",  "8",  "9",  "C", "8 is even (divisible by 2)."),
        # 11-20
        ("What is 5 x 2?",         "8",  "10", "12", "15",  "B", "5 x 2 = 10."),
        ("What is 100 - 1?",       "99", "98", "100","101","A", "100 - 1 = 99."),
        ("What is 3 + 27?",        "28", "30", "29", "31",  "B", "3 + 27 = 30."),
        ("A week has how many days?","5", "6", "7", "8",   "C", "A week has 7 days."),
        ("What is 2 x 2 x 2?",     "4",  "6",  "8",  "10", "C", "2x2=4, 4x2=8."),
        ("What is half of 20?",    "5",  "8",  "10", "15",  "C", "Half of 20 is 10."),
        ("Which is odd?",          "12", "14", "15", "16",  "C", "15 is odd."),
        ("What is 9 x 2?",         "16", "17", "18", "19",  "C", "9 x 2 = 18."),
        ("40 + 40 = ?",            "80", "70", "60", "90",  "A", "40 + 40 = 80."),
        ("Count backwards from 10: 10, 9, _, 7","8","6","5","11","A","Next is 8."),
        # 21-30
        ("How many months in a year?","10","11","12","13",  "C", "A year has 12 months."),
        ("What is 7 x 2?",         "12", "13", "14", "15",  "C", "7 x 2 = 14."),
        ("What is 25 + 25?",       "40", "45", "50", "55",  "C", "25 + 25 = 50."),
        ("What is 36 - 6?",        "28", "29", "30", "31",  "C", "36 - 6 = 30."),
        ("Which shape has no corners?","Triangle","Square","Circle","Rectangle","C","A circle has no corners."),
        ("How many zeros in 100?", "1",  "2",  "3",  "0",  "B", "100 has two zeros."),
        ("What is 6 x 3?",         "15", "16", "17", "18",  "D", "6 x 3 = 18."),
        ("What is 1 dozen?",       "10", "11", "12", "13",  "C", "1 dozen = 12 items."),
        ("What is 99 + 1?",        "99", "100","101","98",  "B", "99 + 1 = 100."),
        ("50 - 25 = ?",            "20", "25", "30", "35",  "B", "50 - 25 = 25."),
    ]
    for i, q in enumerate(maths_qs):
        MCQQuestion.objects.create(
            chapter=maths_chapter, question_text=q[0],
            option_a=q[1], option_b=q[2], option_c=q[3], option_d=q[4],
            correct_option=q[5], explanation=q[6], order=i
        )
    print("  Seeded 30 Maths questions.")


    # ================================================================
    # ENGLISH  (Class 2 level – sentences, grammar, nouns, adjectives)
    # ================================================================
    en_subject = Subject.objects.get(grade=grade, slug='english')
    en_chapter = Chapter.objects.get(subject=en_subject, slug='basics')
    MCQQuestion.objects.filter(chapter=en_chapter).delete()

    en_qs = [
        ("Which sentence is correct?",
         "She go to school.", "She goes to school.", "She going to school.", "She goed to school.", "B",
         "'She goes' is correct subject-verb agreement."),
        ("What is the plural of 'box'?",
         "Boxs", "Boxies", "Boxes", "Boes", "C",
         "Words ending in -x take -es: boxes."),
        ("A ___ is a person, place or thing.",
         "Verb", "Noun", "Adjective", "Adverb", "B",
         "A noun denotes a person, place or thing."),
        ("Which is an adjective?",
         "Run", "Slowly", "Beautiful", "Jump", "C",
         "Beautiful describes something, so it is an adjective."),
        ("Opposite of 'hot' is:",
         "Warm", "Cool", "Cold", "Humid", "C",
         "The opposite of hot is cold."),
        ("The dog ___ in the park.",
         "run", "runs", "running", "ran", "B",
         "'The dog runs' – singular subject takes singular verb."),
        ("Which word rhymes with 'cake'?",
         "Cup", "Lake", "Car", "Bat", "B",
         "Cake and Lake both end in '-ake'."),
        ("Find the verb: 'The bird sings sweetly.'",
         "Bird", "Sweetly", "Sings", "The", "C",
         "'Sings' is the action word (verb)."),
        ("The sun rises in the ___.",
         "West", "North", "South", "East", "D",
         "The sun rises in the East."),
        ("Capital letter of 'river' is:",
         "river", "River", "RIVER", "riVer", "B",
         "A proper noun or start of sentence uses a capital."),
        # 11-20
        ("Best word for 'very big':",
         "Tiny", "Small", "Huge", "Short", "C",
         "Huge means very big."),
        ("Plural of 'child' is:",
         "Childs", "Children", "Childes", "Childrens", "B",
         "The irregular plural of child is children."),
        ("Which is a question sentence?",
         "Go home.", "She is happy.", "Where are you?", "I love cats.", "C",
         "A question sentence ends with a question mark."),
        ("___ is a pronoun for boys.",
         "She", "He", "They", "It", "B",
         "'He' is used for boys/males."),
        ("Which word means 'to start'?",
         "End", "Finish", "Begin", "Stop", "C",
         "Begin means to start."),
        ("Tom ___ his homework.",
         "do", "does", "doing", "done", "B",
         "'Tom does' – third-person singular."),
        ("Find the noun: 'The happy puppy jumped.'",
         "Happy", "Jumped", "Puppy", "The", "C",
         "Puppy is the person/animal/thing – noun."),
        ("What does 'enormous' mean?",
         "Tiny", "Very large", "Fast", "Slow", "B",
         "Enormous means extremely large."),
        ("Which punctuation ends a statement?",
         "?", "!", ".", ",", "C",
         "A full stop (.) ends a statement."),
        ("Opposite of 'dark' is:",
         "Gloomy", "Shadow", "Bright", "Night", "C",
         "Bright is the opposite of dark."),
        # 21-30
        ("I ___ going to school tomorrow.",
         "is", "are", "am", "be", "C",
         "'I am' is correct."),
        ("Correct spelling:",
         "Frend", "Freind", "Friend", "Frenid", "C",
         "Friend is correctly spelled F-R-I-E-N-D."),
        ("Which is a describing word?",
         "Run", "Quickly", "Red", "Cat", "C",
         "'Red' is an adjective – a describing word."),
        ("A sentence starts with a ___ letter.",
         "small", "capital", "middle", "silent", "B",
         "Every sentence begins with a capital letter."),
        ("Plural of 'tooth' is:",
         "Tooths", "Teeth", "Toothes", "Teeths", "B",
         "The irregular plural is teeth."),
        ("She ___ a nice dress today.",
         "wear", "wears", "wearing", "wore", "B",
         "'She wears' – singular present tense."),
        ("What is a synonym for 'happy'?",
         "Sad", "Angry", "Joyful", "Scared", "C",
         "Joyful means the same as happy."),
        ("'Cats' is the ___ of 'cat'.",
         "adjective", "verb", "plural", "pronoun", "C",
         "Cats is the plural form of cat."),
        ("Which sentence has correct punctuation?",
         "She is a girl", "She is a girl.", "she is a girl.", "She is a girl!", "B",
         "A statement ends with a full stop."),
        ("Opposite of 'early' is:",
         "Soon", "Quick", "Late", "Fast", "C",
         "Late is the opposite of early."),
    ]
    for i, q in enumerate(en_qs):
        MCQQuestion.objects.create(
            chapter=en_chapter, question_text=q[0],
            option_a=q[1], option_b=q[2], option_c=q[3], option_d=q[4],
            correct_option=q[5], explanation=q[6], order=i
        )
    print("  Seeded 30 English questions.")


    # ================================================================
    # HINDI  (Class 2 level – romanized for Windows encoding safety)
    # ================================================================
    hi_subject = Subject.objects.get(grade=grade, slug='hindi')
    hi_chapter = Chapter.objects.get(subject=hi_subject, slug='basics')
    MCQQuestion.objects.filter(chapter=hi_chapter).delete()

    hi_qs = [
        ("'Mera' ka arth kya hai?",
         "Tera", "Mera / My", "Humara", "Unka", "B",
         "Mera means My in Hindi."),
        ("'Phool' ka ling kya hai?",
         "Stree ling", "Pulling", "Napunsak ling", "Koi nahi", "B",
         "Phool (flower) is pulling (masculine)."),
        ("Ginti mein 11 ko kya kahte hain?",
         "Das", "Gyarah", "Barah", "Tera", "B",
         "11 = Gyarah."),
        ("'Kamal' kahan khilta hai?",
         "Zameen par", "Paani mein", "Ped par", "Pahad par", "B",
         "Kamal (Lotus) paani mein khilta hai."),
        ("'Naman' ka arth hai:",
         "Pyaar", "Pranam / Greet", "Khana", "Padhna", "B",
         "Naman means greeting with respect."),
        ("Sapte-vaar mein pehla din kaun sa hai?",
         "Mangalwaar", "Somwaar", "Raviwaar", "Guruwaar", "C",
         "Raviwaar (Sunday) is first in most calendars."),
        ("'Aam' kis mausam mein aata hai?",
         "Sardi mein", "Barish mein", "Garmi mein", "Patjhad mein", "C",
         "Aam garmi (summer) mein aata hai."),
        ("'Billi' ki boli kya hoti hai?",
         "Bhaunakna", "Miyaun karna", "Hinhinaana", "Raambhana", "B",
         "Billi miyaun karti hai."),
        ("'Suraj' ka ling kya hai?",
         "Stree ling", "Napunsak ling", "Pulling", "Dono", "C",
         "Suraj pulling (masculine) hai."),
        ("'Pariksha' ka matlab kya hai?",
         "Khel", "Exam / Test", "Tyohar", "Chutti", "B",
         "Pariksha means exam."),
        # 11-20
        ("Barish mein kya pehnte hain?",
         "Sweater", "Raincoat", "T-shirt", "Sari", "B",
         "Barish mein raincoat pehnte hain."),
        ("'Vidyalaya' ka arth kya hai?",
         "Khel ka maidaan", "School", "Aspatal", "Mandir", "B",
         "Vidyalaya = school."),
        ("'Ha' ka vipareet kya hai?",
         "Bilkul", "Nahi", "Accha", "Shukriya", "B",
         "Ha ka vipareet Nahi hai."),
        ("Hamare rashtriya dhwaj mein kitne rang hain?",
         "Do", "Teen", "Chaar", "Paanch", "B",
         "Tiranga mein teen rang hain."),
        ("'Chaand' raat ko kaisa dikhta hai?",
         "Suraj jaise", "Chamakta hua gola", "Kaala", "Hara", "B",
         "Chaand raat ko chamakta hua gola dikhtaa hai."),
        ("'Bada' ka vipareet kya hai?",
         "Mota", "Chhota", "Uncha", "Lamba", "B",
         "Bada ka vipareet Chhota hai."),
        ("'Kapda' kahan se milta hai?",
         "Daraakht se", "Kapas ke paudhe se", "Paani se", "Pathar se", "B",
         "Kapda kapas (cotton plant) se milta hai."),
        ("Month mein kitne hafta hote hain?",
         "2", "3", "4", "5", "C",
         "Ek mahine mein lagbhag 4 hafte hote hain."),
        ("'Prayagraj' kahan sthit hai?",
         "Maharashtra", "Uttar Pradesh", "Gujarat", "Rajasthan", "B",
         "Prayagraj Uttar Pradesh mein hai."),
        ("'Ganga' kya hai?",
         "Pahad", "Nadi", "Jheel", "Samudra", "B",
         "Ganga Bharat ki pavitra nadi hai."),
        # 21-30
        ("'Angrezi' ko English mein kya kahte hain?",
         "Hindi", "English", "French", "Urdu", "B",
         "Angrezi = English."),
        ("Ginti mein 20 ko kya kahte hain?",
         "Bees", "Tera", "Pandrah", "Solah", "A",
         "20 = Bees."),
        ("'Kitab' ka bahuvachan kya hai?",
         "Kitab", "Kitabein", "Kitabi", "Kitabon", "B",
         "Kitab ka bahuvachan Kitabein hai."),
        ("'Baarish' kis mausam mein hoti hai?",
         "Garmi", "Barsaat", "Sardi", "Patjhad", "B",
         "Baarish barsaat ke mausam mein hoti hai."),
        ("Rashtriya gaan ka naam kya hai?",
         "Jana Gana Mana", "Vande Mataram", "Jai Hind", "Bharat Mata Ki Jai", "A",
         "Jana Gana Mana hamara rashtriya gaan hai."),
        ("'Dhoop' kya hai?",
         "Chaaon", "Suraj ki roshni", "Barish", "Andhera", "B",
         "Dhoop suraj ki roshni ko kehte hain."),
        ("'Jalti hui mombatti' deti hai:",
         "Paani", "Roshni", "Hawa", "Khana", "B",
         "Mombatti jalane se roshni milti hai."),
        ("'Pahal' ka arth hai:",
         "Ant", "Shuruwaat", "Beech", "Baad", "B",
         "Pahal = beginning/start."),
        ("'Seedha' ka ulta kya hai?",
         "Tedha", "Bada", "Chhota", "Lamba", "A",
         "Seedha ka ulta Tedha hai."),
        ("'Jameen' par kya gira?",
         "Suraj", "Pani ki boond", "Chaand", "Sitara", "B",
         "Paani ki boond (raindrop) zameen par girti hai."),
    ]
    for i, q in enumerate(hi_qs):
        MCQQuestion.objects.create(
            chapter=hi_chapter, question_text=q[0],
            option_a=q[1], option_b=q[2], option_c=q[3], option_d=q[4],
            correct_option=q[5], explanation=q[6], order=i
        )
    print("  Seeded 30 Hindi questions.")


    # ================================================================
    # EVS  (Class 2 level – family, community, environment, plants)
    # ================================================================
    evs_subject = Subject.objects.get(grade=grade, slug='evs')
    evs_chapter = Chapter.objects.get(subject=evs_subject, slug='basics')
    MCQQuestion.objects.filter(chapter=evs_chapter).delete()

    evs_qs = [
        ("Which part of a plant absorbs water?",
         "Leaf", "Flower", "Root", "Stem", "C",
         "Roots absorb water from the soil."),
        ("What do we breathe out?",
         "Oxygen", "Nitrogen", "Carbon Dioxide", "Steam", "C",
         "Humans exhale carbon dioxide."),
        ("Which is a domestic animal?",
         "Lion", "Tiger", "Elephant", "Cow", "D",
         "Cows are kept at home – domestic animals."),
        ("Water from the tap comes from:",
         "Clouds directly", "Underground / rivers", "Ocean directly", "Factories", "B",
         "Tap water is treated river or ground water."),
        ("Which festival has coloured water?",
         "Diwali", "Eid", "Holi", "Christmas", "C",
         "Holi is the festival of colours."),
        ("What keeps our body warm in winter?",
         "Cotton clothes", "Raincoat", "Woollen clothes", "Short sleeves", "C",
         "Woollen clothes trap heat and keep us warm."),
        ("Who makes honey?",
         "Butterfly", "Ant", "Bee", "Grasshopper", "C",
         "Bees make honey."),
        ("Which of these is NOT a fruit?",
         "Mango", "Potato", "Guava", "Papaya", "B",
         "Potato is a vegetable, not a fruit."),
        ("Sound is produced by ___.",
         "Light", "Vibrations", "Heat", "Water", "B",
         "Sound is caused by vibrations."),
        ("A doctor works at a ___.",
         "School", "Farm", "Fire station", "Hospital", "D",
         "Doctors work at hospitals."),
        # 11-20
        ("Trees give us ___ to breathe.",
         "Carbon dioxide", "Smoke", "Oxygen", "Nitrogen", "C",
         "Trees release oxygen during photosynthesis."),
        ("Which body part pumps blood?",
         "Lungs", "Heart", "Kidneys", "Brain", "B",
         "The heart pumps blood."),
        ("Where do fish live?",
         "Desert", "Forest", "Water", "Air", "C",
         "Fish live in water."),
        ("The three meals of the day are:",
         "Lunch, dinner, tea", "Breakfast, lunch, dinner", "Snack, tea, dinner", "Brunch, supper, dessert", "B",
         "The three main meals are breakfast, lunch and dinner."),
        ("Which planet do we live on?",
         "Mars", "Venus", "Saturn", "Earth", "D",
         "We live on Earth."),
        ("A seed grows into a:",
         "Stone", "Cloud", "Plant", "River", "C",
         "Seeds germinate and grow into plants."),
        ("Which month has 28 or 29 days?",
         "January", "March", "February", "April", "C",
         "February has 28 days (29 in a leap year)."),
        ("What type of home do birds make?",
         "Den", "Nest", "Burrow", "Stable", "B",
         "Birds build nests."),
        ("Which helps us see at night?",
         "Fan", "Heater", "Electric light", "Cooler", "C",
         "Electric lights help us see in the dark."),
        ("Healthy food gives us ___.",
         "Disease", "Weakness", "Energy", "Laziness", "C",
         "Healthy food provides energy to our body."),
        # 21-30
        ("What do we use to keep our teeth clean?",
         "Soap", "Shampoo", "Toothbrush and toothpaste", "Comb", "C",
         "We brush teeth with a toothbrush and paste."),
        ("A postman delivers ___.",
         "Groceries", "Medicine", "Letters and parcels", "Milk", "C",
         "A postman delivers mail and parcels."),
        ("Which season comes after summer?",
         "Winter", "Monsoon", "Spring", "Autumn", "B",
         "Monsoon (rainy season) comes after summer."),
        ("We should wash our hands:",
         "Only before eating", "Never", "Before eating and after using washroom", "Once a week", "C",
         "Washing hands prevents germs from spreading."),
        ("A rainbow appears after ___.",
         "Snowfall", "Rain", "Earthquake", "Drought", "B",
         "Rainbow appears in the sky after rain."),
        ("Which fruit is yellow and long?",
         "Apple", "Grapes", "Banana", "Watermelon", "C",
         "A banana is yellow and long."),
        ("A lion lives in the ___.",
         "Sea", "Forest", "Pond", "Farm", "B",
         "Lions live in forests and grasslands."),
        ("Which vehicle moves on water?",
         "Bus", "Train", "Boat", "Aeroplane", "C",
         "A boat moves on water."),
        ("Vegetables are eaten because they give us ___.",
         "Only taste", "Vitamins and minerals", "Fat only", "Sugar only", "B",
         "Vegetables provide vitamins and minerals."),
        ("Who protects our country?",
         "Teachers", "Doctors", "Soldiers", "Farmers", "C",
         "Soldiers protect our country."),
    ]
    for i, q in enumerate(evs_qs):
        MCQQuestion.objects.create(
            chapter=evs_chapter, question_text=q[0],
            option_a=q[1], option_b=q[2], option_c=q[3], option_d=q[4],
            correct_option=q[5], explanation=q[6], order=i
        )
    print("  Seeded 30 EVS questions.")

    total = MCQQuestion.objects.filter(chapter__subject__grade=grade).count()
    print(f"\nDone! Total MCQ questions for Class 2: {total}")


if __name__ == '__main__':
    seed()
