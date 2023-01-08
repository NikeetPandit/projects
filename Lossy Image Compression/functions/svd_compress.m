% This function compresses an image using SVD

% Inputs:
% (0) inImage - in image 
% (1) Rank

% Output:
% (0) Approximated Image
% (1) Decomposition Matrix 1
% (2) Decomposition Matrix 2
% (3) Decomposition Matrix 3
% (4) Elapsed Time 
% (5) Cumulative Energy vs Rank

% Written by Nikeet Pandit

function [compIm, U_approx, S_approx, V_approx, elTime,cum_energy] = svd_compress(InImage, rank)

tic

% compute the SVD of I 
[U,S,V] = svd(double(InImage),"econ"); 

% compute the k rank approximation of I 
U_approx = double(U(:,1:rank)); % converting to single precision to write out (save memory)
S_approx = double(S(1:rank,1:rank)); 
V_approx = double(V(:,1:rank)); 

% The compressed Image 
compIm = U_approx*S_approx*(V_approx)'; 

elTime = toc; 

% Returning cumulative energy 
cum_energy = cumsum(diag(S))/sum(diag(S)); 

end