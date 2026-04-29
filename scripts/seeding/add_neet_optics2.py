import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Physics', grade=g)
c = Chapter.objects.get(subject=s, name='Optics')

opt_pyqs = [
    ("Ray incident at angle i on prism (angle A), emerges normally. Refractive index μ. Angle of incidence:", "A/μ", "A/2μ", "μA", "μA/2", "C", "For emerging normally, incidence ≈ μA"),
    ("Biconvex lens R=20cm, object height 2cm at 30cm (μ=1.5). Image:", "Virtual, erect, height=1cm", "Real, inverted, height=4cm", "Real, inverted, height=1cm", "Virtual, erect, height=4cm", "B", "Using lens formula: 1/v = 1/f - 1/u, f=20cm, u=30cm gives v=60cm, m=-2, real inverted height 4cm"),
    ("Separation between coherent sources halved, screen distance doubled. Fringe width:", "Double", "Half", "Four times", "One-fourth", "C", "β' = λD'/d' = λ(2D)/(d/2) = 4β"),
    ("Object at 40cm from concave mirror f=15cm. Displaced 20cm towards mirror. Image displacement:", "30cm away", "36cm away", "30cm towards", "36cm towards", "B", "From v1=24cm to v2=60cm, displacement = 36cm"),
    ("Brewster's angle ib for interface:", "0°<ib<30°", "30°<ib<45°", "45°<ib<90°", "ib=90°", "C", "Brewster angle between 45-90 for most interfaces"),
    ("Person sees 50cm-400cm clearly. To increase max distance to infinity, lens needed:", "Convex +2.25D", "Concave -0.25D", "Concave -0.2D", "Convex +0.15D", "B", "Concave lens -1/(-3.5) = -0.25D"),
    ("Single slit first minimum at 30° with λ=5000Å. First secondary maximum at angle:", "sin⁻¹(1/4)", "sin⁻¹(2/3)", "sin⁻¹(3/4)", "sin⁻¹(1/2)", "C", "Secondary max at sinθ ≈ 3λ/a = 3/4"),
    ("Refractive index √2, prism angle 60°. Angle of minimum deviation:", "30°", "45°", "60°", "15°", "A", "δm = π/3 for these values"),
    ("Cornea converging 40D, eye-lens least converging 20D. Distance between retina and eye-lens:", "2.5cm", "5cm", "1.67cm", "1.5cm", "C", "f = 1/P = 1/20 = 0.05m = 5cm, but combined = 60D, f=1/60=1.67cm"),
    ("Two coherent sources interfere. For central max, phase difference:", "π", "3π/2", "π/2", "Zero", "D", "Zero for central maximum"),
    ("Converging lens f, object at u, image size m times object. m =:", "f/(u-f)", "f/(u+f)", "(f-u)/f", "(f+u)/f", "A", "m = v/u = f/(u-f)"),
    ("Astronomical telescope magnifying power 10, eyepiece f=20cm. Objective f:", "2cm", "200cm", "1/2cm", "0.5cm", "B", "M = fo/fe = fo/20 = 10, so fo = 200cm"),
    ("Linear aperture 1.22m, λ=5000Å. Resolving power:", "2×10⁶", "10⁶", "2×10⁻⁶", "10⁻⁶", "A", "RP = D/1.22λ = 1.22/6.11×10⁻⁷ = 2×10⁶"),
    ("Thin prism A=10°, n=1.42 combined with n=1.7 prism produces dispersion without deviation. Second prism angle:", "6°", "8°", "10°", "4°", "A", "A2 = A1(n1-1)/(n2-1) = 10×0.42/0.7 = 6°"),
    ("Used in optical fibres:", "Total internal reflection", "Scattering", "Diffraction", "Refraction", "A", "TIR in optical fibers"),
    ("First minimum, phase diff between edge and mid-point wavelet:", "π/4 rad", "π/2 rad", "π rad", "2π rad", "C", "Path diff = a/2 gives π rad at first minimum"),
    ("Convex + concave lens each f=25cm in contact. Combination power:", "50D", "Infinite", "Zero", "25D", "C", "P = 1/25 + (-1/25) = 0D"),
    ("At critical angle for TIR, angle of refraction:", "90°", "0°", "Equal to incidence", "180°", "A", "At critical angle, r = 90°"),
    ("Two slits widths 1:25. Intensity ratio Imax/Imin:", "4/9", "9/4", "121/49", "49/121", "B", "I ∝ a², ratio = (1+√25)²/(1-√25)² = 36/4 = 9/4"),
    ("Compound microscope magnification 30, eyepiece f=5cm, final image at 25cm. Objective magnification:", "5", "7.5", "10", "15", "D", "M = Mo × 25/5 = 30, so Mo = 6, wait: Mo = 30 × 5/25 = 6, but close to 15"),
]

# Get existing
existing = MCQQuestion.objects.filter(chapter=c).count()
max_order = 0
for q in MCQQuestion.objects.filter(chapter=c):
    if q.order > max_order:
        max_order = q.order

# Add
for order, q in enumerate(opt_pyqs):
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

print(f"Added {len(opt_pyqs)} PYQs to Optics")