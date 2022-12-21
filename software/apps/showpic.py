def showpic(st,oled,positionY:int,filename):
    oled.fill(0)
    st.get('cache',filename).cropDrawXY(posx=0,posy=0,fromx=0,tox=st.get('cache',filename).w,fromy=positionY,toy=positionY+127,display=oled)
    oled.show()
