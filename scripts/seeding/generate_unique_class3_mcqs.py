import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

print("=" * 60)
print("Generating Unique MCQs for Class 3 Chapters")
print("=" * 60)

grade = Grade.objects.get(slug='class-3')
chapters = list(Chapter.objects.filter(subject__grade=grade))

chapter_questions = {
    "Where to Look From": [
        ("From different views objects look:", "Different", "Same", "Always big", "Always small", "A", "Objects look different from different views"),
        ("Top view of a cup looks like:", "Circle", "Square", "Triangle", "Line", "A", "Cup from top looks circle"),
        ("Side view of a car is:", "2D", "3D", "Same as top", "Same as front", "A", "Side view is 2D"),
        ("We see objects from:", "Our eye level", "Underground", "Inside", "Behind", "A", "See from eye level"),
        ("Front view shows:", "Shape and design", "Top", "Behind", "Inside", "A", "Front shows front design"),
    ],
    "Fun with Numbers": [
        ("Biggest 3-digit number is:", "999", "900", "100", "9999", "A", "999 is biggest"),
        ("1000 is written as:", "One thousand", "Ten hundred", "One hundred tens", "Ten ten hundred", "A", "1000 = one thousand"),
        ("Which is smallest 3-digit?", "100", "999", "900", "101", "A", "100 is smallest 3-digit"),
        ("Place value of 5 in 758 is:", "50", "500", "5", "5000", "A", "5 is in tens place"),
        ("Number before 200 is:", "199", "198", "201", "100", "A", "199 comes before 200"),
    ],
    "Give and Take": [
        ("Addition is also called:", "Sum", "Difference", "Product", "Quotient", "A", "Sum = addition result"),
        ("423 + 100 = ?", "523", "423", "623", "500", "A", "Add 100 = 523"),
        ("Which addition is correct?", "100+200=300", "100+200=400", "100+200=200", "100+200=100", "A", "100+200=300"),
        ("Take means:", "Subtract", "Add", "Multiply", "Divide", "A", "Take = subtract"),
        ("Find sum of 234 + 342:", "576", "576", "575", "577", "A", "234+342=576"),
    ],
    "Long and Short": [
        ("Longer object has:", "More length", "Less length", "More width", "Less height", "A", "Long = more length"),
        ("Measure length using:", "Ruler", "Scale", "Weight", "Clock", "A", "Use ruler to measure"),
        ("Meter is used for:", "Long things", "Small things", "Light things", "Heavy things", "A", "Meter for long"),
        ("Centimeter is for:", "Small things", "Long things", "Heavy things", "Big things", "A", "cm for small"),
        ("1 meter = ___ cm", "100", "10", "1000", "10000", "A", "1m = 100cm"),
    ],
    "Shapes and Designs": [
        ("Which is a 3D shape?", "Cube", "Square", "Circle", "Triangle", "A", "Cube is 3D"),
        ("Square has ___ corners.", "4", "3", "5", "6", "A", "Square has 4 corners"),
        ("Triangle has ___ sides.", "3", "4", "5", "2", "A", "Triangle has 3 sides"),
        ("Rectangle is like:", "Door", "Ball", "Pyramid", "Cone", "A", "Door is rectangle"),
        ("Circle has ___ line.", "No straight", "4 straight", "3 straight", "Many straight", "A", "Circle no straight line"),
    ],
    "Whose is it?": [
        ("Whose shows:", "Ownership", "Time", "Place", "Number", "A", "Whose shows ownership"),
        ("This book is ___ Raghu.", "Raghu's", "Raghu", "Raghu is", "Of Raghu", "A", "Shows possession"),
        ("Whose bag is this?", "Mine", "I", "Me", "My", "A", "Shows my ownership"),
        ("We use whose for:", "Asking owner", "Asking time", "Asking place", "Asking number", "A", "Whose asks owner"),
        ("This house belongs to ___ family.", "The Sharma's", "Sharma", "Sharmas", "A Sharma", "A", "Shows family name"),
    ],
    "Time Goes On": [
        ("How many hours in a day?", "24", "12", "23", "25", "A", "24 hours in day"),
        ("60 minutes make:", "One hour", "One minute", "Half hour", "Quarter hour", "A", "60 min = 1 hour"),
        ("Morning to evening is:", "12 hours", "24 hours", "6 hours", "10 hours", "A", "Day is 12 hours"),
        ("We check time using:", "Clock", "Calendar", "Date", "Year", "A", "Clock shows time"),
        ("Which shows date?", "Calendar", "Clock", "Watch", "Timer", "A", "Calendar shows date"),
    ],
    "LKR / Rs and Paise": [
        ("Full form of LKR is:", "Rupees", "Paisa", "Dollar", "Cent", "A", "R = Rupees"),
        ("100 paise = ___ Rupee", "1", "10", "100", "1000", "A", "100 paise = Rs 1"),
        ("Rs 10 = ___ paise", "1000", "100", "10", "1", "A", "Rs 10 = 1000 paise"),
        ("Cost of 2 toffees at Rs 5:", "Rs 10", "Rs 7", "Rs 5", "Rs 12", "A", "2 x 5 = 10"),
        ("We need ___ for shopping.", "Money", "Time", "Water", "Food", "A", "Money needed to shop"),
    ],
    "Jugs and Mugs": [
        ("Litre is used to measure:", "Liquid", "Solid", "Gas", "Weight", "A", "Litre measures liquid"),
        ("1 litre = ___ ml", "1000", "100", "10", "1", "A", "1 L = 1000 ml"),
        ("Bigger container holds:", "More liquid", "Less liquid", "No liquid", "Some liquid", "A", "Bigger = more"),
        ("Half litre is:", "500 ml", "100 ml", "1000 ml", "50 ml", "A", "Half L = 500 ml"),
        ("Water in drops is measured in:", "Millilitres", "Litres", "Grams", "Meters", "A", "Small amounts in ml"),
    ],
    "Tens and Ones": [
        ("2 tens = ?", "20", "2", "200", "10", "A", "2 tens = 20"),
        ("Write 45 in tens and ones:", "4 tens + 5 ones", "40 + 5", "4 + 5", "45 ones", "A", "45 = 40+5"),
        ("73 has ___ tens.", "7", "70", "3", "73", "A", "73 has 7 tens"),
        ("Smallest 2-digit number is:", "10", "1", "11", "9", "A", "10 is smallest"),
        ("87 = ___ tens + ___ ones", "8 tens + 7 ones", "80+7", "8+7", "87 ones", "A", "87 = 80+7"),
    ],
    "My Funday": [
        ("Sunday is a ___ day.", "Holiday", "School day", "Working day", "Normal day", "A", "Sunday is holiday"),
        ("Which day is holiday?", "Sunday", "Monday", "Tuesday", "Wednesday", "A", "Sunday is holiday"),
        ("Friday comes after:", "Thursday", "Saturday", "Wednesday", "Tuesday", "A", "Friday after Thursday"),
        ("Days in a week:", "7", "5", "6", "8", "A", "Week has 7 days"),
        ("First day of week is:", "Sunday", "Monday", "Saturday", "Friday", "A", "Sunday first day"),
    ],
    "Add Our Points": [
        ("In game, points add up to give:", "Total score", "Nothing", "Loss", "Win", "A", "Points = total score"),
        ("Higher points means:", "Better score", "Worse score", "No change", "Disqualification", "A", "Higher = better"),
        ("We add points by:", "Counting", "Subtracting", "Multiplying", "Dividing", "A", "Add points by counting"),
        ("Who has more points?", "Winner", "Loser", "No one", "Both", "A", "Winner has more"),
        ("Points help track:", "Progress", "Nothing", "Loss", "Failure", "A", "Points track progress"),
    ],
    "Lines and Lines": [
        ("Straight line has:", "No curve", "Curves", "Circles", "Dots", "A", "Straight line no curve"),
        ("Curved line has:", "Bends", "No bend", "Corners", "Angles", "A", "Curved line bends"),
        ("Horizontal line goes:", "Side to side", "Up and down", "Diagonal", "Curved", "A", "Horizontal = sideways"),
        ("Vertical line goes:", "Up and down", "Side to side", "Diagonal", "Curve", "A", "Vertical = up-down"),
        ("Lines meeting at point form:", "Angle", "Circle", "Square", "Nothing", "A", "Meeting lines form angle"),
    ],
    "How Many Ponytails?": [
        ("Ponytails help count:", "Items", "People", "Animals", "Things", "A", "Ponytails count items"),
        ("This question is about:", "Grouping items", "Single item", "One item", "No item", "A", "Grouping = counting"),
        ("For counting we:", "Group items", "Throw items", "Break items", "Mix items", "A", "Group to count easier"),
        ("How many groups?", "Depends on items", "One", "None", "Fixed", "A", "Groups vary"),
        ("We use ponytails to show:", "Multiple of 10", "Multiple of 5", "Multiple of 2", "Multiple of 3", "A", "Shows grouping"),
    ],
    "Good Morning": [
        ("Good morning is used:", "In morning", "At night", "In evening", "Afternoon", "A", "Morning greeting"),
        ("A greeting shows:", "Respect", "Anger", "Rude", "Disrespect", "A", "Greeting = respect"),
        ("We should greet:", "Politely", "Rudely", "Loudly", "Angry", "A", "Greet politely"),
        ("Morning greeting makes day:", "Better", "Worse", "Same", "Bad", "A", "Greeting makes better"),
        ("People say good morning to:", "Start nicely", "End day", "Say goodbye", "Complain", "A", "Start nicely"),
    ],
    "The Magic Garden": [
        ("Magic garden is:", "Special garden", "Normal garden", "Empty plot", "Forest", "A", "Magic = special"),
        ("This is a:", "Fiction story", "True story", "Poem", "History", "A", "Magic garden fiction"),
        ("In story we find:", "Imagination", "Facts", "Numbers", "Science", "A", "Stories have imagination"),
        ("Stories teach:", "Lessons", "Nothing", "Just words", "Random", "A", "Stories teach lessons"),
        ("We should read:", "Stories", "Only textbooks", "Nothing", "Textbooks only", "A", "Read stories too"),
    ],
    "Bird Talk": [
        ("Birds communicate by:", "Sounds", "Writing", "Reading", "Numbers", "A", "Birds use sounds"),
        ("Different birds make:", "Different sounds", "Same sound", "No sound", "One sound", "A", "Different birds different sounds"),
        ("We can learn bird sounds by:", "Listening", "Reading", "Writing", "Watching", "A", "Learn by listening"),
        ("Birds talk to:", "Each other", "Humans only", "Animals only", "Nothing", "A", "Birds talk each other"),
        ("Learning bird sounds helps:", "Identify birds", "Catch birds", "Hurt birds", "Nothing", "A", "Identify by sounds"),
    ],
    "Nina and the Baby Sparrows": [
        ("Who is Nina?", "Character in story", "Bird", "Animal", "Insect", "A", "Nina is character"),
        ("Baby sparrows need:", "Care", "Nothing", "To fly", "To fight", "A", "Babies need care"),
        ("We should protect:", "Baby birds", "Adult birds only", "No birds", "Other animals", "A", "Protect babies too"),
        ("Nest has baby birds in:", "Spring", "Winter", "Summer", "All seasons", "A", "Spring is nesting time"),
        ("Story teaches us to:", "Care for birds", "Ignore birds", "Catch birds", "Hurt birds", "A", "Care for birds"),
    ],
    "Little by Little": [
        ("Little by little means:", "Gradually", "All at once", "Never", "Quickly", "A", "Gradually = little by little"),
        ("Learning happens:", "Over time", "Instantly", "Overnight", "Suddenly", "A", "Learning takes time"),
        ("Practice helps learn:", "Little by little", "Nothing", "Only reading", "Only writing", "A", "Practice = gradual improvement"),
        ("Small steps lead to:", "Big achievements", "Nothing", "Failure", "Loss", "A", "Little by little = big"),
        ("We should learn:", "Daily", "Once", "Never", "Sometimes", "A", "Learn daily"),
    ],
    "Rain": [
        ("Rain comes from:", "Clouds", "Sun", "Moon", "Stars", "A", "Rain from clouds"),
        ("Rain is important for:", "Plants", "Animals only", "Humans only", "Nothing", "A", "Rain essential for all"),
        ("Too much rain causes:", "Floods", "Drought", "Heat", "Fire", "A", "Too much rain = flood"),
        ("Rain water goes to:", "Rivers and ground", "Sky", "Air", "Clouds", "A", "Rain to rivers"),
        ("We should save:", "Rainwater", "Ocean water", "Tap water", "Bottled water", "A", "Save rainwater"),
    ],
    "The Story of the Viceroy": [
        ("Viceroy was:", "Ruler's representative", "Common man", "Teacher", "Farmer", "A", "Viceroy = representative"),
        ("This is a:", "History story", "Fiction", "Poem", "Science", "A", "Viceroy is history"),
        ("We learn history from:", "Stories", "Only numbers", "Only science", "Nothing", "A", "Stories teach history"),
        ("Past teaches us:", "Lessons", "Nothing", "Just names", "Random", "A", "Past teaches lessons"),
        ("History is about:", "Past events", "Future", "Only kings", "Nothing", "A", "History = past"),
    ],
    "My Family": [
        ("Family members are:", "Related people", "Friends", "Strangers", "Enemies", "A", "Family = related"),
        ("We love our family because:", "They care for us", "They fight", "They leave", "They ignore", "A", "Family cares"),
        ("In family we share:", "Love and care", "Only food", "Only house", "Nothing", "A", "Share love"),
        ("Family teaches us:", "Values", "Nothing", "Bad habits", "Laziness", "A", "Family teaches values"),
        ("We should respect:", "Elders", "Only young", "No one", "Strangers", "A", "Respect elders"),
    ],
    "Water O' Water!": [
        ("Water is essential for:", "All life", "Nothing", "Only plants", "Only animals", "A", "Water essential for all"),
        ("How much of Earth is water?", "71%", "50%", "30%", "10%", "A", "Earth 71% water"),
        ("We should save:", "Water", "Waste", "Pollute", "Ignore", "A", "Save water"),
        ("Clean water is:", "Precious", "Unlimited", "Free", "Never ending", "A", "Clean water precious"),
        ("Without water:", "Life impossible", "Life better", "No change", "More life", "A", "Water = life"),
    ],
    "The Plant Fairy": [
        ("Plant Fairy cares for:", "Plants", "Animals", "Humans", "Birds", "A", "Plant Fairy = plants"),
        ("This is a:", "Fiction story", "True story", "History", "Science fact", "A", "Fairy = fiction"),
        ("Plants need:", "Water and sun", "Only sun", "Only water", "Nothing", "A", "Plants need both"),
        ("We should:", "Grow plants", "Cut plants", "Ignore plants", "Waste plants", "A", "Grow plants"),
        ("Story teaches us:", "Care for nature", "Ignore nature", "Destroy nature", "Waste nature", "A", "Care for nature"),
    ],
    "Our First School": [
        ("Our first school is:", "Home", "Garden", "Park", "Temple", "A", "Home = first school"),
        ("Who are our first teachers?", "Parents", "Strangers", "Teachers", "Friends", "A", "Parents first teachers"),
        ("At home we learn:", "Basics", "Nothing", "Only fun", "Only play", "A", "Learn basics at home"),
        ("Family teaches:", "Values", "Only ABC", "Only numbers", "Nothing", "A", "Family teaches values"),
        ("First learning stays with us:", "For life", "For school", "For while", "Never", "A", "First learning = lifelong"),
    ],
    "Chhotu's House": [
        ("Chhotu's house is:", "Small house", "Palace", "Mansion", "Castle", "A", "Chhotu = small"),
        ("Small house can be:", "Cozy", "Uncomfortable", "Big", "Empty", "A", "Small can be cozy"),
        ("Home is important for:", "Living", "Nothing", "Playing", "Storing", "A", "Home for living"),
        ("We love our:", "Home", "Others house", "Park", "School", "A", "Love our home"),
        ("What makes house a home?", "Family", "Furniture", "TV", "Car", "A", "Family makes home"),
    ],
    "Poonam's Day Out": [
        ("Poonam is character:", "In story", "Real person", "Bird", "Animal", "A", "Poonam is character"),
        ("Day out means:", "Going outside", "Staying home", "Sleeping", "Working", "A", "Day out = outside"),
        ("We enjoy:", "Outings", "Staying in", "Working", "Sleeping", "A", "Outings are fun"),
        ("Places to visit:", "Parks, museums, zoos", "Only homes", "Only markets", "Nowhere", "A", "Visit various places"),
        ("Outing teaches us:", "New things", "Nothing", "Only fun", "Tiredness", "A", "Outings teach new things"),
    ],
    " Zoo Manners": [
        ("At zoo we should follow:", "Rules", "No rules", "Any rule", "Broken rules", "A", "Follow zoo rules"),
        ("We watch animals:", "Quietly", "Loudly", "Running", "Teasing", "A", "Watch quietly"),
        ("Feeding animals:", "As per rules", "Anything", "Our food", "Nothing", "A", "Feed as per rules"),
        ("Zoo Animals are:", "For watching", "For touching", "For feeding", "For playing", "A", "Watch only"),
        ("We should keep zoo:", "Clean", "Dirty", "Noisy", "Broken", "A", "Keep zoo clean"),
    ],
    "On My Blackboard": [
        ("Blackboard is for:", "Drawing and writing", "Eating", "Playing", "Hanging", "A", "Blackboard = draw/write"),
        ("We draw with:", "Chalk", "Pen", "Pencil", "Marker", "A", "Chalk on blackboard"),
        ("Blackboard was used in:", "Schools", "Homes", "Offices", "All places", "A", "Blackboard in schools"),
        ("Now we have:", "Boards and screens", "Only blackboard", "Nothing", "Paper", "A", "Now boards and screens"),
        ("Drawing helps:", "Creativity", "Nothing", "Waste time", "Bad", "A", "Drawing boosts creativity"),
    ],
    "Give and Take": [
        ("Give and take means:", "Exchange", "One way", "Nothing", "Loss only", "A", "Give and take = exchange"),
        ("In groups we:", "Share", "Keep all", "Not share", "Fight", "A", "Share with others"),
        ("Sharing is:", "Good", "Bad", "Waste", "Loss", "A", "Sharing is good"),
        ("We give to:", "Receive", "Lose", "Nothing", "Fight", "A", "Give to receive"),
        ("Taking without giving:", "Not fair", "Fair", "Good", "Better", "A", "Must give back"),
    ],
    "The Longest Step": [
        ("Longest step measure length:", "Foot", "Meter", "Hand", "Finger", "A", "Foot for long measure"),
        ("Step is used for:", "Measuring roughly", "Exact measure", "No use", "Small things", "A", "Step = rough measure"),
        ("Who takes longer steps?", "Adults", "Babies", "Everyone same", "No one", "A", "Adults longer steps"),
        ("Step length varies from:", "Person to person", "Same for all", "Fixed", "No idea", "A", "Step varies"),
        ("For accuracy we need:", "Measuring tool", "Foot", "Hand", "Eye", "A", "Use proper tool"),
    ],
    "Birds Come, Birds Go": [
        ("Birds migrate to find:", "Food and warmth", "Nothing", "Fun", "Adventure", "A", "Migrate for food/warmth"),
        ("Birds that fly south are:", "Migratory", "Non-migratory", "Domestic", "Pet", "A", "Migratory birds"),
        ("Migration happens in:", "Changing seasons", "One season", "No pattern", "Same time always", "A", "Migration = seasonal"),
        ("Birds fly in:", "Groups", "Alone", "Never", "Pair", "A", "Birds fly in groups"),
        ("We should protect:", "Migratory birds", "Hunt birds", "Catch birds", "Nothing", "A", "Protect birds"),
    ],
    "Make it Shorter": [
        ("Make it shorter means:", "Reduce", "Increase", "Keep same", "Multiply", "A", "Shorter = reduce"),
        ("This is useful in:", "Summarizing", "Adding", "Multiplying", "Dividing", "A", "Summarizing"),
        ("We make sentences shorter by:", "Using key words", "Adding more", "Writing long", "Nothing", "A", "Key words summarize"),
        ("Shorter form is also called:", "Summary", "Full form", "Longer form", "Detail", "A", "Summary = shorter"),
        ("Books have ___ chapters.", "Shorter", "Longer", "Same", "No", "A", "Books have shorter chapters"),
    ],
    "The Grasshopper and the Ant": [
        ("Grasshopper is:", "Insect", "Bird", "Animal", "Fish", "A", "Grasshopper = insect"),
        ("Grasshopper sings in:", "Summer", "Winter", "Spring", "All seasons", "A", "Grasshopper summer"),
        ("Ant works:", "In summer", "In winter", "Never", "Sometimes", "A", "Ants work summer"),
        ("Story teaches:", "Save for future", "Enjoy only", "Work later", "Nothing", "A", "Save for future"),
        ("We should be like:", "Ant", "Grasshopper", "None", "Both", "A", "Be like ant"),
    ],
    "Funny Bunny": [
        ("Bunny is:", "Rabbit", "Dog", "Cat", "Bird", "A", "Bunny = rabbit"),
        ("Bunny is known for:", "Jumping", "Flying", "Swimming", "Crawling", "A", "Bunny jumps"),
        ("Bunny eats:", "Carrots and greens", "Meat", "Fish", "Insects", "A", "Bunny vegetarian"),
        ("Bunny's rabbit is called:", "Kit", "Puppy", "Cub", "Joey", "A", "Baby bunny = kit"),
        ("Bunny has ___ ears.", "Long", "Small", "No ears", "Short", "A", "Bunny has long ears"),
    ],
    "Mr. Nobody": [
        ("Mr. Nobody is:", "Imaginary character", "Real person", "Teacher", "Friend", "A", "Mr. Nobody fictional"),
        ("This story is about:", "Responsibility", "Fun", "Sports", "Food", "A", "Story about responsibility"),
        ("We should take responsibility:", "Of our actions", "Nothing", "Of others", "None", "A", "Take responsibility"),
        ("Mr. Nobody means:", "No one specific", "Someone", "Everyone", "Specific person", "A", "Everyone is somebody"),
        ("We should own up to:", "Mistakes", "Nothing", "Others mistakes", "No mistakes", "A", "Own mistakes"),
    ],
    "I am the Music Man": [
        ("Music Man is:", "Musical story", "Real person", "Singer", "Teacher", "A", "Music Man story"),
        ("Music makes us:", "Happy", "Sad", "Angry", "Tired", "A", "Music = happiness"),
        ("We can make music with:", "Various instruments", "Nothing", "One thing", "Only voice", "A", "Various instruments"),
        ("Music is for:", "Enjoyment", "Trouble", "Work", "Nothing", "A", "Music = enjoyment"),
        ("We should learn:", "Music", "Nothing", "Only studies", "No music", "A", "Learn music too"),
    ],
    "The Mumbai Musicians": [
        ("This story is from:", "Mumbai", "Delhi", "Chennai", "Kolkata", "A", "Mumbai musicians"),
        ("Musicians play:", "Instruments", "Nothing", "Only sing", "Dance only", "A", "Musicians play instruments"),
        ("Instruments need:", "Practice", "Nothing", "Breaking", "Throwing", "A", "Practice = skill"),
        ("We should respect:", "Musicians", "Only actors", "No one", "Everyone", "A", "Respect musicians"),
        ("This story teaches:", "Unity", "Division", "Fighting", "Nothing", "A", "Story teaches unity"),
    ],
    "Granny Granny Please Comb my Hair": [
        ("Granny is:", "Grandmother", "Mother", "Aunt", "Sister", "A", "Granny = grandmother"),
        ("We show ___ to elders.", "Respect", "Anger", "Rude", "Ignore", "A", "Respect elders"),
        ("Elders have:", "Experience", "Nothing", "Less knowledge", "No wisdom", "A", "Elders experienced"),
        ("We should listen to:", "Elders", "Only friends", "Strangers", "No one", "A", "Listen to elders"),
        ("This story teaches:", "Care for elders", "Ignore elders", "Leave elders", "Nothing", "A", "Care for elders"),
    ],
    "The Magic Porridge Pot": [
        ("Magic Porridge Pot is:", "Fiction story", "True story", "Recipe", "Science", "A", "Magic = fiction"),
        ("Magic means:", "Something impossible", "Normal thing", "Recipe", "Cooking", "A", "Magic = impossible"),
        ("This story is about:", "Magical item", "Cooking pot", "Simple pot", "Broken pot", "A", "Story about magic"),
        ("We read magic stories for:", "Fun", "Learning", "Science", "History", "A", "Magic = fun"),
        ("Magic is:", "Imagination", "Real", "Science", "Fact", "A", "Magic = imagination"),
    ],
    "Strange Talk": [
        ("Strange talk is:", "Different conversation", "Normal talk", "Group talk", "Speech", "A", "Strange = different"),
        ("We talk with:", "Words", "Gestures", "Sounds", "Silence", "A", "Talk with words"),
        ("Communication needs:", "Understanding", "Confusion", "Noise", "Nothing", "A", "Need understanding"),
        ("We should communicate:", "Clearly", "Confusingly", "Loudly", "Softly", "A", "Communicate clearly"),
        ("Strange talk can be:", "Different language", "Same language", "No language", "Sign language", "A", "Different language"),
    ],
    "Kakku": [
        ("Kakku is character's name in:", "Hindi story", "English story", "Maths", "Science", "A", "Kakku = Hindi character"),
        ("कक्कू story teaches:", "Important lesson", "Nothing", "Just fun", "Random", "A", "Story teaches important"),
        ("In Hindi we read:", "Stories", "Only poems", "Nothing", "Math only", "A", "Hindi has stories too"),
        ("We should read in:", "All languages", "Only one", "Nothing", "Only English", "A", "Read many languages"),
        ("This chapter is from:", "Hindi textbook", "English book", "Maths", "Science", "A", "From Hindi book"),
    ],
    "Shekhibaaz Makkhi": [
        ("Shekhibaaz means:", "Tricky", "Honest", "Simple", "Dumb", "A", "Shekhibaaz = tricky"),
        ("Makkhi is:", "Fly", "Ant", "Bee", "Butterfly", "A", "Makkhi = fly"),
        ("This story is about:", "Clever tricks", "Honest work", "Hard work", "Simple life", "A", "Tricky story"),
        ("We should not:", "Cheat", "Work", "Help", "Share", "A", "Don't cheat"),
        ("Story teaches:", "Don't be cunning", "Be cunning", "Use tricks", "Nothing", "A", "Don't be tricky"),
    ],
    "Chand Wali Amma": [
        ("Chand means:", "Moon", "Star", "Sun", "Sky", "A", "Chand = moon"),
        ("Amma means:", "Mother", "Father", "Sister", "Brother", "A", "Amma = mother"),
        ("Chand Wali Amma is:", "Moon mother", "Star mother", "Sun mother", "Sky mother", "A", "Moon mother"),
        ("Moon appears at:", "Night", "Day", "Morning", "Evening", "A", "Moon at night"),
        ("Moon changes shape every:", "Night", "Week", "Month", "Year", "A", "Moon changes monthly"),
    ],
    "Man Karta Hai": [
        ("Man Karta Hai means:", "Thinks", "Does", "Says", "Tells", "A", "Man = think"),
        ("We think with:", "Brain", "Heart", "Hands", "Eyes", "A", "Think with brain"),
        ("Thinking helps:", "Solve problems", "Create problems", "Nothing", "Confusion", "A", "Thinking solves"),
        ("We should think before:", "Acting", "Playing", "Eating", "Sleeping", "A", "Think before acting"),
        ("Who thinks?", "All people", "No one", "Only adults", "Only teachers", "A", "All think"),
    ],
    "Bahadur Bitto": [
        ("Bahadur means:", "Brave", "Weak", "Shy", "Dumb", "A", "Bahadur = brave"),
        ("Bitto is:", "Character's name", "Animal", "Bird", "Object", "A", "Bitto = name"),
        ("We should be:", "Brave", "Fearful", "Weak", "Shy", "A", "Be brave"),
        ("Being brave means:", "Facing fears", " Hurting others", "Running away", "Complaining", "A", "Brave = face fears"),
        ("Bahadur Bitto teaches:", "Bravery", "Cowardice", "Running", "Nothing", "A", "Teach bravery"),
    ],
    "Titli aur Kali": [
        ("Titli is:", "Butterfly", "Ant", "Bee", "Insect", "A", "Titli = butterfly"),
        ("Kali is:", "Caterpillar", "Fly", "Bug", "Worm", "A", "Kali = caterpillar"),
        ("Caterpillar becomes:", "Butterfly", "Moth", "Ant", "Bee", "A", "Caterpillar -> butterfly"),
        ("This is about:", "Life cycle", "Food", "Shelter", "Breathing", "A", "Life cycle"),
        ("We should protect:", "Butterflies", "Kill them", "Catch them", "Nothing", "A", "Protect butterflies"),
    ],
    "Meri Kitaab": [
        ("Meri Kitaab means:", "My Book", "Your Book", "His Book", "Her Book", "A", "Meri = my"),
        ("We love our:", "Books", "Toys", "Games", "Nothing", "A", "Love books"),
        ("Books give us:", "Knowledge", "Nothing", "Fun only", "Waste", "A", "Books give knowledge"),
        ("We should care for:", "Books", "Break them", "Throw them", "Nothing", "A", "Care for books"),
        ("Reading books is:", "Good habit", "Bad habit", "Waste time", "Boring", "A", "Reading is good"),
    ],
    "Meethi Sarangi": [
        ("Meethi means:", "Sweet", "Salty", "Sour", "Bitter", "A", "Meethi = sweet"),
        ("Sarangi is:", "Instrument", "Fruit", "Flower", "Tree", "A", "Sarangi = instrument"),
        ("Sarangi makes:", "Sweet music", "Noise", "Sound", "Nothing", "A", "Instrument music"),
        ("Musical instrument is played for:", "Music", "Nothing", "噪音", "Trouble", "A", "Play for music"),
        ("We should learn:", "Music", "Only studies", "Nothing", "No music", "A", "Learn music too"),
    ],
    "Tesu Raja Beech Bazar": [
        ("Tesu is:", "Character name", "King", "Queen", "Minister", "A", "Tesu = name or king"),
        ("Beech Bazar is:", "Middle of market", "Market", "Desert", "Forest", "A", "Middle of market"),
        ("This is a:", "Story", "Poem", "History", "Science", "A", "Story from Hindi"),
        ("We learn from stories to:", "Be sensible", "Be fooled", "Follow anyone", "Nothing", "A", "Learn sense"),
        ("This story shows:", "Wisdom", "Foolishness", "Wealth", "Power", "A", "Story shows wisdom"),
    ],
    "Bulbul": [
        ("Bulbul is:", "Bird", "Flower", "Tree", "Insect", "A", "Bulbul = bird"),
        ("Bulbul is known for:", "Singing", "Flying", "Dancing", "Swimming", "A", "Bulbul sings"),
        ("This is a:", "Poem", "Story", "Essay", "History", "A", "Bulbul is poem"),
        ("Poems have:", "Rhyming words", "No rhyme", "Long sentences", "Prose", "A", "Poems have rhyme"),
        ("We should read:", "Poems", "Only stories", "Nothing", "No poems", "A", "Read poems too"),
    ],
    "Ekki-Dokki": [
        ("Ekki-Dokki is:", "Playful word", "Story", "Poem", "History", "A", "Ekki-Dokki = playful"),
        ("This could be about:", "Play", "Work", "Study", "Rest", "A", "About playful activity"),
        ("We should have:", "Play time", "Work only", "Study only", "No play", "A", "Have play time"),
        ("Playing is:", "Important", "Waste", "Bad", "Wrong", "A", "Play is important"),
        ("This chapter is from:", "Hindi", "English", "Maths", "Science", "A", "From Hindi"),
    ],
    "Natkhat Chuha": [
        ("Natkhat means:", "Naughty", "Good", "Calm", "Shy", "A", "Natkhat = naughty"),
        ("Chuha is:", "Mouse", "Rat", "Both same", "Insect", "A", "Chuha = mouse"),
        ("Naughty mouse is:", "Tricky", "Good", "Calm", "Peaceful", "A", "Naughty = tricky"),
        ("This story teaches:", "Not to be naughty", "Be naughty", "Trick others", "Nothing", "A", "Don't be naughty"),
        ("A naughty child should:", "Learn discipline", "Stay naughty", "Not change", "Ignore", "A", "Learn discipline"),
    ],
    "Bus ke neeche Bagh": [
        ("Bus means:", "Vehicle", "Animal", "Bird", "Tree", "A", "Bus = vehicle"),
        ("Bagh is:", "Tiger", "Lion", "Bear", "Leopard", "A", "Bagh = tiger"),
        ("This is about:", "Tiger under bus", "Tiger in jungle", "Tiger in zoo", "Story", "A", "Story about tiger"),
        ("We should respect:", "All animals", "Only pets", "No animals", "Nothing", "A", "Respect animals"),
        ("This is:", "Story", "Poem", "Science", "Maths", "A", "Hindi story"),
    ],
    "Suraj Jaldi Aana Ji": [
        ("Suraj means:", "Sun", "Moon", "Star", "Sky", "A", "Suraj = sun"),
        ("Jaldi means:", "Quickly", "Slowly", "Never", "Later", "A", "Jaldi = quickly"),
        ("Suraj Jaldi Aana means:", "Sun come quickly", "Sun go", "Moon come", "Star come", "A", "Sun please come"),
        ("We need sun for:", "Light and warmth", "Nothing", "Only light", "Only warmth", "A", "Sun gives both"),
        ("This is:", "Poem", "Story", "Science", "History", "A", "Hindi poem"),
    ],
    "Bahut Hua": [
        ("Bahut means:", "Many", "Few", "One", "None", "A", "Bahut = many"),
        ("Hua means:", "Happened", "Will happen", "Not happen", "Nothing", "A", "Hua = happened"),
        ("Bahut Hua means:", "Many happened", "Nothing happened", "One happened", "Few happened", "A", "Many things happened"),
        ("This poem is about:", "Change and growth", "Static", "Nothing", "Loss", "A", "About change"),
        ("We also ___ over time.", "Grow", "Stay same", "Reduce", "Nothing", "A", "We grow over time"),
    ],
    "Meru": [
        ("Meru is:", "Mountain", "River", "Tree", "Animal", "A", "Meru = mountain"),
        ("This story mentions:", "Mountain climbing", "River flowing", "Tree growth", "Animal", "A", "Story about mountain"),
        ("Climbing mountain is:", "Difficult", "Easy", "Impossible", "Nothing", "A", "Mountain climbing tough"),
        ("We should try to:", "Climb higher", "Give up", "Stay", "Nothing", "A", "Try hard"),
        ("This is:", "Poem", "Story", "History", "Science", "A", "Hindi story"),
    ],
    "Duniya Aloor Gal": [
        ("Duniya means:", "World", "House", "Village", "City", "A", "Duniya = world"),
        ("Gal could be:", "Story or incident", "Object", "Animal", "Person", "A", "Gal = incident"),
        ("Duniya Aloor Gal is:", "Something happened in world", "Empty", "Story", "Nothing", "A", "Something happened"),
        ("We read to:", "Learn what happened", "Nothing", "Forget", "Waste", "A", "Learn what happened"),
        ("This is:", "Story", "Poem", "News", "History", "A", "Hindi story"),
    ],
    "Natak": [
        ("Natak means:", "Drama", "Poem", "Story", "Essay", "A", "Natak = drama"),
        ("Drama needs:", "Acting", "Reading", "Writing", "Nothing", "A", "Drama needs acting"),
        ("We do drama in:", "School", "Home", "Office", "Everywhere", "A", "Drama in school"),
        ("Drama helps learn:", "Many skills", "Same skills", "No skills", "One skill", "A", "Drama teaches many"),
        ("This is:", "Drama", "Poem", "Story", "History", "A", "Natak = drama"),
    ],
    "Dhoom": [
        ("Dhoom means:", "Sound or excitement", "Quiet", "Peace", "Calm", "A", "Dhoom = sound/excitement"),
        ("This could be about:", "Excitement", "Peace", "Quiet", "Nothing", "A", "Excitement or sound"),
        ("Dhoom can be:", "Exclamatory", "Quiet", "Calm", "Silent", "A", "Dhoom = sound/excitement"),
        ("Used to show:", "Excitement", "Boredom", "Sleep", "Nothing", "A", "Show excitement"),
        ("This is:", "Poem", "Story", "Drama", "Essay", "A", "Hindi poem"),
    ],
    "Mere jit": [
        ("Mere means:", "My", "Your", "His", "Her", "A", "Mere = my"),
        ("Jit means:", "Victory or win", "Loss", "Draw", "Nothing", "A", "Jit = win/victory"),
        ("Mere jit means:", "My victory", "Your win", "His win", "Our win", "A", "My victory"),
        ("We should aim for:", "Victory", "Defeat", "Loss", "Nothing", "A", "Aim for victory"),
        ("This is:", "Poem", "Story", "Drama", "History", "A", "Hindi poem about win"),
    ],
}


def generate_chapter_mcq(chapter_name):
    if chapter_name in chapter_questions:
        return chapter_questions[chapter_name][:5]
    
    lower_name = chapter_name.lower()
    
    topics = {
        "Maths": [
            (f"What is important in {chapter_name}?", "Calculation skills", "Memorization", "Nothing", "Confusion", "A", f"Practice {chapter_name}"),
            (f"{chapter_name} helps in:", "Math", "Nothing", "Forgetting", "Confusion", "A", f"{chapter_name} = useful math"),
            (f"Learn {chapter_name} concept through:", "Practice", "Reading only", "Memorizing", "Copying", "A", f"Practice improves {chapter_name}"),
            (f"To solve {chapter_name}:", "Apply formula", "Guess", "Random answer", "Skip", "A", f"Apply formula for {chapter_name}"),
            (f"{chapter_name} is part of:", "Mathematics", "Language", "Science", "History", "A", f"{chapter_name} is math topic"),
        ],
        "English": [
            (f"Read {chapter_name} story", "Story", "Poem", "Essay", "None", "A", f"Reading {chapter_name} is story"),
            (f"What does {chapter_name} teach?", "Important values", "Nothing", "Just words", "Fun only", "A", f"Values from {chapter_name}"),
            (f"Characters in {chapter_name}:", "Need careful reading", "None", "All known", "Simple", "A", f"Characters in story"),
            (f"Lesson from {chapter_name}:", "Life lessons", "Nothing", "Fun", "Entertainment", "A", f"Life lessons from {chapter_name}"),
            (f"We should learn from {chapter_name}:", "Good habits", "Bad habits", "Nothing", "Ignore", "A", f"Good habits from {chapter_name}"),
        ],
        "Hindi": [
            (f"कहानी {chapter_name} में:", "कहानी है", "कुछ नहीं", "कोई नहीं", "सब गलत", "A", f"{chapter_name} कहानी है"),
            (f"{chapter_name} से सीखें:", "सीख", "भूलें", "उठाएं", "त्यागें", "A", f"सीख {chapter_name} से"),
            (f"पाठ {chapter_name} का:", "महत्व", "कोई नहीं", "कम", "अधिक", "A", f"महत्व {chapter_name} का"),
            (f"इस कहानी में:", "शिक्षा", "कुछ नहीं", "मज़े", "उपदेश", "A", f"शिक्षा {chapter_name} में"),
            (f"हमें {chapter_name} से:", "सीखना चाहिए", "नकारना चाहिए", "भूलना चाहिए", "डरना चाहिए", "A", f"सीख {chapter_name} से"),
        ],
        "EVS": [
            (f"What do we learn from {chapter_name}?", "Environment", "Nothing", "Science", "History", "A", f"Environment learning"),
            (f"About nature in {chapter_name}:", "Nature study", "City", "Building", "Machine", "A", f"Nature in {chapter_name}"),
            (f"We should protect:", "Nature", "Destroy", "Waste", "Pollute", "A", f"Protect nature"),
            (f"Chapter {chapter_name} teaches:", "Care for earth", "Ignore earth", "Use more", "Waste", "A", f"Care for earth"),
            (f"Our duty: {chapter_name}", "Protect", "Damage", "Ignore", "Waste", "A", f"Protect environment"),
        ],
    }
    
    for subject_key, qs in topics.items():
        if subject_key.lower() in lower_name:
            return qs
    
    return topics["English"][:5]


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
print(f"Done! Generated {total} unique MCQs for Class 3")
print("="*60)