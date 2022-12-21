def showclkout(st,oled,clktotal:list,total:list):
    st.yakitori(20,1,'midnum',list(str(clktotal[0]))+['.']+list(str(clktotal[1]))+['.']+list(str(clktotal[2]))+['.']+list(str(clktotal[3])[:2]),1,oled)
    st.yakitori(0,3,'ccby4',['point']+list(str(total[4][0]))+['mh']+list(str(total[4][1]))+['mh']+list(str(total[4][2]))+['mh']+list(str(total[4][3])[:2]),1,oled)
    st.yakitori(0,4,'ccby4',['point']+list(str(total[3][0]))+['mh']+list(str(total[3][1]))+['mh']+list(str(total[3][2]))+['mh']+list(str(total[3][3])[:2]),1,oled)
    st.yakitori(0,5,'ccby4',['point']+list(str(total[2][0]))+['mh']+list(str(total[2][1]))+['mh']+list(str(total[2][2]))+['mh']+list(str(total[2][3])[:2]),1,oled)
    st.yakitori(0,6,'ccby4',['point']+list(str(total[1][0]))+['mh']+list(str(total[1][1]))+['mh']+list(str(total[1][2]))+['mh']+list(str(total[1][3])[:2]),1,oled)
    st.yakitori(0,7,'ccby4',['point']+list(str(total[0][0]))+['mh']+list(str(total[0][1]))+['mh']+list(str(total[0][2]))+['mh']+list(str(total[0][3])[:2]),1,oled)
    st.get('otherlogo','duck',85,4).draw(oled)
