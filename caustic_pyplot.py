import caustics
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class Caustics_pyplot(caustics.Caustics):
    def plot(self, data):
        global frame
        H, W = self.z.shape
        N = 4
        frame += 1
        #if frame > 100:
        #    N = 0
        scale = (W-2)/64
        self.progress(N)
        plt.cla()
        self.ax.set_facecolor((0.0, 120/255, 200/255))
        px, py = self.photons(depth=scale**2)
        plt.xlim(1,W-1)
        plt.ylim(1,H-1)
        plt.scatter(px,py,s=20/scale, c=[(1,1,1)], alpha=0.4)


    def animate(self):
        global frame
        frame = 0
        fig, self.ax = plt.subplots(nrows=1, ncols=1)
        fig.subplots_adjust(left=0,right=1)
        self.ax.axis('equal')
        ani = animation.FuncAnimation(fig, self.plot, interval=1 )
        plt.show()

c = Caustics_pyplot(64,36,2)
c.animate()
