import urequest as requests
import ujson
import time
class WebWeather:
    def __init__(self,positioncode:str):
        self.positioncode=positioncode
        self.headers ={"User-Agent":
        '''Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
        AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/102.0.5005.124 Safari/537.36 Edg/102.0.1245.44'''
                  }
        self.data = None
    def getdata(self):
        try:
            response = requests.get(f"http://www.nmc.cn/rest/weather?stationid={self.positioncode}", headers = self.headers)
            data = ujson.loads(response.text)
            self.data = data['data']['predict']['detail']
        except Exception:
            return False
        else:
            return True
    def getNowData(self):
        #night day (风向,风力,天气,温度) 9999 == null
        #微风 a~b级
        #阵雨 多云 大到暴雨 小雨 中雨 大雨 雷阵雨 晴 阴天
        if self.data == None:
            return
        return ((WebWeather.windDecode(self.data[0]['night']['wind']['direct']),self.data[0]['night']['wind']['power'],
                self.data[0]['night']['weather']['info'],self.data[0]['night']['weather']['temperature']),
                (WebWeather.windDecode(self.data[0]['day']['wind']['direct']),self.data[0]['day']['wind']['power'],
                self.data[0]['day']['weather']['info'],self.data[0]['day']['weather']['temperature'])
                )
    @staticmethod
    def windDecode(s):
        if(s=='东北风'):
            return 0
        elif(s=='东风'):
            return 1
        elif(s=='东南风'):
            return 2
        elif(s=='南风'):
            return 3
        elif(s=='西南风'):
            return 4
        elif(s=='西风'):
            return 5
        elif(s=='西北风'):
            return 6
        elif(s=='北风'):
            return 7
        elif(s=='无持续风向'):
            return 8
    def printData(self):
        for d in ('night','day'):
            print(d,end=':\n')
            wind = (self.data[0][d]['wind']['direct'],self.data[0][d]['wind']['power'])
            if(wind[0] != '9999' and wind[1] != '9999'):
                print('风向:',wind[0],'风力:',wind[1])
            else:
                print('已经过去了')
            weather = self.data[0][d]['weather']['info'],self.data[0][d]['weather']['temperature']
            if(weather[0] != '9999' and weather[1] != '9999'):
                print('天气:',weather[0],'温度:',weather[1])
#东西南北多云雷阵雨小中大阴晴
#\u4E1C\u897F\u5357\u5317\u591A\u4E91\u96F7\u9635\u96E8\u5C0F\u4E2D\u5927\u9634\u6674
w=WebWeather('58563')
w.getdata()
w.getNowData()
w.printData()
for i in range(10000):
    time.sleep(0.5)
    w.getdata()
    w.getNowData()
    w.printData()
    print(i)
 