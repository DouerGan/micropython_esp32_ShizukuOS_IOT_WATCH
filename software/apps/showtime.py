def showtime(rtc,oled,ku):#显示时间
    nowtime=rtc.gettime() #秒 分 时 日 星期 月 年
    weekdir=['sun','mon','tue','wed','thu','fri','sat']
    if len(nowtime[2])==2:#0  1  2  3   4   5  6
        ku.yakitori(1,2,'bignum',[nowtime[2][0],nowtime[2][1],'mh'],1,oled)
    else:
        ku.yakitori(1,2,'bignum',['space',nowtime[2],'mh'],0,oled)
    if len(nowtime[1])==2:
        ku.yakitori(ku.gettail('bignum','mh')+1,2,'bignum',nowtime[1],1,oled)
    else:
        ku.yakitori(ku.gettail('bignum','mh')+1,2,'bignum',['0',nowtime[1]],1,oled)
    ku.yakitori(0,7,'ccby4',f"20{nowtime[6]}-{nowtime[5]}-{nowtime[3]}-{weekdir[int(nowtime[4])]}",1,oled)
