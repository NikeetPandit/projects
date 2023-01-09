function accel_total = calc_acc(pos_vec)
mu = 3.986004418e14;
Re = 6378.16e3; % m
J2 = 1.082629e-3;
x = pos_vec(1); y = pos_vec(2); z = pos_vec(3); 
r = sqrt(x^2+y^2+z^2); 
flat_effect_A = 1.5*J2*(Re/r)^2*(1-5*(z/r)^2); %Harmonic A
flat_effect_B = 1.5*J2*(Re/r)^2*(3-5*(z/r)^2); %Harmonic B
xACC = -((mu*x)/r^3)*(1+flat_effect_A); 
yACC = -((mu*y)/r^3)*(1+flat_effect_A); 
zACC = -((mu*z)/r^3)*(1+flat_effect_B); 
accel_total = [xACC yACC zACC]; 