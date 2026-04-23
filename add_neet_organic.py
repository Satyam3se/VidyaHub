import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Chemistry', grade=g)
c = Chapter.objects.get(subject=s, name='Organic Chemistry')

oc_pyqs = [
    # GOC & Hydrocarbons
    ("Which of the following is the most stable carbocation?", "(CH3)3C+ (Tertiary)", "CH3CH2+ (Primary)", "CH3+ (Methyl)", "CH2=CH+ (Vinyl)", "A", "Tertiary carbocation is most stable"),
    ("The IUPAC name of CH3CH(OH)CH2CH2COOH is:", "4-hydroxypentanoic acid", "3-hydroxypentanoic acid", "2-hydroxypentanoic acid", "Pentanoic acid", "A", "HO at C-4 from COOH end"),
    ("Paper chromatography is an example of:", "Partition chromatography", "Adsorption chromatography", "Thin layer chromatography", "None", "A", "Paper chromatography is partition type"),
    ("Which of the following alkanes cannot be made in good yield by Wurtz reaction?", "n-Heptane", "n-Butane", "n-Hexane", "Ethane", "A", "Wurtz gives only even carbon alkanes"),
    ("The most suitable reagent for the conversion of R-CH2OH -> R-CHO is:", "PCC (Pyridinium chlorochromate)", "KMnO4", "CrO3", "None", "A", "PCC oxidizes to aldehyde"),
    ("Which of the following is an electrophile?", "BF3", "NH3", "H2O", "CH4", "A", "BF3 is electron-deficient, acts as electrophile"),
    ("The correct order of inductive effect of the groups -NH2, -OR, -F is:", "-NH2 < -OR < -F", "-F < -OR < -NH2", "-OR < -NH2 < -F", "None", "A", "More electronegative = stronger -I effect"),
    ("Resonance is not shown by:", "CH2=CH-CH2-CH3", "CH2=CH-CH=CH2", "C6H6", "None", "A", "No conjugation in CH2=CH-CH2-CH3"),
    
    # Haloalkanes, Alcohols, Phenols & Ethers
    ("SN1 reaction is fastest in:", "2-Chloro-2-methylpropane", "Chloromethane", "Chloroethane", "1-Chloropropane", "A", "Tertiary halide fastest in SN1"),
    ("When phenol is treated with excess bromine water, it gives:", "2,4,6-Tribromophenol", "Monobromophenol", "Dibromophenol", "No reaction", "A", "Excess bromine gives 2,4,6-tribromophenol"),
    ("The major product of dehydration of 2-butanol is:", "2-Butene (Saytzeff's rule)", "1-Butene", "Isobutene", "None", "A", "More substituted alkene is major"),
    ("Reaction of HI with anisole yields:", "Phenol and Methyl iodide", "Benzene and Methane", "Iodobenzene", "No reaction", "A", "HI breaks ether to phenol + CH3I"),
    ("Which of the following will not undergo Reimer-Tiemann reaction?", "Nitrobenzene", "Phenol", "Salicylaldehyde", "None", "A", "NO2 deactivates ring"),
    ("Identification of primary, secondary, and tertiary alcohols is done by:", "Lucas Test", "Tollen's test", "FeCl3 test", "None", "A", "Lucas test uses ZnCl2/HCl"),
    ("Williamson synthesis is used to prepare:", "Ethers", "Esters", "Aldehydes", "Ketones", "A", "Williamson ether synthesis"),
    
    # Aldehydes, Ketones & Carboxylic Acids
    ("Cannizzaro reaction is not given by:", "Acetaldehyde (Has α-H)", "Formaldehyde", "Benzaldehyde", "None", "A", "α-H prevents Cannizzaro"),
    ("The product formed in Aldol condensation is:", "β-Hydroxy aldehyde", "α,β-unsaturated aldehyde", "Aldehyde dimer", "None", "A", "Aldol gives β-hydroxy aldehyde"),
    ("Which of the following gives Iodoform test?", "Acetophenone", "Benzophenone", "Formaldehyde", "Benzaldehyde", "A", "Methyl ketones give iodoform"),
    ("Hell-Volhard-Zelinsky (HVZ) reaction is used for:", "α-halogenation of acids", "β-halogenation", "γ-halogenation", "None", "A", "HVZ for α-halogenation"),
    ("Clemmensen reduction of a ketone is carried out in the presence of:", "Zn-Hg/HCl", "NaBH4", "LiAlH4", "None", "A", "Clemmensen reduces C=O to CH2"),
    ("The carboxylic acid that does not contain a -COOH group is:", "Picric acid", "Acetic acid", "Benzoic acid", "Formic acid", "A", "Picric acid is 2,4,6-trinitrophenol"),
    
    # Nitrogen Compounds & Biomolecules
    ("Hoffmann Bromamide degradation reaction is used to prepare:", "Primary amines", "Secondary amines", "Tertiary amines", "Quaternary amines", "A", "Hoffmann gives primary amine"),
    ("Which amine gives Carbylamine test?", "Aniline (Primary amines)", "Dimethylamine", "Trimethylamine", "None", "A", "Primary amines give carbylamine test"),
    ("The correct order of basic strength in aqueous solution is:", "(CH3)2NH > CH3NH2 > (CH3)3N", "CH3NH2 > (CH3)2NH > (CH3)3N", "(CH3)3N > (CH3)2NH > CH3NH2", "None", "A", "Steric hindrance reduces basicity in water"),
    ("Hinsberg's reagent is:", "Benzene sulphonyl chloride", "Benzoyl chloride", "Sulfonyl chloride", "None", "A", "Benzene sulfonyl chloride"),
    ("Glucose on prolonged heating with HI gives:", "n-Hexane", "n-Pentane", "n-Heptane", "None", "A", "HI reduces glucose to alkane"),
    ("Which of the following is a non-reducing sugar?", "Sucrose", "Glucose", "Maltose", "Lactose", "A", "Sucrose is non-reducing"),
    ("The linkage present in proteins is:", "Peptide linkage (-CONH-)", "Glycosidic linkage", "Phosphodiester linkage", "None", "A", "Peptide bonds link amino acids"),
    ("Deficiency of Vitamin B12 causes:", "Pernicious anaemia", "Scurvy", "Rickets", "Night blindness", "A", "B12 deficiency causes pernicious anemia"),
    ("Which nitrogenous base is present in DNA but not in RNA?", "Thymine", "Adenine", "Guanine", "Cytosine", "A", "DNA has Thymine, RNA has Uracil"),
]

# Get existing count
existing = MCQQuestion.objects.filter(chapter=c).count()
print(f"Existing PYQs in Organic Chemistry: {existing}")

# Delete and add new
MCQQuestion.objects.filter(chapter=c).delete()
for order, q in enumerate(oc_pyqs):
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

print(f"Added {len(oc_pyqs)} PYQs to Organic Chemistry")