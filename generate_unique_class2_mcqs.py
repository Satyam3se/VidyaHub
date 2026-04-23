import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

print("=" * 60)
print("Generating Unique MCQs for Class 2 Chapters")
print("=" * 60)

grade = Grade.objects.get(slug='class-2')
chapters = list(Chapter.objects.filter(subject__grade=grade))

chapter_questions = {
    "What is Long, What is Round?": [
        ("Which shape is round?", "Circle", "Square", "Rectangle", "Triangle", "A", "Circle is round"),
        ("Which thing is long?", "Pencil", "Ball", "Book", "Eraser", "A", "Pencil is long"),
        ("Which is round like a ball?", "Orange", "Ruler", "Pen", "Notebook", "A", "Orange is round"),
        ("Long things have:", "More height", "No length", "Circle shape", "Square shape", "A", "Long things have more height"),
        ("Which is short?", "Eraser", "Ruler", "Pencil", "Stick", "A", "Eraser is short"),
    ],
    "The Basics": [
        ("What is basic learning?", "Foundation", "Advanced", "Impossible", "Boring", "A", "Basic is foundation"),
        ("We start with:", "Basics", "Hard things", "Impossible", "Nothing", "A", "Start with basics"),
        ("Learning basics helps in:", "Future learning", "Nothing", "Forgetting", "Confusion", "A", "Basics help future"),
        ("In school we first learn:", "Fundamentals", "Exam", "Grades", "Competition", "A", "First learn fundamentals"),
        ("Understanding basics is:", "Important", "Not needed", "Waste of time", "Difficult", "A", "Basics are important"),
    ],
    "First Day at School": [
        ("On first day we feel:", "Nervous and excited", "Angry", "Sad", "Tired", "A", "First day is nervous"),
        ("We should make ___ friends.", "New", "No", "Few", "Old", "A", "Make new friends"),
        ("School is for:", "Learning", "Playing only", "Sleeping", "Nothing", "A", "School is for learning"),
        ("Teacher is our:", "Guide", "Enemy", "Stranger", "Nobody", "A", "Teacher guides us"),
        ("We should ___ school.", "Enjoy", "Hate", "Avoid", "Fear", "A", "We should enjoy school"),
    ],
    "Counting in Groups": [
        ("Groups help in:", "Easy counting", "Hard counting", "Confusion", "Mistakes", "A", "Groups make counting easy"),
        ("2 groups of 5 = ?", "10", "7", "12", "15", "A", "2 x 5 = 10"),
        ("Counting in groups is also called:", "Multiplication", "Addition", "Subtraction", "Division", "A", "Groups = multiplication"),
        ("3 groups of 2 = ?", "6", "5", "8", "4", "A", "3 x 2 = 6"),
        ("How many in 4 groups of 3?", "12", "7", "15", "9", "A", "4 x 3 = 12"),
    ],
    "How Much Can You Carry?": [
        ("Weight is measured in:", "Kilograms", "Meters", "Liters", "Hours", "A", "Weight in kg"),
        ("Which is heavier?", "Elephant", "Cat", "Bird", "Mouse", "A", "Elephant is heaviest"),
        ("We carry things with:", "Hands", "Eyes", "Nose", "Ears", "A", "Carry with hands"),
        ("Which weighs more?", "1 kg iron", "1 kg cotton", "Both equal", "Cannot say", "C", "Both weigh same"),
        ("Heavy things are ___ to carry.", "Difficult", "Easy", "Impossible", "Fun", "A", "Heavy = difficult"),
    ],
    "Counting in Tens": [
        ("Counting in tens means:", "Skip by 10", "Count 1", "Count 2", "Random", "A", "Count by 10s"),
        ("10, 20, 30, __?", "40", "35", "45", "50", "A", "Next is 40"),
        ("5 tens = ?", "50", "5", "15", "25", "A", "5 x 10 = 50"),
        ("How many tens in 70?", "7", "70", "10", "17", "A", "70 has 7 tens"),
        ("70 + 20 = ?", "90", "50", "80", "100", "A", "70 + 20 = 90"),
    ],
    "Patterns": [
        ("Pattern means:", "Repeating sequence", "Random", "One time", "No rule", "A", "Pattern repeats"),
        ("A, B, A, B, A, __?", "B", "A", "C", "D", "A", "Alternates A,B"),
        ("2, 4, 2, 4, __?", "2", "4", "6", "8", "A", "Repeats 2,4"),
        ("What comes next: A, AA, AAA, ?", "AAAA", "A", "AA", "AAAAA", "A", "Adds one more A"),
        ("Red, Blue, Red, __?", "Blue", "Green", "Yellow", "Red", "A", "Alternates Red, Blue"),
    ],
    "Footprints": [
        ("Footprints show:", "Our size", "Our food", "Our height", "Our name", "A", "Footprints show size"),
        ("Big footprints mean:", "Big feet", "Small feet", "No feet", "No meaning", "A", "Big = big feet"),
        ("We can identify by:", "Footprints", "Face", "Voice", "Name", "A", "Identify by footprints"),
        ("Footprints are made by:", "Walking", "Sleeping", "Flying", "Swimming", "A", "Walk to make prints"),
        ("Whose footprint is bigger?", "Adult's", "Baby's", "No difference", "Cannot tell", "A", "Adult footprint bigger"),
    ],
    "I am Lucky!": [
        ("Feeling lucky means:", "Being grateful", "Being sad", "Being angry", "Being lazy", "A", "Lucky = grateful"),
        ("We should be ___ for what we have.", "Grateful", "Ungrateful", "Sad", "Angry", "A", "Be grateful"),
        ("Being lucky is a ___ feeling.", "Positive", "Negative", "Bad", "Sad", "A", "Positive feeling"),
        ("Lucky people ___ others.", "Help", "Hurt", "Ignore", "Fight", "A", "Lucky people help"),
        ("I am lucky because:", "I have family", "I have nothing", "I am alone", "I am sick", "A", "Having family = lucky"),
    ],
    "I Want": [
        ("Having wants is:", "Normal", "Bad", "Wrong", "Impossible", "A", "Having wants is normal"),
        ("We should work for:", "Our wants", "Nothing", "Others", "Random", "A", "Work for wants"),
        ("All wants may not be:", "Fulfilled", "Possible", "Good", "Achieved", "A", "Not all fulfilled"),
        ("Being patient helps:", "Get wants", "Get angry", "Be sad", "Quit", "A", "Patience helps"),
        ("Sometimes waiting is:", "Needed", "Bad", "Impossible", "Useless", "A", "Sometimes wait is needed"),
    ],
    "A Smile": [
        ("Smile shows:", "Happiness", "Anger", "Sadness", "Pain", "A", "Smile = happiness"),
        ("A smile can make others:", "Happy", "Sad", "Angry", "Tired", "A", "Smiles are contagious"),
        ("We should ___ smile.", "Often", "Never", "Rarely", "Only when forced", "A", "Smile often"),
        ("A smile costs:", "Nothing", "Money", "Effort", "Time", "A", "Smile is free"),
        ("Smile is a ___ gift.", "Free", "Expensive", "Rare", "Bought", "A", "Smile is free gift"),
    ],
    "My Family": [
        ("Who is in family?", "Parents, siblings", "Friends only", "Strangers", "Teachers only", "A", "Family = parents & siblings"),
        ("We should ___ our family.", "Love", "Ignore", "Fight", "Leave", "A", "Love family"),
        ("Family supports in:", "Hard times", "Only fun", "Never", "When angry", "A", "Family supports always"),
        ("We share with:", "Family", "Enemies", "Strangers", "No one", "A", "Share with family"),
        ("Family teaches us:", "Values", "Nothing", "Bad things", "Laziness", "A", "Family teaches values"),
    ],
    "Oont Chala": [
        ("Oont is animal:", "Camel", "Dog", "Cat", "Bird", "A", "Oont is camel"),
        ("Camel lives in:", "Desert", "Water", "Forest", "City", "A", "Camels live in desert"),
        ("Camel can travel:", "Long distances", "Nowhere", "Short only", "Only water", "A", "Camels travel far"),
        ("Camel stores ___ in hump.", "Fat", "Water", "Food", "Air", "A", "Hump stores fat"),
        ("Camel is also called:", "Ship of desert", "Fast runner", "Swimmer", "Flyer", "A", "Camel = ship of desert"),
    ],
    "Bhalu ne Kheli Football": [
        ("Bhalu is:", "Bear", "Dog", "Cat", "Bird", "A", "Bhalu is bear"),
        ("Bear played:", "Football", "Cricket", "Tennis", "Basketball", "A", "Bear played football"),
        ("Playing games is:", "Good for health", "Bad", "Waste of time", "Dangerous", "A", "Games are healthy"),
        ("We should play ___ games.", "Outdoor", "No", "Only indoor", "Never", "A", "Play outdoor games"),
        ("Football is played with:", "Feet", "Hands", "Head only", "Stick", "A", "Football uses feet"),
    ],
    "Myaun Myaun": [
        ("Myaun is sound of:", "Cat", "Dog", "Cow", "Bird", "A", "Myaun = cat sound"),
        ("Cat says:", "Meow!", "Woof!", "Moo!", "Quack!", "A", "Cat meows"),
        ("Cat is ___ animal.", "Pet", "Wild", "Farm", "Dangerous", "A", "Cat is pet"),
        ("Cat catches:", "Mice", "Dogs", "Cows", "Horses", "A", "Cat catches mice"),
        ("Cat sleeps in:", "Warm places", "Water", "Outside always", "Trees", "A", "Cat sleeps warm"),
    ],
    "Adhik Balwan Kaun": [
        ("Balwan means:", "Strong", "Weak", "Small", "Slow", "A", "Balwan = strong"),
        ("Who is stronger?", " Lion", "Cat", "Mouse", "Bird", "A", "Lion is strongest"),
        ("Strength comes from:", "Exercise", "Sleeping", "Eating junk", "Laziness", "A", "Exercise gives strength"),
        ("Being strong helps:", "Do work", "Be lazy", "Sleep", "Quit", "A", "Strong = can do work"),
        ("We should stay:", "Strong", "Weak", "Sick", "Tired", "A", "Stay strong"),
    ],
    "Dost ki Madad": [
        ("Dost means:", "Friend", "Enemy", "Stranger", "Teacher", "A", "Dost = friend"),
        ("We should help:", "Friends", "Only ourselves", "Enemies", "No one", "A", "Help friends"),
        ("Helping friends builds:", "Bond", "Fight", "Anger", "Sadness", "A", "Helping builds bond"),
        ("A true friend:", " Helps in need", "Leaves", "Mocks", "Hurts", "A", "True friend helps"),
        ("Friends should ___ each other.", "Support", "Fight", "Ignore", "Compete", "A", "Friends support"),
    ],
    "Tell Me Who": [
        ("We ask 'Who' for:", "People", "Numbers", "Places", "Things", "A", "Who asks about people"),
        ("Who is your teacher?", "Name of teacher", "Number", "Place", "Thing", "A", "Teacher is a person"),
        ("Who made this?", "Someone", "Something", "Somewhere", "Some time", "A", "Who = person"),
        ("Who answers about:", "People", "Numbers", "Animals", "All of these", "D", "Who asks any person"),
        ("Who question needs:", "Person name", "Number", "Color", "Size", "A", "Who needs person answer"),
    ],
    "The Tiger and the clever Rabbit": [
        ("Rabbit is known for:", "Cleverness", "Strength", "Speed", "Size", "A", "Rabbit is clever"),
        ("Tiger is:", "Strong", "Weak", "Small", "Slow", "A", "Tiger is strong"),
        ("Smart can beat:", "Strong", "By being clever", "By running", "By hiding", "B", "Clever beats strong"),
        ("Being smart is:", "Better than strong", "Worse than weak", "Not helpful", "Impossible", "A", "Smart beats strong"),
        ("We should be:", "Smart", "Reckless", "Careless", "Lazy", "A", "Be smart"),
    ],
    "Shapes and Patterns": [
        ("Which is a 3D shape?", "Cube", "Square", "Circle", "Line", "A", "Cube is 3D"),
        ("Square has ___ sides.", "4", "3", "5", "0", "A", "Square has 4 sides"),
        ("Triangle has:", "3 corners", "4 corners", "5 corners", "No corner", "A", "Triangle has 3 corners"),
        ("Pattern helps learn:", "Math", "Nothing", "Language", "Art", "A", "Patterns are math"),
        ("Circle is different from:", "Square", "Triangle", "All of these", "Line", "C", "Circle is different shape"),
    ],
    "Jodna seekhiye": [
        ("Jodna means:", "Addition", "Subtraction", "Division", "Multiplication", "A", "Jodna = addition"),
        ("2 + 3 = ?", "5", "4", "6", "7", "A", "2 + 3 = 5"),
        ("Addition helps find:", "Total", "Difference", "Quotient", "Product", "A", "Addition finds total"),
        ("Which is plus sign?", "+", "-", "x", "÷", "A", "Plus sign is +"),
        ("Find total of 4 and 2:", "6", "2", "8", "4", "A", "4 + 2 = 6"),
    ],
    "Ginti ki Pathshala": [
        ("Ginti means:", "Counting", "Writing", "Reading", "Speaking", "A", "Ginti = counting"),
        ("We learn counting at:", "School", "Park", "Market", "Home", "A", "Counting at school"),
        ("How many in 5 groups of 2?", "10", "7", "12", "8", "A", "5 x 2 = 10"),
        ("Counting helps in:", "Daily life", "Nothing", "Only exam", "Hardly", "A", "Counting used daily"),
        ("Practice makes:", "Perfect", "Bad", "Slow", "Difficult", "A", "Practice = perfect"),
    ],
    "Aam khaane ka sahi samay": [
        ("Aam should be eaten:", "In day", "At night", "Any time", "Never", "A", "Eat fruits in day"),
        ("Fruits give:", "Vitamins", "Only sugar", "Nothing", "Harm", "A", "Fruits give vitamins"),
        ("Raw mango in summer is:", "Common", "Rare", "Impossible", "Not available", "A", "Raw mango common summer"),
        ("Aam is ___ fruit.", "Seasonal", "Available year round", "Imported", "Processed", "A", "Mango is seasonal"),
        ("We should eat ___ Aam.", "Ripe", "Rotten", "Unwashed", "Too much", "A", "Eat ripe mango"),
    ],
    "My School": [
        ("School is for:", "Learning", "Playing only", "Sleeping", "Nothing", "A", "School = learning"),
        ("We learn from:", "Teachers", "No one", "Parents only", "Books only", "A", "Learn from teachers"),
        ("In school we make:", "Friends", "Enemies", "Nothing", "Bad habits", "A", "School makes friends"),
        ("School teaches:", "All subjects", "Nothing", "Only one", "Only sports", "A", "School teaches all"),
        ("We should ___ school.", "Attend regularly", "Skip", "Hate", "Leave", "A", "Attend school"),
    ],
    "Chhutey huee door": [
        ("Door opens and closes to let us:", "Enter and exit", "Sleep", "Play", "Eat", "A", "Door for entry/exit"),
        ("Door keeps us:", "Safe", "In danger", "Uncomfortable", "Hungry", "A", "Door keeps safe"),
        ("Door has:", "Handle", "No use", "Window", "Lock only", "A", "Door has handle"),
        ("We should ___ door properly.", "Close", "Break", "Leave open", "Ignore", "A", "Close door properly"),
        ("Without door:", "Not safe", "Safer", "More fun", "Better", "A", "Without door = not safe"),
    ],
    "Aam ki duniya": [
        ("Aam is famous:", "Indian fruit", "Foreign fruit", "Rare fruit", "Not real", "A", "Mango is Indian"),
        ("Alphonso is type of:", "Mango", "Apple", "Banana", "Grape", "A", "Alphonso mango"),
        ("Mango pulp has:", "Vitamins", "No nutrition", "Poison", "Only sugar", "A", "Mango has vitamins"),
        ("Mango tree is:", "Tall", "Small", "Herb", "Shrub", "A", "Mango tree tall"),
        ("Pick mango when:", "Yellow", "Green", "Red", "Black", "A", "Pick when yellow"),
    ],
    "Aam ko banana": [
        ("This is about:", "Making fruit salad", "Growing", "Cooking", "Baking", "A", "Making fruit salad"),
        ("We cut fruit with:", "Knife", "Fork", "Spoon", "Hands", "A", "Cut with knife"),
        ("Fruit should be ___ before cutting.", "Washed", "Dirty", "Rotten", "Unripe", "A", "Wash before cutting"),
        ("Cut fruit in:", "Small pieces", "Big chunks", "Juice form", "Paste", "A", "Cut in pieces"),
        ("Add ___ to make salad.", "All fruits", "Only one", "Vegetables", "Ice cream", "A", "Add various fruits"),
    ],
    "Pahli pankh": [
        ("Pankh means:", "Wing", "Leg", "Tail", "Beak", "A", "Pankh = wing"),
        ("Birds use wings to:", "Fly", "Swim", "Walk", "Eat", "A", "Wings for flying"),
        ("Baby birds learn to fly from:", "Parents", "Fish", "Animals", "Insects", "A", "Learn from parents"),
        ("First wing experience is:", "Important", "Not needed", "Dangerous", "Impossible", "A", "First experience matters"),
        ("We should ___ our first attempts.", "Not give up", "Give up", "Skip", "Fear", "A", "Don't give up"),
    ],
    "Khadang ko khadang": [
        ("Khadang is:", "Stick", "Feather", "Wing", "Tail", "A", "Khadang = stick"),
        ("With khadang we can:", "Play", "Eat", "Sleep", "Study", "A", "Stick for playing"),
        ("We play with ___ khadang.", "Different", "One type", "No", "Broken", "A", "Various sticks"),
        ("Playing makes us:", "Active", "Lazy", "Sleepy", "Weak", "A", "Play = active"),
        ("We can make khadang from:", "Wood", "Metal", "Plastic", "All of these", "D", "Various materials"),
    ],
    "Chalo chalo gaon": [
        ("Gaon means:", "Village", "City", "Town", "Forest", "A", "Gaon = village"),
        ("Village has:", "Less people", "More buildings", "More traffic", "Pollution", "A", "Village less crowded"),
        ("In village we find:", "Nature", "Factories", "Malls", "Traffic", "A", "Village has nature"),
        ("Village life is:", "Simple", "Complicated", "Fast", "Busy", "A", "Village life simple"),
        ("We should ___ village nature.", "Protect", "Destroy", "Ignore", "Pollute", "A", "Protect nature"),
    ],
    "Dhoop ki cheekh": [
        ("Dhoop is:", "Sunlight", "Rain", "Wind", "Cloud", "A", "Dhoop = sunlight"),
        ("Too much sun is:", "Harmful", "Good", "Helpful", "Necessary", "A", "Too much sun harmful"),
        ("We should avoid harsh:", "Sun", "Rain", "Wind", "Moon", "A", "Avoid harsh sun"),
        ("Dhoop gives us:", "Vitamin D", "Harm", "Both", "Nothing", "C", "Sun gives vitamin D but care needed"),
        ("Best time in sun is:", "Morning", "Midday", "Afternoon", "Evening", "A", "Morning sun best"),
    ],
    "Chhaya ki chaal": [
        ("Chhaya is:", "Shadow", "Light", "Sun", "Moon", "A", "Chhaya = shadow"),
        ("Shadow forms when:", "Light is blocked", "It rains", "It is night", "No reason", "A", "Shadow = blocked light"),
        ("Shadow changes with:", "Sun position", "Nothing", "Time", "Place", "A", "Shadow changes with sun"),
        ("At noon shadow is:", "Short", "Long", "No shadow", "Big", "A", "Noon shadow short"),
        ("Morning shadow falls:", "West", "East", "North", "South", "A", "Morning shadow to west"),
    ],
    "Chhoot! Chhoot!": [
        ("Chhoot means:", "Jump", "Run", "Walk", "Sleep", "A", "Chhoot = jump"),
        ("Rabbits are known for:", "Jumping", "Flying", "Swimming", "Crawling", "A", "Rabbits jump"),
        ("Where do rabbits live?", "Burrows", "Trees", "Water", "Caves", "A", "Rabbits in burrows"),
        ("Baby rabbits are called:", "Kits", "Puppies", "Kittens", "Cubs", "A", "Baby rabbits = kits"),
        ("Rabbits eat:", "Vegetables", "Meat", "Fish", "Insects", "A", "Rabbits are vegetarian"),
    ],
    "Khel ki dart": [
        ("Dart is:", "Sharp pointed toy", "Ball", "Bat", "Racket", "A", "Dart is sharp toy"),
        ("We play darts with:", "Aim and throw", "Run", "Jump", "Swim", "A", "Darts need aim"),
        ("Playing darts helps:", "Focus", "Sleep", "Eat", "Nothing", "A", "Darts improve focus"),
        ("We should play ___ while playing darts.", "Be careful", "Be careless", "Run", "Jump", "A", "Be careful while playing"),
        ("Darts is a ___ game.", "Skill", "Luck", "Chance", "Random", "A", "Darts is skill game"),
    ],
    "Machli jal ki rani": [
        ("Machli jal ki rani is:", "Fish", "Cat", "Dog", "Bird", "A", "Machli jal ki rani = fish"),
        ("Fish lives in:", "Water", "Land", "Air", "Trees", "A", "Fish in water"),
        ("Fish has ___ to swim.", "Fins", "Legs", "Wings", "Arms", "A", "Fish fins for swimming"),
        ("Fish breathe through:", "Gills", "Lungs", "Nose", "Mouth", "A", "Fish gills breathe"),
        ("We can learn ___ from fish.", "Swimming", "Flying", "Running", "Walking", "A", "Learn swimming from fish"),
    ],
    "Khel kaggle": [
        ("Kaggle is:", "Playground", "Room", "Water", "Tree", "A", "Kaggle = playground"),
        ("In kaggle we play:", "Outdoor games", "Video games", "Board games", "Computer games", "A", "Outdoor games in playground"),
        ("Playground should be:", "Clean", "Dirty", "Dangerous", "Broken", "A", "Playground clean"),
        ("We should ___ kaggle.", "Keep clean", "Litter", "Damage", "Ignore", "A", "Keep playground clean"),
        ("Games in kaggle make us:", "Active", "Lazy", "Sleepy", "Tired", "A", "Games keep active"),
    ],
    "Chalo school": [
        ("Chalo school means:", "Let's go to school", "Stay home", "Play", "Sleep", "A", "Chalo = Let's go"),
        ("We go to school to:", "Learn", "Play only", "Sleep", "Eat", "A", "School for learning"),
        ("In school we meet:", "Teachers and friends", "Strangers", "Enemies", "Nobody", "A", "Meet teachers friends"),
        ("School builds:", "Future", "Past", "Nothing", "Bad habits", "A", "School builds future"),
        ("We should ___ to school.", "Go", "Not go", "Late", "Skip", "A", "Go to school"),
    ],
    "My pet animal": [
        ("Pet animal is one we:", "Keep at home", "Hunt", "Fear", "Hurt", "A", "Pet = keep at home"),
        ("Examples of pets:", "Dog, cat, fish", "Tiger, lion", "Elephant, bear", "Snake, scorpion", "A", "Dog, cat are pets"),
        ("Pets need:", "Care and love", "Neglect", "Abuse", "Ignore", "A", "Pets need care"),
        ("Our pet depends on us for:", "Food", "Nothing", "Entertainment", "Their own", "A", "Pets depend on us"),
        ("We should be kind to ___ animals.", "All", "Only pets", "Wild", "None", "A", "Kind to all animals"),
    ],
    "Animal word": [
        ("Animal sound 'Woof' is from:", "Dog", "Cat", "Cow", "Bird", "A", "Woof = dog"),
        ("Cow says:", "Moo!", "Meow!", "Quack!", "Tweet!", "A", "Cow moos"),
        ("Duck says:", "Quack!", "Moo!", "Woof!", "Meow!", "A", "Duck quacks"),
        ("Lion roars!", "Yes", "No", "Sometimes", "Never", "A", "Lion roars"),
        ("Different animals make:", "Different sounds", "Same sound", "No sound", "All silent", "A", "Animals make different sounds"),
    ],
}


def generate_chapter_mcq(chapter_name):
    if chapter_name in chapter_questions:
        return chapter_questions[chapter_name][:5]
    
    lower_name = chapter_name.lower()
    
    topics = {
        "Maths": [
            (f"What is the total in {chapter_name}?", "Sum", "Difference", "Product", "Quotient", "A", f"Calculate total for {chapter_name}"),
            (f"Learn {chapter_name} concept:", "Practice", "Skip", "Ignore", "Memorize", "A", f"Practice {chapter_name}"),
            (f"{chapter_name} helps in:", "Calculations", "Nothing", "Forgetting", "Confusion", "A", f"{chapter_name} = useful concept"),
            (f"Important topic: {chapter_name}", "Yes", "No", "Maybe", "Not sure", "A", f"{chapter_name} is important"),
            (f"Master {chapter_name} by:", "Practice", "Reading", "Watching", "Nothing", "A", "Practice masters all"),
        ],
        "English": [
            (f"Read story: {chapter_name}", "Story", "Poem", "Essay", "Nothing", "A", f"Reading {chapter_name}"),
            (f"What happens in {chapter_name}?", "Story events", "Nothing", "Random", "Data", "A", f"Story events in {chapter_name}"),
            (f"Lesson from {chapter_name}:", "Values", "Nothing", "Only words", "Just entertainment", "A", f"Lesson: values from {chapter_name}"),
            (f"Characters in {chapter_name}:", "People in story", "No one", "Animals", "Objects", "A", f"Characters are in story"),
            (f"We should learn from {chapter_name}:", "Good habits", "Bad habits", "Nothing", "Rude behavior", "A", f"Learn good habits"),
        ],
        "Hindi": [
            (f"कहानी {chapter_name} में:", "कहानी है", "कुछ नहीं", "कोई नहीं", "सब गलत", "A", f"{chapter_name} एक कहानी है"),
            (f"{chapter_name} से सीखें:", "सीख", "भूलें", "उठाएं", "त्यागें", "A", f"सीख {chapter_name} से"),
            (f"पाठ {chapter_name} का:", "महत्व", "कोई नहीं", "कम", "अधिक", "A", f"महत्व {chapter_name} का"),
            (f"इस कहानी में:", "शिक्षा", "कुछ नहीं", "मज़े", "उपदेश", "A", f"शिक्षा {chapter_name} में"),
            (f"हमें {chapter_name} से:", "सीखना चाहिए", "नकारना चाहिए", "भूलना चाहिए", "डरना चाहिए", "A", f"सीख {chapter_name} से"),
        ],
        "EVS": [
            (f"What do we learn from {chapter_name}?", "Environment", "Nothing", "Science", "Math", "A", f"Learn about environment"),
            (f"About nature in {chapter_name}:", "Nature", "City", "Building", "Machine", "A", f"Nature in {chapter_name}"),
            (f"We should protect:", "Nature", "Destroy", "Waste", "Pollute", "A", f"Protect nature"),
            (f"Chapter {chapter_name} teaches:", "Care for earth", "Ignore earth", "Use more", "Waste resources", "A", f"Care for earth"),
            (f"Our duty towards {chapter_name}:", "Protect", "Damage", "Ignore", "Waste", "A", f"Protect environment"),
        ],
    }
    
    for subject_key, qs in topics.items():
        if subject_key.lower() in lower_name:
            return qs
    
    return topics["Maths"][:5]


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
print(f"Done! Generated {total} unique MCQs for Class 2")
print("="*60)