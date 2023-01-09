import HighLevel_v2 as HL
import DebuggingV1 as dbug
import Fileio as Fio
import Parse


#Specify TLE, Station Data in Parse Module
#Specify Tracking in TextFile
#N Refers to Number of Satellites in TLE

#For Debugging...
#Coordinates in: ECI, ELEMENTS, ECF, TOPO
#Elements Returns: Perigee, Raan, True Anom, Meam Anomaly, Mean Anomaly Motion
#GMST Angle, and Eccentric Annomaly (SEE IF STATEMENT AT END)
#Pointing Returns Az, El
#Debugger in Main Works for Chosen Satellite... 
#You May Debug for All Satellites in TLE
#Refer to Debugger Modulue for more details   
#Returns File Designator Based on Satellite Name + Debugging Report Type



StepSize = 60             #Set your StepSize


Fio.BANNER()

## Checking Your Inputs are as Desired 
MyLogic = int(Fio.AnyNum())
if MyLogic == 0:
    raise SystemExit 

print("\nPrinting TLE Epoch Times\n")
TLETimes = list(HL.SatEpoch()); N = len(TLETimes); 
for i in range(N):
    print(TLETimes[i][1])
    
print("\nPrinted TLE Epoch Times\n")
  
MyLogic = int(Fio.AnyNum())
if MyLogic == 0:
    raise SystemExit 
    
print("\nEnsure Station and TLE Data is as Desired")
STNName =  Parse.StationParam()[0]
print("Tracking Station Name:\t" + STNName)   
MyLogic = int(Fio.AnyNum())
if MyLogic == 0:
    raise SystemExit 
    
    
print("\nEnsure Tracking Interval is as Desired")
tstart = Parse.tracking()[0]
tend = Parse.tracking()[1]
print(tstart)
print(tend)

## Finish Checking Inputs are as desired 


#Printing Out AOS/LOS Table to Working Directory 
Names = list(HL.SatName()); 
MyLogic = int(Fio.AnyNum())
if MyLogic == 0:
    raise SystemExit 
print("AOS LOS Table Output\n")
dbug.AOSLOS1(StepSize, N)
# print("Done!")
# print("Please Inspect Output")

# MyLogic = int(Fio.AnyNum())
# if MyLogic == 0:
#     raise SystemExit 
# print("\n")
# dbug.PrintSatName()
    
    
#Select Your Satellite for Tracking Using the Index beside Sat Name   
#Place Your Index Here

## Printing According to ARO Specifications 
AROLogic = input("Generate ASCII text file for ARO Control Computer?  Input 1: Else 0\t\t ")
if AROLogic == 0:
    raise SystemExit 
print("\n")
Index = input("Enter SAT No. for Tracking\t")
Index = int(Index)
dbug.AROTrackData(StepSize,Index)
    

#Debugging Options 
TrackedSat = list(HL.SatName())[Index]
DebugLogic = input("Would you like to Debug " + TrackedSat +"?  Input 1: Else 0\t\t")
DebugLogic = int(DebugLogic)
if DebugLogic == 1:
    dbug.STKoutIndx('ECI',StepSize,N,Index)
    dbug.STKoutIndx('ECF',StepSize,N,Index)
    dbug.STKoutIndx('ELEMENTS',StepSize,N,Index)
    dbug.STKoutIndx('TOPO',StepSize,N,Index)
    dbug.STKspIndx(StepSize,Index,N)
    dbug.TrackData(StepSize,Index)
    print("Done!")
    print("Thank You!")
else:
    print("Thank you!")








