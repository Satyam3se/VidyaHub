import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Chemistry', grade=g)

# Check if Equilibrium chapter exists
try:
    c = Chapter.objects.get(subject=s, name='Equilibrium')
except Chapter.DoesNotExist:
    # Create chapter if not exists
    from main.models import Subject
    sub = Subject.objects.get(name='Chemistry', grade=g)
    c = Chapter.objects.create(subject=sub, name='Equilibrium', order=15)
    print("Created Equilibrium chapter")

eq_pyqs = [
    ("For the reaction N2(g) + 3H2(g) <=> 2NH3(g), the relation between Kp and Kc is:", "Kp = Kc(RT)^-2", "Kp = Kc(RT)^2", "Kp = Kc", "None", "A", "Kp = Kc(RT)^-Δn, Δn = -2"),
    ("Which of the following conditions will favor the maximum formation of product in A2(g) + B2(g) <=> X2(g); ΔrH = -X kJ?", "Low Temp, High Pressure", "High Temp, Low Pressure", "Low Temp, Low Pressure", "None", "A", "Exothermic: low T, fewer moles: high P"),
    ("The solubility of AgCl(s) with solubility product 1.6 x 10^-10 in 0.1 M NaCl solution would be:", "1.6 x 10^-9 M", "1.6 x 10^-5 M", "1.6 x 10^-3 M", "None", "A", "s = Ksp/[Cl-] = 1.6 x 10^-10/0.1"),
    ("Which of the following is a conjugate acid-base pair?", "NH4+ / NH3", "HCl / Cl-", "H2O / OH-", "All", "A", "NH4+ is conjugate acid of NH3"),
    ("The pH of a 0.01 M NaOH solution is:", "12", "10", "14", "11", "A", "pOH = 2, pH = 14-2 = 12"),
    ("Find the Ksp for Bi2S3 in terms of its molar solubility S:", "108 S^5", "27 S^4", "108 S^3", "None", "A", "Ksp = (2)^2(3)^3 S^5 = 108 S^5"),
    ("If the concentration of OH- ions in a solution is 10^-10 M, its pH will be:", "4", "10", "7", "6", "A", "pOH = 10, pH = 14-10 = 4"),
    ("According to Le Chatelier's principle, adding heat to a reversible exothermic reaction will:", "Shift equilibrium to left", "Shift equilibrium to right", "No effect", "None", "A", "Adding heat shifts away from heat"),
    ("The pH of a saturated solution of Ca(OH)2 is 9. The solubility product (Ksp) of Ca(OH)2 is:", "0.5 x 10^-15", "1 x 10^-13", "1 x 10^-15", "None", "A", "pOH = 5, [OH-] = 10^-5, Ksp = s^2 = 10^-15/2"),
    ("A buffer solution is prepared by mixing:", "Weak acid & its salt with strong base", "Strong acid & strong base", "Weak base & strong acid", "None", "A", "Weak acid + conjugate base forms buffer"),
    ("Which of the following salts will undergo anionic hydrolysis?", "Na2CO3", "NaCl", "Na2SO4", "None", "A", "CO3^2- is conjugate base of weak acid"),
    ("The dissociation constant of a weak acid is 1 x 10^-5. The pH of a 0.1 M solution of this acid is:", "3", "2.5", "4", "5", "A", "pH = (1/2)(pKa - logC) = (1/2)(5-1) = 2, wait: pH = 3"),
    ("In the reaction PCl5(g) <=> PCl3(g) + Cl2(g), the unit of Kp is:", "atm", "L atm mol^-1", "mol L^-1 atm^-1", "None", "A", "Kp has unit for gases"),
    ("Which of the following will not affect the state of equilibrium?", "Addition of a catalyst", "Change in concentration", "Change in pressure", "Change in temperature", "A", "Catalyst speeds both forward/reverse equally"),
    ("For the reaction H2 + I2 <=> 2HI, the equilibrium constant K is 50. What is K for HI <=> 1/2H2 + 1/2I2?", "1/√50", "√50", "1/50", "50", "A", "K' = K^(1/2) for reverse: 1/√50"),
    ("The ionic product of water (Kw) at 25°C is:", "1 x 10^-14", "1 x 10^-7", "1 x 10^-7", "None", "A", "Kw = [H+][OH-] = 10^-14"),
    ("Which has the highest pH?", "1 M Na2CO3", "1 M NaCl", "1 M NH4Cl", "None", "A", "Na2CO3 is basic (CO3^2- hydrolysis)"),
    ("The Henderson-Hasselbalch equation for an acidic buffer is:", "pH = pKa + log([Salt]/[Acid])", "pH = pKa + log([Acid]/[Salt])", "pOH = pKb + log([Salt]/[Base])", "None", "A", "pH = pKa + log([A-]/[HA])"),
    ("Solubility of MX2 type electrolyte is 0.5 x 10^-4 mol/L. Its Ksp is:", "5 x 10^-13", "1 x 10^-12", "5 x 10^-11", "None", "A", "Ksp = 4s^3 = 4 x (0.5 x 10^-4)^3 = 5 x 10^-13"),
    ("What is the pH of a 10^-8 M HCl solution?", "6.98 (Less than 7)", "7", "8", "6", "A", "pH between 6-7 due to water ions"),
    ("In which of the following equilibrium, Kp and Kc are not equal?", "PCl5 <=> PCl3 + Cl2", "H2 + I2 <=> 2HI", "N2 + 3H2 <=> 2NH3", "None", "A", "Δn ≠ 0, so Kp ≠ Kc"),
    ("Boron compounds behave as Lewis acids because of their:", "Electron deficient nature", "Electron rich nature", "Stable compounds", "None", "A", "Boron has only 6 valence electrons"),
    ("The solubility product of BaSO4 is 1.1 x 10^-10. In which of the following will it be least soluble?", "0.1 M Na2SO4", "0.1 M NaCl", "Distilled water", "None", "A", "Common ion SO4^2- reduces solubility"),
    ("If Qc > Kc, the reaction will proceed in the:", "Backward direction", "Forward direction", "No change", "None", "A", "Q > K means reverse reaction"),
    ("Hydrolysis of a salt of weak acid and weak base (CH3COONH4) is:", "Independent of concentration", "Dependent on concentration", "No hydrolysis", "None", "A", "Depends on Ka and Kb not concentration"),
    ("The compound that is not a Lewis acid is:", "NH3", "BF3", "AlCl3", "None", "A", "NH3 donates electron pair (Lewis base)"),
    ("Increasing the pressure on the system C(s) + H2O(g) <=> CO(g) + H2(g) will:", "Shift equilibrium to left", "Shift equilibrium to right", "No effect", "None", "A", "More moles on right, high P shifts left"),
    ("The degree of dissociation of a weak electrolyte increases with:", "Dilution (Ostwald's Law)", "Concentration", "Temperature decrease", "None", "A", "Ostwald dilution law"),
    ("For a reversible reaction, if the concentration of reactants is doubled, the equilibrium constant will:", "Remain the same", "Increase", "Decrease", "None", "A", "K is constant at given temperature"),
    ("Which indicator is most suitable for titration of NH4OH and HCl?", "Methyl orange", "Phenolphthalein", "Methyl red", "None", "A", "Strong acid-weak base titrated with methyl orange"),
]

# Get existing count
existing = MCQQuestion.objects.filter(chapter=c).count()
print(f"Existing PYQs in Equilibrium: {existing}")

# Delete and add new
MCQQuestion.objects.filter(chapter=c).delete()
for order, q in enumerate(eq_pyqs):
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

print(f"Added {len(eq_pyqs)} PYQs to Equilibrium")