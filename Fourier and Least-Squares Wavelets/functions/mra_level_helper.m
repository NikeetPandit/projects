% This funciton determines output frequency for corresponding level of ...
% wavelet decomposition 

% Inputs:
% (1): Max Level of Decomposition 
% (2): Sample Rate
% (3): rate, or freq: type string

% Output
% Level and Corresponding Bands (time)

%-- Written by Nikeet Pandit
function result = mra_level_helper(MaxLvl, Fs, str_select)
    LHS = zeros(MaxLvl-1, 1); RHS = LHS; 
    LHS(1) = 2; RHS(1) = 0; 
    LHS(2) = 4; RHS(2) = 2;
    for i = 2:MaxLvl-1
        LHS(i+1) = 2*LHS(i);
        RHS(i+1) = 2*RHS(i); 
    end
    %LHS(end) = 0; 
    FreqWidth = [LHS RHS]; 
    if str_select == "rate"
        result = [flip((1:MaxLvl)') FreqWidth./Fs]; 
    elseif str_select == "freq"
        result = [flip((1:MaxLvl)') Fs./FreqWidth];
    else
        disp("Incorrect Display Type")
    end

end