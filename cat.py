from manimlib import *
import numpy as np
import scipy as sp
import scipy.ndimage

# white noise model for orientation sensitive cells in the visual cortex

class cat(Scene):
    def construct(self):
        pass

class Field2D():
    def __init__(self,res : int):
        self.field=[]
        # use a numpy array to store the two fields
        self.one = 2*np.random.rand(res, res)-1 
        self.two = 2*np.random.rand(res, res)-1
        self.res = res

    # orientation of the field
    def Orientation(self,x, y):
        return math.atan2(self.two[y][x],self.one[y][x])

class _cat():
    res = 50
    _field = None
    sigma_y = .6
    sigma_x = .6

    def __init__(self, res):
        self.res = res
        self._field = Field2D(res)

    def step(self):
        sigma = [self.sigma_y, self.sigma_x]
        self._field.one = sp.ndimage.filters.gaussian_filter(self._field.one, sigma, mode='constant')
        self._field.two = sp.ndimage.filters.gaussian_filter(self._field.two, sigma, mode='constant')

class Cat(Scene):

    res=81

    def construct(self):
        ca = _cat(self.res)
        grid = self.vis(None, ca._field)

        self.wait(1)
        for i in range(68):
            ca.step()
            grid = self.vis(grid, ca._field)
            self.wait(0.3)


    def vis(self, grid, a):
        ft = True
        if grid is None:
            #grid = Square().get_grid(self.res,self.res,height=6, buff=.2).set_stroke(width=0)
            grid = Circle().get_grid(self.res,self.res,height=6, buff=.6).set_stroke(color=WHITE, width=0)
            #grid = RegularPolygon(6).get_grid(self.res,self.res,height=6, buff=.2).set_stroke(width=0)
            
            ft = False
        ma = 0
        for y in range(self.res):
            for x in range(self.res):
                c = a.Orientation(x,y)
                #c = math.sqrt(c[0]**2+c[1]**2)
                ma = max(ma,c)
        if ma == 0:
            ma = 1
        # setup a colormap
        cm = get_color_map("hsv")
        #cm = get_color_map("twilight")
        
        # cm = color_gradient([BLACK, BLUE_A], 256)
        for i in range(self.res*self.res):
            c = a.Orientation(i//self.res,i%self.res)
            # c is now between -pi and pi
            c = (c + np.pi)/(2*np.pi)
            #c = math.sqrt(c[0]**2+c[1]**2)/ma
            #if c > 1:
            #    c = .1

            #col = '#%02x%02x%02x' % (int(255.999 * math.pow(c, 1.0/2.2)),int(255.999 * math.pow(c, 1.0/2.2)),int(255.999 * math.pow(c, 1.0/2.2))) 
            col = rgba_to_color(cm(int(255*c)))
            grid[i].set_fill(col,1)
            x, y = i//self.res - self.res/2, i%self.res - self.res/2
            if math.sqrt(x**2 + y**2) >= self.res/2:
                grid[i].set_opacity(0.1)
        #self.wait(.1)
        if not(ft):
            self.add(grid)
        return grid
