import sys 

def BANNER():
    from Datefun import curday
    Time = str(curday())
    return  print('Team Members: Diego Mateos, Nikeet Pandit\nThe time is:', Time,\
          '\nPython Version',sys.version,'\nWelcome, loved the B-5th excerpt.')
        
def ERRMSG(STRING): #Beep Sound works on Spyder
    print('\a')
    print('beep boop beep - error')
    
def AnyNum():
    Num = input('If Satisfied Press 1 to Continue .OR. Press 0 to Exit:\t\t')
    return Num

class Station(): 
    def __init__(self,STNFIL):
        self.name = STNFIL[0]
        self.stnlat = float(STNFIL[1])
        self.stnlong = float(STNFIL[2])
        self.stnalt = float(STNFIL[3])
        self.utc_offset = float(STNFIL[4])
        self.az_el_nlim = float(STNFIL[5])
        index = int(STNFIL[5])
        AZ = []
        EL_MIN = []
        EL_MAX = []
        for i in range (index):
            TubSplit = (STNFIL[i+6]).split()
            az = float(TubSplit[0])
            el_min = float(TubSplit[1])
            el_max = float(TubSplit[2])
            AZ.append(az)
            EL_MIN.append(el_min)
            EL_MAX.append(el_max)
        self.az = AZ
        self.elmin = EL_MIN
        self.elmax = EL_MAX
        self.st_az_speed_max = float(STNFIL[-2])
        self.st_el_speed_max = float(STNFIL[-1])

class Satellite(): 
    def __init__(self,line0,line1,line2):
        self.name = line0[-11:-5]
        self.refepoch = float(line1[1])
        self.incl = float(line2[0])
        self.raan = float(line2[1])
        self.eccn = float('.'+line2[2])
        self.argper = float(line2[3])
        self.meanan = float(line2[4])
        self.meanmo = float(line2[5])
        self.ndot = float(line1[2])
        self.nddot6 = 0
        self.bstar = float(0)
        self.orbitnum = float(line1[5])
        