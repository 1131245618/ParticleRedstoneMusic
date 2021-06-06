from Particle.LineType import LineType
import Particle.particleLine
import plugins
import sys, os, inspect

f = open("help.txt","w",encoding='utf8')

sys.stdout = f
print("==Ignore the 1st ~ 7th args==")
print("---------------------------")
for pyFunc in Particle.particleLine.pyfuncDict.keys():
    func = Particle.particleLine.pyfuncDict[pyFunc]
    typ = Particle.particleLine.functype[pyFunc]
    print(f"Defined Particle line's name:  {pyFunc}\n")
    print(typ)
    if typ in (LineType.EXPRESSION_EXTRA,  LineType.NORMAL_EXTRA):
        print("\n==The 8th arg is an added value, ignore it!==\n")
    print(func)
    print("argspec:",inspect.signature(func))
    if callable(func.__doc__):
        print("\norigin function:\n    ",end="")
        print(func.__doc__)
        print("    argspec:",inspect.signature(func.__doc__))
        print("    document of function:\n       ", func.__doc__.__doc__)
    else:
        print("document of function:\n   ",func.__doc__)
    print("\n---------------------------\n")

f.close()

os.system("notepad help.txt")

