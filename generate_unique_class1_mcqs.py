import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion
import random

print("=" * 60)
print("Generating Truly Unique MCQs for Each Class 1 Chapter")
print("=" * 60)

grade = Grade.objects.get(slug='class-1')
chapters = list(Chapter.objects.filter(subject__grade=grade))

chapter_questions = {
    'Shapes and Space': [
        ("Which shape has 3 sides?", "Triangle", "Square", "Circle", "Rectangle", "A", "Triangle has 3 sides"),
        ("A circle has how many corners?", "0", "1", "2", "3", "A", "Circle has no corners"),
        ("Which shape has 4 equal sides?", "Square", "Triangle", "Circle", "Rectangle", "A", "Square has 4 equal sides"),
        ("Which shape looks like a ball?", "Circle", "Square", "Triangle", "Box", "A", "Ball is like a circle"),
        ("A rectangle has ___ corners.", "4", "3", "5", "0", "A", "Rectangle has 4 corners"),
    ],
    'The Basics': [
        ("What comes after A?", "B", "C", "D", "Z", "A", "B comes after A"),
        ("How many letters in alphabet?", "26", "24", "25", "23", "A", "English has 26 letters"),
        ("Which is a vowel?", "A", "B", "C", "D", "A", "A is a vowel"),
        ("Capital letter is also called:", "Uppercase", "Small", "Number", "Sound", "A", "Capital = Uppercase"),
        ("Small letter is also called:", "Lowercase", "Big", "Capital", "Number", "A", "Small = Lowercase"),
    ],
    'Numbers from One to Nine': [
        ("What comes before 5?", "4", "3", "6", "2", "A", "4 comes before 5"),
        ("How many fingers on one hand?", "5", "4", "6", "10", "A", "One hand has 5 fingers"),
        ("Which number is between 3 and 5?", "4", "2", "6", "7", "A", "4 is between 3 and 5"),
        ("What is the biggest number from 1 to 9?", "9", "1", "3", "4", "A", "9 is the biggest"),
        ("Count: 1, 2, 3, __?", "4", "5", "2", "0", "A", "Next is 4"),
    ],
    'Addition': [
        ("What is 2 + 3?", "5", "4", "6", "7", "A", "2 + 3 = 5"),
        ("Add 1 + 4:", "5", "4", "6", "3", "A", "1 + 4 = 5"),
        ("What is 3 + 2?", "5", "4", "6", "3", "A", "3 + 2 = 5"),
        ("Find sum: 4 + 1 = ?", "5", "3", "4", "6", "A", "4 + 1 = 5"),
        ("1 more than 4 is:", "5", "3", "4", "6", "A", "4 + 1 = 5"),
    ],
    'Subtraction': [
        ("What is 5 - 2?", "3", "2", "4", "5", "A", "5 - 2 = 3"),
        ("Take away 1 from 4:", "3", "2", "4", "5", "A", "4 - 1 = 3"),
        ("What is 3 minus 1?", "2", "1", "3", "4", "A", "3 - 1 = 2"),
        ("5 less 2 equals:", "3", "2", "4", "5", "A", "5 - 2 = 3"),
        ("Subtract: 4 - 3 = ?", "1", "2", "3", "0", "A", "4 - 3 = 1"),
    ],
    'Numbers from Ten to Twenty': [
        ("How many in one dozen?", "12", "10", "14", "11", "A", "One dozen = 12"),
        ("Write ten in numbers:", "10", "1", "100", "01", "A", "Ten = 10"),
        ("What comes before 12?", "11", "10", "13", "9", "A", "11 comes before 12"),
        ("What is 10 + 5?", "15", "10", "20", "5", "A", "10 + 5 = 15"),
        ("How many digits in 15?", "2", "1", "3", "0", "A", "15 has 2 digits"),
    ],
    'Time': [
        ("How many minutes in one hour?", "60", "30", "100", "50", "A", "One hour = 60 min"),
        ("What time is 3 o'clock?", "3:00", "3:30", "2:00", "4:00", "A", "3 o'clock is 3:00"),
        ("Days in a week:", "7", "5", "6", "8", "A", "A week has 7 days"),
        ("Months in a year:", "12", "10", "11", "13", "A", "A year has 12 months"),
        ("Morning comes ___ evening.", "Before", "After", "With", "Without", "A", "Morning comes first"),
    ],
    'Measurement': [
        ("What is used to measure length?", "Ruler", "Bucket", "Watch", "Scale", "A", "Ruler measures length"),
        ("1 meter = ___ centimeters?", "100", "10", "1000", "50", "A", "1 m = 100 cm"),
        ("What is weight measured in?", "Kilogram", "Meter", "Liter", "Hour", "A", "Weight is in kg"),
        ("Which is heavier: 1 kg cotton or 1 kg iron?", "Both equal", "Cotton", "Iron", "Cannot say", "A", "Both weigh 1 kg"),
        ("Which is for measuring liquid?", "Liter", "Kilogram", "Meter", "Hour", "A", "Liquid measured in liters"),
    ],
    'Numbers from Twenty-one to Fifty': [
        ("What comes after 29?", "30", "28", "31", "40", "A", "30 comes after 29"),
        ("30 + 10 = ?", "40", "30", "50", "20", "A", "30 + 10 = 40"),
        ("The biggest 2-digit number is:", "99", "100", "9", "50", "A", "99 is biggest 2-digit"),
        ("Write 45 in words:", "Forty-five", "Four five", "Fourty-five", "Four-five", "A", "45 is Forty-five"),
        ("How many tens in 50?", "5", "50", "0", "10", "A", "50 has 5 tens"),
    ],
    'Data Handling': [
        ("Which shows data in pictures?", "Pictograph", "Number", "Letter", "Word", "A", "Pictograph uses pictures"),
        ("Tally marks help to:", "Count", "Write", "Draw", "Sing", "A", "Tally counts items"),
        ("Bar graph uses:", "Bars", "Circles", "Triangles", "Lines", "A", "Bar graph has bars"),
        ("We use graph to show:", "Information", "Music", "Stories", "Games", "A", "Graphs show information"),
        ("More children means ___ taller bar.", "Taller", "Shorter", "No change", "Curved", "A", "More = taller bar"),
    ],
    'Patterns': [
        ("What comes next: 2, 4, 6, ?", "8", "7", "9", "10", "A", "Even numbers: +2"),
        ("What pattern is 5, 10, 15, ?", "20", "18", "25", "16", "A", "Table of 5"),
        ("A red, blue, red, blue pattern is:", "ABAB", "AAAA", "BBBB", "AABB", "A", "Red-Blue repeats"),
        ("What comes next: A, B, C, ?", "D", "A", "Z", "E", "A", "Alphabet order"),
        ("Pattern means:", "Repeating thing", "Random thing", "Only one", "No rule", "A", "Pattern repeats"),
    ],
    'Numbers': [
        ("Write 100 in words:", "One hundred", "Ten", "One thousand", "Ten hundred", "A", "100 is One hundred"),
        ("What is 50 + 50?", "100", "150", "50", "200", "A", "50 + 50 = 100"),
        ("Which is biggest 3-digit number?", "999", "100", "99", "900", "A", "999 is biggest"),
        ("Write 500 in expanded form:", "500 + 0 + 0", "50 + 0", "5 + 0 + 0", "5000", "A", "500 = 5 hundreds"),
        ("1 thousand = ___ hundreds.", "10", "100", "1", "1000", "A", "1000 = 10 hundreds"),
    ],
    'Money': [
        ("How many paise in Rs. 5?", "500", "5", "50", "1000", "A", "1 Rupee = 100 paise"),
        ("What is cost of 2 pens at Rs. 5?", "Rs. 10", "Rs. 7", "Rs. 5", "Rs. 15", "A", "2 x 5 = 10"),
        ("You have Rs. 20. Pen costs Rs. 10. Money left?", "Rs. 10", "Rs. 30", "Rs. 0", "Rs. 20", "A", "20 - 10 = 10"),
        ("Rs. 10 note is also called:", "Ten rupees", "Five rupees", "Twenty rupees", "One rupee", "A", "Rs. 10 note"),
        ("Coins are ___ than notes.", "Smaller", "Bigger", "Same", "Heavier", "A", "Coins are smaller"),
    ],
    'How Many': [
        ("Count the apples: 🍎🍎🍎 How many?", "3", "2", "4", "5", "A", "3 apples"),
        ("How many tens in 30?", "3", "30", "0", "10", "A", "30 has 3 tens"),
        ("Write number for nine:", "9", "6", "10", "12", "A", "9 is nine"),
        ("What is 7 + 3?", "10", "7", "3", "17", "A", "7 + 3 = 10"),
        ("How many zeros in 100?", "2", "1", "3", "0", "A", "100 has 2 zeros"),
    ],
    'A Happy Child': [
        ("A happy child:", "Smiles", "Cries", "Sleeps", "Fights", "A", "Happy child smiles"),
        ("What makes children happy?", "Friends and toys", "Being alone", "Crying", "Fighting", "A", "Friends make us happy"),
        ("A happy child says:", "Hello!", "Go away!", "No!", "Bad!", "A", "Happy child greets"),
        ("We should be:", "Kind", "Rude", "Angry", "Selfish", "A", "We should be kind"),
        ("A happy child likes to:", "Play", "Cry", "Fight", "Complain", "A", "Happy child plays"),
    ],
    'Three Little Pigs': [
        ("Three Little Pigs built houses with:", "Straw, sticks, bricks", "Paper", "Cloth", "Leaves", "A", "They used different materials"),
        ("Which house was strongest?", "Brick house", "Straw house", "Stick house", "Paper house", "A", "Brick house was strong"),
        ("The wolf wanted to:", "Eat the pigs", "Play", " Help", "Sleep", "A", "Wolf wanted to eat them"),
        ("Who helped the pigs?", "No one", "Wolf", "Mother", "Farmer", "A", "They helped themselves"),
        ("Lesson from story:", "Work hard", "Be lazy", "Cheat", "Run away", "A", "Hard work pays"),
    ],
    'After a Bath': [
        ("We should take bath:", "Daily", "Once a week", "Once a month", "Never", "A", "Daily bath is good"),
        ("Bath makes us:", "Clean", "Dirty", "Tired", "Hungry", "A", "Bath makes us clean"),
        ("After bath we feel:", "Fresh", "Sleepy", "Tired", "Dirty", "A", "After bath we feel fresh"),
        ("Water is needed for:", "Bath", "Eating", "Sleeping", "Walking", "A", "Bath needs water"),
        ("Clean body means:", "Healthy", "Sick", "Tired", "Weak", "A", "Clean = Healthy"),
    ],
    'The Bubble, the Straw and the Shoe': [
        ("Bubble is filled with:", "Air", "Water", "Sand", "Fire", "A", "Bubbles have air"),
        ("Straw is used to:", "Drink", "Walk", "Write", "Cut", "A", "Straw helps drink"),
        ("Shoe protects:", "Feet", "Hands", "Head", "Eyes", "A", "Shoe protects feet"),
        ("We wear shoes on:", "Feet", "Head", "Hands", "Back", "A", "Shoes go on feet"),
        ("Things that float have:", "Air inside", "Heavy", "No use", "Water", "A", "Air makes things float"),
    ],
    'One Little Kitten': [
        ("Kitten is baby of:", "Cat", "Dog", "Cow", "Bird", "A", "Kitten is baby cat"),
        ("Kitten says:", "Meow!", "Woof!", "Moo!", "Quack!", "A", "Kitten meows"),
        ("Baby of dog is called:", "Puppy", "Kitten", "Calf", "Joey", "A", "Puppy is baby dog"),
        ("Pet animals need:", "Care", "Nothing", "To roam", "To fight", "A", "Pets need care"),
        ("We should be kind to:", "Animals", "Enemies", "Strangers", "Nobody", "A", "Be kind to animals"),
    ],
    'Lalu and Peelu': [
        ("Birds have:", "Feathers", "Scales", "Fur", "Hair", "A", "Birds have feathers"),
        ("Birds can:", "Fly", "Swim only", "Run only", "Jump", "A", "Birds can fly"),
        ("Baby of bird is called:", "Chick", "Puppy", "Kitten", "Calf", "A", "Baby bird is chick"),
        ("Birds make nests in:", "Trees", "Houses", "Water", "Underground", "A", "Nests are in trees"),
        ("What do birds eat?", "Seeds and worms", "Only leaves", "Only water", "Rocks", "A", "Birds eat various things"),
    ],
    'Once I Saw a Little Bird': [
        ("A little bird:", "Sings", "Talks", "Runs", "Swims", "A", "Birds sing"),
        ("Where did the bird sit?", "On the wall", "In water", "Under ground", "In fire", "A", "Bird sat on wall"),
        ("Bird flew away because:", "It was scared", "It was hungry", "It was sleepy", "It was tired", "A", "Bird flew from fear"),
        ("We should watch birds:", "Quietly", "Loudly", "Running", "Chasing", "A", "Watch quietly"),
        ("Birds are:", "Beautiful", "Scary", "Ugly", "Dangerous", "A", "Birds are beautiful"),
    ],
    'Mittu and the Yellow Mango': [
        ("Mango is:", "Fruit", "Vegetable", "Flower", "Leaf", "A", "Mango is fruit"),
        ("Ripe mango is:", "Yellow", "Green", "Red", "Blue", "A", "Ripe mango is yellow"),
        ("Monkey ate:", "Mango", "Leaf", "Root", "Stone", "A", "Monkey ate mango"),
        ("Monkeys live in:", "Trees", "Water", "Houses", "Underground", "A", "Monkeys live in trees"),
        ("Mango is:", "Sweet", "Salty", "Bitter", "Sour", "A", "Mango is sweet"),
    ],
    'Merry-Go-Round': [
        ("Merry-go-round moves:", "Round and round", "Up and down", "Side to side", "Back and forth", "A", "It moves round"),
        ("We sit on ___ merry-go-round.", "Horses", "Dogs", "Cats", "Birds", "A", "We ride horses"),
        ("At fair we can go on:", "Rides", "Study", "Sleep", "Work", "A", "Fair has rides"),
        ("Merry-go-round is also called:", "Carousel", "Train", "Bus", "Plane", "A", "It is carousel"),
        ("While moving we feel:", "Happy", "Sad", "Tired", "Angry", "A", "Moving is fun"),
    ],
    'Circle': [
        ("Circle shape has ___ sides.", "No straight", "4", "3", "Many", "A", "Circle has no straight sides"),
        ("Sun looks like:", "Circle", "Square", "Triangle", "Line", "A", "Sun is round"),
        ("Full moon looks like:", "Circle", "Square", "Triangle", "Rectangle", "A", "Moon is round"),
        ("Circle is also called:", "Round", "Square", "Box", "Flat", "A", "Circle is round"),
        ("Like a circle are:", "Ball, plate, coin", "Book, desk, box", "Door, window, table", "Chair, bed, stool", "A", "Round things"),
    ],
    'If I Were an Apple': [
        ("If I were an apple I would be:", "Red or green", "Blue", "Purple", "Black", "A", "Apples are red/green"),
        ("An apple grows on:", "Tree", "Ground", "Bush", "Water", "A", "Apples grow on trees"),
        ("Apple has ___ inside.", "Seeds", "Bones", "Feathers", "Hair", "A", "Apples have seeds"),
        ("We should eat:", "Fruits", "Only chips", "Only sweets", "Junk food", "A", "Fruits are healthy"),
        ("Apple is ___ fruit.", "A", "B", "C", "D", "A", "Apple is an article"),
    ],
    'Our Tree': [
        ("Trees give us:", "Oxygen", "Smoke", "Dust", "Heat", "A", "Trees give oxygen"),
        ("Birds make nests in:", "Trees", "Houses", "Cars", "Planes", "A", "Nests in trees"),
        ("Roots are ___ ground.", "Under", "Above", "In water", "In air", "A", "Roots are underground"),
        ("Trees need:", "Water and sun", "Only sun", "Only water", "No light", "A", "Trees need both"),
        ("Cutting trees causes:", "Less oxygen", "More oxygen", "More rain", "Clean air", "A", "Cutting trees harms"),
    ],
    'A Kite': [
        ("Kite flies in:", "Sky", "Water", "Ground", "Underground", "A", "Kites fly in sky"),
        ("Kite is held by:", "String", "Chain", "Rope", "Stick", "A", "Kite is held by string"),
        ("Kite moves with:", "Wind", "Rain", "Snow", "Heat", "A", "Wind makes kite fly"),
        ("Kite shape is usually:", "Diamond", "Square", "Circle", "Line", "A", "Kite is diamond shaped"),
        ("We fly kites on:", "Windy days", "Rainy days", "Snowy days", "Calm days", "A", "Wind needed"),
    ],
    'Sundari': [
        ("Sundari is a:", "Character in story", "Flower", "Animal", "Bird", "A", "Sundari is a character"),
        ("The story teaches us:", "Good behavior", "Being lazy", "Fighting", "Being rude", "A", "Story teaches good"),
        ("We should speak:", "Politely", "Rudely", "Loudly", "Badly", "A", "Speak politely"),
        ("Being good means:", "Helping others", "Harming", "Ignoring", "Fighting", "A", "Good means helping"),
        ("Stories teach us:", "Lessons", "Nothing", "Only words", "Just for fun", "A", "Stories teach lessons"),
    ],
    'A Little Turtle': [
        ("Turtle lives in:", "Water and land", "Only water", "Only land", "Air", "A", "Turtle is amphibious"),
        ("Turtle has:", "Shell", "Feathers", "Wings", "Fur", "A", "Turtle has shell"),
        ("Turtle moves:", "Slowly", "Fast", "Running", "Flying", "A", "Turtles move slowly"),
        ("Baby of turtle is called:", "Hatchling", "Puppy", "Kitten", "Cub", "A", "Baby turtle"),
        ("Shell protects turtle from:", "Danger", "Food", "Water", "Sleep", "A", "Shell is protection"),
    ],
    'The Tiger and the Mosquito': [
        ("Mosquito bites:", "Causes itching", "Nothing", "Good", "Pleasant", "A", "Mosquito bites itch"),
        ("Tiger is:", "Strong and bold", "Weak", "Small", "Slow", "A", "Tiger is strong"),
        ("Even small creature has:", "Power", "No use", "No strength", "Weakness", "A", "Everyone has power"),
        ("Small insect can be:", "Annoying", "Pleasant", "Helpful only", "Useless", "A", "Insects can annoy"),
        ("Every creature has:", "Importance", "No use", "Just for fun", "Nothing", "A", "All creatures matter"),
    ],
    'Clouds': [
        ("Clouds are in:", "Sky", "Water", "Ground", "Underground", "A", "Clouds are in sky"),
        ("Clouds have:", "Water drops", "Fire", "Rocks", "Sand", "A", "Clouds have water"),
        ("When clouds are dark it means:", "Rain coming", "Sun coming", "Nothing", "Clear sky", "A", "Dark clouds = rain"),
        ("Clouds float because:", "Air holds them", "They are light", "Magic", "Wings", "A", "Air holds clouds"),
        ("Clouds look like:", "Cotton, animals, ships", "Only circles", "Only squares", "Just white", "A", "Clouds have shapes"),
    ],
    "Anandi's Rainbow": [
        ("Rainbow has ___ colors.", "7", "5", "6", "8", "A", "Rainbow has 7 colors"),
        ("Rainbow appears after:", "Rain", "Snow", "Storm", "Clear sky", "A", "Rainbow after rain"),
        ("Rainbow is:", "In the sky", "On ground", "In water", "Underground", "A", "Rainbow is in sky"),
        ("Color Red is:", "At top or bottom", "Middle", "Everywhere", "Nowhere", "A", "Red is at edge"),
        ("We see rainbow when:", "Sun and rain together", "No sun", "Only rain", "Only sun", "A", "Need both sun and rain"),
    ],
    'Flying-Man': [
        ("Story about Flying-Man is:", "Fiction", "True", "Real", "Fact", "A", "It is fiction/fantasy"),
        ("Flying in dreams is:", "Possible", "Never happens", "Scary", "True", "A", "Dreams can fly"),
        ("We should be:", "Creative", "Serious", "Boring", "Realistic only", "A", "Be creative"),
        ("Stories take us to:", "Imagination", "Reality", "Nowhere", "School", "A", "Stories fuel imagination"),
        ("Fiction stories are:", "Entertaining", "True", "Boring", "Real", "A", "Fiction entertains"),
    ],
    'The Tailor and his Friend': [
        ("Tailor makes:", "Clothes", "Food", "Houses", "Cars", "A", "Tailor makes clothes"),
        ("Needle is used to:", "Sew", "Cut", "Measure", "Draw", "A", "Needle sews"),
        ("Tailor uses:", "Thread", "Chain", "Rope", "Wire", "A", "Tailor uses thread"),
        ("Good friend:", "Helps in need", "Only plays", "Leaves alone", "Mocks", "A", "Good friend helps"),
        ("We should help:", "Friends", "Enemies", "Strangers", "Nobody", "A", "Help our friends"),
    ],
    'Jhoola': [
        ("What is झूला?", "Swing", "Tree", "House", "Bed", "A", "झूला is swing"),
        ("Children enjoy:", "Swinging", "Running", "Sleeping", "Studying", "A", "Children enjoy swinging"),
        ("Swing moves ___ and ___.", "To and fro", "Up only", "Down only", "Sideways", "A", "Swing moves to and fro"),
        ("Best place for swing is:", "Tree branch", "Roof", "Ground", "Wall", "A", "Swing hangs from tree"),
        ("झूला is fun for:", "Children", "Only adults", "Animals", "Birds", "A", "Children enjoy swings"),
    ],
    'Aam ki Kahani': [
        ("आम is what?", "Fruit", "Vegetable", "Flower", "Leaf", "A", "आम is mango"),
        ("Mango grows on:", "Tree", "Ground", "Bush", "Water", "A", "Mango grows on tree"),
        ("Green mango becomes:", "Yellow", "Red", "Blue", "Black", "A", "Green mango turns yellow"),
        ("Mango taste is:", "Sweet", "Salty", "Sour", "Bitter", "A", "Mango is sweet"),
        ("We should eat:", "Seasonal fruits", "Junk food", "Chips", "Chocolates", "A", "Eat seasonal fruits"),
    ],
    'Aam ki Tokari': [
        ("टोकरी is:", "Basket", "Bag", "Box", "Plate", "A", "टोकरी is basket"),
        ("Mangoes are kept in:", "Basket", "Water", "Fire", "Air", "A", "Mangoes in basket"),
        ("We carry things in:", "Basket", "Nothing", "Hands only", "Pocket", "A", "Use basket to carry"),
        ("Basket is made of:", "Straw", "Iron", "Plastic", "Glass", "A", "Baskets often of straw/cane"),
        ("आम का टोकरा means:", "Basket of mangoes", "Mango tree", "Mango leaf", "Mango seed", "A", "Container of mangoes"),
    ],
    'Patte hi Patte': [
        ("पत्ते are found on:", "Plants and trees", "Ground", "Water", "Rocks", "A", "पत्ते on plants"),
        ("Leaves are usually:", "Green", "Red", "Blue", "Black", "A", "Leaves are green"),
        ("Plants need leaves to:", "Make food", "Grow roots", "Make flowers", "Bear fruit only", "A", "Leaves make food"),
        ("When leaves fall:", "New ones grow", "Nothing", "Plant dies", "No change", "A", "New leaves grow"),
        ("पत्ते means:", "Leaves", "Roots", "Flowers", "Seeds", "A", "पत्ते are leaves"),
    ],
    'Pakodi': [
        ("पकोड़ा is:", "Snack", "Drink", "Fruit", "Vegetable", "A", "पकोड़ा is a snack"),
        ("Pakodi is made from:", "Gram flour", "Rice", "Wheat", "Sugar", "A", "Pakodi of gram flour"),
        ("Pakodi is:", "Fried", "Boiled", "Raw", "Steamed", "A", "Pakodi is fried"),
        ("We eat pakodi with:", "Chutney", "Milk", "Water", "Soup", "A", "Chutney goes with pakodi"),
        ("पकोड़ा is famous:", "Indian snack", "Foreign food", "Drink", "Sweet", "A", "It is Indian snack"),
    ],
    'Chhuk-Chhuk Gadi': [
        ("What makes चूक-चूक sound?", "Train", "Car", "Bus", "Bike", "A", "Train makes chuk-chuk"),
        ("Train runs on:", "Tracks", "Road", "Water", "Air", "A", "Train on tracks"),
        ("Train carries:", "Many people", "One person", "No one", "Only goods", "A", "Train carries many"),
        ("Train has:", "Many coaches", "One coach", "No coach", "Wheels only", "A", "Train has many coaches"),
        ("We travel by train for:", "Long distance", "Only short", "No travel", "Nearby", "A", "Train for long distances"),
    ],
    'Rasoi Ghar': [
        ("रसोई is:", "Kitchen", "Bedroom", "Garden", "Bathroom", "A", "रसोई is kitchen"),
        ("In kitchen we:", "Cook food", "Sleep", "Study", "Play", "A", "Cook in kitchen"),
        ("Who cooks food?", "Mother or father", "Stranger", "Doctor", "Teacher", "A", "Parents cook"),
        ("Kitchen has:", "Stove and utensils", "Bed", "Books", "Toys", "A", "Kitchen has cooking things"),
        ("Food is cooked in:", "Kitchen", "Garden", "Bedroom", "Bathroom", "A", "Food cooked in kitchen"),
    ],
    'Chuho! Myau So Rahi Hai': [
        ("बिल्ली Sleeps says:", "Meow!", "Woof!", "Moo!", "Quack!", "A", "Cat says meow"),
        ("Cat sleeps in:", "Various places", "Water", "Outside always", "Trees only", "A", "Cat sleeps anywhere"),
        ("Kitten is baby of:", "Cat", "Dog", "Bird", "Cow", "A", "Kitten = baby cat"),
        ("Cat catches:", "Mice", "Dogs", "Cows", "Horses", "A", "Cats catch mice"),
        ("Cat is:", "Pet animal", "Wild animal", "Bird", "Fish", "A", "Cat can be pet"),
    ],
    'Makdi-Kakdi-Lakdi': [
        ("Spider in Hindi is:", "Makdi", "Kakdi", "Lakdi", "Bhadwa", "A", "Makdi is spider"),
        ("Spider makes:", "Web", "Nest", "House", "Burrow", "A", "Spider makes web"),
        ("Web is for:", "Catching insects", "Sleeping", "Living", "Playing", "A", "Web catches food"),
        ("Spider has ___ legs.", "8", "4", "6", "2", "A", "Spider has 8 legs"),
        ("Web is made of:", "Thread", "Paper", "Cloth", "Wood", "A", "Web is silk thread"),
    ],
    'Pugdi': [
        ("पुगडी is:", "Shoes", "Hat", "Shirt", "Bag", "A", "पुगडी is shoes"),
        ("We wear shoes on:", "Feet", "Head", "Hands", "Back", "A", "Shoes on feet"),
        ("Shoes protect:", "Feet", "Head", "Hands", "Eyes", "A", "Shoes protect feet"),
        ("Shoes have:", "Soles", "Wings", "Feathers", "Lights", "A", "Shoes have soles"),
        ("In winter shoes keep feet:", "Warm", "Cold", "Wet", "Dirty", "A", "Shoes keep warm"),
    ],
    'Patang': [
        ("पतंग is:", "Kite", "Flag", "Banner", "Poster", "A", "पतंग is kite"),
        ("Kite flies in:", "Sky", "Water", "Ground", "Underground", "A", "Kites fly in sky"),
        ("Kite is held by:", "String", "Chain", "Rope", "Stick", "A", "Kite by string"),
        ("Kite needs:", "Wind", "Rain", "Snow", "Storm", "A", "Wind makes kite fly"),
        ("Kite is made of:", "Paper", "Iron", "Cloth", "Plastic", "A", "Kite is paper"),
    ],
    'Gend-Balla': [
        ("गेंद-बल्ला is:", "Ball and bat", "Ball only", "Bat only", "Net", "A", "Ball and bat"),
        ("Ball is for:", "Playing", "Eating", "Studying", "Sleeping", "A", "Ball is for playing"),
        ("With ball we can:", "Play many games", "Study", "Cook", "Clean", "A", "Ball enables games"),
        ("Game keeps us:", "Healthy", "Sick", "Tired", "Weak", "A", "Games keep healthy"),
        ("बल्ला hits:", "Ball", "Person", "Tree", "House", "A", "Bat hits ball"),
    ],
    'Bandar Gaya Khet Me Bhag': [
        ("बंदर monkey went to:", "Farm field", "House", "Water", "Market", "A", "Went to farm field"),
        ("Monkey ate:", "Crops", "Rocks", "Leaves only", "Nothing", "A", "Ate farmer's crops"),
        ("Farmer got:", "Angry", "Happy", "Excited", "Nothing", "A", "Farmer got angry"),
        ("Lesson: Don't ___ crops.", "Destroy", "Grow", "Water", "Protect", "A", "Don't destroy crops"),
        ("Monkey should find:", "Food in forest", "Farmer's field", "House", "Garden", "A", "Find food naturally"),
    ],
    'Ek Budhiya': [
        ("एक बूढीया is:", "Old woman", "Young girl", "Child", "Man", "A", "एक बूढीया is old woman"),
        ("She lived:", "Alone", "With family", "In palace", "In forest", "A", "She lived alone"),
        ("She could:", "Think wisely", "Play", "Run", "Fight", "A", "Old woman wise"),
        ("With smart thinking she:", "Solved problem", "Made trouble", "Got lost", "Got sick", "A", "She solved problem"),
        ("Wisdom comes with:", "Age", "Youth", "Strength", "Speed", "A", "Wisdom from age"),
    ],
    'Main Bhi': [
        ("मैं भी means:", "Me too", "Go away", "Be quiet", "Come here", "A", "मैं भी = Me too"),
        ("When someone says 'Me too' they:", "Agree", "Disagree", "Refuse", "Leave", "A", "'Me too' shows agreement"),
        ("This phrase shows:", "Participation", "Refusal", "Anger", "Sadness", "A", "Shows participation"),
        ("I can do it ___ you.", "Like", "Unlike", "Without", "Before", "A", "Like you"),
        ("Everyone can say:", "Main Bhi", "Main Nahi", "Main Accha", "Main Kharab", "A", "Can say 'Me too'"),
    ],
    'Lalu Aur Peelu': [
        ("लालू और पीलू are:", "Two birds", "Two dogs", "Two cats", "Two animals", "A", "लालू और पीलू are birds"),
        ("They are:", "Parrots", "Sparrows", "Crow", "Peacock", "A", "They are parrots"),
        ("Birds have:", "Feathers", "Scales", "Fur", "Hair", "A", "Birds have feathers"),
        ("These birds were:", "In garden", "In water", "Underground", "In house", "A", "They were in garden"),
        ("Colors of birds were:", "Red and Green", "Blue", "Yellow and Black", "White", "A", "Red and green"),
    ],
}


def generate_generic_mcq_for_chapter(chapter_name, subject):
    generic = [
        (f"What is important in {chapter_name}?", "Learning", "Forgetting", "Skipping", "Ignoring", "A", f"Learn {chapter_name}"),
        (f"In {chapter_name} we study about:", "Key concepts", "Nothing", "Random things", "Wrong answers", "A", f"Study key concepts of {chapter_name}"),
        (f"To understand {chapter_name}:", "Focus", "Daydream", "Sleep", "Be noisy", "A", "Focus is needed for learning"),
        (f"Chapter {chapter_name} teaches:", "Valuable lessons", "Nothing", "Just words", "Just pictures", "A", "Chapters teach valuable lessons"),
        (f"From {chapter_name} we learn:", "Important knowledge", "Nothing useful", "Only for exam", "Just for fun", "A", f"Learn from {chapter_name}"),
    ]
    return generic


total = 0

for chapter in chapters:
    chapter_name = chapter.name.strip()
    subject = chapter.subject.name
    
    MCQQuestion.objects.filter(chapter=chapter).delete()
    
    if chapter_name in chapter_questions:
        qs = chapter_questions[chapter_name][:5]
    else:
        qs = generate_generic_mcq_for_chapter(chapter_name, subject)
    
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
print(f"Done! Generated {total} unique MCQs for Class 1")
print("="*60)