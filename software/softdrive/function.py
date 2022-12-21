from math import cos,sin,pi,tan,acos
def fill0(needlen:int,fillchar:str,key:str,mode=True):
    if type(key)!=str:
        key=str(key)
    if type(fillchar)!=str:
        fillchar=str(fillchar)
    if len(key)>=needlen:
        return key
    else:
        if mode==True:
            return (needlen-len(key))*fillchar+key
        else:
            return key+(needlen-len(key))*fillchar
def matconv(a,matrix):
    res=[0,0,0]
    for i in range(0,3):
        res[i]=matrix[i][0]*a[0]+matrix[i][1]*a[1]+matrix[i][2]*a[2]
    for i in range(0,3):
        a[i]=res[i]
    return a
def rotate(obj,x,y,z):
    x=x/pi
    y=y/pi
    z=z/pi
    rz=[[cos(z),-sin(z),0],[sin(z),cos(z),0],[0,0,1]]
    ry=[[1,0,0],[0,cos(y),-sin(y)],[0,sin(y),cos(y)]]
    rx=[[cos(x),0,sin(x)],[0,1,0],[-sin(x),0,cos(x)]]
    matconv(matconv(matconv(obj,rz),ry),rx)
def pixelpo(roll:float,pitch:float,x,y,lc:int):
    if pitch>=0:
        yr=y-round(pitch*y/lc)
    else:
        yr=y+round(pitch*(64-y)/(-lc))
    if roll>=0:
        xr=x+round(roll*(128-x)/(lc))
    else:
        xr=x-round(roll*x/(-lc))
    return xr,yr
def getgradient(roll,pitch):
    return acos(1/(((tan(roll)**2)+(tan(pitch)**2)+1)**0.5))
def testprint():
    print('this is test')
def compile(bin1):
    print(len(bin1))
    listrmt1=[9000,4500]
    for bit in bin1:
        if bit=='1':
            listrmt1.extend([646,1643])
        else:
            listrmt1.extend([646,516])
        if len(listrmt1)//2==36:
            listrmt1.extend([646,20000])
    return listrmt1
