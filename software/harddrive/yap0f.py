from machine import Pin
from esp32 import RMT
import time
from softdrive.function import fill0,compile
class YAP0F:
    def __init__(self,ioout:int):
        self.ioout=Pin(ioout,Pin.OUT)
        self.rmt=RMT(0,pin=self.ioout,clock_div=80,tx_carrier=(38000, 50, 1))
        self.atdir={}
    def write(self,at):
        self.rmt.write_pulses(self.atdir[at],1)
    def addat(self,checkcode1=None,checkcode2=None,mode=1,powersw=0,speed=0,temp=24,timingsw=0,hour=0,min=0,lightsw=1,powermode=0,usecheckcodedir=True):
        modelist=['000','100','010','110','001']
        speedlist=['00','10','01','11']
        checkcodedir={16:'11101100',17:'00010010',18:'10011010',19:'01010110',20:'11011110',21:'00110001',22:'10111001',23:'01110101',24:'11111101',25:'00000011',26:'10001011',27:'01000111'}
        cc=''
        if powersw==0:
            cc='11101100'
            temp=24
        else:
            if usecheckcodedir:
                cc=checkcodedir[temp]
            else:
                cc=checkcode1+checkcode2
        tempbin=''.join(list(reversed(fill0(4,0,bin(temp-16)[2:]))))
        minbin=''.join(list(reversed(fill0(3,0,bin(min)[2:]))))
        hourbin=''.join(list(reversed(fill0(4,0,bin(hour)[2:]))))
        atlist=modelist[mode]+str(powersw)+speedlist[speed]+2*'0'+tempbin+minbin+str(timingsw)+hourbin
        at1=atlist+str(powermode)+str(lightsw)+3*'0'+'0001010010'+14*'0'+'1'+13*'0'+cc[:4]
        at2=atlist+str(powermode)+str(lightsw)+3*'0'+'0001110010'+28*'0'+cc[4:]
        self.rmt.write_pulses(compile(at1)+[516],1)
        time.sleep_ms(162)
        self.rmt.write_pulses(compile(at2)+[516],1)
