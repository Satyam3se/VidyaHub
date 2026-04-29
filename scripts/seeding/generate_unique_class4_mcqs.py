import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

print("=" * 60)
print("Generating Unique MCQs for Class 4 Chapters")
print("=" * 60)

grade = Grade.objects.get(slug='class-4')
chapters = list(Chapter.objects.filter(subject__grade=grade))

chapter_questions = {
    "Building with Bricks": [
        ("Bricks are used to build:", "Houses", "Roads only", "Bridges only", "Nothing", "A", "Bricks build houses"),
        ("Which is strong building material?", "Brick", "Paper", "Cloth", "Wood", "A", "Brick is strong"),
        ("Bricks are made of:", "Clay", "Plastic", "Glass", "Metal", "A", "Bricks from clay"),
        ("How many faces does a brick have?", "6", "4", "8", "12", "A", "Brick has 6 faces"),
        ("We use bricks to make:", "Walls", "Windows", "Roofs only", "Doors only", "A", "Walls from bricks"),
    ],
    "Long and Short": [
        ("Long and short measure:", "Length", "Weight", "Time", "Volume", "A", "Measure length"),
        ("Standard unit for length is:", "Metre", "Kilogram", "Second", "Litre", "A", "Metre for length"),
        ("1 metre = ___ centimetres", "100", "10", "1000", "1", "A", "1m = 100cm"),
        ("Ruler measures in:", "Centimetres", "Metres", "Kilometres", "Kilograms", "A", "Ruler cm"),
        ("Longer distance measured in:", "Kilometres", "Centimetres", "Grams", "Litres", "A", "Km for long distance"),
    ],
    "A Trip to Bhopal": [
        ("Trip means:", "Journey", "Stay", "Home", "Office", "A", "Trip = journey"),
        ("Bhopal is a:", "City", "Village", "Town", "Forest", "A", "Bhopal is city"),
        ("We travel for:", "Purpose", "Nothing", "Fun only", "Time pass", "A", "Travel has purpose"),
        ("Transport includes:", "Bus, train, plane", "Walking only", "Running", "Nothing", "A", "Various transport"),
        ("Planning a trip needs:", "Preparation", "Nothing", "Luck", "Magic", "A", "Trip needs planning"),
    ],
    "Tick-Tick-Tick": [
        ("Tick-tick shows:", "Time passing", "Sound only", "Music", "Noise", "A", "Sound of clock"),
        ("Clock shows:", "Time", "Date", "Year", "Weather", "A", "Clock shows time"),
        ("How many hours in day?", "24", "12", "36", "48", "A", "24 hours"),
        ("60 seconds = ___ minute", "1", "60", "10", "6", "A", "60 sec = 1 min"),
        ("AM is:", "Before noon", "After noon", "Midnight", "Evening", "A", "AM = before noon"),
    ],
    "The Way to School": [
        ("Going to school is:", "Important", "Optional", "Waste", "Burden", "A", "School important"),
        ("We should reach school:", "On time", "Late", "Never", "Sometimes", "A", "Be on time"),
        ("On the way we must follow:", "Traffic rules", "No rules", "Random", "Nothing", "A", "Follow traffic rules"),
        ("Roads have:", "Lanes", "No lanes", "Anything", "Nothing", "A", "Roads have lanes"),
        ("Crossing road we look:", "Both sides", "One side", "Sky", "Nothing", "A", "Look both sides"),
    ],
    "The Way to School": [
        ("Going to school is:", "Important", "Optional", "Waste", "Burden", "A", "School important"),
        ("We should reach school:", "On time", "Late", "Never", "Sometimes", "A", "Be on time"),
        ("On the way we must follow:", "Traffic rules", "No rules", "Random", "Nothing", "A", "Follow traffic rules"),
        ("Roads have:", "Lanes", "No lanes", "Anything", "Nothing", "A", "Roads have lanes"),
        ("Crossing road we look:", "Both sides", "One side", "Sky", "Nothing", "A", "Look both sides"),
    ],
    "Halves and Quarters": [
        ("Half means:", "One part of two", "Complete", "More than whole", "Nothing", "A", "Half = one of two"),
        ("Quarter means:", "One of four parts", "Half", "Complete", "Three parts", "A", "Quarter = one of four"),
        ("1/2 of 8 is:", "4", "2", "6", "16", "A", "Half of 8 = 4"),
        ("1/4 of 12 is:", "3", "4", "6", "2", "A", "Quarter of 12 = 3"),
        ("More halves make:", "Whole", "Less", "Nothing", "Same", "A", "Two halves = whole"),
    ],
    "Play with Patterns": [
        ("Pattern has:", "Repeating design", "Random design", "One design", "No design", "A", "Pattern repeats"),
        ("AB AB pattern is:", "Repeating two", "One only", "Random", "Three", "A", "AB pattern = two"),
        ("What comes next: 2, 4, 6, ?", "8", "7", "10", "5", "A", "Even numbers 2,4,6,8"),
        ("Square number pattern:", "1, 4, 9, 16", "1, 2, 3, 4", "2, 4, 6, 8", "1, 3, 5, 7", "A", "Square numbers"),
        ("Pattern helps find:", "Next term", "Nothing", "Random", "Confusion", "A", "Pattern = predict"),
    ],
    "Jugs and Mugs": [
        ("Litre measures:", "Liquid", "Solid", "Gas", "Weight", "A", "Litre for liquid"),
        ("1 litre = ___ millilitres", "1000", "100", "10", "1", "A", "1L = 1000ml"),
        ("Half litre is:", "500 ml", "1000 ml", "250 ml", "1500 ml", "A", "Half L = 500ml"),
        ("Millilitre measures:", "Small liquid", "Large liquid", "Solid", "Gas", "A", "ml for small"),
        ("Which holds more?", "1 L bottle", "500 ml bottle", "100 ml bottle", "250 ml bottle", "A", "1L bottle more"),
    ],
    "Fields and Fences": [
        ("Field needs:", "Fencing", "Nothing", "Only walls", "Open", "A", "Fields need fence"),
        ("Fence is for:", "Protection", "Decoration", "Nothing", "Fun", "A", "Fence protects"),
        ("Perimeter measures:", "Boundary length", "Area", "Volume", "Height", "A", "Perimeter = boundary"),
        ("Area is measured in:", "Square units", "Linear units", "Cubic units", "Nothing", "A", "Area = square units"),
        ("Fencing protects:", "Crops", "Nothing", "Animals only", "Humans only", "A", "Fence protects crops"),
    ],
    "Smart Charts": [
        ("Charts help show:", "Data visually", "Numbers only", "Words only", "Nothing", "A", "Charts visualize"),
        ("Pictograph uses:", "Pictures", "Numbers only", "Letters", "Nothing", "A", "Pictograph = pictures"),
        ("Bar graph shows:", "Comparison", "Decoration", "Stories", "Nothing", "A", "Bar graph compares"),
        ("Reading chart needs:", "Understanding", "Nothing", "Memorizing", "Guessing", "A", "Charts need understanding"),
        ("Charts make data:", "Easy to understand", "Difficult", "Confusing", "Boring", "A", "Charts simplify data"),
    ],
    "Cubes and Boxes": [
        ("Cube is:", "3D square shape", "2D shape", "Circle", "Triangle", "A", "Cube has 3 dimensions"),
        ("How many faces?", "6", "4", "8", "12", "A", "Cube has 6 faces"),
        ("Box can be:", "Cube or cuboid", "Only cube", "Flat", "Nothing", "A", "Box = cube/cuboid"),
        ("Volume measures:", "Space inside", "Surface area", "Perimeter", "Nothing", "A", "Volume = space inside"),
        ("Which has more volume?", "Bigger box", "Smaller box", "Same", "Cannot say", "A", "Bigger = more volume"),
    ],
    "How Heavy? How Light?": [
        ("Weight measured in:", "Kilograms", "Metres", "Litres", "Hours", "A", "Weight in kg"),
        ("1 kilogram = ___ grams", "1000", "100", "10", "1", "A", "1kg = 1000g"),
        ("Weighing scale measures:", "Weight", "Height", "Length", "Time", "A", "Scale measures weight"),
        ("Which is heavier?", "1 kg iron", "1 kg cotton", "Same", "Cannot say", "C", "Both same weight"),
        ("Light objects measured in:", "Grams", "Kilograms", "Metres", "Litres", "A", "Light in grams"),
    ],
    "A Trip to Bhopal": [
        ("Bhopal is in:", "Madhya Pradesh", "Maharashtra", "Rajasthan", "Gujarat", "A", "Bhopal MP"),
        ("Distance measured by:", "Kilometres", "Metres", "Grams", "Litres", "A", "Distance km"),
        ("Fuel consumption depends on:", "Distance", "Time", "Driver", "Weather", "A", "Distance affects fuel"),
        ("Transport helps:", "Travel", "Nothing", "Delay", "Trouble", "A", "Transport helps travel"),
        ("Journey planning needs:", "Distance and time", "Nothing", "Luck", "Magic", "A", "Plan with distance"),
    ],
    "Going to School": [
        ("School is for:", "Learning", "Playing only", "Fun only", "Sleeping", "A", "School for learning"),
        ("We should reach school:", "On time", "Late", "Never", "When convenient", "A", "On time matters"),
        ("Walking to school is:", "Healthy", "Tiring", "Waste", "Burden", "A", "Walking healthy"),
        ("What we learn at school:", "Many subjects", "One subject", "Nothing", "Only sports", "A", "Many subjects"),
        ("In school we make:", "Friends", "Enemies", "Nothing", "Bad habits", "A", "Make friends"),
    ],
    "Ear to Ear": [
        ("Ear is for:", "Hearing", "Seeing", "Speaking", "Eating", "A", "Ear = hearing"),
        ("Humans have ___ ears.", "Two", "One", "Three", "Four", "A", "Two ears"),
        ("Ear helps hear:", "Sounds", "Views", "Tastes", "Smells", "A", "Ear hears sounds"),
        ("We should protect:", "Hearing", "Damage", "Ignore", "Nothing", "A", "Protect hearing"),
        ("Loud sounds can:", "Harm hearing", "Help", "Improve", "Nothing", "A", "Loud sounds harmful"),
    ],
    "Noses": [
        ("Nose is for:", "Smelling", "Hearing", "Seeing", "Speaking", "A", "Nose = smell"),
        ("We breathe through:", "Nose", "Ears", "Eyes", "Mouth", "A", "Breathe through nose"),
        ("Good smell is called:", "Fragrance", "Stench", "Nothing", "Odor", "A", "Good smell = fragrance"),
        ("Bad smell is called:", "Stench", "Fragrance", "Nothing", "Nothing", "A", "Bad smell = stench"),
        ("Nose should be kept:", "Clean", "Dirty", "Blocked", "Anything", "A", "Keep nose clean"),
    ],
    "A Day with Nandu": [
        ("Nandu is character's name in:", "Story", "Real person", "Animal", "Object", "A", "Nandu in story"),
        ("This story is about:", "A day in life", "Nothing", "Adventure", "Science", "A", "Story about daily life"),
        ("We should make each day:", "Productive", "Waste", "Boring", "Lazy", "A", "Be productive"),
        ("Daily routine includes:", "Work and rest", "Only work", "Only rest", "Nothing", "A", "Work and rest"),
        ("This story teaches:", "Value of time", "Nothing", "Fun", "Nothing", "A", "Value of time"),
    ],
    "The Story of Amrita": [
        ("Amrita is:", "Character name", "Place", "Thing", "Animal", "A", "Amrita = character"),
        ("This is a:", "Story with lesson", "History", "Science", "Math", "A", "Story with lesson"),
        ("Story teaches:", "Life values", "Nothing", "Just fun", "Numbers", "A", "Story teaches values"),
        ("We learn from stories:", "Good habits", "Bad habits", "Nothing", "Confusion", "A", "Stories teach good"),
        ("Character Amrita shows:", "Good qualities", "Bad qualities", "No qualities", "Weakness", "A", "Good qualities"),
    ],
    "The Little Fir Tree": [
        ("Fir tree is a:", "Type of tree", "Flower", "Fruit", "Vegetable", "A", "Fir is tree type"),
        ("Little fir tree wanted:", "To grow big", "To stay small", "Nothing", "To die", "A", "Wanted to grow"),
        ("Growing takes:", "Time", "Nothing", "Magic", "Instant", "A", "Growing takes time"),
        ("We should be patient like:", "Tree", "Fast", "Impatient", "Quick", "A", "Be patient like tree"),
        ("Tree provides:", "Oxygen", "Nothing", "Smoke", "Pollution", "A", "Trees give oxygen"),
    ],
    "Wake Up!": [
        ("Wake up means:", "Start the day", "Sleep", "Stay awake", "Nothing", "A", "Wake up = start day"),
        ("Good morning starts:", "Fresh day", "Bad day", "Tired day", "Nothing", "A", "Morning = fresh start"),
        ("Morning routine is:", "Important", "Optional", "Waste", "Nothing", "A", "Routine important"),
        ("What we do in morning:", "Exercise and breakfast", "Sleep", "Nothing", "Late", "A", "Exercise good"),
        ("Starting day early is:", "Good habit", "Bad habit", "Waste", "Boring", "A", "Early rising good"),
    ],
    "Neha's Alarm Clock": [
        ("Alarm clock helps:", "Wake on time", "Sleep more", "Nothing", "Play music", "A", "Alarm = wake on time"),
        ("Alarm should be set:", "Before sleeping", "After waking", "Anytime", "Never", "A", "Set before sleep"),
        ("Waking on time helps:", "Be punctual", "Be late", "Be lazy", "Skip", "A", "Punctual = on time"),
        ("Alarm rings to:", "Alert us", "Disturb", "Entertain", "Nothing", "A", "Alarm alerts"),
        ("We should respect:", "Time", "Wasting", "Laziness", "Nothing", "A", "Respect time"),
    ],
    "Noses": [
        ("Nose is for:", "Smelling and breathing", "Hearing", "Seeing", "Speaking", "A", "Nose = smell and breath"),
        ("We should breathe through:", "Nose", "Mouth", "Ears", "Eyes", "A", "Breathe nose is healthy"),
        ("Nose helps smell:", "Aromas", "Sounds", "Tastes", "Colors", "A", "Nose smells"),
        ("Blocked nose causes:", "Difficulty in breathing", "Nothing", "Better", "Good", "A", "Blocked nose = trouble"),
        ("Keep nose:", "Clean", "Dirty", "Blocked", "Anything", "A", "Keep nose clean"),
    ],
    "Flying High": [
        ("Flying high is about:", "Birds or airplanes", "Swimming", "Running", "Walking", "A", "Flying = birds/planes"),
        ("Birds fly in:", "Sky", "Water", "Underground", "Caves", "A", "Fly in sky"),
        ("Airplanes help:", "Travel fast", "Swim", "Run", "Nothing", "A", "Airplanes travel"),
        ("We should protect:", "Birds", "Hunt", "Catch", "Pollute", "A", "Protect birds"),
        ("Flying is possible with:", "Wings or planes", "Legs", "Fins only", "Nothing", "A", "Wings or planes"),
    ],
    "It is Raining": [
        ("Rain comes from:", "Clouds", "Sun", "Moon", "Stars", "A", "Rain from clouds"),
        ("Rain is essential for:", "Plants", "Animals only", "Nothing", "Everyone", "A", "Rain for plants"),
        ("Too much rain causes:", "Floods", "Drought", "Fire", "Nothing", "A", "Rain too much = flood"),
        ("We should save:", "Rainwater", "Ocean only", "Tap only", "Nothing", "A", "Save rainwater"),
        ("Rainy season is:", "Monsoon", "Summer", "Winter", "Spring", "A", "Rainy = monsoon"),
    ],
    "What is Cooking": [
        ("Cooking is preparing:", "Food", "Clothes", "House", "Nothing", "A", "Cooking = food"),
        ("Heat is used in:", "Cooking", "Sleeping", "Walking", "Nothing", "A", "Heat for cooking"),
        ("We cook to make food:", "Edible and tasty", "Raw", "Useless", "Poison", "A", "Cook = make edible"),
        ("After cooking food should be:", "Covered", "Left open", "Thrown away", "Untouched", "A", "Cover cooked food"),
        ("Cooking needs:", "Care", "Nothing", "Risk", "Carelessness", "A", "Cooking needs care"),
    ],
    "Work We Do": [
        ("Work we do includes:", "Various tasks", "Only one", "Nothing", "Rest", "A", "Various work"),
        ("We do work to:", "Earn and help", "Waste", "Laze", "Nothing", "A", "Work = earn and help"),
        ("Different people do:", "Different work", "Same work", "Nothing", "No work", "A", "Different work"),
        ("Work makes us:", "Skilled", "Lazy", "Useless", "Bored", "A", "Work = skills"),
        ("We should do:", "Useful work", "Nothing", "Waste", "Avoid", "A", "Do useful work"),
    ],
    "The Story of Amrita": [
        ("Amrita is a story about:", "Life values", "Science", "Maths", "Adventure", "A", "Story about values"),
        ("We learn from:", "Stories", "Nothing", "Only numbers", "Only words", "A", "Learn from stories"),
        ("Character teaches:", "Good habits", "Bad habits", "Nothing", "Wrong", "A", "Good from story"),
        ("This story is for:", "Moral learning", "Entertainment only", "Nothing", "Fun", "A", "Moral = learn"),
        ("Stories help:", "Grow wise", "Grow confused", "Nothing", "Ignore", "A", "Stories make wise"),
    ],
    "From Here to There": [
        ("From here to there means:", "Movement", "Stay", "Nothing", "Rest", "A", "Movement = from here to there"),
        ("We travel from here to there using:", "Transport", "Nothing", "Magic", "Sleep", "A", "Using transport"),
        ("Movement needs:", "Energy", "Nothing", "Time", "Luck", "A", "Movement needs energy"),
        ("We reach there from here by:", "Distance and time", "Nothing", "Luck", "Magic", "A", "Distance time matter"),
        ("Transport helps:", "Move faster", "Wait", "Rest", "Nothing", "A", "Transport speed"),
    ],
    "He is My Brother": [
        ("This story is about:", "Family relationship", "School", "Friends", "Work", "A", "Family story"),
        ("Brother is from:", "Same family", "Different family", "Friends", "Strangers", "A", "Brother = same family"),
        ("We love:", "Family", "Strangers", "No one", "Enemies", "A", "Love family"),
        ("Family members help:", "Each other", "Nothing", "Leave", "Ignore", "A", "Family helps each other"),
        ("This teaches:", "Family values", "Nothing", "Only fun", "Random", "A", "Family values"),
    ],
    "The Little Fir Tree": [
        ("Fir Tree is a:", "Type of tree", "Flower", "Fruit", "Animal", "A", "Fir = tree"),
        ("Tree grows:", "Slowly", "Instantly", "Nothing", "Fast", "A", "Trees grow slowly"),
        ("Trees need:", "Time to grow", "Nothing", "Magic", "Instant", "A", "Growth takes time"),
        ("Little tree wanted:", "To be big", "To stay small", "Nothing", "Die", "A", "Wanted to grow"),
        ("Tree teaches:", "Patience", "Impatience", "Nothing", "Quick", "A", "Tree teaches patience"),
    ],
    "How Creatures Move": [
        ("Creatures move in:", "Different ways", "Same way", "One way", "No way", "A", "Different movement"),
        ("Fish move by:", "Swimming", "Flying", "Running", "Walking", "A", "Fish swim"),
        ("Birds move by:", "Flying", "Swimming", "Running", "Crawling", "A", "Birds fly"),
        ("Humans move by:", "Walking and running", "Swimming only", "Flying", "Nothing", "A", "Humans walk"),
        ("All creatures have:", "Movement", "No movement", "Same movement", "Fixed", "A", "All creatures move"),
    ],
    "Drop by Drop": [
        ("Drop by drop means:", "Small amounts accumulate", "One drop", "Nothing", "Large amount", "A", "Small accumulates"),
        ("Water drops make:", "Rivers over time", "Nothing", "Immediately", "Poison", "A", "Drops make rivers"),
        ("Every drop:", "Counts", "Nothing", "Wasted", "Ignored", "A", "Every drop counts"),
        ("We should save:", "Every drop", "Waste", "Ignore", "Pollute", "A", "Save every drop"),
        ("Small efforts make:", "Big difference", "Nothing", "No change", "Confusion", "A", "Small efforts = big"),
    ],
    "A Beautiful Cloth": [
        ("Cloth is made from:", "Threads", "Paper", "Plastic", "Metal", "A", "Cloth from threads"),
        ("Weaving makes:", "Cloth", "Paper", "Plastic", "Nothing", "A", "Weaving = cloth"),
        ("Cloth is used for:", "Making clothes", "Eating", "Writing", "Nothing", "A", "Cloth = clothes"),
        ("Different clothes for:", "Different occasions", "Same always", "Nothing", "Everywhere", "A", "Occasion clothes"),
        ("Cloth protects us from:", "Weather", "Nothing", "Fire", "Water only", "A", "Cloth from weather"),
    ],
    "Web of Life": [
        ("Web of life shows:", "Interconnection", "Nothing", "Single", "Separation", "A", "Life connected"),
        ("All living things:", "Depend on each other", "Independent", "Never", "Nothing", "A", "All depend"),
        (" Ecosystem is:", "Community of organisms", "Nothing", "Individual", "Separation", "A", "Ecosystem = community"),
        ("We should protect:", "All life", "Only humans", "Nothing", "Specific", "A", "Protect all life"),
        ("Nature's web is:", "Delicate", "Strong", "Nothing", "Breakable", "A", "Nature delicate"),
    ],
    "Man Ke Bhole Bhale Badal": [
        ("Man means:", "Mind or heart", "Body", "Brain only", "Eye", "A", "Man = mind/heart"),
        ("Bhole means:", "Simple or innocent", "Complex", "Clever", "Bad", "A", "Bhole = innocent"),
        ("Badal means:", "Clouds", "Rain", "Storm", "Nothing", "A", "Badal = clouds"),
        ("This poem shows innocence in:", "Mind", "Knowledge", "Work", "Action", "A", "Mind innocence"),
        ("Poem is about:", "Pure heart", "Complex", "Nothing", "Bad", "A", "Pure heart"),
    ],
    "Jaisa Sawal Waisa Jawab": [
        ("Jaisa Sawal means:", "As the question", "Random question", "No question", "Wrong question", "A", "As the question"),
        ("Jawab means:", "Answer", "Question", "Confusion", "Nothing", "A", "Jawab = answer"),
        ("This shows:", "Asking correctly", "Confusion", "Wrong", "Nothing", "A", "Question match answer"),
        ("We should ask:", "Properly", "Anything", "Random", "Nothing", "A", "Ask properly"),
        ("Right question gives:", "Right answer", "Confusion", "Nothing", "Wrong", "A", "Correct = correct"),
    ],
    "Kirmich Ki Gend": [
        ("Kirmich means:", "Red", "Blue", "Green", "Yellow", "A", "Kirmich = red"),
        ("Gend means:", "Ball", "Bat", "Net", "Stick", "A", "Gend = ball"),
        ("This is about:", "Red ball", "Game", "Nothing", "Story", "A", "Red ball game"),
        ("Playing games is:", "Good for health", "Waste", "Nothing", "Bad", "A", "Games = healthy"),
        ("This chapter is from:", "Hindi", "English", "Maths", "Science", "A", "Hindi chapter"),
    ],
    "Kirmich ki Gend": [
        ("Kirmich means red and Gend means:", "Ball", "Bat", "Net", "Stick", "A", "Red ball"),
        ("This chapter is about:", "Red ball", "Game", "Story", "Nothing", "A", "Chapter about red ball"),
        ("Playing is:", "Healthy", "Waste", "Bad", "Useless", "A", "Playing healthy"),
        ("We should play:", "Outdoor games", "Only video", "Nothing", "Avoid", "A", "Play outdoor"),
        ("Chapter is from:", "Hindi subject", "English", "Maths", "Science", "A", "Hindi subject"),
    ],
    "Pani Ke Dhabbe": [
        ("Pani means:", "Water", "Fire", "Air", "Earth", "A", "Pani = water"),
        ("Dhabbe means:", "Spots or stains", "Clean", "Fresh", "Nothing", "A", "Dhabbe = spots"),
        ("This is about:", "Water spots", "Nothing", "Clean water", "Pollution", "A", "Water spots"),
        ("Water spots are from:", "Dirty water", "Pure water", "Nothing", "Clean", "A", "Dirty water"),
        ("We should use:", "Clean water", "Dirty", "Polluted", "Waste", "A", "Use clean water"),
    ],
    "Ped": [
        ("Ped means:", "Tree", "Flower", "Fruit", "Leaf", "A", "Ped = tree"),
        ("Trees give us:", "Oxygen", "Carbon", "Smoke", "Pollution", "A", "Trees give oxygen"),
        ("We should plant:", "Trees", "Cut trees", "Burn", "Destroy", "A", "Plant trees"),
        ("Trees are:", "Important for life", "Useless", "Decoration", "Nothing", "A", "Trees important"),
        ("This chapter teaches:", "Value of trees", "Cut trees", "Ignore", "Nothing", "A", "Value of trees"),
    ],
    "Chakkar": [
        ("Chakkar means:", "Circle or round", "Square", "Line", "Angle", "A", "Chakkar = circle"),
        ("Chakkar can be:", "Round", "Square", "Straight", "Line", "A", "Chakkar round"),
        ("This is about:", "Circular movement", "Straight", "Nothing", "Linear", "A", "Round/circle"),
        ("Wheels make:", "Circular movement", "Straight", "No movement", "Linear", "A", "Wheel = round"),
        ("Chapter is about:", "Rotation", "Stationary", "Nothing", "Linear", "A", "Chakkar = circle"),
    ],
}


def generate_chapter_mcq(chapter_name):
    if chapter_name in chapter_questions:
        return chapter_questions[chapter_name][:5]
    
    lower_name = chapter_name.lower()
    
    topics = {
        "Maths": [
            (f"What is key in {chapter_name}?", "Practice", "Memorize", "Ignore", "Skip", "A", f"Practice {chapter_name}"),
            (f"{chapter_name} helps in:", "Math skills", "Nothing", "Confusion", "Memory", "A", f"{chapter_name} = math"),
            (f"Learn {chapter_name}:", "Apply formulas", "Guess", "Skip", "Memorize", "A", f"Apply for {chapter_name}"),
            (f"{chapter_name} uses:", "Numbers", "Words", "Pictures", "Nothing", "A", f"Numbers in {chapter_name}"),
            (f"This chapter is part of:", "Mathematics", "English", "Science", "History", "A", "Math topic"),
        ],
        "English": [
            (f"Reading {chapter_name}:", "Comprehension", "Memorize", "Ignore", "Skip", "A", f"Comprehend {chapter_name}"),
            (f"What does {chapter_name} teach?", "Values", "Words", "Nothing", "Fun", "A", f"Values from {chapter_name}"),
            (f"Lesson from {chapter_name}:", "Life skills", "Nothing", "Just fun", "Random", "A", f"Skills from {chapter_name}"),
            (f"We should learn:", "Good habits", "Bad habits", "Nothing", "Ignore", "A", f"Good from {chapter_name}"),
            (f"Chapter is:", "Story", "Poem", "Essay", "Drama", "A", "English reading"),
        ],
        "Hindi": [
            (f"कहानी {chapter_name}:", "कहानी है", "कुछ नहीं", "सब गलत", "कोई नहीं", "A", f"{chapter_name} कहानी है"),
            (f"{chapter_name} से सीखें:", "सीख", "भूलें", "नकारें", "उपेक्षा", "A", f"सीख {chapter_name} से"),
            (f"पाठ {chapter_name} में:", "शिक्षा", "कुछ नहीं", "मज़े", "उपदेश", "A", f"शिक्षा {chapter_name} में"),
            (f"हमें {chapter_name} से:", "सीखना चाहिए", "भूलना चाहिए", "नकारना चाहिए", "छोड़ना चाहिए", "A", f"सीख {chapter_name} से"),
            (f"इस अध्याय में:", "कहानी है", "कविता है", "निबंध है", "कुछ नहीं", "A", f"Story in {chapter_name}"),
        ],
        "EVS": [
            (f"What does {chapter_name} teach?", "Environment", "Nothing", "Science", "History", "A", f"Environment in {chapter_name}"),
            (f"This chapter is about:", "Nature and life", "City", "Buildings", "Machines", "A", f"Nature in {chapter_name}"),
            (f"We should protect:", "Nature", "Destroy", "Pollute", "Ignore", "A", f"Protect nature"),
            (f"Chapter {chapter_name}:", "Learning", "Nothing", "Fun", "Waste", "A", f"Learn from {chapter_name}"),
            (f"Our duty in {chapter_name}:", "Care for earth", "Damage", "Ignore", "Waste", "A", f"Duty = protect"),
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
print(f"Done! Generated {total} unique MCQs for Class 4")
print("="*60)