%Numerical Integration Method: RK4 to find numerical solution to dynamic equations

function [state_prop] = rk4_prop(state_vec_old,h)
r = state_vec_old(1:3); v = state_vec_old(4:6);
k1 = [v calc_acc(r)]; %[dr dv]
k2 = [v + (k1(4:end)/2)*h calc_acc(r+(k1(1:3)/2)*h)];
k3 = [v + (k2(4:end)/2)*h calc_acc(r+(k2(1:3)/2)*h)];
k4 = [v + k3(4:end)*h calc_acc(r+k3(1:3)*h)]; 

state_prop = state_vec_old + (1/6)*h*(k1+2*k2+2*k3+k4); 

% %% Propagating Covariance
% 
% F_k1 = calc_sys_descrip_mat(r);
% F_k2 = calc_sys_descrip_mat(r + k1(1:3)*h/2);
% F_k3 = calc_sys_descrip_mat(r + k2(1:3)*h/2);
% F_k4 = calc_sys_descrip_mat(r + k3(1:3)*h);
% 
% k1_P = F_k1*covariance_old + covariance_old*F_k1' + Q;
% k2_P = F_k2*(covariance_old + k1_P*h/2) + (covariance_old + ...
% k1_P*h/2)*F_k2' + Q;
% k3_P = F_k3*(covariance_old + k2_P*h/2) + (covariance_old + ...
% k2_P*h/2)*F_k3' + Q;
% k4_P = F_k4*(covariance_old + k3_P*h) + (covariance_old + ...
% k3_P*h)*F_k4' + Q;
% 
% covariance_new = covariance_old + h/6 * (k1_P + 2*k2_P + 2*k3_P + k4_P);



