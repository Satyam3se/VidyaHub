import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Biology', grade=g)
c = Chapter.objects.get(subject=s, name='Ecology and Environment')

pyqs = [
    ("Ecology is study of:", "Organisms and environment", "Organisms only", "Environment only", "None", "A", "Interactions"),
    ("Ecosystem includes:", "Biotic factors", "Abiotic factors", "Both", "None", "C", "All components"),
    ("Producers are:", "Autotrophs", "Heterotrophs", "Both", "None", "A", "Make their own food"),
    ("Consumers are:", "Autotrophs", "Heterotrophs", "Both", "None", "B", "Depend on others"),
    ("Decomposers are:", "Fungi", "Bacteria", "Both", "None", "C", "Break down dead matter"),
    ("Food chain shows:", "Energy flow", "Matter flow", "Both", "None", "C", "Energy and matter"),
    ("Food web is:", "Interconnected food chains", "Single chain", "Both", "None", "A", "Complex feeding"),
    ("Primary productivity is:", "Rate of biomass production", "Amount of biomass", "Both", "None", "A", "Rate of production"),
    ("Greenhouse gases are:", "CO2", "CH4", "Both A and B", "None", "C", "Carbon dioxide and methane"),
    ("Global warming is due to:", "Greenhouse gases", "Ozone depletion", "Both", "None", "A", "Greenhouse effect"),
    ("Ozone layer is in:", "Troposphere", "Stratosphere", "Mesosphere", "None", "B", "Stratospheric ozone"),
    ("Acid rain is due to:", "SO2", "NO2", "Both A and B", "None", "C", "Sulfur and nitrogen oxides"),
    ("Eutrophication is:", "Nutrient enrichment", "Nutrient depletion", "Both", "None", "A", "Excess nutrients"),
    ("Biomagnification is:", "Toxin accumulation", "Nutrient accumulation", "Both", "None", "A", "Toxin increase in food chain"),
    ("Endangered species need:", "Protection", "Conservation", "Both", "None", "C", "Protection and conservation"),
    ("Wildlife protection act is:", "1972", "1980", "1986", "1972", "A", "Indian Wildlife Protection Act"),
    ("Biodiversity is:", "Species diversity", "Genetic diversity", "Both", "None", "C", "Variety of life"),
    ("Hotspots are:", "High biodiversity areas", "Low biodiversity", "Both", "None", "A", "Ecologically rich areas"),
    ("Niche is:", "Role of species", "Place of species", "Both", "None", "C", "Role and place"),
    ("Predator-prey relationship is:", "Controls population", "Increases population", "Both", "None", "A", "Population control"),
    ("Symbiosis is:", "Close relationship", "No relationship", "Both", "None", "A", "Living together"),
("Commensalism one benefits:", "Both", "One benefits only", "None", "B", "One benefits no effect on other", "Commensalism benefits one only"),
    ("Parasitism is:", "One benefits", "Both benefits", "None", "A", "One benefits at other's cost", "Parasitism benefits one at cost of other"),
    ("Mutualism is:", "Both benefits", "One benefits", "None", "A", "Both benefit", "Mutualism benefits both"),
    ("Nitrogen cycle has:", "N2 fixation", "Denitrification", "Both", "None", "C", "Fixation and release"),
    ("Carbon cycle includes:", "Photosynthesis", "Respiration", "Both", "None", "C", "Carbon flow"),
    ("Water cycle is:", "Evaporation", "Precipitation", "Both", "None", "C", "Water movement"),
    ("Ecological pyramid is:", "Energy", "Number", "Biomass", "All", "D", "Various pyramids"),
    ("10% rule is:", "Energy transfer", "Biomass transfer", "Both", "None", "A", "10% energy transfer"),
    ("Succession is:", "Community change", "No change", "Both", "None", "A", "Gradual change"),
]

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

print(f"Added {len(pyqs)} PYQs to Ecology and Environment")