import numpy as np
import PIL.ImageDraw as ImageDraw
import PIL.Image as Image
import caustics

def area(p,q):
    return abs(p[1]*q[0] - p[0]*q[1])


def totuple(a):
    try:
        return tuple(totuple(i) for i in a)
    except TypeError:
        return a


def projection(px, py, scale=10, mode='poly'):
    H, W = px.shape
    image = Image.new("RGB", ((W-2)*scale, (H-2)*scale), (0,120,200))
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


class Caustics_PIL(caustics.Caustics):
    def animate(self, zoom=10):
        for loop in range(2000):
            self.progress(10)
            px, py = self.photons(depth=4)
            # image = projection(px, py, scale=10, mode='dot')
            image = projection(px, py, scale=zoom, mode='poly')
            image.save('{0:04d}.png'.format(loop))




c = Caustics_PIL(64,36,2)
c.animate(zoom=50)
