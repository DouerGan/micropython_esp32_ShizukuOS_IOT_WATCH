from machine import Pin,UART
from harddrive.micropyGPS import MicropyGPS
import time
class GPS:
    def __init__(self,rx:int,tx:int,en:int,baudrate:int,bus:int,time_zone=8,stop=0,cmode=False):
        self.bus=bus
        self.baudrate=baudrate
        self.uart1=UART(bus, baudrate=baudrate, tx=tx, rx=rx)
        self.en=Pin(en,Pin.OUT,value=stop)
        self.rx=rx
        self.tx=tx
        self.cmode=cmode
        self.mode=0
        self.my_gps=MicropyGPS(time_zone)
        self.my_gps.local_offset
        self.stop=stop
    def off(self):
        self.uart1.deinit()
        self.en.value(self.stop)
        Pin(self.rx,Pin.OUT,value=0)
        Pin(self.tx,Pin.OUT,value=0)
        self.mode=0
    def on(self):
        self.uart1=UART(self.bus, baudrate=self.baudrate, tx=self.tx, rx=self.rx)
        self.en.value(not self.stop)
        self.mode=1
    def getinf(self):
        time.sleep(0.1)
        inf=str(self.uart1.readline())
        print(inf)
        if inf!=None:
            for x in inf:
                self.my_gps.update(x)
    def getdate(self)->str:
        return '20'+str(self.my_gps.date[2])+'-'+str(self.my_gps.date[1])+'-'+str(self.my_gps.date[0])
    def gettime(self)->str:
        return str(self.my_gps.timestamp[0])+':'+str(self.my_gps.timestamp[1])+':'+str(self.my_gps.timestamp[2])
    def getlongitude(self)->str:
        return str(self.my_gps.longitude[0])+'.'+str(self.my_gps.longitude[1])+'\'--'+str(self.my_gps.longitude[2])
    def getlatitude(self)->str:
        return str(self.my_gps.latitude[0])+'.'+str(self.my_gps.latitude[1])+'\'--'+str(self.my_gps.latitude[2])
    def getplace(self)->str:
        return str(self.my_gps.course)+'--'+str(self.my_gps.geoid_height)+'m'
    def getspeed(self)->str:
        return str(float(self.my_gps.speed[2])*0.514)[0:5]+'m/s'




