import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Chemistry', grade=g)
c = Chapter.objects.get(subject=s, name='Physical Chemistry')

pc_pyqs = [
    ("What is the oxidation number of Phosphorus in Ba(H2PO2)2?", "+1", "+2", "+3", "0", "A", "In hypophosphite, P is +1"),
    ("Which of the following is a colligative property?", "Osmotic Pressure", "Boiling Point", "Melting Point", "Density", "A", "Osmotic pressure is colligative"),
    ("The number of atoms per unit cell in a face-centered cubic (fcc) structure is:", "2", "4", "6", "8", "B", "FCC has 4 atoms per unit cell"),
    ("The device that converts the energy of combustion of fuels directly into electrical energy is:", "Fuel Cell", "Battery", "Electrolytic Cell", " Galvanic Cell", "A", "Fuel cell converts fuel energy to electricity"),
    ("If the rate of a reaction is k[A]^2[B], the overall order of the reaction is:", "2", "3", "4", "5", "B", "Overall order = 2+1 = 3"),
    ("The process of separating a crystalloid from a colloid by filtration through a semi-permeable membrane is:", "Dialysis", "Electrodialysis", "Filtration", "Centrifugation", "A", "Dialysis separates crystalloids"),
    ("The number of radial nodes in a 4s orbital is:", "1", "2", "3", "4", "C", "Nodes = n-l-1 = 4-0-1 = 3"),
    ("The number of molecules in 8.96 L of a gas at 0°C and 1 atm is:", "1.2 x 10^23", "2.4 x 10^23", "3.6 x 10^23", "4.8 x 10^23", "B", "8.96L = 0.4mol, molecules = 0.4 x 6.022 x 10^23"),
    ("For a cyclic process, the change in internal energy (ΔU) is:", "Zero", "Positive", "Negative", "Infinite", "A", "ΔU = 0 for cyclic process"),
    ("If the value of Ksp for CaF2 is 5.3 x 10^-11, its solubility in mol/L is:", "1.7 x 10^-4", "2.4 x 10^-4", "3.4 x 10^-4", "4.0 x 10^-4", "B", "s = (Ksp/4)^(1/3) = (1.325 x 10^-11)^(1/3)"),
    ("The unit of rate constant for a first-order reaction is:", "sec^-1", "L mol^-1 sec^-1", "mol L^-1 sec^-1", "M sec^-1", "A", "First order rate constant unit is sec^-1"),
    ("In the reaction MnO2 + 4HCl -> MnCl2 + 2H2O + Cl2, the oxidizing agent is:", "MnO2", "HCl", "MnCl2", "Cl2", "A", "MnO2 gets reduced, acts as oxidizing agent"),
    ("Schottky defect in crystals is observed when:", "Equal number of cations and anions are missing", "Only cations missing", "Only anions missing", "None", "A", "Schottky defect: equal cations + anions missing"),
    ("The boiling point of a 0.2 molal solution of a non-electrolyte in water is (Kb = 0.52):", "100.104°C", "100.052°C", "100.026°C", "100.208°C", "A", "ΔTb = 0.2 x 0.52 = 0.104"),
    ("On electrolysis of dilute sulphuric acid using Platinum electrodes, the product obtained at anode is:", "Oxygen gas", "Hydrogen gas", "Sulphur dioxide", "None", "A", "O2 evolved at anode"),
    ("Which orbital is represented by n=3, l=1?", "3s", "3p", "3d", "3f", "B", "n=3, l=1 represents 3p orbital"),
    ("A solution with pH = 2 is more acidic than one with pH = 6 by a factor of:", "100", "1000", "10,000", "100,000", "C", "pH 2 has H+ = 10^-2, pH 6 has 10^-6, ratio = 10000"),
    ("For an adiabatic process, which of the following is true?", "q = 0", "w = 0", "ΔU = 0", "None", "A", "Adiabatic: q = 0"),
    ("How many moles of Magnesium Phosphate Mg3(PO4)2 will contain 0.25 mole of oxygen atoms?", "1.56 x 10^-2", "3.125 x 10^-2", "6.25 x 10^-2", "1.25 x 10^-2", "B", "O atoms in Mg3(PO4)2 = 8, moles compound = 0.25/8 = 0.03125"),
    ("Which of the following is an example of an oil-in-water (O/W) emulsion?", "Milk", "Butter", "Cream", "Ghee", "A", "Milk is O/W emulsion"),
    ("The activation energy of a reaction can be determined from the slope of:", "ln k vs 1/T", "k vs T", "ln k vs T", "k vs 1/T", "A", "Arrhenius plot: ln k vs 1/T"),
    ("An element has a bcc structure with a cell edge of 288 pm. The atomic radius is:", "124.7 pm", "144 pm", "104.7 pm", "84.7 pm", "A", "For bcc: r = √3a/4 = 124.7 pm"),
    ("An ideal solution is formed when its components:", "Have zero enthalpy of mixing", "Have positive enthalpy", "Have negative enthalpy", "None", "A", "Ideal solution: ΔHmix = 0"),
    ("Specific conductance of an electrolytic solution decreases with:", "Dilution", "Concentration", "Temperature", "None", "A", "Dilution decreases specific conductance"),
    ("In which of the following reactions Kp = Kc?", "H2 + I2 = 2HI", "N2 + 3H2 = 2NH3", "2NO2 = N2O4", "None", "A", "Kp = Kc when Δn = 0"),
    ("The de-Broglie wavelength of a particle with mass m and velocity v is:", "λ = h/mv", "λ = mv/h", "λ = h/m", "λ = mv", "A", "de Broglie equation: λ = h/mv"),
    ("Oxidation state of Oxygen in F2O is:", "-2", "-1", "+2", "+1", "C", "OF2: O has +2 oxidation state"),
    ("Entropy is a measure of:", "Disorder/Randomness", "Order", "Energy", "Work", "A", "Entropy measures disorder"),
    ("Percentage of Carbon in urea (NH2CONH2) is approximately:", "10%", "20%", "30%", "40%", "B", "Carbon in urea ~20%"),
    ("The Van't Hoff factor (i) for a dilute solution of K2SO4 is:", "2", "3", "4", "1", "B", "K2SO4 dissociates into 3 ions"),
    ("A first-order reaction has a half-life of 69.3 seconds. The rate constant is:", "0.01 sec^-1", "0.1 sec^-1", "0.001 sec^-1", "1 sec^-1", "A", "k = 0.693/69.3 = 0.01 sec^-1"),
    ("Gold number is a measure of:", "Protective power of lyophilic colloid", "Size of colloid", "Charge on colloid", "None", "A", "Gold number measures protective power"),
    ("The coordination number of an atom in a hexagonal close-packed (hcp) structure is:", "6", "8", "12", "10", "C", "HCP coordination number is 12"),
    ("In a galvanic cell, the anode is:", "Negatively charged", "Positively charged", "Neutral", "None", "A", "Anode is negatively charged in galvanic cell"),
    ("The pH of 10^-8 M HCl solution is:", "6", "7", "Between 6 and 7", "8", "C", "pH between 6 and 7 due to water ions"),
    ("The bond energy of H-H is 436 kJ/mol. This is an:", "Exothermic value", "Endothermic value", "Neutral", "None", "A", "Bond energy is positive but released energy"),
    ("Total number of orbitals associated with n=3 is:", "9", "6", "3", "18", "A", "n=3 has n^2 = 9 orbitals"),
    ("Which is the strongest reducing agent in aqueous solution?", "Lithium (Li)", "Sodium (Na)", "Potassium (K)", "Magnesium (Mg)", "A", "Li is strongest reducing agent"),
    ("Raoult's law is applicable to:", "Dilute solutions of non-volatile solutes", "Concentrated solutions", "Gases", "Solids", "A", "Raoult's law for dilute solutions"),
    ("One mole of any gas at STP occupies:", "22.4 L", "11.2 L", "44.8 L", "2.24 L", "A", "1 mole = 22.4 L at STP"),
]

# Get existing PYQs count
existing = MCQQuestion.objects.filter(chapter=c).count()
print(f"Existing PYQs: {existing}")

# Delete and add new with these additional questions
for order, q in enumerate(pc_pyqs):
    MCQQuestion.objects.create(
        chapter=c,
        question_text=q[0],
        option_a=q[1],
        option_b=q[2],
        option_c=q[3],
        option_d=q[4],
        correct_option=q[5],
        explanation=q[6],
        order=existing + order
    )

print(f"Added {len(pc_pyqs)} more PYQs to Physical Chemistry")