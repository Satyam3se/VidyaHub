import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='Class 11')
s = Subject.objects.get(name='Biology', grade=g)
c = Chapter.objects.get(subject=s, name='Locomotion and Movement')

MCQQuestion.objects.filter(chapter=c).delete()

pyqs = [
    ("Skeletal muscle is:", "Voluntary", "Involuntary", "Cardiac", "Smooth", "A", "Skeletal muscle voluntary"),
    ("Muscle contraction needs:", "Ca2+", "ATP", "Both A and B", "None", "C", "Ca2+ and ATP needed"),
    ("Actin filament is attached to:", "Z line", "M line", "H zone", "None", "A", "Actin attached to Z line"),
    ("Myosin head has:", "ATPase", "Kinase", "Phosphatase", "None", "A", "Myosin has ATPase"),
    ("Power stroke is due to:", "ATP hydrolysis", "Ca2+ release", "Action potential", "None", "A", "Power stroke ATP hydrolysis"),
    ("Sliding filament theory was given by:", "Huxley", "Hill", "Meyerhof", "Krebs", "A", "Huxley sliding filament"),
    ("Tropomyosin blocks:", "Actin binding sites", "Myosin binding sites", "ATP binding sites", "None", "B", "Tropomyosin blocks myosin sites"),
    ("Troponin binds to:", "Actin", "Myosin", "Tropomyosin", "All", "A", "Troponin binds actin"),
    ("Neuromuscular junction is:", "Chemical synapse", "Electrical synapse", "Both", "None", "A", "Neuromuscular is chemical"),
    ("ACh is broken by:", "Acetylcholinesterase", "Choline acetyltransferase", "Both", "None", "A", "AChE breaks ACh"),
    ("Muscle fatigue is due to:", "Lactic acid", "ADP", "Both A and B", "None", "C", "Lactic acid and ADP"),
    ("Rigor mortis is due to:", "ATP deficiency", "Ca2+ excess", "Both A and B", "None", "C", "ATP deficiency and Ca2+"),
    ("Red fibers have:", "More mitochondria", "Few mitochondria", "No mitochondria", "None", "A", "Red fibers more mitochondria"),
    ("White fibers have:", "More mitochondria", "Few mitochondria", "No mitochondria", "None", "B", "White fibers few mitochondria"),
    ("Slow fibers are:", "Type I", "Type II", "Type III", "None", "A", "Slow fibers Type I"),
    ("Fast fibers are:", "Type I", "Type II", "Type III", "None", "B", "Fast fibers Type II"),
    ("Isometric contraction is:", "Length constant", "Tension constant", "Both", "None", "B", "Isometric tension constant"),
    ("Isotonic contraction is:", "Length constant", "Tension constant", "Both", "None", "A", "Isotonic length constant"),
    ("Synergistic muscles:", "Work together", "Work opposite", "No effect", "None", "A", "Synergists work together"),
    ("Antagonistic muscles:", "Work together", "Work opposite", "No effect", "None", "B", "Antagonists work opposite"),
    ("Pivot joint is:", "Atlas-axis", "Knee", "Hip", "None", "A", "Atlas-axis is pivot"),
    ("Hinge joint is:", "Knee", "Hip", "Shoulder", "None", "A", "Knee is hinge joint"),
    ("Ball and socket joint is:", "Knee", "Hip", "Elbow", "None", "B", "Hip is ball and socket"),
    ("Gliding joint is:", "Vertebrae", "Knee", "Hip", "None", "A", "Vertebrae gliding joint"),
    ("Sutures are in:", "Skull", "Vertebrae", "Limbs", "None", "A", "Sutures in skull"),
    ("Fontanelles are:", "Soft spots", "Joints", "Bones", "None", "A", "Fontanelles soft spots in infants"),
    ("Bone is composed of:", "Organic matrix", "Inorganic salts", "Both", "None", "C", "Bone has organic and inorganic"),
    ("Osteoblasts form:", "Bone", "Cartilage", "Marrow", "None", "A", "Osteoblasts form bone"),
    ("Osteoclasts resorb:", "Bone", "Cartilage", "Marrow", "None", "A", "Osteoclasts resorb bone"),
    ("Synovial fluid is secreted by:", "Synovial membrane", "Cartilage", "Bone", "None", "A", "Synovial membrane secretes"),
]

for order, q in enumerate(pyqs):
    MCQQuestion.objects.create(
        chapter=c,
        question_text=q[0],
        option_a=q[1],
        option_b=q[2],
        option_c=q[3],
        option_d=q[4],
        correct_option=q[5],
        explanation=q[6],
        order=order
    )

print(f"Added {len(pyqs)} PYQs to Locomotion and Movement")