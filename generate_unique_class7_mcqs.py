import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

print("=" * 60)
print("Generating Unique MCQs for Class 7 Chapters")
print("=" * 60)

grade = Grade.objects.get(slug='class-7')
chapters = list(Chapter.objects.filter(subject__grade=grade))

chapter_questions = {
    "Integers": [
        ("Integers include negative numbers:", "Yes", "No", "Sometimes", "Never", "A", "Integers include negatives"),
        ("(-5) + (-3) = ?", "-8", "8", "-2", "2", "A", "Adding negatives"),
        ("Subtract: 5 - (-3) = ?", "8", "2", "-2", "-8", "A", "Subtract negative"),
        ("(-7) × (-2) = ?", "14", "-14", "7", "-7", "A", "Negative × negative"),
        ("Which is integer?", "All of these", "Only positive", "Only negative", "None", "A", "Integers = all three"),
    ],
    "Fractions and Decimals": [
        ("5/8 as decimal is:", "0.625", "0.5", "0.75", "0.875", "A", "5÷8=0.625"),
        ("0.35 equals fraction:", "35/100", "35/10", "35/1000", "350/100", "A", "Two decimal places"),
        ("3 1/2 as improper fraction:", "7/2", "3/2", "6/2", "5/2", "A", "3×2+1=7/2"),
        ("3/4 + 1/4 = ?", "1", "2", "1/2", "4/4", "A", "Same denominator adds"),
        ("Which fraction is largest?", "5/6", "3/6", "4/6", "2/6", "A", "5/6 > 4/6 > 3/6 > 2/6"),
    ],
    "Data Handling": [
        ("Mean is:", "Sum divided by count", "Total", "Difference", "Product", "A", "Mean = sum÷count"),
        ("Mode is:", "Most frequent value", "Average", "Middle", "Range", "A", "Mode = most common"),
        ("Range is:", "Highest minus lowest", "Sum", "Average", "Total", "A", "Range = max - min"),
        ("Median is:", "Middle value when arranged", "Most frequent", "Mean", "Mode", "A", "Middle arranged"),
        ("Probability range is:", "0 to 1", "Negative to positive", "0 to 100", "-1 to 1", "A", "Probability 0-1"),
    ],
    "Simple Equations": [
        ("Equation has:", "Equal sign", "Plus sign", "Minus sign", "Nothing", "A", "Equation = equal sign"),
        ("If x + 5 = 12, then x = ?", "7", "17", "5", "12", "A", "12-5=7"),
        ("Solution makes equation:", "True", "False", "Unchanged", "Nothing", "A", "True solution"),
        ("Variables can be:", "Replaced by numbers", "Fixed", "None", "Letters only", "A", "Variables are numbers"),
        ("To solve, do same operation:", "Both sides", "One side", "Left side only", "Right side only", "A", "Same both sides"),
    ],
    "Lines and Angles": [
        ("Angles sum in triangle:", "180 degrees", "360 degrees", "90 degrees", "0", "A", "Triangle 180°"),
        ("Vertically opposite angles are:", "Equal", "Complementary", "Supplementary", "Different", "A", "Equal when lines cross"),
        ("Parallel lines have:", "Never meeting", "Meeting at infinity", "Perpendicular", "Intersecting", "A", "Parallel never meet"),
        ("Linear pair adds to:", "180 degrees", "90 degrees", "360 degrees", "45 degrees", "A", "Linear pairs = 180°"),
        ("Corresponding angles are:", "Equal", "Different", "Complementary", "Zero", "A", "Corresponding = equal"),
    ],
    "Triangles and Its Properties": [
        ("Triangle has:", "3 sides", "4 sides", "5 sides", "2 sides", "A", "3 sides = triangle"),
        ("Sum of interior angles:", "180 degrees", "360 degrees", "90 degrees", "0", "A", "Always 180°"),
        ("Equilateral triangle has:", "All equal sides", "Two equal", "No equal", "Different", "A", "All 3 equal"),
        ("Isosceles has:", "Two equal sides", "All equal", "No equal", "Three equal", "A", "Two equal sides"),
        ("Pythagoras theorem relates to:", "Right triangle", "Any triangle", "Equilateral", "Isosceles", "A", "Right triangle"),
    ],
    "Comparing Quantities": [
        ("Ratio compares using:", "Division", "Subtraction", "Addition", "Multiplication", "A", "Ratio is division"),
        ("Percent means:", "Per hundred", "Per ten", "Per thousand", "Per one", "A", "Percent = per 100"),
        ("20% of 150 = ?", "30", "20", "25", "35", "A", "20% = 20/100 × 150"),
        ("Increase 50 by 10%", "55", "50", "60", "45", "A", "50 + 10% of 50 = 55"),
        ("Discount reduces:", "Price", "Quality", "Quantity", "Nothing", "A", "Discount reduces price"),
    ],
    "Rational Numbers": [
        ("Rational number can be expressed as:", "Fraction", "Whole number only", "Decimal only", "Negative only", "A", "Any fraction"),
        ("-3/5 equals:", "-0.6", "0.6", "0.3", "-0.3", "A", "Divide -3 by 5"),
        ("Reciprocal of 3/4 is:", "4/3", "3/4", "1", "7/4", "A", "Flip the fraction"),
        ("Which is rational?", "All of these", "Only integers", "Only decimals", "None", "A", "All can be fractions"),
        ("2/3 × 3/2 = ?", "1", "0", "1/2", "2", "A", "Reciprocals multiply to 1"),
    ],
    "Perimeter and Area": [
        ("Perimeter of rectangle is:", "2(l+b)", "l×b", "l+b", "2lb", "A", "Perimeter formula"),
        ("Area of circle is:", "πr²", "2πr", "πr", "πd", "A", "Circle area"),
        ("Circumference formula is:", "2πr", "πr²", "πr", "2r", "A", "Circle circumference"),
        ("Perimeter of square 5cm:", "20 cm", "25 cm", "10 cm", "5 cm", "A", "4×5=20"),
        ("Area measured in:", "Square units", "Linear units", "Cubic units", "Nothing", "A", "Area in squares"),
    ],
    "Algebraic Expressions": [
        ("Expression contains:", "Variables and numbers", "Only numbers", "Only letters", "Nothing", "A", "Variables+numbers"),
        ("Like terms have:", "Same variable power", "Different variables", "No relation", "None", "A", "Same variable"),
        ("3x + 5x = ?", "8x", "15x", "8", "2x", "A", "Add coefficients"),
        ("Subtract 2x from 7x:", "5x", "9x", "5", "9", "A", "7x - 2x = 5x"),
        ("Value of x if 2x = 10:", "5", "2", "10", "20", "A", "x = 10/2 = 5"),
    ],
    "Exponents and Powers": [
        ("2³ equals:", "8", "6", "4", "2", "A", "2×2×2 = 8"),
        ("10⁰ = ?", "1", "0", "10", "100", "A", "Anything to power 0 is 1"),
        ("10² × 10³ = ?", "10⁵", "10⁶", "10", "10³", "A", "Add exponents"),
        ("(2³)² = ?", "2⁶", "2⁵", "4³", "2⁹", "A", "Multiply exponents"),
        ("5⁻² = ?", "1/25", "25", "1/5", "5", "A", "Negative exponent = 1/5²"),
    ],
    "Symmetry": [
        ("Line of symmetry divides shape into:", "Two equal parts", "Three", "Four", "Unequal", "A", "Two equal parts"),
        ("Regular hexagon has:", "6 lines", "3 lines", "12 lines", "1 line", "A", "Each side = line"),
        ("Circle has:", "Infinite", "One", "Two", "Zero", "A", "Infinite = each diameter"),
        ("Rotational symmetry needs:", "Center of rotation", "Line", "Point only", "Nothing", "A", "Needs center"),
        ("Order of rotational symmetry:", "Times same in 360°", "Exactly once", "None", "Twice", "A", "Times rotate to original"),
    ],
    "Visualising Solid Shapes": [
        ("Cube has:", "6 faces", "4 faces", "8 faces", "12 faces", "A", "6 faces"),
        ("Sphere has:", "1 curved surface", "Flat faces", "No surface", "Edge", "A", "One curved surface"),
        ("Vertices of cube:", "8", "6", "12", "4", "A", "8 corners"),
        ("Edges of cube:", "12", "8", "6", "4", "A", "12 edges"),
        ("Net is:", "Unfolded 2D shape", "Volume", "Area", "Perimeter", "A", "Net = flattened shape"),
    ],
    "Congruence": [
        ("Congruent shapes are:", "Same size and shape", "Same size", "Same shape", "Different", "A", "Same size and shape"),
        ("Similar shapes are:", "Same shape but different size", "Exactly same", "Not related", "None", "A", "Same shape only"),
        ("SSS congruence means:", "Three sides equal", "Two sides", "One side", "Angles only", "A", "Three sides equal"),
        ("When figures are congruent, they can be mapped by:", "Rigid motion", "Stretching", "Breaking", "Distorting", "A", "No stretching"),
        ("Congruence means exact match:", "Yes", "No", "Sometimes", "Never", "A", "Exact = match"),
    ],
    "The Fish Tale": [
        ("This could be about:", "Marine life", "Fresh water fish", "Ocean", "Aquarium", "A", "Fish life"),
        ("Story teaches:", "Life lessons", "Nothing", "Science only", "Fun", "A", "Life lessons"),
        ("We should protect:", "Marine life", "Catch fish", "Pollute", "Ignore", "A", "Protect marine"),
        ("This chapter is from:", "English", "Hindi", "Maths", "Science", "A", "English reading"),
        ("Stories teach:", "Values", "Only vocabulary", "Grammar", "Nothing", "A", "Stories teach values"),
    ],
    "He Said It": [
        ("This is about:", "Speech and reporting", "Silence", "Actions", "Nothing", "A", "Reporting speech"),
        ("Quotation marks show:", "Someone's exact words", "Authors words", "Nothing", "General", "A", "Exact spoken words"),
        ("We should report:", "Accurately", "Wrongly", "Incompletely", "Partial", "A", "Report accurately"),
        ("Direct speech converts to:", "Indirect", "Other's speech", "Your words", "Nothing", "A", "Convert between types"),
        ("This teaches:", "Reporting skills", "Grammar", "Vocabulary", "Nothing", "A", "Reporting skills"),
    ],
    "Children at Work": [
        ("This exposes:", "Child labor issues", "Fun", "Games", "Nothing", "A", "Child labor issues"),
        ("We should protect:", "Children's rights", "Work", "Ignore", "Allow", "A", "Protect children"),
        ("Children should be:", "In school", "At work", "On streets", "Anywhere", "A", "In school"),
        ("This teaches:", "Social responsibility", "Business", "Work", "Nothing", "A", "Social responsibility"),
        ("Story shows:", "Reality of child labor", "Entertainment", "Nothing", "Fun", "A", "Child labor reality"),
    ],
    "Expert Detectives": [
        ("Detective uses:", "Logic and evidence", "Guessing", "Luck", "Nothing", "A", "Logic needed"),
        ("Solving requires:", "Careful analysis", "Random guess", "Speed", "Nothing", "A", "Analyze carefully"),
        ("We should develop:", "Observation skills", "Blind faith", "Ignorance", "Laziness", "A", "Observation skills"),
        ("This chapter teaches:", "Logic", "Sports", "Art", "Nothing", "A", "Logic and reasoning"),
        ("This is from:", "English", "Hindi", "Maths", "Science", "A", "English reading"),
    ],
    "The Selfish Giant": [
        ("This story shows:", "Selfishness changes to generosity", "Wealth", "Power", "Nothing", "A", "Selfish→generous"),
        ("Story teaches:", "Compassion", "Greed", "Anger", "Nothing", "A", "Shows compassion"),
        ("Giant learned:", "To share", "To keep", "To fight", "To ignore", "A", "Learned to share"),
        ("This is about:", "Character transformation", "War", "Peace", "Nothing", "A", "Changes to good"),
        ("We should be:", "Generous", "Selfish", "Greedy", "Careless", "A", "Be generous"),
    ],
    "Shabd Banega": [
        ("Shabd means:", "Word", "Letter", "Sentence", "Paragraph", "A", "Shabd = word"),
        ("Banega means:", "Will become", "Is", "Was", "Can", "A", "Will become word"),
        ("This is about:", "Word formation", "Building", "Letters", "Nothing", "A", "Word formation"),
        ("Hindi language includes:", "Word formation", "Only grammar", "Vocabulary", "All", "A", "All aspects"),
        ("From this we learn:", "Language skills", "Values", "Both", "Nothing", "A", "Language skills"),
    ],
    "Hariti": [
        ("Hariti is a character from:", "Buddhist legend", "History", "Mythology", "Science", "A", "Buddhist story"),
        ("This teaches:", "Compassion", "Wealth", "Power", "Nothing", "A", "Shows compassion"),
        ("We should show:", "Compassion", "Cruelty", "Anger", "Greed", "A", "Show compassion"),
        ("This chapter is about:", "Healthcare", "Wealth", "Power", "Nothing", "A", "Healthcare story"),
        ("From Hindi we learn:", "Values and language", "Only language", "Religion", "Nothing", "A", "Both language and values"),
    ],
    "The King of the Jungles": [
        ("This could be about:", "Animals and their kingdom", "Politics", "Human kingdom", "Nothing", "A", "About animals"),
        ("This teaches:", "Nature and wildlife", "History", "Politics", "Economics", "A", "Nature education"),
        ("We should protect:", "Wildlife", "Hunt", "Capture", "Ignore", "A", "Protect wildlife"),
        ("This is:", "Environmental chapter", "Story only", "Adventure", "Entertainment", "A", "Environment learning"),
        ("From this we learn:", "Conservation", "Entertainment", "Nothing", "Vocabulary only", "A", "Conservation value"),
    ],
    "Paayee Ko Saat": [
        ("Paayee means:", "Feet or legs", "Hands", "Head", "Body", "A", "Paayee = legs/feet"),
        ("Ko means:", "To", "Of", "From", "For", "A", "Ko = to"),
        ("Saat means:", "Seven", "Eight", "Six", "Nine", "A", "Saat = seven"),
        ("This could mean:", "Seven legs", "Seven feet", "To seven", "All seven", "A", "Literal meaning"),
        ("This could be about:", "Animals with seven legs", "Seven steps", "Anything", "Nothing", "A", "Various interpretations"),
    ],
    "Nasir Aamir": [
        ("Nasir Aamir could be:", "Character name", "Place", "Event", "Thing", "A", "Character in story"),
        ("This chapter is:", "About friendship", "History", "Geography", "Science", "A", "Story about friendship"),
        ("We should value:", "Friendship", "Enmity", "Separation", "Conflict", "A", "Value friendship"),
        ("This could teach:", "Unity", "Division", "Conflict", "Nothing", "A", "Unity in diversity"),
        ("From Hindi we learn:", "Language and values", "Only grammar", "Only vocabulary", "Nothing", "A", "Both combined"),
    ],
    "Kalam Ke Dhani": [
        ("Kalam means:", "Pen or writer", "Book", "Paper", "Ink", "A", "Kalam = pen"),
        ("Dhani means:", "Master or owner", "Small", "Large", "Weak", "A", "Dhani = owner/master"),
        ("This means:", "Pen master", "Book owner", "Writer skilled", "All", "A", "Skilled writer"),
        ("This teaches:", "Writing skills", "History", "Science", "Nothing", "A", "Writing improvement"),
        ("From Hindi we learn:", "Language through writing", "Grammar only", "Vocabulary only", "Nothing", "A", "Language improvement"),
    ],
    "Ek Din Ki Bhook": [
        ("Ek Din means:", "One day", "Every day", "Many days", "Never", "A", "Ek Din = one day"),
        ("Ki means:", "Of", "To", "From", "For", "A", "Ki = of"),
        ("Bhook means:", "Hunger", "Thirst", "Desire", "Wish", "A", "Bhook = hunger"),
        ("This is about:", "One day hunger", "Every day", "One time", "Nothing", "A", "One day's hunger"),
        ("This teaches:", "Value of food", "Hunger", "Appreciation", "Nothing", "A", "Food value"),
    ],
    "Pahla Kadam": [
        ("Pahla means:", "First", "Last", "Middle", "All", "A", "Pahla = first"),
        ("Kadam means:", "Step", "Leg", "Foot", "Move", "A", "Kadam = step"),
        ("This means:", "First step", "Last step", "Middle step", "Every step", "A", "First step"),
        ("This teaches:", "Beginning", "End", "Middle", "Nothing", "A", "Importance of beginning"),
        ("From Hindi we learn:", "Values", "Language", "Both", "Nothing", "A", "Both in learning"),
    ],
    "Dusri Dwar": [
        ("Dusri means:", "Second", "First", "Third", "Last", "A", "Dusri = second"),
        ("Dwar means:", "Gate or door", "Window", "Wall", "Room", "A", "Dwar = gate/door"),
        ("This means:", "Second gate", "First door", "Main entrance", "Back door", "A", "Second door/gate"),
        ("This could be about:", "Another option", "One option", "No option", "All options", "A", "Alternative"),
        ("From this we learn:", "Alternative thinking", "Only one way", "No change", "Nothing", "A", "Alternative thinking"),
    ],
    "Mere Baad": [
        ("Mere means:", "My or after", "Your", "Their", "All", "A", "Mere = my/after"),
        ("Baad means:", "After or behind", "Before", "During", "Now", "A", "Baad = after/behind"),
        ("This means:", "After me", "Before me", "With me", "My behind", "A", "My after/behind"),
        ("This is about:", "Sequence or priority", "Present", "Nothing", "Past", "A", "After or behind"),
        ("This teaches:", "Order of sequence", "First", "Priority", "Nothing", "A", "Sequence"),
    ],
}


def generate_chapter_mcq(chapter_name):
    if chapter_name in chapter_questions:
        return chapter_questions[chapter_name][:5]
    
    lower_name = chapter_name.lower()
    
    topics = {
        "Maths": [
            (f"Key in {chapter_name} is:", "Problem solving", "Memorizing", "Ignoring", "Skipping", "A", f"Solve {chapter_name}"),
            (f"{chapter_name} involves:", "Calculations", "Words", "Stories", "Nothing", "A", f"Math calculations"),
            (f"Practice {chapter_name} by:", "Solving examples", "Reading", "Memorizing", "Ignoring", "A", f"Solve examples"),
            (f"{chapter_name} uses:", "Numbers", "Only words", "Pictures", "Nothing", "A", f"Math uses numbers"),
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
        "Science": [
            (f"What does {chapter_name} teach?", "Science concepts", "Nothing", "History", "Math", "A", f"Science in {chapter_name}"),
            (f"This chapter is about:", "Science topics", "City", "Buildings", "Stories", "A", f"Science topics"),
            (f"We should learn:", "Scientific facts", "Ignore", "Memorize only", "Nothing", "A", f"Learn science"),
            (f"Chapter {chapter_name}:", "Learning", "Nothing", "Fun", "Waste", "A", f"Learn from {chapter_name}"),
            (f"Our duty from {chapter_name}:", "Apply knowledge", "Ignore", "Waste", "Nothing", "A", f"Apply science"),
        ],
    }
    
    for subject_key, qs in topics.items():
        if subject_key.lower() in lower_name:
            return qs
    
    return topics["Science"][:5]


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
print(f"Done! Generated {total} unique MCQs for Class 7")
print("="*60)