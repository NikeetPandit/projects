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
    <img src='https://github.com/NikeetPandit/projects/blob/main/Satellite%20Tracking%20Project/functions/IM/read_me_IM.PNG' width="450" height="350" align="center"/>
    <figcaption align="center"><b>Verification in Systems Tool Kit</b></figcaption>
  </div>

  <div style="float: right; padding: 8px;">
    <img src='https://github.com/NikeetPandit/projects/blob/main/Satellite%20Tracking%20Project/functions/IM/read_me_IM_2.PNG' width="450" height="350" align="center"/>
    <figcaption align="center"><b>Spectrum Analyzer at ARO while Driving Dish to GPS Satellite: GPS L1 Signal: 1574.42MHz </b></figcaption>
  </div>
  </figure>
</div>

--------------------------------------------
### Cite As
All functions here have been collaboratively worked on by Nikeet Pandit and Diego Mateos. 

Nikeet Pandit and Diego Mateos (2023). Image Processing Work (https://github.com/NikeetPandit/practice)
* Use functions at own risk. Do not use for any academic purposes (i.e, Space Hardware). 
