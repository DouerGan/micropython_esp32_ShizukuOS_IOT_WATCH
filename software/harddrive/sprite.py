# The MIT License (MIT)

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Author:爱玩游戏的陆千辰
# Video:https://space.bilibili.com/87690728
# Describe:屏幕精灵控制
# Version:v0.51a
# The project deponds on Micropython
# Support: SSD1306(i2c spi) SSH1106(i2c spi)
import framebuf
import math
import time,os
# def getbin(inta: int, x: int) -> int:
#     if x > 0:
#         return (inta >> x) - (inta >> (x + 1)) * 2
#     elif x == 0:
#         return inta - (inta >> 1) * 2
def getbin(inta: int, x: int) -> int:
    return (inta & (1<<x))>>x
def clamp(a,min,max):
    global aa,bb,cc
    if max < min:
        return min
    if a>max:
        return min
    elif a<min:
        return max
    else:
        return a
def getPageLen2(num: int) -> int:
    temp = num >> 3
    if (num == temp << 3):
        return temp
    else:
        return temp + 1
def getPageLen(num: int) -> int:
    temp = num >> 3
    if (num & 7):
        return temp + 1
    else:
        return temp
def DataScale(data,scale):
    re = []
    inv = False
    if scale == 0:
        return re
    if scale < 0:
        scale = - scale
        inv = True
    scale = len(data)/(scale*len(data))
    i = 0
    while  math.ceil(i) < len(data):
        re.append(data[math.ceil(i)])
        i += scale
    if inv:
        re.reverse()
    return re
def fillBlock(display,x,y,width = 8,value = 1):
    if(value):
        display.buffer[x+y*128:x+width+y*128] = bytearray(b'\xff'*width)
    else:
        display.buffer[x+y*128:x+width+y*128] = bytearray(width)
def bmpdecode(filename,newname = None,biasY = 0,limit=128,log=True,InvertColor=False,delAfterDecode = False):
    f=open(filename, 'rb')
    if f.read(2) == b'BM':  #header
        dummy = f.read(8) #file size(4), creator bytes(4)
        offset = int.from_bytes(f.read(4), 'little')
        hdrsize = int.from_bytes(f.read(4), 'little')
        width = int.from_bytes(f.read(4), 'little')
        height = int.from_bytes(f.read(4), 'little')
        if int.from_bytes(f.read(2), 'little') == 1: #planes must be 1
            depth = int.from_bytes(f.read(2), 'little')
            if depth == 24 and int.from_bytes(f.read(4), 'little') == 0:#compress method == uncompressed
                print("Image size:", width, "x", height)
                rowsize = (width * 3 + 3) & ~3
                if height < 0:
                    height = -height
                    flip = False
                else:
                    flip = True
                #display._setwindowloc((posX,posY),(posX+w - 1,posY+h - 1))
                row = 0
                if newname == None:
                    newname = filename[:-4]
                buff = open(newname+'.bin','wb+')
                buff.write(b'\x22\x01')
                buff.write(width.to_bytes(2,'little'))
                buff.write((getPageLen(height)*8).to_bytes(2,'little'))
                temp = [0]*width
                temp2 = height - 1+ biasY
                if(InvertColor):
                    while row < height:
                        if(row != 0 and row % 8 == 0):
                            buff.write(bytearray(temp))
                            temp = [0]*width
                        if flip:
                            pos = offset + ( temp2 - row ) * rowsize
                        else:
                            pos = offset + (row + biasY)* rowsize
                        if f.tell() != pos:
                            f.seek(pos)
                        col = 0
                        while col < width:
                            bgr = f.read(3)
                            gray = (bgr[2]*77+ bgr[1]*151+bgr[0]*28)>>8
                            #(R*77+G*151+B*28)>>8
                            if(gray<=limit):
                                data = 128 # 1<<7
                            else:
                                data = 0
                            temp[col] = (temp[col]>>1)+data
                            col = col+ 1
                        row = row+1
                        if log:
                            print("decoding :%d%%"%(row*100//height))
                else:# 空间换时间 本质一个if
                    while row < height:
                        if(row != 0 and row % 8 == 0):
                            buff.write(bytearray(temp))
                            temp = [0]*width
                        if flip:
                            pos = offset + ( temp2 - row ) * rowsize
                        else:
                            pos = offset + (row + biasY)* rowsize
                        if f.tell() != pos:
                            f.seek(pos)
                        col = 0
                        while col < width:
                            bgr = f.read(3)
                            gray = (bgr[2]*77+ bgr[1]*151+bgr[0]*28)>>8
                            #(R*77+G*151+B*28)>>8
                            if(gray>limit):
                                    data = 128 # 1<<7
                            else:
                                data = 0
                            temp[col] = (temp[col]>>1)+data
                            col = col+ 1
                        row = row+1
                        if log:
                            print("decoding :%d%%"%(row*100//height))
    else:
        raise TypeError("Type not support")
    shift = height % 8
    if(shift != 0):
        shift = (8 - shift)
        i = 0
        while i < len(temp):
            temp[i] = temp[i] >> shift
            i+=1
    buff.write(bytearray(temp))
    f.close()
    buff.close()
    if(delAfterDecode):
        os.remove(filename)
    print('Encode Finish save to: '+newname+'.bin')
    return BinloaderFile(newname+'.bin')
def qr2frame(matrix,savename = "QRCode.bin"):
    buff = open(savename,'wb')
    buff.write(b'\x22\x01')
    boxSize = len(matrix)
    buff.write(boxSize.to_bytes(2,'little'))

    boxHigh = getPageLen(boxSize)
    buff.write((boxHigh*8).to_bytes(2,'little'))
    i = 0
    data = [0] * boxSize
    while i<boxSize:
        j = 0
        if(i != 0 and i % 8 == 0):
            buff.write(bytearray(data))
            data = [0]*boxSize

        while j < boxSize:
            data[j] = data[j]>>1
            if(matrix[i][j]):
                data[j] = data[j]+128
            j = j+1
        i = i+1
    shift = (8 - boxSize % 8)
    if(shift != 0):
        i = 0
        while i < boxSize:
            data[i] = data[i] >> shift
            i+=1
    buff.write(bytearray(data))
    buff.close()
    return BinloaderFile(savename)
def qr2frameSize2(matrix,savename = "QRCode.bin"):
    buff = open(savename,'wb')
    buff.write(b'\x22\x01')
    boxSize = len(matrix)*2
    buff.write(boxSize.to_bytes(2,'little'))

    boxHigh = getPageLen(boxSize)
    buff.write((boxHigh*8).to_bytes(2,'little'))
    i = 0
    data = [0] * boxSize
    while i<boxSize:
        j = 0
        if(i != 0 and i % 8 == 0):
            buff.write(bytearray(data))
            data = [0]*boxSize

        while j < boxSize:
            data[j] = data[j]>>1
            if(matrix[i//2][j//2]):
                data[j] = data[j]+128
            j = j+1
        i = i+1
    shift = boxSize % 8
    if(shift != 0):
        i = 0
        while i < boxSize:
            data[i] = data[i] >> shift
            i+=1
    buff.write(bytearray(data))
    buff.close()
    return BinloaderFile(savename)
class __fframe:
    def draw(self, display, has_transform: bool = False):
        try:
            w = display.width
        except AttributeError:
            w = display.w
        deltaY = getPageLen(self.h)

        try:
            posx = clamp(self.x,0,display.width - self.w)
            posy = clamp(self.y,0,deltaY)
        except AttributeError:
            posx = clamp(self.x,0,display.w - self.w)
            posy = clamp(self.y,0,deltaY)
        start = posx + 128 * posy
        i = 0
        drawW = min(self.w,w)
        drawH = min(deltaY,display.pages)
        # maxSize = len(display.buffer)
        temp = start
        if has_transform:
            while i<drawH:
                j = 0
                while j < drawW:
                    display.buffer[temp+j] |= self.data[i * self.w + j]
                    j+=1
                i+=1
                temp += 128
            return
        else:
            while i<drawH:
                display.buffer[temp:temp+drawW] = self.data[i * self.w:i * self.w + drawW]
                i+=1
                temp += 128
            return
    def setxy(self, x=None, y=None):
        if x != None:
            self.x = x
        if y != None:
            self.y = y
    def cropDrawX(self,posx,posy,fromx,tox,display):
        try:
            w,h = display.width,display.height
        except AttributeError:
            w,h = display.w,display.h
        if tox > self.w:
            tox = self.w
        temp = getPageLen(h)
        maxH = getPageLen(self.h)
        if maxH>temp:
            maxH = temp
        ax = clamp(posx,0,w - (tox - fromx))
        ay = clamp(getPageLen(posy),0,temp - maxH)
        start = ax + 128 * ay
        drawW = min(tox-fromx,w)
        if drawW > w:
            drawW = w
        i = 0
        temp = fromx
        while i<maxH:
            display.buffer[start:start+drawW] = self.data[temp:temp + drawW]
            i+=1
            start += 128
            temp += self.w
    def cropDrawXY(self,posx,posy,fromx,tox,fromy,toy,display,has_transform: bool = False):
        try:
            w,h = display.width,display.height
        except AttributeError:
            w,h = display.w,display.h
        deltaY = getPageLen(toy - fromy)
        deltaX = tox - fromx
        temp = getPageLen(h)
        deltaY = min(temp,deltaY)
        deltaX = min(w,deltaX)
        posx = clamp(posx,0,w - deltaX)
        posy = clamp(posy,0,temp - deltaY)
        start = posx + 128 * posy
        i = 0
        di = getPageLen(fromy)
        temp = start
        temp2 = di * self.w + fromx
        # maxData = len(display.buffer)
        if has_transform:
            while i<deltaY:
                if temp2 + deltaX> len(self.data):
                    return
                j = 0
                while j<deltaX:
                    display.buffer[temp+j] |= self.data[temp2+ j]
                    j+=1
                i+=1
                temp += 128
                temp2 += self.w
            return
        else:
            while i<deltaY:
                if temp2 + deltaX> len(self.data):
                    return
                display.buffer[temp:temp+deltaX] = self.data[temp2:temp2+ deltaX]
                i+=1
                temp += 128
                temp2 += self.w
            return

class framebufPic(__fframe):
    def __init__(self, display):
        try:
            self.w = display.width
            self.h = display.height
        except AttributeError:
            self.w = display.w
            self.h = display.h
        self.buffer = bytearray(display.pages * self.w)
        self.data = framebuf.FrameBuffer1(self.buffer, self.w, self.h)
        self.x, self.y = 0, 0

class BinloaderMem(__fframe):
    def __init__(self, filename, x = 0, y= 0):
        self.x, self.y = x, y
        f = open(filename, "rb")
        temp = f.read(6)
        self.w = temp[2] + (temp[3] << 8)
        self.h = temp[4]
        self.data = f.read()
        f.close()

class BinloaderFile(__fframe):
    def __init__(self, filename, x =0, y =0):
        self.x, self.y = x, y
        self.f = open(filename, "rb")
        temp = self.f.read(6)
        self.w = temp[2] + (temp[3] << 8)
        self.h = temp[4]
    def draw(self, display, has_transform: bool = False):
        try:
            w = display.width
        except AttributeError:
            w = display.w
        deltaY = getPageLen(self.h)

        try:
            posx = clamp(self.x,0,display.width - self.w)
            posy = clamp(self.y,0,display.height - deltaY)
        except AttributeError:
            posx = clamp(self.x,0,display.w - self.w)
            posy = clamp(self.y,0,display.h - deltaY)
        start = posx + 128 * posy
        i = 0
        drawW = min(self.w,w)
        drawH = min(deltaY,display.pages)
        # maxSize = len(display.buffer)
        temp = start
        if has_transform:
            while i<drawH:
                j = 0
                self.f.seek(i * self.w+6)
                while j < drawW:
                    display.buffer[temp+j] |= int.from_bytes(self.f.read(1),'big')
                    j+=1
                i+=1
                temp += 128
            return
        else:
            while i<drawH:
                self.f.seek(i * self.w+6)
                da = self.f.read(drawW)
                if(da):
                    display.buffer[temp:temp+drawW] = da
                else:
                    display.buffer[temp:temp+drawW] = bytearray(drawW)
                i+=1
                temp += 128
            return
    def cropDrawX(self,posx,posy,fromx,tox,display):
        try:
            w,h = display.width,display.height
        except AttributeError:
            w,h = display.w,display.h
        if tox > self.w:
            tox = self.w
        temp = getPageLen(h)
        maxH = getPageLen(self.h)
        if maxH>temp:
            maxH = temp
        ax = clamp(posx,0,w - (tox - fromx))
        ay = clamp(getPageLen(posy),0,temp - maxH)
        start = ax + 128 * ay
        drawW = min(tox-fromx,w)
        if drawW > w:
            drawW = w
        i = 0
        temp = fromx
        while i<maxH:
            self.f.seek(temp+6)
            display.buffer[start:start+drawW] = self.f.read(drawW)# self.data[temp:temp + drawW]
            i+=1
            start += 128
            temp += self.w
    def cropDrawXY(self,posx,posy,fromx,tox,fromy,toy,display,has_transform: bool = False):
        try:
            w,h = display.width,display.height
        except AttributeError:
            w,h = display.w,display.h
        deltaY = getPageLen(toy - fromy)
        deltaX = tox - fromx
        temp = getPageLen(h)
        deltaY = min(temp,deltaY,self.h)
        deltaX = min(w,deltaX,self.w)
        posx = clamp(posx,0,w - deltaX)
        posy = clamp(posy,0,temp - deltaY)
        start = posx + 128 * posy
        i = 0
        di = getPageLen(fromy)
        temp = start
        temp2 = di * self.w + fromx
        # maxData = len(display.buffer)
        if has_transform:
            while i<deltaY:
                self.f.seek(temp2+6)
                j = 0
                while j<deltaX:
                    display.buffer[temp+j] |= int.from_bytes(self.f.read(1),'big')
                    j+=1
                i+=1
                temp += 128
                temp2 += self.w
            return
        else:
            while i<deltaY:
                self.f.seek(temp2+6)
                display.buffer[temp:temp+deltaX] = self.f.read(deltaX)
                i+=1
                temp += 128
                temp2 += self.w
            return
    def __del__(self):
        self.f.close()
class rhombus8:
    def __init__(self, x: int, y: int, r: int, width: int = None, select: int = None):
        #       *2
        #    *1    *3
        #  *0    C   *4
        #    *7    *5
        #       *6
        # draw_rhombus8_box(display,68,32,20,5,0xf0)  //Old
        self.data = [(x - r, y),
                     (x - (r >> 1), y - (r >> 1)),
                     (x, y - r),
                     (x + (r >> 1), y - (r >> 1)),
                     (x + r, y),
                     (x + (r >> 1), y + (r >> 1)),
                     (x, y + r),
                     (x - (r >> 1), y + (r >> 1)),
                     ]

        self.select = select
        self.r = r
        self.x = x
        self.y = y
        self.t = "        "
        if width is None:
            self.width = self.r >> 1
        else:
            self.width = width

    def setxy(self, x=None, y=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y

    def setText(self, t: str):
        self.t = t

    def setSelect(self, s):
        self.select = s

    def draw(self, display):
        if self.select is None:
            for i in range(8):
                display.rect(self.x + self.data[i][0] - self.width, self.y + self.data[i][1] - self.width,
                             self.width << 1,
                             self.width << 1, 1)
                if self.t[i] != " ":
                    display.text(self.x + self.t[i], self.y + self.data[i][0] - (self.width - 2),
                                 self.data[i][1] - (self.width - 2), 1)
        else:
            for i in range(8):
                if getbin(self.select, i):
                    display.fill_rect(self.x + self.data[i][0] - self.width, self.y + self.data[i][1] - self.width,
                                      self.width << 1,
                                      self.width << 1, 1)
                    if self.t[i] != " ":
                        display.text(self.x + self.t[i], self.y + self.data[i][0] - (self.width - 2),
                                     self.data[i][1] - (self.width - 2),
                                     0)
                else:
                    display.rect(self.x + self.data[i][0] - self.width, self.y + self.data[i][1] - self.width,
                                 self.width << 1,
                                 self.width << 1, 1)
                    if self.t[i] != " ":
                        display.text(self.t[i], self.x + self.data[i][0] - (self.width - 2),
                                     self.y + self.data[i][1] - (self.width - 2),
                                     1)

class TextFullUI:
    def __init__(self, x=0, y=0,w = 16,h = 6):
        self.w = w
        self.h = h
        self.texts = ['']*self.h
        self.isCenter = [False]*self.h
        self.__pointer = 0
        self.x, self.y = x, y

    def AddLine(self, t: str,isCenter = False):
        i = 0
        while i < len(t):
            if self.__pointer < self.h:
                self.texts[self.__pointer] = t[i:i + self.w]
                self.isCenter[self.__pointer] = isCenter
                self.__pointer += 1

            else:
                temp = self.__pointer -1
                del self.texts[0]
                self.texts.append(t[i:i + self.w])
                del self.isCenter[0]
                self.isCenter.append(isCenter)
            i += 16

    def clear(self):
        self.texts = ['']*self.h
        self.__pointer = 0

    def seek(self, p):
        self.__pointer = p
        return self.__pointer
    def tell(self):
        return self.__pointer
    def draw(self, display):
        i = 0
        while i < self.h:
            if(self.isCenter[min(self.h-1,i)]):
                 display.text(self.texts[i], 64-len(self.texts[i])*4, self.y + i * 10, 1)
            else:
                display.text(self.texts[i], self.x, self.y + i * 10, 1)
            i += 1

class TextSelectUI:
    def __init__(self, x=0, y=0,w = 16,h = 6,deltaY = 9):
        self.x, self.y = x, y
        self.selectIndex = 0
        self.text= []
        self.data = []
        self.deltaY = deltaY
        self.selectH = 1
        self.w = w
        self.h = h
        self.start = 0
        self.nowLine = 0
        # self.end = self.start + self.h
    def SetText(self,data):
        self.text = []
        self.data = []

        for d in data:
            if(len(d))<self.w:
                self.text.append(d)
                self.data.append(1)
            else:
                i = 0
                CeilLen = 0
                while i <len(d):
                    self.text.append(d[i:i+min(len(d)-i,self.w)])
                    i += self.w
                    CeilLen += 1
                self.data.append(CeilLen)
    def NextIndex(self):
        self.selectIndex += 1
        # 返回
        if(self.selectIndex >= len(self.data)):
            self.selectIndex = 0
            self.start = 0
            self.nowLine = 0
            return
        self.nowLine += self.data[self.selectIndex]
        if(self.nowLine>self.start+self.h):
            self.start = self.nowLine-self.h
    def LastIndex(self):
        self.nowLine -= self.data[self.selectIndex]
        self.selectIndex -= 1
        # 返回
        if(self.selectIndex < 0):
            self.selectIndex = len(self.data) - 1
            self.nowLine = len(self.text) - 1
            self.start = self.nowLine - min(self.h,len(self.text)-1)
            return
        if(self.nowLine<self.start):
            self.start = self.nowLine - self.data[self.selectIndex] + 1
    def draw(self, display):
        loop = 0 # 能画几行
        start = self.start # 行数开始
        end = min(self.h+1,len(self.text))
        while loop < end:
            display.text(self.text[loop+start], self.x, self.y + loop *self.deltaY, 1)
            if(loop+start == self.nowLine):
                display.fill_rect(120, self.y + loop *self.deltaY,8,8,1)
            loop += 1

class DataDisplayScreen:
    def __init__(self, delta=5, length=128, x=0, y=32,width = 1,height = 1):
        self.data = []
        self.len = (length/delta)
        if(self.len <= 0):self.len = 128
        self.delta = delta if delta > 1 else 1
        self.height = height
        self.x = x
        self.y = y
        self.width = width
    def __add__(self, other):
        if len(self.data) >= self.len:
            self.data.pop(0)
        self.data.append(other)
        return self
    def AutoHeight(self):
        self.height = min(abs((self.y-1)/max(self.data)),abs((63-self.y)/min(self.data)))
    def draw(self, display):
        if len(self.data) <= 1:
            return
        i = 0
        while i < len(self.data) - 1:
            display.line(self.x+ i*self.delta,round(-self.data[i]*self.height)+self.y,
                         self.x+(i+1)*self.delta,round(-self.data[i+1]*self.height)+self.y,
                         self.width)
            i += 1
class AnimatePics:
    def __init__(self,frameList,x = 0,y = 0,isLoop= True,dt = 50):
        self.framList = frameList
        self.isLoop = isLoop
        self.index = 0
        self.x = x
        self.y = y
        self.dt = dt
        self.lastDrawTime = 0
    def draw(self,display):
        temp = time.ticks_ms()
        if temp - self.lastDrawTime > self.dt:
            self.lastDrawTime = temp
            if(self.index == len(self.framList) - 1):
                if(self.isLoop):
                    self.index = 0
            else:
                self.index += 1
        self.framList[self.index].setxy(self.x,self.y)
        self.framList[self.index].draw(display)
class CloseAni:
    def __init__(self,display) -> None:
        self.isFinished = False
        try:
            self.h = display.h
            self.w = display.w
        except Exception:
            self.h = display.height
            self.w = display.width
        self.index = 0
    def draw(self,display):
        if self.isFinished:
            return
        display.line(0,self.index,self.w,self.index,0)
        display.line(0,self.index+1,self.w,self.index+1,1)
        display.line(0,self.h-self.index,self.w,self.h-self.index,0)
        display.line(0,self.h-self.index-1,self.w,self.h-self.index-1,1)
        self.index += 1
        if self.index == self.h//2:
            self.isFinished = True
            display.fill(0)
def chsC2enc(d):
    if 0x4e00<=d<=0x9fa5 or d < 128:
        return d
    if(d == 0xff0c):
        return 0x2c
    elif(d == 0x3002):
        return 0x2e
    elif(d == 0xff1a):
        return 0x3b
    elif(d == 0x201c or d == 0x201d):
        return 0x22
    elif(d == 0x2019 or d == 0x2018):
        return 0x27
    elif(d == 0x3010):
        return 0x5b
    elif(d == 0x3011):
        return 0x5d
    elif(d == 0xff08):
        return 0x28
    elif(d == 0xff09):
        return 0x29
    elif(d==0xff1b):
        return 0x3b
    elif(d == 0x3001):
        return 0xb7
    elif(d == 0xff01):
        return 0x21
    print(d,chr(d))
class SpriteFont16:
    def __init__(self,filename) -> None:
        self.bias = 0x4e00
        #self.end = 0x9fa5
        self.f = open(filename,'rb')
        if(self.f.read(3) != b'f16'):
            raise TypeError("!!!Font not support!!!")
    def text(self,x,y,data,display,width = 17):
        i = 0
        p = 0
        for d in data:
            #print(d)
            d = ord(d)
            d = chsC2enc(d)
            if 0< d <128:
                self.f.seek((d)*32 +3)
            elif d> 0x4e00:
                self.f.seek((d-self.bias+128)*32 +3)
            fromD = x+y*128+i
            if(fromD+144 > 128*8):
                break
            display.buffer[fromD:fromD+16] = self.f.read(16)
            display.buffer[fromD+128:fromD+144] = self.f.read(16)

            i = i+width
            if i> 128 - width + 256 * p:
                #print(i)
                p += 1
                i = 256 *p
# class AniLineX:
#     def __init__(self,frame,to_xs:list,speed:int = 1,dt = 0.3,isloop = False):
#         self.frame = frame
#         self.frame.x = to_xs[0]
#         self.tox = to_xs[1]
#         self.to_xs = to_xs
#         self.isEnd = False
#         self.isloop = isloop
#         self.speed = speed
#         self.dt = dt
#     def draw(self,display):
#         self.frame.draw(display)
#         if(self.isEnd):
#             return
#         temp = self.frame.x + self.speed
