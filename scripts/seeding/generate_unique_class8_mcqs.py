import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

print("=" * 60)
print("Generating Unique MCQs for Class 8 Chapters")
print("=" * 60)

grade = Grade.objects.get(slug='class-8')
chapters = list(Chapter.objects.filter(subject__grade=grade))

chapter_questions = {
    "Rational Numbers": [
        ("Rational number can be written as:", "Fraction", "Only whole", "Only decimal", "Negative only", "A", "Any fraction"),
        ("-3/8 equals:", "-0.375", "0.375", "0.75", "3.75", "A", "-3 divided by 8"),
        ("Reciprocal of 4/7 is:", "7/4", "4/7", "1", "1/4", "A", "Reciprocal flips fraction"),
        ("Which is rational?", "All can be", "Only integers", "Only decimals", "None", "A", "All can be fractions"),
        ("Multiply: 2/3 × 3/4 = ?", "1/2", "5/12", "1", "1/4", "A", "Multiply numerators, denominators"),
    ],
    "Linear Equations in One Variable": [
        ("Equation has equal sign:", "Yes", "No", "Sometimes", "Never", "A", "Equation = equal sign"),
        ("If x + 7 = 15, then x = ?", "8", "22", "7", "15", "A", "15-7=8"),
        ("Solve: 3x = 18", "6", "3", "54", "15", "A", "18÷3=6"),
        ("2x - 5 = 7 gives x = ?", "6", "5", "12", "1", "A", "2x=12, x=6"),
        ("Solution makes equation:", "True", "False", "Unchanged", "Nothing", "A", "True value"),
    ],
    "Understanding Quadrilaterals": [
        ("Quadrilateral has:", "4 sides", "3 sides", "5 sides", "6 sides", "A", "Quadrilateral = 4 sides"),
        ("Parallelogram has:", "Both pairs parallel", "One pair", "No pair", "All sides equal", "A", "Both pairs parallel"),
        ("Rectangle has:", "Opposite sides equal", "All sides equal", "Two equal", "No equal", "A", "Opposite = equal"),
        ("Kite has:", "Two pairs equal", "No equal", "All equal", "Parallel", "A", "Two pairs adjacent equal"),
        ("Rhombus is:", "All sides equal", "Only opposite equal", "No equal", "One pair", "A", "All sides equal"),
    ],
    "Practical Geometry": [
        ("Construction helps:", "Accurate figures", "Rough drawings", "Freehand", "Anything", "A", "Accurate needed"),
        ("To construct square, we need:", "Side length", "Angles", "Both", "Nothing", "A", "Need side + angles"),
        ("Ruler and compass help draw:", "Equal lengths", "Angles", "Both", "Everything", "A", "Used for accuracy"),
        ("Diagonal cuts square into:", "Two triangles", "Three", "Four", "None", "A", "Two congruent triangles"),
        ("Construction requires:", "Precision", "Guessing", "Approximation", "Nothing", "A", "Precision important"),
    ],
    "Data Handling": [
        ("Frequency shows:", "How often", "Total", "Average", "Range", "A", "Frequency = how many times"),
        ("Pie chart shows parts of:", "Whole", "Nothing", "Total", "Average", "A", "Shows whole as portions"),
        ("Probability of impossible event:", "0", "1", "1/2", "Any", "A", "Impossible = 0"),
        ("Probability is always between:", "0 and 1", "-1 and 1", "1 and 100", "Any", "A", "0 to 1 range"),
        ("Mean is affected by:", "All values", "Extremes", "Only extremes", "None", "A", "All values count"),
    ],
    "Squares and Square Roots": [
        ("Square of 12 is:", "144", "24", "121", "169", "A", "12×12 = 144"),
        ("Square root reverses:", "Squaring", "Multiplying", "Adding", "Nothing", "A", "Opposite of square"),
        ("Which is perfect square?", "144", "50", "60", "45", "A", "12² = 144"),
        ("√81 = ?", "9", "8", "7", "10", "A", "9×9 = 81"),
        ("Only positive square root exists:", "Yes", "No", "Sometimes", "Never", "A", "Principal = positive"),
    ],
    "Cubes and Cube Roots": [
        ("Cube of 4 is:", "64", "16", "44", "48", "A", "4×4×4 = 64"),
        ("Cube root of 125 is:", "5", "4", "3", "25", "A", "5³ = 125"),
        ("Which is perfect cube?", "27", "30", "35", "40", "A", "3³ = 27"),
        ("(-2)³ equals:", "-8", "-6", "8", "6", "A", "-2 × -2 × -2 = -8"),
        ("Cube root reverses:", "Cubing", "Squaring", "Multiplying", "Nothing", "A", "Opposite of cube"),
    ],
    "Comparing Quantities": [
        ("Ratio compares using:", "Division", "Subtraction", "Addition", "Multiplication", "A", "Ratio is division"),
        ("10% of 200 = ?", "20", "10", "200", "2", "A", "10% = 10/100 × 200"),
        ("Increase 80 by 15%:", "92", "95", "88", "90", "A", "80 + 12 = 92"),
        ("Discount reduces:", "Price", "Quality", "Quantity", "Value", "A", "Discount reduces price"),
        ("Simple interest formula:", "P×R×T/100", "P+R+T", "P×R+T", "Nothing", "A", "Interest = PTR/100"),
    ],
    "Algebraic Expressions": [
        ("Expression contains:", "Variables and numbers", "Only numbers", "Only variables", "Nothing", "A", "Variables+numbers"),
        ("Like terms have:", "Same variable power", "Different variables", "No relation", "None", "A", "Same variable power"),
        ("Add: 3x + 4x = ?", "7x", "x", "7", "12x", "A", "3+4=7 coefficients"),
        ("Subtract 2y from 7y:", "5y", "9y", "5", "9", "A", "7y - 2y = 5y"),
        ("Value of x if 3x + 2 = 14:", "4", "3", "5", "6", "A", "3x = 12, x = 4"),
    ],
    "Visualising Solid Shapes": [
        ("Cube has:", "6 faces", "4 faces", "8 faces", "12 faces", "A", "6 faces"),
        ("Solid has:", "Three dimensions", "Two dimensions", "One dimension", "Nothing", "A", "3D = L,B,H"),
        ("Vertices are:", "Corners", "Flat surfaces", "Edges", "Anything", "A", "Vertex = corner point"),
        ("Edges meet at:", "Vertices", "Faces", "Surfaces", "Nothing", "A", "Edge meets at vertex"),
        ("Net represents:", "Unfolded shape", "Volume", "Area", "Height", "A", "Net = 2D version"),
    ],
    "Factorisation": [
        ("Factor means:", "Divide completely", "Multiply", "Add", "Subtract", "A", "Factor divides evenly"),
        ("Common factor divides:", "Both terms", "One term", "None", "Nothing", "A", "Common factor shared"),
        ("Factorize: x² - 9 = ?", "(x+3)(x-3)", "x²-9", "x-3", "x+3", "A", "Difference of squares"),
        ("Factorization helps solve:", "Equations", "Nothing", "Multiply", "Add", "A", "Solve equations easier"),
        ("Factor by grouping:", "Groups terms", "One term", "All terms", "Nothing", "A", "Group common factors"),
    ],
    "Introduction to Graphs": [
        ("Graph shows relationship between:", "Variables", "Same value", "Nothing", "One variable", "A", "Graph shows relation"),
        ("x-axis is:", "Horizontal", "Vertical", "Diagonal", "Circle", "A", "Horizontal = x-axis"),
        ("y-axis is:", "Vertical", "Horizontal", "Diagonal", "Line", "A", "Vertical = y-axis"),
        ("Origin is:", "Where axes meet", "Any point", "On x-axis", "On y-axis", "A", "Origin at (0,0)"),
        ("Ordered pair shows:", "x and y", "Only x", "Only y", "Nothing", "A", "(x,y) coordinates"),
    ],
    "Playing with Numbers": [
        ("Number patterns help find:", "Rules", "Randomness", "Nothing", "Fun only", "A", "Patterns = rules"),
        ("Divisibility rules help:", "Quick division", "Multiply", "Add", "Subtract", "A", "Quickly check divisibility"),
        ("Test for 3:", "Sum divisible by 3", "Last digit 3", "Even", "Nothing", "A", "Sum of digits"),
        ("Test for 11:", "Difference divisible", "Same", "Sum", "Nothing", "A", "Difference divisible"),
        ("Generalization means:", "Statement from pattern", "One case", "Random", "Nothing", "A", "Pattern becomes rule"),
    ],
    "Crop Production and Management": [
        ("Crops need:", "Water, nutrients, care", "Only water", "Nothing", "Sun only", "A", "Multiple needs"),
        ("Kharif crops grow in:", "Rainy season", "Winter", "Summer", "All seasons", "A", "Monsoon crops"),
        ("Rabi crops grow in:", "Winter", "Rainy season", "Summer", "All", "A", "Winter crops"),
        ("Weeding removes:", "Unwanted plants", "Crops", "Water", "Nothing", "A", "Remove competitors"),
        ("Manure provides:", "Nutrients", "Water", "Pests", "Nothing", "A", "Nutrients for crops"),
    ],
    "Microorganisms: Friend and Foe": [
        ("Microorganisms are:", "Tiny organisms", "Large organisms", "Visible", "Nothing", "A", "Too small to see"),
        ("Bacteria help in:", "Making curd", "Disease only", "Nothing", "Breaking", "A", "Useful bacteria"),
        ("Fungi can be:", "Useful and harmful", "Only useful", "Only harmful", "Nothing", "A", "Both useful/harmful"),
        ("Vaccines use:", "Killed/weakened germs", "Healthy germs", "Nothing", "Chemicals", "A", "immunity from germs"),
        ("Food preservation prevents:", "Growth of harmful microorganisms", "Nutrients", "Nothing", "Taste", "A", "Stop harmful growth"),
    ],
    "Synthetic Fibres and Plastics": [
        ("Synthetic fibers are:", "Man-made", "Natural", "From plants", "From animals", "A", "Artificial"),
        ("Nylon is:", "Synthetic", "Natural", "Cotton", "Silk", "A", "Nylon is synthetic"),
        ("Plastics are:", "Non-biodegradable", "Biodegradable", "Natural", "Organic", "A", "Do not decompose easily"),
        ("We should:", "Reduce plastic use", "Increase", "Throw everywhere", "Ignore", "A", "Reduce plastic"),
        ("Polythene comes from:", "Petroleum", "Plants", "Animals", "Nothing", "A", "From petroleum"),
    ],
    "Metals and Non-Metals": [
        ("Metals are generally:", "Shiny and malleable", "Dull", "Brittle", "Soft", "A", "Metals are shiny"),
        ("Non-metals are generally:", "Dull and brittle", "Shiny", "Malleable", "Hard", "A", "Non-metals are dull"),
        ("Metals conduct:", "Heat and electricity", "Only heat", "Only cold", "Nothing", "A", "Conductors"),
        ("Non-metals do NOT conduct:", "Heat and electricity", "Light", "Sound", "Nothing", "A", "Insulators"),
        ("Carbon makes:", "Graphite and diamond", "One form only", "Nothing", "Metal", "A", "Carbon allotropes"),
    ],
    "The Best Christmas Present in the World": [
        ("This is a story about:", "Gift and humanity", "Business", "Commerce", "Nothing", "A", "Gift of love"),
        ("Best present is:", "Something meaningful", "Expensive", "Popular", "Nothing", "A", "Meaning matters"),
        ("We should value:", "Relations over things", "Things over relations", "Money", "Nothing", "A", "Relationships important"),
        ("Story teaches:", "Humanity", "Commerce", "Competition", "Nothing", "A", "Humanity > material"),
        ("This is from:", "English reading", "Hindi", "Maths", "Science", "A", "English chapter"),
    ],
    "The Tsunami": [
        ("Tsunami is:", "Ocean waves caused by earthquakes", "Normal waves", "Tides", "Nothing", "A", "Earthquake waves"),
        ("This teaches about:", "Natural disasters", "Fun", "Business", "Nothing", "A", "Nature's power"),
        ("We should be prepared for:", "Disasters", "Nothing", "Parties", "Fun", "A", "Be prepared"),
        ("This brings awareness:", "Safety measures", "Entertainment", "Games", "Nothing", "A", "Safety awareness"),
        ("This is factual:", "Yes", "No", "Sometimes", "Never", "A", "Based on real events"),
    ],
    "The Last Stonecutter": [
        ("This shows:", "Contentment over ambition", "Ambition", "Wealth", "Power", "A", "Contentment lessons"),
        ("Story teaches:", "Be happy with what you have", "Want more", "Compete", "Nothing", "A", "Contentment"),
        ("Material success leads to:", "Not always happiness", "Always happiness", "Nothing", "Misery", "A", "Not guarantee happiness"),
        ("Best work is:", "One done with heart", "High pay", "Low effort", "Nothing", "A", "Heart matters"),
        ("We should value:", "Inner happiness", "Outer success", "Wealth", "Status", "A", "Inner happiness matters"),
    ],
    "Dhwani": [
        ("Dhwani means:", "Sound or rhyme", "Letter", "Word", "Silence", "A", "Dhwani = sound"),
        ("In poetry, dhwani adds:", "Musical quality", "Meaninglessness", "Complication", "Nothing", "A", "Adds music"),
        ("Sanskrit/Hindi poetry uses:", "Rhymes", "Free verse", "Nothing", "Prose", "A", "Rhymes common"),
        ("Dhwani helps express:", "Emotions", "Facts", "Numbers", "Nothing", "A", "Express feelings"),
        ("This is from:", "Hindi/Sanskrit", "English", "Maths", "Science", "A", "Language subject"),
    ],
    "Subhashitani": [
        ("Subhashita means:", "Wisdom saying", "Story", "Poem", "Nothing", "A", "Wise sayings"),
        ("This teaches:", "Moral values", "Stories", "Grammar", "Nothing", "A", "Teach wisdom"),
        ("Subhashitaani are:", "Moral maxims", "Love stories", "Adventures", "Nothing", "A", "Wise quotes"),
        ("We should follow:", "Moral teachings", "Worldly things", "Fame", "Nothing", "A", "Follow morals"),
        ("This is from:", "Sanskrit/Hindi", "English", "Science", "Maths", "A", "Language learning"),
    ],
    "How, When and Where": [
        ("History tells us about:", "Past events", "Future", "Present only", "Nothing", "A", "History = past"),
        ("Sources of history include:", "Documents, artifacts, oral accounts", "Guessing", "Nothing", "One source", "A", "Various sources"),
        ("Important to study history because:", "We learn from past", "It's boring", "Nothing", "For exams", "A", "Learn from past"),
        ("History helps understand:", "Present and future", "Nothing", "Just past", "Entertainment", "A", "Connect time"),
        ("This chapter is from:", "Social Science", "English", "Maths", "Science", "A", "History/Social"),
    ],
    "From Trade to Territory": [
        ("East India Company came as:", "Traders and then rulers", "Conquerors", "Visitors", "Nothing", "A", "Traders → rulers"),
        ("Company wanted:", "Profits and control", "Help", "Trade only", "Nothing", "A", "Wanted power"),
        ("This led to:", "British rule", "Indian freedom", "Nothing", "Partnership", "A", "Started British rule"),
        ("Trade led to:", "Territorial control", "Nothing", "Friendship", "Independence", "A", "Business → rule"),
        ("This is from:", "History", "Science", "Maths", "English", "A", "History chapter"),
    ],
    "Ruling the Countryside": [
        ("British ruled through:", "Revenue and legal systems", "Friendship", "Nothing", "Local kings", "A", "Control systems"),
        ("They introduced:", "New revenue system", "Old system", "Nothing", "Partnership", "A", "New systems"),
        ("Farmers were affected by:", "New taxes", "Benefits", "Nothing", "Freedom", "A", "Adverse effects"),
        ("This shows colonial:", "Administrative control", "Help", "Development", "Nothing", "A", "Control methods"),
        ("We learn about:", "Colonial history", "Future", "Nothing", "Entertainment", "A", "Past systems"),
    ],
    "Lakh Ki Chudiyan": [
        ("Lakh means:", "One lakh", "Small", "Few", "Many", "A", "One lakh = 100,000"),
        ("Ki means:", "Of", "With", "To", "For", "A", "Ki = of"),
        ("Chudiyan means:", "Bangles", "Ring", "Bracelet", "Necklace", "A", "Chudiyan = bangles"),
        ("Lakh ki chudiyan could mean:", "Bangles worth one lakh", "Cheap bangles", "One bangles", "No bangles", "A", "Expensive bangles"),
        ("This is from:", "Hindi", "English", "Maths", "Science", "A", "Hindi chapter"),
    ],
    "Dhool Bhari": [
        ("Dhool means:", "Dust", "Clean", "Water", "Air", "A", "Dhool = dust"),
        ("Bhari means:", "Filled or heavy", "Empty", "Light", "Clean", "A", "Bhari = filled"),
        ("Dhool bhari could mean:", "Dusty", "Clean", "Water", "Empty", "A", "Dusty or full of dust"),
        ("Hindi teaches:", "Language", "Values", "Both", "Nothing", "A", "Language and values"),
        ("Chapter is from:", "Hindi", "English", "Maths", "Science", "A", "Hindi subject"),
    ],
    "Vani Vyakhya": [
        ("Vani means:", "Sound, voice, speech", "Word", "Letter", "Silence", "A", "Vani = voice"),
        ("Vyakhya means:", "Explanation, interpretation", "Definition", "Meaning", "All", "A", "Interpretation"),
        ("Vani-vyakhya could mean:", "Speech interpretation", "Silent explanation", "Written", "No meaning", "A", "Explaining speech"),
        ("This is used in:", "Sanskrit/Hindi learning", "English", "Maths", "Science", "A", "Language learning"),
        ("We learn language through:", "Interpretation", "Memorization", "Rules", "Nothing", "A", "Learn meaning"),
    ],
}


def generate_chapter_mcq(chapter_name):
    if chapter_name in chapter_questions:
        return chapter_questions[chapter_name][:5]
    
    lower_name = chapter_name.lower()
    
    topics = {
        "Maths": [
            (f"Key concept in {chapter_name} is:", "Problem solving", "Memorizing", "Ignoring", "Skipping", "A", f"Solve {chapter_name}"),
            (f"{chapter_name} involves:", "Calculations", "Words", "Stories", "Nothing", "A", f"Math calculations"),
            (f"Practice {chapter_name} by:", "Solving examples", "Reading", "Memorizing", "Ignoring", "A", f"Solve examples"),
            (f"{chapter_name} uses:", "Numbers and formulas", "Only words", "Pictures", "Nothing", "A", f"Math formulas"),
            (f"This is part of:", "Mathematics", "English", "Science", "History", "A", "Maths topic"),
        ],
        "Science": [
            (f"What does {chapter_name} teach?", "Science concepts", "Nothing", "History", "Math", "A", f"Science in {chapter_name}"),
            (f"This chapter is about:", "Science topics", "City", "Buildings", "Stories", "A", f"Science topics"),
            (f"We should learn:", "Scientific facts", "Ignore", "Memorize only", "Nothing", "A", f"Learn science"),
            (f"Chapter {chapter_name}:", "Learning", "Nothing", "Fun", "Waste", "A", f"Learn from {chapter_name}"),
            (f"Our duty from {chapter_name}:", "Apply knowledge", "Ignore", "Waste", "Nothing", "A", f"Apply science"),
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
        "Social Science": [
            (f"What does {chapter_name} teach?", "History and geography", "Nothing", "Science", "Math", "A", f"Social in {chapter_name}"),
            (f"This chapter is about:", "Social topics", "Science", "Sports", "Entertainment", "A", f"Social topics"),
            (f"We should understand:", "Past events", "Ignore", "Memorize", "Nothing", "A", f"Understand history"),
            (f"Chapter {chapter_name}:", "Learning", "Nothing", "Fun", "Waste", "A", f"Learn from {chapter_name}"),
            (f"Our duty from {chapter_name}:", "Learn from past", "Ignore", "Waste", "Nothing", "A", f"Learn from past"),
        ],
    }
    
    for subject_key, qs in topics.items():
        if subject_key.lower() in lower_name:
            return qs
    
    return topics["Social Science"][:5]


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
print(f"Done! Generated {total} unique MCQs for Class 8")
print("="*60)