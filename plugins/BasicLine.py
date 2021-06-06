from Particle.particleLine import register_cacl, register_normal
import math
from math import sqrt, sin, cos, atan
from Particle.util import ceil, toPolar
from Particle.LineType import LineType

PI = math.pi

@register_cacl(typ=LineType.EXPRESSION)
def parabola(x1, y1, z1, x2, y2, z2, ticks, color, high, accuary=0.2,**kargs):
    '''
    抛物线，参数high为高度与两点距离的比值
    '''
    speed = (x2 -x1) / ticks
    T = round((x2-x1) / speed)
    vx, vz = (x2-x1)/T, (z2-z1)/T
    s = sqrt((x2-x1)**2+(z2-z1)**2)
    vy = 4*high*s/T
    half_a = vy/T
    timesPerTick = round(s/(accuary*(x2-x1)))
    R, G, B = color
    return f'Particleex endRod {x1} {y1} {z1} tickParameter {R} {G} {B} 1 240 0 0 0 0 {T} x={vx}*t;y={vy}*t-({half_a}*t^2);z={vz}*t {1/timesPerTick} {timesPerTick} 160'

@register_cacl(typ=LineType.EXPRESSION)
def straightEx(x1, y1, z1, x2, y2, z2, ticks, color=(0,0,0), accuary=0.2, **kargs):
    '''
    普通的直线(=・ω・=)
    '''
    speed = (x2 -x1) / ticks
    r, g, b = color
    T = (x2 - x1) // speed
    if T > 0:
        length = sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
        vx = (x2 - x1) / T
        vy = (y2 - y1) / T
        vz = (z2 - z1) / T
        timesPerTick = round(length/(accuary*(x2-x1)))
        return f'Particleex endRod {x1} {y1} {z1} tickParameter {r} {g} {b} 1 240 0 0 0 0 {T} x={vx}*t;y={vy}*t;z={vz}*t {1/timesPerTick} {timesPerTick} 160'
        
    elif T == 0:
        T = z2 - z1
        vx = 0
        vy = (y2 - y1) / T
        vz = (z2 - z1) / T
        return f'Particleex endRod {x1} {y1} {z1} parameter 1 0 1 1 240 0 0 0 0 {T} x={vx}*t;y={vy}*t;z={vz}*t {accuary}'

@register_cacl()
def spiralParabola(x1, y1, z1, x2, y2, z2, ticks, omega, n, r, accuary=0.1,**kargs):
    '''
    螺旋抛物线，n为高度与两点距离的比值，omega为角速度，r为半径(粒子扩散的速度)
    '''
    T = ticks
    S = sqrt((x1-x2)**2+(z1-z2)**2)
    H = n*S
    vx = (x2-x1)/T
    vy= 4*H/T
    a= 8*H/(T**2)
    vz = (z2-z1)/T
    if vz != 0:
        theta = atan(vx/vz)
    else:
        theta = 1.5708
    cmdLines = []

    t = 0
    while t <= T:
        x=x1+vx*t
        y=y1+vy*t-0.5*a*t**2 
        z=z1+vz*t
        ds = sqrt((x-x1)**2+(z-z1)**2)
        phi= atan((vy - a * t)/sqrt(vx**2+vz**2))
        vector_x1 = r*(sin(theta)*cos(omega*ds)-cos(theta)*sin(phi)*sin(omega*ds))
        vector_y1 = r*cos(phi)*sin(omega*ds)
        vector_z1 = r*(cos(theta)*cos(omega*ds)+sin(theta)*sin(phi)*sin(omega*ds))
        vector_x2 = r*(sin(theta)*cos(omega*ds+3.1415)-cos(theta)*sin(phi)*sin(omega*ds+3.1415))
        vector_y2 = r*cos(phi)*sin(omega*ds+3.1415)
        vector_z2 = r*(cos(theta)*cos(omega*ds+3.1415)+sin(theta)*sin(phi)*sin(omega*ds+3.1415))
        cmd = f"particle endRod {x} {y} {z} {vector_x1} {vector_y1} {vector_z1} 0.1 0 force \nparticle endRod {x} {y} {z} {vector_x2} {vector_y2} {vector_z2} 0.1 0 force "
        cmdLines.append(cmd)
        t += accuary

    return ceil(cmdLines, T)

@register_cacl(typ=LineType.EXPRESSION)
def spiral(x1,y1,z1,x2,y2,z2, ticks, color, omega, n = 12, accuary=0.2, **kargs):
    '''
    两头小中间大的螺旋线，omega为角速度，n为两点距离与最大半径的比值
    '''
    speed = (x2 -x1) / ticks
    if abs((x2-x1)/((z2-z1)+0.001)) <= 1/4:
        return parabola(x1, y1, z1, x2, y1, z2, ticks, color=color, high=0.25, speed=0.5, accuary=0.1)
    T = round((x2-x1) / speed)
    s = sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
    h = y2-y1
    theta = atan((z2-z1)/(x2-x1))
    phi = atan(h/s)
    vx, vy, vz = (x2-x1)/T, (y2-y1)/T, (z2-z1)/T
    R, G, B = color
    r = s/n if s/n <= 2 else 2
    bbb = 4*r/T
    aaa = -(4*r/T**2)
    cmd = f'Particleex endRod {x1} {y1} {z1} tickParameter {R} {G} {B} 1 240 0 0 0 0 {T} r={aaa}*t^2+({bbb}*t);x={vx}*t+r*({sin(theta)}*cos({omega}*t)+({(-cos(theta)*sin(phi))}*sin({omega}*t)));y={vy}*t+r*{cos(phi)}*sin({omega}*t);z={vz}*t+r*({cos(theta)}*cos({omega}*t)+({sin(theta)*sin(phi)}*sin({omega}*t))) {accuary} {round(1/accuary)} 180'
    cmd += f'\nParticleex endRod {x1} {y1} {z1} tickParameter {R} {G} {B} 1 240 0 0 0 0 {T} r={aaa}*t^2+({bbb}*t);x={vx}*t+r*({sin(theta)}*cos({omega}*t+PI)+({(-cos(theta)*sin(phi))}*sin({omega}*t+PI)));y={vy}*t+r*{cos(phi)}*sin({omega}*t+PI);z={vz}*t+r*({cos(theta)}*cos({omega}*t+PI)+({sin(theta)*sin(phi)}*sin({omega}*t+PI))) {accuary} {round(1/accuary)} 180'
    return cmd


@register_cacl(typ=LineType.EXPRESSION_EXTRA)
def circle(x1,y1,z1,x2,y2,z2, ticks, vector, color, accuary=0.1, **keyargs):
    '''
    圆
    '''
    speed = (x2 -x1) / ticks
    if not vector:
        vector = (1,0)
    if x2-x1 <= 2:
        return (parabola(x1,y1,z1,x2,y2,z2, ticks, high=0.1, color = color, **keyargs), (z2-z1,x2-x1))
    R, G, B = color
    T = (x2 - x1) // speed
    vz1, vx1 = vector
    vx2, vz2 = (x2-x1), (z2-z1)
    a1, b1, c1 = vz1, vx1, vx1*x1+vz1*z1
    a2, b2, c2 = vz2, vx2, vx2*((x1+x2)/2)+vz2*((z1+z2)/2)
    delta = a1*b2 - b1*a2
    if abs(delta) <= 0.01:return (parabola(x1,y1,z1,x2,y2,z2, ticks,high=0.1, color = color, **keyargs), (z2-z1,x2-x1))
    oz, ox = (c1*b2-c2*b1)/delta, (-a2*c1+a1*c2)/delta
    r, stAngle = toPolar((x1-ox), (z1-oz))
    if r >= 40:return (parabola(x1,y1,z1,x2,y2,z2, ticks, high=0.1, color = color, **keyargs), (z2-z1,x2-x1))
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

    return (f'Particleex endRod {ox} {y1} {oz} tickParameter {R} {G} {B} 1 240 0 0 0 {stAngle} {enAngle} x={r}*cos({k}*t+PI/2);y=0;z={r}*sin({k}*t+PI/2) {da} {timesPerTick} 160', outVector)


@register_cacl(name="straight")
def straight(x1, y1, z1, x2, y2, z2, ticks, dxyz, amount, velocity, accuary=0.3, **kargs):
    '''
    基于原版的直线，dxyz为粒子范围，是个三元素列表。amount为粒子数量，velocity为粒子扩散速度，精度accuary可以设大一点。
    '''
    length = sqrt((x2-x1)**2+(y2-y1)**2+(z2-z1)**2)
    vector_x = (x2-x1)/(length/accuary)
    vector_y = (y2-y1)/(length/accuary)
    vector_z = (z2-z1)/(length/accuary)
    pos = []
    dx, dy, dz = dxyz
    t = 0
    while t <= length/accuary:
        pos.append(f"Particle endRod {x1+vector_x*t+0.5} {y1+vector_y*t} {z1+vector_z*t+0.5} {dx} {dy} {dz} {velocity} {amount} force")
        t += accuary

    return ceil(pos,ticks)



