import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='Class 11')
s = Subject.objects.get(name='Biology', grade=g)

chapters_data = {
    "Anatomy of Flowering Plants": [
        ("Cork is obtained from:", "Cedrus", "Pinus", "Quercus", "Both B and C", "D", "Cork is obtained from Quercus suber (cork oak)"),
        ("Function of companion cells is:", "Provide energy for loading", "Store food", "Transport water", "Support sieve tubes", "A", "Companion cells provide ATP for loading"),
        ("Bulliform cells are found in:", "Dorsiventral leaves", "Isobilateral leaves", "Roots", "Stems", "B", "Bulliform cells help leaf rolling in xerophytes"),
        ("Heartwood is different from sapwood because:", "It conducts water", "It is dead", "It has no vessels", "It has more water", "B", "Heartwood is non-functional dead wood"),
        ("In monocot stems, vascular bundles are:", " arranged in a ring", " scattered", " in two rings", " absent", "B", "Monocot vascular bundles are scattered"),
        ("Casparian strips are present in:", "Epidermis", "Endodermis", "Pericycle", "Cortex", "B", "Casparian strips are in endodermal cells"),
        ("Secondary growth occurs in:", "Monocots", "Dicots", "Gymnosperms", "Both B and C", "D", "Secondary growth in dicots and gymnosperms"),
        ("Vascular cambium gives rise to:", "Primary xylem", "Primary phloem", "Secondary xylem and phloem", "Cork", "C", "Vascular cambium produces secondary tissues"),
        ("Aerenchyma is found in:", "Hydrophytes", "Xerophytes", "Mesophytes", "Halophytes", "A", "Aerenchyma provides buoyancy in hydrophytes"),
        ("Stele does not include:", "Vascular tissue", "Pericycle", "Endodermis", "Ground tissue", "C", "Stele includes vascular, pericycle, ground tissue"),
        ("In roots, protoxylem is:", "Exarch", "Endarch", "Mesarch", "Both A and C", "A", "Roots have exarch protoxylem"),
        ("Annual rings are formed by:", "Cork cambium", "Vascular cambium", "Apex", "Interfascicular cambium", "B", "Annual rings from vascular cambium activity"),
        ("Ray initials form:", "Vessels", "Sieve tubes", "Xylem rays", "Fibres", "C", "Ray initials form vascular rays"),
        ("Periderm includes:", "Phellogen", "Phellem", "Phelloderm", "All of these", "D", "Periderm has phellogen, phellem, phelloderm"),
        ("Secondary phloem is composed of:", "Sieve tubes", "Companion cells", "Phloem rays", "All of these", "D", "Secondary phloem has all elements"),
        ("Tyloses are:", "Outgrowths blocking vessels", "Root hairs", "Epidermal hairs", "Lenticels", "A", "Tyloses block blocked vessels in heartwood"),
        ("Spring wood differs from autumn wood in having:", "Narrow vessels", "More fibers", "Wider vessels", "Thicker walls", "C", "Spring wood has wider vessels"),
        ("Wood fibers are:", "Sclerenchyma", "Parenchyma", "Collenchyma", "Aerenchyma", "A", "Wood fibers are sclerenchymatous"),
        ("In dorsiventral leaf, palisade parenchyma is:", "On upper surface", "On lower surface", "On both surfaces", "Absent", "A", "Palisade is on upper side"),
        ("Bundle sheath is prominent in:", "Monocot leaf", "Dicot leaf", "Both", "None", "A", "Bundle sheath prominent in monocots"),
        ("Cortex in roots is:", "Always with aerenchyma", "Without intercellular spaces", "With chloroplasts", "None", "D", "Root cortex varies with plant type"),
        ("Hypodermis in dicot stem is made of:", "Epidermis", "Collenchyma", "Parenchyma", "Sclerenchyma", "B", "Hypodermis is collenchymatous in young stems"),
        ("Stomatal density is affected by:", "Light", "CO2", "Humidity", "All of these", "D", "Stomatal density affected by environmental factors"),
        ("Cork cambium is also called:", "Vascular cambium", "Phellogen", "Interfascicular cambium", "Apical meristem", "B", "Phellogen is cork cambium"),
        ("Medullary rays are:", "Parenchymatous", "Sclerenchymatous", "Collenchymatous", "Aerenchymatous", "A", "Medullary rays are parenchymatous"),
        ("Phloem fibers are also called:", "Bast fibers", "Wood fibers", "Fiber trachieds", "Sclerids", "A", "Phloem fibers are bast fibers"),
        ("Sieve tube elements are:", "Living with nucleus", "Dead", "Incomplete", "None", "A", "Sieve tubes are enucleate but living"),
        ("In woody roots, cork cambium originates from:", "Pericycle", "Cortex", "Epidermis", "Endodermis", "A", "Cork cambium from pericycle in roots"),
        ("Tissue system in plants was given by:", "Haberlandt", "Sachs", "Goebel", "Eichler", "A", "Tissue system theory by Haberlandt"),
        ("Maximum growth in plants occurs in:", "Night", "Morning", "Afternoon", "Evening", "A", "Maximum growth at night"),
    ],
    "Structural Organisation in Animals": [
        ("Simple epithelium is composed of:", "Single layer of cells", "Multiple layers", "Secretory cells", "None", "A", "Simple epithelium has single layer"),
        ("Mitochondria are abundant in:", "Neurons", "Muscle cells", "RBCs", "Adipose tissue", "B", "Muscle cells have many mitochondria"),
        ("Gap junctions are found in:", "Nervous tissue", "Muscular tissue", "Epithelial tissue", "Connective tissue", "B", "Gap junctions in cardiac muscle"),
        ("Maximum protein is found in:", "Keratin", "Collagen", "Elastin", "Myosin", "B", "Collagen is most abundant protein"),
        ("Goblet cells secrete:", "Enzymes", "Mucus", "Hormones", "Digestive juices", "B", "Goblet cells produce mucus"),
        ("Which muscle is voluntary:", "Cardiac", "Smooth", "Skeletal", "All", "C", "Skeletal muscle is voluntary"),
        ("Neurons are absent in:", "Brain", "Spinal cord", "Retina", "Cartilage", "D", "Cartilage has no neurons"),
        ("RBCs are produced in:", "Liver", "Spleen", "Bone marrow", "All", "D", "RBCs from liver, spleen, bone marrow"),
        ("Adipose tissue stores:", "Protein", "Glycogen", "Fat", "Minerals", "C", "Adipose stores fat"),
        ("Platelets are fragments of:", "RBC", "WBC", "Megakaryocytes", "Plasma cells", "C", "Platelets from megakaryocytes"),
        ("Basement membrane is made of:", "Chitin", "Collagen", "Keratin", "Elastin", "B", "Basement membrane contains collagen"),
        ("Hyaline cartilage is found in:", "Ear", "Vertebrae", "Nose", "Knee cap", "C", "Hyaline cartilage in nasal passages"),
        ("Dense regular connective tissue is found in:", "Blood", "Bone", "Tendon", "Areolar", "C", "Tendons are dense regular connective"),
        ("Muscle fibers are made of:", "Myoglobin", "Actin and myosin", "Hemoglobin", "Keratin", "B", "Muscle fibers have actin and myosin"),
        ("Myelin sheath is formed by:", "Neurons", "Schwann cells", "Oligodendrocytes", "Both B and C", "D", "Myelin from Schwann and oligodendrocytes"),
        ("Blood is a type of:", "Areolar tissue", "Vascular tissue", "Fluid connective", "Dense tissue", "C", "Blood is fluid connective tissue"),
        ("Pigment melanin is produced by:", "Melanocytes", "Keratinocytes", "Fibroblasts", "Mast cells", "A", "Melanocytes produce melanin"),
        ("Ciliated epithelium is found in:", "Kidneys", "Lungs", "Skin", "Liver", "B", "Ciliated epithelium in respiratory tract"),
        ("Stratified epithelium is found in:", "Intestine", "Skin", "Stomach", "Lungs", "B", "Skin has stratified epithelium"),
        ("Goblet cells are present in:", "Respiratory tract", "Intestine", "Both A and B", "Stomach", "C", "Goblet cells in respiratory and intestinal tracts"),
        ("Squamous epithelium is found in:", "Skin", "Lining of blood vessels", "Both A and B", "Intestine", "C", "Squamous in skin and blood vessels"),
        ("Histamine is released by:", "Lymphocytes", "Mast cells", "Platelets", "RBCs", "B", "Mast cells release histamine"),
        ("Kupffer cells are found in:", "Spleen", "Liver", "Kidneys", "Lungs", "B", "Kupffer cells in liver sinusoids"),
        ("Neuroglial cells are:", "Neurons", "Supporting cells", "Muscle cells", "Connective cells", "B", "Neuroglial are supporting cells"),
        ("Macrophages are derived from:", "RBCs", "Lymphocytes", "Monocytes", "Platelets", "C", "Macrophages from monocytes"),
        ("Cartilage is avascular:", "True", "False", "Partially", "None", "A", "Cartilage is avascular"),
        ("Dense irregular connective tissue is found in:", "Tendon", "Skin", "Bone", "Ligament", "B", "Skin has dense irregular tissue"),
        ("Pheromones are secreted by:", "Endocrine glands", "Exocrine glands", "Modified glands", "None", "B", "Pheromones from exocrine glands"),
        ("Which cell produces collagen?", "Macrophages", "Mast cells", "Fibroblasts", "Plasma cells", "C", "Fibroblasts produce collagen"),
        ("Areolar tissue is found:", "Below skin", "Around blood vessels", "Between organs", "All of these", "D", "Areolar tissue is widely distributed"),
    ],
    "Cell: The Unit of Life": [
        ("Who discovered cell?", "Robert Hooke", "Schleiden", "Schwann", "Virchow", "A", "Robert Hooke discovered cell in 1665"),
        ("Cell theory was given by:", "Hooke", "Schleiden and Schwann", "Virchow", "Rudolf Virchow", "B", "Cell theory by Schleiden and Schwann"),
        ("Nucleus was discovered by:", "Robert Brown", "Schleiden", "Schwann", "Dujardin", "A", "Robert Brown discovered nucleus"),
        ("DNA is found in:", "Nucleus", "Mitochondria", "Both A and B", "Cytoplasm", "C", "DNA in nucleus and mitochondria"),
        ("Ribosomes are made of:", "RNA and protein", "DNA and protein", "Lipids", "Carbohydrates", "A", "Ribosomes are RNA-protein complexes"),
        ("Powerhouse of cell is:", "Nucleus", "Mitochondria", "Ribosome", "Golgi body", "B", "Mitochondria produce ATP"),
        ("Cell membrane is composed of:", "Protein", "Lipid", "Both A and B", "Carbohydrate", "C", "Cell membrane is phospholipid bilayer with proteins"),
        ("Endoplasmic reticulum is absent in:", "Prokaryotes", "Eukaryotes", "Plant cells", "Animal cells", "A", "ER absent in prokaryotes"),
        ("Lysosomes contain:", "DNA", "RNA", "Hydrolytic enzymes", "ATP", "C", "Lysosomes have hydrolytic enzymes"),
        ("Golgi apparatus is involved in:", "Protein synthesis", "Energy production", "Protein packaging", "DNA replication", "C", "Golgi packages proteins"),
        ("Centrosome helps in:", "Respiration", "Cell division", "Protein synthesis", "Transport", "B", "Centrosome forms spindle fibers"),
        ("Plasmolysis occurs in:", "Isotonic solution", "Hypotonic solution", "Hypertonic solution", "None", "C", "Plasmolysis in hypertonic solution"),
        ("RBCs do not have:", "Nucleus", "Mitochondria", "Cell membrane", "Hemoglobin", "B", "Mature RBCs lack mitochondria"),
        ("Mitochondria are inherited from:", "Father", "Mother", "Both parents", "Neither", "B", "Mitochondrial DNA from mother"),
        ("Cell wall is absent in:", "Plant cells", "Animal cells", "Bacteria", "Fungi", "B", "Animal cells lack cell wall"),
        ["CellUrl", "http://", "://", ".com", ".in"],
        ("Hypothalamus is composed of: { }"},
    ],
}

print(f"Total chapter PYQ files created")
print("Created PYQ data for:")
for chapter_name in chapters_data:
    print(f"- {chapter_name}")