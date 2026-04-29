import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Physics', grade=g)
c = Chapter.objects.get(subject=s, name='Thermodynamics')

td_pyqs = [
    ("Which statement is not true? A) Isothermal: Temp constant B) Adiabatic: PV^γ = C C) Isochoric: Pressure constant D) Adiabatic: Insulated", "Isochoric: Pressure constant", "Isothermal: Temp constant", "Adiabatic: PV^γ = C", "Adiabatic: Insulated", "C", "Isochoric means constant volume, not pressure"),
    ("Work done during expansion of gas from V1 to V2 in vacuum is:", "P(V2-V1)", "Zero", "Infinite", "V2/V1", "B", "Free expansion against zero pressure: w=0"),
    ("For reaction 2Cl(g) → Cl2(g), signs of ΔH and ΔS are:", "+, +", "-, -", "-, +", "+, -", "B", "Exothermic (-): heat released, Entropy decreases (-)"),
    ("One mole ideal gas does 6R Joules work adiabatically. If γ=5/3, final temp is:", "T-2.4", "T+4", "T-4", "T+2.4", "C", "Adiabatic work = nRΔT/(γ-1) = 6R, so ΔT = -4"),
    ("Which is an intensive property?", "Enthalpy", "Internal Energy", "Temperature", "Volume", "C", "Temperature is intensive"),
    ("In reversible isothermal expansion of ideal gas, ΔU is:", "Positive", "Negative", "Zero", "∞", "C", "For isothermal ideal gas, ΔU=0"),
    ("Unit of entropy is:", "JK⁻¹mol⁻¹", "J mol⁻¹", "J g⁻¹", "JK mol⁻¹", "A", "Entropy per mole has SI unit JK⁻¹mol⁻¹"),
    ("For a spontaneous process, ΔStotal must be:", "> 0", "< 0", "Zero", "1", "A", "Second law: ΔStotal > 0 for spontaneous"),
    ("Adiabatic compressibility of ideal gas at pressure P is:", "γP", "1/P", "1/(γP)", "P/γ", "C", "Compressibility β = 1/(γP) for adiabatic"),
    ("Bond dissociation energy of F2 is less than Cl2 because of:", "High Electronegativity", "Lone pair repulsion", "Small size", "Both B and C", "D", "Lone pair repulsion in F2"),
    ("System absorbs 10 kJ heat, does 4 kJ work. ΔU is:", "14 kJ", "6 kJ", "-6 kJ", "40 kJ", "B", "ΔU = q - w = 10 - 4 = 6 kJ"),
    ("Which process has ΔS negative?", "Melting of Ice", "Boiling of Water", "Crystallization", "Expansion of Gas", "C", "Crystallization decreases entropy"),
    ("Efficiency of Carnot engine working between 300K and 600K is:", "25%", "50%", "75%", "100%", "B", "η = 1 - Tc/Th = 1 - 300/600 = 0.5 = 50%"),
    ("ΔG° related to K as:", "-RT ln K", "RT ln K", "RT log K", "-RT log K", "A", "ΔG° = -RT ln K"),
    ("Heat of combustion is always:", "Positive", "Negative", "Zero", "Neutral", "B", "Combustion releases heat: always negative"),
    ("During adiabatic process, gas density doubled. If γ=1.5, pressure increases by:", "2 times", "2.82 times", "4 times", "1.41 times", "B", "P2/P1 = (ρ2/ρ1)^γ = 2^1.5 = 2.82"),
    ("Molar heat capacity of water at Cp = 75 J K⁻¹ mol⁻¹. Heat for 100g water raised by 10K is:", "4.2 kJ", "7.5 kJ", "41.6 kJ", "1.2 kJ", "A", "q = 100g × 4.18 J/gK × 10K = 4.18 kJ ≈ 4.2 kJ"),
    ("For ideal gas, Cp - Cv equals:", "R", "R/2", "2R", "R²", "A", "Cp - Cv = R for ideal gas"),
    ("Reaction spontaneous at all temperatures if:", "ΔH < 0, ΔS > 0", "ΔH > 0, ΔS < 0", "ΔH > 0, ΔS > 0", "ΔH < 0, ΔS < 0", "A", "ΔH < 0 and ΔS > 0 makes ΔG < 0 at all T"),
    ("Slope of adiabatic P-V curve is:", "Same as Isothermal", "γ × Isothermal", "1/γ × Isothermal", "Zero", "B", "Adiabatic curve is γ times steeper than isothermal"),
    ("Entropy of perfectly crystalline substance is zero at:", "0°C", "0 K", "273 K", "100°C", "B", "Third law: entropy = 0 at absolute zero"),
    ("Hess's Law is based on:", "Law of mass action", "First Law of Thermo", "Second Law of Thermo", "Equilibrium", "B", "Hess's Law: enthalpy is state function - First Law"),
    ("Internal energy of ideal gas depends only on:", "Pressure", "Volume", "Temperature", "Molecular size", "C", "U = nCvT depends only on T"),
    ("Work done in isochoric process is:", "Positive", "Negative", "Zero", "PΔV", "C", "Isochoric: ΔV = 0, so w = 0"),
    ("ΔH and ΔU are related by:", "ΔH = ΔU + Δn_g RT", "ΔU = ΔH + Δn_g RT", "ΔH = ΔU - Δn_g RT", "ΔH = ΔU + PΔT", "A", "ΔH = ΔU + Δn_g RT"),
    ("In cyclic process, net work is:", "Zero", "Area of PV loop", "Q", "ΔU", "B", "Net work = area enclosed by loop"),
    ("Which ΔHf° is taken as zero?", "H2O(l)", "Fe(s)", "CO2(g)", "NH3(g)", "B", "Standard enthalpy of formation of elements in standard state = 0"),
    ("Coefficient of performance of refrigerator is:", "Q1/W", "Q2/W", "W/Q2", "T1/T2", "A", "COP = Ql/W = Qh/W × (Th/Tl) formula"),
    ("For monoatomic gas, γ is:", "1.40", "1.66", "1.33", "1.00", "B", "For monoatomic: γ = Cp/Cv = 5/3 ≈ 1.66"),
    ("Atomicity of gas can be determined from:", "Cp only", "Cv only", "Cp/Cv", "Density", "C", "γ = Cp/Cv gives atomicity"),
]

# Get existing
existing = MCQQuestion.objects.filter(chapter=c).count()
max_order = 0
for q in MCQQuestion.objects.filter(chapter=c):
    if q.order > max_order:
        max_order = q.order

# Add
for order, q in enumerate(td_pyqs):
    MCQQuestion.objects.create(
        chapter=c,
        question_text=q[0],
        option_a=q[1],
        option_b=q[2],
        option_c=q[3],
        option_d=q[4],
        correct_option=q[5],
        explanation=q[6],
        order=existing + order + 1
    )

print(f"Added {len(td_pyqs)} PYQs to Thermodynamics")