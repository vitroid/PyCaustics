import numpy as np
from math import exp
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image

def gauss(z,cx,cy):
    for x in range(-10,11):
        for y in range(-10,11):
            z[cy+y,cx+x] += 10*exp(-(x**2+y**2)/20)


def photons(map, depth=1):
    """
    Determine the destinations of the photons from the surface gradient.
    """
    H,W = map.shape
    dx  = np.zeros((H,W))
    dy  = np.zeros((H,W))
    for w in range(W-1):
        for h in range(H-1):
            dx[h,w]  = map[h,w+1] - map[h,w]
            dy[h,w]  = map[h+1,w] - map[h,w]
    x = np.arange(0, W)
    y = np.arange(0, H)
    xv, yv = np.meshgrid(x, y)
    px = xv - dx*depth
    py = yv - dy*depth
    return px,py


def area(p,q):
    return abs(p[1]*q[0] - p[0]*q[1])


def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a


def projection(px, py, scale=10, mode='poly'):
    image = Image.new("RGB", (W*scale, H*scale), (0,120,200))
    draw = ImageDraw.Draw(image, 'RGBA')

    for w in range(W-1):
        for h in range(H-1):
            if mode == 'poly':
                p00 = np.array([px[h,w], py[h,w]])
                p10 = np.array([px[h,w+1],py[h,w+1]])
                p11 = np.array([px[h+1,w+1],py[h+1,w+1]])
                p01 = np.array([px[h+1,w], py[h+1,w]])
                S = area(p10-p00,p11-p00) + area(p11-p00,p01-p00)
                brightness = 1./S

                points = np.array([p00,p01,p11,p10]) * scale
                points = np.array(points, dtype=int)
                points = totuple(points)
                draw.polygon(points, fill=(255,255,255,int(255*brightness)))
            elif mode == 'dot':
                p00 = (px[h,w]*scale, py[h,w]*scale)
                p01 = (p00[0]+scale-2,p00[1])
                p11 = (p00[0]+scale-2,p00[1]+scale-2)
                p10 = (p00[0],p00[1]+scale-2)
                draw.polygon((p00,p01,p11,p10), fill=(255,255,255,100))
    return image

#including two ends
W=128+2
H=72+2

z = np.zeros([H,W])
v = np.zeros([H,W])
gauss(z,10,10)
gauss(z,110,50)
gauss(z,55,60)
mass = 1.0
k    = 1.0
dt   = 0.1

for loop in range(1000):
    for skips in range(10):
        z += v*(dt/2)

        F = k*(z[1:H-1, 0:W-2] + z[1:H-1, 2:W] + z[0:H-2, 1:W-1] + z[2:H, 1:W-1] - 4*z[1:H-1, 1:W-1])
        a = F/mass
        v[1:H-1, 1:W-1] += a*dt

        z += v*(dt/2)

    Ek = np.sum(v**2)*mass/2
    Eph = np.sum((z[1:H-1, 0:W-1] - z[1:H-1, 1:W])**2)*k/2
    Epv = np.sum((z[0:H-1, 1:W-1] - z[1:H, 1:W-1])**2)*k/2
    Ep = Eph+Epv
    px, py = photons(z, depth=10)
    # image = projection(px, py, scale=10, mode='dot')
    image = projection(px, py, scale=10, mode='poly')
    image.save('{0:04d}.png'.format(loop))
    print(loop, Ep+Ek,Ep,Ek)


