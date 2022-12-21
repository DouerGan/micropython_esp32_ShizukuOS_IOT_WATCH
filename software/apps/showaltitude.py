def showaltitude(oled,barometer,stock,offset):
        altitude=barometer.getAltitude()
        stock.get('menulogo','temp',12,3).cropDrawX(5,2,26,stock.get('menulogo','temp').w,oled)
        stock.yakitori(45,4,'midnum',list(str(altitude-offset)[:5]+'m'),1,oled)
        stock.get('otherlogo','pointright',121,4).draw(oled)
        stock.get('otherlogo','pointleft',0,4).draw(oled)
