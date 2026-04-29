import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Biology', grade=g)
c = Chapter.objects.get(subject=s, name='Diversity in Living World')

pyqs = [
    ("The label of a herbarium sheet does not carry information on:", "Date of collection", "Name of collector", "Local names", "Height of the plant", "D", "Height of plant is not recorded on herbarium labels"),
    ("Which of the following is less general in characters as compared to genus?", "Species", "Family", "Class", "Division", "A", "Species is more specific than genus"),
    ("Taxonomic hierarchy refers to:", "Step-wise arrangement of all categories for classification of plants and animals", "A group of senior taxonomists who decide the nomenclature of plants and animals", "A list of botanists or zoologists who have worked on taxonomy of a species or group", "Classification of a species based on fossil record", "A", "It is the step-wise arrangement of taxonomic categories"),
    ("Which of the following is a defining characteristic of living organisms?", "Growth", "Ability to make sound", "Reproduction", "Response to external stimuli", "D", "Response to stimuli is a defining characteristic"),
    ("In binomial nomenclature, the name of the author appears:", "After the specific epithet", "Before the specific epithet", "After the genus", "In italics", "A", "Author name comes after specific epithet"),
    ("The suffix '-oideae' is used for which taxonomic category?", "Family", "Tribe", "Sub-family", "Class", "C", "-oideae denotes sub-family"),
    ("The sum total of all the chemical reactions occurring in our body is known as:", "Metabolism", "Anabolism", "Catabolism", "Homeostasis", "A", "Metabolism is all chemical reactions"),
    ("A group of related genera which resemble each other in floral characters are placed in:", "Order", "Family", "Species", "Variety", "B", "Family contains related genera"),
    ("Linnaeus used which kingdom of classification?", "Five kingdom", "Three kingdom", "Two kingdom", "Four kingdom", "C", "Linnaeus used two kingdom: Plantae and Animalia"),
    ("Systematics deals with:", "Identification and preservation", "Nomenclature and identification", "Diversity of kinds of organisms and their relationship", "Habitats of organisms and their classification", "C", "Systematics deals with diversity and relationships"),
    ("Which one of the following is a taxonomic aid for identification of both plants and animals?", "Herbarium", "Botanical Garden", "Flora", "Keys", "D", "Keys are used for both plants and animals"),
    ("National Botanical Research Institute is located in:", "Shimla", "Dehradun", "Howrah", "Lucknow", "D", "NBRI is in Lucknow"),
    ("Which of the following is the correct scientific name of Wheat?", "Triticum aestivum", "Oryza sativa", "Mangifera indica", "Zea mays", "A", "Triticum aestivum is wheat"),
    ("The term 'Phylum' was coined by:", "Cuvier", "Haeckel", "Theophrastus", "Linnaeus", "A", "Cuvier coined the term Phylum"),
    ("Genus represents:", "An individual plant or animal", "A collection of plants or animals", "A group of closely related species of plants or animals", "None of these", "C", "Genus is a group of closely related species"),
    ("The basic unit of classification is:", "Genus", "Species", "Order", "Family", "B", "Species is the basic unit"),
    ("Which of the following is not a category?", "Phylum", "Class", "Glumaceae", "Order", "C", "Glumaceae is not a taxonomic category"),
    ("Biological organization starts with:", "Cellular level", "Organismic level", "Atomic level", "Submicroscopic molecular level", "D", "Starts at molecular level"),
    ("Manuals are useful in providing information for:", "Identification of name of species found in an area", "Only one taxon", "Index of plant species in a particular area", "Complete information of any one taxon", "A", "Manuals help identify species"),
    ("As we go from species to kingdom in a taxonomic hierarchy, the number of common characteristics:", "Will decrease", "Will increase", "Remain same", "May increase or decrease", "A", "Characteristics decrease as we go higher"),
    ("True regeneration is found in:", "Hydra", "Planaria", "Sponges", "Amoeba", "B", "Planaria shows true regeneration"),
    ("Growth in non-living objects occurs through:", "Accumulation of material on the surface", "AccumULATION OF material from inside", "Both A and B", "None of the above", "A", "Non-living objects grow by surface accumulation"),
    ("The most obvious and technically complicated feature of all living organisms is:", "Reproduction", "Metabolism", "Consciousness", "Growth", "C", "Consciousness is complex"),
    ("In binomial nomenclature, the first name is ________ and the second name is ________.", "Specific epithet, Genus", "Genus, Specific epithet", "Family, Genus", "Order, Family", "B", "Genus first, then specific epithet"),
    ("Housefly belongs to the order:", "Diptera", "Musca", "Insecta", "Arthropoda", "A", "Housefly is in Diptera"),
    ("Which of the following organisms does not reproduce?", "Mule", "Sterile worker bees", "Infertile human couples", "All of the above", "D", "All are non-reproductive"),
    ("Modern taxonomy includes:", "External and internal structure", "Cell structure and development process", "Ecological information", "All of the above", "D", "Modern taxonomy is comprehensive"),
    ("Families like Solanaceae and Convolvulaceae are included in the order:", "Sapindales", "Polymoniales", "Poales", "Carnivora", "B", "Solanaceae and Convolvulaceae are in Polymoniales"),
    ("Suffix used for order is:", "-ales", "-aceae", "-ae", "-phyta", "A", "-ales is the suffix for order"),
    ("Which is not a component of taxonomy?", "Identification", "Classification", "Ecological variation", "Nomenclature", "C", "Ecological variation is not a component"),
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

print(f"Added {len(pyqs)} PYQs to Diversity in Living World")