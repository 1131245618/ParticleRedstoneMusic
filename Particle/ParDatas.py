
import json
from bisect import bisect_left

class ParDatas:

    def __init__(self, datas, channel, tickrate):
        self.datas = {}
        self.channel = channel
        for i in datas:
            tick = 0
            if type(i['tick']) == float:
                tick = round(i['tick']*tickrate)
            elif type(i['tick']) == int:
                tick = i["tick"]
            else:
                raise Exception(f"tick must be float or int, not {type(i['tick'])}")
            self.datas[tick] = i['data']
        self.__tickList = list(self.datas.keys())
        self.__tickList.sort()
    
    def getData(self, tick):
        myList = self.__tickList
        if not(myList and tick >= myList[0]):
            return None
        pos = bisect_left(myList, tick)
        if pos == 0:
            return self.datas[myList[0]]
        if pos == len(myList):
            return self.datas[myList[-1]]
        if tick ==  myList[pos]:
            return self.datas[myList[pos]]
        return self.datas[myList[pos - 1]]
    
    def getDataByTick(self, tick):
        return self.datas.get(tick)


class ParDataLists:

    def __init__(self, data_file_path):
        self.filePath = data_file_path
        self.dataDict = {}
        self.mcfunction_group = {}
        self.data_group = {}
        self.pos = (0, 0, 0)
        self.particle_group = {}
        self.block = {}


    def __iter__(self):
        for channel, datas in self.dataDict.items():
            for i in datas:
                yield channel, i
    
    def getPos(self):
        return self.pos
    
    def getChanData(self, channel, tick):
        return self.dataDict[channel].getData(tick)

    def getChanDataByTick(self, channel, tick):
        return self.dataDict[channel].getDataByTick(tick)

    def getblock(self, channel):
        return self.block.get(f"{channel}", "air 0")

    def load(self):
        
        f = open(self.filePath, "r")
        js = json.loads(f.read())

        self.pos = js["basic"]["position"]
        self.tickrate = int(js["basic"]["tickrate"])
        self.data_group = js["data_group"]
        self.mcfunction_group = js["mcfunction_group"]
        self.particle_group = js["particle_group"]
        self.block = js["block"]

        for key in self.data_group.keys():
            data = self.data_group[key]

            if data["particle_point"] in self.mcfunction_group.keys():
                data['particle_point'] = self.mcfunction_group[data['particle_point']]

            data['particle_line'] = self.particle_group.get(data['particle_line'],{})

        for i in range(16):
            item = js["playEvents"].get(f"{i}", {})
            
            for datas in item:

                if type(datas['data']) == str:
                    datas['data'] = self.data_group.get(datas['data'], {})

                if datas['data']['particle_point'] in self.mcfunction_group.keys():
                    datas['data']['particle_point'] = self.mcfunction_group[datas['data']['particle_point']]

                if type(datas['data']['particle_line']) == str:
                    datas['data']['particle_line'] = self.particle_group.get(datas['data']['particle_line'],{})

            self.dataDict[i] = ParDatas(item, i, self.tickrate)



if __name__ == "__main__":
    data = ParDataLists(r".\data_example.json")
    data.load()
    print(data.getChanData(0,2301)) #you will get something
    #print(data.getChanDataByTick(0,2301)) #None
