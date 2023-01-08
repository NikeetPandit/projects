% Ideal FFT Compression (method described in report)

% This function performs wavelet compression (DWT)
% Inputs: 
% (0) inImage - in image 
% (1) percent - percent of coefficients to keep

% Output
% (0) Input Image Spectrum
% (1) Compressed Image Spectrum 
% (2) Compressed Image
% (3) Elapsed time 

% Written by Changin Oh 



function [spInImage, spCompImage, compImage, elTime] = compressWithFFT(inImage, percent)

% Display error message if wrong percentage is given
if (percent > 100) || (percent < 0)
    error("Specify percentage correctly.")
end

% Measure time
tic

% Perform Fourier transform of image
trImage = fft2(inImage);

% Sort coefficients by magnitude
coeffs = sort(abs(trImage(:)));

% Convert percentage into ratio
ratio = percent*0.01;

% Decide threshold level based on what percentage to keep coefficients
threshold = coeffs(floor(length(coeffs)*(1-ratio)));

% Find positions of coefficients whose magnitude is greater than threshold
positions = abs(trImage) > threshold;

% Keep coefficients whose magnitude is greater than threshold
trCompImage = trImage.*positions;

% Obtain compressed image
compImage = uint8(ifft2(trCompImage));

% Save time
elTime = toc;

% Make spectrum of input image
spInImage = log(abs(fftshift(trImage))+1);

% Make spectrum of compressed image
spCompImage = log(abs(fftshift(trCompImage))+1);
end