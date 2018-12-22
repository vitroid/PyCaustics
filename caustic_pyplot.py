import numpy as np
from math import exp
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def gauss(z,cx,cy,R):
    """
    Gaussian wave packet
    """
    for x in range(-R,R+1):
        for y in range(-R,R+1):
            z[cy+y,cx+x] += 10*exp(-(x**2+y**2)/(R*2))

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


def progress(N=4):
    """
    Solve the Newton's equation numerically.
    """
    global z
    for skips in range(N):
        # leap-frog algorithm
        z += v*(dt/2)
        F = k*(z[1:H-1, 0:W-2] + z[1:H-1, 2:W] + z[0:H-2, 1:W-1] + z[2:H, 1:W-1] - 4*z[1:H-1, 1:W-1])
        a = F/mass
        v[1:H-1, 1:W-1] += a*dt
        z += v*(dt/2)

    # verify energy conservation
    # Ek = np.sum(v**2)*mass/2
    # Eph = np.sum((z[1:H-1, 0:W-1] - z[1:H-1, 1:W])**2)*k/2
    # Epv = np.sum((z[0:H-1, 1:W-1] - z[1:H, 1:W-1])**2)*k/2
    # Ep = Eph+Epv
    # print(Ep+Ek,Ep,Ek)

def plot(data):
    progress()
    plt.cla()
    ax.set_facecolor((0.0, 120/255, 200/255))
    px, py = photons(z, depth=3)
    plt.xlim(0,W)
    plt.ylim(0,H)
    plt.scatter(px,py,s=20, c=[(1,1,1)], alpha=0.4)



#including two ends
W=64+2
H=36+2

z = np.zeros([H,W])
v = np.zeros([H,W])
gauss(z,5,5,5)
gauss(z,55,25,5)
gauss(z,27,30,5)
mass = 1.0
k    = 1.0
dt   = 0.25

fig, ax = plt.subplots(nrows=1, ncols=1)
fig.subplots_adjust(left=0,right=1)
ax.axis('equal')
ani = animation.FuncAnimation(fig, plot, interval=30)
plt.show()


