% Compress by Block 
%
% This function performs an operation as selected by the user to each block
% The results from all the blocks are synthesised into the full image

% Inputs:
% (0) inImage - in image 
% (1) Block Size: (1) Block is a square ... must be even 
% (2) CompressType: 'DCT', 'FFT', 
% (3) varargin (1) = Kernel type - 'Gaussian', 'JPEG'
% (4) varargin (2)  = quality... only inputted for JPEG kernel type 
% (5) varagin  (3) = DO - cut off frequency

% Outputs:
% (1) Recovered (after compression) Image
% (2) Compressed image
% (3) Kernel (for weighting of coefficients)
% (4) Elapsed Time

function [I_recovered, I_compressed, kernel, elTime] = block_compress(inImage, BlockSize, CompressType, varargin)
    %--- Converting image to double
    inImage = double(inImage); CompressType = lower(CompressType); 
    
    %--- Setting variable inputs 
    if length(varargin) == 1
        kernel_type = lower(varargin{1}); 
    elseif length(varargin) == 2
        kernel_type = lower(varargin{1}); 
        quality = varargin{2}; 
    elseif length(varargin) == 3
        kernel_type = lower(varargin{1}); 
        quality = varargin{2}; 
        DO = varargin{3}; 
    end
    tic
    if kernel_type == "jpeg"
        kernel = ...
        [16 11 10 16 24 40 51 61
         12 12 14 19 26 58 60 55
         14 13 16 24 40 57 69 56
         14 17 22 29 51 87 80 62
         18 22 37 56 68 109 103 77
         24 35 55 64 81 104 113 92
         49 64 78 87 103 121 120 101
         72 92 95 98 112 100 103 99]; %default kernel selection
        kernel = kernel*quality; 
     
        %--- Interpolating JPEG kernel to block size if not 8
        if BlockSize ~= 8
            [X, Y] = meshgrid(1:8, 1:8);
            [Xq, Yq] = meshgrid(linspace(1,8,BlockSize)); 
            kernel = interp2(X,Y,kernel,Xq,Yq,'cubic');
        end
        
    elseif kernel_type == "gaussian"
        addpath('Calc - Fun'); 
        [~, kernel, ~, ~, ~, ~] = lowpass_im(inImage(1:BlockSize/2,1:BlockSize/2), DO, kernel_type, 'FFT');
        
    else
        disp('Invalid Kernel Selection');
        return
    end
 
    %--- Applying compressiong to block based on user selection 
    switch CompressType
        case 'dct'
        %--- applying quantization to each block
        fun_dct_quant = @(block_struct) round(((dct2(block_struct.data)))./kernel);
        I_compressed = (blockproc(inImage,[BlockSize, BlockSize],fun_dct_quant));
        elTime = toc;
        
        %--- recovering image
        fun_dct_recover = @(block_struct) (idct2(block_struct.data.*kernel));
        I_recovered = blockproc(I_compressed,[BlockSize, BlockSize],fun_dct_recover);
        I_recovered = uint8(I_recovered); 
        
        case 'fft'
        %--- applying quantization to each block
        fun_fft_quant = @(block_struct) round(((fft2(block_struct.data)))./kernel);
        I_compressed = (blockproc(inImage,[BlockSize, BlockSize],fun_fft_quant));
        
        %--- recovering image
        fun_dct_recover = @(block_struct) real((ifft2(block_struct.data.*kernel)));
        I_recovered = blockproc(I_compressed,[BlockSize, BlockSize],fun_dct_recover);
        
        otherwise
            disp("Invalid Compress Type Selection")
    end





