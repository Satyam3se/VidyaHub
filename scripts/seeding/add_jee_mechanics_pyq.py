import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vidyahub.settings')
django.setup()

from main.models import Chapter, MCQQuestion

chapter = Chapter.objects.get(name='Mechanics', subject__name='Physics', subject__grade__name='JEE')
print('Chapter:', chapter.name)

mcqs_data = [
    ('01', 'Rotation', r'A solid sphere is rolling on a frictionless surface, it enters a rough horizontal surface. Which of the following remains constant during the transition?', r'A) Linear Momentum', r'B) Angular Momentum about CM', r'C) Angular Momentum about contact point', r'D) Kinetic Energy', 'C', 'Angular momentum about contact point remains constant because there is no external torque about the contact point.'),
    ('02', 'WPE', r'A particle of mass m is moving in a circular path of constant radius r such that its centripetal acceleration a_c is varying with time t as a_c = k^2 r t^2. The power delivered to the particle by the forces is:', r'A) 2\pi mk^2 r^2 t', r'B) mk^2 r^2 t', r'C) (1/3) mk^4 r^2 t^5', r'D) Zero', 'B', 'Power = F.v = ma_c . v = m(k^2rt^2) . (kr) = mk^2 r^2 t.'),
    ('03', 'COM', r'A man of mass M stands at one end of a plank of length L and mass M/3, which is floating in water. If the man walks to the other end of the plank, the distance that the man moves relative to the water is:', r'A) L/4', r'B) 3L/4', r'C) L/3', r'D) 2L/3', 'A', 'Using center of mass conservation: M.x = (M/3).(L-x), solving gives x = L/4.'),
    ('04', 'Gravity', r'A planet of mass M has two satellites S1 and S2 in circular orbits of radii r and 4r. The ratio of their tangential velocities is:', r'A) 1:2', r'B) 2:1', r'C) 1:4', r'D) 4:1', 'B', 'v = sqrt(GM/r), so v1/v2 = sqrt(4r/r) = 2:1.'),
    ('05', 'Rotation', r'A thin uniform rod of length L and mass M is swinging freely about a horizontal axis passing through its end. Its maximum angular speed is omega. Its center of mass rises to a maximum height of:', r'A) (1/6)(L^2 omega^2/g)', r'B) (1/2)(L^2 omega^2/g)', r'C) (1/3)(L^2 omega^2/g)', r'D) (L^2 omega^2/g)', 'A', 'Using energy conservation: (1/2)Iomega^2 = mgh. For rod about end, I = ML^2/3, CM at L/2. Solving gives h = L^2omega^2/6g.'),
    ('06', 'Fluids', r'A wooden block floats in water with 2/3 of its volume submerged. When the same block floats in oil, 5/6 of its volume is submerged. The density of oil is:', r'A) 0.6 g/cm^3', r'B) 0.8 g/cm^3', r'C) 0.9 g/cm^3', r'D) 1.2 g/cm^3', 'B', 'Using buoyancy: rho_block = (2/3)rho_water. Also rho_block = (5/6)rho_oil. So rho_oil = (2/3)/(5/6) = 0.8 g/cm^3.'),
    ('07', 'NLM', r'A block of mass m is pushed against a vertical wall by a horizontal force F. If the coefficient of friction is mu, the minimum value of F to prevent the block from falling is:', r'A) mu mg', r'B) mg/mu', r'C) mu/mg', r'D) mg', 'B', 'Friction upward = mu*F must balance weight mg, so F = mg/mu.'),
    ('08', 'Rotation', r'A ring, a disc, and a solid sphere (all same M and R) roll down the same inclined plane without slipping. The order of their arrival at the bottom is:', r'A) Ring, Disc, Sphere', r'B) Sphere, Disc, Ring', r'C) Disc, Ring, Sphere', r'D) All arrive together', 'B', 'Sphere has smallest moment of inertia, so largest acceleration. Ring has largest, so smallest acceleration.'),
    ('09', 'Collisions', r'A ball of mass m moving with velocity v strikes a stationary ball of mass 2m head-on. If e = 0.5, the velocity of the first ball after collision is:', r'A) v/2', r'B) Zero', r'C) -v/4', r'D) v/4', 'C', 'Using conservation of momentum and coefficient of restitution: v1 = (m - 2m*e)/(m + 2m) * v = -v/4.'),
    ('10', 'Kinematics', r'A projectile is fired with a velocity u making an angle theta with the horizontal. The radius of curvature of its path at the highest point is:', r'A) u^2 sin^2 theta/g', r'B) u^2 cos^2 theta/g', r'C) u^2/g', r'D) u^2 cos^2 theta/(g sin theta)', 'B', 'At highest point, velocity = u cos theta. Radius of curvature = v^2/a where a = g. So R = u^2 cos^2 theta/g.'),
    ('11', 'Elasticity', r'A wire of length L and cross-section A is stretched by a force F. If Youngs modulus is Y, the energy stored per unit volume is:', r'A) F^2/(2AY)', r'B) F^2/(2A^2Y)', r'C) FY/(2AL)', r'D) F^2L/(2AY)', 'A', 'Strain = FL/(AY), stress = F/A. Energy = (1/2)(stress)(strain) = F^2L/(2AY). Per unit volume = F^2/(2AY).'),
    ('12', 'Rotation', r'The moment of inertia of a square plate of side a and mass M about an axis passing through its center and perpendicular to its plane is:', r'A) Ma^2/6', r'B) Ma^2/12', r'C) Ma^2/3', r'D) 2Ma^2/3', 'A', 'I = I_x + I_y. For square about center: I = Ma^2/12 + Ma^2/12 = Ma^2/6.'),
    ('13', 'WPE', r'A force F = -kx^3 acts on a particle. The work done by this force in moving the particle from x1 to x2 is:', r'A) (k/4)(x1^4 - x2^4)', r'B) (k/4)(x2^4 - x1^4)', r'C) k(x1^2 - x2^2)', r'D) Zero', 'A', 'W = integral F dx = integral -kx^3 dx from x1 to x2 = -k(x2^4 - x1^4)/4 = k(x1^4 - x2^4)/4.'),
    ('14', 'Gravity', r'If the radius of earth shrinks by 1% while mass remains same, the acceleration due to gravity on its surface will:', r'A) Increase by 1%', r'B) Increase by 2%', r'C) Decrease by 1%', r'D) Decrease by 2%', 'B', 'g = GM/R^2. If R becomes 0.99R, g increases by (1/0.99)^2 approximately 1.0201, so increase approximately 2%.'),
    ('15', 'Fluids', r'Terminal velocity v of a spherical ball of radius r falling through a viscous liquid is proportional to:', r'A) r', r'B) r^2', r'C) 1/r', r'D) 1/r^2', 'B', 'For Stokes law: mg = 6*pi*eta*r*v, so v proportional to r^2 (since mg proportional to r^3).'),
    ('16', 'NLM', r'A spring of force constant k is cut into two equal halves. The force constant of each half is:', r'A) k/2', r'B) k', r'C) 2k', r'D) 4k', 'C', 'For same material, k proportional to 1/L. Halving length doubles k to 2k.'),
    ('17', 'COM', r'A shell of mass 200g is ejected from a gun of mass 4kg with a velocity of 80m/s. The recoil velocity of the gun is:', r'A) 4 m/s', r'B) 2 m/s', r'C) 1 m/s', r'D) 8 m/s', 'A', 'Momentum conserved: 4*v = 0.2*80, so v = 4 m/s.'),
    ('18', 'Rotation', r'A couple produces:', r'A) Linear motion', r'B) Rotational motion', r'C) Both A and B', r'D) No motion', 'B', 'A couple is two equal and opposite forces not in line. It produces pure rotation, no translation.'),
    ('19', 'Kinematics', r'If the displacement of a particle is given by s = t^3 - 6t^2 + 3t + 7, the velocity when acceleration is zero is:', r'A) 9 units', r'B) -9 units', r'C) 3 units', r'D) Zero', 'A', 'v = ds/dt = 3t^2 - 12t + 3. a = dv/dt = 6t - 12 = 0 when t = 2. v(2) = 12 - 24 + 3 = -9 units.'),
    ('20', 'WPE', r'A vertical spring is compressed by a distance x and a ball of mass m is placed on it. When released, the ball rises to a height h. The spring constant k is:', r'A) 2mgh/x^2', r'B) mgh/x', r'C) mgh/x^2', r'D) 2mgh/x', 'A', 'Energy conserved: (1/2)kx^2 = mgh, so k = 2mgh/x^2.'),
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

print(f'Added {len(mcqs_data)} MCQs to Mechanics chapter')