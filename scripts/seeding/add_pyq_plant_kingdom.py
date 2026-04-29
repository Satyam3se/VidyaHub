import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='Class 11')
s = Subject.objects.get(name='Biology', grade=g)
c = Chapter.objects.get(subject=s, name='Plant Kingdom')

pyqs = [
    ("Phylogenetic system of classification is based on:", "Morphological features", "Chemical constituents", "Evolutionary relationships", "Floral characters", "C", "Phylogenetic system is based on evolutionary relationships"),
    ("Floreidan starch has a structure similar to:", "Starch and cellulose", "Amylopectin and glycogen", "Mannitol and algin", "Laminarin and cellulose", "B", "Floreidan starch is similar to amylopectin and glycogen"),
    ("Which of the following is responsible for peat formation?", "Marchantia", "Riccia", "Funaria", "Sphagnum", "D", "Sphagnum is responsible for peat formation"),
    ("The giant redwood tree (Sequoia sempervirens) is a/an:", "Angiosperm", "Free fern", "Pteridophyte", "Gymnosperm", "D", "Sequoia is a gymnosperm"),
    ("Agar is commercially obtained from:", "Gelidium and Gracilaria", "Ulothrix and Spirogyra", "Sargassum and Laminaria", "Chlamydomonas and Volvox", "A", "Agar is obtained from Gelidium and Gracilaria"),
    ("In Bryophytes and Pteridophytes, transport of male gametes requires:", "Birds", "Water", "Wind", "Insects", "B", "Water is required for gamete transport"),
    ("An example of colonial alga is:", "Volvox", "Ulothrix", "Spirogyra", "Chlorella", "A", "Volvox is a colonial alga"),
    ("Zygotic meiosis is characteristic of:", "Fucus", "Funaria", "Chlamydomonas", "Marchantia", "C", "Chlamydomonas shows zygotic meiosis"),
    ("Life cycle of Ectocarpus and Fucus respectively are:", "Haplontic, Diplontic", "Diplontic, Haplodiplontic", "Haplodiplontic, Diplontic", "Haplodiplontic, Haplontic", "C", "Ectocarpus: haplodiplontic, Fucus: diplontic"),
    ("Conifers are adapted to tolerate extreme environmental conditions because of:", "Broad hardy leaves", "Presence of vessels", "Thick cuticle and sunken stomata", "Superficial stomata", "C", "Thick cuticle and sunken stomata help adapt"),
    ("Which one is a vascular cryptogam?", "Equisetum", "Marchantia", "Cedrus", "Sargassum", "A", "Equisetum is a vascular cryptogam"),
    ("Double fertilization is exhibited by:", "Algae", "Fungi", "Angiosperms", "Gymnosperms", "C", "Angiosperms exhibit double fertilization"),
    ("Holdfast, stipe, and frond constitute the plant body in case of:", "Rhodophyceae", "Chlorophyceae", "Phaeophyceae", "All of the above", "C", "Phaeophyceae have holdfast, stipe, frond"),
    ("Which of the following is a 'living fossil'?", "Pinus", "Cycas", "Ginkgo", "Both B and C", "D", "Cycas and Ginkgo are living fossils"),
    ("A prothallus is:", "A structure in pteridophytes formed before the thallus develops", "A sporophytic free-living structure formed in pteridophytes", "A gametophytic free-living structure formed in pteridophytes", "A primitive structure formed after fertilization in pteridophytes", "C", "Prothallus is free-living gametophyte in pteridophytes"),
    ("Isogamous condition with non-flagellated gametes is found in:", "Spirogyra", "Volvox", "Fucus", "Chlamydomonas", "A", "Spirogyra has isogamous non-flagellated gametes"),
    ("The predominant stage of the life cycle of a moss is the:", "Protonema stage", "Leafy stage", "Gametophyte", "Both A and B", "C", "Gametophyte is predominant in moss"),
    ("In Gymnosperms, the pollen chamber represents:", "A cavity in the ovule in which pollen grains are stored after pollination", "An opening in the megasporophyll through which the pollen tube passes", "The microsporangium in which pollen grains are developed", "A cell in the pollen grain in which the sperms are formed", "A", "Pollen chamber stores pollen after pollination"),
    ("Pyrenoids contain:", "Protein only", "Starch only", "Protein and starch", "Oil droplets", "C", "Pyrenoids have protein and starch"),
    ("Brown algae are characterized by the presence of:", "Phycocyanin", "Phycoerythrin", "Fucoxanthin", "Haematochrome", "C", "Fucoxanthin gives brown color"),
    ("Heterospory and seed habit are often exhibited by a plant possessing:", "Petiole", "Ligule", "Bract", "Spathe", "B", "Ligule is associated with heterospory and seed habit"),
    ("The endosperm of Gymnosperms is:", "Haploid (n)", "Diploid (2n)", "Triploid (3n)", "Polyploid", "A", "Endosperm is haploid in gymnosperms"),
    ("Which one of the following is considered important in the development of seed habit?", "Homospory", "Heterospory", "Dependent sporophyte", "Free living gametophyte", "B", "Heterospory is important for seed habit"),
    ("Male gametes are flagellated in:", "Anabaena", "Ectocarpus", "Spirogyra", "Polysiphonia", "B", "Ectocarpus has flagellated male gametes"),
    ("The archegonium is absent in:", "Bryophytes", "Pteridophytes", "Gymnosperms", "Angiosperms", "D", "Archegonium is absent in angiosperms"),
    ("Which of the following is a medicinal plant?", "Aloe", "Asparagus", "Colchicum", "All of the above", "D", "All are medicinal plants"),
    ("Coralloid roots of Cycas are associated with:", "Nitrogen-fixing cyanobacteria", "Mycorrhizal fungi", "Parasitic bacteria", "Saprophytic fungi", "A", "Cycas roots have cyanobacteria"),
    ("Mannitol is the stored food in:", "Porphyra", "Fucus", "Gracilaria", "Chara", "B", "Fucus stores mannitol"),
    ("Dominant phase in Pteridophytes is:", "Gametophyte", "Sporophyte", "Protonema", "None of these", "B", "Sporophyte is dominant in pteridophytes"),
    ("Numerical taxonomy is based on:", "All observable characteristics", "Cytological information", "Chemical constituents", "Genetic lineage", "A", "Numerical taxonomy uses all observable characteristics"),
]

for order, q in enumerate(pyqs):
    MCQQuestion.objects.create(chapter=c, question_text=q[0], option_a=q[1], option_b=q[2], option_c=q[3], option_d=q[4], correct_option=q[5], explanation=q[6], order=order)

print(f"Added {len(pyqs)} PYQs to Plant Kingdom")