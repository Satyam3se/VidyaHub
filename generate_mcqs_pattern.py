"""
Pattern-based MCQ Generator following CBSE curriculum
Generates MCQs for ALL chapters based on chapter name and subject patterns
"""

import os
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

import django
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Chapter, MCQQuestion

print("=" * 60)
print("CBSE Pattern-based MCQ Generator")
print("=" * 60)

# CBSE Question Banks by Subject and Topic Patterns
MATH_QUESTIONS = {
    'number': [
        ("What is the place value of 5 in 5,672?", "5000", "500", "50", "5", "A", "5 is in thousands place"),
        ("Which is the smallest 4-digit number?", "1000", "999", "1001", "9999", "A", "1000 is the smallest 4-digit number"),
        ("What comes after 999?", "1000", "998", "1001", "999", "A", "999 + 1 = 1000"),
        ("Write 543 in expanded form:", "500 + 40 + 3", "5000 + 400 + 3", "50 + 40 + 3", "500 + 400 + 30", "A", "5 hundreds + 4 tens + 3 ones"),
        ("Which digit is in tens place in 892?", "8", "9", "2", "892", "B", "9 is in tens place"),
    ],
    'addition': [
        ("What is 456 + 123?", "579", "578", "580", "569", "A", "456 + 123 = 579"),
        ("Find the sum of 234 and 345:", "579", "578", "577", "580", "A", "234 + 345 = 579"),
        ("What is 500 + 250?", "750", "700", "800", "650", "A", "500 + 250 = 750"),
        ("Add 123 + 234 + 345:", "702", "700", "701", "703", "A", "123 + 234 + 345 = 702"),
        ("What is 0 + 789?", "789", "0", "7890", "790", "A", "Any number + 0 = the number"),
    ],
    'subtraction': [
        ("What is 890 - 123?", "767", "766", "768", "765", "A", "890 - 123 = 767"),
        ("Find the difference: 500 - 250", "250", "240", "260", "300", "A", "500 - 250 = 250"),
        ("What is 1000 - 1?", "999", "998", "1001", "900", "A", "1000 - 1 = 999"),
        ("Subtract 45 from 100:", "55", "45", "65", "50", "A", "100 - 45 = 55"),
        ("What remains when 100 is subtracted from 234?", "134", "124", "144", "134", "A", "234 - 100 = 134"),
    ],
    'multiplication': [
        ("What is 12 x 4?", "48", "46", "44", "50", "A", "12 × 4 = 48"),
        ("Find the product: 15 x 3", "45", "40", "50", "35", "A", "15 × 3 = 45"),
        ("What is 20 x 5?", "100", "90", "110", "80", "A", "20 × 5 = 100"),
        ("Multiply 25 by 4:", "100", "90", "110", "80", "A", "25 × 4 = 100"),
        ("What is 11 x 7?", "77", "70", "75", "80", "A", "11 × 7 = 77"),
    ],
    'division': [
        ("What is 84 ÷ 4?", "21", "20", "22", "24", "A", "84 ÷ 4 = 21"),
        ("Divide 99 by 9:", "11", "10", "12", "9", "A", "99 ÷ 9 = 11"),
        ("What is 144 ÷ 12?", "12", "10", "14", "11", "A", "144 ÷ 12 = 12"),
        ("Find quotient: 75 ÷ 15", "5", "4", "6", "3", "A", "75 ÷ 15 = 5"),
        ("What is 64 ÷ 8?", "8", "6", "7", "9", "A", "64 ÷ 8 = 8"),
    ],
    'fraction': [
        ("What is 1/2 of 20?", "10", "5", "15", "20", "A", "Half of 20 = 10"),
        ("Which is a proper fraction?", "2/5", "5/2", "3/3", "7/5", "A", "Numerator < denominator"),
        ("What is 3/4 as decimal?", "0.75", "0.5", "0.25", "1.0", "A", "3/4 = 0.75"),
        ("Add 1/4 + 1/4:", "1/2", "1/8", "2/4", "1", "A", "1/4 + 1/4 = 1/2"),
        ("Which equals 1/2?", "3/6", "2/3", "3/4", "4/5", "A", "3/6 simplifies to 1/2"),
    ],
    'money': [
        ("How many paise in Rs. 5?", "500 paise", "50 paise", "5 paise", "5000 paise", "A", "1 Rupee = 100 paise"),
        ("What is cost of 2 pencils at Rs. 5 each?", "Rs. 10", "Rs. 7", "Rs. 5", "Rs. 12", "A", "2 × 5 = 10"),
        ("You have Rs. 50. Pen costs Rs. 30. How much left?", "Rs. 20", "Rs. 80", "Rs. 30", "Rs. 10", "A", "50 - 30 = 20"),
        ("Cost of 5 pens at Rs. 10 each:", "Rs. 50", "Rs. 40", "Rs. 60", "Rs. 15", "A", "5 × 10 = 50"),
        ("Rs. 100 divided among 4 children. Each gets:", "Rs. 25", "Rs. 20", "Rs. 30", "Rs. 50", "A", "100 ÷ 4 = 25"),
    ],
    'time': [
        ("How many minutes in 2 hours?", "120 minutes", "60 minutes", "100 minutes", "90 minutes", "A", "1 hour = 60 minutes"),
        ("What time is 3 o'clock?", "3:00", "3:30", "2:00", "4:00", "A", "3 o'clock is 3:00"),
        ("Minutes in half hour:", "30 minutes", "15 minutes", "45 minutes", "60 minutes", "A", "Half hour = 30 min"),
        ("Days in a week:", "7 days", "5 days", "6 days", "8 days", "A", "A week has 7 days"),
        ("Months in a year:", "12 months", "10 months", "11 months", "13 months", "A", "A year has 12 months"),
    ],
    'shape': [
        ("How many sides does a square have?", "4 sides", "3 sides", "5 sides", "6 sides", "A", "Square has 4 equal sides"),
        ("Which shape has no corners?", "Circle", "Square", "Triangle", "Rectangle", "A", "Circle has no corners"),
        ("How many sides a triangle has?", "3 sides", "4 sides", "5 sides", "2 sides", "A", "Triangle has 3 sides"),
        ("A rectangle has how many sides?", "4 sides", "3 sides", "5 sides", "6 sides", "A", "Rectangle has 4 sides"),
        ("Which is a 3D shape?", "Cube", "Square", "Circle", "Triangle", "A", "Cube is a 3D shape"),
    ],
    'measurement': [
        ("What is unit to measure length?", "Meter", "Kilogram", "Liter", "Second", "A", "Length is measured in meters"),
        ("1 meter = ___ centimeters?", "100 cm", "10 cm", "1000 cm", "10", "A", "1 m = 100 cm"),
        ("What is weight measured in?", "Kilogram", "Meter", "Liter", "Second", "A", "Weight is in kg"),
        ("1 kilogram = ___ grams?", "1000 grams", "100 grams", "10 grams", "100 grams", "A", "1 kg = 1000 g"),
        ("Which is bigger: 1 meter or 100 centimeters?", "Both equal", "1 meter", "100 cm", "Cannot say", "A", "1 m = 100 cm"),
    ],
    'data': [
        ("Which shows data in pictures?", "Pictograph", "Bar graph", "Line graph", "Pie chart", "A", "Pictograph uses pictures"),
        ("In a bar graph, height shows:", "Frequency", "Color", "Shape", "Size", "A", "Bar height shows frequency"),
        ("Tally marks represent:", "Numbers", "Letters", "Shapes", "Colors", "A", "Each tally = 1 count"),
    ],
    'pattern': [
        ("What comes next: 2, 4, 6, 8, ?", "10", "9", "11", "12", "A", "Even numbers: +2"),
        ("Next term: A, C, E, G, ?", "I", "K", "J", "H", "A", "Skip one letter"),
        ("What is missing: 5, 10, 15, ?, 25", "20", "18", "22", "19", "A", "Table of 5"),
    ],
    'default': [
        ("Solve: 45 + 32 = ?", "77", "76", "78", "75", "A", "45 + 32 = 77"),
        ("What is 100 - 25?", "75", "70", "80", "65", "A", "100 - 25 = 75"),
        ("Multiply: 8 × 6 = ?", "48", "46", "44", "50", "A", "8 × 6 = 48"),
        ("Divide: 96 ÷ 8 = ?", "12", "10", "11", "14", "A", "96 ÷ 8 = 12"),
        ("What is 1/4 of 80?", "20", "15", "25", "40", "A", "80 ÷ 4 = 20"),
    ],
}

SCIENCE_QUESTIONS = {
    'plant': [
        ("Which part of plant makes food?", "Leaves", "Roots", "Stem", "Flowers", "A", "Leaves contain chlorophyll"),
        ("Plants need ___ to make food:", "Sunlight", "Moon", "Stars", "Soil only", "A", "Photosynthesis needs light"),
        ("Roots absorb:", "Water and minerals", "Sunlight", "Air", "Food", "A", "Roots take water/minerals"),
        ("Which is a flowering plant?", "Rose", "Moss", "Fern", "Algae", "A", "Rose produces flowers"),
        ("Seeds are formed in:", "Flowers", "Roots", "Stem", "Leaves", "A", "Flowers develop into fruits with seeds"),
    ],
    'animal': [
        ("What do animals need from food?", "Energy", "Soil", "Sunlight", "Water only", "A", "Food gives energy"),
        ("Which is a carnivore?", "Lion", "Cow", "Goat", "Rabbit", "A", "Lion eats meat"),
        ("Baby of dog is called:", "Puppy", "Calf", "Kitten", "Foal", "A", "Dog's baby is puppy"),
        ("How do animals move?", "Legs, wings, fins", "Roots", "Leaves", "Stems", "A", "Animals have various body parts"),
        ("Which animal lays eggs?", "Hen", "Cow", "Dog", "Cat", "A", "Hens lay eggs"),
    ],
    'food': [
        ("Which is a source of protein?", "Dal", "Rice", "Sugar", "Oil", "A", "Pulses contain protein"),
        ("Which gives us energy?", "Rice", "Water", "Salt", "Chalk", "A", "Carbohydrates give energy"),
        ("Which is a healthy food?", "Fruits", "Junk food", "Soft drinks", "Chips", "A", "Fruits are nutritious"),
        ("We should eat ___ daily:", "Vegetables", "Only rice", "More sugar", "Fried food", "A", "Vegetables are essential"),
        ("Which is a balanced diet?", "Rice + dal + vegetables", "Only chips", "Only sugar", "Fried items", "A", "Balanced diet has all nutrients"),
    ],
    'water': [
        ("Water covers ___ of Earth?", "71%", "50%", "20%", "10%", "A", "Most of Earth is water"),
        ("Which is water in three forms?", "Ice, water, steam", "Stone", "Sand", "Soil", "A", "Solid, liquid, gas"),
        ("WaterChanges to ice at:", "0°C", "100°C", "50°C", "25°C", "A", "Freezing point of water"),
        ("Rainwater is:", "Pure", "Salty", "Dirty", "Sweet", "A", "Rain is distilled water"),
        ("We should ___ water:", "Save", "Waste", "Pollute", "Throw", "A", "Water is precious"),
    ],
    'air': [
        ("Air has:", "Oxygen", "Only carbon dioxide", "Nothing", "Soil", "A", "Air contains oxygen"),
        ("What does breathing give us?", "Oxygen", "Carbon dioxide", "Nitrogen", "Soil", "A", "We breathe in oxygen"),
        ("Air moves to form:", "Wind", "Water", "Soil", "Fire", "A", "Moving air is wind"),
        ("Air is needed for:", "Burning", "Sleeping", "Growing", "All of these", "D", "Air is essential for life"),
        ("Which shows air has weight?", "Fan makes cool air", "Balloon inflates", "Leaf falls", "All of these", "D", "Air takes space and has weight"),
    ],
    'body': [
        ("We breathe through:", "Nose", "Mouth only", "Ears", "Eyes", "A", "Nose filters and warms air"),
        ("How many bones in adult body?", "206", "200", "300", "100", "A", "Adult has 206 bones"),
        ("Which organ pumps blood?", "Heart", "Lungs", "Brain", "Stomach", "A", "Heart pumps blood"),
        ("We think with our:", "Brain", "Heart", "Liver", "Lungs", "A", "Brain is the control center"),
        ("Which organ helps us see?", "Eyes", "Nose", "Ears", "Tongue", "A", "Eyes enable vision"),
    ],
    'light': [
        ("We need light to see:", "Yes", "No", "Sometimes", "Not sure", "A", "Light is essential for sight"),
        ("Which is a source of light?", "Sun", "Mirror", "Moon", "Glass", "A", "Sun is natural light"),
        ("Light travels in:", "Straight line", "Curved path", "Circle", "Any direction", "A", "Light moves in straight lines"),
        ("What reflects light?", "Mirror", "Wood", "Stone", "Water only", "A", "Mirrors reflect light well"),
        ("Shadow forms because:", "Light is blocked", "It is dark", "Sun is not out", "All of these", "A", "Blockage of light creates shadow"),
    ],
    'force': [
        ("Force can make things:", "Move", "Stop", "Change direction", "All of these", "D", "Force causes motion changes"),
        ("Which is a pushing force?", "Push", "Magnet", "Gravity", "Friction", "A", "Pushing is an applied force"),
        ("Friction acts between:", "Surfaces in contact", "Far apart objects", "Same objects", "No contact needed", "A", "Friction needs contact"),
        ("Gravity pulls things:", "Downwards", "Upwards", "Sideways", "Any direction", "A", "Gravity is downward pull"),
        ("Which is magnetic force?", "Magnet attracting iron", "Push", "Pull", "Friction", "A", "Magnets attract iron objects"),
    ],
    'earth': [
        ("Earth is made of:", "Rocks and soil", "Only water", "Only air", "Fire", "A", "Earth has rocks and soil"),
        ("Which is natural resource?", "Water", "Plastic", "Steel", "Plastic bags", "A", "Water is natural"),
        ("We should not ___ waste:", "Litter", "Recycle", "Use bin", "Compost", "A", "Littering harms environment"),
        ("Earth provides us with:", "Food, water, shelter", "Only toys", "Only roads", "Only buildings", "A", "Earth gives all essentials"),
        ("We should protect Earth by:", "Not polluting", "Using more plastic", "Cutting trees", "Wasting water", "A", "Protection needs no pollution"),
    ],
    'default': [
        ("Which is a natural resource?", "Water", "Plastic", "Polythene", "Glass", "A", "Water occurs naturally"),
        ("Our body needs:", "All of these", "Only food", "Only water", "Only air", "A", "We need food, water, air"),
        ("Plants and animals are:", "Living things", "Non-living", "Rocks", "Clouds", "A", "They show life processes"),
        ("Which is essential for life?", "Air", "Plastic", "Metal", "Synthetic items", "A", "Air is essential"),
        ("We should ___ nature:", "Protect", "Harm", "Ignore", "Destroy", "A", "Nature needs protection"),
    ],
}

ENGLISH_QUESTIONS = {
    'grammar': [
        ("Which is a noun?", "Book", "Running", "Happy", "Quickly", "A", "Noun names a thing/person/place"),
        ("What is opposite of 'big'?", "Small", "Tall", "Happy", "Fast", "A", "Small is opposite of big"),
        ("Which is a verb?", "Run", "Beautiful", "Happy", "Book", "A", "Verb shows action"),
        ("'Cat' is a:", "Noun", "Verb", "Adjective", "Adverb", "A", "Cat is a naming word"),
        ('"Run" is example of:', "Verb", "Noun", "Adjective", "Adverb", "A", "Run is an action word"),
    ],
    'reading': [
        ("A story mainly has:", "Characters and events", "Only numbers", "Only pictures", "Rules", "A", "Stories have characters"),
        ("We read to:", "Understand and enjoy", "Only memorize", "Waste time", "Only pass exams", "A", "Reading builds knowledge"),
        ("A poem has:", "Rhyming words", "Rules", "Numbers", "All pages", "A", "Poems use rhyme"),
        ("Comprehension means:", "Understanding", "Memorizing", "Skipping", "Ignoring", "A", "Comprehension is understanding"),
        ("Reading skills help in:", "All subjects", "Only English", "Only Math", "Only Science", "A", "Reading is for all learning"),
    ],
    'writing': [
        ("A sentence starts with:", "Capital letter", "Small letter", "Number", "Symbol", "A", "First letter is capital"),
        ("A sentence ends with:", "Period or question mark", "Comma", "Space", "Number", "A", "End mark completes sentence"),
        ("Paragraph is about:", "One idea", "Many topics", "Random thoughts", "Numbers", "A", "One main topic per paragraph"),
        ("Writing helps:", "Express thoughts", "Forget", "Waste time", "Nothing", "A", "Writing is expression"),
        ("Good writing includes:", "Clear ideas", "Only long sentences", "Many mistakes", "Random words", "A", "Clarity matters"),
    ],
    'spelling': [
        ("Which is spelled correctly?", "School", "Scooll", "Skul", "Scol", "A", "School - s-c-h-o-o-l"),
        ("Find correct spelling of 'apple':", "Apple", "Aple", "Appel", "appel", "A", "Apple is correct"),
        ("Which is right: 'their' or 'there'?", "their", "ther", "thier", "thre", "A", "their shows possession"),
        ("Correct: 'because' or 'bcoz'?", "because", "bcoz", "becoz", "becuse", "A", "because is proper"),
        ("Right spelling: 'friend' or 'frnd'?", "friend", "frend", "frind", "frnd", "A", "friend spelled correctly"),
    ],
    'vocabulary': [
        ("What is meaning of 'happy'?", "Joyful", "Sad", "Angry", "Tired", "A", "Happy means joyful"),
        ("Opposite of 'above':", "Below", "High", "Up", "Top", "A", "Below is opposite of above"),
        ("Synonym of 'happy':", "Joyful", "Sad", "Tired", "Slow", "A", "Happy and joyful are synonyms"),
        ("'Beautiful' means:", "Pretty", "Ugly", "Old", "New", "A", "Beautiful means pretty"),
        ("What is 'fast' opposite?", "Slow", "Quick", "Rapid", "Swift", "A", "Fast and slow are opposites"),
    ],
    'default': [
        ("English helps us:", "Communicate", "Only read", "Only write", "Only speak", "A", "English enables communication"),
        ("We learn English to:", "Express ourselves", "Confuse", "Just pass", "Nothing", "A", "Language is expression tool"),
        ("Reading English stories helps:", "Learn new words", "Waste time", "Get poor marks", "Nothing", "A", "Stories expand vocabulary"),
        ("Writing practice improves:", "All skills", "Nothing", "Only memory", "Only spelling", "A", "Practice helps all skills"),
        ("English is spoken:", "Globally", "Only in India", "Only UK", "Only USA", "A", "English is worldwide"),
    ],
}

HINDI_QUESTIONS = {
    'default': [
        ("'पानी' का अर्थ है:", "Water", "Fire", "Air", "Earth", "A", "पानी means water"),
        ("'गाय' क्या है?", "Animal", "Bird", "Fish", "Insect", "A", "गाय is an animal (cow)"),
        ("'किताब' का अर्थ है:", "Book", "Pen", "Note", "Page", "A", "किताब means book"),
        ("'स्कूल' में क्या होता है?", "School", "Hospital", "Market", "Temple", "A", "स्कूल means school"),
        ("'माता' का अर्थ है:", "Mother", "Father", "Sister", "Brother", "A", "माता means mother"),
    ],
}

EVS_QUESTIONS = {
    'default': [
        ("What is good for health?", "Exercise", "Junk food", "Staying awake", "Smoking", "A", "Exercise keeps us healthy"),
        ("We should brush teeth:", "Twice daily", "Once a week", "Never", "Once a month", "A", "Twice daily is healthy"),
        ("Which is safe to eat?", "Home food", "Street food", "Mud", "Raw meat", "A", "Home food is safe"),
        ("Sleep is important for:", "Rest", "Working", "Eating", "Nothing", "A", "Sleep gives rest"),
        ("We should wash hands before:", "Eating", "Sleeping", "Running", "Watching TV", "A", "Clean hands prevent disease"),
    ],
}

def get_topic_key(chapter_name):
    """Detect topic from chapter name"""
    name = chapter_name.lower()

    topics = {
        'number': ['number', 'counting', 'digit', 'place', 'value'],
        'addition': ['addition', 'add', 'sum', 'plus'],
        'subtraction': ['subtraction', 'subtract', 'minus', 'difference', 'take'],
        'multiplication': ['multiplication', 'multiply', 'product', 'times'],
        'division': ['division', 'divide', 'quotient', 'share'],
        'fraction': ['fraction', 'half', 'quarter', 'part'],
        'money': ['money', 'rupee', 'paise', 'cost', 'price', 'coin'],
        'time': ['time', 'clock', 'hour', 'minute', 'day', 'month', 'year', 'week'],
        'shape': ['shape', 'triangle', 'square', 'circle', 'rectangle', 'angle', 'line', ' symmetry'],
        'measurement': ['measurement', 'length', 'weight', 'height', 'measure', 'heavy', 'light', 'meter', 'kilogram'],
        'data': ['data', 'graph', 'chart', 'picture', 'tally', 'bar'],
        'pattern': ['pattern', 'sequence', 'series'],
        'plant': ['plant', 'tree', 'leaf', 'flower', 'seed', 'root', 'stem', 'photosynthesis'],
        'animal': ['animal', 'bird', 'fish', 'dog', 'cat', 'cow', 'animal', 'pet', 'wild'],
        'food': ['food', 'eat', 'diet', 'nutrition', 'balanced', 'health', 'vitamin'],
        'water': ['water', 'rain', 'river', 'ocean', 'drink', 'liquid'],
        'air': ['air', 'wind', 'breathe', 'oxygen'],
        'body': ['body', 'bone', 'blood', 'heart', 'brain', 'organ', 'muscle', 'skin'],
        'light': ['light', 'shadow', 'sun', 'lamp', 'dark'],
        'force': ['force', 'push', 'pull', 'motion', 'friction', 'magnet', 'gravity'],
        'earth': ['earth', 'rock', 'soil', 'land', 'environment', 'pollution', 'natural'],
        'grammar': ['grammar', 'noun', 'verb', 'adjective', 'sentence', 'word'],
        'reading': ['story', 'poem', 'reading', 'comprehension'],
        'writing': ['writing', 'paragraph', 'essay', 'letter'],
        'spelling': ['spelling', 'spell', 'alphabet', 'letter'],
        'vocabulary': ['meaning', 'opposite', 'synonym', 'word meaning'],
    }

    for topic, keywords in topics.items():
        for kw in keywords:
            if kw in name:
                return topic

    return None

def get_question_bank(subject_name):
    """Get appropriate question bank"""
    subject = subject_name.lower()

    if 'math' in subject or 'गणित' in subject:
        return MATH_QUESTIONS
    elif 'science' in subject or 'विज्ञान' in subject or ' evs' in subject:
        return SCIENCE_QUESTIONS
    elif 'english' in subject or 'अंग्रेजी' in subject:
        return ENGLISH_QUESTIONS
    elif 'hindi' in subject or 'हिंदी' in subject:
        return HINDI_QUESTIONS
    elif 'evs' in subject:
        return EVS_QUESTIONS
    else:
        return MATH_QUESTIONS

def get_questions_for_chapter(chapter, count=20):
    """Get questions matching chapter topic"""
    topic = get_topic_key(chapter.name)
    subject = chapter.subject.name
    question_bank = get_question_bank(subject_name=subject)

    # Try specific topic first
    if topic and topic in question_bank:
        questions = question_bank[topic]
    else:
        questions = question_bank.get('default', MATH_QUESTIONS['default'])

    # Return 20 unique questions (shuffle)
    q_list = list(questions)
    random.shuffle(q_list)
    return q_list[:count]

def seed_all_chapters():
    """Seed all chapters with MCQs"""
    chapters = Chapter.objects.all().order_by('subject__grade__order')

    total = chapters.count()
    chapters_needing = 0
    processed = 0

    print(f"\nTotal chapters: {total}")

    for chapter in chapters:
        existing = MCQQuestion.objects.filter(chapter=chapter).count()
        if existing == 0:
            chapters_needing += 1

    print(f"Chapters needing MCQs: {chapters_needing}")

    if chapters_needing == 0:
        print("\nAll chapters already have MCQs!")
        return

    print(f"\nGenerating MCQs...")

    for i, chapter in enumerate(chapters, 1):
        existing = MCQQuestion.objects.filter(chapter=chapter).count()
        if existing > 0:
            continue

        questions = get_questions_for_chapter(chapter)

        for order, q in enumerate(questions):
            MCQQuestion.objects.create(
                chapter=chapter,
                question_text=q[0],
                option_a=q[1],
                option_b=q[2],
                option_c=q[3],
                option_d=q[4],
                correct_option=q[5],
                explanation=q[6],
                order=order
            )

        processed += 1
        print(f"[{i}] {chapter.subject.grade.name} - {chapter.subject.name}: {chapter.name} -> {len(questions)} MCQs")

    print(f"\n" + "=" * 60)
    print(f"Done! Generated MCQs for {processed} chapters")
    print("=" * 60)

if __name__ == '__main__':
    seed_all_chapters()