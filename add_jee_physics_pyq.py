import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Chapter, MCQQuestion

print("=" * 60)
print("Adding JEE Physics PYQs - Question Numbers from Data")
print("=" * 60)

# First, clear existing MCQs
chapters = Chapter.objects.filter(subject__name='Physics', subject__grade__name='JEE', name__in=['Mechanics', 'Thermodynamics', 'Electromagnetism'])
for ch in chapters:
    MCQQuestion.objects.filter(chapter=ch).delete()
    print(f"Cleared {ch.name}")

# ===== MECHANICS =====
chapter = Chapter.objects.get(name='Mechanics', subject__name='Physics', subject__grade__name='JEE')

mechanics_mcqs = [
    ('01', 'Rotation', 'A solid sphere is rolling on a frictionless surface, it enters a rough horizontal surface. Which of the following remains constant during the transition?', 'A) Linear Momentum', 'B) Angular Momentum about CM', 'C) Angular Momentum about contact point', 'D) Kinetic Energy', 'C', 'Angular momentum about contact point remains constant because there is no external torque about the contact point.'),
    ('02', 'WPE', 'A particle of mass m is moving in a circular path of constant radius r such that its centripetal acceleration a_c is varying with time t as a_c = k^2 r t^2. The power delivered to the particle by the forces is:', 'A) 2 pi mk^2 r^2 t', 'B) mk^2 r^2 t', 'C) (1/3) mk^4 r^2 t^5', 'D) Zero', 'B', 'Power = F.v = ma_c . v = m(k^2 r t^2) . (k r) = mk^2 r^2 t.'),
    ('03', 'COM', 'A man of mass M stands at one end of a plank of length L and mass M/3, which is floating in water. If the man walks to the other end of the plank, the distance that the man moves relative to the water is:', 'A) L/4', 'B) 3L/4', 'C) L/3', 'D) 2L/3', 'A', 'Using center of mass conservation: M.x = (M/3).(L-x), solving gives x = L/4.'),
    ('04', 'Gravity', 'A planet of mass M has two satellites S1 and S2 in circular orbits of radii r and 4r. The ratio of their tangential velocities is:', 'A) 1:2', 'B) 2:1', 'C) 1:4', 'D) 4:1', 'B', 'v = sqrt(GM/r), so v1/v2 = sqrt(4r/r) = 2:1.'),
    ('05', 'Rotation', 'A thin uniform rod of length L and mass M is swinging freely about a horizontal axis passing through its end. Its maximum angular speed is omega. Its center of mass rises to a maximum height of:', 'A) (1/6)(L^2 omega^2/g)', 'B) (1/2)(L^2 omega^2/g)', 'C) (1/3)(L^2 omega^2/g)', 'D) (L^2 omega^2/g)', 'A', 'Using energy conservation: (1/2)I omega^2 = mgh. For rod about end, I = ML^2/3, CM at L/2. Solving gives h = L^2 omega^2/6g.'),
    ('06', 'Fluids', 'A wooden block floats in water with 2/3 of its volume submerged. When the same block floats in oil, 5/6 of its volume is submerged. The density of oil is:', 'A) 0.6 g/cm^3', 'B) 0.8 g/cm^3', 'C) 0.9 g/cm^3', 'D) 1.2 g/cm^3', 'B', 'Using buoyancy: rho_block = (2/3) rho_water. Also rho_block = (5/6) rho_oil. So rho_oil = (2/3)/(5/6) = 0.8 g/cm^3.'),
    ('07', 'NLM', 'A block of mass m is pushed against a vertical wall by a horizontal force F. If the coefficient of friction is mu, the minimum value of F to prevent the block from falling is:', 'A) mu mg', 'B) mg/mu', 'C) mu/mg', 'D) mg', 'B', 'Friction upward = mu*F must balance weight mg, so F = mg/mu.'),
    ('08', 'Rotation', 'A ring, a disc, and a solid sphere (all same M and R) roll down the same inclined plane without slipping. The order of their arrival at the bottom is:', 'A) Ring, Disc, Sphere', 'B) Sphere, Disc, Ring', 'C) Disc, Ring, Sphere', 'D) All arrive together', 'B', 'Sphere has smallest moment of inertia, so largest acceleration. Ring has largest, so smallest acceleration.'),
    ('09', 'Collisions', 'A ball of mass m moving with velocity v strikes a stationary ball of mass 2m head-on. If e = 0.5, the velocity of the first ball after collision is:', 'A) v/2', 'B) Zero', 'C) -v/4', 'D) v/4', 'C', 'Using conservation of momentum and coefficient of restitution: v1 = (m - 2m*e)/(m + 2m) * v = -v/4.'),
    ('10', 'Kinematics', 'A projectile is fired with a velocity u making an angle theta with the horizontal. The radius of curvature of its path at the highest point is:', 'A) u^2 sin^2 theta/g', 'B) u^2 cos^2 theta/g', 'C) u^2/g', 'D) u^2 cos^2 theta/(g sin theta)', 'B', 'At highest point, velocity = u cos theta. Radius of curvature = v^2/a where a = g. So R = u^2 cos^2 theta/g.'),
    ('11', 'Elasticity', 'A wire of length L and cross-section A is stretched by a force F. If Youngs modulus is Y, the energy stored per unit volume is:', 'A) F^2/(2AY)', 'B) F^2/(2A^2 Y)', 'C) FY/(2AL)', 'D) F^2 L/(2AY)', 'A', 'Strain = FL/(AY), stress = F/A. Energy = (1/2)(stress)(strain) = F^2 L/(2AY). Per unit volume = F^2/(2AY).'),
    ('12', 'Rotation', 'The moment of inertia of a square plate of side a and mass M about an axis passing through its center and perpendicular to its plane is:', 'A) Ma^2/6', 'B) Ma^2/12', 'C) Ma^2/3', 'D) 2Ma^2/3', 'A', 'I = I_x + I_y. For square about center: I = Ma^2/12 + Ma^2/12 = Ma^2/6.'),
    ('13', 'WPE', 'A force F = -kx^3 acts on a particle. The work done by this force in moving the particle from x1 to x2 is:', 'A) (k/4)(x1^4 - x2^4)', 'B) (k/4)(x2^4 - x1^4)', 'C) k(x1^2 - x2^2)', 'D) Zero', 'A', 'W = integral F dx = integral -kx^3 dx from x1 to x2 = -k(x2^4 - x1^4)/4 = k(x1^4 - x2^4)/4.'),
    ('14', 'Gravity', 'If the radius of earth shrinks by 1% while mass remains same, the acceleration due to gravity on its surface will:', 'A) Increase by 1%', 'B) Increase by 2%', 'C) Decrease by 1%', 'D) Decrease by 2%', 'B', 'g = GM/R^2. If R becomes 0.99R, g increases by (1/0.99)^2 approximately 1.0201, so approximately 2% increase.'),
    ('15', 'Fluids', 'Terminal velocity v of a spherical ball of radius r falling through a viscous liquid is proportional to:', 'A) r', 'B) r^2', 'C) 1/r', 'D) 1/r^2', 'B', 'For Stokes law: mg = 6 pi eta r v, so v proportional to r^2 (since mg proportional to r^3).'),
    ('16', 'NLM', 'A spring of force constant k is cut into two equal halves. The force constant of each half is:', 'A) k/2', 'B) k', 'C) 2k', 'D) 4k', 'C', 'For same material, k proportional to 1/L. Halving length doubles k to 2k.'),
    ('17', 'COM', 'A shell of mass 200g is ejected from a gun of mass 4kg with a velocity of 80m/s. The recoil velocity of the gun is:', 'A) 4 m/s', 'B) 2 m/s', 'C) 1 m/s', 'D) 8 m/s', 'A', 'Momentum conserved: 4*v = 0.2*80, so v = 4 m/s.'),
    ('18', 'Rotation', 'A couple produces:', 'A) Linear motion', 'B) Rotational motion', 'C) Both A and B', 'D) No motion', 'B', 'A couple is two equal and opposite forces not in line. It produces pure rotation, no translation.'),
    ('19', 'Kinematics', 'If the displacement of a particle is given by s = t^3 - 6t^2 + 3t + 7, the velocity when acceleration is zero is:', 'A) 9 units', 'B) -9 units', 'C) 3 units', 'D) Zero', 'A', 'v = ds/dt = 3t^2 - 12t + 3. a = dv/dt = 6t - 12 = 0 when t = 2. v(2) = 12 - 24 + 3 = -9 units.'),
    ('20', 'WPE', 'A vertical spring is compressed by a distance x and a ball of mass m is placed on it. When released, the ball rises to a height h. The spring constant k is:', 'A) 2mgh/x^2', 'B) mgh/x', 'C) mgh/x^2', 'D) 2mgh/x', 'A', 'Energy conserved: (1/2)k x^2 = mgh, so k = 2mgh/x^2.'),
]

for q_no, topic, q, a, b, c, d, correct, exp in mechanics_mcqs:
    MCQQuestion.objects.create(
        chapter=chapter,
        question_text=f'({topic}) {q}',
        option_a=a,
        option_b=b,
        option_c=c,
        option_d=d,
        correct_option=correct,
        explanation=exp,
        order=int(q_no)
    )

print(f"Added {len(mechanics_mcqs)} MCQs to Mechanics")

# ===== THERMODYNAMICS =====
chapter = Chapter.objects.get(name='Thermodynamics', subject__name='Physics', subject__grade__name='JEE')

thermo_mcqs = [
    ('01', 'First Law', 'If delta U and delta W represent the increase in internal energy and work done by the system respectively in a thermodynamical process, which of the following is true?', 'A) delta U = -delta Q + delta W', 'B) delta U = delta Q - delta W', 'C) delta U = delta Q + delta W', 'D) delta U = delta W - delta Q', 'B', 'First law of thermodynamics: delta Q = delta U + delta W, so delta U = delta Q - delta W.'),
    ('02', 'Adiabatic', 'For an adiabatic process, the relation between V and T is TV^x = constant. The value of x is:', 'A) gamma', 'B) gamma - 1', 'C) 1 - gamma', 'D) 1/gamma', 'B', 'For adiabatic process: TV^(gamma-1) = constant, so x = gamma - 1.'),
    ('03', 'KTG', 'The temperature at which the RMS speed of hydrogen molecules is equal to the RMS speed of oxygen molecules at 47C is:', 'A) 20 K', 'B) 80 K', 'C) -73C', 'D) 320 K', 'A', 'v_rms = sqrt(3kT/M). For H2 and O2 at same v_rms: T_H2/T_O2 = M_H2/M_O2 = 2/32 = 1/16. So T_H2 = 320/16 = 20 K.'),
    ('04', 'Heat Engine', 'A Carnot engine working between 300 K and 600 K has work output of 800 J per cycle. The amount of heat energy supplied from the source is:', 'A) 800 J', 'B) 1600 J', 'C) 1200 J', 'D) 2400 J', 'B', 'Efficiency eta = 1 - T_c/T_h = 1 - 300/600 = 0.5. Also eta = W/Q_h, so Q_h = W/eta = 800/0.5 = 1600 J.'),
    ('05', 'Degrees of Freedom', 'The molar specific heat at constant volume of a mixture of n1 moles of monatomic gas and n2 moles of diatomic gas is:', 'A) (3n1 + 5n2)/(2(n1 + n2))R', 'B) (5n1 + 3n2)/(2(n1 + n2))R', 'C) (n1 + n2)/2 R', 'D) 3R', 'A', 'Cv = f/2 * R. Monatomic f=3, diatomic f=5. So Cv_mix = (3n1 + 5n2)/(n1+n2) * R/2.'),
    ('06', 'Isothermal', 'Work done in an isothermal expansion of an ideal gas from volume V1 to V2 is:', 'A) nRT ln(V2/V1)', 'B) nRT (V2/V1)', 'C) nRT ln(V1/V2)', 'D) P(V2-V1)', 'A', 'For isothermal process: W = nRT ln(V2/V1).'),
    ('07', 'Radiation', 'A spherical black body with a radius of 12 cm radiates 450 W power at 500 K. If the radius were halved and the temperature doubled, the power radiated in watt would be:', 'A) 450', 'B) 1000', 'C) 1800', 'D) 225', 'C', 'P = e*sigma*A*T^4. Area = 4piR^2. New radius = 6 cm, T = 1000 K. P_new = P*(r_new/r)^2*(T_new/T)^4 = 450*(1/2)^2*(2)^4 = 450*(1/4)*16 = 1800 W.'),
    ('08', 'Specific Heat', 'If gamma is the ratio of specific heats and R is the universal gas constant, then molar specific heat at constant volume Cv is:', 'A) R/(gamma-1)', 'B) gamma R/(gamma-1)', 'C) R(gamma-1)', 'D) gamma R', 'A', 'Cp/Cv = gamma, Cp - Cv = R. Solving: Cv = R/(gamma-1).'),
    ('09', 'Cyclic Process', 'In a cyclic process, the change in internal energy of a system is:', 'A) Positive', 'B) Negative', 'C) Zero', 'D) Dependent on path', 'C', 'Internal energy is a state function, so for a cyclic process delta U = 0.'),
    ('10', 'KTG', 'The average translational kinetic energy of a gas molecule at temperature T is:', 'A) (1/2)kT', 'B) (3/2)kT', 'C) kT', 'D) (5/2)kT', 'B', 'For ideal gas, average translational KE = 3/2 kT.'),
    ('11', 'Calorimetry', '10 g of ice at 0C is mixed with 10 g of water at 10C. The final temperature of the mixture is:', 'A) 10C', 'B) 5C', 'C) 0C', 'D) -5C', 'C', 'Heat lost by water to cool to 0C: 10*1*10 = 100 cal. Heat required to melt ice: 10*80 = 800 cal. Since 100 < 800, all ice melts and final temp is 0C.'),
    ('12', 'Heat Transfer', 'The thermal conductivity of a rod depends on:', 'A) Length', 'B) Area of cross-section', 'C) Temperature difference', 'D) Material of the rod', 'D', 'Thermal conductivity is a material property and does not depend on dimensions or temperature difference.'),
    ('13', 'Entropy', 'During an adiabatic expansion, the entropy of the system:', 'A) Increases', 'B) Decreases', 'C) Remains constant', 'D) Becomes zero', 'C', 'Adiabatic process is isentropic, entropy remains constant.'),
    ('14', 'Newton''s Cooling', 'A hot liquid cools from 80C to 70C in 2 minutes. The time taken for it to cool from 60C to 50C will be:', 'A) 2 min', 'B) Less than 2 min', 'C) More than 2 min', 'D) 4 min', 'C', 'Rate of cooling proportional to temperature difference. At higher temp difference, cools faster. So takes more time for same temperature drop at lower difference.'),
    ('15', 'Internal Energy', 'The internal energy of an ideal gas is a function of:', 'A) Pressure only', 'B) Volume only', 'C) Temperature only', 'D) Both P and V', 'C', 'For ideal gas, internal energy depends only on temperature.'),
    ('16', 'Work Done', 'Which of the following is a path-dependent function?', 'A) Internal Energy', 'B) Temperature', 'C) Work done', 'D) Pressure', 'C', 'Work done is a path function, not a state function.'),
    ('17', 'Mayer''s Formula', 'For one mole of an ideal gas, Cp - Cv is equal to:', 'A) R', 'B) R/J', 'C) 1.98 cal', 'D) All of these', 'D', 'Mayer''s formula: Cp - Cv = R = 8.314 J/mol-K = 1.98 cal/mol-K.'),
    ('18', 'KTG', 'If the pressure of an ideal gas is halved and its volume is doubled, its temperature will:', 'A) Remain constant', 'B) Become double', 'C) Become four times', 'D) Become half', 'A', 'PV = nRT. P becomes P/2, V becomes 2V. So new T = (P*2V)/(nR) = 2(PV)/(nR) = 2T? Wait: P1V1/T1 = P2V2/T2. (P/2 * 2V)/T2 = PV/T => P/T2 = PV/T => T2 = T. Temperature remains constant.'),
    ('19', 'Black Body', 'The wavelength of maximum emission lambda_m and absolute temperature T are related as:', 'A) lambda_m T = constant', 'B) lambda_m / T = constant', 'C) T / lambda_m = constant', 'D) lambda_m + T = constant', 'A', 'Wien''s displacement law: lambda_m * T = constant (b = 2.898 x 10^-3 m-K).'),
    ('20', 'Free Expansion', 'In the free expansion of a gas, which of the following is true?', 'A) W = 0', 'B) delta U = 0', 'C) Q = 0', 'D) All of the above', 'D', 'Free expansion is adiabatic and against zero pressure, so W=0, Q=0. For ideal gas, internal energy constant, so delta U = 0.'),
    ('21', 'Adiabatic', 'A diatomic gas is compressed to 1/32 times its initial volume adiabatically. If initial temperature is T, final temperature is:', 'A) 4T', 'B) 8T', 'C) 2T', 'D) 16T', 'A', 'TV^(gamma-1) = constant. For diatomic gamma = 7/5 = 1.4. V2 = V1/32. T2 = T1*(V1/V2)^(gamma-1) = T*(32)^(0.4) = T*4. So final temperature = 4T.'),
    ('22', 'Efficiency', 'If the temperature of the sink is decreased, the efficiency of a Carnot engine:', 'A) Increases', 'B) Decreases', 'C) Remains same', 'D) Becomes zero', 'A', 'Efficiency eta = 1 - Tc/Th. Decreasing Tc increases efficiency.'),
    ('23', 'Mean Free Path', 'The mean free path lambda of gas molecules varies with density rho as:', 'A) lambda proportional to rho', 'B) lambda proportional to 1/rho', 'C) lambda proportional to sqrt(rho)', 'D) lambda proportional to rho^2', 'B', 'Mean free path lambda = 1/(sqrt(2)*pi*d^2*n), where n is number density. So lambda inversely proportional to density.'),
    ('24', 'Radiation', 'Two stars emit maximum radiation at 3600 A and 4800 A. The ratio of their temperatures is:', 'A) 3:4', 'B) 4:3', 'C) 9:16', 'D) 16:9', 'B', 'Wien''s law: lambda1*T1 = lambda2*T2. So T1/T2 = lambda2/lambda1 = 4800/3600 = 4/3.'),
    ('25', 'Internal Energy', 'Change in internal energy of an ideal gas in an isothermal process is:', 'A) Positive', 'B) Negative', 'C) Zero', 'D) Infinite', 'C', 'For ideal gas, internal energy depends only on temperature. In isothermal process, temperature constant, so delta U = 0.'),
    ('26', 'Stefan''s Law', 'The energy radiated per second by a black body at T K is E. If temperature is doubled, energy becomes:', 'A) 2E', 'B) 4E', 'C) 8E', 'D) 16E', 'D', 'Stefan''s law: P = e*sigma*A*T^4. If T doubles, P becomes 2^4 = 16 times.'),
    ('27', 'Molar Heat', 'The ratio Cp/Cv for a monatomic gas is:', 'A) 1.67', 'B) 1.40', 'C) 1.33', 'D) 1.00', 'A', 'For monatomic gas: Cv = 3R/2, Cp = 5R/2, so Cp/Cv = 5/3 = 1.67.'),
    ('28', 'Latent Heat', 'Heat required to convert 1 g of ice at 0C to steam at 100C is:', 'A) 80 cal', 'B) 540 cal', 'C) 620 cal', 'D) 720 cal', 'D', 'Heat = heat to melt ice (80 cal) + heat to warm water (100 cal) + heat to vaporize (540 cal) = 720 cal.'),
    ('29', 'Isobaric', 'In an isobaric process, work done by the gas is P delta V. This work is also equal to:', 'A) nR delta T', 'B) Cp delta T', 'C) Cv delta T', 'D) delta U', 'A', 'For isobaric process: W = P delta V = nR delta T.'),
    ('30', 'Second Law', 'A heat engine rejects 600 J of heat to the sink for every 1000 J of heat absorbed from the source. Its efficiency is:', 'A) 60%', 'B) 40%', 'C) 100%', 'D) 20%', 'B', 'Efficiency = W/Q_h = (Q_h - Q_c)/Q_h = (1000 - 600)/1000 = 0.4 = 40%.'),
]

for q_no, topic, q, a, b, c, d, correct, exp in thermo_mcqs:
    MCQQuestion.objects.create(
        chapter=chapter,
        question_text=f'({topic}) {q}',
        option_a=a,
        option_b=b,
        option_c=c,
        option_d=d,
        correct_option=correct,
        explanation=exp,
        order=int(q_no)
    )

print(f"Added {len(thermo_mcqs)} MCQs to Thermodynamics")

# ===== ELECTROMAGNETISM =====
chapter = Chapter.objects.get(name='Electromagnetism', subject__name='Physics', subject__grade__name='JEE')

em_mcqs = [
    ('01', 'Electrostatics', 'Two point charges Q and -3Q are placed some distance apart. If the electric field at the location of Q is E, then at the location of -3Q, it is:', 'A) E/3', 'B) -E/3', 'C) 3E', 'D) -3E', 'B', 'Electric field follows inverse square law. E at -3Q due to Q = kQ/(r)^2. At Q due to -3Q = k(-3Q)/(r)^2 = -3E. So it is -E/3.'),
    ('02', 'Gauss Law', 'A charge q is placed at the center of the open end of a cylindrical vessel. The flux of the electric field through the surface of the vessel is:', 'A) q/epsilon_0', 'B) q/2epsilon_0', 'C) 2q/epsilon_0', 'D) Zero', 'B', 'Charge at open end of cylinder: only half the Gaussian surface is covered. Flux = q/2epsilon_0.'),
    ('03', 'Capacitance', 'A parallel plate capacitor is charged and then disconnected from the source. A dielectric slab is then inserted between the plates. The quantity that remains constant is:', 'A) Potential', 'B) Capacity', 'C) Charge', 'D) Energy', 'C', 'When disconnected from battery, charge remains constant.'),
    ('04', 'Current Elec.', 'The resistance of a wire is 5 ohm at 50C and 6 ohm at 100C. The resistance of the wire at 0C is:', 'A) 3 ohm', 'B) 4 ohm', 'C) 1 ohm', 'D) 2 ohm', 'B', 'R_t = R_0(1 + alpha*t). Using both equations: 5 = R_0(1 + 50alpha), 6 = R_0(1 + 100alpha). Solving: alpha = 1/2500, R_0 = 4 ohm.'),
    ('05', 'Magnetism', 'A long straight wire carries a current of 35 A. The magnitude of the magnetic field B at a point 20 cm from the wire is:', 'A) 3.5 x 10^-5 T', 'B) 7 x 10^-5 T', 'C) 3.5 x 10^-4 T', 'D) 1.75 x 10^-4 T', 'A', 'B = (mu_0 I)/(2 pi r) = (4pi x 10^-7 x 35)/(2pi x 0.2) = 3.5 x 10^-5 T.'),
    ('06', 'EMI', 'A circular coil of radius 10 cm and 500 turns is rotated in a magnetic field of 0.5 T at 600 rpm. The peak EMF induced is:', 'A) 25pi V', 'B) 50pi V', 'C) 5pi V', 'D) 10pi V', 'A', 'omega = 600 rpm = 10 pi rad/s. E_0 = NBA omega = 500 x 0.5 x pi x 0.1^2 x 10pi = 25 pi V.'),
    ('07', 'AC', 'In an LCR series circuit, the resonance frequency is f. If the capacitance is made 4 times, the new resonance frequency will be:', 'A) f/2', 'B) 2f', 'C) f/4', 'D) 4f', 'A', 'f = 1/(2pi sqrt(LC)). If C becomes 4C, new f = f/sqrt(4) = f/2.'),
    ('08', 'Electrostatics', 'The work done in moving a charge of 2 C across two points having a potential difference of 12 V is:', 'A) 6 J', 'B) 12 J', 'C) 24 J', 'D) 48 J', 'C', 'W = qV = 2 x 12 = 24 J.'),
    ('09', 'Magnetism', 'The magnetic susceptibility of a paramagnetic material at -73C is 0.0075. Its value at -173C will be:', 'A) 0.00375', 'B) 0.0150', 'C) 0.0300', 'D) 0.0075', 'B', 'For paramagnetic, chi inversely proportional to T. T1 = 200K, T2 = 100K. chi2/chi1 = T1/T2 = 200/100 = 2. So chi2 = 0.0150.'),
    ('10', 'Current Elec.', 'Five equal resistances each of R ohm are connected as a Wheatstone bridge. The equivalent resistance between the battery terminals is:', 'A) R/2', 'B) R', 'C) 2R', 'D) 5R', 'B', 'Balanced Wheatstone bridge: equivalent resistance = R.'),
    ('11', 'EM Waves', 'The ratio of contributions made by the electric field and magnetic field components to the intensity of an EM wave is:', 'A) c : 1', 'B) 1 : 1', 'C) c^2 : 1', 'D) sqrt(c) : 1', 'B', 'In EM wave, energy is equally shared between electric and magnetic fields.'),
    ('12', 'Capacitance', 'Two capacitors of 2 muF and 3 muF are connected in series. The total capacitance is:', 'A) 5 muF', 'B) 1.2 muF', 'C) 6 muF', 'D) 0.8 muF', 'B', '1/C = 1/2 + 1/3 = 5/6, so C = 6/5 = 1.2 muF.'),
    ('13', 'Magnetism', 'A proton and an alpha particle enter a uniform magnetic field with the same velocity. The ratio of the radii of their paths r_p/r_alpha is:', 'A) 1 : 1', 'B) 1 : 2', 'C) 2 : 1', 'D) 1 : 4', 'C', 'r = mv/(qB). For same v, r proportional to m/q. p: m, q=e; alpha: 4m, q=2e. Ratio = (m/e)/(4m/2e) = 2/1.'),
    ('14', 'EMI', 'The self-inductance of a solenoid of length L, area A and total turns N is:', 'A) mu_0 N^2 A / L', 'B) mu_0 N A / L', 'C) mu_0 N^2 A L', 'D) mu_0 N A L', 'A', 'L = mu_0 N^2 A / L.'),
    ('15', 'AC', 'The power factor of a purely inductive circuit is:', 'A) 1', 'B) 0', 'C) 0.5', 'D) Infinite', 'B', 'Power factor = cos phi. For purely inductive, phi = 90 degree, so cos phi = 0.'),
    ('16', 'Electrostatics', 'An electric dipole is placed in a non-uniform electric field. It experiences:', 'A) Only force', 'B) Only torque', 'C) Both force and torque', 'D) Neither', 'C', 'In non-uniform field, dipole experiences both force (due to field gradient) and torque.'),
    ('17', 'Current Elec.', 'A wire of resistance R is stretched to double its length. The new resistance is:', 'A) 2R', 'B) 4R', 'C) R/2', 'D) R/4', 'B', 'R = rho*L/A. When length doubles, volume constant, so area halves. New R = rho*(2L)/(A/2) = 4R.'),
    ('18', 'Magnetism', 'At a certain place, the horizontal component of earth magnetic field is sqrt(3) times the vertical component. The angle of dip at this place is:', 'A) 30 degree', 'B) 60 degree', 'C) 45 degree', 'D) 0 degree', 'A', 'tan delta = B_v/B_h = 1/sqrt(3), so delta = 30 degree.'),
    ('19', 'EMI', 'If the number of turns in a coil is doubled without changing its length and area, the self-inductance becomes:', 'A) Double', 'B) Four times', 'C) Half', 'D) Unchanged', 'B', 'L proportional to N^2. Doubling N gives L becomes 4 times.'),
    ('20', 'AC', 'The peak value of an AC voltage is 440 V. Its RMS value is:', 'A) 311 V', 'B) 220 V', 'C) 440 V', 'D) 622 V', 'A', 'V_rms = V_peak/sqrt(2) = 440/1.414 = 311 V.'),
    ('21', 'Electrostatics', 'The capacitance of a spherical conductor of radius 1 m is:', 'A) 1.1 x 10^-10 F', 'B) 9 x 10^9 F', 'C) 10^-6 F', 'D) 1 F', 'A', 'C = 4 pi epsilon_0 R = (1/9 x 10^9) x 1 = 1.11 x 10^-10 F.'),
    ('22', 'Current Elec.', 'In a potentiometer experiment, the balancing length is 250 cm for a cell. When the cell is shunted by 10 ohm, the balancing length becomes 200 cm. The internal resistance of the cell is:', 'A) 2 ohm', 'B) 2.5 ohm', 'C) 5 ohm', 'D) 1.25 ohm', 'B', 'V = kl*250, V_shunted = kl*200. Also V_shunted = E*R/(R+r). Solving: r = 2.5 ohm.'),
    ('23', 'Magnetism', 'A galvanometer of resistance 100 ohm gives full scale deflection for 10 mA current. To use it as an ammeter of range 10 A, the shunt resistance required is:', 'A) 0.1 ohm', 'B) 0.01 ohm', 'C) 1 ohm', 'D) 10 ohm', 'A', 'I_g*R_g = I_s*R_s. 0.01*100 = 10*R_s, R_s = 0.1 ohm.'),
    ('24', 'EMI', 'Two coils of self-inductances 2 mH and 8 mH are placed close to each other. The maximum mutual inductance between them is:', 'A) 10 mH', 'B) 6 mH', 'C) 4 mH', 'D) 16 mH', 'C', 'M_max = sqrt(L1*L2) = sqrt(2*8) = 4 mH.'),
    ('25', 'AC', 'In a series LCR circuit, if V_L = V_C = 100 V and V_R = 50 V, the total applied voltage is:', 'A) 250 V', 'B) 200 V', 'C) 50 V', 'D) 100 V', 'C', 'V = sqrt(V_R^2 + (V_L - V_C)^2) = sqrt(50^2 + 0) = 50 V.'),
    ('26', 'EM Waves', 'The electric field of an EM wave is E = 30 sin(10^8 t - kx) V/m. The peak magnetic field B_0 is:', 'A) 10^-7 T', 'B) 3 x 10^-7 T', 'C) 10^-8 T', 'D) 3 x 10^-8 T', 'A', 'E_0/B_0 = c, so B_0 = 30/(3 x 10^8) = 10^-7 T.'),
    ('27', 'Electrostatics', 'If an electron is accelerated through a potential difference of 1 V, its kinetic energy is:', 'A) 1 J', 'B) 1.6 x 10^-19 J', 'C) 1 eV', 'D) Both B and C', 'D', '1 eV = 1.6 x 10^-19 J. KE = 1 eV = 1.6 x 10^-19 J.'),
    ('28', 'Current Elec.', 'Kirchhoffs second law (Loop rule) is based on the conservation of:', 'A) Charge', 'B) Momentum', 'C) Mass', 'D) Energy', 'D', 'Loop rule is based on conservation of energy (potential drop around loop = 0).'),
    ('29', 'Magnetism', 'The force per unit length between two parallel wires carrying currents I_1 and I_2 separated by distance d is:', 'A) mu_0 I_1 I_2 / (2 pi d)', 'B) mu_0 I_1 I_2 / d', 'C) mu_0 I_1 I_2 / (4 pi d^2)', 'D) mu_0 I_1^2 / d', 'A', 'F/L = (mu_0 I_1 I_2)/(2 pi d).'),
    ('30', 'AC', 'The quality factor Q of a series LCR circuit at resonance is:', 'A) (1/R) sqrt(L/C)', 'B) R sqrt(L/C)', 'C) (1/R) sqrt(C/L)', 'D) omega L R', 'A', 'Q = (omega_0 L)/R = (1/R) sqrt(L/C).'),
]

for q_no, topic, q, a, b, c, d, correct, exp in em_mcqs:
    MCQQuestion.objects.create(
        chapter=chapter,
        question_text=f'({topic}) {q}',
        option_a=a,
        option_b=b,
        option_c=c,
        option_d=d,
        correct_option=correct,
        explanation=exp,
        order=int(q_no)
    )

print(f"Added {len(em_mcqs)} MCQs to Electromagnetism")

print("\n" + "=" * 60)
print("DONE! JEE Physics PYQs Added")
print("=" * 60)