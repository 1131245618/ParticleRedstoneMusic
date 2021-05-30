import builder.LineType
import builder.particleLine
import added
import sys,os

f = open("help.txt","w")
tmp = sys.stdout
sys.stdout = f

print("============================")
for pyFunc in builder.particleLine.pyfuncDict.keys():
    print(f"Defined particle line's name:  {pyFunc}\n")
    print(builder.particleLine.functype[pyFunc])
    print(help(builder.particleLine.pyfuncDict[pyFunc]))
    print("\n---------------------------\n")

f.close()

sys.stdout= tmp

os.system("notepad help.txt")

