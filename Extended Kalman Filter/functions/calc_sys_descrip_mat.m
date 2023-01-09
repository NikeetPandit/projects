%% Calculation of Jacobian Matrix F
function [F,F_Mat] = calc_sys_descrip_mat(pos_vec)

mu = 3.986004418e14;
Re = 6378.16e3; % m
J2 = 1.082629e-3;
x = pos_vec(1); y = pos_vec(2); z = pos_vec(3); 

df1_dx = -(2*mu*(x^2 + y^2 + z^2)^3 - 6*mu*x^2*(x^2 + y^2 + z^2)^2 + 3*J2*Re^2*mu*(x^2 + y^2 + z^2)^2 + ...
    105*J2*Re^2*mu*x^2*z^2 - 15*J2*Re^2*mu*x^2*(x^2 + y^2 + z^2) - 15*J2*Re^2*mu*z^2*(x^2 + y^2 + z^2))/(2*(x^2 + y^2 + z^2)^(9/2));

df1_dy = (6*mu*x*y*(x^2 + y^2 + z^2)^2 - 105*J2*Re^2*mu*x*y*z^2 + 15*J2*Re^2*mu*x*y*(x^2 + y^2 + z^2))/(2*(x^2 + y^2 + z^2)^(9/2));

df1_dz = (6*mu*x*z*(x^2 + y^2 + z^2)^2 - 105*J2*Re^2*mu*x*z^3 + 45*J2*Re^2*mu*x*z*(x^2 + y^2 + z^2))/(2*(x^2 + y^2 + z^2)^(9/2));

df2_dx = (6*mu*x*y*(x^2 + y^2 + z^2)^2 - 105*J2*Re^2*mu*x*y*z^2 + 15*J2*Re^2*mu*x*y*(x^2 + y^2 + z^2))/(2*(x^2 + y^2 + z^2)^(9/2));

df2_dy = -(2*mu*(x^2 + y^2 + z^2)^3 - 6*mu*y^2*(x^2 + y^2 + z^2)^2 + 3*J2*Re^2*mu*(x^2 + y^2 + z^2)^2 + 105*J2*Re^2*mu*y^2*z^2 ...
    - 15*J2*Re^2*mu*y^2*(x^2 + y^2 + z^2) - 15*J2*Re^2*mu*z^2*(x^2 + y^2 + z^2))/(2*(x^2 + y^2 + z^2)^(9/2));


df2_dz = (6*mu*y*z*(x^2 + y^2 + z^2)^2 - 105*J2*Re^2*mu*y*z^3 + 45*J2*Re^2*mu*y*z*(x^2 + y^2 + z^2))/(2*(x^2 + y^2 + z^2)^(9/2));

df3_dx = (6*mu*x*z*(x^2 + y^2 + z^2)^2 - 105*J2*Re^2*mu*x*z^3 + 45*J2*Re^2*mu*x*z*(x^2 + y^2 + z^2))/(2*(x^2 + y^2 + z^2)^(9/2));

df3_dy = (6*mu*y*z*(x^2 + y^2 + z^2)^2 - 105*J2*Re^2*mu*y*z^3 + 45*J2*Re^2*mu*y*z*(x^2 + y^2 + z^2))/(2*(x^2 + y^2 + z^2)^(9/2));

df3_dz = -(2*mu*(x^2 + y^2 + z^2)^3 - 6*mu*z^2*(x^2 + y^2 + z^2)^2 + 9*J2*Re^2*mu*(x^2 + y^2 + z^2)^2 + 105*J2*Re^2*mu*z^4 - 90*J2*Re^2*mu*z^2*(x^2 + y^2 + z^2))/(2*(x^2 + y^2 + z^2)^(9/2));


F_Mat = [df1_dx df1_dy df1_dz; df2_dx df2_dy df2_dz; df3_dx df3_dy df3_dz];

F = [zeros(3,3) eye(3,3); F_Mat zeros(3,3)]; %Final F System Description Matrix 


%% Non Linear Equations for Motions in ECI Frame:
% -- Symbolic Math is Inserted Above
% -- Matrix if a function of time because elements change but symbolically
% it is static and only needs to be evaluated once 
% 
% syms r x y z J2 Re mu flat_effect
% r = sqrt(x^2+y^2+z^2); 
% flat_effect_A = 1.5*J2*(Re/r)^2*(1-5*(z/r)^2); %Harmonic A
% flat_effect_B = 1.5*J2*(Re/r)^2*(3-5*(z/r)^2); %Harmonic B
% xACC = -((mu*x)/r^3)*(1+flat_effect_A); 
% yACC = -((mu*y)/r^3)*(1+flat_effect_A); 
% zACC = -((mu*z)/r^3)*(1+flat_effect_B); 
% F_Time = simplify(jacobian([xACC; yACC; zACC],[x,y,z]));




