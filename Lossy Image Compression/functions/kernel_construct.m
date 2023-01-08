% Kernel Construct Fun

% Inputs:
% (1) DO is cut off frequency 
% (2) P and Q are dimensions of padded kernel size
% (3) type is class string 
% Options are: Gaussian, Butterworth

% Output:
% (1): Low pass kernel in frequency domain

% Written by Nikeet Pandit


function kernel = kernel_construct(D0, P, Q, type,varargin)

if length(varargin) ==1
    n = varargin{1}; 
end

type = lower(type);
u = 0:P-1; %frequency components
v = 0:Q-1; 
[U, V] = meshgrid(u,v); 
D = hypot(U-P/2, V-Q/2); %calculating distances

if type == "gaussian"
    kernel = fftshift(exp(-(D.^2)./(2*(D0^2))))'; %Shifts kernel to nominal fft2 position (uncentered)
    
elseif type == "butterworth"
    NumExp = D; 
    DenExp = D0; 
    %kernel = fftshift(1./(1+((NumExp./DenExp).^(2*n))))'; %Butterworth T.F. (uncentered)
    Den = 1 + (D./D0)^(2*n); 
    kernel = fftshift(1./Den)'; 
  
end