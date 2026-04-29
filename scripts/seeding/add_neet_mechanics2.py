import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Physics', grade=g)
c = Chapter.objects.get(subject=s, name='Mechanics')

mechanics_pyqs = [
    ("A person sitting in ground floor sees ball dropped from roof cross window (height 1.5m) in 0.1s. Velocity at top of window (g=10):", "14.5 m/s", "15 m/s", "13.5 m/s", "None", "A", "v = u + at, calculate from kinematics"),
    ("Two projectiles with same velocity at 60° and 30°, which remains same?", "Range", "Time of flight", "Maximum height", "None", "A", "Same initial speed gives equal range at complementary angles"),
    ("Rigid ball strikes rigid wall at 60° and reflects without loss. Impulse imparted by wall:", "mv", "2mv", "mv/2", "None", "A", "Impulse = 2mv cos60 = mv"),
    ("Block of mass 10kg on rough surface (μ=0.5), horizontal force 100N. Acceleration:", "5 m/s²", "10 m/s²", "2.5 m/s²", "None", "A", "F_net = 100 - 50 = 50N, a = 5"),
    ("1kg body thrown up at 20m/s rises 18m. Energy lost due to air friction (g=10):", "20 J", "40 J", "10 J", "None", "A", "KE = 200J, PE = 180J, lost = 20J"),
    ("Car on curved road radius R, banked at θ, μs. Maximum safe velocity:", "√(gR(μs+tanθ)/(1-μstanθ))", "√(gR)", "√(gRtanθ)", "None", "A", "Max speed formula for banked curve with friction"),
    ("Two bodies 1kg at i+2j+k and 3kg at -3i-2j+k. COM position:", "-2i - j + k", "2i + j - k", "i + k", "None", "A", "r_cm = (m1r1+m2r2)/(m1+m2)"),
    ("Ratio of radii of gyration of disc to ring (same mass, radius):", "1:√2", "√2:1", "1:1", "None", "A", "I_disc/I_ring = 1:2, k ratio = 1:√2"),
    ("Acceleration due to gravity at height R from earth surface:", "g/4", "g/2", "g", "None", "A", "g_h = g/(1+h/R)² at h=R gives g/4"),
    ("Young's modulus of wire length L, radius r is Y. If L→L/2, r→r/2, Young's modulus:", "Y", "2Y", "Y/2", "None", "A", "Y is material property, independent of dimensions"),
    ("Two liquids densities ρ and nρ (n>1), height h each. Cylinder (length L, density d) floats with axis vertical, pL (p<1) in denser liquid. d:", "ρ[1+(n-1)p]", "ρ[n+(n-1)p]", "ρ[1+n-p]", "None", "A", "Density from buoyancy"),
    ("Particle covers half distance at v1, rest at v2. Average speed:", "2v1v2/(v1+v2)", "(v1+v2)/2", "v1v2/(v1+v2)", "None", "A", "Harmonic mean formula"),
    ("Sphere rotating about symmetry axis in free space, radius increases keeping mass same. Constant quantity:", "Angular momentum", "Kinetic energy", "Angular velocity", "None", "A", "L conserved in absence of external torque"),
    ("Particle potential U = A/r² - B/r (A,B >0). For equilibrium distance:", "2A/B", "A/B", "B/A", "None", "A", "dU/dr = 0 at r = 2A/B"),
    ("Bullet 10g at 400m/s strikes 2kg wood block suspended by 5m string. Block rises 10cm. Bullet emerges with speed:", "120 m/s", "200 m/s", "80 m/s", "None", "A", "Momentum conservation"),
    ("Disk and sphere same radius, different masses roll down identical inclined planes from same height. Which reaches bottom first?", "Sphere", "Disk", "Both same", "None", "A", "Sphere has lower moment of inertia"),
    ("At what height from earth surface is potential -5.4x10^7 J/kg and g=6.0 m/s²?", "2600 km", "1600 km", "3600 km", "None", "A", "Calculate from gravitational formulas"),
    ("Wettability of surface by liquid depends on:", "Angle of contact", "Density", "Viscosity", "None", "A", "Contact angle determines wettability"),
    ("Record revolving at ω, coin at distance r, static μ. Coin revolves with record if:", "r ≤ μg/ω²", "r ≥ μg/ω²", "r = μg/ω²", "None", "A", "Condition for static friction to provide centripetal force"),
    ("Particle displacement x = ae^(-αt) + be^(βt). Velocity will:", "Go on increasing with time", "Decrease then increase", "Remain constant", "None", "A", "Derivative shows increasing velocity"),
]

# Get existing count
existing = MCQQuestion.objects.filter(chapter=c).count()
print(f"Existing Mechanics PYQs: {existing}")

# Get max order
max_order = 0
for q in MCQQuestion.objects.filter(chapter=c):
    if q.order > max_order:
        max_order = q.order

# Add new PYQs
for order, q in enumerate(mechanics_pyqs):
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

print(f"Added {len(mechanics_pyqs)} PYQs to Mechanics")