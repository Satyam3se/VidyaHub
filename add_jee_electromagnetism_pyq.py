import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Chapter, MCQQuestion

chapter = Chapter.objects.get(name='Electromagnetism', subject__name='Physics', subject__grade__name='JEE')
print('Chapter:', chapter.name)

mcqs_data = [
    ('01', 'Electrostatics', r'Two point charges Q and -3Q are placed some distance apart. If the electric field at the location of Q is E, then at the location of -3Q, it is:', r'A) E/3', r'B) -E/3', r'C) 3E', r'D) -3E', 'B', 'Electric field follows inverse square law. E at -3Q due to Q = kQ/(r)^2. At Q due to -3Q = k(-3Q)/(r)^2 = -3E. So it is -E/3.'),
    ('02', 'Gauss Law', r'A charge q is placed at the center of the open end of a cylindrical vessel. The flux of the electric field through the surface of the vessel is:', r'A) q/epsilon_0', r'B) q/2epsilon_0', r'C) 2q/epsilon_0', r'D) Zero', 'B', 'Charge at open end of cylinder: only half the Gaussian surface is covered. Flux = q/2epsilon_0.'),
    ('03', 'Capacitance', r'A parallel plate capacitor is charged and then disconnected from the source. A dielectric slab is then inserted between the plates. The quantity that remains constant is:', r'A) Potential', r'B) Capacity', r'C) Charge', r'D) Energy', 'C', 'When disconnected from battery, charge remains constant.'),
    ('04', 'Current Elec.', r'The resistance of a wire is 5 ohm at 50C and 6 ohm at 100C. The resistance of the wire at 0C is:', r'A) 3 ohm', r'B) 4 ohm', r'C) 1 ohm', r'D) 2 ohm', 'B', 'R_t = R_0(1 + alpha*t). Using both equations: 5 = R_0(1 + 50alpha), 6 = R_0(1 + 100alpha). Solving: alpha = 1/2500, R_0 = 4 ohm.'),
    ('05', 'Magnetism', r'A long straight wire carries a current of 35 A. The magnitude of the magnetic field B at a point 20 cm from the wire is:', r'A) 3.5 x 10^-5 T', r'B) 7 x 10^-5 T', r'C) 3.5 x 10^-4 T', r'D) 1.75 x 10^-4 T', 'A', 'B = (mu_0 I)/(2 pi r) = (4pi x 10^-7 x 35)/(2pi x 0.2) = 3.5 x 10^-5 T.'),
    ('06', 'EMI', r'A circular coil of radius 10 cm and 500 turns is rotated in a magnetic field of 0.5 T at 600 rpm. The peak EMF induced is:', r'A) 25pi V', r'B) 50pi V', r'C) 5pi V', r'D) 10pi V', 'A', 'omega = 600 rpm = 10 pi rad/s. E_0 = NBA omega = 500 x 0.5 x pi x 0.1^2 x 10pi = 25 pi V.'),
    ('07', 'AC', r'In an LCR series circuit, the resonance frequency is f. If the capacitance is made 4 times, the new resonance frequency will be:', r'A) f/2', r'B) 2f', r'C) f/4', r'D) 4f', 'A', 'f = 1/(2pi sqrt(LC)). If C becomes 4C, new f = f/sqrt(4) = f/2.'),
    ('08', 'Electrostatics', r'The work done in moving a charge of 2 C across two points having a potential difference of 12 V is:', r'A) 6 J', r'B) 12 J', r'C) 24 J', r'D) 48 J', 'C', 'W = qV = 2 x 12 = 24 J.'),
    ('09', 'Magnetism', r'The magnetic susceptibility of a paramagnetic material at -73C is 0.0075. Its value at -173C will be:', r'A) 0.00375', r'B) 0.0150', r'C) 0.0300', r'D) 0.0075', 'B', 'For paramagnetic, chi inversely proportional to T. T1 = 200K, T2 = 100K. chi2/chi1 = T1/T2 = 200/100 = 2. So chi2 = 0.0150.'),
    ('10', 'Current Elec.', r'Five equal resistances each of R ohm are connected as a Wheatstone bridge. The equivalent resistance between the battery terminals is:', r'A) R/2', r'B) R', r'C) 2R', r'D) 5R', 'B', 'Balanced Wheatstone bridge: equivalent resistance = R.'),
    ('11', 'EM Waves', r'The ratio of contributions made by the electric field and magnetic field components to the intensity of an EM wave is:', r'A) c : 1', r'B) 1 : 1', r'C) c^2 : 1', r'D) sqrt(c) : 1', 'B', 'In EM wave, energy is equally shared between electric and magnetic fields.'),
    ('12', 'Capacitance', r'Two capacitors of 2 muF and 3 muF are connected in series. The total capacitance is:', r'A) 5 muF', r'B) 1.2 muF', r'C) 6 muF', r'D) 0.8 muF', 'B', '1/C = 1/2 + 1/3 = 5/6, so C = 6/5 = 1.2 muF.'),
    ('13', 'Magnetism', r'A proton and an alpha particle enter a uniform magnetic field with the same velocity. The ratio of the radii of their paths r_p/r_alpha is:', r'A) 1 : 1', r'B) 1 : 2', r'C) 2 : 1', r'D) 1 : 4', 'C', 'r = mv/(qB). For same v, r proportional to m/q. p: m, q=e; alpha: 4m, q=2e. Ratio = (m/e)/(4m/2e) = 2/1.'),
    ('14', 'EMI', r'The self-inductance of a solenoid of length L, area A and total turns N is:', r'A) mu_0 N^2 A / L', r'B) mu_0 N A / L', r'C) mu_0 N^2 A L', r'D) mu_0 N A L', 'A', 'L = mu_0 N^2 A / L.'),
    ('15', 'AC', r'The power factor of a purely inductive circuit is:', r'A) 1', r'B) 0', r'C) 0.5', r'D) Infinite', 'B', 'Power factor = cos phi. For purely inductive, phi = 90 degree, so cos phi = 0.'),
    ('16', 'Electrostatics', r'An electric dipole is placed in a non-uniform electric field. It experiences:', r'A) Only force', r'B) Only torque', r'C) Both force and torque', r'D) Neither', 'C', 'In non-uniform field, dipole experiences both force (due to field gradient) and torque.'),
    ('17', 'Current Elec.', r'A wire of resistance R is stretched to double its length. The new resistance is:', r'A) 2R', r'B) 4R', r'C) R/2', r'D) R/4', 'B', 'R = rho*L/A. When length doubles, volume constant, so area halves. New R = rho*(2L)/(A/2) = 4R.'),
    ('18', 'Magnetism', r'At a certain place, the horizontal component of earth magnetic field is sqrt(3) times the vertical component. The angle of dip at this place is:', r'A) 30 degree', r'B) 60 degree', r'C) 45 degree', r'D) 0 degree', 'A', 'tan delta = B_v/B_h = 1/sqrt(3), so delta = 30 degree.'),
    ('19', 'EMI', r'If the number of turns in a coil is doubled without changing its length and area, the self-inductance becomes:', r'A) Double', r'B) Four times', r'C) Half', r'D) Unchanged', 'B', 'L proportional to N^2. Doubling N gives L becomes 4 times.'),
    ('20', 'AC', r'The peak value of an AC voltage is 440 V. Its RMS value is:', r'A) 311 V', r'B) 220 V', r'C) 440 V', r'D) 622 V', 'A', 'V_rms = V_peak/sqrt(2) = 440/1.414 = 311 V.'),
    ('21', 'Electrostatics', r'The capacitance of a spherical conductor of radius 1 m is:', r'A) 1.1 x 10^-10 F', r'B) 9 x 10^9 F', r'C) 10^-6 F', r'D) 1 F', 'A', 'C = 4 pi epsilon_0 R = (1/9 x 10^9) x 1 = 1.11 x 10^-10 F.'),
    ('22', 'Current Elec.', r'In a potentiometer experiment, the balancing length is 250 cm for a cell. When the cell is shunted by 10 ohm, the balancing length becomes 200 cm. The internal resistance of the cell is:', r'A) 2 ohm', r'B) 2.5 ohm', r'C) 5 ohm', r'D) 1.25 ohm', 'B', 'V = kl*250, V_shunted = kl*200. Also V_shunted = E*R/(R+r). Solving: r = 2.5 ohm.'),
    ('23', 'Magnetism', r'A galvanometer of resistance 100 ohm gives full scale deflection for 10 mA current. To use it as an ammeter of range 10 A, the shunt resistance required is:', r'A) 0.1 ohm', r'B) 0.01 ohm', r'C) 1 ohm', r'D) 10 ohm', 'A', 'I_g*R_g = I_s*R_s. 0.01*100 = 10*R_s, R_s = 0.1 ohm.'),
    ('24', 'EMI', r'Two coils of self-inductances 2 mH and 8 mH are placed close to each other. The maximum mutual inductance between them is:', r'A) 10 mH', r'B) 6 mH', r'C) 4 mH', r'D) 16 mH', 'C', 'M_max = sqrt(L1*L2) = sqrt(2*8) = 4 mH.'),
    ('25', 'AC', r'In a series LCR circuit, if V_L = V_C = 100 V and V_R = 50 V, the total applied voltage is:', r'A) 250 V', r'B) 200 V', r'C) 50 V', r'D) 100 V', 'C', 'V = sqrt(V_R^2 + (V_L - V_C)^2) = sqrt(50^2 + 0) = 50 V.'),
    ('26', 'EM Waves', r'The electric field of an EM wave is E = 30 sin(10^8 t - kx) V/m. The peak magnetic field B_0 is:', r'A) 10^-7 T', r'B) 3 x 10^-7 T', r'C) 10^-8 T', r'D) 3 x 10^-8 T', 'A', 'E_0/B_0 = c, so B_0 = 30/(3 x 10^8) = 10^-7 T.'),
    ('27', 'Electrostatics', r'If an electron is accelerated through a potential difference of 1 V, its kinetic energy is:', r'A) 1 J', r'B) 1.6 x 10^-19 J', r'C) 1 eV', r'D) Both B and C', 'D', '1 eV = 1.6 x 10^-19 J. KE = 1 eV = 1.6 x 10^-19 J.'),
    ('28', 'Current Elec.', r'Kirchhoffs second law (Loop rule) is based on the conservation of:', r'A) Charge', r'B) Momentum', r'C) Mass', r'D) Energy', 'D', 'Loop rule is based on conservation of energy (potential drop around loop = 0).'),
    ('29', 'Magnetism', r'The force per unit length between two parallel wires carrying currents I_1 and I_2 separated by distance d is:', r'A) mu_0 I_1 I_2 / (2 pi d)', r'B) mu_0 I_1 I_2 / d', r'C) mu_0 I_1 I_2 / (4 pi d^2)', r'D) mu_0 I_1^2 / d', 'A', 'F/L = (mu_0 I_1 I_2)/(2 pi d).'),
    ('30', 'AC', r'The quality factor Q of a series LCR circuit at resonance is:', r'A) (1/R) sqrt(L/C)', r'B) R sqrt(L/C)', r'C) (1/R) sqrt(C/L)', r'D) omega L R', 'A', 'Q = (omega_0 L)/R = (1/R) sqrt(L/C).'),
]

order = MCQQuestion.objects.filter(chapter=chapter).count() + 1
for q_no, topic, q, a, b, c, d, correct, exp in mcqs_data:
    MCQQuestion.objects.create(
        chapter=chapter,
        question_text=f'Q{q_no} ({topic}): {q}',
        option_a=a,
        option_b=b,
        option_c=c,
        option_d=d,
        correct_option=correct,
        explanation=exp,
        order=order
    )
    order += 1

print(f'Added {len(mcqs_data)} MCQs to Electromagnetism chapter')