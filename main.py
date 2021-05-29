from builder import parMsg
import configparser
from added import added

config = configparser.ConfigParser()
config.read(r"./config.cfg", encoding="utf8")
midifile = config.get("Base_Config", "MIDI_FILE")
datafile = config.get("Base_Config", "DATA_FILE")
tickrate = config.get("Base_Config", "TICKRATE")

_msgDict = parMsg.parMsgList()
_msgDict.load(midifile, datafile, int(tickrate), makePitch=True, makeLength=True)
_msgDict.buildNotes()
_msgDict.buildParticle()
_msgDict.buildBlocks()
_msgDict.buildPointPar()
_msgDict.seq.makeCmd(log=True,loopCmd='tp @p ~0.5 ~ ~')

