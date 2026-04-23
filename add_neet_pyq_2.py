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

neet_pyqs = [
    ("Five kingdom system of classification suggested by R.H. Whittaker is not based on:", "Presence or absence of a well-defined nucleus", "Mode of reproduction", "Mode of nutrition", "Complexity of body organization", "A", "Whittaker system was based on mode of nutrition, reproduction and organization"),
    ("Organisms living in salty areas are called:", "Methanogens", "Halophiles", "Heliophytes", "Thermoacidophiles", "B", "Halophiles live in salty areas"),
    ("Naked cytoplasm, multinucleated and saprophytic are the characteristics of:", "Monerans", "Protists", "Fungi", "Slime molds", "D", "Slime molds have these characteristics"),
    ("An association between roots of higher plants and fungi is called:", "Lichen", "Fern", "Mycorrhiza", "BGA", "C", "Mycorrhiza is fungus-root association"),
    ("A dikaryon is formed when:", "Meiosis is arrested", "The two haploid cells do not fuse immediately", "Cytoplasm does not fuse", "None of the above", "B", "Dikaryon forms when cells don't fuse after plasmogamy"),
    ("Contagium vivum fluidum was proposed by:", "D.J. Ivanowsky", "M.W. Beijerinck", "Stanley", "Robert Hooke", "B", "Beijerinck proposed this term"),
    ("The association of algae and fungi is known as:", "Lichen", "Mycorrhiza", "Biocontrol agent", "Mycoses", "A", "Lichen is algae-fungi association"),
    ("Which of the following are found in extreme saline conditions?", "Eubacteria", "Cyanobacteria", "Mycobacteria", "Archaebacteria", "D", "Archaebacteria live in extreme saline conditions"),
    ("Viroids differ from viruses in having:", "DNA molecules without protein coat", "RNA molecules with protein coat", "RNA molecules without protein coat", "DNA molecules with protein coat", "C", "Viroids have RNA without protein coat"),
    ("The cyanobacteria are also referred to as:", "Protists", "Golden algae", "Slime moulds", "Blue-green algae", "D", "Cyanobacteria are blue-green algae"),
    ("Which kingdom includes unicellular eukaryotes?", "Monera", "Protista", "Fungi", "Plantae", "B", "Protista has unicellular eukaryotes"),
    ("Methanogens belong to:", "Eubacteria", "Archaebacteria", "Protista", "Fungi", "B", "Methanogens are Archaebacteria"),
    ("The cell wall of fungi is composed of:", "Cellulose", "Chitin", "Peptidoglycan", "Pectin", "B", "Fungal cell wall has chitin"),
    ("Which organism is known as 'Joker of plant kingdom'?", "Mycoplasma", "Virus", "Viroid", "Prion", "A", "Mycoplasma is called joker"),
    ("Red tides are caused by:", "Diatoms", "Dinoflagellates", "Green algae", "Blue-green algae", "B", "Dinoflagellates cause red tides"),
    ("Causal agent of Mad Cow Disease is:", "Virus", "Viroid", "Prion", "Bacteria", "C", "Prions cause Mad Cow Disease"),
    ("Diatomaceous earth is formed by:", "Diatoms", "Dinoflagellates", "Green algae", "Brown algae", "A", "Diatomaceous earth from diatoms"),
    ("Sleeping sickness is caused by:", "Leishmania", "Trypanosoma", "Plasmodium", "Entamoeba", "B", "Trypanosoma causes sleeping sickness"),
    ("Kingdom Monera includes:", "Fungi", "Algae", "Bacteria", "Protozoa", "C", "Monera includes bacteria"),
    ("Sexual cycle is absent in which fungi group?", "Ascomycetes", "Basidiomycetes", "Deuteromycetes", "Zygomycetes", "C", "Deuteromycetes have no sexual cycle"),
    ("Protein rich layer in Euglenoids is:", "Cell wall", "Pellicle", "Cyst", "Membrane", "B", "Euglenoids have pellicle"),
    ("Heterocyst is found in:", "Nostoc", "Spirogyra", "Ulothrix", "Chlamydomonas", "A", "Nostoc has heterocysts for nitrogen fixation"),
    ("Viruses are:", "Autotrophs", "Saprotrophs", "Obligate parasites", "Phototrophs", "C", "Viruses are obligate parasites"),
    ("Potato spindle tuber disease is caused by:", "Virus", "Viroid", "Prion", "Bacteria", "B", "Viroids cause this disease"),
    ("Fungi causing rust in wheat is:", "Uromyces", "Puccinia", "Alternaria", "Claviceps", "B", "Puccinia causes wheat rust"),
    ("Which are the chief producers in oceans?", "Diatoms", "Dinoflagellates", "Green algae", "Brown algae", "A", "Diatoms are chief producers"),
    ("Genetic material in TMV is:", "ssDNA", "dsDNA", "ssRNA", "dsRNA", "C", "TMV has single-stranded RNA"),
    ("Smallest living cell without cell wall is:", "Bacteria", "Mycoplasma", "Virus", "Prion", "B", "Mycoplasma lacks cell wall"),
    ("Sac-fungi is the common name for:", "Zygomycetes", "Ascomycetes", "Basidiomycetes", "Deuteromycetes", "B", "Ascomycetes are sac-fungi"),
    ("Symbiotic association of Algae and Fungi is known as:", "Mycorrhiza", "Lichen", "Bioluminescence", "Decomposition", "B", "Lichens are algae-fungi symbiosis"),
]

for order, q in enumerate(neet_pyqs):
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

print(f"Added {len(neet_pyqs)} PYQs to Diversity in Living World")