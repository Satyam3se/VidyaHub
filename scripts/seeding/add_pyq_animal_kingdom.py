import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='Class 11')
s = Subject.objects.get(name='Biology', grade=g)
c = Chapter.objects.get(subject=s, name='Animal Kingdom')

pyqs = [
    ("In which of the following, the cells are loosely aggregated and do not form tissues?", "Cnidaria", "Porifera", "Platyhelminthes", "Ctenophora", "B", "Porifera cells are loosely aggregated"),
    ("Radial symmetry is found in:", "Coelenterata and Ctenophora", "Adult Echinodermata", "Both A and B", "Platyhelminthes and Annelida", "C", "Both groups show radial symmetry"),
    ("Which of the following is a pseudocoelomate?", "Ascaris", "Fasciola", "Taenia", "Pheretima", "A", "Ascaris is pseudocoelomate"),
    ("Metameric segmentation is the characteristic of:", "Mollusca and Chordata", "Platyhelminthes and Acanthocephala", "Annelida and Arthropoda", "Echinodermata and Coelenterata", "C", "Annelida and Arthropoda have metameric segmentation"),
    ("The canal system is a characteristic feature of:", "Sponges", "Helminthes", "Echinoderms", "Coelenterates", "A", "Sponges have canal system"),
    ("Which of the following cells are present only in Coelenterata?", "Choanocytes", "Cnidoblasts", "Flame cells", "Nephridia", "B", "Cnidoblasts are unique to Coelenterata"),
    ("The skeleton of corals is composed of:", "Silica", "Calcium carbonate", "Calcium phosphate", "Potassium sulphate", "B", "Corals have calcium carbonate skeleton"),
    ("Which of the following belongs to Phylum Ctenophora?", "Pleurobrachia", "Adamsia", "Meandrina", "Physalia", "A", "Pleurobrachia is a ctenophore"),
    ("Flame cells are the excretory structures in:", "Arthropoda", "Platyhelminthes", "Annelida", "Mollusca", "B", "Flame cells are in Platyhelminthes"),
    ("The first phylum to exhibit a complete digestive tract is:", "Platyhelminthes", "Aschelminthes", "Annelida", "Arthropoda", "B", "Aschelminthes have complete digestive tract"),
    ("An important characteristic that Hemichordates share with Chordates is:", "Ventral tubular nerve cord", "Pharynx with gill slits", "Pharynx without gill slits", "Absence of notochord", "B", "Gill slits are shared characteristic"),
    ("Which of the following are cold-blooded animals?", "Schistosoma and Fasciola", "Columba and Neophron", "Ichthyophis and Vipera", "Ornithorhynchus and Macropus", "C", "Ichthyophis and Vipera are cold-blooded"),
    ("Which one of these animals is not a homeotherm?", "Macropus", "Chelone", "Camelus", "Psittacula", "B", "Chelone (turtle) is not homeotherm"),
    ("Presence of a water vascular system is a unique feature of:", "Porifera", "Ctenophora", "Echinodermata", "Chordata", "C", "Echinodermata has water vascular system"),
    ("A file-like rasping organ for feeding, called radula, is found in:", "Pila", "Asterias", "Ophiura", "Echinus", "A", "Pila has radula"),
    ("Metagenesis is observed in:", "Hydra", "Adamsia", "Obelia", "Aurelia", "C", "Obelia shows metagenesis"),
    ("Which of the following is a flightless bird?", "Struthio (Ostrich)", "Neophron", "Pavo", "Columba", "A", "Ostrich is flightless"),
    ("The presence of pneumatic bones is found in:", "Mammals", "Reptiles", "Birds", "Amphibians", "C", "Birds have pneumatic bones"),
    ("Nematocytes are found in:", "Porifera", "Cnidaria", "Nemertinea", "Nematoda", "B", "Cnidaria has nematocytes"),
    ("Which phylum has a true coelom?", "Cnidaria", "Aschelminthes", "Annelida", "Platyhelminthes", "C", "Annelida has true coelom"),
    ("The body of Arthropods is covered by an exoskeleton made of:", "Cellulose", "Chitin", "Keratin", "Calcium", "B", "Arthropods have chitinous exoskeleton"),
    ("In which group of animals do the adults show radial symmetry but larvae show bilateral symmetry?", "Coelenterata", "Ctenophora", "Echinodermata", "Mollusca", "C", "Echinodermata larvae are bilateral"),
    ("Which class of animals possess two pairs of limbs and have dry, cornified skin?", "Amphibia", "Reptilia", "Aves", "Mammalia", "B", "Reptilia has these features"),
    ("A common characteristic of all vertebrates is:", "Presence of a skull", "Division of body into head, neck, trunk and tail", "Presence of two pairs of functional appendages", "Presence of a dorsal tubular nerve cord", "A", "All vertebrates have skull"),
    ("Air bladder is present in:", "Chondrichthyes", "Osteichthyes", "Both A and B", "None of the above", "B", "Osteichthyes have air bladder"),
    ("Which of the following is a limbless amphibian?", "Hyla", "Rana", "Ichthyophis", "Bufo", "C", "Ichthyophis is limbless amphibian"),
    ("The heart of a crocodile is:", "Two-chambered", "Three-chambered", "Four-chambered", "Single-chambered", "C", "Crocodile has four-chambered heart"),
    ("Uric acid is the nitrogenous waste in:", "Mammals and amphibians", "Birds and reptiles", "Fishes and protozoa", "Cartilaginous fishes", "B", "Birds and reptiles excrete uric acid"),
    ("Which of the following is an egg-laying mammal?", "Delphinus", "Ornithorhynchus", "Macropus", "Equus", "B", "Ornithorhynchus lays eggs"),
    ("Malpighian tubules are the excretory organs in:", "Insects", "Flatworms", "Earthworms", "Molluscs", "A", "Insects have Malpighian tubules"),
]

for order, q in enumerate(pyqs):
    MCQQuestion.objects.create(chapter=c, question_text=q[0], option_a=q[1], option_b=q[2], option_c=q[3], option_d=q[4], correct_option=q[5], explanation=q[6], order=order)

print(f"Added {len(pyqs)} PYQs to Animal Kingdom")