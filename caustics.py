import numpy as np
from math import exp


class Caustics():
    def __init__(self, W_, H_, resol):
        self.resolution = resol
        self.W = W_*resol + 2
        self.H = H_*resol + 2

        self.z = np.zeros([self.H,self.W])
        self.v = np.zeros([self.H,self.W])
        # self.gauss(5*resol,5*resol,5*resol)
        # self.gauss(55*resol,25*resol,5*resol)
        # self.gauss(27*resol,30*resol,5*resol)
        self.mass = 4.0 / resol**2
        self.k    = 4.0 # / resol**2
        self.dt   = 0.05

    def gauss(self, cx,cy,R):
        """
        Gaussian wave packet
        """
        for x in range(-R,R+1):
            for y in range(-R,R+1):
                self.v[cy+y,cx+x] += 10*exp(-(x**2+y**2)/(R*2))

    def photons(self, depth=1):
        """
        Determine the destinations of the photons from the surface gradient.
        """
        dx  = np.zeros_like(self.z)
        dy  = np.zeros_like(self.z)
        for w in range(self.W-1):
            for h in range(self.H-1):
                dx[h,w]  = self.z[h,w+1] - self.z[h,w]
                dy[h,w]  = self.z[h+1,w] - self.z[h,w]
        x = np.arange(0, self.W)
        y = np.arange(0, self.H)
        xv, yv = np.meshgrid(x, y)
        px = xv - dx*depth
        py = yv - dy*depth
        return px,py


    def progress(self, N=4):
        """
        Solve the Newton's equation numerically.
        """
        for skips in range(N):
            # leap-frog algorithm
            self.z += self.v*(self.dt/2)
            F = self.k*(self.z[1:self.H-1, 0:self.W-2] + self.z[1:self.H-1, 2:self.W] + self.z[0:self.H-2, 1:self.W-1] + self.z[2:self.H, 1:self.W-1] - 4*self.z[1:self.H-1, 1:self.W-1])
            a = F/self.mass
            self.v[1:self.H-1, 1:self.W-1] += a*self.dt
            self.z += self.v*(self.dt/2)

        # verify energy conservation
        # Ek = np.sum(v**2)*mass/2
        # Eph = np.sum((z[1:self.H-1, 0:self.W-1] - z[1:self.H-1, 1:self.W])**2)*k/2
        # Epv = np.sum((z[0:self.H-1, 1:self.W-1] - z[1:self.H, 1:self.W-1])**2)*k/2
        # Ep = Eph+Epv
        # print(Ep+Ek,Ep,Ek)


