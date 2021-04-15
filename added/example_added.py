from builder.particleLine import register_parEX
import math

@register_parEX()
def parabola(x1, y1, z1, x2, y2, z2, color, high, speed=0.5, accuary=0.2):
    T = round((x2-x1) / speed)
    vx, vz = (x2-x1)/T, (z2-z1)/T
    s = math.sqrt((x2-x1)**2+(z2-z1)**2)
    vy = 4*high*s/T
    half_a = vy/T
    timesPerTick = round(s/(accuary*(x2-x1)))
    R, G, B = color
    return f'particleex endRod {x1} {y1} {z1} tickParameter {R} {G} {B} 1 240 0 0 0 0 {T} x={vx}*t;y={vy}*t-({half_a}*t^2);z={vz}*t {1/timesPerTick} {timesPerTick} 160'
