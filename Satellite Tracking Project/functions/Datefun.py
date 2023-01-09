import datetime as dt 
import numpy as np

def dtay(YEAR):
    TimeTuple = dt.datetime(YEAR,1,1)
    return TimeTuple 


def dtep(EPOCH):
    EPOCHint = str(np.int((np.modf(EPOCH)[1]))).zfill(5)
    EPOCHdt = dt.datetime.strptime(EPOCHint,'%y%j')
    dfrac = np.modf(EPOCH)[0]
    dfracdt = dt.timedelta(microseconds = (dfrac*24*3600*10**6))
    TimeTuple = EPOCHdt + dfracdt
    return TimeTuple

def doy(YR,MO,D):
    DateObj = dt.date(YR,MO,D)
    dayNumber = DateObj.timetuple().tm_yday #Sees where the Python Datetime is in range [1 366] 
    return dayNumber


def frcofd(HR,MI,SE):
    MItoHR = MI/60
    SEtoHR = SE/3600
    dayFraction = np.modf((HR + MItoHR + SEtoHR)/24)[0]
    if dayFraction == 0:
            dayFraction = 1
    return dayFraction

def dat2dt(DateString):
    TimeTuple = dt.datetime.strptime(DateString, '%Y-%m-%d %H:%M:%S')
    return TimeTuple

def dt2dat(TimeTuple):
    DateString = dt.datetime.strftime(TimeTuple,'%Y-%m-%d %H:%M:%S')
    return DateString 

def dt2dat1(TimeTuple):
    DateString = dt.datetime.strftime(TimeTuple,'%Y-%m-%d %H-%M-%S')
    return DateString 

def deg2ms(degrees):
    Hours = np.modf(degrees)[1]
    Minutes = (np.modf(degrees)[0]*60)
    Seconds = round(np.modf(Minutes)[0]*60,1)
    Minutes = round(Minutes)
    return Hours, Minutes, Seconds

def curday():
    dt.datetime.now()
    NowUTC = dt.datetime.strftime(dt.datetime.now(), '%Y-%m-%d %H:%M:%S.%f')
    return NowUTC[:-4]