import math
from builder import util
from builder.LineType import LineType

sqrt = math.sqrt
ceil = util.ceil

pyfuncDict = {}
functype = {}


def register(pyfunc,name=None,typ=LineType.NORMAL):
    if not name: name = pyfunc.__name__
    pyfuncDict[name] = pyfunc
    functype[name] = typ


def getfunc(name):
    return pyfuncDict.get(name)

def getfuncType(name):
    return functype.get(name)

def register_cacl(name=None, typ=LineType.NORMAL):
    def regist(func):
        register(func, name, typ)
        return func
    return regist

def register_normal(name=None):
    def regist(func):

        def decorator(x1, y1, z1, x2, y2, z2, ticks, particle_name, color, **kargs):

            pos = func(x1, y1, z1, x2, y2, z2, **kargs)
            particles = []
            for p in pos:
                x, y, z = p
                particles.append(f"particle {particle_name} {x} {y} {z} 0 0 0 0 1 force")
            particles = ceil(particles, ticks)
            return particles
        decorator.__name__ = func.__name__
        register(decorator,name,LineType.NORMAL)
        return decorator
    return regist

def register_normalExtra(name=None):
    def regist(func):

        def decorator(x1, y1, z1, x2, y2, z2, ticks, added, particle_name, **kargs):

            pos, other = func(x1, y1, z1, x2, y2, z2, added, **kargs)
            particles = []
            for p in pos:
                x, y, z = p
                particles.append(f"particle {particle_name} {x} {y} {z} 0 0 0 0 1 force")
            particles = ceil(particles, ticks)
            return particles, other
        decorator.__name__ = func.__name__
        register(decorator,name,LineType.NORMAL_EXTRA)
        return decorator
    return regist


def register_parEX(name=None):
    def regist(func):
        register(func,name,LineType.EXPRESSION)
        return func
    return regist

def register_parEXExtra(name=None):
    def regist(func):
        register(func,name,LineType.EXPRESSION_EXTRA)
        return func
    return regist

def register_normalEX(name=None):
    def regist(func):

        def decorator(x1, y1, z1, x2, y2, z2, ticks, particle_name, **kargs):

            pos = func(x1, y1, z1, x2, y2, z2, **kargs)
            particles = []
            for p in pos:
                x, y, z = p
                particles.append(f"particleex {particle_name} {x} {y} {z} normal 0 0 0 1 240 0 0 0 0 0 0 1 200")
            particles = ceil(particles, ticks)
            return particles
        decorator.__name__ = func.__name__
        register(decorator,name,LineType.NORMAL)
        return decorator
    return regist


if __name__ == "__main__":
    a = {"particle_name":"endRod", "accuary":0.1, "speed":0.5, "color":tuple([0,0,1])}
    #cmdline = getfunc("st")(0,1,1,2,2,2, ticks= 2,**a)
    #print(cmdline)
    #print(pyfuncDict)
    #print(functype)


