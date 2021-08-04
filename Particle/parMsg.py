from re import L
from xuetaolu.noteMsg import MsgList
from Particle import parDatas, sequence2, util, particleLine
import plugins
from Particle.LineType import LineType
import configparser
import random


class parMsgList(MsgList):

    def __init__(self, *args, **keys):
        super().__init__(*args, **keys)
        self.parMsgDict = {}
        for i in range(16):
            self.parMsgDict[i] = {}
        self.particleSpeed = 0.5
        self.seq = None
        self.length = 0
        self.data = None

    def load(self, file, data_file_path, outputFolder, tickrate=20.0, makeLength=True, makePitch=True):

        self.seq = sequence2.Seq2(outputFolder)
        self.data = parDatas.ParDataLists(data_file_path)
        self.data.load()
        super().load(file, self.data.tickrate, makeLength, makePitch)

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

            last_pos = [(157, 30, -228)]
            last_tick = -40
            line_type = None
            line_func = lambda *args, **kargs : None
            last_func = None
            posAndValues = []
            delta_pos = [0,0,0]
            keyargs = {}

            for tick in range(0, self.length + 1):

                temp = self.data.getChanDataByTick(channel, tick)
                if temp:
                    line_func = particleLine.getfunc(temp["particle_line"]["pyFunction"])
                    if last_func != line_func:
                        posAndValues = []# 若函数改变，将附加值清空
                    line_type = particleLine.getfuncType(temp["particle_line"]["pyFunction"])
                    last_func = line_func
                    keyargs = temp["particle_line"]["args"]
                    delta_pos = temp.get("pos",delta_pos)

                if self.parMsgDict[channel].__contains__(tick):
                    this_pos = self.parMsgDict[channel][tick]
                    dx, dy, dz = delta_pos
                    if last_pos:
                        #开始计算线段
                        if line_type == LineType.NORMAL:
                            linkedLines = util.link(last_pos, this_pos)
                            for pos1, pos2 in linkedLines:
                                (x1, y1, z1), (x2, y2, z2) = pos1, pos2
                                cmdlines = line_func(x1+dx, y1+dy, z1+dz, x2+dx, y2+dy, z2+dz, ticks = tick - last_tick, **keyargs)
                                for i, cmdLine in enumerate(cmdlines):
                                    for cmd in cmdLine:
                                        self.seq.findByTick(last_tick+i).addCmd(cmd)

                        elif line_type == LineType.EXPRESSION:
                            linkedLines = util.link(last_pos, this_pos)
                            for pos1, pos2 in linkedLines:
                                (x1, y1, z1), (x2, y2, z2) = pos1, pos2
                                cmd= line_func(x1+dx, y1+dy, z1+dz, x2+dx, y2+dy, z2+dz,  ticks = tick - last_tick, **keyargs)
                                self.seq.findByTick(last_tick).addCmd(cmd)

                        elif line_type == LineType.NORMAL_EXTRA:
                            if not posAndValues:
                                linkedLines = util.link(last_pos, this_pos)
                                temp = []
                                for i in linkedLines:
                                    temp.append(i+(None,))
                                linkedLines = temp
                            else:
                                linkedLines = util.linkWithValue(posAndValues, this_pos)
                            posAndValues = []
                            for pos1, pos2, addedVal in linkedLines:
                                (x1, y1, z1), (x2, y2, z2) = pos1, pos2
                                cmdlines, other = line_func(x1+dx, y1+dy, z1+dz, x2+dx, y2+dy, z2+dz, tick - last_tick,addedVal, **keyargs)
                                posAndValues.append(((x2,y2,z2), other))
                                for i, cmdLine in enumerate(cmdlines):
                                    for cmd in cmdLine:
                                        self.seq.findByTick(last_tick+i).addCmd(cmd)

                        elif line_type == LineType.EXPRESSION_EXTRA:
                            if not posAndValues:
                                linkedLines = util.link(last_pos, this_pos)
                                temp = []
                                for i in linkedLines:
                                    temp.append(i+(None,))
                                linkedLines = temp
                            else:
                                linkedLines = util.linkWithValue(posAndValues, this_pos)
                            posAndValues = []
                            for pos1, pos2, addedVal in linkedLines:
                                (x1, y1, z1), (x2, y2, z2) = pos1, pos2
                                cmd, other = line_func(x1+dx, y1+dy, z1+dz, x2+dx, y2+dy, z2+dz, tick - last_tick, addedVal, **keyargs)
                                posAndValues.append(((x2,y2,z2), other))
                                self.seq.findByTick(last_tick).addCmd(cmd)
                            
                    last_pos = this_pos
                    last_tick = tick
            
            last_pos = [(147, 30, -318)]
            last_tick = -60
            delta_pos = [0,0,0]
            line_type = None


    def buildNotes(self):

        for item in self:
            rsTick = item.tick
            for msg in item.msgs.msgs:
                if msg.velocity >= 0:
                    self.seq.findByTick(rsTick).addCmd(util.noteToCmd(msg.channel, msg.note, msg.velocity))


    def buildPointPar(self):

        for channel in range(0, 16):

            delta_pos = [0,0,0]
            isRandom = False

            for tick in range(0, self.length + 1):
                
                temp = self.data.getChanDataByTick(channel, tick)
                if temp:
                    delta_pos = temp.get("pos",delta_pos)
                    try:
                        pointFuncList = temp["particle_point"]["list"]
                        times = int(temp["particle_point"]["times"])
                        tpt = int(temp["particle_point"]["tickspertime"])
                        isRandom = temp["particle_point"].get("random", False)
                    except TypeError:
                        pointFuncList = [temp["particle_point"]]
                        times = 1
                        tpt = 1

                if self.parMsgDict[channel].__contains__(tick):
                    this_pos = self.parMsgDict[channel][tick]
                    for pos in this_pos:
                        x, y, z = pos
                        dx, dy, dz = delta_pos
                        if isRandom:
                            random.shuffle(pointFuncList)

                        for i, func in enumerate(pointFuncList):
                            if i <= times:
                                self.seq.findByTick(tick+i*tpt).addCmd(f"execute @p {x+dx} {y+dy} {z+dz} function {func}")
                            else:
                                break

            isRandom = False
            delta_pos = [0,0,0]


    def buildBlocks(self):

        for channel in range(0, 16):

            delta_pos = [0,0,0]
            for tick in range(0, self.length + 1):

                temp = self.data.getChanDataByTick(channel, tick)
                if temp:
                    delta_pos = temp.get("pos",delta_pos)

                if self.parMsgDict[channel].__contains__(tick):
                    this_pos = self.parMsgDict[channel][tick]
                    for pos in this_pos:
                        x, y, z = pos
                        dx, dy, dz = delta_pos
                        self.seq.findByTick(tick).addCmd(f"setblock {x+dx} {y+dy} {z+dz} {self.data.getblock(channel)} replace")
            delta_pos = [0,0,0]


    def buildMcFunction(self, nonEmpty=True, log=True, loopCmd=''):
        if nonEmpty:
            self.seq.makeNonemptyCmd(log=log, loopCmd=loopCmd)
        else:
            self.seq.makeCmd(log=log, loopCmd=loopCmd)


if __name__ == "__main__":
    
    config = configparser.ConfigParser()
    config.read(r"./config.cfg", encoding="utf8")

    midifile = config.get("Base_Config", "MIDI_FILE")
    datafile = config.get("Base_Config", "DATA_FILE")
    outputFolder = config.get("Base_Config", "OUTPUT_FOLDER")

    _msgDict = parMsgList()
    _msgDict.load(midifile, datafile, outputFolder, makePitch=True, makeLength=True)
    _msgDict.buildNotes()
    _msgDict.buildparticle()
    _msgDict.buildBlocks()
    #_msgDict.seq.makeNonemptyCmd(log=True)
    
    