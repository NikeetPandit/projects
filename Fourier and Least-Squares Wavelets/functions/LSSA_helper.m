function result = LSSA_helper(CScoeff,return_type,varargin)

%% This function calculates based on selection from CS_coeff
% --- Inputs 
% (1) CS_coeff - Estimated coefficients of cosine and sine functions
% (2) String Selector: Option A) 'Amplitude', Option B) 'PSD', 'Power'
% (3) Must input time vector for PSD option 
% --- Outputs
% (1) Amplitude spectrum
% (2) Power Spectrum
% (3) PSD 
%
% Written by Nikeet Pandit

return_type = lower(return_type); 

if length(varargin) == 1
    Omega = varargin{1}';
end

CScoeff = reshape(CScoeff, 2, [] )'; %reshaping 1D array to 2D array with cosine and sine term corresponding to 1 and 2 column

switch return_type
    case 'amplitude'
        result = vecnorm(CScoeff,2,2);
        
    case 'power'
        result = (vecnorm(CScoeff,2,2).^2)/2;

    case 'psd'
%         result_pwr = (vecnorm(CScoeff,2,2).^2)/2;
%         result_var = rms(result_pwr).^2; 
%         result = result_pwr/result_var; 
        result_pwr = (vecnorm(CScoeff,2,2).^2)/2;
        result = 2*rdivide(result_pwr,Omega); %2 sided spec
        
end