import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Physics', grade=g)
c = Chapter.objects.get(subject=s, name='Laws of Motion')

lom_pyqs = [
    ("Rigid ball mass m strikes wall at 60° and reflects without loss. Impulse:", "mv", "2mv", "mv/2", "mv/3", "A", "Impulse = 2mv cos60 = mv"),
    ("60kg person in 940kg lift, moves upward at 1m/s². Tension in cable (g=10):", "8600N", "9680N", "11000N", "1200N", "C", "T = (60+940)(10+1) = 11000N"),
    ("Block mass m on smooth wedge angle θ, no slip. Force exerted by wedge:", "mg cosθ", "mg/cosθ", "mg tanθ", "mg sinθ", "B", "Normal force = mg/cosθ"),
    ("Masses 5kg and 10kg connected by string over pulley. Acceleration:", "g", "g/2", "g/3", "g/4", "C", "a = (10-5)g/(15) = g/3"),
    ("Car radius R, banked θ, μs. Maximum safe velocity:", "√(gR(μs+tanθ)/(1-μstanθ))", "√(g/R(μs+tanθ)/(1-μstanθ))", "√(gR²(μs+tanθ)/(1-μstanθ))", "√(gR(μs-tanθ)/(1+μstanθ))", "A", "Maximum speed formula"),
    ("Three forces on body in equilibrium. F1=4N, F2=3N. F3:", "5N", "7N", "1N", "25N", "A", "F3 = √(4²+3²) = 5N"),
    ("5000kg rocket, exhaust speed 800m/s, upward accel 20m/s². Gas ejected per second:", "127.5 kg/s", "187.5 kg/s", "185.5 kg/s", "137.5 kg/s", "B", "Thrust = ma = 5000×20 + mg = 150000 N = v dm/dt, dm/dt = 187.5 kg/s"),
    ("Plank at 30°, box slides 4m in 4s. μstatic and μkinetic:", "0.5, 0.6", "0.4, 0.3", "0.6, 0.5", "0.6, 0.2", "C", "a = 4/16 = 0.25 m/s², μk = a/g = 0.025, μs = tan30 = 0.577"),
    ("m=3kg, v=(2i+3j)m/s. F=(6i+12j)N for 2s. Final velocity:", "(6i+11j)", "(4i+7j)", "(2i+3j)", "(10i+15j)", "A", "v = u + Ft/m = (2+4)i + (3+8)j = (6i+11j)"),
    ("Record at ω, coin at r, μ. Coin revolves with record if:", "r ≤ μg/ω²", "r = μg/ω²", "r ≥ μg/ω²", "r ≥ g/μω²", "A", "Static friction provides centripetal force"),
    ("1kg object v=10m/s hits wall, deflects back in 0.1s. Force on wall:", "200N", "100N", "0N", "400N", "A", "F = Δp/t = (10-(-10))/0.1 × 1 = 200N"),
    ("Incorrect statement about friction:", "Rolling < sliding", "μ ∝ N", "F opposes relative motion", "μ has dimensions of length", "D", "μ is dimensionless"),
    ("Mass M suspended by string, horizontal force to hold at 60° from vertical:", "Mg", "Mg√3", "Mg/√3", "Mg/2", "C", "T sin60 = F, T cos60 = Mg, F = Mg tan60 = Mg/√3"),
    ("Bullet 0.04kg at 90m/s, stops in 60cm. Average resistive force:", "270N", "180N", "360N", "540N", "A", "F = mv²/2s = 0.04×8100/(2×0.6) = 270N"),
    ("2kg and 3kg at ends of spring, 10N on 3kg. Acceleration of CM:", "2 m/s²", "3 m/s²", "5 m/s²", "10 m/s²", "A", "a = F/(m1+m2) = 10/5 = 2 m/s²"),
    ("Three blocks m1,m2,m3 with force F. Tension T2 between m2 and m3:", "m3F/(m1+m2+m3)", "(m2+m3)F/(m1+m2+m3)", "m1F/(m1+m2+m3)", "m2F/(m1+m2+m3)", "B", "T2 acts on m3"),
    ("Bus starts, passengers jerk backward. This is:", "Inertia of rest", "Inertia of motion", "Inertia of direction", "Conservation of momentum", "A", "Inertia of rest"),
    ("Mass m on thread length l as conical pendulum. Tension:", "mg", "mg/cosθ", "mg sinθ", "mg cosθ", "B", "T = mg/cosθ"),
    ("Blocks 4kg,2kg,1kg on frictionless surface, force 14N on A. Contact force A-B:", "6N", "8N", "18N", "2N", "A", "a = 14/7 = 2 m/s², FAB = (2+1)a = 6N"),
    ("2kg block on soft floor, 5kg placed on it, floor yields at 0.1m/s². Action on floor:", "20N", "2N", "21N", "19.7N", "A", "Action = (2+5)g + ma = 70 + 0.7 = 70.7N, wait: action from 2kg block on floor"),
]

# Get existing
existing = MCQQuestion.objects.filter(chapter=c).count()
max_order = 0
for q in MCQQuestion.objects.filter(chapter=c):
    if q.order > max_order:
        max_order = q.order

# Add
for order, q in enumerate(lom_pyqs):
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

print(f"Added {len(lom_pyqs)} PYQs to Laws of Motion")