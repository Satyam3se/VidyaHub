import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='Class 11')
s = Subject.objects.get(name='Biology', grade=g)

# Get remaining chapters that need PYQs
chapters = Chapter.objects.filter(subject=s)[5:]  # Skip first 5 chapters already done

# Dictionary of 30 PYQs per chapter (NEET exam relevant)
chapters_pyqs = {
    "Anatomy of Flowering Plants": [
        ("Cork is obtained from:", "Cedrus", "Pinus", "Quercus", "Both B and C", "D", "Cork from Quercus suber"),
        ("Function of companion cells is:", "Provide energy for loading", "Store food", "Transport water", "Support sieve tubes", "A", "Companion cells provide ATP for loading"),
        ("Bulliform cells are found in:", "Dorsiventral leaves", "Isobilateral leaves", "Roots", "Stems", "B", "Bulliform cells in isobilateral leaves"),
        ("Heartwood is different from sapwood because:", "It conducts water", "It is dead", "It has no vessels", "It has more water", "B", "Heartwood is non-functional"),
        ("In monocot stems, vascular bundles are:", "arranged in a ring", "scattered", "in two rings", "absent", "B", "Monocot bundles are scattered"),
        ("Casparian strips are present in:", "Epidermis", "Endodermis", "Pericycle", "Cortex", "B", "Casparian in endodermis"),
        ("Secondary growth occurs in:", "Monocots", "Dicots", "Gymnosperms", "Both B and C", "D", "Secondary growth in dicots/gymnosperms"),
        ("Vascular cambium gives rise to:", "Primary xylem", "Primary phloem", "Secondary xylem and phloem", "Cork", "C", "Vascular cambium produces secondary tissues"),
        ("Aerenchyma is found in:", "Hydrophytes", "Xerophytes", "Mesophytes", "Halophytes", "A", "Aerenchyma in hydrophytes"),
        ("Stele does not include:", "Vascular tissue", "Pericycle", "Endodermis", "Ground tissue", "C", "Stele includes vascular, pericycle, ground"),
        ("In roots, protoxylem is:", "Exarch", "Endarch", "Mesarch", "Both A and C", "A", "Roots have exarch xylem"),
        ("Annual rings are formed by:", "Cork cambium", "Vascular cambium", "Apex", "Interfascicular cambium", "B", "Annual rings from vascular cambium"),
        ("Ray initials form:", "Vessels", "Sieve tubes", "Xylem rays", "Fibres", "C", "Ray initials form vascular rays"),
        ("Periderm includes:", "Phellogen", "Phellem", "Phelloderm", "All of these", "D", "Periderm has all three"),
        ("Secondary phloem is composed of:", "Sieve tubes", "Companion cells", "Phloem rays", "All of these", "D", "Secondary phloem has all elements"),
        ("Tyloses are:", "Outgrowths blocking vessels", "Root hairs", "Epidermal hairs", "Lenticels", "A", "Tyloses block vessels"),
        ("Spring wood differs from autumn wood in having:", "Narrow vessels", "More fibers", "Wider vessels", "Thicker walls", "C", "Spring wood has wider vessels"),
        ("Wood fibers are:", "Sclerenchyma", "Parenchyma", "Collenchyma", "Aerenchyma", "A", "Wood fibers sclerenchymatous"),
        ("In dorsiventral leaf, palisade parenchyma is:", "On upper surface", "On lower surface", "On both surfaces", "Absent", "A", "Palisade on upper side"),
        ("Bundle sheath is prominent in:", "Monocot leaf", "Dicot leaf", "Both", "None", "A", "Bundle sheath in monocots"),
        ("Cortex in roots is:", "Always with aerenchyma", "Without intercellular spaces", "With chloroplasts", "None", "D", "Root cortex varies"),
        ("Hypodermis in dicot stem is made of:", "Epidermis", "Collenchyma", "Parenchyma", "Sclerenchyma", "B", "Hypodermis collenchymatous"),
        ("Stomatal density is affected by:", "Light", "CO2", "Humidity", "All of these", "D", "Multiple environmental factors"),
        ("Cork cambium is also called:", "Vascular cambium", "Phellogen", "Interfascicular cambium", "Apical meristem", "B", "Phellogen is cork cambium"),
        ("Medullary rays are:", "Parenchymatous", "Sclerenchymatous", "Collenchymatous", "Aerenchymatous", "A", "Medullary rays parenchymatous"),
        ("Phloem fibers are also called:", "Bast fibers", "Wood fibers", "Fiber trachieds", "Sclerids", "A", "Phloem fibers are bast"),
        ("Sieve tube elements are:", "Living with nucleus", "Dead", "Incomplete", "None", "A", "Sieve tubes enucleate but living"),
        ("In woody roots, cork cambium originates from:", "Pericycle", "Cortex", "Epidermis", "Endodermis", "A", "From pericycle in roots"),
        ("Tissue system in plants was given by:", "Haberlandt", "Sachs", "Goebel", "Eichler", "A", "Haberlandt proposed tissue system"),
    ],
    "Structural Organisation in Animals": [
        ("Simple epithelium is composed of:", "Single layer of cells", "Multiple layers", "Secretory cells", "None", "A", "Simple epithelium single layer"),
        ("Mitochondria are abundant in:", "Neurons", "Muscle cells", "RBCs", "Adipose tissue", "B", "Muscle cells have many mitochondria"),
        ("Gap junctions are found in:", "Nervous tissue", "Muscular tissue", "Epithelial tissue", "Connective tissue", "B", "Gap junctions in cardiac muscle"),
        ("Maximum protein is found in:", "Keratin", "Collagen", "Elastin", "Myosin", "B", "Collagen most abundant"),
        ("Goblet cells secrete:", "Enzymes", "Mucus", "Hormones", "Digestive juices", "B", "Goblet cells produce mucus"),
        ("Which muscle is voluntary:", "Cardiac", "Smooth", "Skeletal", "All", "C", "Skeletal muscle voluntary"),
        ("Neurons are absent in:", "Brain", "Spinal cord", "Retina", "Cartilage", "D", "Cartilage has no neurons"),
        ("RBCs are produced in:", "Liver", "Spleen", "Bone marrow", "All", "D", "RBCs from liver, spleen, marrow"),
        ("Adipose tissue stores:", "Protein", "Glycogen", "Fat", "Minerals", "C", "Adipose stores fat"),
        ("Platelets are fragments of:", "RBC", "WBC", "Megakaryocytes", "Plasma cells", "C", "Platelets from megakaryocytes"),
        ("Basement membrane is made of:", "Chitin", "Collagen", "Keratin", "Elastin", "B", "Basement membrane collagen"),
        ("Hyaline cartilage is found in:", "Ear", "Vertebrae", "Nose", "Knee cap", "C", "Hyaline in nose"),
        ("Dense regular connective tissue is found in:", "Blood", "Bone", "Tendon", "Areolar", "C", "Tendons dense regular"),
        ("Muscle fibers are made of:", "Myoglobin", "Actin and myosin", "Hemoglobin", "Keratin", "B", "Actin and myosin"),
        ("Myelin sheath is formed by:", "Neurons", "Schwann cells", "Oligodendrocytes", "Both B and C", "D", "From Schwann and oligodendrocytes"),
        ("Blood is a type of:", "Areolar tissue", "Vascular tissue", "Fluid connective", "Dense tissue", "C", "Blood fluid connective"),
        ("Pigment melanin is produced by:", "Melanocytes", "Keratinocytes", "Fibroblasts", "Mast cells", "A", "Melanocytes produce melanin"),
        ("Ciliated epithelium is found in:", "Kidneys", "Lungs", "Skin", "Liver", "B", "Respiratory tract ciliated"),
        ("Stratified epithelium is found in:", "Intestine", "Skin", "Stomach", "Lungs", "B", "Skin has stratified"),
        ("Goblet cells are present in:", "Respiratory tract", "Intestine", "Both A and B", "Stomach", "C", "Goblet cells in both"),
        ("Squamous epithelium is found in:", "Skin", "Lining of blood vessels", "Both A and B", "Intestine", "C", "Squamous in skin and vessels"),
        ("Histamine is released by:", "Lymphocytes", "Mast cells", "Platelets", "RBCs", "B", "Mast cells release histamine"),
        ("Kupffer cells are found in:", "Spleen", "Liver", "Kidneys", "Lungs", "B", "Kupffer in liver"),
        ("Neuroglial cells are:", "Neurons", "Supporting cells", "Muscle cells", "Connective cells", "B", "Neuroglial supporting"),
        ("Macrophages are derived from:", "RBCs", "Lymphocytes", "Monocytes", "Platelets", "C", "Macrophages from monocytes"),
        ("Cartilage is avascular:", "True", "False", "Partially", "None", "A", "Cartilage avascular"),
        ("Dense irregular connective tissue is found in:", "Tendon", "Skin", "Bone", "Ligament", "B", "Skin dense irregular"),
        ("Pheromones are secreted by:", "Endocrine glands", "Exocrine glands", "Modified glands", "None", "B", "Exocrine glands"),
        ("Which cell produces collagen?", "Macrophages", "Mast cells", "Fibroblasts", "Plasma cells", "C", "Fibroblasts produce collagen"),
        ("Areolar tissue is found:", "Below skin", "Around blood vessels", "Between organs", "All of these", "D", "Areolar widely distributed"),
    ],
    "Cell: The Unit of Life": [
        ("Who discovered cell?", "Robert Hooke", "Schleiden", "Schwann", "Virchow", "A", "Hooke discovered cell 1665"),
        ("Cell theory was given by:", "Hooke", "Schleiden and Schwann", "Virchow", "Rudolf Virchow", "B", "Schleiden and Schwann"),
        ("Nucleus was discovered by:", "Robert Brown", "Schleiden", "Schwann", "Dujardin", "A", "Robert Brown discovered nucleus"),
        ("DNA is found in:", "Nucleus", "Mitochondria", "Both A and B", "Cytoplasm", "C", "DNA in nucleus and mitochondria"),
        ("Ribosomes are made of:", "RNA and protein", "DNA and protein", "Lipids", "Carbohydrates", "A", "Ribosomes RNA-protein"),
        ("Powerhouse of cell is:", "Nucleus", "Mitochondria", "Ribosome", "Golgi body", "B", "Mitochondria produce ATP"),
        ("Cell membrane is composed of:", "Protein", "Lipid", "Both A and B", "Carbohydrate", "C", "Phospholipid bilayer with proteins"),
        ("Endoplasmic reticulum is absent in:", "Prokaryotes", "Eukaryotes", "Plant cells", "Animal cells", "A", "ER absent in prokaryotes"),
        ("Lysosomes contain:", "DNA", "RNA", "Hydrolytic enzymes", "ATP", "C", "Lysosomes have enzymes"),
        ("Golgi apparatus is involved in:", "Protein synthesis", "Energy production", "Protein packaging", "DNA replication", "C", "Golgi packages proteins"),
        ("Centrosome helps in:", "Respiration", "Cell division", "Protein synthesis", "Transport", "B", "Centrosome forms spindle"),
        ("Plasmolysis occurs in:", "Isotonic solution", "Hypotonic solution", "Hypertonic solution", "None", "C", "Plasmolysis in hypertonic"),
        ("RBCs do not have:", "Nucleus", "Mitochondria", "Cell membrane", "Hemoglobin", "B", "Mature RBCs no mitochondria"),
        ("Mitochondria are inherited from:", "Father", "Mother", "Both parents", "Neither", "B", "Mitochondrial DNA from mother"),
        ("Cell wall is absent in:", "Plant cells", "Animal cells", "Bacteria", "Fungi", "B", "Animal cells lack cell wall"),
        ("Unit of inheritance is:", "DNA", "Gene", "Chromosome", "Nucleus", "B", "Gene is unit of inheritance"),
        ("Nuclear envelope is absent in:", "Plant cells", "Animal cells", "Prokaryotes", "Fungi", "C", "Prokaryotes no nuclear envelope"),
        ("Ribosomes were discovered by:", "Porter", "Robertson", "Kölliker", "Robert Hooke", "C", "Kölliker discovered ribosomes"),
        ("Cristae are found in:", "Nucleus", "Mitochondria", "Ribosome", "Golgi", "B", "Cristae in mitochondria"),
        ("Which organelle is semi-autonomous?", "Ribosome", "Mitochondria", "Lysosome", "Peroxisome", "B", "Mitochondria semi-autonomous"),
        ("Cell ingestion is called:", "Exocytosis", "Endocytosis", "Pinocytosis", "Phagocytosis", "B", "Endocytosis cell ingestion"),
        ("Fluid mosaic model was given by:", "Singer", "Nicolson", "Both A and B", "Robertson", "C", "Singer and Nicolson"),
        ("Nucleolus is not surrounded by:", "Membrane", "DNA", "RNA", "Proteins", "A", "Nucleolus no membrane"),
        ("Vacuoles are most prominent in:", "Animal cells", "Plant cells", "Bacterial cells", "Fungal cells", "B", "Plant cells have large vacuoles"),
        ("Chromatid becomes chromosome during:", "Interphase", "Prophase", "Anaphase", "Telophase", "C", "Chromatids separate in anaphase"),
        ("Cell organelle not bounded by membrane:", "Ribosome", "Lysosome", "Mitochondria", "Golgi", "A", "Ribosome not membrane-bound"),
        ("Middle lamella is composed of:", "Protein", "Pectin", "Cellulose", "Lignin", "B", "Middle lamella pectin"),
        ("Plasmodesmata connect:", "Two cells", "Two nuclei", "Cytoplasm of adjacent cells", "All", "C", "Connect cytoplasm"),
        ("Cell to cell communication is via:", "Tankers", "Gap junctions", "Desmosomes", "Hemidesmosomes", "B", "Gap junctions allow communication"),
    ],
    "Biomolecules": [
        ("Living cells are made up of:", "Inorganic compounds", "Organic compounds", "Both A and B", "None", "C", "Both inorganic and organic"),
        ("The most abundant biomolecule is:", "Proteins", "Carbohydrates", "Lipids", "Water", "D", "Water is most abundant"),
        ("Inulin is a:", "Protein", "Carbohydrate", "Lipid", "Nucleic acid", "B", "Inulin is carbohydrate"),
        ("Glucose is a:", "Hexose", "Pentose", "Tetrose", "Triose", "A", "Glucose is hexose"),
        ("Cellulose is a:", "Structural polysaccharide", "Storage polysaccharide", "Lipid", "Protein", "A", "Cellulose is structural polysaccharide"),
        ("Chitin is found in:", "Plant cell wall", "Fungal cell wall", "Bacterial cell wall", "Animal tissues", "B", "Chitin in fungal cell wall"),
        ("Amino acids are linked by:", "Glycosidic bond", "Peptide bond", "Ester bond", "Hydrogen bond", "B", "Peptide bond in proteins"),
        ("Enzymes are:", "Lipids", "Proteins", "Carbohydrates", "Nucleic acids", "B", "Enzes are proteins"),
        ("DNA has thymine, RNA has:", "Adenine", "Guanine", "Uracil", "Cytosine", "C", "RNA has uracil instead of thymine"),
        ("ATP is a:", "Nucleotide", "Vitamin", "Protein", "Lipid", "A", "ATP is a nucleotide"),
        ("Vitamin B complex is:", "Carbohydrate", "Protein", "Coenzyme", "Lipid", "C", "B complex are coenzymes"),
        ("Zwitterion form is seen in:", "Amino acids", "Fatty acids", "Sugars", "Nucleic acids", "A", "Amino acids form zwitterions"),
        ("Inorganic ions are called:", "Biomolecules", "Microelements", "Electrolytes", "None", "C", "Inorganic ions are electrolytes"),
        ("Glycogen is stored in:", "Liver only", "Muscle only", "Liver and muscle", "Bone", "C", "Glycogen in liver and muscle"),
        ("Cholesterol is a:", "Phospholipid", "Steroid", "Fatty acid", " wax", "B", "Cholesterol is steroid"),
        ("Ribe sugar is:", "Monosaccharide", "Disaccharide", "Polysaccharide", "None", "A", "Ribe is monosaccharide"),
        ("Amylose is component of:", "Protein", "Starch", "Cellulose", "Chitin", "B", "Amylose is starch component"),
        ("DNA double helix is held by:", "Hydrogen bonds", "Phosphodiester bonds", "Peptide bonds", "Ionic bonds", "A", "Hydrogen bonds in DNA helix"),
        ("Coenzyme A contains:", "Vitamin B1", "Vitamin B2", "Vitamin B3", "Pantothenic acid", "D", "Coenzyme A has pantothenic acid"),
        ("The most abundant protein is:", "Keratin", "Myosin", "Collagen", "Elastin", "C", "Collagen most abundant"),
        ("Lipids are soluble in:", "Water", "Organic solvents", "Acids", "Bases", "B", "Lipids soluble in organic solvents"),
        ("Glucose test is done by:", "Iodine solution", "Benedict's solution", "Biuret solution", "Millon's reagent", "B", "Benedict's test for glucose"),
        ("Saturated fatty acids have:", "Single bonds", "Double bonds", "Triple bonds", "None", "A", "Saturated single bonds only"),
        ("Protein primary structure is:", "3D arrangement", "Linear sequence", "Alpha helix", "Beta sheet", "B", "Primary is linear sequence"),
        ("Essential amino acids are:", "10 in number", "8 in number", "20 in number", "5 in number", "B", "8 essential amino acids"),
        ("Phospholipids are components of:", "Cell wall", "Cell membrane", "Ribosome", "Nucleus", "B", "Phospholipids in cell membrane"),
        ("RNA is not found in:", "Nucleus", "Ribosome", "Cytoplasm", "Cell wall", "D", "RNA not in cell wall"),
        ("Urea is formed from:", "Ammonia", "Uric acid", "Cyclic compounds", "All", "A", "Urea from ammonia"),
        ("Catalase is a:", "Protein", "Lipid", "Carbohydrate", "Nucleic acid", "A", "Catalase is protein"),
        ("Heme contains:", "Iron", "Copper", "Zinc", "Magnesium", "A", "Heme contains iron"),
    ],
}

# Add PYQs to chapters
for chapter_name, pyqs in chapters_pyqs.items():
    try:
        c = Chapter.objects.get(subject=s, name=chapter_name)
        # Clear existing and add new PYQs
        MCQQuestion.objects.filter(chapter=c).delete()
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
        print(f"Added {len(pyqs)} PYQs to {chapter_name}")
    except Chapter.DoesNotExist:
        print(f"Chapter {chapter_name} not found")
    except Exception as e:
        print(f"Error with {chapter_name}: {e}")

print("\nDone adding PYQs to remaining chapters")