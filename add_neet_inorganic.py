import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Chemistry', grade=g)
c = Chapter.objects.get(subject=s, name='Inorganic Chemistry')

ic_pyqs = [
    # Classification of Elements & Periodicity
    ("The element with the highest electronegativity in the periodic table is:", "Fluorine", "Oxygen", "Chlorine", "Nitrogen", "A", "Fluorine has highest EN"),
    ("The correct order of atomic radii is:", "Li > Be > B", "Be > Li > B", "B > Be > Li", "None", "A", "Atomic radius decreases across period"),
    ("Which of the following is an amphoteric oxide?", "Al2O3", "MgO", "Na2O", "K2O", "A", "Al2O3 is amphoteric"),
    ("Identify the incorrect statement: In a group, as atomic number increases:", "Ionization enthalpy increases", "Atomic size increases", "Metallic character increases", "None", "A", "IE decreases down group"),
    ("The formation of the oxide ion O2-(g) from oxygen atom requires an exothermic step followed by an endothermic step because:", "O- repels the incoming electron", "O- attracts electron", "O is stable", "None", "A", "Electron-electron repulsion in O-"),
    
    # Chemical Bonding & Molecular Structure
    ("Which of the following molecules has a net dipole moment?", "NF3", "BF3", "CO2", "CH4", "A", "NF3 has dipole, BF3 is symmetrical"),
    ("The hybridisation of atomic orbitals of Nitrogen in NO2+, NO3- and NH4+ respectively are:", "sp, sp2, sp3", "sp2, sp3, sp", "sp3, sp2, sp", "None", "A", "NO2+: sp, NO3-: sp2, NH4+: sp3"),
    ("Which of the following is isoelectronic with CO?", "CN-", "N2", "O2", "CO2", "A", "CN- and CO are isoelectronic (14 e-)"),
    ("The shape of XeF4 is:", "Square Planar", "Tetrahedral", "Octahedral", "Trigonal", "A", "XeF4 has square planar geometry"),
    ("Bond order of 1.5 is shown by:", "O2-", "O2", "O2+", "O22-", "A", "Superoxide ion O2- has BO 1.5"),
    
    # p-Block Elements
    ("Boric acid is an acid because its molecule:", "Accepts OH- from water", "Donates H+", "Forms H-bonds", "None", "A", "Boric acid is Lewis acid"),
    ("Which of the following is the strongest oxidizing agent?", "F2", "Cl2", "O3", "H2O2", "A", "F2 is strongest oxidizing agent"),
    ("The geometry of PCl5 is:", "Trigonal Bipyramidal", "Tetrahedral", "Octahedral", "Square planar", "A", "PCl5 has TBP geometry"),
    ("Which gas is evolved when copper reacts with dilute HNO3?", "Nitric Oxide (NO)", "Nitrogen Dioxide (NO2)", "Nitrogen (N2)", "Nitrous Oxide", "A", "Cu + dil HNO3 gives NO"),
    ("Nitrogen forms N2, but Phosphorus forms P4 because:", "P cannot form pπ-pπ multiple bonds", "P is too small", "N is more electronegative", "None", "A", "P lacks pπ-pπ bonding"),
    ("The catalyst used in the Contact Process for H2SO4 is:", "V2O5", "Pt", "Fe", "Cu", "A", "Vanadium pentoxide catalyst"),
    ("Which noble gas has the lowest boiling point?", "Helium", "Neon", "Argon", "Xenon", "A", "Helium has lowest boiling point (4K)"),
    ("In SF6, the oxidation state of Sulphur is:", "+6", "+4", "+2", "0", "A", "F is -1 each, S is +6"),
    
    # d and f-Block Elements
    ("Which of the following transition metal ions is colorless?", "Sc3+", "Cu2+", "Co2+", "Fe2+", "A", "Sc3+ has no d electrons (colorless)"),
    ("The Lanthanoid Contraction is responsible for the fact that:", "Zr and Hf have same radius", "Zr and Y have same radius", "Zr and Nb have same radius", "None", "A", "Lanthanoid contraction causes Zr-Hf similarity"),
    ("Magnetic moment of 2.84 BM is given by:", "Ni2+", "Cu2+", "Fe2+", "Co2+", "A", "Ni2+ has 2 unpaired electrons (BM = √n(n+2) = √8 = 2.83)"),
    ("Transition metals act as catalysts because:", "They show variable oxidation states", "They are inert", "They have fixed valence", "None", "A", "Variable oxidation states make them catalytic"),
    ("The common oxidation state of Lanthanoids is:", "+3", "+2", "+4", "+5", "A", "Lanthanoids show +3 oxidation state"),
    ("Potassium dichromate (K2Cr2O7) in acidic medium acts as:", "Oxidizing agent", "Reducing agent", "Catalyst", "Indicator", "A", "K2Cr2O7 is oxidizing agent"),
    
    # Coordination Compounds
    ("The IUPAC name of [Co(NH3)4Cl(NO2)]Cl is:", "Tetraamminichloridonitritocobalt(III) chloride", "Tetraamminenitritochloridocobalt chloride", "Chloronitrotetraammincobalt chloride", "None", "A", "Correct IUPAC naming"),
    ("Which of the following will give a white precipitate with AgNO3?", "[Co(NH3)5Cl]Cl2", "[Co(NH3)6]Cl3", "[Co(NH3)5Br]SO4", "None", "A", "Free Cl- gives white AgCl"),
    ("Coordination number of Iron in [Fe(C2O4)3]3- is:", "6", "4", "3", "8", "A", "Oxalate is bidentate (3 x 2 = 6)"),
    ("The type of isomerism shown by [Co(NH3)5SO4]Br and [Co(NH3)5Br]SO4 is:", "Ionization isomerism", "Linkage isomerism", "Coordination isomerism", "Geometric isomerism", "A", "Ion exchange isomerism"),
    ("According to Crystal Field Theory, for a d4 ion in high spin octahedral field:", "t2g3 eg1", "t2g4", "t2g2 eg2", "None", "A", "High spin d4: t2g3 eg1"),
    ("Which is used as an anti-cancer drug?", "Cis-platin", "Trans-platin", " cisplatin", "Carboplatin", "A", "Cisplatin is anti-cancer drug"),
]

# Get existing count
existing = MCQQuestion.objects.filter(chapter=c).count()
print(f"Existing PYQs in Inorganic Chemistry: {existing}")

# Delete and add
MCQQuestion.objects.filter(chapter=c).delete()
for order, q in enumerate(ic_pyqs):
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

print(f"Added {len(ic_pyqs)} PYQs to Inorganic Chemistry")