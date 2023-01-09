import math
import math as m
import datetime as dt 
import numpy as np 
import Datefun
from scipy.spatial.transform import Rotation as R

def THETAN1(TimeOfGMST):
    #Converting TLE to Python Datetime Obj by calling dtep from Datefun
    Tstart = TimeOfGMST;
    #Tmid, Epoch J2000
    Tmid = dt.datetime(Tstart.year,Tstart.month,Tstart.day,0,0,0)
    EpochJ2000 = dt.datetime(2000,1,1,12,0,0)
    
   #Calculation Du, Tu Parameters 
    Du = (Tmid-EpochJ2000+dt.timedelta(hours = 12)).days
    Tu = Du/36525
    
    #This is in unit of degrees
    GMST0 = 99.9677947 + 36000.77006361*Tu + 0.00038793*Tu**2 -2.6e-8*Tu**3
    
    #Non-uniform relations between Solar time and Sidereal Time #rev/day
    #Dividing by 240 converts rev/per day to degrees per seconds
    r = (1.002737909350795 + 5.9006e-11*Tu-5.9e-15*Tu**2)/240 
    
    #Calculating Interval of elapsed seconds from Tstart and Tmid 
    Intval = (Tstart-Tmid).total_seconds()
    
    #Calculating GMST at Tstart
    GMST = (GMST0 + r*Intval)%360
   
    return GMST      

  
def THETAN(refepoch):
    #Converting TLE to Python Datetime Obj by calling dtep from Datefun
    Tstart = Datefun.dtep(refepoch)
        
    #Tmid, Epoch J2000
    Tmid = dt.datetime(Tstart.year,Tstart.month,Tstart.day,0,0,0)
    EpochJ2000 = dt.datetime(2000,1,1,12,0,0)
    
   #Calculation Du, Tu Parameters 
    Du = (Tmid-EpochJ2000+dt.timedelta(hours = 12)).days
    Tu = Du/36525
    
    #This is in unit of degrees
    GMST0 = 99.9677947 + 36000.77006361*Tu + 0.00038793*Tu**2 -2.6e-8*Tu**3
    
    #Non-uniform relations between Solar time and Sidereal Time #rev/day
    #Dividing by 240 converts rev/per day to degrees per seconds
    r = (1.002737909350795 + 5.9006e-11*Tu-5.9e-15*Tu**2)/240 
    
    #Calculating Interval of elapsed seconds from Tstart and Tmid 
    Intval = (Tstart-Tmid).total_seconds()
    
    #Calculating GMST at Tstart
    GMST = (GMST0 + r*Intval)%360
   
    return GMST

def THETAJ(time):
    
    #Assigning Tstart, Tmid, Epoch J2000
    Tstart = time
    Tmid = dt.datetime(Tstart.year,Tstart.month,Tstart.day,0,0,0)
    EpochJ2000 = dt.datetime(2000,1,1,12,0,0)
    
    #Calculation Du, Tu Parameters 
    Du = (Tmid-EpochJ2000+dt.timedelta(hours = 12)).days
    Tu = Du/36525
    
    #This is in unit of degrees and GMST at 0h
    GMST0 = 99.9677947 + 36000.77006361*Tu + 0.00038793*Tu**2 -2.6e-8*Tu**3
    
    #Non-uniform relations between Solar time and Sidereal Time #rev/day
    #Dividing by 240 converts rev/per day to degrees per seconds
    r = (1.002737909350795 + 5.9006e-11*Tu-5.9e-15*Tu**2)/240 
    
    #Calculating Interval of elapsed seconds from Tstart and Tmid 
    Intval = (Tstart-Tmid).total_seconds()
    
    #Calculating GMST at Tstart and converting to radians
    GMSTrad = math.radians((GMST0 + r*Intval)%360)
   
    return GMSTrad 

def mean_anomaly_motion(time,ts_sat_epoch,M0_mean_anomaly,n_mean_motion,n_dot_mean_motion,n_2dots_mean_motion):
    time = (time-Datefun.dtep(ts_sat_epoch)).total_seconds()
    
    #Calculating Mean Anomaly at time 
    Mt_mean_anomaly = M0_mean_anomaly + n_mean_motion*((360*time)/(86400)) \
    + 360*(n_dot_mean_motion)*((time/86400))**2 + 360*(n_2dots_mean_motion)*(((time)/86400))**3
    Mt_mean_anomaly = Mt_mean_anomaly%360
    
    #Calculating mean motion at time 
    nt_mean_motion = n_mean_motion*(360/86400)+2*(360)*(n_dot_mean_motion)*((time/(86400**2))) \
    + 3*(360)*(n_2dots_mean_motion)*((time**2)/(86400**3))
    
    nt_mean_motion = nt_mean_motion*240
    
    return Mt_mean_anomaly, nt_mean_motion

def KeplerEqn(MT_mean_anomaly,eccentricity):
    MT_mean_anomaly = m.radians(MT_mean_anomaly) #Converting to radians 
    Eo = MT_mean_anomaly #Setting Initial Condition 
    deltaE = 10 #Placeholder Delta so program enteres first Itt. of loop
    for x in range(10000):
        deltaM = Eo-eccentricity*m.sin(Eo)-MT_mean_anomaly #Newton's Raphson Method
        deltaE  = deltaM/(1-eccentricity*m.cos(Eo))
        E = Eo - deltaE
        Eo = E #Setting Last to Current for loop
        if deltaE<1e-9: #Breaking out of loop tolerance is met
            E = m.degrees(E)
            return E
        x = x+1
        

def sat_ECI(eccentricity,ecc_anomaly,omega_longitude_ascending_node,
            omega_argument_periapsis,inclination,nt_mean_motion,ts_sat_epoch,time):
    
    #Setting Coefficients
    J2 = 1.081874e-3
    Mu = 398600.4418
    Re = 6378.135
    
    #Calculating Semi Major Axis at t 
    a_semi_major_axis = (Mu**(1/3))/(((2*np.pi*nt_mean_motion)/(86400))**(2/3)) 
    
    #True Anomaly at t *atan2
    Theta = (2*(math.atan(math.sqrt((1+eccentricity)/(1-eccentricity))*(math.tan(math.radians(ecc_anomaly/2))))))
    Theta = Theta%(math.pi*2)
    
    #Perifocal Position Vector 
    r = (a_semi_major_axis*(1-eccentricity**2))/(1+eccentricity*math.cos(((Theta))))
    rpx = r*math.cos(Theta)
    rpy = r*math.sin(Theta)
    rpz = 0
    rPr = (np.array([rpx, rpy, rpz]))
    
    #Calculating Current Raan with J2
    #po = a_semi_major_axis*(1-eccentricity**2)
    ts_sat_epochObj = Datefun.dtep(ts_sat_epoch)
    
    #Omega Bug is here
    #omegaDot = (-3/2)*J2*((a_semi_major_axis**2)/(po**2))*nt_mean_motion*math.cos(math.radians(inclination))
    #omegaDot = (-3/2)*((J2*Re**2*math.cos(math.radians(inclination)))/(2*a_semi_major_axis**2*(1-eccentricity**2)**2))*nt_mean_motion
    #omega = omega_longitude_ascending_node + omegaDot*((time-ts_sat_epochObj).total_seconds())
    omega = omega_longitude_ascending_node
    
    #Calculate Current Arg of Perigee with J2
    #perDot = (3/4)*J2*((Re**2*(5*(math.cos(math.radians(inclination))**2)-1))/(2*a_semi_major_axis**2*(1-eccentricity**2)**2))*nt_mean_motion  
    #perDot = (3/4)*J2*(Re**2/po**2)*nt_mean_motion*math.cos(math.radians(inclination))
    perigee = omega_argument_periapsis
    #perigee = omega_argument_periapsis + perDot*((time-ts_sat_epochObj).total_seconds())
    
    
    #Perifocal Velocity Vector 
    h = math.sqrt(Mu*(r+r*eccentricity*(math.cos(Theta)))) 
    vpx = -(Mu/h)*math.sin(Theta)
    vpy = (Mu/h)*(eccentricity+ math.cos(Theta))
    vpz = 0
    vPr = np.array([vpx, vpy, vpz])
    
    #Rotating to ECI Frame 
    Rot1 = R.from_euler('zxz',[perigee, inclination, omega], degrees = True).as_matrix()
    eci_position = np.matmul(Rot1,rPr)
    eci_velocity = np.matmul(Rot1,vPr)
    
    return eci_position, eci_velocity, omega, perigee, Theta

def sat_ECF(time,eci_position, eci_velocity,GMST):
    Tei = np.array([m.cos(GMST), m.sin(GMST), 0, -m.sin(GMST), m.cos(GMST), 0, 0, 0, 1]).reshape(3,3)
    sat_ecf_position = np.matmul(Tei,eci_position)  
    #sat_ecf_velocity_inertial = np.matmul(Tei,eci_velocity)
    GMSTK = m.radians(360/86164.091)     
    OmegaDot = np.array([0, -GMSTK, 0, GMSTK, 0, 0, 0, 0, 0]).reshape(3,3)
    SndTerm = eci_velocity - np.matmul(OmegaDot,eci_position)
    sat_ecf_velocity_relative = np.matmul(Tei,SndTerm)
    sat_ecf_velocity = sat_ecf_velocity_relative
    return sat_ecf_position, sat_ecf_velocity

#This is good
def station_ECF(station_longitude, station_latitude, station_elevation):
    f = 1/298.25223563
    Re = 6378.135
    e = math.sqrt(2*f-f**2)
    Ne = Re/(math.sqrt(1-e**2*(math.sin(math.radians(station_latitude))**2)))
    stn_ecf_x = (Ne+station_elevation)*math.cos(math.radians(station_latitude))*math.cos(math.radians(station_longitude))
    stn_ecf_y = (Ne+station_elevation)*math.cos(math.radians(station_latitude))*math.sin(math.radians(station_longitude))
    stn_ecf_z = ((1-e**2)*Ne+station_elevation)*math.sin(math.radians(station_latitude))
    stn_ecf_position = np.array([stn_ecf_x,stn_ecf_y,stn_ecf_z])
    return stn_ecf_position


#Topo Velcoity matches with Sign Flip
def range_ECF2topo(sat_ecf_position,sat_ecf_velocity,station_longitude, station_latitude,stn_ecf_position):
    RangeVecSat = sat_ecf_position-stn_ecf_position 
    Tx = [-math.sin(math.radians(station_longitude)),math.cos(math.radians(station_longitude)),0]
    Ty = [-math.cos(math.radians(station_longitude))*math.sin(math.radians(station_latitude)),-math.sin(math.radians(station_longitude))*math.sin(math.radians(station_latitude)),math.cos(math.radians(station_latitude))]
    Tz = [math.cos(math.radians(station_longitude))*math.cos(math.radians(station_latitude)),math.sin(math.radians(station_longitude))*math.cos(math.radians(station_latitude)),math.sin(math.radians(station_latitude))]
    T = np.array([Tx,Ty,Tz]) 
    

    range_topo_position = np.matmul(T,RangeVecSat) #Range in topo
    range_topo_velocity = np.matmul(T,sat_ecf_velocity) #Range rate in topo
    Range = range_topo_position
    #Range Equations    
    range_scalar = np.linalg.norm(Range)
    range_rate = (np.dot(range_topo_velocity, range_topo_position))/range_scalar
    #Calculating Doppler 
    ft = 1575.42e6; 
    Doppler = ((-range_rate)/(3e8))*ft*10**-3
    #Calculating Effective Isotropic Power (Min)
    n = 0.5; D = 46 #Link Inputs
    
    Gr = 0; #FROM STK  
    range_scalerM = range_scalar*10**3;
    Ls = 20*np.log10(((3e8/(4*np.pi*range_scalerM*ft))))

    Pt = 41.3988; #FROM STK 
    Gt = 13.5; #FROM STK 
    EIRP =  Pt - Gt; #From STK 
    Gs = 0; #From STK 
    RcedPower = EIRP+Ls
    return range_topo_position, range_topo_velocity, RangeVecSat, range_scalar, range_rate, Doppler,RcedPower

    
#Using atan2... 
def range_topo2look_angles(range_topo_position, range_topo_velocity,RangeVecSat):
    
    #Calculating Az and El Look Angles
    AZ = math.degrees(math.atan2(range_topo_position[0],range_topo_position[1]))
    AZ = AZ%360
    EL = math.degrees(math.atan2(range_topo_position[2],(math.sqrt(range_topo_position[0]**2+range_topo_position[1]**2))))
    
    
    
    ## Future if-statement to see if EL>ELmin. ELmin from station class (Fio)

    #Calculating Derivative El, Az
    Rxy = range_topo_position[0:2]; 
    Vxy = range_topo_velocity[0:2]
    NormRxy = np.linalg.norm(Rxy); NormRange = np.linalg.norm(range_topo_position)
    dAZ = math.degrees((1/(NormRxy)**2)*np.cross(Vxy,Rxy))
    dEL = math.degrees((1/(NormRange)**2)*((NormRxy*range_topo_velocity[2]-((range_topo_position[2]/(NormRxy))*np.dot(Rxy,Vxy)))))

    return AZ, EL, dAZ, dEL


#Just needs that if statement fix...angles seem to match STK already

# def range_topo2look_angles(range_topo_position, range_topo_velocity,RangeVecSat):
#     xy = (range_topo_position[0])/(range_topo_position[1])
#     AZ = math.degrees(math.atan(xy))
#     AZ = AZ%360
#     if (270 <= AZ <= 360) and (xy <= 0):
#         AZ = math.degrees(np.arctan2(range_topo_position[0],range_topo_position[1]))
#         AZ = AZ%360
#     elif (270 <= AZ <= 360) and (xy >= 0):
#         AZ = math.degrees(np.arctan2(range_topo_position[1],range_topo_position[0]))-180
#         AZ = AZ%360

#     # Future if-statement to see if EL>ELmin. ELmin from station class (Fio)--> in high lvl fct?
#     Rxy = np.array([range_topo_position[0],range_topo_position[1]])
#     EL = math.degrees(math.atan(range_topo_position[2]/(Vec.magntd(Rxy,0))))
#     EL = EL%360
#     Vxy = np.array([range_topo_velocity[0],range_topo_velocity[1]])
#     dAZ = Vec.mycross(Vxy,Rxy,0)/(Vec.magntd(Rxy,0)**2)
#     dEL = ((Vec.magntd(Rxy,0))*range_topo_velocity[2]-((range_topo_position[2])*(np.dot(Rxy,Vxy)))/(Vec.magntd(Rxy,0)))/(Vec.magntd(RangeVecSat,0))
#     return AZ, EL, dAZ, dEL, range_topo_position

