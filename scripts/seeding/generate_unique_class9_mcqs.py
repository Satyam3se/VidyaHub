import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

print("=" * 60)
print("Generating Unique MCQs for Class 9 Chapters")
print("=" * 60)

grade = Grade.objects.get(slug='class-9')
chapters = list(Chapter.objects.filter(subject__grade=grade))

chapter_questions = {
    "Number Systems": [
        ("Every rational number can be expressed as:", "Terminating or repeating decimal", "Only terminating", "Only repeating", "Never", "A", "Rational = decimal form"),
        ("Irrational numbers cannot be expressed as:", "Terminating or repeating decimal", "Whole number", "Integer", "Fraction", "A", "Irrational = non-repeating"),
        ("√2 is:", "Irrational", "Rational", "Integer", "Whole", "A", "Cannot write as fraction"),
        ("Decimal expansion of 3/8 is:", "Terminating", "Repeating", "Non-terminating", "None", "A", "3÷8 = 0.375"),
        ("The set of real numbers includes:", "Rational and irrational", "Only rational", "Only irrational", "Integers only", "A", "Real = rational + irrational"),
    ],
    "Polynomials": [
        ("Polynomial of degree 2 is called:", "Quadratic", "Linear", "Cubic", "Constant", "A", "Degree 2 = quadratic"),
        ("Zero of polynomial is where:", "Polynomial equals zero", "Value is maximum", "Value is minimum", "Nothing", "A", "Root/zero = value = 0"),
        ("Factor theorem states: If (x-a) is factor, then p(a) equals:", "0", "1", "-1", "a", "A", "Substitute gives 0"),
        ("(x+y)² equals:", "x² + 2xy + y²", "x² + y²", "x² - 2xy + y²", "x² + xy + y²", "A", "(x+y)² formula"),
        ("Area of rectangle represents:", "Product of length × breadth", "Sum", "Difference", "Nothing", "A", "Area = multiplication"),
    ],
    "Coordinate Geometry": [
        ("Coordinate geometry uses:", "x and y coordinates", "Only x", "Only y", "Nothing", "A", "Coordinates = (x,y)"),
        ("x-axis is:", "Horizontal", "Vertical", "Diagonal", "Circular", "A", "Horizontal = x-axis"),
        ("y-axis is:", "Vertical", "Horizontal", "Diagonal", "Circle", "A", "Vertical = y-axis"),
        ("Quadrants are:", "Four regions", "Two regions", "Six regions", "Three regions", "A", "Four quadrants"),
        ("Midpoint of (x1,y1) and (x2,y2) is:", "((x1+x2)/2, (y1+y2)/2)", "(x1+x2, y1+y2)", "(x1-x2, y1-y2)", "Anything else", "A", "Midpoint formula"),
    ],
    "Linear Equations in Two Variables": [
        ("Linear equation in two variables has:", "Degree 1", "Degree 2", "Degree 0", "None", "A", "Highest power = 1"),
        ("Solution satisfies:", "Equation", "Nothing", "One variable only", "All", "A", "Make equation true"),
        ("Graph of ax + by + c = 0 is:", "Straight line", "Curve", "Parabola", "Circle", "A", "Linear = straight line"),
        ("Lines that never meet are:", "Parallel", "Perpendicular", "Intersecting", "Same", "A", "Parallel never meet"),
        ("System of equations can be solved by:", "Graphical or algebraic method", "One way only", "Only graphically", "Nothing", "A", "Multiple methods exist"),
    ],
    "Introduction to Euclid's Geometry": [
        ("Euclid gave:", "Axioms and postulates", "Formulas only", "Theorems only", "Nothing", "A", "Basic truths axioms"),
        ("Postulate is:", "Accepted without proof", "Needs proof", "Disproved", "None", "A", "Accept without proof"),
        ("Axiom is:", "Common notion", "Complex statement", "Problem", "Nothing", "A", "Common sense truths"),
        ("Euclid's fifth postulate deals with:", "Parallel lines", "Circles", "Triangles", "Angles", "A", "Parallel lines"),
        ("Theorems need:", "Proof", "No proof", "Assumption", "Nothing", "A", "Proven statements"),
    ],
    "Lines and Angles": [
        ("Angle sum in triangle equals:", "180 degrees", "360 degrees", "90 degrees", "0", "A", "Triangle = 180°"),
        ("Vertically opposite angles are:", "Equal", "Complementary", "Supplementary", "Different", "A", "Equal angles"),
        ("Exterior angle equals:", "Sum of two opposite interior angles", "One interior", "Nothing", "Half", "A", "Exterior = sum interior"),
        ("Corresponding angles are equal when:", "Lines are parallel", "Lines intersect", "Lines are perpendicular", "Nothing", "A", "Parallel gives equal"),
        ("Sum of angles on straight line is:", "180 degrees", "360 degrees", "90 degrees", "45 degrees", "A", "Straight = 180°"),
    ],
    "Triangles": [
        ("Triangle has:", "3 sides and 3 angles", "4 sides", "2 sides", "None", "A", "3 = triangle"),
        ("SSS congruence requires:", "Three sides equal", "Two sides", "One side", "Angles only", "A", "Three sides equal"),
        ("ASA congruence requires:", "Two angles and side", "Two sides", "Three angles", "Nothing", "A", "Angles + side"),
        ("Isosceles triangle has:", "Two equal sides", "All equal", "No equal", "Three equal", "A", "Two equal sides"),
        ("Pythagoras theorem applies to:", "Right triangle", "Any triangle", "Equilateral", "Isosceles", "A", "Right triangle only"),
    ],
    "Quadrilaterals": [
        ("Quadrilateral has:", "4 sides and 4 angles", "3 sides", "5 sides", "None", "A", "Four = quadrilateral"),
        ("Sum of interior angles:", "360 degrees", "180 degrees", "720 degrees", "0", "A", "Quadrilateral = 360°"),
        ("Parallelogram has:", "Both pairs parallel", "One pair parallel", "No pair", "All equal", "A", "Both pairs parallel"),
        ("Rectangle's diagonals are:", "Equal", "Unequal", "One diagonal", "Nothing", "A", "Equal = rectangle"),
        ("Rhombus is special type of:", "Parallelogram", "Trapezium", "Kite", "Square", "A", "Has parallelogram properties"),
    ],
    "Areas of Parallelograms and Triangles": [
        ("Area of parallelogram equals:", "Base × height", "Side × side", "Perimeter", "Nothing", "A", "Formula = b×h"),
        ("Triangle area is:", "½ × base × height", "Base × height", "Twice base × height", "Sum", "A", "Triangle = ½ × parallelogram"),
        ("Figures on same base and between same parallels have:", "Equal area", "Different", "Sum", "Nothing", "A", "Equal when related"),
        ("Congruent figures have:", "Equal area", "Different area", "No relation", "Nothing", "A", "Equal = congruent"),
        ("Area of triangle can be found by:", "Using Heron's formula", "Only base-height", "Only coordinates", "Nothing", "A", "Heron's formula exists"),
    ],
    "Circles": [
        ("Circle is set of points at:", "Fixed distance from center", "Varying distance", "Inside center", "Nothing", "A", "Constant radius"),
        ("Chord passes through:", "Center", "Outside center", "Never through", "Anywhere", "A", "Diameter passes center"),
        ("Tangent touches circle at:", "One point", "Two points", "Three points", "Nothing", "A", "One point = tangent"),
        ("Angle in semicircle is:", "90 degrees", "180 degrees", "45 degrees", "0", "A", "Right angle = semicircle"),
        ("Two chords equal when:", "Equidistant from center", "Same length", "Nothing", "Different", "A", "Equal distance = equal chords"),
    ],
    "Constructions": [
        ("Construction uses:", "Ruler and compass only", "Protractor", "Transportor only", "Nothing", "A", "Limited tools"),
        ("To construct triangle, we need:", "Three measurements", "Two", "Angles only", "One", "A", "SSS/ASA/SAS"),
        ("Angle bisector divides angle into:", "Two equal parts", "Three parts", "Four parts", "One", "A", "Equal angles"),
        ("Perpendicular bisector goes through:", "Midpoint at right angle", "Any point", "Vertex only", "Nothing", "A", "Perpendicular at midpoint"),
        ("Construction requires:", "Precision and steps", "Guessing", "Accuracy not needed", "Nothing", "A", "Follow steps exactly"),
    ],
    "Heron's Formula": [
        ("Heron's formula uses:", "Semi-perimeter", "Perimeter", "Base only", "Height only", "A", "Semi = s = p/2"),
        ("Area equals √[s(s-a)(s-b)(s-c)] where s is:", "Semi-perimeter", "Perimeter", "Half area", "Nothing", "A", "s = semi-perimeter"),
        ("This formula is for:", "Triangle", "Square", "Circle", "Rectangle", "A", "Triangle only"),
        ("Area of triangle can be found if sides known:", "Yes", "No", "Sometimes", "Never", "A", "Heron finds with sides"),
        ("If sides are 5,6,7, then semi-perimeter is:", "9", "18", "3", "4.5", "A", "(5+6+7)/2 = 9"),
    ],
    "Surface Areas and Volumes": [
        ("Surface area of cube is:", "6a²", "4a²", "a²", "a³", "A", "6×side² = cube SA"),
        ("Total surface area of cuboid is:", "2(lb + bh + hl)", "lb + bh + hl", "4(lb + bh)", "Anything else", "A", "All faces sum"),
        ("Volume of cube is:", "a³", "a²", "6a²", "4a²", "A", "a³ = cube volume"),
        ("Sphere's surface area is:", "4πr²", "4πr", "πr²", "2πr²", "A", "4πr² = sphere SA"),
        ("Cylinder's volume equals:", "πr²h", "πrh", "2πr²", "πr²", "A", "πr²h = cylinder"),
    ],
    "Statistics": [
        ("Statistics deals with:", "Data collection and interpretation", "Only collection", "Only numbers", "Nothing", "A", "Collect and interpret"),
        ("Mean is:", "Average", "Middle value", "Most frequent", "Range", "A", "Mean = sum/count"),
        ("Mode is:", "Most frequent value", "Middle value", "Average", "Difference", "A", "Mode = most frequent"),
        ("Median is:", "Middle value when arranged", "Most frequent", "Average", "Range", "A", "Arrange then middle"),
        ("Class interval in grouped data is:", "Group of values", "Single value", "Nothing", "One class", "A", "Grouping creates classes"),
    ],
    "Probability": [
        ("Probability ranges from:", "0 to 1", "1 to 10", "-1 to 1", "Any value", "A", "0 ≤ P ≤ 1"),
        ("Favorable outcomes divided by:", "Total outcomes", "Some outcomes", "Nothing", "All", "A", "P = favorable/total"),
        ("Probability of impossible event is:", "0", "1", "1/2", "Any", "A", "Impossible = 0"),
        ("Probability of certain event is:", "1", "0", "1/2", "Any", "A", "Certain = 1"),
        ("Experimental probability is based on:", "Actual trials", "Theoretical only", "Nothing", "Assumptions", "A", "From real experiments"),
    ],
    "Matter in Our Surroundings": [
        ("Matter is made of:", "Particles", "Only atoms", "Nothing", "Space", "A", "Particles = matter"),
        ("States of matter are:", "Solid, liquid, gas", "Only solid", "Only liquid", "Two only", "A", "Three states"),
        ("Particle motion differs in:", "Solids least, gases most", "Equal", "No motion", "Varies randomly", "A", "Solid < liquid < gas"),
        ("Diffusion is faster in:", "Gases", "Liquids", "Solids", "Equal", "A", "Gas particles move fastest"),
        ("Brownian motion shows:", "Random particle movement", "Straight motion", "No movement", "Fixed path", "A", "Random zigzag"),
    ],
    "Is Matter Around Us Pure": [
        ("Pure substance has:", "Fixed composition", "Variable composition", "Mixture", "Nothing", "A", "Pure = single substance"),
        ("Mixture contains:", "Two or more substances", "One substance", "Nothing", "One element", "A", "Multiple = mixture"),
        ("Filtration separates:", "Solid from liquid", "Liquid from liquid", "Gases", "Nothing", "A", "Solid retained on filter"),
        ("Distillation separates:", "Liquids with different boiling points", "Same boiling", "Solids", "Gases", "A", "Based on boiling points"),
        ("Chromatography separates:", "Based on solubility", "Boiling point", "Density", "Nothing", "A", "Different solubilities"),
    ],
    "Atoms and Molecules": [
        ("Atom is:", "Smallest unit of matter", "Collection", "Nothing", "Complex", "A", "Atom = smallest unit"),
        ("Molecule is:", "Group of atoms bonded together", "Single atom", "Nothing", "Smaller than atom", "A", "Atoms bonded = molecule"),
        ("Atomic mass is mass of:", "Protons and neutrons", "Electrons only", "Only protons", "Nothing", "A", "Nucleus mass"),
        ("Chemical formula shows:", "Elements and proportions", "Only elements", "Nothing", "Numbers", "A", "Shows composition"),
        ("Ion forms when:", "Atoms gain or lose electrons", "Always gain", "Nothing", "Share only", "A", "Electron transfer = ion"),
    ],
    "Structure of the Atom": [
        ("Atom consists of:", "Nucleus and electrons", "Only nucleus", "Nothing", "Electrons only", "A", "Central + orbiting"),
        ("Nucleus contains:", "Protons and neutrons", "Electrons only", "Nothing", "Only protons", "A", "Protons + neutrons"),
        ("Electrons are:", "Outside nucleus", "Inside", "Nowhere", "Part of nucleus", "A", "Orbit = electrons"),
        ("Atomic number equals:", "Number of protons", "Number of neutrons", "Mass number", "Electrons only", "A", "Z = number of protons"),
        ("Isotopes have:", "Same protons, different neutrons", "Different protons", "Same neutrons", "Nothing", "A", "Same element = same Z"),
    ],
    "The Fun They Had": [
        ("This story is about:", "Future education", "Past education", "Current education", "Nothing", "A", "Future schooling"),
        ("This shows:", "Technology in education", "Problems", "Nothing", "Disadvantages only", "A", "Tech in learning"),
        ("Story compares:", "Traditional vs technology", "Only traditional", "Only technology", "Nothing", "A", "Comparison"),
        ("We should use technology:", "Wisely", "Completely", "Not at all", "Without limits", "A", "Balance needed"),
        ("This is from:", "English", "Hindi", "Maths", "Science", "A", "English reading"),
    ],
    "The Sound of Music": [
        ("This story is about:", "Music and passion", "Science", "Nothing", "Entertainment", "A", "Musical passion"),
        ("Following your passion requires:", "Dedication", "Nothing", "Less effort", "Luck", "A", "Dedication = success"),
        ("Story shows examples of:", "Musical journey", "Science only", "Nothing", "Problems", "A", "Pursuit of passion"),
        ("We should develop:", "Our talents", "Only studies", "Nothing", "Follow crowds", "A", "Develop talents"),
        ("This is from:", "English", "Hindi", "Maths", "Science", "A", "English chapter"),
    ],
    "The French Revolution": [
        ("French Revolution was in:", "1789", "1776", "1799", "1800", "A", "1789 French Revolution"),
        ("Causes included:", "Inequality and taxes", "Nothing", "Foreign attack", "Prosperity", "A", "Social inequality"),
        ("It led to:", "End of monarchy", "Weaker monarchy", "Stronger monarchy", "Nothing", "A", "France became republic"),
        ("This is part of:", "History", "Science", "Geography", "Nothing", "A", "Historical event"),
        ("We learn about:", "Past events and lessons", "Nothing", "Just dates", "Entertainment", "A", "Learn from history"),
    ],
    "Nazism and the Rise of Hitler": [
        ("Hitler rose in:", "Germany", "Italy", "France", "Russia", "A", "Germany 1930s"),
        ("Nazism spread through:", "Propaganda and promises", "Nothing", "Peace", "Democracy", "A", "Used propaganda"),
        ("This led to:", "World War II", "Peace", "Nothing", "Prosperity", "A", "Caused WWII"),
        ("We should prevent such ideology by:", "Education and awareness", "Nothing", "Ignoring", "Following", "A", "Through education"),
        ("This is from:", "History/Social Science", "English", "Maths", "Science", "A", "History chapter"),
    ],
    "Do Bailon Ki Katha": [
        ("Do Bailon means:", "Two bullocks", "One bullock", "Three bullocks", "Four bullocks", "A", "Do = two, bail = bullock"),
        ("Ki means:", "Of", "With", "To", "For", "A", "Ki = of"),
        ("Katha means:", "Story or tale", "Work", "Journey", "Nothing", "A", "Katha = story"),
        ("Do Bailon Ki Katha could mean:", "Story of two bullocks", "Two animals", "Work story", "Journey", "A", "Story about two oxen"),
        ("This is from:", "Hindi", "English", "Maths", "Science", "A", "Hindi chapter"),
    ],
    "Lhasa Ki Aur": [
        ("Lhasa is:", "Capital of Tibet", "Indian city", "Nepal city", "Bhutan city", "A", "Lhasa = Tibet capital"),
        ("Ki means:", "Of", "With", "To", "For", "A", "Ki = of"),
        ("Aur means:", "And", "Towards", "From", "For", "A", "Aur = and"),
        ("Lhasa ki aur could mean:", "Towards Lhasa", "From Lhasa", "Lhasa's", "In Lhasa", "A", "Direction toward Lhasa"),
        ("This is from:", "Hindi", "English", "Maths", "Science", "A", "Hindi chapter"),
    ],
    "Poem: Rain on the Roof": [
        ("This poem is about:", "Rain", "Sun", "Snow", "Wind", "A", "Rain is theme"),
        ("Poem uses imagery of:", "Rain falling on roof", "Sunny day", "Winter", "Nothing", "A", "Visual imagery"),
        ("Poem shows:", "Peaceful feeling", "Sadness", "Anger", "Nothing", "A", "Mood peaceful"),
        ("We should appreciate:", "Nature's beauty", "Nothing", "Urban life", "Nothing", "A", "Nature appreciation"),
        ("This is from:", "English", "Hindi", "Maths", "Science", "A", "English poetry"),
    ],
}


def generate_chapter_mcq(chapter_name):
    if chapter_name in chapter_questions:
        return chapter_questions[chapter_name][:5]
    
    lower_name = chapter_name.lower()
    
    topics = {
        "Maths": [
            (f"Key concept in {chapter_name}:", "Problem solving", "Memorizing", "Ignoring", "Skipping", "A", f"Solve {chapter_name}"),
            (f"{chapter_name} involves:", "Calculations", "Words", "Stories", "Nothing", "A", f"Math calculations"),
            (f"Practice {chapter_name}:", "Solving examples", "Reading", "Memorizing", "Ignoring", "A", f"Solve examples"),
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
print(f"Done! Generated {total} unique MCQs for Class 9")
print("="*60)