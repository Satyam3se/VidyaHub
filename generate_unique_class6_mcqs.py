import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

print("=" * 60)
print("Generating Unique MCQs for Class 6 Chapters")
print("=" * 60)

grade = Grade.objects.get(slug='class-6')
chapters = list(Chapter.objects.filter(subject__grade=grade))

chapter_questions = {
    "Knowing Our Numbers": [
        ("Biggest natural number is:", "No limit", "1 lakh", "1 crore", "10 lakh", "A", "Numbers infinite"),
        ("Place value shows:", "Position of digit", "Digit value", "Number name", "Nothing", "A", "Place = position"),
        ("Roman numerals use:", "Letters", "Numbers", "Symbols", "Nothing", "A", "Roman = letters"),
        ("In 345, face value of 4 is:", "4", "40", "400", "0", "A", "Face = digit itself"),
        ("Ascending means:", "Small to big", "Big to small", "Same", "Random", "A", "Ascending = increasing"),
    ],
    "Whole Numbers": [
        ("Whole numbers start from:", "0", "1", "-1", "10", "A", "Whole = 0,1,2,..."),
        ("1 is neither:", "Prime nor composite", "Prime", "Composite", "Even", "A", "1 is special"),
        ("Successor of 999 is:", "1000", "998", "1001", "9990", "A", "999+1=1000"),
        ("Predecessor of 100 is:", "99", "101", "98", "1000", "A", "100-1=99"),
        ("Which is whole number?", "All counting numbers", "Negatives", "Decimals", "Fractions", "A", "Whole = 0,1,2,3..."),
    ],
    "Playing with Numbers": [
        ("Factors divide:", "Exactly", "With remainder", "Partially", "Nothing", "A", "Factors divide exactly"),
        ("Multiples come from:", "Multiplying", "Dividing", "Adding", "Subtracting", "A", "Multiples by multiplying"),
        ("LCM is:", "Smallest common", "Largest common", "First common", "Last common", "A", "Least common multiple"),
        ("HCF is:", "Greatest common divisor", "Smallest common", "First common", "Last common", "A", "Highest common factor"),
        ("Prime numbers have:", "Only 2 factors", "More than 2", "No factors", "Many factors", "A", "Prime = 2 factors only"),
    ],
    "Basic Geometrical Ideas": [
        ("Line has:", "No endpoints", "Two endpoints", "One endpoint", "Many endpoints", "A", "Line extends both ends"),
        ("Ray has:", "One endpoint", "No endpoints", "Two endpoints", "Fixed", "A", "Ray = one endpoint"),
        ("Intersecting lines meet at:", "One point", "Two points", "No point", "Many points", "A", "Meet at one point"),
        ("Parallel lines:", "Never meet", "Meet at infinity", "Cross", "Touch", "A", "Parallel never meet"),
        ("Circle is a:", "Closed curve", "Straight line", "Angle", "Triangle", "A", "Circle closed curve"),
    ],
    "Understanding Elementary Shapes": [
        ("Triangle has:", "3 sides", "4 sides", "5 sides", "2 sides", "A", "Triangle 3 sides"),
        ("Quadrilateral has:", "4 sides", "3 sides", "5 sides", "6 sides", "A", "Quadrilateral 4 sides"),
        ("Right angle is:", "90 degrees", "180 degrees", "45 degrees", "360 degrees", "A", "Right = 90°"),
        ("Regular polygon has:", "Equal sides and angles", "Unequal", "Different", "None", "A", "Regular = equal all"),
        ("Cube is a:", "3D shape", "2D shape", "Line", "Point", "A", "Cube has 3 dimensions"),
    ],
    "Integers": [
        ("Integers include:", "Positives, negatives and zero", "Only positives", "Only negatives", "Decimals", "A", "Integers = ...-2,-1,0,1,2..."),
        ("Which is integer?", "-5", "1/2", "0.5", "2.1", "A", "Whole negatives"),
        ("Absolute value of -7 is:", "7", "-7", "0", "1", "A", "Absolute = positive"),
        ("-3 + -2 = ?", "-5", "5", "1", "-1", "A", "Negative adding negative"),
        ("Greater than -3 is:", "-2", "-4", "-5", "-10", "A", "-2 > -3"),
    ],
    "Fractions": [
        ("Fraction shows:", "Part of whole", "Complete", "Multiple", "Nothing", "A", "Fraction = part"),
        ("1/2 is:", "Half", "Quarter", "Complete", "Double", "A", "Half = 1/2"),
        ("In 5/7, denominator is:", "7", "5", "12", "1", "A", "Below = denominator"),
        ("Proper fraction numerator is:", "Less than denominator", "Greater", "Equal", "Double", "A", "Proper < denominator"),
        ("5/5 = ?", "1", "0", "5", "10", "A", "Same/same = 1"),
    ],
    "Decimals": [
        ("Decimal is another way to show:", "Fraction", "Whole", "Nothing", "Negative", "A", "Decimal = fraction form"),
        ("0.5 equals:", "1/2", "1/4", "3/4", "1/10", "A", "0.5 = half"),
        ("Decimal has decimal point:", "Yes", "No", "Sometimes", "Never", "A", "Decimal has point"),
        ("50 paise in rupees is:", "Rs 0.50", "Rs 50", "Rs 5", "Rs 0.05", "A", "100 paise = Re 1"),
        ("2.5 + 1.2 = ?", "3.7", "3.5", "4.0", "3.0", "A", "2.5+1.2=3.7"),
    ],
    "Data Handling": [
        ("Data handling means:", "Collecting and organizing data", "Throwing data", "Creating data", "Ignoring data", "A", "Data = collect and organize"),
        ("Average is:", "Sum divided by count", "Total", "Difference", "Product", "A", "Average = sum/count"),
        ("Pictograph uses:", "Pictures", "Numbers only", "Words", "Nothing", "A", "Pictograph = pictures"),
        ("Mode is:", "Most frequent", "Least frequent", "Middle", "Sum", "A", "Mode = most common"),
        ("Range is:", "Highest minus lowest", "Sum", "Average", "Total", "A", "Range = max-min"),
    ],
    "Mensuration": [
        ("Perimeter is:", "Boundary length", "Area", "Volume", "Height", "A", "Perimeter = boundary"),
        ("Area of rectangle is:", "Length × breadth", "2(length+breadth)", "Square of side", "Nothing", "A", "Area = L×B"),
        ("Square has all sides:", "Equal", "Different", "Two equal", "None", "A", "Square all equal"),
        ("Perimeter of square 4a is:", "4a", "a", "a²", "4a²", "A", "Square perimeter=4×side"),
        ("Circumference relates to:", "π × diameter", "Diameter", "Radius only", "Nothing", "A", "Circle circumference"),
    ],
    "Ratio and Proportion": [
        ("Ratio compares:", "Two quantities", "Many quantities", "One quantity", "Nothing", "A", "Ratio = two"),
        ("In ratio a:b, a is:", "First term", "Second term", "Third", "Last", "A", "First term = antecedent"),
        ("Proportion says:", "Two ratios equal", "Different", "One ratio", "Many ratios", "A", "Equal ratios = proportion"),
        ("If 2:3 = 4:x, then x is:", "6", "5", "7", "8", "A", "2/3=4/6 → x=6"),
        ("Unitary method finds:", "Value of one", "Total", "Difference", "Nothing", "A", "Find one unit first"),
    ],
    "Algebra": [
        ("Algebra uses:", "Letters for numbers", "Only numbers", "Only words", "Nothing", "A", "Algebra = letters"),
        ("Variable is:", "Can change value", "Fixed value", "Equal to number", "None", "A", "Variable = changeable"),
        ("Expression contains:", "Numbers and variables", "Only numbers", "Only variables", "Nothing", "A", "Expression = numbers+letters"),
        ("Equation has:", "Equal sign", "No sign", "Plus sign", "Minus sign", "A", "Equation = equal sign"),
        ("Solution makes equation:", "True", "False", "Unchanged", "Nothing", "A", "Solution = true"),
    ],
    "Practical Geometry": [
        ("Compass helps draw:", "Circles", "Squares", "Triangles", "Angles", "A", "Compass = circles"),
        ("Protractor measures:", "Angles", "Lengths", "Areas", "Circles", "A", "Protractor = angles"),
        ("Perpendicular lines meet at:", "90 degrees", "45 degrees", "180 degrees", "0", "A", "Perpendicular = 90°"),
        ("Bisector divides into:", "Two equal parts", "Three parts", "Four parts", "Nothing", "A", "Divide equally"),
        ("Construction needs:", "Ruler and compass", "Pen only", "Paper only", "Eraser", "A", "Requires tools"),
    ],
    "Symmetry": [
        ("Line of symmetry divides into:", "Two equal parts", "Three parts", "Four parts", "Nothing", "A", "Equal mirror parts"),
        ("Line symmetry shows:", "Mirror image", "Rotation", "Translation", "Nothing", "A", "Symmetry = mirror"),
        ("Circle has:", "Infinite lines", "One line", "Two lines", "No line", "A", "Circle infinite symmetry"),
        ("Regular polygon sides = lines of symmetry:", "Yes", "No", "Sometimes", "Never", "A", "Equal sides = equal lines"),
        ("Reflection changes:", "Orientation", "Size", "Position only", "Nothing", "A", "Mirror changes orientation"),
    ],
    "Visualising Solid Shapes": [
        ("3D shapes have:", "Length, breadth, height", "Only length", "Two dimensions", "One dimension", "A", "3D = 3 dimensions"),
        ("Cube is 3D because it has:", "Volume", "Only surface", "Perimeter", "Nothing", "A", "Volume means 3D"),
        ("Face of solid is:", "Flat surface", "Curved only", "Edge only", "Vertex only", "A", "Face = flat surface"),
        ("Edge is where:", "Two faces meet", "Three faces", "Four faces", "Nothing", "A", "Edge = face meeting"),
        ("Vertex is:", "Corner point", "Line", "Face", "Edge", "A", "Vertex = corner point"),
    ],
    "A Fire-rising Story": [
        ("This story is about:", "History", "Nothing", "Future", "Science", "A", "Historical story"),
        ("We should learn from:", "History", "Ignore", "Forget", "Waste", "A", "Learn from past"),
        ("History teaches:", "Lessons", "Nothing", "Entertainment only", "Random", "A", "Past = lessons"),
        ("Important events should be:", "Remembered", "Forgotten", "Ignored", "Changed", "A", "Remember important"),
        ("This is from:", "English textbook", "Hindi", "Maths", "Science", "A", "English reading"),
    ],
    "The Seven Brothers": [
        ("This is a story about:", "Family", "Adventure", "Science", "Math", "A", "Family story"),
        ("Family members should:", "Help each other", "Fight", "Separate", "Ignore", "A", "Family helps"),
        ("The story teaches:", "Unity", "Division", "Conflict", "Separation", "A", "Teaches unity"),
        ("We should respect:", "Elders", "Strangers only", "No one", "Enemies", "A", "Respect elders"),
        ("From stories we learn:", "Values", "Nothing", "Just fun", "Words only", "A", "Stories teach values"),
    ],
    "Taro's Reward": [
        ("Taro worked hard to:", "Help mother", "Play", "Sleep", "Waste", "A", "Helped mother"),
        ("Reward came to those who:", "Work hard", "Are lazy", "Quit", "Complain", "A", "Hard work rewarded"),
        ("This teaches:", "Hard work", "Laziness", "Complaining", "Waste", "A", "Teaches hard work"),
        ("We should help:", "Family", "Strangers", "No one", "Enemies", "A", "Help family"),
        ("Story shows:", "Good values", "Bad values", "Nothing", "Just fun", "A", "Shows good values"),
    ],
    "The Ashes That Made the King": [
        ("This story is from:", "Folk tales", "History", "Science", "Math", "A", "Folk tale story"),
        ("The story teaches:", "Wisdom", "Wealth", "Power", "Nothing", "A", "Wisdom from story"),
        ("We should value:", "Wisdom", "Money", "Power", "Status", "A", "Wisdom important"),
        ("Making king shows:", "Values matter over wealth", "Wealth is all", "Power is all", "Nothing", "A", "Values over wealth"),
        ("This is from:", "English reading", "Hindi", "Maths", "Science", "A", "English chapter"),
    ],
    "The Junk Seller": [
        ("Junk seller sells:", "Waste items", "New items", "Food", "Clothes", "A", "Sells waste"),
        ("Selling junk is:", "Waste management", "Waste of time", "Fun", "Nothing", "A", "Also waste mgmt"),
        ("We should:", "Recycle waste", "Throw waste", "Ignore waste", "Create more waste", "A", "Recycle waste"),
        ("Junk can be:", "Recycled", "Useless", "Thrown", "Pollution", "A", "Junk recyclable"),
        ("This teaches:", "Environmental value", "Nothing", "Just business", "Waste", "A", "Environment care"),
    ],
    "Colours": [
        ("Primary colours are:", "Red, blue, yellow", "Green, orange, purple", "Pink, brown, black", "All colours", "A", "Primary = red, blue, yellow"),
        ("Mixing red and yellow gives:", "Orange", "Green", "Purple", "Brown", "A", "Red+yellow=orange"),
        ("Blue and yellow mix to make:", "Green", "Orange", "Purple", "Brown", "A", "Blue+yellow=green"),
        ("Secondary colours come from:", "Mixing two primaries", "One primary", "No mixing", "Breaking", "A", "Secondary = mixed"),
        ("We use colours in:", "Art", "Science", "Math", "Nothing", "A", "Colours in art"),
    ],
    "Quality Time": [
        ("Quality time means:", "Meaningful time together", "Time alone", "Working time", "Sleeping time", "A", "Time together matters"),
        ("Family should spend:", "Quality time", "Separate time", "No time", "Busy time", "A", "Family time important"),
        ("Quality matters over:", "Quantity", "Nothing", "Money", "Status", "A", "Quality=meaningful"),
        ("This teaches:", "Family values", "Business", "Work", "Nothing", "A", "Family values"),
        ("This chapter is from:", "English", "Hindi", "Maths", "Science", "A", "English reading"),
    ],
    "Water": [
        ("Water is essential for:", "Life", "Nothing", "Luxury", "Fun", "A", "Water = life"),
        ("We should save:", "Water", "Waste", "Pollute", "Ignore", "A", "Save water"),
        ("Water covers ___ of Earth:", "71%", "50%", "20%", "10%", "A", "71% water"),
        ("Fresh water is:", "Limited", "Unlimited", "Available everywhere", "Free", "A", "Fresh water limited"),
        ("We should protect:", "Water sources", "Pollute", "Waste", "Ignore", "A", "Protect water"),
    ],
    "The Stone in the Belly": [
        ("This story shows:", "Problem solving", "Ignore problems", "Giving up", "Nothing", "A", "Problem solving"),
        ("Stone in the belly means:", "Fear or worry", "Eating stones", "Health issue", "Nothing", "A", "Metaphor for worry"),
        ("We should face:", "Problems", "Avoid", "Ignore", "Run away", "A", "Face problems"),
        ("Solutions come from:", "Thinking", "Complaining", "Worrying", "Ignoring", "A", "Thinking solves"),
        ("This teaches:", "Problem solving", "Running away", "Ignoring", "Complaining", "A", "Solve problems"),
    ],
    "The Legend of the Basil": [
        ("Basil is:", "Sacred plant", "Common weed", "Vegetable", "Fruit", "A", "Basil sacred"),
        ("This is from:", "Cultural stories", "Science only", "Math", "Nothing", "A", "Cultural story"),
        ("We should respect:", "Cultural values", "Ignore", "Break", "Waste", "A", "Respect culture"),
        ("Plants like basil are:", "Valuable", "Useless", "Common", "Nothing", "A", "Plants valuable"),
        ("From stories we learn:", "Values", "Nothing", "Just words", "Entertainment", "A", "Learn values"),
    ],
    "The Sun and the Moon": [
        ("This story is about:", "Astronomy", "Mere facts", "History", "Math", "A", "About sun and moon"),
        ("We should learn about:", "Science", "Nothing", "Myths only", "Entertainment", "A", "Learn science"),
        ("The sun is:", "Star", "Planet", "Moon", "Comet", "A", "Sun is a star"),
        ("The moon is:", "Earth's satellite", "Star", "Planet", "Sun", "A", "Moon satellite"),
        ("This teaches us:", "Scientific facts", "Nothing", "Just myths", "Stories", "A", "Science facts"),
    ],
    "The Thief Who Stole a Night": [
        ("This is a story showing:", "Value of time", "How to steal", "Crime", "Nothing", "A", "Value of time"),
        ("One night cannot be:", "Stolen", "Used", "Wasted", "Anything", "A", "Time valuable"),
        ("Time lost cannot be:", "Recovered", "Used", "Enjoyed", "Anything", "A", "Time cannot return"),
        ("We should value:", "Time", "Waste", "Lose", "Forget", "A", "Value time"),
        ("This is from:", "English", "Hindi", "Maths", "Science", "A", "English chapter"),
    ],
    "A Tale of Two Pots": [
        ("Two pots show:", "Different characteristics", "Same", "Nothing", "Equal", "A", "Different pots"),
        ("This teaches:", "Accept differences", "Copy others", "Be same", "Nothing", "A", "Accept differences"),
        ("Each pot has:", "Its own qualities", "No qualities", "Same qualities", "Bad qualities", "A", "Own unique qualities"),
        ("We should respect:", "Individuality", "Equality", "Similarity", "Sameness", "A", "Respect individuality"),
        ("This is:", "Life lesson", "Math", "Science", "History", "A", "Life lesson"),
    ],
    "The Gift of the River": [
        ("River gives:", "Water and life", "Nothing", "Flood only", "Erosion only", "A", "River gives life"),
        ("We should respect:", "Nature", "Pollute", "Waste", "Ignore", "A", "Respect nature"),
        ("Rivers are:", "Valuable resources", "Waste", "Problems", "Nothing", "A", "Rivers valuable"),
        ("We should keep rivers:", "Clean", "Polluted", "Dirty", "Anything", "A", "Keep clean"),
        ("This teaches:", "Environmental value", "Nothing", "Business", "Fun", "A", "Environment value"),
    ],
    "Kaun": [
        ("Kaun means:", "Who", "What", "Where", "When", "A", "Kaun = who"),
        ("This is used to ask about:", "Person", "Place", "Thing", "Time", "A", "Ask about person"),
        ("Kaun question needs:", "Person name", "Number", "Reason", "Time", "A", "Person answer"),
        ("We use kaun to ask:", "Identity", "Number", "Place", "Choice", "A", "Identity question"),
        ("This is from:", "Hindi", "English", "Maths", "Science", "A", "Hindi"),
    ],
    "Kaha Suna": [
        ("Kaha means:", "Said", "Did", "Went", "Came", "A", "Kaha = said"),
        ("Suna means:", "Heard", "Saw", "Did", "Went", "A", "Suna = heard"),
        ("This shows:", "Reporting", "Asking", "Telling", "Nothing", "A", "Reported speech"),
        ("This is used in:", "Storytelling", "Science", "Math", "Nothing", "A", "Stories telling"),
        ("From Hindi, we learn:", "Language", "Values", "Both", "Nothing", "A", "Language and values"),
    ],
    "Ladka Ladki": [
        ("Ladka means:", "Boy", "Girl", "Woman", "Man", "A", "Ladka = boy"),
        ("Ladki means:", "Girl", "Boy", "Woman", "Man", "A", "Ladki = girl"),
        ("Both are:", "Equal", "Different", "Not equal", "Similar", "A", "Both equal"),
        ("We should treat:", "Equally", "Differently", "With bias", "Unfair", "A", "Treat equally"),
        ("Hindi teaches:", "Language and values", "Only language", "Only grammar", "Nothing", "A", "All combined"),
    ],
    "Nanakraj Dhrub": [
        ("Nanakraj Dhrub was:", "Saint and scholar", "King", "Soldier", "Merchant", "A", "Saint and scholar"),
        ("This chapter teaches:", "Wisdom and knowledge", "Only history", "Religion", "Culture", "A", "Wisdom and knowledge"),
        ("We should learn:", "From wise people", "Ignore", "Follow blindly", "Reject", "A", "Learn from wise"),
        ("History shows:", "Role models", "Only events", "Nothing", "Fun", "A", "History = role models"),
        ("This is from:", "Hindi", "English", "Maths", "Science", "A", "Hindi chapter"),
    ],
}


def generate_chapter_mcq(chapter_name):
    if chapter_name in chapter_questions:
        return chapter_questions[chapter_name][:5]
    
    lower_name = chapter_name.lower()
    
    topics = {
        "Maths": [
            (f"Key concept in {chapter_name} is:", "Solving problems", "Memorizing", "Ignoring", "Skipping", "A", f"Solve {chapter_name}"),
            (f"{chapter_name} involves:", "Calculations", "Words", "Stories", "Nothing", "A", f"Math calculations"),
            (f"Practice {chapter_name} by:", "Solving examples", "Reading", "Memorizing", "Ignoring", "A", f"Solve examples"),
            (f"{chapter_name} uses:", "Numbers and formulas", "Only words", "Pictures", "Nothing", "A", f"Math formulas"),
            (f"This is part of:", "Mathematics", "English", "Science", "History", "A", "Maths topic"),
        ],
        "English": [
            (f"Reading {chapter_name}:", "Comprehension", "Vocabulary", "Grammar", "Nothing", "A", f"Read {chapter_name}"),
            (f"Lesson from {chapter_name}:", "Values", "Words", "Fun", "Nothing", "A", f"Values from {chapter_name}"),
            (f"Story in {chapter_name} teaches:", "Life skills", "Nothing", "Just entertainment", "Grammar", "A", f"Life skills"),
            (f"Characters in {chapter_name}:", "Show values", "Are boring", "Nothing", "No purpose", "A", f"Character values"),
            (f"The chapter is:", "Story or poem", "Essay only", "Article", "Nothing", "A", "English reading"),
        ],
        "Hindi": [
            (f"कहानी {chapter_name}:", "है", "नहीं है", "कुछ भी", "कोई नहीं", "A", f"{chapter_name} = story"),
            (f"{chapter_name} से सीखें:", "सीख", "भूलें", "नकारें", "उपेक्षा", "A", f"सीख {chapter_name} से"),
            (f"इस अध्याय में:", "कहानी या कविता", "व्याकरण", "शब्दावली", "कुछ भी", "A", f"Learning in {chapter_name}"),
            (f"पाठ {chapter_name} का:", "महत्व", "कोई नहीं", "कम", "अधिक", "A", f"Value of {chapter_name}"),
            (f"हमें {chapter_name} से:", "सीखना चाहिए", "भूलना चाहिए", "नकारना चाहिए", "छोड़ना चाहिए", "A", f"Learn from {chapter_name}"),
        ],
        "EVS": [
            (f"What does {chapter_name} teach?", "Environment", "Nothing", "Science", "History", "A", f"Environment"),
            (f"This chapter is about:", "Nature and life", "City", "Buildings", "Machines", "A", f"Nature"),
            (f"We should protect:", "Nature", "Destroy", "Pollute", "Ignore", "A", "Protect nature"),
            (f"Chapter {chapter_name}:", "Learning", "Nothing", "Fun", "Waste", "A", f"Learn"),
            (f"Our duty from {chapter_name}:", "Care for earth", "Damage", "Ignore", "Waste", "A", f"Duty"),
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
print(f"Done! Generated {total} unique MCQs for Class 6")
print("="*60)