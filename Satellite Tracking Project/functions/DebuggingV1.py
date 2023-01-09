import datetime as dt 
import Datefun 
import HighLevel_v2 as HL
import Parse
import math 
import numpy as np
import os
import pathlib 



#Coord is Either ECI, ELEMENTS, ECF, TOPO
#Elements Returns: Perigee, Raan, True Anom, Meam Anomaly, Mean Anomaly Motion
#GMST Angle, and Eccentric Annomaly for Debugging Purposes...

#Call in Main Function 


def STKout(Coord,StepSize,N):
    print('Files Printing To Working Directory')
    tstart = Parse.tracking()[0]; tstartStr = Datefun.dt2dat(tstart)
    tstart0 = tstart
    tend = Parse.tracking()[1]
    Filename = list(HL.FileNames(Coord, N, StepSize))
 
    i = int(((tend-tstart).total_seconds())/StepSize); 
    NumOfPoint = str(i)  #Number of Ephem Points
    
    if Coord == 'ECI':
        Coord1 = 'J2000'
    elif Coord == 'ECF':
        Coord1 = 'Fixed' 
    elif Coord == 'TOPO':
        Coord1 = 'Custom Topocentric_ARO'
    elif Coord == 'ELEMENTS':
        Coord1 = ' My Custom Element Debugging Report'
    
    for N in range (N):
        tstart = tstart0
        Ephem = open(f'{Filename[N]}.e',"a")
        Ephem.write('stk.v.12.0\n\n\n\n')
        Ephem.write('BEGIN Ephemeris\n\n')
        Ephem.write('\tNumberOfEphemerisPoints\t\t'+NumOfPoint)
        Ephem.write('\n\n\tScenarioEpoch\t\t\t'+tstartStr)
        Ephem.write('\n\n\n\tInterpolationMethod		 Lagrange\n\n')
        Ephem.write('\tInterpolationSamplesM1		 1')
        Ephem.write('\n\n\tCentralBody		 Earth')
        Ephem.write('\n\n\tCoordinateSystem		 '+Coord1)
        
        if Coord == 'ECF':
            Ephem.write('\n\n\n\n\tEphemerisTimePosVel\n\n')
            for i in range (i+1):
                Epoch = (tstart-tstart0).total_seconds()
                Result = list(HL.ECF(tstart))    
                Pos = str(Result[N][0]*1000); Vel = str(Result[N][1]*1000); Epoch = str(Epoch)
                Pos = Pos.replace("["," "); Pos = Pos.replace("]"," ")
                Vel = Vel.replace("["," "); Vel = Vel.replace("]"," ")
                Ephem.write(Epoch + '\t' + Pos + '\t' + Vel + '\n')
                Looptime = tstart +dt.timedelta(seconds = StepSize)
                tstart = Looptime
                
               
            Ephem.write('\n\nEND Ephemeris')
            Ephem.close()
            
            
        elif Coord == 'ECI':
           Ephem.write('\n\n\n\n\tEphemerisTimePosVel\n\n')
           for i in range (i+1):
               Epoch = (tstart-tstart0).total_seconds()
               Result = list(HL.ECI(tstart))    
               Pos = str(Result[N][0]*1000); Vel = str(Result[N][1]*1000); Epoch = str(Epoch)
               Pos = Pos.replace("["," "); Pos = Pos.replace("]"," ")
               Vel = Vel.replace("["," "); Vel = Vel.replace("]"," ")
               Ephem.write(Epoch + '\t' + Pos + '\t' + Vel + '\n')
               Looptime = tstart +dt.timedelta(seconds = StepSize)
               tstart = Looptime
               
              
           Ephem.write('\n\nEND Ephemeris')
           Ephem.close()     
               
        elif Coord == 'TOPO':
            Ephem.write('\n\n\n\n\tEphemerisTimePosVel\n\n')
            for i in range (i+1):
                Epoch = (tstart-tstart0).total_seconds()
                Result = list(HL.TOPO(tstart))    
                Pos = str(Result[N][0]*1000); Vel = str(Result[N][1]*1000); Epoch = str(Epoch)
                Pos = Pos.replace("["," "); Pos = Pos.replace("]"," ")
                Vel = Vel.replace("["," "); Vel = Vel.replace("]"," ")
                Ephem.write(Epoch + '\t' + Pos + '\t' + Vel + '\n')
    
                Looptime = tstart +dt.timedelta(seconds = StepSize)
                tstart = Looptime
                
               
            Ephem.write('\n\nEND Ephemeris')
            Ephem.close()         
            
        elif Coord == 'ELEMENTS':
            Ephem.write('\n\n\n\nTime\t\tPERIGEE\t\t RAAN\t\tTRUE ANOMALY\t\tMean Anomaly\t\tMean Motion\tGMST\tECC Anomaly\n\n')
            for i in range (i+1):
                Epoch = (tstart-tstart0).total_seconds()
                Result = list(HL.ECI(tstart))   
                Result1 = list(HL.DebugElements(tstart))
                
                PERIGEE = str(Result[N][2]); RAAN = str(Result[N][3]);
                THETA =str(math.degrees(Result[N][4])); Epoch = str(Epoch)
                Mt_mean = str(Result1[N][0]); nt_mean = str(Result1[N][1]);
                GMST = str(Result1[N][2]); ecc_anomaly = str(Result1[N][3]);
                
                Ephem.write(Epoch + '\t\t' + PERIGEE+ '\t\t' + RAAN + '\t\t' + THETA + '\t\t'+ Mt_mean + '\t\t' + nt_mean + '\t\t'+ GMST + '\t\t'+ ecc_anomaly+'\n')
                Looptime = tstart +dt.timedelta(seconds = StepSize)
                tstart = Looptime
                
               
            Ephem.write('\n\nEND Ephemeris')
            Ephem.close()              
 
def STKoutIndx(Coord,StepSize,N,Index):
    print('Files Printing To Working Directory')
    tstart = Parse.tracking()[0]; tstartStr = Datefun.dt2dat(tstart)
    tstart0 = tstart
    tend = Parse.tracking()[1]
    Filename = list(HL.FileNames(Coord, N, StepSize))
 
    i = int(((tend-tstart).total_seconds())/StepSize); 
    NumOfPoint = str(i)  #Number of Ephem Points
    N = Index
    if Coord == 'ECI':
        Coord1 = 'J2000'
    elif Coord == 'ECF':
        Coord1 = 'Fixed' 
    elif Coord == 'TOPO':
        Coord1 = 'Custom Topocentric_ARO'
    elif Coord == 'ELEMENTS':
        Coord1 = ' My Custom Element Debugging Report'
    
    tstart = tstart0
    Ephem = open(f'{Filename[Index]}.e',"a")
    Ephem.write('stk.v.12.0\n\n\n\n')
    Ephem.write('BEGIN Ephemeris\n\n')
    Ephem.write('\tNumberOfEphemerisPoints\t\t'+NumOfPoint)
    Ephem.write('\n\n\tScenarioEpoch\t\t\t'+tstartStr)
    Ephem.write('\n\n\n\tInterpolationMethod		 Lagrange\n\n')
    Ephem.write('\tInterpolationSamplesM1		 1')
    Ephem.write('\n\n\tCentralBody		 Earth')
    Ephem.write('\n\n\tCoordinateSystem		 '+Coord1)

    if Coord == 'ECF':
        Ephem.write('\n\n\n\n\tEphemerisTimePosVel\n\n')
        for i in range (i+1):
            Epoch = (tstart-tstart0).total_seconds()
            Result = list(HL.ECF(tstart))    
            Pos = str(Result[Index][0]*1000); Vel = str(Result[Index][1]*1000); Epoch = str(Epoch)
            Pos = Pos.replace("["," "); Pos = Pos.replace("]"," ")
            Vel = Vel.replace("["," "); Vel = Vel.replace("]"," ")
            Ephem.write(Epoch + '\t' + Pos + '\t' + Vel + '\n')
            Looptime = tstart +dt.timedelta(seconds = StepSize)
            tstart = Looptime
            
           
        Ephem.write('\n\nEND Ephemeris')
        Ephem.close()
        
        
    elif Coord == 'ECI':
       Ephem.write('\n\n\n\n\tEphemerisTimePosVel\n\n')
       for i in range (i+1):
           Epoch = (tstart-tstart0).total_seconds()
           Result = list(HL.ECI(tstart))    
           Pos = str(Result[N][0]*1000); Vel = str(Result[N][1]*1000); Epoch = str(Epoch)
           Pos = Pos.replace("["," "); Pos = Pos.replace("]"," ")
           Vel = Vel.replace("["," "); Vel = Vel.replace("]"," ")
           Ephem.write(Epoch + '\t' + Pos + '\t' + Vel + '\n')
           Looptime = tstart +dt.timedelta(seconds = StepSize)
           tstart = Looptime
           
          
       Ephem.write('\n\nEND Ephemeris')
       Ephem.close()     
           
    elif Coord == 'TOPO':
        Ephem.write('\n\n\n\n\tEphemerisTimePosVel\n\n')
        for i in range (i+1):
            Epoch = (tstart-tstart0).total_seconds()
            Result = list(HL.TOPO(tstart))    
            Pos = str(Result[N][0]*1000); Vel = str(Result[N][1]*1000); Epoch = str(Epoch)
            Pos = Pos.replace("["," "); Pos = Pos.replace("]"," ")
            Vel = Vel.replace("["," "); Vel = Vel.replace("]"," ")
            Ephem.write(Epoch + '\t' + Pos + '\t' + Vel + '\n')

            Looptime = tstart +dt.timedelta(seconds = StepSize)
            tstart = Looptime
            
           
        Ephem.write('\n\nEND Ephemeris')
        Ephem.close()         
        
    elif Coord == 'ELEMENTS':
        Ephem.write('\n\n\n\nTime\t\tPERIGEE\t\t\t RAAN\t\t\tTRUE ANOMALY\t\t\tMean Anomaly\t\t\tMean Motion\t\t\t\tGMST\t\t\t\tECC Anomaly\n\n')
        for i in range (i+1):
            Epoch = (tstart-tstart0).total_seconds()
            Result = list(HL.ECI(tstart))   
            Result1 = list(HL.DebugElements(tstart))
            
            PERIGEE = str(Result[N][2]); RAAN = str(Result[N][3]);
            THETA =str(math.degrees(Result[N][4])); Epoch = str(Epoch)
            Mt_mean = str(Result1[N][0]); nt_mean = str(Result1[N][1]);
            GMST = str(Result1[N][2]); ecc_anomaly = str(Result1[N][3]);
            
            Ephem.write(Epoch + '\t\t' + PERIGEE+ '\t\t' + RAAN + '\t\t' + THETA + '\t\t'+ Mt_mean + '\t\t' + nt_mean + '\t\t'+ GMST + '\t\t'+ ecc_anomaly+'\n')
            Looptime = tstart +dt.timedelta(seconds = StepSize)
            tstart = Looptime
            
           
        Ephem.write('\n\nEND Ephemeris')
        Ephem.close()                           
             
def STKsp(StepSize,N):
    print('Files Printing To Working Directory')
    tstart = Parse.tracking()[0]; tstartStr = Datefun.dt2dat(tstart)
    tstart0 = tstart
    tend = Parse.tracking()[1]
    Coord = 'Point'
    Filename = list(HL.FileNames(Coord, N, StepSize))
    i = int(((tend-tstart).total_seconds())/StepSize);  NumOfPoint = str(i)
    for N in range (N):
        tstart = tstart0
        Ephem = open(f'{Filename[N]}.sp',"a")
        Ephem.write('stk.v.12.0\n\n\n\n')
        Ephem.write('Begin	Attitude	  ')
        Ephem.write('\nNumberofAttitudePoints\t'+NumOfPoint)
        Ephem.write('\n#ScenarioEpoch\t\t\t'+tstartStr)
        Ephem.write('\nSequence\t\t323')
        Ephem.write('\nAttitudeTimeAzElAngles		\n\n')
        for i in range (i+1):
                Epoch = (tstart-tstart0).total_seconds()
                Result = list(HL.LookAngles(tstart))   
                
                Az = str(Result[N][0]); El = str(Result[N][1]); Epoch = str(Epoch)
                Ephem.write(Epoch + '\t' + Az + '\t' + El + '\t' + '\n')
                Looptime = tstart +dt.timedelta(seconds = StepSize)
                tstart = Looptime
                
           
        Ephem.write('\n\nEnd Attitude')
        Ephem.close()        
 

def STKspIndx(StepSize,Index,N):
    print('Files Printing To Working Directory')
    tstart = Parse.tracking()[0]; tstartStr = Datefun.dt2dat(tstart)
    tstart0 = tstart
    tend = Parse.tracking()[1]
    Coord = 'Point'
    Filename = list(HL.FileNames(Coord, N, StepSize))
    i = int(((tend-tstart).total_seconds())/StepSize);  NumOfPoint = str(i)
    tstart = tstart0
    Ephem = open(f'{Filename[Index]}.sp',"a")
    Ephem.write('stk.v.12.0\n\n\n\n')
    Ephem.write('Begin	Attitude	  ')
    Ephem.write('\nNumberofAttitudePoints\t'+NumOfPoint)
    Ephem.write('\n#ScenarioEpoch\t\t\t'+tstartStr)
    Ephem.write('\nSequence\t\t323')
    Ephem.write('\nAttitudeTimeAzElAngles		\n\n')
    for i in range (i+1):
            Epoch = (tstart-tstart0).total_seconds()
            Result = list(HL.LookAngles(tstart))   
            
            Az = str(Result[Index][0]); El = str(Result[Index][1]); Epoch = str(Epoch)
            Ephem.write(Epoch + '\t' + Az + '\t' + El + '\t' + '\n')
            Looptime = tstart +dt.timedelta(seconds = StepSize)
            tstart = Looptime
            
           
    Ephem.write('\n\nEnd Attitude')
    Ephem.close()        
     

        
             
def AOSLOS(StepSize,N):
    print('Files Printing To Working Directory')
    tstart = Parse.tracking()[0]; tstart0 = tstart
    tend = Parse.tracking()[1]
    SatName = list(HL. SatName())
    FileName = 'AOS_LOS_Table'
    i = int(((tend-tstart).total_seconds())/StepSize); 
    Ephem = open(f'{FileName}.txt',"a")
    Ephem.write('SAT No.\tName\t\tAOS\t\t\tLOS\t\t\tMin. Expected Level [dB]\n')
    for N in range (N):
        LoopN = str(N)
        Ephem.write('\n' + LoopN + '\t' + SatName[N] + '\t')
        tstart = tstart0; cnt = 0; cnt1 = 0; cnt4 = 0; cnt5 = 0; 
        Power = np.zeros([1,i+1])
        for i in range (i+1):
            Result = list(HL.LookAngles(tstart)) 
            Result1 = list(HL.TOPO(tstart))
            Power[0,i]= ((np.sum(np.array((Result1[N][6])))))    
            AOS = Result[N][4]; LOS = Result[N][5] 
            if AOS == 9999: #NO SIGNAL
                cnt = cnt + 1;
            elif LOS == 9999: #YES SIGNAL
                cnt1 = cnt1 + 1
            
            if cnt == 1:
                cnt4 = 4
                LOStr = Datefun.dt2dat(LOS)

                if cnt1 == 0:
                    Ephem.write('\t\t\t' + LOStr + '(LOS)\n')
                    
                else: 
                    Ephem.write('\t' + LOStr + '(LOS)')
                                
                cnt1 = 0
                
            elif cnt1 == 1:
                cnt5 = 4;
                AOSStr = Datefun.dt2dat(AOS)
                if cnt == 0:
                    Ephem.write(AOSStr)
                else:
                    Ephem.write('\t\t'+AOSStr)
                cnt = 0
            if (cnt4+cnt5) == 8:
                cnt4 = 0; cnt5 = 0; 
            Looptime = tstart +dt.timedelta(seconds = StepSize)
            tstart = Looptime
        MinPower = str(round(np.min(Power),3))
        Ephem.write('\n')
        Ephem.write('\t\t\t\t\t\t\t\t\t'+ MinPower)
        Ephem.write('\n')
    Ephem.close()        

def AOSLOS1(StepSize,N):
    tstart = Parse.tracking()[0]; tstart0 = tstart
    tend = Parse.tracking()[1]
    SatName = list(HL. SatName())
    AOSStr = []; LOStr = []; 
    i = int(((tend-tstart).total_seconds())/StepSize); 
    print('SAT No.\tName\t\tAOS\t\t\tLOS\t\tMin. Expected Level [dB]\n')
    for N in range (N):
        j = 0;
        LoopN = str(N)
        tstart = tstart0; cnt = 0; cnt1 = 0; cnt4 = 0; cnt5 = 0; 
        Power = np.zeros([1,i+1])
        for i in range (i+1):
            Result = list(HL.LookAngles(tstart)) 
            Result1 = list(HL.TOPO(tstart))
            Power[0,i]= ((np.sum(np.array((Result1[N][6])))))    
            AOS = Result[N][4]; LOS = Result[N][5] 
            if AOS == 9999: #NO SIGNAL
                cnt = cnt + 1;
            elif LOS == 9999: #YES SIGNAL
                cnt1 = cnt1 + 1
            if cnt == 1:
                cnt4 = 4
                j = j+1;
                LOStr = Datefun.dt2dat(LOS)
                cnt1 = 0      
            elif cnt1 == 1:
                cnt5 = 4;      
                AOSStr = Datefun.dt2dat(AOS)
                cnt = 0
            if (cnt4+cnt5) == 8:
                cnt4 = 0; cnt5 = 0; 
            Looptime = tstart +dt.timedelta(seconds = StepSize)
            tstart = Looptime
        MinPower = str(round(np.min(Power),2))[::-1].zfill(7)[::-1]
        if AOSStr == []:
            Myspace = ' '
            AOSStr = Myspace*19;
        elif LOStr == []:
            Myspace = ' ';
            LOStr = Myspace*19;
        print('\n' + LoopN + '\t' + SatName[N] + '\t' + AOSStr + '\t' + LOStr + '\t\t' + MinPower)
        AOSStr = [];
        LOStr = [];
    #Ephem.close()        


def PrintSatName():
    Names = list(HL.SatName()); N = len(Names)
    #FileName = 'SatNameList'
    #Ephem = open(f'{FileName}.txt',"a")
    #Ephem.write('Choose Index of Satellite\n You wish to track Please\n\n')
    #Ephem.write('Index\tName')
    for i in range(N):
        istr = str(i)
        #Ephem.write(istr + '\t\t' + Names[i]+'\n')  
        print(istr + '\t\t' + Names[i])
        
    #Ephem.close()
    
def AROTrackData(StepSize,Index):
    tstart = Parse.tracking()[0]; 
    tstart0 = tstart
    tend = Parse.tracking()[1]
    STNName =  Parse.StationParam()[0]
    Coord = list(HL.SatName())[Index]
    print('Files Printing To Working Directory')
    print(Coord)
    Filename = 'AROTrackData_' + Coord
    Filename = Filename.replace(" ","_")
    i = int(((tend-tstart).total_seconds())/StepSize); 
    tstart = tstart0
    Ephem = open(f'{Filename}.ascii',"a")
    Ephem.write('#ARO Tracking Data by Nikeet Pandit and Diego Mateos\n')
    for i in range (i+1):
            Year = (tstart.year)
            Day = tstart.day
            Month = tstart.month
            DoY = Datefun.doy(Year,Month,Day)
            Hour = tstart.hour
            Minutes = tstart.minute
            Seconds = tstart.second
            Result = list(HL.LookAngles(tstart))   
            Yearz = str(Year); DoY = str(DoY).zfill(3); Hourz = str(Hour).zfill(2); 
            Min = str(Minutes).zfill(2); Secs = str(Seconds).zfill(2)
            Az = str(Result[Index][0]).zfill(3);  El = str(Result[Index][1]);
            dAz = str(Result[Index][2]); dEl = str(Result[Index][3])

            ## Converting Az to Degrees Minutes Seconds...
            Azdms = Datefun.deg2ms(float(Az)); AZd = str(int(Azdms[0])).zfill(3); 
            AZm = str(int(Azdms[1])).zfill(2); AZs = str(Azdms[2]).zfill(4);
            dAz = str(round(float(dAz),6))[::-1].zfill(9)[::-1]
            
            ## Converting El to Degrees Minutes Seconds 
            Eldms = Datefun.deg2ms(float(El)); Eld = str(int(Eldms[0])).zfill(2); 
            Elm = str(int(Eldms[1])).zfill(2); Els = str(Eldms[2]).zfill(4); 
            dEl = str(round(float(dEl),6))[::-1].zfill(9)[::-1]
            
            Ephem.write(Yearz+'.'+DoY+'.'+Hourz+':'+Min+':'+Secs+'  '+AZd+' '+AZm+' '+AZs+'  '+dAz+'  '+Eld+' '+Elm+'  '+Els+'  '+dEl+'\n')
            Looptime = tstart +dt.timedelta(seconds = StepSize)
            tstart = Looptime
    Ephem.write(str.rstrip('\n'))           
    Ephem.close()      
       

def TrackData(StepSize,Index):
    tstart = Parse.tracking()[0]; 
    tstart0 = tstart
    tend = Parse.tracking()[1]
    Coord = list(HL.SatName())[Index]
    print('Files Printing To Working Directory')
    print(Coord)
    Filename = 'TrackData_' + Coord
    Filename = Filename.replace(" ","_")
    i = int(((tend-tstart).total_seconds())/StepSize); 
    tstart = tstart0
    Ephem = open(f'{Filename}.txt',"a")
    Ephem.write('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
    Ephem.write('UTC\t\t\t\t\tAZ[deg]\t\tEL[deg]\t\t\t AZ-vel[deg/s]\t\t\tEl-vel[deg/s]\t\tRange[km]\tRangeRate[km/s]\t     Doppler[khz]\t\tLevel[dBm] \n')
    Ephem.write('--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n')
    for i in range (i+1):
        
            Epoch = (tstart-tstart0).total_seconds()
            PrintUTC = Datefun.dt2dat(tstart)
            Result = list(HL.LookAngles(tstart))   
            Result1 = list(HL.TOPO(tstart))
            
            Az = str(Result[Index][0]);  El = str(Result[Index][1]);
            dAz = str(Result[Index][2]); dEl = str(Result[Index][3])
            
            range_scalar = str(Result1[Index][3]);
            range_rate =  str(Result1[Index][4]) 
            Doppler = str(1000*(Result1[Index][5])) 
            Power =  str((np.sum(np.array((Result1[Index][6])))))    
            Epoch = str(Epoch)
            Ephem.write(PrintUTC + '\t\t' + Az + '\t' + El + '\t' + dAz + '\t' +\
                        dEl + '\t' + range_scalar + '\t' + range_rate + '\t' + \
                            Doppler + '\t' + '\t' + Power + '\n')
            Looptime = tstart +dt.timedelta(seconds = StepSize)
            tstart = Looptime
                   
    Ephem.close()      
       
