import math
from builder.particleLine import *
import added

sin, cos, sqrt, PI = math.sin, math.cos, math.sqrt, math.pi

def toPolar(x,z):
    rou = math.sqrt(x**2+z**2)
    theta = math.atan(x/z) if z != 0 else PI/2
    if x > 0:theta = theta if theta >= 0 else PI+theta
    elif x == 0:theta = 0 if z > 0 else PI
    else:theta += PI if theta > 0 else 2*PI
    return (rou,theta)

@register_parEXAdded()
def circle(x1,y1,z1,x2,y2,z2,vector,color,speed=0.5,accuary=0.1,**keyargs):
    if not vector:
        vector = (1,0)
    if x2-x1 <= 1:
        return (straight(x1,y1,z1,x2,y2,z2, color = color, **keyargs), (z2-z1,x2-x1))
    R, G, B = color
    T = (x2 - x1) // speed
    vz1, vx1 = vector
    vx2, vz2 = (x2-x1), (z2-z1)
    a1, b1, c1 = vz1, vx1, vx1*x1+vz1*z1
    a2, b2, c2 = vz2, vx2, vx2*((x1+x2)/2)+vz2*((z1+z2)/2)
    delta = a1*b2 - b1*a2
    if abs(delta) <= 0.1:return (straight(x1,y1,z1,x2,y2,z2, color = color, **keyargs), (z2-z1,x2-x1))
    oz, ox = (c1*b2-c2*b1)/delta, (-a2*c1+a1*c2)/delta
    r, stAngle = toPolar((x1-ox), (z1-oz))
    if r >= 50:return (straight(x1,y1,z1,x2,y2,z2, color = color, **keyargs), (z2-z1,x2-x1))
    enAngle = toPolar((x2-ox), (z2-oz))[-1]
    temp = toPolar(vx1,vz1)[-1] - toPolar(x2-x1,z2-z1)[-1]
    if temp > PI or -PI < temp < 0: #逆时针
        k = -1
        outVector = (ox-x2, z2-oz)
        if enAngle < stAngle:enAngle += 2*PI
    else: #顺时针
        k = 1
        outVector = (x2-ox, oz-z2)
        enAngle = 2*PI-enAngle
        stAngle = 2*PI-stAngle
        if enAngle < stAngle:enAngle += 2*PI
    crossAngle = enAngle - stAngle
    timesPerTick = round((crossAngle/(accuary/r))/T)
    da = crossAngle/(timesPerTick*T)

    return (f'particleex endRod {ox} {y1} {oz} tickParameter {R} {G} {B} 1 240 0 0 0 {stAngle} {enAngle} x={r}*cos({k}*t+PI/2);y=0;z={r}*sin({k}*t+PI/2) {da} {timesPerTick} 160', outVector)


@register_parEX()
def straight(x1, y1, z1, x2, y2, z2, color=(0,0,0), speed=0.5, accuary=0.2, **kargs):
    r, g, b = color
    T = (x2 - x1) // speed
    if T > 0:
        length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        vx = (x2 - x1) / T
        vy = (y2 - y1) / T
        vz = (z2 - z1) / T
        timesPerTick = round(length/(accuary*(x2-x1)))
        return f'particleex endRod {x1} {y1} {z1} tickParameter {r} {g} {b} 1 240 0 0 0 0 {T} x={vx}*t;y={vy}*t;z={vz}*t {1/timesPerTick} {timesPerTick} 160'
        
    elif T == 0:
        T = z2 - z1
        vx = 0
        vy = (y2 - y1) / T
        vz = (z2 - z1) / T
        return f'particleex endRod {x1} {y1} {z1} parameter 1 0 1 1 240 0 0 0 0 {T} x={vx}*t;y={vy}*t;z={vz}*t {accuary}'
 

@register_normal("st")
def straigh_line(x1, y1, z1, x2, y2, z2, accuary=0.1, **kargs):
    '''
    穷举直线的函数，返回坐标的列表。
    accuary为线中每个点之间的距离，可理解为精细程度。
    '''
    length = sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
    vector_x = (x2-x1)/(length/accuary)
    vector_y = (y2-y1)/(length/accuary)
    vector_z = (z2-z1)/(length/accuary)

    pos = []

    t = 0
    while t <= length/accuary:
        pos.append((x1+vector_x*t, y1+vector_y*t, z1+vector_z*t))
        t += accuary

    return pos




