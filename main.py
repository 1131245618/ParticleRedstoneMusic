from Particle import parMsg
import configparser

config = configparser.ConfigParser()
config.read(r"./config.cfg", encoding="utf8")
midifile = config.get("Base_Config", "MIDI_FILE")
datafile = config.get("Base_Config", "DATA_FILE")

outputFolder = config.get("Base_Config", "OUTPUT_FOLDER")

_msgDict = parMsg.parMsgList()
_msgDict.load(midifile, datafile, outputFolder, makePitch=True, makeLength=True)
_msgDict.buildNotes()
_msgDict.buildParticle()
_msgDict.buildBlocks()
_msgDict.buildPointPar()
_msgDict.buildMcFunction(nonEmpty=False, log=True, loopCmd='tp @p ~0.5 ~ ~')
