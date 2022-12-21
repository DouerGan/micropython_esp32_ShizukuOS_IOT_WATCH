from machine import I2C
from struct import pack
class PCF8563:
    def __init__(self,i2c:I2C):
        self.i2c=i2c
        self.sec=0
        self.min=0
        self.hour=0
        self.day=0
        self.month=0
        self.year=0
        self.week=0
        self.clkout=False
        self.i2c.writeto_mem(0x51,0x0d,pack('b',0b00000010))
        self.timelist=[]  #秒分时日星期月年
        self.i2c.writeto_mem(0x51,0x00,pack('b',0b0))
    def clkouton(self):
        self.i2c.writeto_mem(0x51,0x0d,pack('b',0b10000010))
        self.clkout=True
    def clkoutoff(self):
        self.i2c.writeto_mem(0x51,0x0d,pack('b',0b00000010))
        self.clkout=False
    def gettime(self):
        self.timelist=self.i2c.readfrom_mem(0x51,0x02,8,addrsize=8)
        self.sec=self.timelist[0]<<1>>1
        self.min=self.timelist[1]
        self.hour=self.timelist[2]
        self.day=self.timelist[3]
        self.week=self.timelist[4]
        self.month=self.timelist[5]
        self.year=self.timelist[6]
        self.timelist=[hex(int(bin(self.sec),2))[2:],hex(self.min)[2:],hex(self.hour)[2:],hex(self.day)[2:],hex(self.week)[2:],hex(self.month)[2:],hex(self.year)[2:],0x00]
        #秒分时日星期月年
        return self.timelist
    def settime(self,list):
        for i in range(0,7):
            self.i2c.writeto_mem(0x51,i+2, bytes([list[i]]),addrsize=8)
