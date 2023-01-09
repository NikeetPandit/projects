import numpy as np
import datetime as dt   

#Example Formatting For Tracking Input
#2021-01-01-17:00:00 
#2021-01-01-17:00:00


#Example Formatting For Station Coordinates
#ARO parameters:
#latitide 45d57'19.812"N
#longitude 281d55'37.055"E
#elevation 260.42m
#diameter = 46m solid and mesh parts (36.6m solid part)
#focal ratio = 0.4(0.5 solid)
#focal length = 18.3 m prime
#surface accuracy 0.32 cm (solid), 0.64 cm (mesh)
#beamwidth = 3 arcmin (10 GHz)
#AZ speed max = 10 deg/min
#EL speed max = 10 deg/min,
#EL_min limit > 9, EL_max < 89



## PARSE MODULE
    ## Parse tracking interval
def tracking():
    data0 = open(r'Inputs\TrackingInterval.txt')
    Interval = np.array(data0.read().replace('-',' ').split('\n'))
    t_start = Interval[0].replace(':',' ').split('\n')[0].split()
    t_end = Interval[1].replace(':',' ').split('\n')[0].split()
    tstart = dt.datetime(int(t_start[0]),int(t_start[1]),int(t_start[2]),int(t_start[3]),int(t_start[4]),int(t_start[5]))
    tend = dt.datetime(int(t_end[0]),int(t_end[1]),int(t_end[2]),int(t_end[3]),int(t_end[4]),int(t_end[5]))
    return tstart, tend 

    ## Parse Station Parameters
def StationParam():
    data1 = open('Inputs\ARO_COORD.txt') #Mock ARO station file, opened as a txt file of length 1
    STNFIL = np.array(data1.read().replace(',','').split('\n'))
    return STNFIL

     ## Parse TLE Parameters
def TLEParam():
    data2 = open(r'Inputs\gnss_TLE.txt') #Can bring in any size TLE
    TLE = np.array((data2.read().split('\n'))) #creates list with seperation by newline from textfile above
    TLE = [x for x in TLE if x]
    
    return TLE