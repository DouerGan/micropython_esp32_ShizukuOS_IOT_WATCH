from micropython import const
from machine import I2C
from struct import pack
import time
from math import atan2,atan
class QMC5883L():
    def __init__(self,i2c:I2C,addr=13) -> None:
        self.i2c=i2c
        self.addr=addr
        self.i2c.writeto_mem(self.addr,0x09,pack('b',0b00001100))
        self.i2c.writeto_mem(self.addr,0x0a,pack('b',0b0))
        self.i2c.writeto_mem(self.addr,0x0b,pack('b',0x01))
        self.data=bytearray(9)
    def on(self):
        self.i2c.writeto_mem(self.addr,0x9,pack('b',0b00001101))
    def off(self):
        self.i2c.writeto_mem(self.addr,0x9,pack('b',0b00001100))
    def getdata(self):
        self.data=self.i2c.readfrom_mem(self.addr,0x0,9)
        if (self.data[1]>>7)&1==0:
            x=self.data[0]+((self.data[1])<<8)
        else:
            x=-(pack('b',~(self.data[0]))[0]+(pack('b',~(self.data[1]))[0]<<8)+1)

        if (self.data[3]>>7)&1==0:
            y=self.data[2]+((self.data[3])<<8)
        else:
            y=-(pack('b',~(self.data[2]))[0]+(pack('b',~(self.data[3]))[0]<<8)+1)

        if (self.data[5]>>7)&1==0:
            z=self.data[4]+((self.data[5])<<8)
        else:
            z=-(pack('b',~(self.data[4]))[0]+(pack('b',~(self.data[5]))[0]<<8)+1)
        return x,y,z
    def getmag(self,GaX,GaY):
        a=0
        if GaX>0 and GaY>0:
            return atan(GaY/GaX)*57-a
        elif((GaX > 0)and(GaY < 0)):
            return 360+atan(GaY/GaX)*57-a
        elif((GaX == 0)and(GaY > 0)):
            return 90-a
        elif((GaX == 0)and(GaY < 0)):
            return 270-a
        elif(GaX < 0):
            return 180+atan(GaY/GaX)*57-a

from machine import freq,Pin,I2C,UART,ADC,SPI,Timer
from softdrive.averagefiter import AVERAGEFITER
i2c=I2C(0,scl=Pin(21),sda=Pin(22),freq=400000)
fiter=AVERAGEFITER(13,3)
qmc=QMC5883L(i2c)
qmc.off()
qmc.on()
while True:
    a=fiter.update(qmc.getdata())
    #print(a)
    print(qmc.getmag(a[0],a[1]))
    time.sleep(0.1)
