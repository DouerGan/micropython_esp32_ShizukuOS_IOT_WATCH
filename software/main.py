# 2022-11-06-1:11 v1.1
#导入模块
from machine import freq,Pin,I2C,SPI,Timer,lightsleep
freq(240000000)
from gc import collect,mem_free
import _thread
# from harddrive.gps import GPS
from gps import GPS
from harddrive.pcf8563 import PCF8563
from harddrive.ssd1306 import SSD1306_SPI
from harddrive.ads1115 import ADS1115
from harddrive.bmp280 import BMP280
from harddrive.yap0f import YAP0F
from adxl345 import ADXL345
from softdrive.stock import STOCK
from softdrive.averagefiter import AVERAGEFITER
from softdrive.function import pixelpo
from softdrive.menu import POINT,MENU
from apps.cube import CUBE
from apps.showsettime import showsettime
from apps.showtaskbar import showtaskbar
from apps.showtime import showtime
from apps.showtemp import showtemp
from apps.showaltitude import showaltitude
from apps.showbds import showbds
from apps.showtly import showtly
from apps.showclkout import showclkout
from apps.showchoicemenu import showchoicemenu
from apps.showpic import showpic
from time import sleep_us,sleep_ms
import esp32
#定义类————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
i2c=I2C(0,scl=Pin(21),sda=Pin(22),freq=400000)
spi=SPI(2,baudrate=20000000,sck=Pin(2),mosi=Pin(15))
oled=SSD1306_SPI(128,64,spi,dc=Pin(14),res=Pin(13),cs=Pin(27))
rtc=PCF8563(i2c)
accelerometer=ADXL345(i2c)
adc_1115=ADS1115(i2c)
barometer=BMP280(i2c)
rmt=YAP0F(4)
# compass=HMC5883L(i2c)
gps=GPS(25,26,33,9600,1,8,1)
menucube=CUBE(4,110,56,oled)
collect()
picstock=STOCK(['bignum','ccby4','menulogo','otherlogo','midnum'])
fil=AVERAGEFITER(16,3)
#定义全局变量——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
settime_pointer=6
rmt_list=[23,0,0,1]
settime_list=[0,0,0,0,0,0,0]
statemode='menu'
tasklist=[]
statelist=['menu','adxl345','flashlight','temp','pdf','clock','hmc5883l','photo','rmt','pcimachine','setting']
state=0
clktotal=[0,0,0,0]
totallistforclk=[[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
adc=[0,0]
sleeptime_int=5000
iswake_bool=True
menuspan=40
gyrospan=40
loadpic_str=None
picpositionY_int=0
imgtoosmall=False
offset=0
#定义输入引脚_____________________________________________________________________________________________________________________
pinup=Pin(38,Pin.IN)
pindown=Pin(36,Pin.IN)
pinsure=Pin(37,Pin.IN)
pinback=Pin(0,Pin.IN,Pin.PULL_UP)
pindoubletap=Pin(35,Pin.IN)
pinmoveint=Pin(34,Pin.IN)
pinclkout=Pin(9,Pin.IN,Pin.PULL_UP)
pinrecharge_read=Pin(39,Pin.IN)
pinrecharge_en=Pin(19,Pin.OUT,value=1)
wakePin_tuple=(pinup,pindown,pinsure,pindoubletap)
#定义输出引脚#——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
led=Pin(32,Pin.OUT,value=0)
#定义计时器
sleep_timer=Timer(1)
#定义多级菜单类__________________________________________________________________________________________________________________
    #定义单项
        #setting菜单
def tosettime():
    global statemode,settime_pointer,settime_list,rtc
    statemode='settime'
    settime_pointer=6
    a=rtc.gettime()
    settime_list=[]
    for i in a:
        try:
            settime_list.append(abs(int(i)))
        except:
            settime_list.append(0)
settime_point=POINT('settime',picstock,['point'],tosettime,True)
def displayinvert():
    global oled,invert_point
    oled.invert(not invert_point.pointer)
invert_point=POINT('oled.invert',picstock,['off','on'],displayinvert,True,priority=False)
def display_contrast():
    global contrast_point,oled
    oled.contrast(int(contrast_point.modelist[contrast_point.pointer]))
contrast_point=POINT('oled.lum',picstock,['8','16','32','64','128','255'],display_contrast,False)
def setsleeptime():
    global sleeptime_int
    sleeptime_int=int(sleeptime_point.modelist[sleeptime_point.pointer])*1000
    print(sleeptime_int)
sleeptime_point=POINT('sleep.time',picstock,['5','10','20','600'],setsleeptime,False)
def showsysteminfo():
    global statemode
    statemode='systeminfo'
systemifor_point=POINT('systeminfo',picstock,['point'],showsysteminfo,True)
def choicemenuspan_function():
    global menuspan
    menuspan=int(choicemenuspan_point.modelist[choicemenuspan_point.pointer])
choicemenuspan_point=POINT('menuspan',picstock,['30','45','60','75','90'],choicemenuspan_function,False)
def choicegyrospan_function():
    global gyrospan
    gyrospan=int(choicegyrospan_point.modelist[choicegyrospan_point.pointer])
choicegyrospan_point=POINT('gyrospan',picstock,['30','45','60','75','90'],choicegyrospan_function,False)
def overclock_function():
    freq(int(overclock_point.modelist[overclock_point.pointer])*1000000)
overclock_point=POINT('overclock',picstock,['40','80','160','240'],overclock_function,False)
        #led控制菜单
def ledfilp():
    global led,ledmode_point,tasklist
    if led.value()==0:
        led.value(1)
        tasklist.append('flash')
    else:
        led.value(0)
        tasklist.remove('flash')
ledmode_point=POINT('ledmode',picstock,['off','on'],ledfilp,True)
        #图库控制菜单
def picshowonoled():
    global picstock,picmenu_menu,statemode,loadpic_str,imgtoosmall
    loadpic_str=picmenu_menu.window[picmenu_menu.pointer].title
    picstock.loadintocache('picst',loadpic_str)
    if picstock.get('cache',loadpic_str).h<=64:
        imgtoosmall=True
    else:
        imgtoosmall=False
    statemode='pic'
picpoint_list=[]
for i in picstock.getfilelist('/picst'):
    picpoint_list.append(POINT(i[:-4:].lower(),picstock,['point'],picshowonoled,True))
        #空调控制菜单
def setrmt_list():
    global rmt_list
    rmt_list[1]=int(powersw_point.modelist[powersw_point.pointer])
    rmt_list[0]=int(temp_point.modelist[temp_point.pointer])
    rmt_list[2]=int(forceful_point.modelist[forceful_point.pointer])
    rmt_list[3]=int(lightsw_point.modelist[lightsw_point.pointer])
powersw_point=POINT('power-sw',picstock,['0','1'],setrmt_list,False)
temp_point=POINT('temp',picstock,['16','17','18','19','20','21','22','23','24','25','26','27'],setrmt_list,False)
forceful_point=POINT('forceful',picstock,['0','1'],setrmt_list,False)
lightsw_point=POINT('light-sw',picstock,['0','1'],setrmt_list,False)
def sendrmt_list():
    global rmt_list,rmt
    rmt.addat(temp=rmt_list[0],powersw=rmt_list[1],powermode=rmt_list[2],lightsw=rmt_list[3])
send_point=POINT('send',picstock,['point'],sendrmt_list,True)
        #smartHOME控制菜单
def showyap0f():
    global statemode
    statemode='rmtmenu'
gotoyap0f_point=POINT('yap0f',picstock,['point'],showyap0f,True)
        #pcimachine控制菜单
def showbdsmenu():
    global statemode
    statemode='bdsmenu'
gotobds_point=POINT('gnss-bds',picstock,['point'],showbdsmenu,True)
    #定义菜单
settingmenu_menu=MENU([invert_point,contrast_point,sleeptime_point,settime_point,choicemenuspan_point,choicegyrospan_point,overclock_point,systemifor_point],7)
ledmenu_menu=MENU([ledmode_point],7)
picmenu_menu=MENU(picpoint_list,7)
smarthome_menu=MENU([gotoyap0f_point],7)
pcimachine_menu=MENU([gotobds_point],7)
rmtmenu_menu=MENU([powersw_point,temp_point,forceful_point,lightsw_point,send_point],7)
#中断函数——————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
def upint(irq):
    global statemode,state,statelist,clktotal,settingmenu_menu,settime_pointer,settime_list,ledmenu_menu,sleep_timer,sleeptime_int,iswake_bool,oled
    global menucube,picstock,picpositionY_int,imgtoosmall
    accelerometer.doubleTap_int()
    accelerometer.intclear()
    sleep_ms(15)
    if pinup.value()==1:
        print('pinupirq')
        print(picstock.stockdir['cache'])
        collect()
        print(mem_free())
        sleep_timer.init(period=sleeptime_int,mode=Timer.PERIODIC,callback=tosleep)
        if iswake_bool==False:
            oled.poweron()
            oled.contrast(int(contrast_point.modelist[contrast_point.pointer]))
            oled.invert(invert_point.pointer)
            menucube=CUBE(4,110,56,oled)
            accelerometer.intclear()
            iswake_bool=True
        else:
            if statemode in statelist:
                state=state-1
                if state==-1:
                    state=len(statelist)-1
                statemode=statelist[state]
            elif statemode=='showtemp':
                statemode='showaltitude'
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
            elif statemode=='showaltitude':
                statemode='showtemp'
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
            elif statemode=='clkout':
                clktotal=[0,0,0,0]
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
            elif statemode=='settingmenu':
                settingmenu_menu.up()
            elif statemode=='settime':#秒分时日星期月年
                settime_list[settime_pointer]+=1
                if settime_pointer in [0,1]:
                    if settime_list[settime_pointer]==60:
                        settime_list[settime_pointer]=0
                elif settime_pointer==2:
                    if settime_list[settime_pointer]==24:
                        settime_list[settime_pointer]=0
                elif settime_pointer==3:
                    if settime_list[settime_pointer]==32:
                        settime_list[settime_pointer]=0
                elif settime_pointer==4:
                    if settime_list[settime_pointer]==7:
                        settime_list[settime_pointer]=0
                elif settime_pointer==5:
                    if settime_list[settime_pointer]==13:
                        settime_list[settime_pointer]=1
                elif settime_pointer==6:
                    if settime_list[settime_pointer]==100:
                        settime_list[settime_pointer]=0
            elif statemode=='ledmenu':
                ledmenu_menu.up()
            elif statemode=='picmenu':
                picmenu_menu.up()
            elif statemode=='pic':
                if not imgtoosmall:
                    if picpositionY_int-8>=0:
                        picpositionY_int-=8
            elif statemode=='rmtmenu':
                rmtmenu_menu.up()
            elif statemode=='smarthomemenu':
                smarthome_menu.up()
            elif statemode=='pcimachinemenu':
                pcimachine_menu.up()
def downint(irq):
    global statemode,state,statelist,totallistforclk,clktotal,settingmenu_menu,settime_pointer,settime_list,ledmenu_menu,sleep_timer,sleeptime_int,iswake_bool,oled
    global menucube,picpositionY_int,imgtoosmall
    accelerometer.doubleTap_int()
    accelerometer.intclear()
    sleep_ms(15)
    if pindown.value()==1:
        print('pindownirq')
        print(mem_free())
        collect()
        sleep_timer.init(period=sleeptime_int,mode=Timer.PERIODIC,callback=tosleep)
        if iswake_bool==False:
            oled.poweron()
            oled.contrast(int(contrast_point.modelist[contrast_point.pointer]))
            oled.invert(invert_point.pointer)
            menucube=CUBE(4,110,56,oled)
            accelerometer.intclear()
            iswake_bool=True
        else:
            if statemode in statelist:
                state=state+1
                if state==len(statelist):
                    state=0
                statemode=statelist[state]
            elif statemode=='showtemp':
                statemode='showaltitude'
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
            elif statemode=='showaltitude':
                statemode='showtemp'
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
            elif statemode=='clkout':
                totallistforclk.append([clktotal[0],clktotal[1],clktotal[2],clktotal[3]])
                totallistforclk.pop(0)
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
            elif statemode=='settingmenu':
                settingmenu_menu.down()
            elif statemode=='settime':#秒分时日星期月年
                settime_list[settime_pointer]-=1
                if settime_list[settime_pointer]==-1:
                    if settime_pointer in [0,1]:
                        settime_list[settime_pointer]=59
                    elif settime_pointer==2:
                        settime_list[settime_pointer]=23
                    elif settime_pointer==6:
                        settime_list[settime_pointer]=99
                    elif settime_pointer==4:
                        settime_list[settime_pointer]=6
                if settime_list[settime_pointer]==0:
                    if settime_pointer==3:
                        settime_list[settime_pointer]=31
                    elif settime_pointer==5:
                        settime_list[settime_pointer]=12
            elif statemode=='ledmenu':
                ledmenu_menu.down()
            elif statemode=='picmenu':
                picmenu_menu.down()
            elif statemode=='pic':
                if not imgtoosmall:
                    if picpositionY_int+64<=127:
                        picpositionY_int+=8
            elif statemode=='rmtmenu':
                rmtmenu_menu.down()
            elif statemode=='smarthomemenu':
                smarthome_menu.down()
            elif statemode=='pcimachinemenu':
                pcimachine_menu.down()
def backint(irq):
    global statemode,state,statelist,rtc,accelerometer,ledmenu_menu,sleep_timer,sleeptime_int,iswake_bool,oled,menucube
    global loadpic_str,picstock,picpositionY_int
    sleep_ms(35)
    if pinback.value()==0:
        print('pinbackirq')
        print(mem_free())
        collect()
        sleep_timer.init(period=sleeptime_int,mode=Timer.PERIODIC,callback=tosleep)
        if iswake_bool==False:
            pass
        else:
            if statemode=='menu':
                oled.poweroff()
                oled.poweroff()
                print('irq to sleep')
                iswake_bool=False
                gps.off()
                rtc.clkoutoff()
                if 'clock' in tasklist:
                    tasklist.remove('clock')
                if 'bds' in tasklist:
                    tasklist.remove('bds')
                lightsleep()
            elif statemode in statelist:
                state=0
                statemode=statelist[state]
            elif statemode=='showtly':
                statemode='adxl345'
                accelerometer.off()
                state=statelist.index('adxl345')
            elif statemode=='showtemp' or statemode=='showaltitude':
                statemode='temp'
                barometer.off()
                state=statelist.index('temp')
            elif statemode=='clkout':
                statemode='clock'
                state=statelist.index('clock')
            elif statemode=='choicemenu':
                statemode='menu'
                accelerometer.off()
                state=statelist.index('menu')
            elif statemode=='settingmenu':
                statemode='setting'
                state=statelist.index('setting')
            elif statemode=='settime':
                statemode='settingmenu'
            elif statemode=='systeminfo':
                statemode='settingmenu'
            elif statemode=='ledmenu':
                statemode='flashlight'
                state=statelist.index('flashlight')
            elif statemode=='picmenu':
                statemode='photo'
                state=statelist.index('photo')
            elif statemode=='pic':
                statemode='picmenu'
            elif statemode=='smarthomemenu':
                statemode='rmt'
            elif statemode=='rmtmenu':
                statemode='smarthomemenu'
            elif statemode=='bdsmenu':
                statemode='pcimachinemenu'
            elif statemode=='pcimachinemenu':
                statemode='pcimachine'
                state=statelist.index('pcimachine')
def sureint(irq):
    global statemode,state,statelist,rtc,tasklist,fil,accelerometer,settingmenu_menu,settime_pointer,settime_list,rtc,ledmenu_menu,ledmenu_menu,sleep_timer,sleeptime_int,iswake_bool,oled
    global menucube,menuspan,picpositionY_int,offset,barometer
    accelerometer.doubleTap_int()
    accelerometer.intclear()
    sleep_ms(15)
    if pinsure.value()==1:
        print('pinsure')
        print(freq())
        collect()
        sleep_timer.init(period=sleeptime_int,mode=Timer.PERIODIC,callback=tosleep)
        if iswake_bool==False:
            oled.poweron()
            oled.contrast(int(contrast_point.modelist[contrast_point.pointer]))
            oled.invert(invert_point.pointer)
            menucube=CUBE(4,110,56,oled)
            accelerometer.intclear()
            iswake_bool=True
        else:
            sleep_timer.init(period=sleeptime_int,mode=Timer.PERIODIC,callback=tosleep)
            if statemode=='adxl345':
                fil.clear()
                statemode='showtly'
                accelerometer.on()
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
            elif statemode=='temp':
                statemode='showtemp'
                barometer.on()
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
            elif statemode=='clock':
                statemode='clkout'
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
            elif statemode=='clkout':
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
                if rtc.clkout==True:
                    rtc.clkoutoff()
                    tasklist.remove('clock')
                else:
                    rtc.clkouton()
                    tasklist.append('clock')
            elif statemode=='pdf':
                # sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
                # statemode='bdsmenu'
                pass
            elif statemode=='bdsmenu':
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
                if gps.mode==0:
                    gps.on()
                    tasklist.append('bds')
                else:
                    gps.off()
                    tasklist.remove('bds')
            elif statemode=='menu':
                sleep_timer.init(period=sleeptime_int*2,mode=Timer.PERIODIC,callback=tosleep)
                statemode='choicemenu'
                accelerometer.on()
                fil.clear()
            elif statemode=='choicemenu':
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
                accelerometer.off()
                xyz_list=fil.getvalue()
                rollandpitch=accelerometer.RP_calculate(xyz_list[0],xyz_list[1],xyz_list[2])
                position=pixelpo(rollandpitch[0],rollandpitch[1],64,36,menuspan)
                if position[1]<=34:
                    if position[0]<=28:
                        accelerometer.on()
                        statemode='showtly'
                    elif 57>=position[0] and position[0]>27:
                        statemode='ledmenu'
                    elif 94>=position[0] and position[0]>57:
                        statemode='showtemp'
                        barometer.on()
                    else:
                        pass
                else:
                    if position[0]<=26:
                        statemode='clkout'
                    elif 59>=position[0] and position[0]>25:
                        statemode='picmenu'
                    elif 90>=position[0] and position[0]>59:
                        statemode='pcimachinemenu'
                    else:
                        statemode='settingmenu'
            elif statemode=='setting':
                statemode='settingmenu'
            elif statemode=='settingmenu':
                settingmenu_menu.do()
            elif statemode=='settime':#秒分时日星期月年
                if settime_pointer==6:
                    settime_pointer=5
                elif settime_pointer==5:
                    settime_pointer=3
                elif settime_pointer==3:
                    settime_pointer=2
                elif settime_pointer==2:
                    settime_pointer=1
                elif settime_pointer==1:
                    settime_pointer=4
                elif settime_pointer==4:
                    a=[]
                    for i in settime_list:
                        a.append(int('0x'+str(i)))
                    a[0]=0
                    rtc.settime(a)
                    statemode='settingmenu'
            elif statemode=='ledmenu':
                ledmenu_menu.do()
            elif statemode=='flashlight':
                statemode='ledmenu'
            elif statemode=='photo':
                statemode='picmenu'
            elif statemode=='picmenu':
                picpositionY_int=0
                picmenu_menu.do()
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
            elif statemode=='rmtmenu':
                rmtmenu_menu.do()
            elif statemode=='rmt':
                statemode='smarthomemenu'
            elif statemode=='smarthomemenu':
                smarthome_menu.do()
            elif statemode=='showaltitude':
                offset+=(barometer.getAltitude()-offset)
            elif statemode=='pcimachine':
                statemode='pcimachinemenu'
            elif statemode=='pcimachinemenu':
                pcimachine_menu.do()
def clkoutint(irq):
    global clktotal
    clktotal[3]+=31.25
    if clktotal[3]==1000:
        clktotal[2]+=1
        clktotal[3]=0
    if clktotal[2]==60:
        clktotal[1]+=1
        clktotal[2]=0
    if clktotal[1]==60:
        clktotal[0]+=1
        clktotal[1]=0
def tosleep(irq):
    global iswake_bool,oled,gps,rtc
    oled.poweroff()
    oled.poweroff()
    collect()
    iswake_bool=False
    print('timer to sleep')
    if 'clock' in tasklist:
        tasklist.remove('clock')
    rtc.clkoutoff()
    lightsleep()
def doubletapint(irq):
    global statemode,state,statelist,rtc,tasklist,fil,accelerometer,settingmenu_menu,settime_pointer,settime_list,rtc,ledmenu_menu,ledmenu_menu,sleep_timer,sleeptime_int,iswake_bool,oled
    global menucube,accelerometer
    sleep_us(100)
    if pindoubletap.value()==1:
        print('doubletap',pindoubletap.value())
        print(mem_free())
        collect()
        accelerometer.intclear()
        sleep_timer.init(period=sleeptime_int,mode=Timer.PERIODIC,callback=tosleep)
        if iswake_bool==False:
            oled.poweron()
            oled.contrast(int(contrast_point.modelist[contrast_point.pointer]))
            oled.invert(invert_point.pointer)
            menucube=CUBE(4,110,56,oled)
            accelerometer.intclear()
            iswake_bool=True
        else:
            if statemode=='adxl345':
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
                fil.clear()
                statemode='showtly'
                accelerometer.on()
            elif statemode=='temp':
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
                statemode='showtemp'
                barometer.on()
            elif statemode=='clock':
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
                statemode='clkout'
            elif statemode=='clkout':
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
            elif statemode=='bds':
                # sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
                # statemode='bdsmenu'
                pass
            elif statemode=='bdsmenu':
                sleep_timer.init(period=600000,mode=Timer.PERIODIC,callback=tosleep)
                if gps.mode==0:
                    gps.on()
                    tasklist.append('bds')
                else:
                    gps.off()
                    tasklist.remove('bds')
            elif statemode=='setting':
                statemode='settingmenu'
            elif statemode=='settingmenu':
                settingmenu_menu.do()
            elif statemode=='settime':#秒分时日星期月年
                if settime_pointer==6:
                    settime_pointer=5
                elif settime_pointer==5:
                    settime_pointer=3
                elif settime_pointer==3:
                    settime_pointer=2
                elif settime_pointer==2:
                    settime_pointer=1
                elif settime_pointer==1:
                    settime_pointer=4
                elif settime_pointer==4:
                    a=[]
                    for i in settime_list:
                        a.append(int('0x'+str(i)))
                    a[0]=0
                    rtc.settime(a)
                    statemode='settingmenu'
            elif statemode=='ledmenu':
                ledmenu_menu.do()
            elif statemode=='flashlight':
                statemode='ledmenu'
            elif statemode=='menu':
                pass
            elif statemode=='photo':
                statemode='picmenu'
            elif statemode=='picmenu':
                picmenu_menu.do()
            elif statemode=='rmt':
                statemode='smarthomemenu'
            elif statemode=='smarthomemenu':
                smarthome_menu.do()
            elif statemode=='rmtmenu':
                rmtmenu_menu.do()
            elif statemode=='pcimachine':
                statemode='pcimachinemenu'
            elif statemode=='pcimachinemenu':
                pcimachine_menu.do()
#定时器中断函数
def feeddog():
    global adc_1115,adc,statemode,picstock,loadpic_str,picpositionY_int
    while 1:
        sleep_ms(5000)
        adc[0]=adc_1115.raw_to_v((adc_1115.read(rate=4,channel1=0)))*2
        adc[1]=adc_1115.raw_to_v((adc_1115.read(rate=4,channel1=1)))
        print(adc)
        if statemode!='pic':
            picstock.clearcache()
            loadpic_str=None
            picpositionY_int=0
#中断配置———————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
pinup.irq(trigger=Pin.IRQ_RISING, handler=upint)
pindown.irq(trigger=Pin.IRQ_RISING, handler=downint)
pinback.irq(trigger=Pin.IRQ_FALLING, handler=backint)
pinsure.irq(trigger=Pin.IRQ_RISING, handler=sureint)
pinclkout.irq(trigger=Pin.IRQ_FALLING, handler=clkoutint)
sleep_timer.init(period=sleeptime_int,mode=Timer.PERIODIC,callback=tosleep)
pindoubletap.irq(trigger=Pin.IRQ_RISING, handler=doubletapint)
esp32.wake_on_ext1(wakePin_tuple,esp32.WAKEUP_ANY_HIGH)
_thread.start_new_thread(feeddog,())
choicemenuspan_point.pointer=1
choicegyrospan_point.pointer=3
contrast_point.pointer=4
overclock_point.pointer=3


freq(int(overclock_point.modelist[overclock_point.pointer])*1000000)
oled.contrast(int(contrast_point.modelist[contrast_point.pointer]))
choicegyrospan_function()
choicemenuspan_function()
setrmt_list()

adc[0]=adc_1115.raw_to_v((adc_1115.read(rate=4,channel1=0)))*2
adc[1]=adc_1115.raw_to_v((adc_1115.read(rate=4,channel1=1)))
print(mem_free())
rtc.clkoutoff()
accelerometer.doubleTap_int()
collect()
#主函数————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————————
while True:
    while statemode=='menu':
        oled.fill(0)
        showtime(rtc,oled,picstock)
        menucube.draw()
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='adxl345':
        oled.fill(0)
        picstock.get('menulogo','adxl345',43,1).draw(oled)
        picstock.get('menulogo','flashlight').cropDrawX(103,1,0,picstock.get('menulogo','flashlight').w//2,oled)
        picstock.get('otherlogo','pointleft',0,4).draw(oled)
        picstock.yakitori(35,7,'ccby4','adxl345',1,oled)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='flashlight':
        oled.fill(0)
        picstock.get('menulogo','flashlight',40,1).draw(oled)
        picstock.get('menulogo','adxl345').cropDrawX(0,1,picstock.get('menulogo','adxl345').w//2,picstock.get('menulogo','adxl345').w,oled)
        picstock.get('menulogo','temp').cropDrawX(108,1,0,picstock.get('menulogo','temp').w//2-18,oled)
        picstock.yakitori(31,7,'ccby4','flashlight',1,oled)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='temp':
        oled.fill(0)
        picstock.get('menulogo','temp',33,1).draw(oled)
        picstock.get('menulogo','flashlight').cropDrawX(0,1,picstock.get('menulogo','flashlight').w//2+9,picstock.get('menulogo','flashlight').w,oled)
        picstock.get('menulogo','pdf').cropDrawX(114,1,0,picstock.get('menulogo','pdf').w//2-11,oled)
        picstock.yakitori(45,7,'ccby4','bmp280',1,oled)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='pdf':
        oled.fill(0)
        picstock.get('menulogo','pdf',40,1).draw(oled)
        picstock.get('menulogo','temp').cropDrawX(0,1,picstock.get('menulogo','temp').w//2+10,picstock.get('menulogo','temp').w,oled)
        picstock.get('menulogo','clock').cropDrawX(103,1,0,picstock.get('menulogo','clock').w//2,oled)
        picstock.yakitori(53,7,'ccby4','pdf',1,oled)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='clock':
        oled.fill(0)
        picstock.get('menulogo','clock',40,1).draw(oled)
        picstock.get('menulogo','pdf').cropDrawX(0,1,picstock.get('menulogo','pdf').w//2,picstock.get('menulogo','pdf').w,oled)
        picstock.get('menulogo','hmc5883l').cropDrawX(103,1,0,picstock.get('menulogo','hmc5883l').w//2,oled)
        picstock.yakitori(48,7,'ccby4','timer',1,oled)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='hmc5883l':
        oled.fill(0)
        picstock.get('menulogo','hmc5883l',40,1).draw(oled)
        picstock.get('menulogo','clock').cropDrawX(0,1,picstock.get('menulogo','clock').w//2,picstock.get('menulogo','clock').w,oled)
        picstock.get('menulogo','photo').cropDrawX(103,1,0,picstock.get('menulogo','photo').w//2,oled)
        picstock.yakitori(31,7,'ccby4','qmc5883l',1,oled)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='photo':
        oled.fill(0)
        picstock.get('menulogo','photo',40,1).draw(oled)
        picstock.get('menulogo','hmc5883l').cropDrawX(0,1,picstock.get('menulogo','hmc5883l').w//2,picstock.get('menulogo','hmc5883l').w,oled)
        picstock.get('menulogo','rmt').cropDrawX(103,1,0,picstock.get('menulogo','rmt').w//2,oled)
        picstock.yakitori(40,7,'ccby4','photos',1,oled)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='rmt':
        oled.fill(0)
        picstock.get('menulogo','rmt',40,1).draw(oled)
        picstock.get('menulogo','photo').cropDrawX(0,1,picstock.get('menulogo','photo').w//2,picstock.get('menulogo','photo').w,oled)
        picstock.get('menulogo','pcimachine').cropDrawX(103,1,0,picstock.get('menulogo','pcimachine').w//2,oled)
        picstock.yakitori(30,7,'ccby4','smarthome',1,oled)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='pcimachine':
        oled.fill(0)
        picstock.get('menulogo','pcimachine',40,1).draw(oled)
        picstock.get('menulogo','rmt').cropDrawX(0,1,picstock.get('menulogo','rmt').w//2,picstock.get('menulogo','rmt').w,oled)
        picstock.get('menulogo','setting').cropDrawX(103,1,0,picstock.get('menulogo','setting').w//2,oled)
        picstock.yakitori(32,7,'ccby4','pcimachine',1,oled)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='setting':
        oled.fill(0)
        picstock.get('menulogo','setting',43,1).draw(oled)
        picstock.get('menulogo','pcimachine').cropDrawX(0,1,picstock.get('menulogo','pcimachine').w//2,picstock.get('menulogo','pcimachine').w,oled)
        picstock.get('otherlogo','pointright',121,4).draw(oled)
        picstock.yakitori(38,7,'ccby4','setting',1,oled)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='showtly':
        oled.fill(0)
        showtly(oled,picstock,accelerometer,fil,gyrospan,2)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='showtemp':
        oled.fill(0)
        showtemp(oled,barometer,picstock)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='showaltitude':
        oled.fill(0)
        showaltitude(oled,barometer,picstock,offset)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='clkout':
        oled.fill(0)
        showclkout(picstock,oled,clktotal,totallistforclk)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='bdsmenu':
        oled.fill(0)
        showbds(gps,oled,picstock)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='choicemenu':
        oled.fill(0)
        showchoicemenu(oled,picstock,accelerometer,fil,menuspan)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='settingmenu':
        oled.fill(0)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        settingmenu_menu.show(picstock,oled)
        oled.show()
    while statemode=='settime':
        oled.fill(0)
        showsettime(picstock,oled,settime_list,settime_pointer)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='systeminfo':
        oled.fill(0)
        picstock.get('otherlogo','na',80,2).draw(oled)
        picstock.yakitori(0,2,'ccby4','shizukuos',1,oled)
        picstock.yakitori(0,3,'ccby4','v1.1',1,oled)
        picstock.yakitori(0,4,'ccby4','made',1,oled)
        picstock.yakitori(0,5,'ccby4','by',1,oled)
        picstock.yakitori(0,6,'ccby4','douergan',1,oled)
        picstock.yakitori(0,7,'ccby4','micropython',1,oled)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        oled.show()
    while statemode=='ledmenu':
        oled.fill(0)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        ledmenu_menu.show(picstock,oled)
        oled.show()
    while statemode=='picmenu':
        oled.fill(0)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        picmenu_menu.show(picstock,oled)
        oled.show()
    while statemode=='pic':
        oled.fill(0)
        showpic(picstock,oled,picpositionY_int,loadpic_str)
        oled.show()
    while statemode=='rmtmenu':
        oled.fill(0)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        rmtmenu_menu.show(picstock,oled)
        oled.show()
    while statemode=='smarthomemenu':
        oled.fill(0)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        smarthome_menu.show(picstock,oled)
        oled.show()
    while statemode=='pcimachinemenu':
        oled.fill(0)
        showtaskbar(picstock,rtc,statemode,tasklist,adc,oled,pinrecharge_read)
        pcimachine_menu.show(picstock,oled)
        oled.show()
