%--- Function takes input series and makes it gappy where each data point
% has a probability of being gappy
% Written by Nikeet Pandit

function [xOut, yOut] = make_gappy(xIn, yIn, ProbOfGap)

%--- Determine Length of Series
len = numel(yIn); 

%--- Construct Random Numbers and Index Based on Prob.
r = rand([1, len])*10; 
ProbOfGap = ProbOfGap*10; 

IndexKeep = ProbOfGap < r; 

yOut = yIn(IndexKeep); 
xOut = xIn(IndexKeep);

end