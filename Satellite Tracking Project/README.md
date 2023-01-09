# Satellite Tracking 
The purpose of this project is to apply theoretical knowledge of orbital mechanics to application; this algorithm’s output has been used to point and drive the Algonquin Radio Observatory (ARO) 46m antenna dish to receive a downlink signal (see photo below). 
### How to Use
1.	Download a TLE file from https://celestrak.org/ and place into “Inputs” folder. Go to Parse module, place file name + extension of TLE
2.	Go to Inputs module, place desired tracking interval. See Parse module for input conventions
3.	Go to Inputs module, place desired station parameters. See Parse module for input conventions
4.	Follow On Screen prompts for selecting satellite to track and desired outputs!

### Validation in Systems Tool Kit (STK)
The software, if selected by the user, will output ephemeris data in ECI, ECEF, topocentric coordinate systems formatted to be seamlessly integrated into STK. 
### Modules
Algorithms have been developed for orbit propagation, date calculations, and debugging. All functions have been exhaustively validated and verified. 

--------------------------------------------

<div class="container" style="display: inline-block;">  
  <figure>
  <div style="float: left; padding: 8px;">
    <img src='https://github.com/NikeetPandit/practice/blob/main/Spectral%20Analysis%20Work/functions/IM/read_me_IM.PNG' width="450" height="350" align="center"/>
    <figcaption align="center"><b>Sub-Nyquist Artefacts; Aliasing even when Nyquist condition is obeyed</b></figcaption>
  </div>

  <div style="float: right; padding: 8px;">
    <img src='https://github.com/NikeetPandit/practice/blob/main/Spectral%20Analysis%20Work/functions/IM/read_me_IM2.PNG' width="450" height="350" align="center"/>
    <figcaption align="center"><b>Transient synthetic series which, due to aliasing, keeps folding over itself</b></figcaption>
  </div>
  </figure>
</div>

--------------------------------------------
### Cite As
All functions here have been collaboratively worked on by Nikeet Pandit and Diego Mateos. 
Nikeet Pandit and Diego Mateos (2023). Image Processing Work (https://github.com/NikeetPandit/practice)
* Use functions at own risk