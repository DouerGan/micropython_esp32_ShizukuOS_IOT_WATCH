from apps.showlittletime import showlittletime
from machine import Pin
def showtaskbar(st,rtc,state:str,tasklist:list,adcvalue:list,oled,rechargepin:Pin):
    fullcell=4.1
    undercell=3.4
    startpixel=0
    if state!='menu':
        startpixel=showlittletime(rtc,oled,st,0,0)
    width=round((adcvalue[0]-undercell)/(fullcell-undercell)*16)
    st.yakitori(startpixel,0,'otherlogo',tasklist,1,oled)
    if rechargepin.value():
        st.get('otherlogo','cell',x=105,y=0).draw(oled)
        oled.fill_rect(107,2,width,3,1)
    else:
        st.get('otherlogo','cellrecharge',x=105,y=0).draw(oled)

