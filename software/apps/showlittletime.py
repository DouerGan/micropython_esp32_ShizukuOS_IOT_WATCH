def showlittletime(rtc,oled,ku,x,y):#显示时间
    nowtime=rtc.gettime() #秒 分 时 日 星期 月 年
    if len(nowtime[2])==2:#0  1  2  3   4   5  6
        ku.yakitori(x,y,'ccby4',[nowtime[2][0],nowtime[2][1],'mh'],1,oled)
    else:
        ku.yakitori(x,y,'ccby4',[nowtime[2],'mh'],0,oled)
    if len(nowtime[1])==2:
        return ku.yakitori(ku.gettail('ccby4','mh')+1,y,'ccby4',nowtime[1],1,oled)
    else:
        return ku.yakitori(ku.gettail('ccby4','mh')+1,y,'ccby4',['0',nowtime[1]],1,oled)
