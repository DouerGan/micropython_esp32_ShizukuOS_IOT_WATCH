from softdrive.function import pixelpo,getgradient
def showchoicemenu(oled,st,sensor,fiter,span:int):
    st.get('otherlogo','choicemenu',0,1).draw(oled)
    xyz_list=fiter.update(sensor.readXYZ())
    rollandpitch=sensor.RP_calculate(xyz_list[0],xyz_list[1],xyz_list[2])
    b=pixelpo(rollandpitch[0],rollandpitch[1],64,36,span)
    oled.rect(b[0]-12,b[1]-12,25,25,1)
