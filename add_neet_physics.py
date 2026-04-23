import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Physics', grade=g)

# Get all Physics chapters
chapters = Chapter.objects.filter(subject=s)
print(f"Found {chapters.count()} Physics chapters:", [c.name for c in chapters])

# Create PYQs for each major chapter
all_pyqs = {
    "Mechanics": [
        ("Which of the following is the best example of simple harmonic motion?", "Simple pendulum", "Circular motion", "Uniform circular motion", "Projectile motion", "A", "Simple pendulum is SHM"),
        ("The dimension of universal gravitational constant G is:", "M^-1 L^3 T^-2", "M^-1 L^2 T^-1", "M L^3 T^-2", "None", "A", "G has dimension M^-1 L^3 T^-2"),
        ("A particle moves in a circle with constant speed. It has:", "No acceleration", "Radial acceleration", "Tangential acceleration", "None", "B", "Centripetal acceleration towards center"),
        ("Work done in moving a body against gravitational field is:", "Potential energy", "Kinetic energy", "Both", "None", "A", "Against gravity = PE"),
        ("A block of mass m slides down an inclined plane. The acceleration is:", "g sinθ", "g cosθ", "g", "None", "A", "a = g sinθ"),
        ("Impulse equals change in:", "Momentum", "Force", "Velocity", "Energy", "A", "Impulse = Δp"),
        ("For perfectly inelastic one-dimensional collision, the coefficient of restitution is:", "0", "1", "0.5", "None", "A", "e = 0 for perfectly inelastic"),
        ("Angular momentum is conserved when:", "No net torque", "No net force", "No work done", "None", "A", "L conserved when τ = 0"),
        ("The SI unit of work is:", "Joule", "Watt", "Newton", "None", "A", "Joule is SI unit"),
        ("Kinetic energy of a rotating body depends on:", "Mass", "Moment of inertia", "Both", "None", "C", "KE = 1/2 Iω^2"),
        ("Which has more kinetic energy: bullet or car? It depends on:", "Both mass and velocity", "Mass only", "Velocity only", "None", "A", "KE = 1/2 mv^2"),
        ("Escape velocity from Earth is:", "11.2 km/s", "7.9 km/s", "9.8 km/s", "None", "A", "11.2 km/s"),
        ("A mass m is rotated in a circle with constant angular velocity ω. The centripetal force is:", "mω^2r", "mrω^2", "mr/ω^2", "None", "A", "F = mω^2r = mv^2/r"),
        ("The period of a simple pendulum in a lift moving upward with acceleration a is:", "2π√(l/(g+a))", "2π√(l/g)", "2π√(l/(g-a))", "None", "A", "Effective g' = g+a"),
        ("Young's modulus is for:", "Tensile stress", "Bulk stress", "Shear stress", "None", "A", "Y = stress/strain"),
        ("Bernoulli's equation is based on:", "Conservation of energy", "Conservation of momentum", "Conservation of mass", "None", "A", "Bernoulli energy equation"),
        ("The terminal velocity is achieved when:", "Drag force = Weight", "Drag force > Weight", "Drag force < Weight", "None", "A", "Net force zero at terminal velocity"),
        ("In projectile motion, total time of flight is:", "2u sinθ/g", "u sinθ/g", "u cosθ/g", "None", "A", "T = 2usinθ/g"),
        ("The banking of roads helps to provide:", "Required centripetal force", "Additional friction", "Both", "None", "A", "Banking provides centripetal force"),
        ("The nature of central force is:", "Conservative", "Non-conservative", "Both", "None", "A", "Central forces are conservative"),
        ("In elastic collision, which is conserved?", "Both KE and momentum", "Only KE", "Only momentum", "None", "A", "KE and momentum conserved"),
        ("Rolling without slipping has:", "v = ωr", "v > ωr", "v < ωr", "None", "A", "v = ωr for pure rolling"),
        ("The minimum speed to orbit Earth is:", "7.9 km/s", "11.2 km/s", "9.8 km/s", "None", "A", "First cosmic velocity"),
        ("In simple harmonic motion, acceleration is proportional to:", "-displacement", "velocity", "time", "None", "A", "a = -ω^2x"),
        ("A satellite orbiting Earth has:", "Centripetal force from gravity", "Tangential force", "No force", "None", "A", "Gravity provides centripetal force"),
        ("Conservation of linear momentum applies when:", "No external force", "No internal force", "Force is zero", "None", "A", "External force zero"),
        ("In SHM, the velocity is maximum at:", "Mean position", "Extreme position", "Both same", "None", "A", "v max at x=0"),
        ("The work-energy theorem states:", "W = ΔKE", "W = ΔPE", "W = Fd", "None", "A", "Work = change in KE"),
        ("Center of mass of uniform rod is at:", "Midpoint", "One-third", "Two-thirds", "None", "A", "Uniform rod CM at midpoint"),
        ("For a system of particles, center of mass moves like:", "A single particle with total mass", "Two particles", "Three particles", "None", "A", "CM moves as single particle"),
    ],
    "Kinematics": [
        ("A ball is thrown upward. Its velocity at highest point is:", "Zero", "Maximum", " Constant", "None", "A", "v = 0 at highest point"),
        ("The slope of displacement-time graph gives:", "Velocity", "Acceleration", "Jerk", "None", "A", "dx/dt = v"),
        ("A car starts from rest with constant acceleration. Distance traveled in nth second is:", "a(2n-1)/2", "an", "a n^2/2", "None", "A", "Sn = a(2n-1)/2"),
        ("The range of projectile is maximum when θ equals:", "45°", "30°", "60°", "None", "A", "R max at 45°"),
        ("For a particle moving with constant acceleration, displacement in nth second is:", "u + a/2 (2n-1)", "u + an", "u + a n", "None", "A", "Sn = u + a(2n-1)/2"),
        ("If v = u + at, then acceleration is:", "Constant", "Variable", "Zero", "None", "A", "Constant acceleration"),
        ("Area under velocity-time graph gives:", "Displacement", "Acceleration", "Force", "None", "A", "Area under v-t gives displacement"),
        ("In uniform circular motion, velocity is:", "Constant", "Variable", "Zero", "None", "A", "Uniform speed but direction changes"),
        ("If a car covers 1/3 distance at v, 2/3 at 2v, average speed is:", "1.5v", "3v/2", "1.33v", "None", "A", "v_avg = 3v/2"),
        ("A particle's motion is described by v = √x. Its acceleration is:", "v dv/dx", "Constant", "Zero", "None", "A", "a = v dv/dx"),
        ("The trajectory of projectile is:", "Parabolic", "Circular", "Elliptical", "None", "A", "Parabolic path"),
        ("A body travels equal distances in first, second, third seconds. It moves with:", "Increasing velocity", "Decreasing velocity", "Constant velocity", "None", "A", "v increases if equal distances"),
        ("If s = t^3, acceleration at t = 2s:", "12 units", "6 units", "4 units", "None", "A", "a = d^2s/dt^2 = 6t = 12"),
        ("The condition for upward motion is:", "v = u - gt", "v = u + gt", "v = u", "None", "A", "v = u - gt for upward"),
        ("For free fall from height h, time is:", "√(2h/g)", "h/g", "2h/g", "None", "A", "t = √(2h/g)"),
        ("In a loop, minimum speed at top is:", "√(gR)", "√(g/R)", "gR", "None", "A", "v_min = √(gR) for loop"),
        ("The angle between velocity and acceleration is:", "Zero for uniform motion", "90° for circular", "Both", "None", "C", "Depends on path"),
        ("If an object returns to starting point, displacement is:", "Zero", "Positive", "Negative", "None", "A", "Displacement is zero"),
    ],
    "Laws of Motion": [
        ("Newton's first law defines:", "Inertia", "Force", "Momentum", "None", "A", "First law defines inertia"),
        ("Momentum is product of:", "Mass and velocity", "Mass and acceleration", "Force and time", "None", "A", "p = mv"),
        ("A body moves on frictionless surface. Inertia is:", "100%", "50%", "Any %", "None", "A", "Inertia proportional to mass"),
        ("The coefficient of friction is ratio of:", "f/N", "f/mg", "f/N", "None", "A", "μ = f/N"),
        ("A block on inclined plane starts sliding when angle is:", "tan^-1(μ)", "sin^-1(μ)", "cos^-1(μ)", "None", "A", "θ = tan^-1(μ)"),
        ("Impulse is equal to area under:", "Force-time graph", "Force-distance graph", "Mass-time graph", "None", "A", "Impulse = ∫F dt"),
        ("Rolling friction is:", "Less than sliding", "Greater than sliding", "Equal to sliding", "None", "A", "Rolling < sliding friction"),
        ("In rocket propulsion, momentum is conserved between:", "Rocket and ejected gases", "Rocket and Earth", "None", "A", "Rocket and gases"),
    ],
    "Thermodynamics": [
        ("First law of thermodynamics is:", "Conservation of energy", "Conservation of heat", "Conservation of work", "None", "A", "ΔQ = ΔU + ΔW"),
        ("For isothermal process, temperature is:", "Constant", "Variable", "Zero", "None", "A", "Isothermal: T = constant"),
        ("For adiabatic process:", "No heat exchange", "No work done", "Both", "None", "A", "q = 0 for adiabatic"),
        ("Molar specific heat of gas at constant pressure is:", "Cp", "Cv", "Cp - Cv", "None", "A", "Cp > Cv for all gases"),
        ("Adiabatic process follows:", "PV^γ = constant", "PV = constant", "P/V = constant", "None", "A", "PV^γ = K for adiabatic"),
        ("During condensation, heat is:", "Released", "Absorbed", "No change", "None", "A", "Condensation releases heat"),
        ("The efficiency of heat engine is:", "W/Qh", "Q/W", "Qh/W", "None", "A", "η = W/Qh"),
        ("Carnot engine has efficiency:", "1 - Tc/Th", "Tc/Th", "1 - Th/Tc", "None", "A", "η = 1 - Tc/Th"),
        ("Entropy increases in:", "Irreversible process", "Reversible process", "Constant", "None", "A", "ΔS > 0 for irreversible"),
        ("For isolated system, entropy:", "Increases", "Decreases", "Constant", "None", "A", "ΔS ≥ 0"),
    ],
    "Electromagnetism": [
        ("Coulomb's law deals with:", "Point charges", "Continuous charges", "Both", "None", "A", "F = kq1q2/r^2"),
        ("Electric field due to point charge is:", "Radial", "Circular", "Both", "None", "A", "E radiates outward/ inward"),
        ("Capacitance depends on:", "Geometry", "Dielectric", "Both", "None", "C", "C = εA/d"),
        ("Current is flow of:", "Electrons", "Protons", "Ions", "None", "A", "Electron flow"),
        ("Ohm's law is:", "V = IR", "P = IV", "R = V/I", "None", "A", "V = IR is Ohm's law"),
        ("Resistance of conductor depends on:", "Length, Area, ρ", "Temperature only", "Area only", "None", "A", "R = ρl/A"),
        ("Magnetic field inside solenoid is:", "μ0nI", "μ0I/n", "nI/μ0", "None", "A", "B = μ0nI"),
        ("Force on moving charge in magnetic field is:", "qvB sinθ", "qE", "qvB", "None", "A", "F = qvB sinθ"),
        ("Faraday's law deals with:", "EMF = -dΦ/dt", "V = IR", "F = qvB", "None", "A", "ε = -dΦ/dt"),
        ("Lenz's law is statement of:", "Conservation of energy", "Conservation of momentum", "Both", "None", "A", "Energy conservation"),
    ],
    "Optics": [
        ("Laws of reflection state that angle of incidence equals:", "Angle of reflection", "Complement", "Twice", "None", "A", "∠i = ∠r"),
        ("Refractive index of medium is ratio of:", "sin i / sin r", "sin r / sin i", "i/r", "None", "A", "n = sin i / sin r"),
        ("Critical angle occurs when:", "r = 90°", "i = 90°", "n = 1", "None", "A", "r = 90° at critical angle"),
        ("Total internal reflection requires:", "i > critical angle", "i < critical angle", "r > 90°", "None", "A", "i > ic for TIR"),
        ("Lens maker formula is:", "1/f = (n-1)(1/R1 - 1/R2)", "f = (n-1)(R1-R2)", "n = f/R", "None", "A", "Lens maker formula"),
        ("Optical fiber works on:", "Total internal reflection", "Refraction", "Reflection", "None", "A", "TIR in optical fiber"),
        ("For convex lens, focal length is:", "Positive", "Negative", "Zero", "None", "A", "Convex lens has + focal length"),
        ("Young's double slit experiment shows:", "Interference", "Diffraction", "Polarization", "None", "A", "Interference pattern"),
        ("Diffraction is evidence of:", "Wave nature", "Particle nature", "Both", "None", "A", "Diffraction shows wave nature"),
    ],
    "Modern Physics": [
        ("Photon concept was given by:", "Einstein", "Planck", "Bohr", "None", "A", "Einstein explained photoelectric effect"),
        ("Einstein's photoelectric equation is:", "KE = hν - φ", "E = mc^2", "E = hν", "None", "A", "Kmax = hν - φ0"),
        ("Bohr's model gives:", "Circular orbits", "Elliptical orbits", "Both", "None", "A", "Bohr proposed circular orbits"),
        ("Energy of nth orbit in H-atom is:", "-13.6/n^2 eV", "-13.6n^2 eV", "13.6/n^2 eV", "None", "A", "En = -13.6/n^2 eV"),
        ("Ionization potential of H-atom is:", "13.6 eV", "10.2 eV", "3.4 eV", "None", "A", "13.6 eV to remove electron"),
        ("Radioactivity is:", "Spontaneous process", "Induced process", "Both", "None", "A", "Spontaneous nuclear decay"),
        ("Alpha particle is:", "He2+ nucleus", "Electron", "Photon", "None", "A", "Alpha = He nucleus"),
        ("Beta decay involves emission of:", "Electron", "Proton", "Neutron", "None", "A", "Beta is electron emission"),
        ("Gamma rays are:", "High energy photons", "Electrons", "Protons", "None", "A", "Gamma are EM waves"),
        ("Half-life is independent of:", "Initial amount", "Temperature", "Pressure", "None", "A", "Half-life constant"),
        ("In nuclear fission, energy is released from:", "Mass defect", "Binding energy", "Both", "None", "C", "E = Δmc^2 from mass defect"),
        ("De Broglie wavelength is:", "h/mv", "mv/h", "h/m", "None", "A", "λ = h/p"),
        ("Uncertainty principle is:", "Δx Δp ≥ h/4π", "E = mc^2", "λ = h/p", "None", "A", "Heisenberg principle"),
    ],
}

total_added = 0
for chapter_name, pyqs in all_pyqs.items():
    try:
        c = Chapter.objects.get(subject=s, name=chapter_name)
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
        total_added += len(pyqs)
    except Chapter.DoesNotExist:
        print(f"Chapter {chapter_name} not found")

print(f"\nTotal added to NEET Physics: {total_added} PYQs")