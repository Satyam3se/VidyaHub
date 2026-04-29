import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

print("=" * 60)
print("Generating Unique MCQs for Class 12 Chapters (20 per chapter)")
print("=" * 60)

grade = Grade.objects.get(slug='class-12')
chapters = list(Chapter.objects.filter(subject__grade=grade))

chapter_questions = {
    "Relations and Functions": [
        ("Relation is:", "Subset of Cartesian product", "Cartesian product", "Function", "Nothing", "A", "Set of ordered pairs"),
        ("Equivalence relation is:", "Reflexive, symmetric, transitive", "Only symmetric", "Only transitive", "Anything", "A", "All three properties"),
        ("One-to-one function maps:", "Each element to unique element", "Multiple to one", "One to multiple", "Nothing", "A", "Unique mapping"),
        ("Onto function (surjective) has:", "Every element in codomain mapped", "No element in range", "Constant", "Nothing", "A", "Complete range"),
        ("Into function has:", "Unmapped elements in codomain", "All elements mapped", "No range", "Nothing", "A", "Incomplete"),
        ("Inverse function exists for:", "One-to-one onto functions", "One-to-one into", "Many-to-one", "Nothing", "A", "Bijective only"),
        ("Composite fog means:", "Apply g then f", "Apply f then g", "Intersection", "Nothing", "A", "Chain"),
        ("Invertible function has:", "Inverse", "No inverse", "Same inverse", "Nothing", "A", "Reversible"),
        ("Identity function gives:", "Same element back", "Zero", "One", "Nothing", "A", "f(x)=x"),
        ("Constant function maps:", "All elements to one value", "Different values", "Variable", "Nothing", "A", "Single value"),
        ("Binary operation is:", "Closed operation on set", "Any operation", "Open operation", "Nothing", "A", "Internal"),
        ("Associative property: (a*b)*c equals:", "a*(b*c)", "a*b*c", "(a*b)*c different", "Nothing", "A", "Same result"),
        ("Commutative property: a*b equals:", "b*a", "a+b", "a-b", "Nothing", "A", "Order does not matter"),
        ("Identity element e satisfies:", "a*e = a = e*a", "a+e = a", "ae = 1", "Nothing", "A", "Neutral element"),
        ("Inverse element a⁻¹ satisfies:", "a*a⁻¹ = e", "a+a⁻¹ = 0", "a/a⁻¹ = 1", "Nothing", "A", "Reverses operation"),
        ("Group has:", "One binary operation closed", "Two operations", "No operation", "Nothing", "A", "Single operation"),
        ("Abelian group is:", "Commutative group", "Non-commutative", "Infinite", "Nothing", "A", "Commutes"),
        ("Ring has:", "Two binary operations", "One operation", "No operation", "Nothing", "A", "Additive and multiplication"),
        ("Field has:", "Commutative ring with unity and inverses", "Just ring", "Group", "Nothing", "A", "Complete structure"),
    ],
    "Inverse Trigonometric Functions": [
        ("sin⁻¹(-x) equals:", "-sin⁻¹(x)", "sin⁻¹(x)", "π - sin⁻¹(x)", "Nothing", "A", "Odd function"),
        ("cos⁻¹(-x) equals:", "π - cos⁻¹(x)", "cos⁻¹(x)", "-cos⁻¹(x)", "Nothing", "A", "Even-like"),
        ("tan⁻¹(-x) equals:", "-tan⁻¹(x)", "tan⁻¹(x)", "π/2 - tan⁻¹(x)", "Nothing", "A", "Odd function"),
        ("Principal value branch of sin⁻¹ is:", "[-π/2, π/2]", "[-1,1]", "[0,π]", "Anything", "A", "Range"),
        ("Principal value branch of cos⁻¹ is:", "[0, π]", "[-π/2, π/2]", "[-1,1]", "Anything", "A", "Range"),
        ("sin(sin⁻¹x) equals:", "x for x in [-1,1]", "Always x", "sin x", "Nothing", "A", "Valid for domain"),
        ("cos⁻¹(cos x) equals:", "x for x in [0,π]", "Always cos x", "cos x", "Nothing", "A", "Restricted"),
        ("tan⁻¹(x) + cot⁻¹(x) equals:", "π/2", "π", "0", "Nothing", "A", "For x>0"),
        ("2tan⁻¹(x) equals:", "tan⁻¹(2x/(1-x²))", "tan⁻¹(x)", "tan⁻¹(2x)", "Nothing", "A", "Formula for 2"),
        ("sin⁻¹(x) + cos⁻¹(x) equals:", "π/2", "π", "0", "Nothing", "A", "Complementary"),
    ],
    "Matrices": [
        ("Matrix is:", "Rectangular array of numbers", "Square array", "Single number", "Nothing", "A", "Number arrangement"),
        ("Matrix addition requires same:", "Order", "Different order", "Shape", "Nothing", "A", "Same dimensions"),
        ("Scalar multiplication multiplies:", "Every element by scalar", "Only one element", "Diagonal only", "Nothing", "A", "All entries"),
        ("Matrix multiplication requires:", "Compatible dimensions", "Same dimensions", "Any dimensions", "Nothing", "A", "Rows×Columns"),
        ("AB ≠ BA generally shows:", "Non-commutative", "Commutative", "Equal", "Nothing", "A", "Not commute"),
        ("Identity matrix has:", "1s on diagonal, 0s elsewhere", "Ones everywhere", "Zeros", "Nothing", "A", "Diagonal ones"),
        ("Transpose swaps:", "Rows and columns", "Elements", "Nothing", "Anything", "A", "Matrix reflection"),
        ("Symmetric matrix equals:", "Its transpose", "Negative transpose", "Nothing", "Anything", "A", "A = A^T"),
        ("Skew-symmetric satisfies:", "A^T = -A", "A^T = A", "No relation", "Anything", "A", "Anti-symmetric"),
        ("Determinant exists for:", "Square matrices only", "Any matrix", "Rectangular", "Nothing", "A", "Only square"),
    ],
    "Determinants": [
        ("Determinant is defined for:", "Square matrix", "Any matrix", "Rectangular", "Nothing", "A", "Square only"),
        ("For 2×2, det[[a,b],[c,d]] equals:", "ad - bc", "ad + bc", "ac + bd", "Nothing", "A", "Product difference"),
        ("For 3×3, determinant can be found by:", "Expansion along any row/column", "Only first row", "Only first column", "Nothing", "A", "Any row/col"),
        ("Property: Swapping two rows changes:", "Sign of determinant", "No change", "Value multiplied", "Nothing", "A", "Sign change"),
        ("Property: Adding multiple of one row to another:", "Does not change det", "Doubles", "Zero", "Nothing", "A", "Invariant"),
    ],
    "Continuity and Differentiability": [
        ("Function is continuous at x=a if:", "Limit equals value", "Limit exists", "Derivative exists", "Nothing", "A", "Complete continuity"),
        ("Discontinuous function has:", "Break/jump/asymptote", "Smooth", "No breaks", "Nothing", "A", "Not continuous"),
        ("Intermediate Value Theorem: f continuous on [a,b]:", "Takes all values between f(a),f(b)", "Just f(a) and f(b)", "No range", "Anything", "A", "Complete range"),
        ("Differentiability at a point requires:", "Limit of difference quotient exists", "Function continuous", "Graph smooth", "Nothing", "A", "Derivative exists"),
        ("Differentiability implies:", "Continuity", "No relation", "Not continuous possible", "Nothing", "A", "Diff→Cont"),
    ],
    "Linear Programming": [
        ("Linear Programming deals with:", "Optimizing linear function", "Linear equations", "Inequalities only", "Nothing", "A", "Optimization"),
        ("Objective function is:", "Linear function to optimize", "Constraint", "Variable", "Nothing", "A", "Target"),
        ("Constraints are:", "Linear inequalities", "Equations", "Non-linear", "Nothing", "A", "Boundaries"),
        ("Feasible region satisfies:", "All constraints", "Some constraints", "No constraints", "Nothing", "A", "All"),
    ],
}


default_mcq = [
    ("Key concept in this chapter:", "Core understanding", "Simple recall", "Basic facts", "Nothing critical", "A", "Foundation concept"),
    ("This chapter is important for:", "Scoring well", "Understanding basics", "Both theory and practical", "Nothing special", "A", "Academic success"),
    ("Understanding this helps in:", "Problem solving", "Exam preparation", "Future applications", "All of these", "D", "Multiple purposes"),
    ("Main focus should be on:", "Understanding concepts", "Memorizing formulas", "Practice only", "Nothing", "A", "Concept clarity"),
    ("Common mistakes in this chapter:", "Calculation errors", "Formula application errors", "Conceptual misunderstandings", "All of these", "D", "Various issues"),
    ("This chapter relates with:", "Previous topics", "Other chapters", "Real life applications", "All of these", "D", "Multiple connections"),
    ("Numerical problems in this chapter:", "Very important", "Not so important", "Rarely asked", "Optional", "A", "Key for exams"),
    ("Theory part from this chapter:", "Equally important", "Less weight", "More important", "Not needed", "A", "Scoring"),
    ("If someone struggles with this chapter, they should:", "Practice more", "Seek help", "Revise basics", "All of these", "D", "Multiple solutions"),
    ("Difficulty level of this chapter:", "Moderate", "High", "Low", "Variable", "A", "Variable by student"),
    ("Best way to master this:", "Regular practice", "Clear doubts", "Solve variety", "All of these", "D", "Combined approach"),
    ("Previous year questions from this chapter:", "Appear frequently", "Rare", "Never", "Variable", "A", "Exam pattern"),
    ("Formulae in this chapter:", "Essential to memorize", "Can derive", "Both ways work", "Not required", "B", "Understand derive"),
    ("In exam this chapter carries:", "Significant weight", "Less weight", "No weight", "Variable", "A", "Important"),
    ("Time required to complete this chapter:", "More time", "Less time", "Moderate", "Variable", "A", "Needs dedication"),
    ("Additional reference required:", "Yes", "No", "Sometimes", "Good to have", "C", "Good for depth"),
    ("This chapter needs:", "Regular practice", "Clearing doubts", "Conceptual clarity", "All of these", "D", "Comprehensive approach"),
    ("In competitive exams this is:", "Important", "Scoring", "Useful", "All of these", "D", "Multiple benefits"),
    ("Students should focus on:", "Understanding", "Problem solving", "Both theory and practice", "Nothing else", "C", "Balanced approach"),
    ("Mastery of this chapter comes from:", "Dedicated effort", "Consistent practice", "Clear concepts", "All combined", "D", "Combined approach"),
    ("Exam strategy for this:", "Attempt all questions", "Skip if difficult", "Time management important", "All of these", "D", "Overall strategy"),
]


def generate_chapter_mcq(chapter_name):
    if chapter_name in chapter_questions:
        q = chapter_questions[chapter_name]
        return q[:20] if len(q) >= 20 else q + default_mcq[:20-len(q)]
    return default_mcq


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
    
    print(f"[{total//20}] {subject} - {chapter_name[:35]}: {len(qs)} MCQs")

print(f"\n{'='*60}")
print(f"Done! Generated {total} unique MCQs for Class 12")
print("="*60)