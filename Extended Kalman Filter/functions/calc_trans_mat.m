
function [TransitionMat] = calc_trans_mat(F,delta_t) %Parses in System Design Matrix 
TransitionMat = eye(6,6) + F*delta_t + (F^2*delta_t^2)/factorial(2) + (F^3*delta_t^3)/factorial(3) + (F^4*delta_t^4)/factorial(4);
