import numpy as np
import Fileio as Fio
import Propagate as pgate
import Parse 
import Datefun
import DebuggingV1 as Dbug

#time = dt.datetime(2020,9,22,5,0,0) #test time.

#Parse Tracking Interval 
tstart = Parse.tracking()[0]
tend = Parse.tracking()[1]

#Parse Station Parameters 
STNFIL =  Parse.StationParam() 

#Parse TLE Parameters 
TLE = Parse.TLEParam()

N = int(np.size(TLE)/3) # sat NUM of TLE input file.

def Satlist(TLE):
    N = int(np.size(TLE)/3) 
    SatList = [None]*N
    for i in range (N):
        line0 = TLE[0+3*(i-1)] #Obtain name (line0)
        line1 = np.array((TLE[1+3*(i-1)]).split())[2:] #Obtain line 1 of TLE file (ignore naming conventions - can be added if required)
        line2 = np.array((TLE[2+3*(i-1)]).split())[2:] #Obtain line 2 of TLE file (ignore naming conventions - can be added if required)
        SatList[i] = Fio.Satellite(line0,line1,line2) #create instance of Satellite object & save in SatList
        #Instant = SatList[i].raan #Call atrribute (TLE file parameter) of certain instance
    return SatList

Satellites = Satlist(TLE)      

 
#Initialize 1 station
Stn = Fio.Station(STNFIL); station_latitude = Stn.stnlat              
station_longitude = Stn.stnlong; station_elevation = Stn.stnalt/1000
utc_off = Stn.utc_offset
az_el_nlim = Stn.az_el_nlim
Stn_AZ = Stn.az
StnEL_min = float(np.array(Stn.elmin))
StnEL_max = float(np.array(Stn.elmax))
st_az_speed_max = Stn.st_az_speed_max
st_el_speed_max = Stn.st_el_speed_max 
stn_ecf_position = pgate.station_ECF(station_longitude, station_latitude, station_elevation)  
## End parser


## Look Angle 
def LookAngles(time):
    for i in range(N):
        ts_sat_epoch = Satellites[i].refepoch
        M0_mean_anomaly = Satellites[i].meanan
        n_mean_motion = Satellites[i].meanmo
        n_dot_mean_motion = Satellites[i].ndot
        n_2dots_mean_motion = Satellites[i].nddot6
        eccentricity = Satellites[i].eccn
        omega_longitude_ascending_node = Satellites[i].raan
        omega_argument_periapsis = Satellites[i].argper
        inclination = Satellites[i].incl
        
        #Sequential initialization of orbital parameters required.
        
        #GMST, Mean Anomaly, Mean Anomaly Motion, Eccentric Anomaly 
        Mt_mean_anomaly = pgate.mean_anomaly_motion(time,ts_sat_epoch,M0_mean_anomaly,n_mean_motion,n_dot_mean_motion,n_2dots_mean_motion)[0]
        nt_mean_motion = pgate.mean_anomaly_motion(time,ts_sat_epoch,M0_mean_anomaly,n_mean_motion,n_dot_mean_motion,n_2dots_mean_motion)[1]
        GMST = pgate.THETAJ(time)
        ecc_anomaly = pgate.KeplerEqn(Mt_mean_anomaly,eccentricity)
        
        #ECI POS, VEL, RAAN, PERIGEE, THETA [2, 3, 4]
        eci_position = pgate.sat_ECI(eccentricity,ecc_anomaly,omega_longitude_ascending_node,
                omega_argument_periapsis,inclination,nt_mean_motion,ts_sat_epoch,time)[0]
        eci_velocity = pgate.sat_ECI(eccentricity,ecc_anomaly,omega_longitude_ascending_node,
                omega_argument_periapsis,inclination,nt_mean_motion,ts_sat_epoch,time)[1]
        
        #ECF POS, VEL
        sat_ecf_position = pgate.sat_ECF(time,eci_position,eci_velocity,GMST)[0]
        sat_ecf_velocity = pgate.sat_ECF(time,eci_position,eci_velocity,GMST)[1]
        
        #Topocentric Position and Velocity 
        range_topo_position = pgate.range_ECF2topo(sat_ecf_position,sat_ecf_velocity,station_longitude,station_latitude,stn_ecf_position)[0]
        range_topo_velocity = pgate.range_ECF2topo(sat_ecf_position,sat_ecf_velocity,station_longitude,station_latitude,stn_ecf_position)[1]
        RangeVecSat = pgate.range_ECF2topo(sat_ecf_position,sat_ecf_velocity,station_longitude, station_latitude,stn_ecf_position)[2]
        
        #Look Angles of Station - Az, El 
        Az = pgate.range_topo2look_angles(range_topo_position,range_topo_velocity,RangeVecSat)[0]
        El = pgate.range_topo2look_angles(range_topo_position,range_topo_velocity,RangeVecSat)[1]
        dAz = pgate.range_topo2look_angles(range_topo_position,range_topo_velocity,RangeVecSat)[2]
        dEl = pgate.range_topo2look_angles(range_topo_position,range_topo_velocity,RangeVecSat)[3]
        
        if StnEL_min<El<StnEL_max:
            AOS = time
            LOS = 9999
        else: 
            LOS = time
            AOS = 9999
        yield Az, El, dAz, dEl, AOS, LOS
            
           
## #ECI POS, VEL, PERIGEE, RAAN, THETA
def ECI(time):
    for i in range(N):
        ts_sat_epoch = Satellites[i].refepoch
        M0_mean_anomaly = Satellites[i].meanan
        n_mean_motion = Satellites[i].meanmo
        n_dot_mean_motion = Satellites[i].ndot
        n_2dots_mean_motion = Satellites[i].nddot6
        eccentricity = Satellites[i].eccn
        omega_longitude_ascending_node = Satellites[i].raan
        omega_argument_periapsis = Satellites[i].argper
        inclination = Satellites[i].incl
        
        #Sequential initialization of orbital parameters required.
        
        #GMST, Mean Anomaly, Mean Anomaly Motion, Eccentric Anomaly 
        Mt_mean_anomaly = pgate.mean_anomaly_motion(time,ts_sat_epoch,M0_mean_anomaly,n_mean_motion,n_dot_mean_motion,n_2dots_mean_motion)[0]
        nt_mean_motion = pgate.mean_anomaly_motion(time,ts_sat_epoch,M0_mean_anomaly,n_mean_motion,n_dot_mean_motion,n_2dots_mean_motion)[1]
        ecc_anomaly = pgate.KeplerEqn(Mt_mean_anomaly,eccentricity)
        
        #ECI POS, VEL, RAAN, PERIGEE, THETA [2, 3, 4]
        eci_position = pgate.sat_ECI(eccentricity,ecc_anomaly,omega_longitude_ascending_node,
                omega_argument_periapsis,inclination,nt_mean_motion,ts_sat_epoch,time)[0]
        eci_velocity = pgate.sat_ECI(eccentricity,ecc_anomaly,omega_longitude_ascending_node,
                omega_argument_periapsis,inclination,nt_mean_motion,ts_sat_epoch,time)[1]
        Perigee = pgate.sat_ECI(eccentricity,ecc_anomaly,omega_longitude_ascending_node,
                omega_argument_periapsis,inclination,nt_mean_motion,ts_sat_epoch,time)[3]
        RAAN = pgate.sat_ECI(eccentricity,ecc_anomaly,omega_longitude_ascending_node,
                omega_argument_periapsis,inclination,nt_mean_motion,ts_sat_epoch,time)[2]
        Theta = pgate.sat_ECI(eccentricity,ecc_anomaly,omega_longitude_ascending_node,
                omega_argument_periapsis,inclination,nt_mean_motion,ts_sat_epoch,time)[4]
        yield eci_position, eci_velocity, Perigee, RAAN, Theta
        
## ECF        
def ECF(time):
    for i in range(N):
        ts_sat_epoch = Satellites[i].refepoch
        M0_mean_anomaly = Satellites[i].meanan
        n_mean_motion = Satellites[i].meanmo
        n_dot_mean_motion = Satellites[i].ndot
        n_2dots_mean_motion = Satellites[i].nddot6
        eccentricity = Satellites[i].eccn
        omega_longitude_ascending_node = Satellites[i].raan
        omega_argument_periapsis = Satellites[i].argper
        inclination = Satellites[i].incl
        #Sequential initialization of orbital parameters required.
        
        #GMST, Mean Anomaly, Mean Anomaly Motion, Eccentric Anomaly 
        Mt_mean_anomaly = pgate.mean_anomaly_motion(time,ts_sat_epoch,M0_mean_anomaly,n_mean_motion,n_dot_mean_motion,n_2dots_mean_motion)[0]
        nt_mean_motion = pgate.mean_anomaly_motion(time,ts_sat_epoch,M0_mean_anomaly,n_mean_motion,n_dot_mean_motion,n_2dots_mean_motion)[1]
        GMST = pgate.THETAJ(time)
        ecc_anomaly = pgate.KeplerEqn(Mt_mean_anomaly,eccentricity)
        
        #ECI POS, VEL, RAAN, PERIGEE, THETA [2, 3, 4]
        eci_position = pgate.sat_ECI(eccentricity,ecc_anomaly,omega_longitude_ascending_node,
                omega_argument_periapsis,inclination,nt_mean_motion,ts_sat_epoch,time)[0]
        eci_velocity = pgate.sat_ECI(eccentricity,ecc_anomaly,omega_longitude_ascending_node,
                omega_argument_periapsis,inclination,nt_mean_motion,ts_sat_epoch,time)[1]
        
        #ECF POS, VEL
        sat_ecf_position = pgate.sat_ECF(time,eci_position,eci_velocity,GMST)[0]
        sat_ecf_velocity = pgate.sat_ECF(time,eci_position,eci_velocity,GMST)[1]

        yield sat_ecf_position, sat_ecf_velocity 

    

## Topocentric 
def TOPO(time):
    for i in range(N):
        ts_sat_epoch = Satellites[i].refepoch
        M0_mean_anomaly = Satellites[i].meanan
        n_mean_motion = Satellites[i].meanmo
        n_dot_mean_motion = Satellites[i].ndot
        n_2dots_mean_motion = Satellites[i].nddot6
        eccentricity = Satellites[i].eccn
        omega_longitude_ascending_node = Satellites[i].raan
        omega_argument_periapsis = Satellites[i].argper
        inclination = Satellites[i].incl
        
        #Sequential initialization of orbital parameters required.
        
        #GMST, Mean Anomaly, Mean Anomaly Motion, Eccentric Anomaly 
        Mt_mean_anomaly = pgate.mean_anomaly_motion(time,ts_sat_epoch,M0_mean_anomaly,n_mean_motion,n_dot_mean_motion,n_2dots_mean_motion)[0]
        nt_mean_motion = pgate.mean_anomaly_motion(time,ts_sat_epoch,M0_mean_anomaly,n_mean_motion,n_dot_mean_motion,n_2dots_mean_motion)[1]
        GMST = pgate.THETAJ(time)
        ecc_anomaly = pgate.KeplerEqn(Mt_mean_anomaly,eccentricity)
        
        #ECI POS, VEL, RAAN, PERIGEE, THETA [2, 3, 4]
        eci_position = pgate.sat_ECI(eccentricity,ecc_anomaly,omega_longitude_ascending_node,
                omega_argument_periapsis,inclination,nt_mean_motion,ts_sat_epoch,time)[0]
        eci_velocity = pgate.sat_ECI(eccentricity,ecc_anomaly,omega_longitude_ascending_node,
                omega_argument_periapsis,inclination,nt_mean_motion,ts_sat_epoch,time)[1]
        
        #ECF POS, VEL
        sat_ecf_position = pgate.sat_ECF(time,eci_position,eci_velocity,GMST)[0]
        sat_ecf_velocity = pgate.sat_ECF(time,eci_position,eci_velocity,GMST)[1]
        
        #Topocentric Position and Velocity 
        range_topo_position = pgate.range_ECF2topo(sat_ecf_position,sat_ecf_velocity,station_longitude,station_latitude,stn_ecf_position)[0]
        range_topo_velocity = pgate.range_ECF2topo(sat_ecf_position,sat_ecf_velocity,station_longitude,station_latitude,stn_ecf_position)[1]
        RangeVecSat = pgate.range_ECF2topo(sat_ecf_position,sat_ecf_velocity,station_longitude, station_latitude,stn_ecf_position)[2]
        range_scalar = pgate.range_ECF2topo(sat_ecf_position,sat_ecf_velocity,station_longitude, station_latitude,stn_ecf_position)[3]
        range_rate = pgate.range_ECF2topo(sat_ecf_position,sat_ecf_velocity,station_longitude, station_latitude,stn_ecf_position)[4]
        Doppler = pgate.range_ECF2topo(sat_ecf_position,sat_ecf_velocity,station_longitude, station_latitude,stn_ecf_position)[5]
        RcedPower = pgate.range_ECF2topo(sat_ecf_position,sat_ecf_velocity,station_longitude, station_latitude,stn_ecf_position)[6]

        
        yield range_topo_position, range_topo_velocity, RangeVecSat, range_scalar, range_rate, Doppler, RcedPower
        
      
## Debugging [Mt_mean, nt_mean, GMST, ecc_anomaly]
def DebugElements(time):
    for i in range(N):
        ts_sat_epoch = Satellites[i].refepoch
        M0_mean_anomaly = Satellites[i].meanan
        n_mean_motion = Satellites[i].meanmo
        n_dot_mean_motion = Satellites[i].ndot
        n_2dots_mean_motion = Satellites[i].nddot6
        eccentricity = Satellites[i].eccn
        Mt_mean_anomaly = pgate.mean_anomaly_motion(time,ts_sat_epoch,M0_mean_anomaly,n_mean_motion,n_dot_mean_motion,n_2dots_mean_motion)[0]
        nt_mean_motion = pgate.mean_anomaly_motion(time,ts_sat_epoch,M0_mean_anomaly,n_mean_motion,n_dot_mean_motion,n_2dots_mean_motion)[1]
        GMST = pgate.THETAJ(time)
        ecc_anomaly = pgate.KeplerEqn(Mt_mean_anomaly,eccentricity)
        yield Mt_mean_anomaly, nt_mean_motion, GMST, ecc_anomaly

def SatName():
    for i in range(N):
        Name = Satellites[i].name
        yield Name
      
def SatEpoch():
   for i in range(N):
       ts_sat_epoch = Satellites[i].refepoch
       ts_sat_epoch_UTC = Datefun.dtep(ts_sat_epoch)
       yield ts_sat_epoch, ts_sat_epoch_UTC

def FileNames(Coord,N, StepSize):
    SatName1 = list(SatName())
    i = int(((tend-tstart).total_seconds())/StepSize)+1; 
    for i in range (N):
         FileName = (SatName1[i]+"_"+Coord).replace(" ","_") #Setting FileName for Saving
         yield FileName














#     StepSize = 60
#     N = 1; 
#     tstart = Parse.tracking()[0]; tstart0 = tstart
#     tend = Parse.tracking()[1]
#     FileName = 'AOS_LOS'
#     i = int(((tend-tstart).total_seconds())/StepSize); 
#     #Ephem = open(f'{FileName}.txt',"a")
#     #Ephem.write('SAT No.\t Name\t\t AOS\t\t LOS\t\t Min. Expected Level')
#     for N in range (N):
#         tstart = tstart0
#         for i in range (i+1):
#             Epoch = (tstart-tstart0).total_seconds()
#             Result = list(LookAngles(tstart))  
#             El = (Result[0][1])
#             El = float(El)
#             if StnEL_min<El<StnEL_max:
#                 AOS1 = tstart 
#             else: 
#                 LOS1 = tstart 
          
            
#             yield AOS1, LOS1








# ##Return TLE Parameters for Debugging

# for i in range(N):
#       Name = Satellites[i].name
#       ts_sat_epoch = Satellites[i].refepoch
#       M0_mean_anomaly = Satellites[i].meanan
#       n_mean_motion = Satellites[i].meanmo
#       n_dot_mean_motion = Satellites[i].ndot
#       n_2dots_mean_motion = Satellites[i].nddot6
#       eccentricity = Satellites[i].eccn
#       omega_longitude_ascending_node = Satellites[i].raan
#       omega_argument_periapsis = Satellites[i].argper
#       inclination = Satellites[i].incl
      


#Initiialize times
# ts_sat_epoch = refepoch #Some fct call one or the other, idk which.
# ts_sat_epochObj = Datefun.dtep(refepoch)
# tt = tstart-refepoch
# t1 = tt.days*(24*3600)+tt.seconds #tracking interval start time in (s) after TLE 'snaptime' epoch.
# #Will propagate forward starting at time t1
# ttend = tend-refepoch
# t2 = ttend.days*(24*3600)+ttend.seconds
# tmid = tstart.replace(hour=0,minute=0,second=0)
## See readme^^

# Coord = 'ECF' #ECI or ECF or TOPO or Elements in Quotes Please
# timeStart = dt.datetime(2020,9,22,0,0)
# timeEnd = dt.datetime(2020,9,22,10,0,0)
# StepSize = 60*5
