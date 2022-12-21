def showsettime(st,oled,settimelist,pointer): #秒分时日星期月年
    po=((0,0),(44,7),(24,7),(92,4),(62,7),(71,4),(35,4))
    st.yakitori(16,2,'midnum',list('20'+str(settimelist[6])+'.'+str(settimelist[5])+'.'+str(settimelist[3])),1,oled)
    st.yakitori(16,5,'midnum',list(str(settimelist[2])+'.'+str(settimelist[1])+'.'+str(settimelist[4])),1,oled)
    st.get('otherlogo','pointon',po[pointer][0],po[pointer][1]).draw(oled)


