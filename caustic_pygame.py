import numpy as np
import caustics
import random
import pygame



def projection(px, py, scale=10):
    H, W = px.shape
    screen.fill((0,120,200))

    for w in range(W-1):
        for h in range(H-1):
            pygame.draw.rect(screen, (255,255,255), (px[h,w]*scale, py[h,w]*scale, scale-2, scale-2), 0)


class Caustics_PIL(caustics.Caustics):
    def animate(self, zoom=10):
        while True:
            self.progress(10)
            # decay
            self.v *= 0.999 # decay
            H, W = self.z.shape
            # random drop
            #x = random.randint(4,W-2-4)
            #y = random.randint(4,H-2-4)
            # self.gauss(x,y,4)
            px, py = self.photons(depth=4)
            # image = projection(px, py, scale=10, mode='dot')
            projection(px, py, scale=zoom)
            pygame.display.flip()
            
            
            
pygame.init()
screen = pygame.display.set_mode((640,360))

c = Caustics_PIL(64,36,2)
c.animate(zoom=10)
