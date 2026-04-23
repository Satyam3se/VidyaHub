import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Chemistry', grade=g)

# Physical Chemistry chapter
c_pc = Chapter.objects.get(subject=s, name='Physical Chemistry')
pc_pyqs = [
    ("The number of moles of hydrogen molecules required to produce 20 moles of ammonia through Haber's process is:", "10", "20", "30", "40", "C", "N2 + 3H2 -> 2NH3, need 30 moles H2"),
    ("Mixture of 2.3 g formic acid and 4.5 g oxalic acid is treated with conc. H2SO4. The evolved gaseous mixture is passed through KOH pellets. Weight (in g) of the remaining product at STP will be:", "1.4", "3.0", "2.8", "4.4", "C", "2.8g CO remaining after absorbing CO2"),
    ("The number of atoms in 0.1 mol of a triatomic gas is:", "6.026 x 10^22", "1.806 x 10^23", "3.6 x 10^23", "1.8 x 10^22", "B", "0.1 x 3 x 6.022 x 10^23 = 1.806 x 10^23"),
    ("Concentrated aqueous sulphuric acid is 98% H2SO4 by mass and has a density of 1.80 g/mL. Volume of acid required to make 1 liter of 0.1 M H2SO4 solution is:", "11.10 mL", "16.65 mL", "22.20 mL", "5.55 mL", "D", "5.55 mL acid needed"),
    ("Which has the maximum number of molecules among the following?", "44g CO2", "48g O3", "8g H2", "64g SO2", "C", "8g H2 has most molecules"),
    ("For the reaction, 2Cl(g) -> Cl2(g), the correct option is:", "ΔH > 0, ΔS > 0", "ΔH < 0, ΔS < 0", "ΔH < 0, ΔS > 0", "ΔH > 0, ΔS < 0", "B", "Bond formation releases heat, entropy decreases"),
    ("Under isothermal conditions, for a reversible process, the work done by an ideal gas is:", "w = -nRT ln(V2/V1)", "w = PΔV", "w = q", "w = 0", "A", "Isothermal work formula"),
    ("For a sample of perfect gas when its pressure is changed isothermally from Pi to Pf, the entropy change is given by:", "ΔS = nR ln(Pi/Pf)", "ΔS = nR ln(Pf/Pi)", "ΔS = nRT ln(Pi/Pf)", "ΔS = RT ln(Pi/Pf)", "A", "Entropy change formula for isothermal process"),
    ("The bond dissociation energies of X2, Y2 and XY are in the ratio of 1 : 0.5 : 1. ΔH for the formation of XY is -200 kJ/mol. The bond dissociation energy of X2 will be:", "200 kJ/mol", "800 kJ/mol", "100 kJ/mol", "400 kJ/mol", "B", "800 kJ/mol"),
    ("Which of the following is an intensive property?", "Enthalpy", "Entrophy", "Specific heat", "Volume", "C", "Specific heat is intensive"),
    ("Which of the following salts will give highest pH in water?", "KCl", "NaCl", "Na2CO3", "CuSO4", "C", "Na2CO3 is basic"),
    ("The solubility of BaSO4 in water is 2.42 x 10^-3 g/L at 298 K. The value of its solubility product (Ksp) will be (Molar mass of BaSO4 = 233 g/mol):", "1.08 x 10^-10 mol^2 L^-2", "1.08 x 10^-12 mol^2 L^-2", "1.08 x 10^-14 mol^2 L^-2", "1.08 x 10^-8 mol^2 L^-2", "A", "Ksp = (1.04 x 10^-5)^2 = 1.08 x 10^-10"),
    ("For the reaction N2(g) + 3H2(g) <=> 2NH3(g), Kp/Kc is equal to:", "RT", "(RT)^-2", "(RT)^2", "RT^-1", "B", "Kp/Kc = (RT)^-Δn = (RT)^-2"),
    ("The pH of 0.01 M NaOH solution will be:", "2", "12", "9", "11", "B", "pH = 14 - pOH = 14 - 2 = 12"),
    ("The conjugate acid of NH2- is:", "NH3", "NH4+", "NH2OH", "N2H4", "A", "NH2- + H+ -> NH3"),
    ("0.1 M Na2CO3 solution has pH:", "13", "12.5", "11", "9", "B", "pH = 12.5 (basic salt)"),
    ("The species that acts as a Lewis acid is:", "NH3", "H2O", "BF3", "OH-", "C", "BF3 is electron pair acceptor"),
    ("Buffer solution has pH = 9. If pKa = 4.5, then [salt]/[acid] ratio is:", "3162", "316.2", "3.162", "31.62", "A", "10^(pH-pKa) = 10^4.5 = 31623"),
    ("For a weak acid HA with Ka = 1 x 10^-5, pH of 0.1 M solution is:", "2.5", "2", "3", "4", "C", "pH = (1/2)(pKa - logC) = 3"),
    ("Oxidation number of Cr in K2Cr2O7 is:", "+6", "+3", "+5", "+7", "A", "Cr in dichromate is +6"),
    ("Oxidation number of Mn in MnO4- is:", "+7", "+6", "+5", "+8", "A", "Mn in permanganate is +7"),
    ("Reducing agent is a substance that:", "Gains electrons", "Loses electrons", "Neither", "Both", "B", "Reducing agent loses electrons"),
    ("In which compound, oxidation number of oxygen is -2?", "O2", "H2O2", "OF2", "Na2O", "B", "Peroxide has oxygen as -2"),
    ("The number of oxidation states exhibited by oxygen are:", "2", "3", "4", "5", "B", "O shows -2, -1, 0"),
    ("Standard enthalpy of formation of CO2 is:", "-393.5 kJ/mol", "+393.5 kJ/mol", "0 kJ/mol", "100 kJ/mol", "A", "Exothermic formation"),
    ("Heat required to raise temperature of 1kg water by 1K is:", "4.18 J", "4.18 kJ", "418 J", "4.18 J", "B", "Specific heat = 4.18 kJ/kg.K"),
    ("At absolute zero, entropy of perfect crystalline substance is:", "Zero", "Maximum", "Minimum", "Infinite", "A", "Third law of thermodynamics"),
    ("For a cyclic process, ΔU is:", "Zero", "Positive", "Negative", "Depends", "A", "Internal energy is state function"),
    ("Work done in adiabatic expansion is equal to:", "q", "ΔU", "Zero", "PV", "B", "Adiabatic: w = ΔU"),
    ("Cp - Cv for ideal gas is equal to:", "R", "2R", "R/2", "3R", "A", "Cp - Cv = R"),
    ("In free expansion of gas, w equals:", "R", "Zero", "P", "V", "B", "Free expansion: w = 0"),
]

# Add to Physical Chemistry chapter
for chapter, pyqs in [(c_pc, pc_pyqs)]:
    MCQQuestion.objects.filter(chapter=chapter).delete()
    for order, q in enumerate(pyqs):
        MCQQuestion.objects.create(
            chapter=chapter,
            question_text=q[0],
            option_a=q[1],
            option_b=q[2],
            option_c=q[3],
            option_d=q[4],
            correct_option=q[5],
            explanation=q[6],
            order=order
        )
    print(f"Added {len(pyqs)} PYQs to Physical Chemistry")

# Add Atomic Structure PYQs to Structure of Atom chapter
c_sa = Chapter.objects.get(subject=s, name='Structure of Atom')
sa_pyqs = [
    ("The number of angular nodes and radial nodes of 3p orbital are:", "1, 1", "1, 2", "2, 1", "3, 1", "A", "3p has 1 angular, 1 radial node"),
    ("Based on equation E = -2.178 x 10^-18 J (Z^2/n^2), certain conclusions are written. Which of them is not correct?", "Larger n means larger orbit radius", "Equation can be used to calculate change in energy", "For n=1, electron has more negative energy than n=6", "Negative sign means electron is bound to nucleus", "C", "n=1 has more negative energy"),
    ("Who modified Bohr's theory by introducing elliptical orbits?", "Rutherford", "Thomson", "Sommerfeld", "Hund", "C", "Sommerfeld introduced elliptical orbits"),
    ("The energy of second Bohr orbit of the hydrogen atom is -328 kJ/mol; hence the energy of fourth Bohr orbit would be:", "-41 kJ/mol", "-82 kJ/mol", "-164 kJ/mol", "-1312 kJ/mol", "B", "E4 = -328/4 = -82 kJ/mol"),
    ("The orientation of an atomic orbital is governed by:", "Principal quantum number", "Azimuthal quantum number", "Spin quantum number", "Magnetic quantum number", "D", "Magnetic quantum number defines orientation"),
    ("Angular momentum of electron in 'd' orbital is:", "h/π", "√2 h/π", "√3 h/π", "√6 h/π", "C", "d orbital has l=2, ml = √(l(l+1))h = √6h/π"),
    ("Maximum number of electrons in 'd' subshell is:", "2", "6", "10", "14", "C", "d subshell can hold 10 electrons"),
    ("Which quantum number defines the shape of an orbital?", "Principal", "Azimuthal", "Spin", "Magnetic", "B", "Azimuthal quantum number defines shape"),
    ("The wave function for a 1s electron in hydrogen atom is:", "Ae^-r/a0", "Are^-r/a0", "A(2-r/a0)e^-r/a0", "Ae^r/a0", "A", "1s wave function"),
    ("Probability of finding electron in 1s orbital is maximum at:", "Nucleus", "r = a0", "r = 0.529 Å", "At infinity", "B", "Maximum at r = a0 (Bohr radius)"),
    ("The spin quantum number describes:", "Shape", "Energy", "Orientation of spin", "Orbital", "C", "Spin quantum number (ms) describes electron spin"),
    ("Rutherford's alpha particle scattering experiment proved:", "Electron exists", "Nucleus exists", "Neutron exists", "Proton exists", "B", "Experiment proved existence of nucleus"),
    (" Cathode ray experiment shows:", "Electron has mass", "Electron has negative charge", "Both A and B", "Electron has positive charge", "C", "Cathode rays show electron properties"),
    ("Canal rays are:", "Electrons", "Protons", "Positive ions", "Neutrons", "C", "Canal rays are positive ions"),
    ("Atomic number is number of:", "Electrons", "Protons", "Neutrons", "Nucleons", "B", "Atomic number = number of protons"),
    ("Mass number is number of:", "Protons only", "Neutrons only", "Protons + Neutrons", "Electrons + Protons", "C", "Mass number = protons + neutrons"),
    ("Isotope has same:", "Atomic mass", "Atomic number", "Both", "None", "B", "Isotopes have same proton number"),
    ("Isobar has same:", "Atomic mass", "Atomic number", "Both", "None", "A", "Isobars have same mass number"),
    ("Which has no neutron?", "H1", "H2", "H3", "He4", "A", "Protium (H1) has no neutron"),
    ("Moseley's law is related to:", "X-rays", "Radio waves", "UV rays", "Gamma rays", "A", "Moseley studied X-rays"),
    ("Photoelectric effect was explained by:", "Einstein", "Rutherford", "Thomson", "Planck", "A", "Einstein explained photoelectric effect"),
    ("Photon has:", "Zero rest mass", "Energy", "Momentum", "All", "D", "Photon has energy and momentum"),
    ("De Broglie wavelength of electron is:", "h/mv", "mv/h", "h/m", "m/hv", "A", "λ = h/mv"),
    ("Uncertainty principle was given by:", "Heisenberg", "Schrodinger", "Dirac", "Pauli", "A", "Heisenberg uncertainty principle"),
    ("If Δx is minimum, then Δp is:", "Minimum", "Maximum", "Zero", "Infinite", "B", "Δx.Δp ≥ h/4π"),
    ("The orbital with n=2, l=1 is:", "2s", "2p", "2d", "2f", "B", "n=2, l=1 is 2p orbital"),
    ("Maximum number of orbitals in n=2 is:", "2", "4", "6", "8", "B", "n=2 can have 4 orbitals"),
    ("Pauli exclusion principle states:", "Electrons repel", "No two electrons can have same quantum numbers", "Electrons attract", "None", "B", "Pauli exclusion principle"),
    ("Hund's rule is about:", "Orbital filling", "Electron spin", "Both", "None", "A", "Hund's rule for orbital filling"),
    ("s-orbital can hold:", "1 electron", "2 electrons", "6 electrons", "8 electrons", "B", "s-orbital can hold 2 electrons"),
    ("p-orbital can hold:", "2 electrons", "4 electrons", "6 electrons", "8 electrons", "C", "p-orbitals can hold 6 electrons"),
]

for chapter, pyqs in [(c_sa, sa_pyqs)]:
    MCQQuestion.objects.filter(chapter=chapter).delete()
    for order, q in enumerate(pyqs):
        MCQQuestion.objects.create(
            chapter=chapter,
            question_text=q[0],
            option_a=q[1],
            option_b=q[2],
            option_c=q[3],
            option_d=q[4],
            correct_option=q[5],
            explanation=q[6],
            order=order
        )
    print(f"Added {len(pyqs)} PYQs to Structure of Atom")

print(f"\nTotal added NEET Physical Chemistry PYQs: {len(pc_pyqs) + len(sa_pyqs)}")