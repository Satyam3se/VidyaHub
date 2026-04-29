import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='Class 11')
s = Subject.objects.get(name='Biology', grade=g)
c = Chapter.objects.get(subject=s, name='Morphology of Flowering Plants')

pyqs = [
    ("In some plants like Rhizophora, roots come out of the ground and grow vertically upwards. These are called:", "Prop roots", "Stilt roots", "Pneumatophores", "Adventitious roots", "C", "Pneumatophores are above-ground roots for gas exchange"),
    ("The region of the root that is responsible for the growth in length is:", "Region of maturation", "Region of elongation", "Region of meristematic activity", "Root cap", "B", "Region of elongation is behind root cap"),
    ("In Australian Acacia, the leaves are small and short-lived. The petioles expand, become green and synthesize food. These are called:", "Phyllodes", "Phylloclades", "Cladodes", "Tendrils", "A", "Phyllodes are modified petioles acting as leaves"),
    ("When the leaflets are attached at a common point, i.e., at the tip of the petiole, the leaf is:", "Pinnately compound", "Palmately compound", "Simple leaf", "Parallel venation", "B", "Palmately compound leaves have leaflets at tip of petiole"),
    ("The arrangement of flowers on the floral axis is termed as:", "Phyllotaxy", "Inflorescence", "Aestivation", "Placentation", "B", "Inflorescence is arrangement of flowers on axis"),
    ("In a cymose inflorescence, the main axis:", "Terminates in a flower", "Continues to grow indefinitely", "Bears flowers in acropetal succession", "Has no floral axis", "A", "In cymose, main axis terminates in flower"),
    ("A flower which can be divided into two equal radial halves in any radial plane passing through the center is:", "Zygomorphic", "Actinomorphic", "Asymmetric", "Irregular", "B", "Actinomorphic flowers are radially symmetrical"),
    ("In epigynous flowers, the ovary is situated:", "Above the thalamus", "Below the other floral parts", "At the same level as other parts", "On the side of the thalamus", "B", "Epigynous flowers have inferior ovary"),
    ("The mode of arrangement of sepals or petals in a floral bud with respect to other members of the same whorl is:", "Placentation", "Aestivation", "Phyllotaxy", "Inflorescence", "B", "Aestivation is arrangement of floral parts in bud"),
    ("When ovules are borne on a central axis and septa are absent, the placentation is:", "Marginal", "Axile", "Parietal", "Free central", "D", "Free central placentation has ovules on central axis"),
    ("Edible part of Mango is the:", "Endocarp", "Mesocarp", "Exocarp", "Seed", "B", "Mesocarp is the fleshy edible part"),
    ("Coconut fruit is a:", "Berry", "Drupe", "Capsule", "Legume", "B", "Coconut is a drupe"),
    ("Stamens attached to petals are called:", "Epipetalous", "Epiphyllous", "Gynandrous", "Free", "A", "Epipetalous means attached to petals"),
    ("Radicle is enclosed in a sheath called:", "Coleorhiza", "Coleoptile", "Testa", "Hilum", "A", "Coleorhiza is radicle sheath"),
    ("The technical term for the ovary in a Mustard flower is:", "Superior", "Inferior", "Half-inferior", "Perigynous", "A", "Mustard has superior ovary"),
    ("Venation in Monocot leaves is usually:", "Reticulate", "Parallel", "Palmate", "Pinnate", "B", "Monocots have parallel venation"),
    ("Ginger is an underground:", "Root", "Stem", "Leaf", "Flower", "B", "Ginger is a rhizome (modified stem)"),
    ("The outermost layer of maize endosperm is the:", "Aleurone layer", "Endosperm", "Perisperm", "Scmutellum", "A", "Aleurone is the outermost layer"),
    ("The smallest unit of a compound leaf is the:", "Leaflet", "Stipule", "Petiole", "Blade", "A", "Leaflet is the unit of compound leaf"),
    ("Papilionaceous corolla is found in:", "Asteraceae", "Fabaceae", "Solanaceae", "Brassicaceae", "B", "Fabaceae has butterfly-like corolla"),
    ("Vexillary aestivation is characteristic of:", "Solanaceae", "Fabaceae", "Liliaceae", "Asteraceae", "B", "Fabaceae shows vexillary aestivation"),
    ("Sterile stamen is called:", "Staminode", "Pistil", "Anther", "Filament", "A", "Staminode is non-functional stamen"),
    ("Placentation in Tomato is:", "Marginal", "Axile", "Parietal", "Free central", "B", "Tomato has axile placentation"),
    ("Shield-shaped cotyledon in Monocots is the:", "Scutellum", "Coleoptile", "Epiblast", "Coleorhiza", "A", "Scutellum is shield-shaped in maize"),
    ("Floral formula of Solanaceae is:", "oplus K5 C5 A5 G(2)", "oplus K5 C5 A5 G(2)", "oplus K5 C5 A5 G(2)", "oplus K5 C5 A5 G(2)", "A", "Solanaceae: actinomorphic, pentamerous"),
    ("Which of the following is a False fruit?", "Apple", "Mango", "Pea", "Gram", "A", "Apple is a false fruit (pome)"),
    ("Whorled phyllotaxy is found in:", "Calotropis", "Alstonia", "Mango", "Grass", "B", "Alstonia shows whorled phyllotaxy"),
    ("Thorns are modifications of:", "Roots", "Leaves", "Axillary buds", "Flowers", "C", "Thorns are modified axillary buds"),
    ("Non-endospermic seed example is:", "Castor", "Wheat", "Bean", "Rice", "C", "Bean seeds are non-endospermic"),
    ("Monadelphous stamens are found in:", "Tomato", "China rose", "Mustard", "Pea", "B", "China rose has monadelphous stamens"),
]

for order, q in enumerate(pyqs):
    MCQQuestion.objects.create(chapter=c, question_text=q[0], option_a=q[1], option_b=q[2], option_c=q[3], option_d=q[4], correct_option=q[5], explanation=q[6], order=order)

print(f"Added {len(pyqs)} PYQs to Morphology of Flowering Plants")