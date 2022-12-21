def showbds(gps,oled,st):
    if gps.mode==0:
        st.yakitori(0,3,'ccby4',list('bds')+['space']+list('is')+['space']+list('off'),1,oled)
        st.yakitori(0,4,'ccby4',list('press')+['space']+list('sure')+['space']+list('to')+['space']+list('on'),1,oled)
    else:
        gps.getinf()
        oled.text(gps.getlongitude(),0,15,1)
        oled.text(gps.getlatitude(),0,25,1)
        oled.text(gps.getplace(),0,35,1)
        oled.text(gps.getspeed(),0,45,1)
