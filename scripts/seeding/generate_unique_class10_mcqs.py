import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

print("=" * 60)
print("Generating Unique MCQs for Class 10 Chapters")
print("=" * 60)

grade = Grade.objects.get(slug='class-10')
chapters = list(Chapter.objects.filter(subject__grade=grade))

chapter_questions = {
    "Real Numbers": [
        ("Euclid's division lemma states: For integers a,b there exist unique q,r such that:", "a = bq + r, 0 ≤ r < b", "a = bq", "a = b + q", "a = q + b", "A", "Division algorithm"),
        ("If 72 = 2ⁿ × 3² × 5³, then prime factors are:", "2,3,5", "3", "2,3", "Only 2", "A", "Prime factorization"),
        ("HCF(36,48) = ?", "12", "6", "24", "4", "A", "Greatest common factor = 12"),
        ("LCM(4,6) = ?", "12", "24", "2", "4", "A", "Least common multiple = 12"),
        ("√2 is:", "Irrational", "Rational", "Integer", "Whole", "A", "Cannot be expressed as fraction"),
    ],
    "Polynomials": [
        ("If (x-2) is factor of p(x), p(2) equals:", "0", "1", "2", "-2", "A", "Root = zero for factor"),
        ("Zeros of quadratic polynomial sum to:", "-b/a", "b/a", "c/a", "0", "A", "Sum = -coef ratio"),
        ("Product of zeros equals:", "c/a", "-c/a", "b/a", "0", "A", "Product = constant ratio"),
        ("x² - 5x + 6 factors as:", "(x-2)(x-3)", "(x+2)(x+3)", "(x-1)(x-6)", "x(x-6)", "A", "Find roots then factors"),
        ("Degree of polynomial is:", "Highest power of variable", "Lowest power", "Constant", "Variable", "A", "Highest exponent"),
    ],
    "Pair of Linear Equations": [
        ("System has unique solution when:", "a₁/b₁ ≠ a₂/b₂", "a₁/b₁ = a₂/b₂", "a₁b₁ = a₂b₂", "a₁+b₁ = a₂+b₂", "A", "Not parallel = unique"),
        ("Parallel lines have:", "No solution", "One solution", "Infinitely many", "Two solutions", "A", "Never meet = no solution"),
        ("Coincident lines have:", "Infinitely many solutions", "No solution", "One solution", "Zero solutions", "A", "Same line = infinite"),
        ("Substitution method solves by:", "Expressing one variable in terms of other", "Adding equations", "Multiplying", "Dividing", "A", "Isolate and substitute"),
        ("Cross multiplication applies to form:", "a₁x + b₁y + c₁ = 0 / a₂x + b₂y + c₂ = 0", "One equation", "Three equations", "Not linear", "A", "Requires both linear"),
    ],
    "Quadratic Equations": [
        ("Standard form: ax² + bx + c = 0 where a ≠", "0", "1", "2", "-1", "A", "a cannot be zero"),
        ("Discriminant b² - 4ac determines:", "Nature of roots", "Value of roots", "Sum of roots", "Nothing", "A", "Shows root type"),
        ("If discriminant > 0, roots are:", "Real and unequal", "Real and equal", "Not real", "Equal only", "A", "Two different real roots"),
        ("If discriminant = 0, roots are:", "Real and equal", "Real and unequal", "Not real", "Imaginary", "A", "Both same"),
        ("x² - 7x + 12 = 0 gives x equals:", "3, 4", "2, 6", "-3, -4", "1, 12", "A", "Factor and solve"),
    ],
    "Arithmetic Progressions": [
        ("AP has constant:", "Common difference", "Common ratio", "Constant sum", "Nothing", "A", "Constant difference d"),
        ("nth term formula: aₙ = a + (n-1)d, where n is:", "Term number", "Value", "Common diff", "First term", "A", "n = position"),
        ("Sum of n terms: Sₙ = n/2[2a + (n-1)d], n is:", "Number of terms", "First term", "Difference", "Nothing", "A", "n = count"),
        ("If a = 2, d = 3, S₅ equals:", "40", "30", "50", "45", "A", "Sum of first 5 terms"),
        ("For consecutive terms, d equals:", "Constant difference", "0", "Variable", "Nothing", "A", "Same value throughout"),
    ],
    "Triangles": [
        ("Similar triangles have:", "Equal corresponding angles", "Sides in ratio", "Not equal", "Different angles", "A", "Angles equal, sides proportional"),
        ("If ΔABC ~ ΔDEF, ratio AB/DE equals:", "Perimeter ratio", "Area ratio", "No relation", "Half", "A", "Corresponding sides ratio"),
        ("Pythagorean theorem: In right triangle, c² = a² + b², where c is:", "Hypotenuse", "Base", "Altitude", "Nothing", "A", "Hypotenuse largest side"),
        ("AA similarity states:", "Two angles equal", "Two sides proportional", "Three sides equal", "Nothing", "A", "Two angles equal = similar"),
        ("If ΔABC and ΔPQR are similar, angles correspond:", "Match exactly", "Any order", "Opposite", "Different", "A", "Same position equals similar"),
    ],
    "Coordinate Geometry": [
        ("Distance formula: d = √[(x₂-x₁)² + (y₂-y₁)²], where x's are:", "x-coordinates", "y-coordinates", "Slopes", "Nothing", "A", "Compute x difference"),
        ("Midpoint of (x₁,y₁) and (x₂,y₂) equals:", "((x₁+x₂)/2, (y₁+y₂)/2)", "(x₁+x₂, y₁+y₂)", "Difference", "Nothing", "A", "Average of coordinates"),
        ("Section formula for internal division: ( (mx₂+nx₁)/(m+n), (my₂+ny₁)/(m+n) ), m:n is:", "Ratio of division", "Slope", "Distance", "Nothing", "A", "Parts ratio"),
        ("Area of triangle with vertices formula:", "1/2|x₁(y₂-y₃) + x₂(y₃-y₁) + x₃(y₁-y₂)|", "Sum of coordinates", "Product", "Nothing", "A", "Coordinate formula"),
        ("Slope of line ax + by + c = 0 equals:", "-a/b", "a/b", "c/b", "-b/a", "A", "Negative coefficient ratio"),
    ],
    "Introduction to Trigonometry": [
        ("In right triangle, sinθ = opposite/hypotenuse, θ is:", "Angle considered", "Side", "Right angle", "Nothing", "A", "θ = acute angle"),
        ("cosθ equals:", "Adjacent/hypotenuse", "Opposite/adjacent", "Opposite/hypotenuse", "Hypotenuse/opposite", "A", "cos = adjacent/hypotenuse"),
        ("tanθ equals:", "Opposite/adjacent", "Adjacent/opposite", "Opposite/hypotenuse", "Hypotenuse/opposite", "A", "tan = opposite/adjacent"),
        ("sin(90°-θ) equals:", "cosθ", "sinθ", "1-sinθ", "sin²θ", "A", "Co-function identity"),
        ("If sin A = 3/5, cos A equals:", "4/5", "5/3", "3/4", "5/4", "A", "Pythagorean gives cos = 4/5"),
    ],
    "Some Applications of Trigonometry": [
        ("Height and distance problems use:", "Right triangles", "Any triangle", "Circles", "Nothing", "A", "Right triangle model"),
        ("Angle of elevation forms from:", "Eye to object above", "Object to eye", "Horizontal", "Vertical", "A", "Looking up = elevation"),
        ("Angle of depression forms from:", "Eye to object below", "Object to eye", "Eye horizontally", "Nothing", "A", "Looking down = depression"),
        ("Line of sight forms:", "Right triangle with horizontal", "Circle", "Diagonal", "Nothing", "A", "Eye to object line"),
        ("To find height, we use trigonometric ratios:", "tan or sin", "Only sin", "Cos only", "Nothing", "A", "Depending on angle type"),
    ],
    "Circles": [
        ("Circle is set of points at:", "Fixed distance from center", "Varying distance", "Inside", "Nothing", "A", "Constant radius"),
        ("Tangent touches circle at:", "One point", "Two points", "Three points", "Nothing", "A", "One point of contact"),
        ("Angle in semicircle equals:", "90 degrees", "180 degrees", "45 degrees", "0", "A", "Right angle property"),
        ("From external point, tangents to circle:", "Have equal length", "Different lengths", "Infinite", "Impossible", "A", "Equal tangents theorem"),
        ("If two chords intersect inside circle, products equal:", "Product of segments", "Sum", "Difference", "Nothing", "A", "Intersecting chords theorem"),
    ],
    "Areas Related to Circles": [
        ("Circumference of circle equals:", "2πr", "πr²", "πr", "2r", "A", "Perimeter formula = 2πr"),
        ("Area of circle equals:", "πr²", "πr", "2πr", "πr²/2", "A", "Area formula = πr²"),
        ("Length of arc equals:", "θ/360 × 2πr", "θ × r", "θπr", "Nothing", "A", "Arc length formula"),
        ("Area of sector equals:", "θ/360 × πr²", "θr²", "πrθ", "Something else", "A", "Sector area formula"),
        ("Segment area equals:", "Sector - Triangle", "Sector + Triangle", "Triangle only", "Nothing", "A", "Segment below arc"),
    ],
    "Surface Areas and Volumes": [
        ("Surface area of cuboid is:", "2(lb + bh + hl)", "lb + bh", "lw + bh", "lb + lw", "A", "All faces sum"),
        ("Volume of cylinder equals:", "πr²h", "πr²", "2πrh", "πr²h/2", "A", "πr²h = cylinder"),
        ("Sphere surface area equals:", "4πr²", "πr²", "4πr", "2πr²", "A", "Constant × r²"),
        ("Cone volume equals:", "(1/3)πr²h", "πr²h", "πr²", "2πrh", "A", "One-third of cylinder"),
        ("Hollow sphere has inner and outer radius, volume equals:", "4/3π(R³-r³)", "4π(R²-r²)", "4π(R-r)", "Nothing", "A", "Sphere shell formula"),
    ],
    "Statistics": [
        ("Mean of grouped data uses:", "Class mark × frequency", "Only frequency", "Class boundaries", "Nothing", "A", "Midpoint × freq"),
        ("To find mode, check:", "Highest frequency class", "Lowest frequency", "Mean", "Nothing", "A", "Mode in frequency"),
        ("Median formula: L + (n/2 - cf) × h/f, where L is:", "Lower class boundary", "Upper boundary", "Class mark", "Midpoint", "A", "Median class lower"),
        ("Standard deviation measures:", "Spread of data", "Central value", "Range", "Mode only", "A", "Variation from mean"),
        ("Cumulative frequency shows:", "Running total", "Highest value", "Lowest value", "Nothing", "A", "Adding frequencies"),
    ],
    "Probability": [
        ("Probability ranges between:", "0 and 1", "1 and 10", "-1 to 1", "Any number", "A", "0 ≤ P ≤ 1"),
        ("P(E) + P(Ē) equals:", "1", "0", "2", "-1", "A", "Event + complement = 1"),
        ("Mutually exclusive events:", "Cannot happen together", "Can happen together", "Related", "Nothing", "A", "No overlap"),
        ("If P(A) = 1/3, P(B) = 1/2, P(A∪B) = ?:", "Sum if independent", "Sum always", "Product", "Nothing", "A", "Addition rule if exclusive"),
        ("Odds in favor = P(success)/P(failure), expressed as:", "a:b", "a+b", "a × b", "Nothing", "A", "Ratio form"),
    ],
    "Chemical Reactions and Equations": [
        ("Skeletal equation shows:", "Formulas only", "Values", "Nothing", "Coefficients", "A", "Chemicals not balanced"),
        ("Balanced equation satisfies:", "Mass conservation", "Volume", "Nothing", "Pressure", "A", "Atoms equal on both sides"),
        ("Combination reaction: A + B → AB, type:", "Two or more combine", "One splits", "Oxygen transfer", "Nothing", "A", "A+B=AB"),
        ("Decomposition: AB → A + B, needs:", "Energy input", "Nothing", "Catalyst", "Nothing", "A", "Breakdown needs energy"),
        ("Oxidation involves:", "Gain of oxygen/loss of electrons", "Nothing", "Loss of oxygen", "Nothing", "A", "Oxidation definition"),
    ],
    "Acids, Bases and Salts": [
        ("Acids have pH less than:", "7", "14", "0", "1", "A", "Less than 7 acidic"),
        ("Bases have pH greater than:", "7", "0", "14", "1", "A", "More than 7 = basic"),
        ("Universal indicator shows:", "Full pH range", "Only acid", "Only base", "Nothing", "A", "Multiple colors"),
        ("Salt is formed from:", "Acid + base", "Acid + acid", "Base + base", "Water only", "A", "Neutralization product"),
        ("Bleaching powder formula: CaOCl₂, contains:", "Chlorine", "Oxygen", "Nothing", "Carbon", "A", "Active chlorine"),
    ],
    "Metals and Non-Metals": [
        ("Metals are generally:", "Good conductors", "Insulators", "Neither", "Semiconductors", "A", "Conduct heat/electricity"),
        ("Gold is:", "Least reactive", "Most reactive", "Reactive", "Amphoteric", "A", "Gold doesn't react easily"),
        ("Ionic compounds are:", "Soluble in water", "Insoluble", "Covalent", "Nothing", "A", "Dissolve as ions"),
        ("Non-metals generally form:", "Covalent bonds", "Ionic bonds", "Metallic bonds", "Nothing", "A", "Share electrons"),
        ("Aluminium is:", "More reactive than iron", "Less reactive", "Non-reactive", "None", "A", "More reactive in series"),
    ],
    "Carbon and its Compounds": [
        ("Carbon has unique property:", "Catenation", "Ionization", "Nothing", "Metallic", "A", "Carbon bonds to carbon"),
        ("Saturated compounds have:", "Single bonds only", "Double bonds", "Triple bonds", "All of above", "A", "Single = saturated"),
        ("Unsaturated have:", "Double or triple bonds", "Single bonds only", "No bonds", "All single", "A", "Double/triple = unsaturated"),
        ("Ethanol reaction with Na produces:", "Sodium ethoxide + H₂", "Salt only", "Acid only", "Nothing", "A", "Hydrogen gas released"),
        ("Acetic acid is found in:", "Vinegar", "Sugar", "Salt", "Nothing", "A", "Acetic = vinegar"),
    ],
    "Periodic Classification of Elements": [
        ("Modern periodic law: properties repeat periodically with:", "Atomic number", "Atomic mass", "Electrons", "Nothing", "A", "Atomic number = basis"),
        ("Periods are:", "Horizontal rows", "Vertical columns", "Groups", "Blocks", "A", "Left to right rows"),
        ("Groups show:", "Similar properties", "Different properties", "Nothing", "Similar size", "A", "Same electron = similar"),
        ("Metals are on:", "Left and center", "Right", "Middle", "Edges only", "A", "Mostly left side"),
        ("Atomic size increases down group because:", "Electrons added in higher shells", "Shells decrease", "Protons decrease", "Nothing", "A", "More shells = larger"),
    ],
    "Life Processes": [
        ("Nutrition involves:", "Getting and using food", "Breathing", "Moving", "Nothing", "A", "Food-related functions"),
        ("Respiration releases:", "Energy", "Water", "CO₂ only", "Nothing", "A", "Releases energy from food"),
        ("Blood carries:", "Oxygen and nutrients", "Only oxygen", "Only nutrients", "Nothing", "A", "Transport medium"),
        ("Kidneys filter:", "Waste from blood", "Food", "Air", "Nothing", "A", "Remove waste products"),
        ("Veins carry blood:", "Towards heart", "Away from heart", "Nothing", "Same direction", "A", "Veins toward heart"),
    ],
    "Control and Coordination": [
        ("Nervous system uses:", "Electrical impulses", "Chemicals only", "Nothing", "Both only", "A", "Electrical + chemical signals"),
        ("Reflex action is:", "Automatic response", "Thoughtful action", "Voluntary", "Nothing", "A", "Quick automatic"),
        ("Synapse is:", "Nerve junction", "Nerve end", "Nerve cell", "Nothing", "A", "Signal transfer point"),
        ("Plant hormones control:", "Growth and responses", "Reproduction", "Food making", "Nothing", "A", "Growth responses"),
        ("Insulin regulates:", "Blood sugar", "Blood pressure", "Heart rate", "Nothing", "A", "Sugar level"),
    ],
    "Heredity and Evolution": [
        ("Heredity is transfer of:", "Traits from parents", "Only genes", "Nothing", "Cells", "A", "Parent to offspring"),
        ("DNA carries:", "Genetic information", "Energy", "Nothing", "Proteins", "A", "Genetic code"),
        ("Variation occurs due to:", "Mutations and recombination", "One reason", "Nothing", "No reason", "A", "Random changes + mixing"),
        ("Evolution shows:", "Change in species over time", "No change", "All at once", "Nothing", "A", "Gradual species change"),
        ("Fossils provide:", "Evidence of past life", "Nothing", "Modern life", "Nothing", "A", "Past organism evidence"),
    ],
    "Our Environment": [
        ("Ecosystem includes:", "Living and non-living", "Only living", "Only non-living", "Nothing", "A", "Both interact"),
        ("Food chain shows:", "Energy transfer", "Nothing", "One direction", "All directions", "A", "Energy flow"),
        ("Decomposers:", "Break down dead matter", "Make food", "Nothing", "Use oxygen", "A", "Recycle nutrients"),
        ("Bioamplification increases:", "Toxin concentration upward", "Energy upward", "Nothing", "Lesser upward", "A", "Toxins accumulate"),
        ("We should reduce:", "Pollution", "Nothing", "Development", "Nothing", "A", "Minimize waste"),
    ],
    "Sources of Energy": [
        ("Solar energy is:", "Renewable", "Non-renewable", "Finite", "Nothing", "A", "Sun infinite for practical"),
        ("Fossil fuels are:", "Non-renewable", "Renewable", "Unlimited", "Infinite", "A", "Take long to form"),
        ("Nuclear energy uses:", "Fission or fusion", "Burning", "Chemical reaction", "Nothing", "A", "Nuclear reactions"),
        ("Green energy sources:", "Wind, solar, hydro", "Coal", "Petroleum", "Natural gas", "A", "Renewable options"),
        ("Tidal energy based on:", "Moon's gravity", "Sun's heat", "Nothing", "Earth's rotation", "A", "Tidal movements"),
    ],
    "The Story of Progress": [
        ("This chapter shows:", "Development over time", "Problems", "Nothing", "Stagnation", "A", "Historical progress"),
        ("Development includes:", "Social, economic, scientific", "Only financial", "Nothing", "Personal", "A", "Many aspects"),
        ("Progress requires:", "Science and values", "Nothing", "Luck", "Only money", "A", "Wisdom + change"),
        ("History teaches:", "From past experiences", "Nothing", "Just dates", "Entertainment", "A", "Learn from past"),
        ("This is from:", "English", "Hindi", "Maths", "Science", "A", "English reading"),
    ],
    "A Letter to God": [
        ("This story is about:", "Hope and faith", "Complaining", "Success", "Nothing", "A", "Hope against odds"),
        ("Best gift is:", "Food for the poor", "Wealth", "Nothing", "Entertainment", "A", "Essential = food"),
        ("We should help:", "Those in need", "Rich", "Friends", "Nothing", "A", "Help the poor"),
        ("Story teaches:", "Compassion", "Greed", "Anger", "Nothing", "A", "Teach compassion"),
        ("This is from:", "English", "Hindi", "Maths", "Science", "A", "English chapter"),
    ],
    "The Proposal": [
        ("This could be a story about:", "Proposal and hope", "Rejection", "Nothing", "Failure", "A", "Hope for acceptance"),
        ("Dialogue shows:", "Character and intent", "Compliments", "Nothing", "Anger", "A", "Reveals intent"),
        ("Story should teach:", "Proper behavior", "Rudeness", "Disrespect", "Nothing", "A", "Proper manners"),
        ("This is from:", "English", "Hindi", "Maths", "Science", "A", "English reading"),
    ],
    "Do Bailon Ki Katha": [
        ("Do Bailon means:", "Two bullocks", "One bullock", "Three bullocks", "Four bullocks", "A", "Do = two"),
        ("Ki means:", "Of", "With", "To", "For", "A", "Ki = of"),
        ("Katha means:", "Story", "Work", "Journey", "Nothing", "A", "Katha = story"),
        ("This could be:", "Story about two oxen", "Two animals", "Journey", "Work", "A", "Story about two oxen"),
        ("This is from:", "Hindi", "English", "Maths", "Science", "A", "Hindi chapter"),
    ],
    "Sanskrit Shloka": [
        ("Shloka is:", "Sanskrit verse", "Prose", "Nothing", "Prayer", "A", "Sanskrit verse form"),
        ("Sanskrit is:", "Ancient language", "Modern", "Regional", "Nothing", "A", "Classical language"),
        ("Shloka teaches:", "Wisdom", "History", "Nothing", "Values", "A", "Moral wisdom"),
        ("We should learn from:", "Wisdom of ancient", "Nothing", "Only grammar", "Memorize", "A", "Ancient wisdom"),
        ("This is from:", "Sanskrit", "English", "Hindi", "Maths", "A", "Sanskrit subject"),
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
            (f"{chapter_name} uses:", "_numbers and formulas", "Only words", "Pictures", "Nothing", "A", f"Math formulas"),
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
print(f"Done! Generated {total} unique MCQs for Class 10")
print("="*60)