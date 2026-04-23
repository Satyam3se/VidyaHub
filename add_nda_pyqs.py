import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Chapter, MCQQuestion

print("=" * 60)
print("Generating NDA PYQ MCQs for Each Chapter")
print("=" * 60)

try:
    grade = Grade.objects.get(slug='nda')
except Grade.DoesNotExist:
    print("NDA Grade not found. Try running populate_cbse.py first.")
    sys.exit(1)

chapters = list(Chapter.objects.filter(subject__grade=grade))

nda_questions = {
    # MATHS
    'Algebra': [
        ("If roots of equation x² + px + q = 0 are equal, then:", "p² = 4q", "p² = q", "p = 2q", "p² + 4q = 0", "A", "For equal roots, discriminant b² - 4ac = 0 => p² - 4q = 0 => p² = 4q."),
        ("What is the degree of the polynomial 5x³ - 4x² + 2x - 1?", "3", "2", "1", "4", "A", "Highest power of x is 3."),
        ("The value of log₂(16) is:", "4", "2", "8", "16", "A", "2^4 = 16, so log_2(16) = 4."),
        ("If A and B are two sets such that n(A)=5, n(B)=7, n(A ∩ B)=3. Then n(A ∪ B) is:", "9", "12", "15", "8", "A", "n(A ∪ B) = n(A) + n(B) - n(A ∩ B) = 5 + 7 - 3 = 9."),
        ("What is the binary equivalent of decimal 13?", "1101", "1011", "1001", "1110", "A", "13 = 8 + 4 + 1 = 1101 in binary."),
    ],
    'Matrices and Determinants': [
        ("If A is a square matrix of order n, then det(kA) is equal to:", "k^n * det(A)", "k * det(A)", "k^(n-1) * det(A)", "det(A)/k", "A", "Property of determinants: |kA| = k^n|A|."),
        ("If AB = A and BA = B, then B² is equal to:", "B", "A", "I", "0", "A", "B² = B(BA) = (BB)A = BA = B."),
        ("The inverse of a symmetric matrix is:", "Symmetric", "Skew-symmetric", "Diagonal", "Scalar", "A", "Inverse of symmetric matrix is symmetric."),
        ("If A is an invertible matrix, then det(A^-1) is equal to:", "1/det(A)", "det(A)", "1", "0", "A", "|A^-1| = 1/|A|."),
        ("What is the value of the determinant of an identity matrix?", "1", "0", "n", "-1", "A", "Determinant of identity matrix is always 1."),
    ],
    'Trigonometry': [
        ("What is the value of sin 15°?", "(√6 - √2)/4", "(√6 + √2)/4", "√3/2", "1/2", "A", "sin 15° = sin(45°-30°) = (√6 - √2)/4."),
        ("The maximum value of 3 sin x + 4 cos x is:", "5", "7", "1", "12", "A", "Max value of a sin x + b cos x is √(a² + b²) = √(9+16) = 5."),
        ("What is the value of tan 22.5°?", "√2 - 1", "√2 + 1", "1/√2", "√3 - 1", "A", "tan 22.5° = √2 - 1."),
        ("If sin θ + cosec θ = 2, then sin² θ + cosec² θ is:", "2", "4", "1", "0", "A", "Squaring both sides, sin²θ + cosec²θ + 2 = 4 => sin²θ + cosec²θ = 2."),
        ("What is the principal value of sec^-1 (-2)?", "2π/3", "π/3", "5π/6", "π/6", "A", "sec(2π/3) = -2."),
    ],
    # ENGLISH
    'Grammar and Usage': [
        ("Spot the error: He told me that (a)/ he has completed (b)/ the work yesterday (c)/ No error (d).", "b", "a", "c", "d", "A", "'he has completed' should be 'he had completed' as the sentence is in past tense."),
        ("Neither of the boys ____ returned.", "has", "have", "were", "are", "A", "'Neither' takes a singular verb."),
        ("He is extremely ____ of his child's success.", "proud", "pride", "proudly", "priding", "A", "Adjective 'proud' is correct here."),
        ("She prefers tea ____ coffee.", "to", "than", "over", "from", "A", "'Prefer' is followed by 'to'."),
        ("The jury ____ divided in their opinion.", "were", "was", "has", "is", "A", "When jury is divided, it is considered plural."),
    ],
    'Vocabulary': [
        ("What is the synonym of 'Abundant'?", "Plentiful", "Scarce", "Sparse", "Rare", "A", "Abundant means existing or available in large quantities; plentiful."),
        ("What is the antonym of 'Mitigate'?", "Aggravate", "Alleviate", "Soothe", "Pacify", "A", "Mitigate means to make less severe. Aggravate means to make worse."),
        ("Choose the correct spelling:", "Vacuum", "Vaccuum", "Vacum", "Vaccum", "A", "Vacuum is spelled with one 'c' and two 'u's."),
        ("A place where birds are kept is called:", "Aviary", "Apiary", "Aquarium", "Zoo", "A", "Aviary is for birds, Apiary is for bees."),
        ("Meaning of the idiom 'To bite the dust':", "To be defeated", "To clean", "To eat soil", "To fall sick", "A", "'Bite the dust' means to suffer a defeat."),
    ],
    # PHYSICS
    'Mechanics': [
        ("A body falls freely from rest. The distance covered in the 3rd second is proportional to:", "5", "3", "7", "9", "A", "Distance in nth sec is proportional to (2n-1). For 3rd sec, 2(3)-1 = 5."),
        ("Which of the following is a scalar quantity?", "Work", "Force", "Velocity", "Acceleration", "A", "Work is the dot product of two vectors, hence scalar."),
        ("The escape velocity on earth is approximately:", "11.2 km/s", "9.8 km/s", "7.9 km/s", "15 km/s", "A", "Escape velocity from earth is about 11.2 km/s."),
        ("Momentum is a measure of:", "Quantity of motion", "Inertia", "Mass", "Force", "A", "Momentum (p=mv) represents quantity of motion."),
        ("Friction can be reduced by using:", "Lubricants", "Sand", "Rough surfaces", "Greater weight", "A", "Lubricants decrease the coefficient of friction."),
    ],
    'Optics': [
        ("The image formed by a convex mirror is always:", "Virtual and erect", "Real and inverted", "Virtual and inverted", "Real and erect", "A", "Convex mirror always forms a virtual, erect, and diminished image."),
        ("Twinkling of stars is due to:", "Atmospheric refraction", "Dispersion", "Total internal reflection", "Scattering", "A", "Refractive index of atmosphere fluctuates, causing twinkling."),
        ("Which colour has the longest wavelength in visible spectrum?", "Red", "Blue", "Violet", "Green", "A", "Red light has the longest wavelength."),
        ("The power of a sunglass is:", "0 Dioptre", "-1 Dioptre", "+1 Dioptre", "Infinite", "A", "Curvature is zero, so power is 0 D."),
        ("Mirage is a phenomenon due to:", "Total internal reflection", "Interference", "Diffraction", "Polarization", "A", "Mirages are formed by total internal reflection of light in hot air layers."),
    ],
    # SOCIAL SCIENCE
    'Constitution of India': [
        ("Who is the guardian of Fundamental Rights in India?", "Supreme Court", "Parliament", "President", "Prime Minister", "A", "Supreme Court is the guardian of the Constitution and Fundamental Rights."),
        ("Which Article is associated with Equality before Law?", "Article 14", "Article 17", "Article 19", "Article 21", "A", "Article 14 guarantees equality before law."),
        ("Who appoints the Chief Election Commissioner of India?", "President", "Prime Minister", "Chief Justice", "Parliament", "A", "The President of India appoints the CEC."),
        ("The Directive Principles of State Policy are borrowed from:", "Ireland", "UK", "USA", "USSR", "A", "DPSP is borrowed from the Irish Constitution."),
        ("Who was the Chairman of the Drafting Committee of the Constitution?", "Dr. B.R. Ambedkar", "Dr. Rajendra Prasad", "J.L. Nehru", "Sardar Patel", "A", "Dr. B.R. Ambedkar led the drafting committee."),
    ],
    'Indian History': [
        ("Who was the founder of the Maurya Empire?", "Chandragupta Maurya", "Ashoka", "Bindusara", "Harsha", "A", "Chandragupta Maurya founded the empire."),
        ("The Battle of Plassey was fought in the year:", "1757", "1764", "1857", "1761", "A", "Battle of Plassey took place in 1757."),
        ("Who gave the slogan 'Do or Die'?", "Mahatma Gandhi", "Subhash Chandra Bose", "Bhagat Singh", "Bal Gangadhar Tilak", "A", "Gandhi gave it during the Quit India Movement in 1942."),
        ("The first Viceroy of India was:", "Lord Canning", "Lord Dalhousie", "Lord Mountbatten", "Lord Curzon", "A", "Lord Canning became the first Viceroy after the 1857 revolt."),
        ("Who wrote the book 'Arthashastra'?", "Chanakya", "Megasthenes", "Kalidasa", "Banabhatta", "A", "Chanakya (Kautilya) authored the Arthashastra."),
    ],
}

def generate_generic_nda_mcq(chapter_name, subject):
    generic = [
        (f"Important concept from NDA PYQ on {chapter_name}:", "Is fundamental to the topic", "Is irrelevant", "Is rarely asked", "Can be ignored", "A", f"Basic fundamentals of {chapter_name} are essential."),
        (f"Which principle is central to understanding {chapter_name}?", "Core theoretical models", "Random guesswork", "Skipping the chapter", "Rote memorization only", "A", "Core theories clarify the subject."),
        (f"A typical Previous Year Question from {chapter_name} tests:", "Conceptual clarity", "Handwriting", "Vocabulary only", "Nothing", "A", "NDA exams test conceptual understanding."),
        (f"To master {chapter_name} for NDA, one should focus on:", "Practice and revision", "Ignoring past papers", "Only reading summaries", "Guessing", "A", "Practice is key for success."),
        (f"The foundation of {chapter_name} is built upon:", "Basic principles of {subject}", "Unrelated facts", "Rumors", "Out of syllabus topics", "A", f"Connecting back to {subject} basics."),
    ]
    return generic

total = 0

for chapter in chapters:
    chapter_name = chapter.name.strip()
    subject = chapter.subject.name
    
    # Delete existing MCQs to prevent duplicates
    MCQQuestion.objects.filter(chapter=chapter).delete()
    
    if chapter_name in nda_questions:
        qs = nda_questions[chapter_name][:5]
    else:
        qs = generate_generic_nda_mcq(chapter_name, subject)
    
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
print(f"Done! Seeded {total} NDA PYQ MCQs")
print("="*60)
