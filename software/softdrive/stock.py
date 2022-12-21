from harddrive.sprite import BinloaderFile
from os import listdir
class STOCK():
    def __init__(self,stockdir:list,log=True) -> None:
        self.stockdir={}
        self.stockdir['cache']={}
        for i in stockdir:                             #获得分文件夹
            self.stockdir[i]={}
            for fileadress in listdir('filebin/'+i):#获得分文件夹中的bin文件列表
                self.stockdir[i][fileadress[:-4:]]=BinloaderFile('filebin/'+i+'/'+fileadress)
                if log:
                    print(fileadress)
    def get(self,stock:str,filename:str,x=None,y=None)->int:#获取图像类，设置坐标
        if x!=None and y!=None:
            self.stockdir[stock][filename].setxy(x,y)
        return self.stockdir[stock][filename]

    def gettail(self,stock:str,filename:str)->int:
        return self.stockdir[stock][filename].w+self.stockdir[stock][filename].x

    def yakitori(self,x:int,y:int,stock:str,ya:list,between:int,display)->int:
        px,py=x,y
        for char in ya:
            self.stockdir[stock][char].setxy(px,py)
            self.stockdir[stock][char].draw(display)
            px=px+self.stockdir[stock][char].w+between
        return px
    def getfilelist(self,filepath:str):
        return listdir(filepath)

    def loadintocache(self,filepath:str,filename:str):
        self.stockdir['cache'][filename]=BinloaderFile(filepath+'/'+filename+'.bin')

    def delfromcache(self,filename:str):
        del self.stockdir['cache'][filename]

    def clearcache(self):
        del self.stockdir['cache']
        self.stockdir['cache']={}



