import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Grade, Subject, Chapter, MCQQuestion

g = Grade.objects.get(name='NEET')
s = Subject.objects.get(name='Physics', grade=g)
c = Chapter.objects.get(subject=s, name='Electromagnetism')

em_pyqs = [
    ("Spherical conductor radius 10cm has charge 3.2×10^-7C distributed uniformly. Electric field at 15cm from centre:", "1.28×10^5 N/C", "1.28×10^4 N/C", "1.28×10^6 N/C", "1.28×10^7 N/C", "A", "E = kq/r² = 9×10^9 × 3.2×10^-7 / (0.15)² = 1.28×10^5 N/C"),
    ("Capacitance with air is 6μF. With dielectric, becomes 30μF. Permittivity of medium:", "0.44×10^-10", "1.77×10^-12", "5.00", "0.44×10^-13", "A", "ε = εr × ε0 = 5 × 0.88×10^-11 = 0.44×10^-10"),
    ("Solids with negative temperature coefficient of resistance are:", "Metals", "Insulators only", "Semiconductors only", "Insulators and Semiconductors", "D", "Insulators and semiconductors have negative TCR"),
    ("Electron projected along axis of current-carrying solenoid. Which is true?", "Electron will be accelerated", "Path will be circular", "Electron will continue with uniform velocity", "Path will be helical", "C", "Uniform velocity along uniform B field"),
    ("800 turn coil area 0.05m² kept perpendicular to B = 5×10^-5T. Rotated 90° in 0.1s. Induced emf:", "0.02 V", "2 V", "0.2 V", "2×10^-3 V", "A", "ε = NBAω sinθ = 800×5×10^-5×0.05×(π/2)/0.1 ≈ 0.02V"),
    ("LCR circuit: L removed → phase diff = π/3. C removed → phase diff = π/3. Power factor:", "Zero", "0.5", "1.0", "-1.0", "C", "Both give same phase, so circuit at resonance with PF=1"),
    ("Charges +Q and -Q at distance, force F. 25% charge transferred from A to B. New force:", "F", "9F/16", "16F/9", "4F/3", "B", "q1'=3Q/4, q2'=Q/4, F' = F × (3/4 × 1/4) = 9F/16"),
    ("Potentiometer wire length 4m, resistance 8Ω. Resistance to get 1mV/cm with 2V accumulator:", "40Ω", "44Ω", "48Ω", "32Ω", "D", "V/x = 0.001V/cm = 0.1V/m, need R = (2/0.1) - 8 = 12, wait: 32Ω"),
    ("Long solenoid 50cm, 100 turns, current 2.5A. Magnetic field at centre:", "6.28×10^-4 T", "3.14×10^-4 T", "6.28×10^-5 T", "3.14×10^-5 T", "A", "B = μ0nI = 4π×10^-7 × (100/0.5) × 2.5 = 6.28×10^-4 T"),
    ("Cycle wheel radius 0.5m rotated at 10 rad/s in B=0.1T perpendicular. EMF between centre and rim:", "0.25 V", "0.125 V", "0.5 V", "Zero", "B", "ε = Bωr²/2 = 0.1×10×(0.5)²/2 = 0.125V"),
    ("RMS value of potential difference shown in figure:", "V0/√2", "V0/2", "V0", "V0/√3", "B", "RMS = V0/2 for half-wave rectified"),
    ("Which has minimum wavelength?", "X-rays", "UV rays", "γ-rays", "Cosmic rays", "D", "Cosmic rays have shortest λ"),
    ("Hollow metal sphere radius R uniformly charged. Electric field at distance r:", "Zero as r increases for r<R", "Zero for r<R, decreases for r>R", "Increases for r<R", "Decreases for r<R", "B", "No field inside conductor, drops outside"),
    ("Wire resistance R melted and stretched to n times length. New resistance:", "R/n", "n²R", "R/n²", "nR", "B", "R' = ρ × (nL) / (A/n) = n²R"),
    ("Magnetic susceptibility negative for:", "Diamagnetic materials", "Paramagnetic materials", "Ferromagnetic materials", "All", "A", "Diamagnetic materials have negative χ"),
    ("LCR series circuit resonance when:", "XL = XC", "XL = R", "XC = R", "XL + XC = R", "A", "Resonance at XL = XC"),
    ("Ratio of amplitude of B to E for EM wave in vacuum is:", "c", "1/c", "c²", "√c", "B", "E/B = c in vacuum, so B/E = 1/c"),
    ("Electric flux entering and leaving is φ1 and φ2. Charge inside:", "(φ2-φ1)ε0", "(φ1+φ2)ε0", "(φ2-φ1)/ε0", "(φ1+φ2)/ε0", "A", "Gauss: q = ε0φnet = ε0(φ2-φ1)"),
    ("Bar magnet moment M placed perpendicular to B. Force on each pole of length l:", "M = Fl", "M = F/l", "F = MB/l", "F = MBl", "C", "M = BIl × l, so F = M/l"),
    ("Magnetic flux φ = 3t² + 4t + 9. Induced emf at t=2s:", "16 V", "9 V", "1 V", "4 V", "A", "ε = dφ/dt = 6t+4, at t=2: 6×2+4=16V"),
]

# Get existing
existing = MCQQuestion.objects.filter(chapter=c).count()
max_order = 0
for q in MCQQuestion.objects.filter(chapter=c):
    if q.order > max_order:
        max_order = q.order

# Add
for order, q in enumerate(em_pyqs):
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

print(f"Added {len(em_pyqs)} PYQs to Electromagnetism")