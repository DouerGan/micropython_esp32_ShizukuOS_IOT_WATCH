from softdrive.function import rotate
class CUBE:
    def __init__(self,linelong,x,y,oled) -> None:
        self.cube=[[-linelong,-linelong,-linelong],[-linelong,linelong,-linelong],[linelong,linelong,-linelong],[linelong,-linelong,-linelong],[-linelong,-linelong,linelong],[-linelong,linelong,linelong],[linelong,linelong,linelong],[linelong,-linelong,linelong]]
        self.lineid=[1,2,2,3,3,4,4,1,5,6,6,7,7,8,8,5,8,4,7,3,6,2,5,1]
        self.oled=oled
        self.x=x
        self.y=y
    def draw(self,a=0.1,b=0.2,c=0.3):
        for i in range(0,8):
            rotate(self.cube[i],a,b,c)
        for i in range(0,24,2):
            x1=int(self.x+self.cube[self.lineid[i]-1][0])
            y1=int(self.y+self.cube[self.lineid[i]-1][1])
            x2=int(self.x+self.cube[self.lineid[i+1]-1][0])
            y2=int(self.y+self.cube[self.lineid[i+1]-1][1])
            self.oled.line(x1,y1,x2,y2,1)
            #print(64+cube[lineid[i]-1][0],32+cube[lineid[i]-1][1],64+cube[lineid[i+1]-1][0],32+cube[lineid[i+1]-1][1])



