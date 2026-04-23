import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Physics', grade=g)

# Laws of Motion
c = Chapter.objects.get(subject=s, name='Laws of Motion')
lom_pyqs = [
    ("Newton's first law defines:", "Inertia", "Force", "Momentum", "Velocity", "A", "First law defines inertia"),
    ("Momentum is:", "mv", "ma", "Fv", "None", "A", "p = mv product"),
    ("A body on frictionless surface has:", "100% inertia", "50% inertia", "Any %", "None", "A", "Inertia proportional to mass"),
    ("Coefficient of friction is:", "f/N", "fmg", "mg/N", "None", "A", "μ = f/N"),
    ("Block slides down when angle is:", "tan^-1(μ)", "sin^-1(μ)", "cos^-1(μ)", "None", "A", "θ = tan^-1(μ)"),
    ("Impulse equals area under:", "F-t graph", "F-x graph", "m-t graph", "None", "A", "Impulse = ∫F dt"),
    ("Rolling friction is:", "less than sliding", "greater", "equal", "None", "A", "rolling < sliding"),
    ("Rocket propulsion conserves momentum between:", "rocket and gases", "rocket and earth", "none", "None", "A", "rocket-gases momentum"),
    ("Action and reaction are:", "Equal and opposite", "equal", "same direction", "None", "A", "Newton's third law"),
    ("Frictional force opposes:", "Relative motion", "Absolute motion", "none", "none", "A", "relative motion"),
]

MCQQuestion.objects.filter(chapter=c).delete()
for order, q in enumerate(lom_pyqs):
    MCQQuestion.objects.create(chapter=c, question_text=q[0], option_a=q[1], option_b=q[2], option_c=q[3], option_d=q[4], correct_option=q[5], explanation=q[6], order=order)
print(f"Added {len(lom_pyqs)} to Laws of Motion")

# Thermodynamics
c = Chapter.objects.get(subject=s, name='Thermodynamics')
td_pyqs = [
    ("First law is:", "Conservation of energy", "Conservation of heat", "Conservation of work", "None", "A", "ΔQ = ΔU + ΔW"),
    ("Isothermal process:", "Constant T", "Constant P", "Zero T", "None", "A", "T constant"),
    ("Adiabatic:", "No heat exchange", "No work done", "Both", "None", "A", "q = 0"),
    ("Cp - Cv =:", "R", "2R", "0", "None", "A", "Cp - Cv = R"),
    ("Adiabatic follows:", "PV^γ = K", "PV = K", "P/V = K", "None", "A", "PV^γ = constant"),
    ("Condensation releases:", "Heat", "Absorbs heat", "No change", "None", "A", "Heat releases"),
    ("Efficiency =:", "W/Qh", "Q/W", "Qh/W", "None", "A", "η = W/Qh"),
    ("Carnot efficiency:", "1 - Tc/Th", "Tc/Th", "Th/Tc", "None", "A", "η = 1-Tc/Th"),
    ("Entropy increases in:", "Irreversible", "Reversible", "Constant", "None", "A", "ΔS > 0 irreversible"),
    ("For isolated system:", "ΔS increases", "ΔS decreases", "ΔS = 0", "None", "A", "ΔS ≥ 0"),
    ("Kelvin-Planck statement is about:", "Heat engine", "Refrigerator", "Both", "None", "A", "cannot be 100% efficient"),
    ("Clausius statement:", "Heat cannot flow cold to hot", "Heat flows cold to hot", "none", "none", "A", "heat engine statement"),
]

MCQQuestion.objects.filter(chapter=c).delete()
for order, q in enumerate(td_pyqs):
    MCQQuestion.objects.create(chapter=c, question_text=q[0], option_a=q[1], option_b=q[2], option_c=q[3], option_d=q[4], correct_option=q[5], explanation=q[6], order=order)
print(f"Added {len(td_pyqs)} to Thermodynamics")

# Electromagnetism
c = Chapter.objects.get(subject=s, name='Electromagnetism')
em_pyqs = [
    ("Coulomb's law for:", "Point charges", "Continuous", "Both", "None", "A", "F = kq1q2/r^2"),
    ("Electric field from point charge is:", "Radial", "Circular", "Elliptical", "None", "A", "radiates outward"),
    ("Capacitance depends on:", "Geometry and dielectric", "Voltage only", "Charge only", "None", "A", "C = εA/d"),
    ("Current is flow of:", "Electrons", "Protons", "Ions", "None", "A", "electron flow"),
    ("Ohm's law:", "V = IR", "P = IV", "R = V/I", "none", "A", "V = IR"),
    ("Resistance depends on:", "l, A, ρ", "only temperature", "only area", "none", "A", "R = ρl/A"),
    ("Magnetic field in solenoid:", "μ0nI", "μ0I/n", "nI/μ0", "none", "A", "B = μ0nI"),
    ("Force on charge:", "qvB sinθ", "qE", "both", "none", "A", "F = qvB sinθ"),
    ("Faraday's law:", "ε = -dΦ/dt", "V = IR", "F = qvB", "none", "A", "ε = -dΦ/dt"),
    ("Lenz's law is:", "Energy conservation", "Momentum conservation", "Both", "none", "A", "energy conservation"),
    ("Right hand rule gives:", "Direction of B", "Direction of F", "none", "none", "A", "direction of field"),
    ("Cyclotron works on:", "Resonance", "Reflection", "Both", "none", "A", "resonance principle"),
]

MCQQuestion.objects.filter(chapter=c).delete()
for order, q in enumerate(em_pyqs):
    MCQQuestion.objects.create(chapter=c, question_text=q[0], option_a=q[1], option_b=q[2], option_c=q[3], option_d=q[4], correct_option=q[5], explanation=q[6], order=order)
print(f"Added {len(em_pyqs)} to Electromagnetism")

# Optics
c = Chapter.objects.get(subject=s, name='Optics')
opt_pyqs = [
    ("Reflection law:", "i = r", "i = 90-r", "i + r = 90", "none", "A", "angle i = angle r"),
    ("Refractive index:", "sin i/sin r", "sin r/sin i", "i/r", "none", "A", "n = sin i/sin r"),
    ("Critical angle:", "r = 90°", "i = 90°", "n = 1", "none", "A", "r = 90°"),
    ("TIR requires:", "i > critical", "i < critical", "r > 90", "none", "A", "i > ic for TIR"),
    ("Lens maker formula:", "1/f = (n-1)(1/R1-1/R2)", "f = (n-1)(R1-R2)", "n = f/R", "none", "A", "lens formula"),
    ("Optical fiber on:", "TIR", "refraction", "both", "none", "A", "TIR in fiber"),
    ("Convex lens focal:", "Positive", "Negative", "Zero", "none", "A", "convex +f"),
    ("Young's slit shows:", "interference", "diffraction", "both", "none", "A", "interference pattern"),
    ("Diffraction proves:", "Wave nature", "Particle nature", "both", "none", "A", "wave nature"),
    ("Polarization proves:", "Transverse wave", "Longitudinal", "both", "none", "A", "transverse wave"),
    ("Compound microscope has:", "2 convex lenses", "1 convex + 1 concave", "2 concave", "none", "A", "2 convex lenses"),
    ("Astronomical telescope:", "2 convex", "convex + concave", "2 concave", "none", "A", "inverted image"),
]

MCQQuestion.objects.filter(chapter=c).delete()
for order, q in enumerate(opt_pyqs):
    MCQQuestion.objects.create(chapter=c, question_text=q[0], option_a=q[1], option_b=q[2], option_c=q[3], option_d=q[4], correct_option=q[5], explanation=q[6], order=order)
print(f"Added {len(opt_pyqs)} to Optics")

# Modern Physics
c = Chapter.objects.get(subject=s, name='Modern Physics')
mp_pyqs = [
    ("Photon given by:", "Planck", "Einstein", "Bohr", "none", "A", "Planck quantum"),
    ("Photoelectric equation:", "KE = hν - φ", "E = mc^2", "E = hν", "none", "A", "Kmax = hν - φ0"),
    ("Bohr model:", "circular orbits", "elliptical", "both", "none", "A", "circular orbits"),
    ("Energy of nth orbit:", "-13.6/n^2 eV", "-13.6n^2 eV", "13.6/n^2", "none", "A", "En = -13.6/n^2"),
    ("Ionization potential:", "13.6 eV", "10.2 eV", "3.4 eV", "none", "A", "13.6 eV"),
    ("Radioactivity:", "Spontaneous", "Induced", "both", "none", "A", "spontaneous decay"),
    ("Alpha particle:", "He2+", "electron", "photon", "none", "A", "He nucleus"),
    ("Beta emission is:", "electron", "proton", "neutron", "none", "A", "beta = electron"),
    ("Gamma rays:", "high energy photons", "electrons", "protons", "none", "A", "gamma = EM wave"),
    ("Half-life is:", "independent of initial amount", "dependent", "zero", "none", "A", "constant"),
    ("Nuclear fission releases:", "mass defect", "binding energy", "both", "none", "C", "E = Δmc^2"),
    ("De Broglie λ:", "h/mv", "mv/h", "h/m", "none", "A", "λ = h/p"),
    ("Uncertainty:", "ΔxΔp ≥ h/4π", "E = mc^2", "λ = h/p", "none", "A", "Heisenberg"),
    ("Photoelectric effect proves:", "particle nature", "wave nature", "both", "none", "A", "particle nature"),
    ("Bohr couldn't explain:", "fine structure", "zeeman effect", "stark effect", "none", "B", "magnetic effect"),
]

MCQQuestion.objects.filter(chapter=c).delete()
for order, q in enumerate(mp_pyqs):
    MCQQuestion.objects.create(chapter=c, question_text=q[0], option_a=q[1], option_b=q[2], option_c=q[3], option_d=q[4], correct_option=q[5], explanation=q[6], order=order)
print(f"Added {len(mp_pyqs)} to Modern Physics")

print("\nAll NEET Physics chapters updated!")