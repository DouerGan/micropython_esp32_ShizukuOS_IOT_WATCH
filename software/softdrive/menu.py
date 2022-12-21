from harddrive.ssd1306 import SSD1306_SPI
class POINT:
    def __init__(self,title:str,st,modelist:list,irq:function,ischange:bool,priority=True):#True为图标类，False为数值类
        self.title=title
        self.modelist=modelist
        self.pointer=0
        self.pitchout=False
        self.irq=irq
        self.st=st
        self.ischange=ischange
        self.priority=priority
    def change(self):
        if self.priority==True:
            self.pointer+=1
            if self.pointer==len(self.modelist):
                self.pointer=0
            self.irq()
        else:
            self.irq()
            self.pointer+=1
            if self.pointer==len(self.modelist):
                self.pointer=0
    def pitchoff(self):
        self.pitchout=False
    def pitchon(self):
        self.pitchout=True
#_____________________________________________________________________________________________
#_____________________________________________________________________________________________
class MENU:
    def __init__(self,pointlist:list,window_w:int):
        self.pointlist=pointlist
        if window_w>=len(self.pointlist):
            self.window_w=len(self.pointlist)
        else:
            self.window_w=window_w
        self.window=self.pointlist[0:self.window_w]
        self.windowstart=0
        self.windowover=6
        self.pointer=0
        self.roll=window_w<len(self.pointlist)
        self.window[self.pointer].pitchon()
    def do(self):
        self.window[self.pointer].change()
    def up(self):
        self.window[self.pointer].pitchoff()
        self.pointer-=1
        if self.pointer==-1:
            if self.roll:
                self.pointer=0
                self.windowstart-=1
                if self.windowstart==-1:
                    self.windowstart=len(self.pointlist)-1
                self.window.pop()
                self.window.insert(0,self.pointlist[self.windowstart])
                self.windowover=self.pointlist.index(self.window[-1])
            else:
                self.pointer+=1
        self.window[self.pointer].pitchon()
    def down(self):
        self.window[self.pointer].pitchoff()
        self.pointer+=1
        if self.pointer==len(self.window):
            if self.roll:
                self.pointer=len(self.window)-1
                self.windowover+=1
                if self.windowover==len(self.pointlist):
                    self.windowover=0
                self.window.pop(0)
                self.window.append(self.pointlist[self.windowover])
                self.windowstart=self.pointlist.index(self.window[0])
            else:
                self.pointer-=1
        self.window[self.pointer].pitchon()
    def show(self,st,oled:SSD1306_SPI):
        a=0
        for point in self.window:
            a+=1
            st.yakitori(2,a,'ccby4',list(point.title),1,oled)
            if point.ischange==True:
                st.get('otherlogo',point.modelist[point.pointer],107,a).draw(oled)
            else:
                st.yakitori(105,a,'ccby4',list(point.modelist[point.pointer]),1,oled)
            if point.pitchout:
                #st.get('otherlogo','point',3,a).draw(oled)
                oled.rect(0,a*8-2,128,10,1)

