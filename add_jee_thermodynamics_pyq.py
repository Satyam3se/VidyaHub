import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Chapter, MCQQuestion

chapter = Chapter.objects.get(name='Thermodynamics', subject__name='Physics', subject__grade__name='JEE')
print('Chapter:', chapter.name)

mcqs_data = [
    ('01', 'First Law', r'If delta U and delta W represent the increase in internal energy and work done by the system respectively in a thermodynamical process, which of the following is true?', r'A) delta U = -delta Q + delta W', r'B) delta U = delta Q - delta W', r'C) delta U = delta Q + delta W', r'D) delta U = delta W - delta Q', 'B', 'First law of thermodynamics: delta Q = delta U + delta W, so delta U = delta Q - delta W.'),
    ('02', 'Adiabatic', r'For an adiabatic process, the relation between V and T is TV^x = constant. The value of x is:', r'A) gamma', r'B) gamma - 1', r'C) 1 - gamma', r'D) 1/gamma', 'B', 'For adiabatic process: TV^(gamma-1) = constant, so x = gamma - 1.'),
    ('03', 'KTG', r'The temperature at which the RMS speed of hydrogen molecules is equal to the RMS speed of oxygen molecules at 47C is:', r'A) 20 K', r'B) 80 K', r'C) -73C', r'D) 320 K', 'A', 'v_rms = sqrt(3kT/M). For H2 and O2 at same v_rms: T_H2/T_O2 = M_H2/M_O2 = 2/32 = 1/16. So T_H2 = 320/16 = 20 K.'),
    ('04', 'Heat Engine', r'A Carnot engine working between 300 K and 600 K has work output of 800 J per cycle. The amount of heat energy supplied from the source is:', r'A) 800 J', r'B) 1600 J', r'C) 1200 J', r'D) 2400 J', 'B', 'Efficiency eta = 1 - T_c/T_h = 1 - 300/600 = 0.5. Also eta = W/Q_h, so Q_h = W/eta = 800/0.5 = 1600 J.'),
    ('05', 'Degrees of Freedom', r'The molar specific heat at constant volume of a mixture of n1 moles of monatomic gas and n2 moles of diatomic gas is:', r'A) (3n1 + 5n2)/(2(n1 + n2))R', r'B) (5n1 + 3n2)/(2(n1 + n2))R', r'C) (n1 + n2)/2 R', r'D) 3R', 'A', 'Cv = f/2 * R. Monatomic f=3, diatomic f=5. So Cv_mix = (3n1 + 5n2)/(n1+n2) * R/2.'),
    ('06', 'Isothermal', r'Work done in an isothermal expansion of an ideal gas from volume V1 to V2 is:', r'A) nRT ln(V2/V1)', r'B) nRT (V2/V1)', r'C) nRT ln(V1/V2)', r'D) P(V2-V1)', 'A', 'For isothermal process: W = nRT ln(V2/V1).'),
    ('07', 'Radiation', r'A spherical black body with a radius of 12 cm radiates 450 W power at 500 K. If the radius were halved and the temperature doubled, the power radiated in watt would be:', r'A) 450', r'B) 1000', r'C) 1800', r'D) 225', 'C', 'P = e*sigma*A*T^4. New radius = 6 cm, T = 1000 K. P_new = P*(r_new/r)^4*(T_new/T)^4 = 450*(1/2)^4*(2)^4 = 450*16/16 = 450? Wait: (1/2)^4*(2)^4 = 1, so 450. Correction: (1/2)^3*(2)^4 = 1*2 = 2, wait: Area = 4piR^2, so ratio = (r_new/r)^2*(T_new/T)^4 = (1/2)^2*(2)^4 = 1/4*16 = 4. P_new = 450*4 = 1800 W.'),
    ('08', 'Specific Heat', r'If gamma is the ratio of specific heats and R is the universal gas constant, then molar specific heat at constant volume Cv is:', r'A) R/(gamma-1)', r'B) gamma R/(gamma-1)', r'C) R(gamma-1)', r'D) gamma R', 'A', 'Cp/Cv = gamma, Cp - Cv = R. Solving: Cv = R/(gamma-1).'),
    ('09', 'Cyclic Process', r'In a cyclic process, the change in internal energy of a system is:', r'A) Positive', r'B) Negative', r'C) Zero', r'D) Dependent on path', 'C', 'Internal energy is a state function, so for a cyclic process delta U = 0.'),
    ('10', 'KTG', r'The average translational kinetic energy of a gas molecule at temperature T is:', r'A) (1/2)kT', r'B) (3/2)kT', r'C) kT', r'D) (5/2)kT', 'B', 'For ideal gas, average translational KE = 3/2 kT.'),
    ('11', 'Calorimetry', r'10 g of ice at 0C is mixed with 10 g of water at 10C. The final temperature of the mixture is:', r'A) 10C', r'B) 5C', r'C) 0C', r'D) -5C', 'C', 'Heat lost by water to cool to 0C: 10*1*10 = 100 cal. Heat required to melt ice: 10*80 = 800 cal. Since 100 < 800, all ice melts and final temp is 0C.'),
    ('12', 'Heat Transfer', r'The thermal conductivity of a rod depends on:', r'A) Length', r'B) Area of cross-section', r'C) Temperature difference', r'D) Material of the rod', 'D', 'Thermal conductivity is a material property and does not depend on dimensions or temperature difference.'),
    ('13', 'Entropy', r'During an adiabatic expansion, the entropy of the system:', r'A) Increases', r'B) Decreases', r'C) Remains constant', r'D) Becomes zero', 'C', 'Adiabatic process is isentropic, entropy remains constant.'),
    ('14', 'Newton''s Cooling', r'A hot liquid cools from 80C to 70C in 2 minutes. The time taken for it to cool from 60C to 50C will be:', r'A) 2 min', r'B) Less than 2 min', r'C) More than 2 min', r'D) 4 min', 'C', 'Rate of cooling proportional to temperature difference. At higher temp difference, cools faster. So takes more time for same temperature drop at lower difference.'),
    ('15', 'Internal Energy', r'The internal energy of an ideal gas is a function of:', r'A) Pressure only', r'B) Volume only', r'C) Temperature only', r'D) Both P and V', 'C', 'For ideal gas, internal energy depends only on temperature.'),
    ('16', 'Work Done', r'Which of the following is a path-dependent function?', r'A) Internal Energy', r'B) Temperature', r'C) Work done', r'D) Pressure', 'C', 'Work done is a path function, not a state function.'),
    ('17', 'Mayer''s Formula', r'For one mole of an ideal gas, Cp - Cv is equal to:', r'A) R', r'B) R/J', r'C) 1.98 cal', r'D) All of these', 'D', 'Mayer''s formula: Cp - Cv = R = 8.314 J/mol-K = 1.98 cal/mol-K.'),
    ('18', 'KTG', r'If the pressure of an ideal gas is halved and its volume is doubled, its temperature will:', r'A) Remain constant', r'B) Become double', r'C) Become four times', r'D) Become half', 'A', 'PV = nRT. P becomes P/2, V becomes 2V. So new T = (P*2V)/(nR) = 2(PV)/(nR) = 2T? Wait: P1V1/T1 = P2V2/T2. (P/2 * 2V)/T2 = PV/T => P/T2 = PV/T => T2 = T. Temperature remains constant.'),
    ('19', 'Black Body', r'The wavelength of maximum emission lambda_m and absolute temperature T are related as:', r'A) lambda_m T = constant', r'B) lambda_m / T = constant', r'C) T / lambda_m = constant', r'D) lambda_m + T = constant', 'A', 'Wien''s displacement law: lambda_m * T = constant (b = 2.898 x 10^-3 m-K).'),
    ('20', 'Free Expansion', r'In the free expansion of a gas, which of the following is true?', r'A) W = 0', r'B) delta U = 0', r'C) Q = 0', r'D) All of the above', 'D', 'Free expansion is adiabatic and against zero pressure, so W=0, Q=0. For ideal gas, internal energy constant, so delta U = 0.'),
    ('21', 'Adiabatic', r'A diatomic gas is compressed to 1/32 times its initial volume adiabatically. If initial temperature is T, final temperature is:', r'A) 4T', r'B) 8T', r'C) 2T', r'D) 16T', 'A', 'TV^(gamma-1) = constant. For diatomic gamma = 7/5 = 1.4. V2 = V1/32. T2 = T1*(V1/V2)^(gamma-1) = T*(32)^(0.4) = T*4. So final temperature = 4T.'),
    ('22', 'Efficiency', r'If the temperature of the sink is decreased, the efficiency of a Carnot engine:', r'A) Increases', r'B) Decreases', r'C) Remains same', r'D) Becomes zero', 'A', 'Efficiency eta = 1 - Tc/Th. Decreasing Tc increases efficiency.'),
    ('23', 'Mean Free Path', r'The mean free path lambda of gas molecules varies with density rho as:', r'A) lambda proportional to rho', r'B) lambda proportional to 1/rho', r'C) lambda proportional to sqrt(rho)', r'D) lambda proportional to rho^2', 'B', 'Mean free path lambda = 1/(sqrt(2)*pi*d^2*n), where n is number density. So lambda inversely proportional to density.'),
    ('24', 'Radiation', r'Two stars emit maximum radiation at 3600 A and 4800 A. The ratio of their temperatures is:', r'A) 3:4', r'B) 4:3', r'C) 9:16', r'D) 16:9', 'B', 'Wien''s law: lambda1*T1 = lambda2*T2. So T1/T2 = lambda2/lambda1 = 4800/3600 = 4/3.'),
    ('25', 'Internal Energy', r'Change in internal energy of an ideal gas in an isothermal process is:', r'A) Positive', r'B) Negative', r'C) Zero', r'D) Infinite', 'C', 'For ideal gas, internal energy depends only on temperature. In isothermal process, temperature constant, so delta U = 0.'),
    ('26', 'Stefan''s Law', r'The energy radiated per second by a black body at T K is E. If temperature is doubled, energy becomes:', r'A) 2E', r'B) 4E', r'C) 8E', r'D) 16E', 'D', 'Stefan''s law: P = e*sigma*A*T^4. If T doubles, P becomes 2^4 = 16 times.'),
    ('27', 'Molar Heat', r'The ratio Cp/Cv for a monatomic gas is:', r'A) 1.67', r'B) 1.40', r'C) 1.33', r'D) 1.00', 'A', 'For monatomic gas:Cv = 3R/2, Cp = 5R/2, so Cp/Cv = 5/3 = 1.67.'),
    ('28', 'Latent Heat', r'Heat required to convert 1 g of ice at 0C to steam at 100C is:', r'A) 80 cal', r'B) 540 cal', r'C) 620 cal', r'D) 720 cal', 'D', 'Heat = heat to melt ice (80 cal) + heat to warm water (100 cal) + heat to vaporize (540 cal) = 720 cal.'),
    ('29', 'Isobaric', r'In an isobaric process, work done by the gas is P delta V. This work is also equal to:', r'A) nR delta T', r'B) Cp delta T', r'C) Cv delta T', r'D) delta U', 'A', 'For isobaric process: W = P delta V = nR delta T.'),
    ('30', 'Second Law', r'A heat engine rejects 600 J of heat to the sink for every 1000 J of heat absorbed from the source. Its efficiency is:', r'A) 60%', r'B) 40%', r'C) 100%', r'D) 20%', 'B', 'Efficiency = W/Q_h = (Q_h - Q_c)/Q_h = (1000 - 600)/1000 = 0.4 = 40%.'),
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

print(f'Added {len(mcqs_data)} MCQs to Thermodynamics chapter')