from struct import pack
import math
from micropython import const
from machine import I2C
THRESH_TAP=const(0x1d)     #敲击部分寄存器地址
DUR=const(0x21)
LATENT=const(0x22)
WINDOW=const(0x23)
TAP_AXES=const(0x2a)

THRESH_ACT=const(0x24)     #活动静止部分寄存器地址
THRESH_INACT=const(0x25)
TIME_INACT=const(0x26)
ACT_INACT_CTL=const(0x27)

THRESH_FF=const(0x28)    #自由落体部分寄存器地址
TIME_FF=const(0x29)

OFSX = const(0x1e)      #偏置补偿寄存器
OFSY =const(0x1f)
OFSZ =const(0x20)

DATA_FORMAT = const(0x31)#格式输出数据
BW_RATE  = const(0x2c)   #功耗寄存器
POWER_CTL = const(0x2d)  #测量模式寄存器


INT_ENABLE  = const(0x2E)#中断设置部分寄存器
INT_MAP=const(0x2f)      #中断映射
INT_SOURCE=const(0x30)  #只读
class ADXL345:
    def __init__(self, i2c:I2C):

        self.i2c = i2c
        self.slvAddr = 83

        self.writeByte(THRESH_TAP,0x3f)#62.5mg/lsb  敲击阈值
        self.writeByte(DUR,0x20)#625us/lsb          敲击时最大时长
        self.writeByte(LATENT,0x20)#1.25ms/lsb      到等待窗口的时间
        self.writeByte(WINDOW,0xd0)#1.25ms/lsb      等待窗口的时间
        self.writeByte(TAP_AXES,0b1)#              抑制|TAP_X|Y|Z

        #self.writeByte(THRESH_ACT,0xf)#62.5mg/lsb     检测活动阈值
        #self.writeByte(THRESH_INACT,0xff)#62.5mg/lsb  检测静止阈值
        #self.writeByte(TIME_INACT,0xff)# 1sec/lsb     静止时间阈值
        #self.writeByte(ACT_INACT_CTL,0b00)#     活动：交流|X|Y|Z 静止：交流|X|Y|Z

        #self.writeByte(THRESH_FF,0X30)#62.5mg/lsb     自由落体检测
        #self.writeByte(TIME_FF,0X30)#5ms/lsb          自由落体时间检测

        self.writeByte(INT_ENABLE,0b00100000)#中断使能，双击检测和单击检测
        self.writeByte(INT_MAP,0b00100000)   #双击映射到INT2,单击映射到INT1

        self.writeByte(DATA_FORMAT,0Xb)#全分辨率，16g量程，自测力关闭,右对齐

        self.writeByte(OFSX,0x00)#无修正
        self.writeByte(OFSY,0x00)
        self.writeByte(OFSZ,0x00)

        self.writeByte(POWER_CTL,0x28)#始终为测量模式，关闭Auto睡眠mode

        self.writeByte(BW_RATE,0xc)#开局为common模式，50HZ，速率代码1001（Lowpower模式）
        self.i2c.readfrom_mem(self.slvAddr,INT_SOURCE,1)
        self.singleTap_thresh=0x16

    def doubleTap_int(self):
        self.writeByte(INT_ENABLE,0b00100000)
        self.writeByte(THRESH_TAP,0x3f)
        self.writeByte(TAP_AXES,0b111)

    def deinit_int(self):
        self.writeByte(INT_ENABLE,0x00)


    def intclear(self):
        self.i2c.readfrom_mem(self.slvAddr,INT_SOURCE,1)

    def on(self):
        self.writeByte(BW_RATE,0xc)#进入测量模式，50HZ,速率代码1001,（testmode）

    def off(self):
        self.writeByte(BW_RATE,0xc)#common模式，50HZ，速率代码1001（Lowpower模式）

    def readXYZ(self):
        data_rev=self.i2c.readfrom_mem(83,0x32,6)
        if (data_rev[1]>>7)&1==0:
            x=data_rev[0]+((data_rev[1]&0b11111)<<8)
        else:
            x=-(pack('b',~(data_rev[0]))[0]+(pack('b',~(data_rev[1]))[0]<<8)+1)

        if (data_rev[3]>>7)&1==0:
            y=data_rev[2]+((data_rev[3]&0b11111)<<8)
        else:
            y=-(pack('b',~(data_rev[2]))[0]+(pack('b',~(data_rev[3]))[0]<<8)+1)

        if (data_rev[5]>>7)&1==0:
            z=data_rev[4]+((data_rev[5]&0b11111)<<8)
        else:
            z=-(pack('b',~(data_rev[4]))[0]+(pack('b',~(data_rev[5]))[0]<<8)+1)
        return (x,y,z)
    def writeByte(self, addr, data):
        d = bytearray([data])
        self.i2c.writeto_mem(self.slvAddr, addr, d)
    def readByte(self, addr):
        return self.i2c.readfrom_mem(self.slvAddr, addr, 1)
    def RP_calculate(self,x,y,z):
        roll = math.atan2(float(y) , float(z)) * 57.3
        pitch = math.atan2((- float(x)) , math.sqrt(float(y) * float(y) + float(z) * float(z))) * 57.3
        return roll,pitch


