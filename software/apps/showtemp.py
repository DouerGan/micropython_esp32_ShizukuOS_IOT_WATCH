def showtemp(oled,barometer,stock):
        press=barometer.getPress()
        stock.get('menulogo','temp',15,3).cropDrawX(5,3,0,26,oled)
        stock.yakitori(35,3,'midnum',list(str(press)[:6]+'p'),1,oled)
        stock.get('otherlogo','pointright',121,4).draw(oled)
        stock.get('otherlogo','pointleft',0,4).draw(oled)
