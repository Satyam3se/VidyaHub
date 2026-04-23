import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Physics', grade=g)
c = Chapter.objects.get(subject=s, name='Kinematics')

kin_pyqs = [
    ("Particle covers half distance at v1, rest at v2. Average speed:", "(v1+v2)/2", "√(v1v2)", "2v1v2/(v1+v2)", "v1v2/(v1+v2)", "C", "Harmonic mean: 2v1v2/(v1+v2)"),
    ("Displacement x = at^2 - bt^3. Acceleration zero at time:", "a/(3b)", "a/b", "2a/(3b)", "Zero", "A", "a = d²x/dt² = 2a-6bt, set =0 gives t=a/3b"),
    ("Horizontal range = max height. Angle of projection:", "θ = tan⁻¹(1)", "θ = tan⁻¹(4)", "θ = tan⁻¹(2)", "45°", "B", "R = u²sin2θ/g, H = u²sin²θ/2g, equate: tanθ = 4"),
    ("Ball thrown down at 20m/s, hits ground at 80m/s. Height of tower (g=10):", "340m", "320m", "300m", "360m", "C", "v² = u²+2gh, 80² = 20²+20h, h=300m"),
    ("Train 150m, 10m/s North. Parrot 5m/s South crosses train in:", "12s", "8s", "15s", "10s", "D", "Relative speed = 15m/s, t = 150/15 = 10s"),
    ("v-t graph shown. Displacement and distance in 6s:", "8m, 16m", "16m, 8m", "16m, 16m", "8m, 8m", "A", "From graph: displacement = area above = 8m, distance with reversals = 16m"),
    ("Stone falls freely. h1, h2, h3 in first, next, next 5s. Relation:", "h1 = 2h2 = 3h3", "h1 = h2/3 = h3/5", "h2 = 3h1, h3 = 3h2", "h1 = h2 = h3", "B", "h ∝ 1:3:5, so h1:h2:h3 = 25:75:125 = 1:3:5"),
    ("Initial velocity 3i+4j, acceleration 0.4i+0.3j. Speed after 10s:", "7 units", "7√2 units", "8.5 units", "10 units", "B", "v = u+at = (3+4)i + (4+3)j = 7i+7j, |v| = 7√2"),
    ("Projectiles at (45°-θ) and (45°+θ). Range ratio:", "2:1", "1:1", "2:3", "1:2", "B", "Ranges equal for complementary angles"),
    ("Position x = 9t² - t³. Position when maximum speed:", "54m", "81m", "24m", "32m", "A", "v = 18t-3t², dv/dt = 18-6t=0 at t=3, x=81-27=54m"),
    ("Cars: xP = at+bt², xQ = ft-t². Same velocity at time:", "(a-f)/(1+b)", "(f-a)/(2(1+b))", "(a+f)/(2(b-1))", "(a+f)/(2(1+b))", "D", "vP = a+2bt, vQ = f-2t, equate gives t=(a+f)/2(1+b)"),
    ("Thrown up, velocity at half max height 10m/s. Max height (g=10):", "8m", "20m", "10m", "12m", "C", "v² = u²-2gh, 0 = 100-20h, h=10m"),
    ("Projectile 5m/s on Earth, identical on planet with 3m/s. Planet g:", "3.5 m/s²", "5.9 m/s²", "16.3 m/s²", "3.6 m/s²", "D", "Same trajectory when R/H ratio same: g2 = (3/5)²×10 = 3.6 m/s²"),
    ("Velocity 30m/s East becomes 40m/s North in 10s. Average acceleration:", "1 m/s²", "7 m/s²", "5 m/s²", "10 m/s²", "C", "Δv = 50 m/s at 45°, a = 50/10 = 5 m/s²"),
    ("v-t graph: particle from rest with constant acceleration:", "Parabolic curve", "Line || t-axis", "Line inclined to t-axis", "Hyperbolic curve", "C", "Constant acceleration gives straight line inclined to t-axis"),
    ("v = At + Bt². Distance 1s to 2s:", "3A/2 + 7B/3", "A/2 + B/3", "3A/2 + 4B", "3A + 7B", "A", "s = ∫v dt from 1 to 2 = 3A/2 + 7B/3"),
    ("Projectile at A: 2i+3j m/s. At B:", "2i+3j", "-2i-3j", "-2i+3j", "2i-3j", "D", "Same horizontal velocity, vertical reverses"),
    ("Boat 8km/h across, resultant 10km/h. River velocity:", "12.8 km/h", "6 km/h", "8 km/h", "10 km/h", "B", "V² = 8² + Vr² = 100, Vr = 6 km/h"),
    ("Block slides from rest on smooth incline. Sn/Sn+1:", "(2n-1)/(2n)", "(2n-1)/(2n+1)", "(2n+1)/(2n-1)", "(2n)/(2n-1)", "B", "Sn = distance in nth sec = (1/2)a(n²-(n-1)²) = a(n-1/2), ratio = (2n-1)/(2n+1)"),
    ("Drop stone from 125m, throw another 10m/s horizontally. Time:", "12.5s", "5s", "10s", "2.5s", "B", "t = √(2h/g) = √(250/10) = 5s both same time"),
]

# Get existing
existing = MCQQuestion.objects.filter(chapter=c).count()
max_order = 0
for q in MCQQuestion.objects.filter(chapter=c):
    if q.order > max_order:
        max_order = q.order

# Add
for order, q in enumerate(kin_pyqs):
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

print(f"Added {len(kin_pyqs)} PYQs to Kinematics")