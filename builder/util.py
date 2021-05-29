import math
PI = math.pi

def link(lst1, lst2):
    lst1.sort(key=lambda x: x[2])
    lst2.sort(key=lambda x: x[2])
    l1, l2 = len(lst1), len(lst2)
    build = []
    if l1 == l2 > 0:
        for i, pos in enumerate(lst1):
            build.append((pos, lst2[i]))
        return build
    elif 0 < l1 < l2:
        s = int(l2 / l1)
        for i, pos in enumerate(lst1[0:-1]):
            for pos2 in lst2[i:i * s + 1]:
                build.append((pos, pos2))
        for pos2 in lst2[l1 - 1:]:
            build.append((lst1[-1], pos2))
        return build
    elif l1 > l2 > 0:
        for i, pos in enumerate(lst2):
            build.append((lst1[i], pos))
        return build

def toPolar(x,z):
    rou = math.sqrt(x**2+z**2)
    theta = math.atan(x/z) if z != 0 else PI/2
    if x > 0:theta = theta if theta >= 0 else PI+theta
    elif x == 0:theta = 0 if z > 0 else PI
    else:theta += PI if theta > 0 else 2*PI
    return (rou,theta)



def linkWithAdded(zippedlst1,lst2):
    
    lst1, addedValue = zip(*zippedlst1)
    lst1 = list(lst1)
    lst1.sort(key=lambda x: x[2])
    lst2.sort(key=lambda x: x[2])
    l1, l2 = len(lst1), len(lst2)
    build = []
    if l1 == l2 > 0:
        for i, pos in enumerate(lst1):
            build.append((pos, lst2[i],addedValue[i]))
        return build
    elif 0 < l1 < l2:
        s = int(l2 / l1)
        for i, pos in enumerate(lst1[0:-1]):
            for pos2 in lst2[i:i * s + 1]:
                build.append((pos, pos2, addedValue[i]))
        for pos2 in lst2[l1 - 1:]:
            build.append((lst1[-1], pos2, addedValue[-1]))
        return build
    elif l1 > l2 > 0:
        for i, pos in enumerate(lst2):
            build.append((lst1[i], pos, addedValue[i]))
        return build

def noteToCmd(channel, note, velocity):
    if velocity == 0:
        return f'midiout noteclose {channel} {note}'
    else:
        return f'midiout noteopen {channel} {note} {velocity}'


def noFunc(*args, **kargs):
    pass


def ceil(lst, n):
    total = []
    length = len(lst)  # 总长
    step = int(length / n) + 1  # 每份的长度
    for i in range(0, length, step):
        total.append(lst[i: i + step])
    return total

def writeMcFunction(name, cmd):
  namespace, _name = name.split(':')
  file = f'./{namespace}/{_name}.mcfunction'
  doc = open(file, 'w')
  doc.write(cmd)
  doc.close()


def blockParticle(a,h,RGB,name,lifetime=80):
    t = 0
    build = []
    r, g, b = RGB
    k = 8
    while t < a:
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {(a/2-t)/k} {h/k} {(a/2)/k} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {(a/2)/k} {h/k} {(a/2-t)/k} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {(a/2)/-k} {h/k} {(a/2-t)/-k} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {(a/2-t)/-k} {h/k} {(a/2)/-k} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {(a/2-t)/k} {(h+a)/k} {(a/2)/k} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {(a/2)/k} {(h+a)/k} {(a/2-t)/k} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {(a/2)/-k} {(h+a)/k} {(a/2-t)/-k} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {(a/2-t)/-k} {(h+a)/k} {(a/2)/-k} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {a/(2*k)} {(h+t)/k} {a/(2*k)} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {-a/(2*k)} {(h+t)/k} {a/(2*k)} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {a/(2*k)} {(h+t)/k} {-a/(2*k)} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {-a/(2*k)} {(h+t)/k} {-a/(2*k)} 0 0 0 1 {lifetime}')
        t += 0.1
    writeMcFunction(name,'\n'.join(build))


def pyramidParticle(a,h,RGB,name,lifetime=80):
    t = 0
    build = []
    r, g, b = RGB
    k = 8
    sqrt3 = 1.73205
    sqrt2 = 1.41421
    sqrt6 = sqrt2*sqrt3
    while t < a:
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {t/k} {h/k} {0} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {t/(2*k)} {h/k} {(sqrt3/2)*t/k} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {(1/2)*t/k} {(h+(sqrt6/3)*t)/k} {(sqrt3/6)*t/k} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {(a/2)/k} {(h+(sqrt6/3)*t)/k} {(sqrt3/2)*a/k-(sqrt3/3)*t/k} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {(a/2)/k+(1/2)*t/k} {h/k} {(sqrt3/2)*a/k-(sqrt3/2)*t/k} 0 0 0 1 {lifetime}')
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {a/k-(1/2)*t/k} {(h+(sqrt6/3)*t)/k} {(sqrt3/6)*t/k} 0 0 0 1 {lifetime}')
        

        t += 0.1
    writeMcFunction(name,'\n'.join(build))

def circleParticle(R,h,RGB,name,lifetime=80):
    build = []
    t = 0
    k = 16
    r, g, b = RGB
    while t <= 2*3.14159:
        build.append(f'particleex endRod ~0.5 ~ ~0.5 normal {r} {g} {b} 1 240 {R*math.cos(t)/k} {h/k} {R*math.sin(t)/k} 0 0 0 1 {lifetime}')
        t += 0.05
    writeMcFunction(name,'\n'.join(build))


if __name__ == '__main__':
    #circleParticle(4,0,(0.7,0.2,0.7),"point:circle1")
    blockParticle(0.8, -0.2, (0.86,0.12,0.91),"point:block1")
