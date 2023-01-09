%--- Function shift_dist summary
% Dialates or (compresses) and centres unit normal dist 
% about time vector. Uses propagation of errors. Attempt will 
% be made to use this function for LSSA basis. 

function [distOut] = shift_dist(t,Type)

Type = lower(Type); 

%--- RV propagation (t vector must be even)
%--- Assuming odd t vector
funwidth = 5; 
b = t(ceil(end/2)); %finding offset
t_centred = t - b; 
a = sqrt(t_centred(end)/funwidth); %finding scale
mu0 = 0; sigma0 = 1; 
mu = a*mu0 + b; 
sigma = (a^2*sigma0^2); 

switch Type
    case "gaussian"
        distOut = (1/(sigma*sqrt(2*pi))).*exp((-0.5*(((t-mu).^2)/sigma^2))); 
    case "mhat"
        distOut =  (2/(sqrt(3)*pi^(1/4)))*((1-((t-mu)/sigma).^2).*exp(-(t-mu).^2/(2*sigma^2)));
end
distOut = distOut/norm(distOut); 
end