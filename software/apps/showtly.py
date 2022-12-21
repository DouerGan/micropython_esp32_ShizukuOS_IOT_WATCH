from softdrive.function import pixelpo
def showtly(oled,st,sensor,fiter,span,widthpga=1):
    st.yakitori(60,4,'otherlogo',['circle'],0,oled)
    xyz_list=fiter.update(sensor.readXYZ())
    rollandpitch=sensor.RP_calculate(xyz_list[0],xyz_list[1],xyz_list[2])
    b=pixelpo(rollandpitch[0],rollandpitch[1],64,36,span)
    oled.line(b[0]-widthpga,b[1],b[0]+widthpga,b[1],1)
    oled.line(b[0],b[1]-widthpga,b[0],b[1]+widthpga,1)
    st.yakitori(0,6,'ccby4',list('r')+['mh']+list(str(rollandpitch[0])[:4]),1,oled)
    st.yakitori(0,7,'ccby4',list('p')+['mh']+list(str(rollandpitch[1])[:4]),1,oled)
    print(rollandpitch[0],rollandpitch[1])

