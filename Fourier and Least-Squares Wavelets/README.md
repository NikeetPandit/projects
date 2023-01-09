# On Wavelets
In this report, I investigate the principle and theory of wavelets, looking at both Fourier wavelets and Least-Squares Wavelets. I abridge this theoretical discussion to three practical applications. Specifically, anyone using MATLAB’s CWT function, Dr. Ghaderpour’s JUST package, or requiring the usage of multi-resolution analysis in 2D will find this manuscript helpful since I connect very thoroughly theory to the written software and then experimentation. 
## (1) Matched Filtering 
Matched filtering involves detecting a known signal in another signal. This can be used to determine the location of the known signal in another signal and the scaling between the two. Using a time reversal convolution of the known signal with another signal is the standard optimal estimator for detecting a known signal. 
I employ, using least-squares wavelets, a novel method that actual shifts and scales the known signal, across the unknown signal, to locate and detect the known signal in the unknown signal. In my project report, I show that it performed very well while the normally matched filter did not work at all. In addition to scaling information in a vertical sense, my method provides horizontal scaling between the signal and the unknown signal; this is does not only detect the location and amplitude of the known signal and unknown signal, it determines the location. This is due to the scaling and dilating nature of wavelets, and in-particular least-squares wavelets which is a highly redundant transform. 


## (2) Least-Squares Wavelets vs Fourier Wavelets
In this application, I compare exhaustively Fourier wavelets (i.e., continuous wavelet transform) and least-squares wavelets (i.e., least-squares wavelet analysis). Least-squares wavelet has the benefit that, unlike Fourier wavelets, is not constrained to strict requirements like evenly spaced data and non-stationarity. The least-squares wavelet analysis (LSWA) – found here: https://github.com/Ghaderpour/LSWAVE-SignalProcessing takes in particularly two parameters LO and L1. Anyone using the LSWA will find my testing useful since these two parameters can be quite hard to interpret. In essence, they provide the parameterization for time-frequency resolution which is a very great flexibility that Fourier wavelets simply do not offer for signal processing. 

## (3) Multi-Resolution Analysis in Wavelets: 2D
In this application, I develop a simple routine for performing MRA in 2D using wavelets. See function in GitHub. Since the discrete-wavelet transform (DWT) downsampled each level, in the return of the function it upsamples back to the original resolution using Sinc interpolation; theoretically this will completely restore the signal due to its band-limited nature without any aliasing. 

--------------------------------------------

<div class="container" style="display: inline-block;">  
  <figure>
  <div style="float: left; padding: 8px;">
    <img src='https://github.com/NikeetPandit/projects/blob/main/Fourier%20and%20Least-Squares%20Wavelets/functions/IM/read_me_IM.png' width="450" height="350" align="center"/>
    <figcaption align="center"><b>Using function MRAinWavelet_Fun2D to perform MRA of photo</b></figcaption>
  </div>

  <div style="float: right; padding: 8px;">
    <img src='https://github.com/NikeetPandit/practice/blob/main/Spectral%20Analysis%20Work/functions/IM/read_me_IM2.PNG' width="450" height="350" align="center"/>
    <figcaption align="center"><b>Spectrogram of Aphex Twin's Song Equation</b></figcaption>
  </div>
  </figure>
</div>

--------------------------------------------

### Cite As
Nikeet Pandit (2023). Image Processing Work (https://github.com/NikeetPandit/practice)
* Use functions at own risk

