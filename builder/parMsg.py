from builder.noteMsg import MsgList
from builder import ParDatas, sequence2, util, particleLine, line_util
import configparser


class parMsgList(MsgList):

    def __init__(self, *args, **keys):
        super().__init__(*args, **keys)
        self.parMsgDict = {}
        for i in range(16):
            self.parMsgDict[i] = {}
        self.particleSpeed = 0.5
        self.seq = sequence2.Seq2()
        self.length = 0
        self.data = None

    def load(self, file, data_file_path, tickrate=20.0, makeLength=True, makePitch=True):
        super().load(file, tickrate, makeLength, makePitch)
        self.data = ParDatas.ParDataLists(data_file_path)
        self.data.load()

        for item in self:
            rsTick = item.tick
            for msg in item.msgs.msgs:
                if msg.velocity >= 0:
                    sTick = rsTick
                    note = msg.note
                    if msg.velocity > 0:

                        px, py, pz = self.data.getPos()

                        if not self.parMsgDict[msg.channel].__contains__(rsTick):
                            self.parMsgDict[msg.channel][rsTick] = []
                            self.parMsgDict[msg.channel][rsTick].append(
                                (px + sTick * self.particleSpeed, py, pz + note))

                        else:
                            self.parMsgDict[msg.channel][rsTick].append(
                                (px + sTick * self.particleSpeed, py, pz + note))

                        lastRsTick = rsTick
        self.length = lastRsTick

    def buildParticle(self):

        for channel in range(0,16):

            last_pos = []
            last_tick = 0
            line_type = "normal"
            line_func = util.noFunc
            last_func = None
            posAndAddedValues = []

            for tick in range(0, self.length + 1):

                temp = self.data.getChanDataByTick(channel, tick)
                if temp:

                    line_func = particleLine.getfunc(temp["particle_line"]["name"])
                    if last_func != line_func:
                        print(last_func, line_func)
                        posAndAddedValues = []#若函数改变，将附加值清空
                    line_type = particleLine.getfuncType(temp["particle_line"]["name"])
                    last_func = line_func
                    keyargs = temp["particle_line"]["args"]

                if self.parMsgDict[channel].__contains__(tick):
                    this_pos = self.parMsgDict[channel][tick]
                    if last_pos:
                        #开始计算线段
                        if line_type == "normal":
                            linkedLines = util.link(last_pos, this_pos)
                            for pos1, pos2 in linkedLines:
                                (x1, y1, z1), (x2, y2, z2) = pos1, pos2
                                cmdlines = line_func(x1, y1, z1, x2, y2, z2, ticks = tick - last_tick, **keyargs)
                                for i, cmdLine in enumerate(cmdlines):
                                    for cmd in cmdLine:
                                        self.seq.findByTick(last_tick+i).addCmd(cmd)
                                        
                        elif line_type == "ex":
                            linkedLines = util.link(last_pos, this_pos)
                            for pos1, pos2 in linkedLines:
                                (x1, y1, z1), (x2, y2, z2) = pos1, pos2
                                cmd= line_func(x1, y1, z1, x2, y2, z2, **keyargs)
                                self.seq.findByTick(last_tick).addCmd(cmd)

                        elif line_type == "added":
                            if not posAndAddedValues:
                                linkedLines = util.link(last_pos, this_pos)
                                temp = []
                                for i in linkedLines:
                                    temp.append(i+(None,))
                                linkedLines = temp
                            else:
                                linkedLines = util.linkWithAdded(posAndAddedValues, this_pos)
                            posAndAddedValues = []
                            for pos1, pos2, addedVal in linkedLines:
                                (x1, y1, z1), (x2, y2, z2) = pos1, pos2
                                cmdlines, other = line_func(x1, y1, z1, x2, y2, z2, addedVal,  ticks = tick - last_tick, **keyargs)
                                posAndAddedValues.append(((x2,y2,z2), other))
                                for i, cmdLine in enumerate(cmdlines):
                                    for cmd in cmdLine:
                                        self.seq.findByTick(last_tick+i).addCmd(cmd)

                        elif line_type == "exadded":
                            if not posAndAddedValues:
                                linkedLines = util.link(last_pos, this_pos)
                                temp = []
                                for i in linkedLines:
                                    temp.append(i+(None,))
                                linkedLines = temp
                            else:
                                linkedLines = util.linkWithAdded(posAndAddedValues, this_pos)
                            posAndAddedValues = []
                            for pos1, pos2, addedVal in linkedLines:
                                (x1, y1, z1), (x2, y2, z2) = pos1, pos2
                                cmd, other = line_func(x1, y1, z1, x2, y2, z2, addedVal, **keyargs)
                                posAndAddedValues.append(((x2,y2,z2), other))
                                self.seq.findByTick(last_tick).addCmd(cmd)
                            
                    last_pos = this_pos
                    last_tick = tick
            
            last_pos = []


    def buildNotes(self):
        for item in self:
            rsTick = item.tick
            for msg in item.msgs.msgs:
                if msg.velocity >= 0:
                    self.seq.findByTick(rsTick).addCmd(util.noteToCmd(msg.channel, msg.note, msg.velocity))

    def buildBlocks(self):

        for channel in range(0, 16):

            for tick in range(0, self.length + 1):

                temp = self.data.getChanDataByTick(channel, tick)
                if temp:
                    try:
                        pointFuncList = temp["particle_point"]["list"]
                        fpt = int(temp["particle_point"]["fpt"])
                    except TypeError:
                        pointFuncList = [temp["particle_point"]]
                        fpt = 1
                
                if self.parMsgDict[channel].__contains__(tick):
                    this_pos = self.parMsgDict[channel][tick]
                    for pos in this_pos:
                        x, y, z = pos

                        for i, functions in enumerate(util.ceil(pointFuncList, int(len(pointFuncList)/fpt)+1)):
                            for func in functions:
                                self.seq.findByTick(tick+i).addCmd(f"execute @p {x} {y} {z} function {func}")



    def buildMcFunction(self):
        self.seq.makeNonemptyCmd(log=True)

if __name__ == "__main__":
    
    config = configparser.ConfigParser()
    config.read(r"./config.cfg", encoding="utf8")
    midifile = config.get("Base_Config", "MIDI_FILE")
    datafile = config.get("Base_Config", "DATA_FILE")
    tickrate = config.get("Base_Config", "TICKRATE")

    _msgDict = parMsgList()
    _msgDict.load(midifile, datafile, int(tickrate), makePitch=True, makeLength=True)
    _msgDict.buildNotes()
    _msgDict.buildParticle()
    _msgDict.buildBlocks()
    #_msgDict.seq.makeNonemptyCmd(log=True)
    
    