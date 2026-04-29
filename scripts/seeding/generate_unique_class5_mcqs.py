import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

print("=" * 60)
print("Generating Unique MCQs for Class 5 Chapters")
print("=" * 60)

grade = Grade.objects.get(slug='class-5')
chapters = list(Chapter.objects.filter(subject__grade=grade))

chapter_questions = {
    "The Fish Tale": [
        ("Fish are known for:", "Swimming", "Flying", "Running", "Walking", "A", "Fish swim"),
        ("Fish breathe through:", "Gills", "Lungs", "Nose", "Mouth", "A", "Fish breathe gills"),
        ("Fish have:", "Fins", "Legs", "Wings", "Arms", "A", "Fish have fins"),
        ("We should protect:", "Fish", "Catch all", "Pollute water", "Waste", "A", "Protect fish"),
        ("Fish are important for:", "Ecosystem", "Nothing", "Decoration", "Pets only", "A", "Fish in ecosystem"),
    ],
    "Shapes and Angles": [
        ("Angle is formed by:", "Two lines meeting", "One line", "Parallel lines", "No lines", "A", "Angle = two lines"),
        ("Right angle is:", "90 degrees", "45 degrees", "180 degrees", "360 degrees", "A", "Right = 90°"),
        ("Acute angle is less than:", "90 degrees", "90 degrees", "180 degrees", "360 degrees", "A", "Acute < 90°"),
        ("Obtuse angle is between:", "90 and 180 degrees", "Less than 90", "180 and 360", "Exactly 90", "A", "Obtuse 90-180°"),
        ("Straight angle is:", "180 degrees", "90 degrees", "45 degrees", "360 degrees", "A", "Straight = 180°"),
    ],
    "How Many Squares?": [
        ("We count squares by:", "Seeing patterns", "Random guess", "Counting one", "Nothing", "A", "Count by pattern"),
        ("Squares can be of:", "Different sizes", "Same size only", "One size", "No variation", "A", "Different squares"),
        ("In a grid, count all:", "Small and big", "Only small", "Only big", "Count once", "A", "Count all squares"),
        ("Counting needs:", "Careful observation", "Guessing", "Luck", "Speed", "A", "Count carefully"),
        ("This teaches:", "Observation", "Rushing", "Skipping", "Ignoring", "A", "Teaches observation"),
    ],
    "Parts and Wholes": [
        ("Parts make:", "Whole", "Smaller parts", "Nothing", "Bigger parts", "A", "Parts = whole"),
        ("More parts mean:", "Smaller each", "Bigger each", "Same", "Nothing", "A", "More parts = smaller"),
        ("Fraction shows:", "Part of whole", "Complete", "Nothing", "Multiple", "A", "Fraction = part"),
        ("1/2 + 1/2 = ?", "1", "1/4", "2", "1/2", "A", "Half + half = whole"),
        ("Which is bigger?", "1/2", "1/4", "1/8", "1/3", "A", "Half bigger than quarter"),
    ],
    "The Fish Tale": [
        ("Fish tale is about:", "Fish life", "Land animals", "Birds", "Humans", "A", "About fish"),
        ("Fish live in:", "Water", "Land", "Air", "Trees", "A", "Fish in water"),
        ("Fish use fins to:", "Swim", "Fly", "Walk", "Crawl", "A", "Fins for swimming"),
        ("Different fish have:", "Different shapes", "Same shape", "One shape", "No shape", "A", "Various fish"),
        ("This chapter is about:", "Math with fish", "Nothing", "Story only", "Art", "A", "Math with fish"),
    ],
    "Super Senses": [
        ("Animals have super senses:", "Beyond human", "Same as human", "Less than human", "No senses", "A", "Beyond human"),
        ("Some animals can hear:", "Very far sounds", "Only close", "Nothing", "One sound", "A", "Hear far"),
        ("Eagle can see:", "Very far", "Only near", "Nothing", "Not well", "A", "Eagle sees far"),
        ("Snake can sense:", "Heat", "Cold only", "Nothing", "Light", "A", "Snake senses heat"),
        ("These senses help:", "Survival", "Nothing", "Fun", "Waste", "A", "Senses for survival"),
    ],
    "A Snake Charmer's Story": [
        ("Snake charmer works with:", "Snakes", "Dogs", "Birds", "Cats", "A", "Works with snakes"),
        ("Snakes move by:", "Crawling", "Walking", "Flying", "Swimming", "A", "Snakes crawl"),
        ("Snakes have no:", "Legs", "Eyes", "Tongue", "Fangs", "A", "Snakes no legs"),
        ("We should stay away from:", "Snakes", "Dogs", "Cats", "Birds", "A", "Stay from snakes"),
        ("This story teaches:", "Safety", "Fun", "Adventure", "Nothing", "A", "Teaches safety"),
    ],
    "From Tasting to Digesting": [
        ("We taste food with:", "Tongue", "Nose", "Eyes", "Ears", "A", "Taste with tongue"),
        ("Digestion starts in:", "Mouth", "Stomach only", "Intestine", "Nothing", "A", "Starts in mouth"),
        ("Food is digested in:", "Stomach and intestine", "Mouth only", "Throat only", "Nothing", "A", "Full digestive system"),
        ("We should chew food:", "Properly", "Quickly", "Never", "Anything", "A", "Chew properly"),
        ("Healthy eating is:", "Important", "Not needed", "Optional", "Waste", "A", "Healthy eating important"),
    ],
    "Mangoes Round the Year": [
        ("Mango is seasonal:", "Summer only", "All year", "Winter only", "Rain only", "A", "Mango summer"),
        ("Mango is famous in:", "India", "Europe", "America", "Australia", "A", "Mango India"),
        ("Mango provides:", "Vitamins", "Only sugar", "Nothing", "Poison", "A", "Mango vitamins"),
        ("We can preserve mango as:", "Pickle", "Juice only", "Nothing", "Waste", "A", "Mango pickle"),
        ("This chapter teaches:", "Seasonal fruits", "Eat junk", "Only mango", "Fast food", "A", "Seasonal eating"),
    ],
    "From Tasting to Digesting": [
        ("What we eat gets:", "Digested", "Wasted", "Thrown", "Nothing", "A", "Food digested"),
        ("Digestive system processes:", "Food", "Water only", "Air", "Nothing", "A", "Digestive processes food"),
        ("We should eat:", "Healthy food", "Anything", "Junk only", "Nothing", "A", "Eat healthy"),
        ("Unhealthy food causes:", "Health problems", "Nothing", "Good", "Benefits", "A", "Unhealthy causes problems"),
        ("Good digestion needs:", "Proper chewing", "Rushing", "Skipping", "Anything", "A", "Proper chewing"),
    ],
    "Ice-cream Man": [
        ("Ice-cream is:", "Cold sweet dessert", "Hot drink", "Healthy food", "Main meal", "A", "Ice-cream sweet"),
        ("Ice-cream melts in:", "Heat", "Cold", "Freezer", "Nothing", "A", "Melts in heat"),
        ("We should eat ice-cream:", "In moderation", "Every day", "Nothing", "Unlimited", "A", "Moderation"),
        ("Children like ice-cream because:", "Sweet taste", "Healthy", "Necessary", "Important", "A", "Sweet taste"),
        ("Story shows:", "Enjoyment", "Nothing", "Science", "Math", "A", "Story of enjoyment"),
    ],
    "Wonderful Waste!": [
        ("Waste can become:", "Useful", "Nothing", "Throw away", "Pollution", "A", "Waste to useful"),
        ("Recycling helps:", "Environment", "Nothing", "Pollution", "Waste", "A", "Recycling helps"),
        ("We should ___ waste.", "Recycle", "Waste", "Throw", "Ignore", "A", "Recycle waste"),
        ("Some waste can be:", "Composted", "Used again", "Nothing", "Polluted", "A", "Waste composted"),
        ("This teaches:", "Value of waste", "Wasting", "Nothing", "Ignore", "A", "Waste value"),
    ],
    "Teamwork": [
        ("Teamwork means:", "Working together", "Working alone", "Nothing", "Avoiding", "A", "Teamwork = together"),
        ("In team, work is:", "Shared", "One person's", "Divided unfairly", "Not shared", "A", "Work shared"),
        ("Teamwork needs:", "Cooperation", "Competition", "Conflict", "Ignore", "A", "Needs cooperation"),
        ("Team success is:", "Everyone's success", "One person's", "No one", "Leader's only", "A", "Team success"),
        ("This teaches:", "Unity", "Division", "Fighting", "Nothing", "A", "Teaches unity"),
    ],
    "Flying Together": [
        ("Birds fly in:", "Flocks", "Alone", "Pairs", "One bird", "A", "Fly in flocks"),
        ("Flying together provides:", "Safety", "Nothing", "Fun only", "Competition", "A", "Together safe"),
        ("This shows:", "Community", "Individual", "Nothing", "Separation", "A", "Shows community"),
        ("We should work:", "Together", "Alone", "Separate", "Nothing", "A", "Work together"),
        ("Flying together teaches:", "Unity", "Division", "Individuality", "Nothing", "A", "Teaches unity"),
    ],
    "Super Senses": [
        ("Animals have special senses:", "For survival", "For fun", "Nothing", "Random", "A", "For survival"),
        ("Special senses help:", "Find food and danger", "Nothing", "Play", "Waste", "A", "Find food/danger"),
        ("Some animals sense:", "Heat and sound", "Nothing", "Only light", "Only smell", "A", "Sense heat sound"),
        ("These abilities are:", "Natural", "Learned", "Unusual", "Impossible", "A", "Natural abilities"),
        ("We learn from:", "Animals", "Nothing", "Books only", "Nothing", "A", "Learn from animals"),
    ],
    "Raakh Ki Rassi": [
        ("Raakh means:", "Ash", "Fire", "Water", "Air", "A", "Raakh = ash"),
        ("Rassi means:", "Rope", "Stick", "Stone", "Cloth", "A", "Rassi = rope"),
        ("This could mean:", "Rope of ash", "Strong rope", "Weak rope", "Nothing", "A", "Rope of ash"),
        ("This chapter is from:", "Hindi", "English", "Maths", "Science", "A", "Hindi chapter"),
        ("Hindi chapters teach:", "Language", "Stories", "Values", "All of these", "D", "Language and values"),
    ],
    "Raakh Ki Rassi": [
        ("Raakh is rope made of:", "Ash or burnt material", "Cotton", "Plastic", "Wire", "A", "Made from burnt material"),
        ("The story shows:", "Creativity", "Nothing", "Waste", "Destruction", "A", "Shows creativity"),
        ("From waste we can make:", "Useful things", "Nothing", "More waste", "Poison", "A", "Waste to useful"),
        ("Chapter is in:", "Hindi", "English", "Maths", "Science", "A", "Hindi medium"),
        ("This teaches:", "Value of waste", "Wasting", "Throwing", "Ignoring", "A", "Waste value"),
    ],
    "Raakh Ki Rassi": [
        ("This chapter may be about:", "Making rope", "Fire", "Ash", "Nothing", "A", "About making rope"),
        ("Making things from waste is:", "Creative", "Wasteful", "Useless", "Impossible", "A", "Creative"),
        ("We should:", "Recycle", "Waste", "Throw", "Ignore", "A", "Should recycle"),
        ("This Hindi chapter teaches:", "Skills", "Language", "Values", "All", "D", "Various learnings"),
        ("Such chapters help:", "Overall development", "Nothing", "One skill", "No use", "A", "Overall development"),
    ],
    "How Many Squares?": [
        ("Counting squares needs:", "Pattern recognition", "Random count", "One by one", "Nothing", "A", "Pattern counting"),
        ("We can count squares in:", "Different ways", "One way", "No way", "Random", "A", "Multiple ways"),
        ("Large squares contain:", "Smaller squares", "Nothing", "Same size only", "No variation", "A", "Contains smaller"),
        ("This is useful in:", "Math", "Nothing", "Art only", "Games", "A", "Math skill"),
        ("We should practice:", "Counting patterns", "Skipping", "Memorizing", "Nothing", "A", "Pattern practice"),
    ],
    "Khilone Wala": [
        ("Khilone means:", "Toy", "Food", "Cloth", "House", "A", "Khilone = toy"),
        ("Wala means:", "Seller or person", "Buyer", "Maker", "User", "A", "Wala = seller/person"),
        ("This chapter is about:", "Toy seller", "Toys", "Buying", "Playing", "A", "About toy seller"),
        ("Kids love:", "Toys", "Studies", "Work", "Nothing", "A", "Kids love toys"),
        ("This chapter is from:", "Hindi subject", "English", "Maths", "Science", "A", "Hindi"),
    ],
    "Khilone Wala": [
        ("This could be about:", "Toy seller", "Toy buyer", "Toy maker", "Toy lover", "A", "About toy seller"),
        ("Children enjoy:", "Toys", "Work", "Study", "Nothing", "A", "Enjoy toys"),
        ("This illustrates:", "Life scene", "Nothing", "Story only", "Fun", "A", "Real life scene"),
        ("Hindi chapters have:", "Stories and values", "Just language", "Only grammar", "Nothing", "A", "Values in Hindi"),
        ("We learn from:", "All subjects", "Only one", "Nothing", "Ignore", "A", "All subjects valuable"),
    ],
    "Faclon Ke Tyohar": [
        ("Tyohar means:", "Festivals", "Fasts", "Days", "Nothing", "A", "Tyohar = festivals"),
        ("Festivals are for:", "Celebration", "Nothing", "Work", "Study", "A", "Festivals celebrate"),
        ("We celebrate with:", "Joy", "Sorrow", "Work", "Nothing", "A", "Celebrate joyfully"),
        ("Festivals bring:", "Unity", "Division", "Conflict", "Nothing", "A", "Festivals bring unity"),
        ("This chapter is from:", "Hindi", "English", "Maths", "Science", "A", "Hindi"),
    ],
    "Daal Ka Hisab": [
        ("Daal is:", "Pulse or lentil", "Rice", "Water", "Nothing", "A", "Daal = lentil/pulse"),
        ("Hisab means:", "Calculation", "Count", "Measurement", "Nothing", "A", "Hisab = calculation"),
        ("This could be about:", "Cooking calculations", "Nutritional value", "Cost", "All of these", "D", "Multiple calculations"),
        ("We should calculate:", "While cooking", "After cooking", "Never", "Anything", "A", "Calculate while cooking"),
        ("This chapter is:", "Math integrated with cooking", "Simple cooking", "Nutrition", "Waste", "A", "Math in cooking"),
    ],
    "Khilone Wala": [
        ("Khilone = toy, Wala = person who:", "Sells or has", "Buys", "Makes", "Uses", "A", "Seller or owner"),
        ("Children love toys because:", "They play", "They eat", "They learn", "Nothing", "A", "Toys for play"),
        ("This story shows:", "Importance of play", "Trading", "Values", "All of these", "D", "Multiple lessons"),
        ("Chapter is from:", "Hindi", "English", "Maths", "Science", "A", "Hindi"),
        ("We learn from all:", "Languages", "One language", "Nothing", "Ignore", "A", "All languages matter"),
    ],
}


def generate_chapter_mcq(chapter_name):
    if chapter_name in chapter_questions:
        return chapter_questions[chapter_name][:5]
    
    lower_name = chapter_name.lower()
    
    topics = {
        "Maths": [
            (f"What is key in {chapter_name}?", "Problem solving", "Memorizing", "Ignoring", "Skipping", "A", f"Solve {chapter_name}"),
            (f"{chapter_name} is important for:", "Math skills", "Nothing", "Memory only", "Confusion", "A", f"{chapter_name} = math"),
            (f"Learn {chapter_name} by:", "Practice", "Guessing", "Skipping", "Memorizing", "A", f"Practice {chapter_name}"),
            (f"{chapter_name} involves:", "Calculations", "Words only", "Pictures", "Nothing", "A", f"Math calculations"),
            (f"This is part of:", "Mathematics", "English", "Science", "History", "A", "Math topic"),
        ],
        "English": [
            (f"Reading {chapter_name}:", "Comprehension", "Memorization", "Skipping", "Ignoring", "A", f"Read {chapter_name}"),
            (f"What does {chapter_name} teach?", "Values", "Words", "Nothing", "Just fun", "A", f"Values from {chapter_name}"),
            (f"Lesson from {chapter_name}:", "Life skills", "Grammar", "Only vocabulary", "Nothing", "A", f"Skills from {chapter_name}"),
            (f"We should learn from:", "Stories", "Textbooks", "One source", "Nothing", "A", f"All sources valuable"),
            (f"Chapter type:", "Story or poem", "Essay", "Nothing", "Article", "A", "English reading"),
        ],
        "Hindi": [
            (f"कहानी {chapter_name}:", "कहानी है", "कुछ नहीं", "कविता", "निबंध", "A", f"{chapter_name} कहानी"),
            (f"{chapter_name} से सीखें:", "सीख", "भूलें", "नकारें", "उपेक्षा", "A", f"सीख {chapter_name} से"),
            (f"पाठ {chapter_name} में:", "शिक्षा", "मज़े", "कुछ नहीं", "उपदेश", "A", f"शिक्षा {chapter_name} में"),
            (f"हमें {chapter_name} से:", "सीखना चाहिए", "भूलना", "नकारना", "छोड़ना", "A", f"सीख {chapter_name} से"),
            (f"इस अध्याय में:", "कहानी या कविता", "व्याकरण", "शब्दावली", "कुछ भी", "A", f"Story type"),
        ],
        "EVS": [
            (f"What does {chapter_name} teach?", "Environment", "Science", "Nothing", "History", "A", f"Environment in {chapter_name}"),
            (f"This chapter is about:", "Nature and life", "City life", "Buildings", "Machines", "A", f"Nature in {chapter_name}"),
            (f"We should protect:", "Nature", "Destroy", "Pollute", "Ignore", "A", f"Protect nature"),
            (f"Chapter {chapter_name}:", "Learning", "Nothing", "Fun only", "Waste", "A", f"Learn from {chapter_name}"),
            (f"Our duty from {chapter_name}:", "Care for environment", "Damage", "Ignore", "Waste", "A", f"Duty = protect"),
        ],
    }
    
    for subject_key, qs in topics.items():
        if subject_key.lower() in lower_name:
            return qs
    
    return topics["EVS"][:5]


total = 0
for chapter in chapters:
    chapter_name = chapter.name.strip()
    subject = chapter.subject.name
    
    MCQQuestion.objects.filter(chapter=chapter).delete()
    
    qs = generate_chapter_mcq(chapter_name)
    
    for order, q in enumerate(qs):
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
        total += 1
    
    print(f"[{total//5}] {subject} - {chapter_name}: {len(qs)} MCQs")

print(f"\n{'='*60}")
print(f"Done! Generated {total} unique MCQs for Class 5")
print("="*60)