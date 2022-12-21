class AVERAGEFITER():
    def __init__(self,lenth:int,samplenum:int) -> None:
        self.valuelist=[]
        self.lenth=lenth
        self.samplenum=samplenum
        for i in range(self.samplenum):
            self.valuelist.append([])
    def update(self,value:tuple):
        for i in range(self.samplenum):
            self.valuelist[i].append(value[i])
        if len(self.valuelist[0])>self.lenth:
            for i in range(self.samplenum):
                self.valuelist[i].pop(0)
                #self.valuelist[i].remove(max(self.valuelist[i]))
                #self.valuelist[i].remove(min(self.valuelist[i]))
        total_list=[0]*self.samplenum
        for i in range(self.samplenum):
            for j in self.valuelist[i]:
                total_list[i]=total_list[i]+j
            total_list[i]/=len(self.valuelist[0])
        return total_list
    def clear(self):
        self.valuelist=[]
        for i in range(self.samplenum):
            self.valuelist.append([])
    def getvalue(self):
        total_list=[0]*self.samplenum
        for i in range(self.samplenum):
            for j in self.valuelist[i]:
                total_list[i]=total_list[i]+j
            total_list[i]/=len(self.valuelist[0])
        return total_list



