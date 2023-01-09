% --- FUNCTION SUMMARY --- %
% Performs MRA in Wavelets for 2D Case

%--- Inputs --- %
% x - locator along horizontal (for ex longitude)
% y - locator along vertical (for ex latitude)
% z - amplitude indexed by (x,y)
% wname - wavelet function -
% for wname... see https://www.mathworks.com/help/wavelet/ref/wfilters.html
% for wname... see https://www.mathworks.com/help/wavelet/gs/choose-a-wavelet.html
% LevelOfDecomp - select level of decompostion 
% ... use https://www.mathworks.com/help/wavelet/ref/wmaxlev.html 
% to determine max. level of decomposition allowable based on wname!

% if x, y, z ... are 1D vectors (columns) 
%   function will grid inside
% else
%   function will asume gridding as provided by user where x and y are []
%
% Since there is downsampling after each step of the DWT... the returned
% decomposed levels are interpolated via Sinc interpolation which
% theoretically perfectly reconstructs the signal do the band-limited
% nature

%--- Outputs --- %
% Decomp - MRA decomposition level x
% Level - corresponds to level of decomposition 

%------ Written by Nikeet Pandit



function [Decompostion, Level] = MRAinWavelet_Fun2D(x, y, z, wname, LevelOfDecomp)


%--- Check Dimensions 
if ~isequal(size(x), size(y), size(z)) && ~isempty(y) && ~isempty(z)
    error("Inputed Data is not same dimensions!");
end

%--- If Data is columns... GRID!
if isvector(x)
    [~, ~, Z] = xyz2grid(x,y,z);
else
    Z = z; 
end


%--- Do Wavelet Decomposition Specified by gridded Z
[C, S] = wavedec2(Z, LevelOfDecomp, wname); 

%--- Get approximation coefficient (LP result) 
%--- At lowest level of decomposition 
A = appcoef2(C,S,wname, LevelOfDecomp); 

D = num2cell(zeros(1,LevelOfDecomp)); %Initializing Detail Coeffficient Cell Array

%--- Do all decompositions specified by N
%--- Add all detail coefficients to D
for i = 1:LevelOfDecomp
    [h,v,d] = detcoef2('all', C, S, i);
    D{i} = h+v+d; 
end

%--- Add approximation coefficient to lowest level of decomposition
D{end} = A + D{end}; 

%--- Do 2D Sinc Interpolation
[M, N] = size(Z); Decompostion = num2cell(zeros(1,length(D)));
for i = 1:length(D)
    Decompostion{i} = (sincInterp2D(D{i}, M, N))/(2^i); %Scale down by level of decompostion? (EXPERIMENTAL)
end

Decompostion = flip(Decompostion); %Flipping to match level 

%--- Determine level of decompostion 
Level = mra_level_helper(LevelOfDecomp, 1, 'rate');

end


