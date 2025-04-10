from manimlib import *
import math

def sum(a):
    s=0
    for e in a:
        s=s+e
    return s

class Field2D():
    def __init__(self,res : int):
        self.field=[]
        for b in range(res):
            fm=[]
            for a in range(res):
                fm.append([0,0,0,
                           0,1,0,
                           0,0,0])
            self.field.append(fm[:])
        self.res = res
    # Momentum of the field
    def Momentum(self,x,y,velocityField):
        return velocityField[y][x][0]*sum(self.field[y][x]),velocityField[y][x][1]*sum(self.field[y][x])

class _LB():
    res = 50
    _field = None
    Weights = [ 1/36, 1/9, 1/36, 1/9, 4/9, 1/9, 1/36, 1/9, 1/36 ]
    DiscreteVelocityVectors = [ [-1,1], [0,1], [1,1], [-1,0], [0,0], [1,0], [-1,-1], [0,-1], [1,-1] ]
    velocityField = []
    DensityField = []
    SpeedOfSound = 1/math.sqrt(3)
    # The speed of sound, specifically 1/sqrt(3) ~ 0.57
    TimeRelaxationConstant = 0.52
    a = None
    bc = "periodic"  # "bounce-back"

    def __init__(self, res, boundary_condition="periodic"):
        self.res = res
        self.bc = boundary_condition
        self._field = Field2D(self.res)
        self.velocityField=[]
        for DummyVariable in range(self.res):
            DummyList=[]
            for DummyVariable2 in range(self.res):
                DummyList.append([0,0])
            self.velocityField.append(DummyList[:])
        self.DensityField=[]
        for DummyVariable in range(self.res):
            DummyList=[]
            for DummyVariable2 in range(self.res):
                DummyList.append(1)
            self.DensityField.append(DummyList[:])

        self.a = Field2D(self.res)


    def step(self):
        # Collision Step
        df=Field2D(self.res)
        for y in range(self.res):
            for x in range(self.res):
                for v in range(9):
                    Velocity=self.a.field[y][x][v]
                    FirstTerm=Velocity
                    # The Flow Velocity
                    FlowVelocity=self.velocityField[y][x]
                    Dotted=FlowVelocity[0]*self.DiscreteVelocityVectors[v][0]+FlowVelocity[1]*self.DiscreteVelocityVectors[v][1]
                    # #The taylor expainsion of equilibrium term
                    taylor=1+((Dotted)/(self.SpeedOfSound**2))+((Dotted**2)/(2*self.SpeedOfSound**4))-((FlowVelocity[0]**2+FlowVelocity[1]**2)/(2*self.SpeedOfSound**2))
                    # The current density
                    density=self.DensityField[y][x]
                    # The equilibrium
                    equilibrium=density*taylor*self.Weights[v]
                    SecondTerm=(equilibrium-Velocity)/self.TimeRelaxationConstant
                    df.field[y][x][v]=FirstTerm+SecondTerm
        # Streaming Step
        # bc = "periodic"
        # bc = "bounce-back"
        for y in range(0,self.res):
            for x in range(0,self.res):
                for v in range(9):
                    # Target, the lattice point this iteration is solving
                    TargetY=y+self.DiscreteVelocityVectors[v][1]
                    TargetX=x+self.DiscreteVelocityVectors[v][0]
                    if self.bc == "periodic":
                        # Periodic Boundary
                        if TargetY == self.res and TargetX == self.res:
                            self.a.field[TargetY-self.res][TargetX-self.res][v]=df.field[y][x][v]
                        elif TargetX == self.res:
                            self.a.field[TargetY][TargetX-self.res][v]=df.field[y][x][v]
                        elif TargetY == self.res:
                            self.a.field[TargetY-self.res][TargetX][v]=df.field[y][x][v]
                        elif TargetY == -1 and TargetX == -1:
                            self.a.field[TargetY+self.res][TargetX+self.res][v]=df.field[y][x][v]   
                        elif TargetX == -1:
                            self.a.field[TargetY][TargetX+self.res][v]=df.field[y][x][v]
                        elif TargetY == -1:
                            self.a.field[TargetY+self.res][TargetX][v]=df.field[y][x][v]
                        else:
                            self.a.field[TargetY][TargetX][v]=df.field[y][x][v]
                    elif self.bc == "bounce-back":
                        # Bounce Back Boundary Conditions
                        vv = [8,7,6,5,4,3,2,1,0]
                        if TargetY == self.res and TargetX == self.res:
                            self.a.field[y][x][vv[v]] = df.field[y][x][v]
                        elif TargetX == self.res:
                            self.a.field[y][x][vv[v]] = df.field[y][x][v]
                        elif TargetY == self.res:
                            self.a.field[y][x][vv[v]] = df.field[y][x][v]
                        elif TargetY == -1 and TargetX == -1:
                            self.a.field[y][x][vv[v]] = df.field[y][x][v]
                        elif TargetX == -1:
                            self.a.field[y][x][vv[v]] = df.field[y][x][v]
                        elif TargetY == -1:
                            self.a.field[y][x][vv[v]] = df.field[y][x][v]
                        else:
                            self.a.field[TargetY][TargetX][v] = df.field[y][x][v]
        # Calculate macroscopic variables
        for y in range(self.res):
            for x in range(self.res):
                # Recompute Density Field
                self.DensityField[y][x]=sum(self.a.field[y][x])
                # Recompute Flow Velocity
                FlowVelocity=[0,0]
                for DummyVariable in range(9):
                    FlowVelocity[0]=FlowVelocity[0]+self.DiscreteVelocityVectors[DummyVariable][0]*self.a.field[y][x][DummyVariable]
                for DummyVariable in range(9):
                    FlowVelocity[1]=FlowVelocity[1]+self.DiscreteVelocityVectors[DummyVariable][1]*self.a.field[y][x][DummyVariable]
                FlowVelocity[0]=FlowVelocity[0]/self.DensityField[y][x]
                FlowVelocity[1]=FlowVelocity[1]/self.DensityField[y][x]
                # Insert to Velocity Field
                self.velocityField[y][x]=FlowVelocity


class LB(Scene):

    res=300

    def construct(self):
        # periodic or bounce-back
        lb1 = _LB(self.res, boundary_condition="bounce-back")
        grid1 = self.vis(None, lb1.a, lb1.velocityField)
        grid1.shift(LEFT*3.3)
        lb2 = _LB(self.res, boundary_condition="periodic")
        grid2 = self.vis(None, lb2.a, lb2.velocityField)
        grid2.shift(RIGHT*3.3)

        lb1.DensityField[round(self.res/3.0)][round(self.res/2.0)] = 2.5
        lb2.DensityField[self.res - round(self.res/3.0)][round(self.res/2.0)] = 2.5

        self.wait(1)
        for i in range(512):
            lb1.step()
            lb2.step()
            grid1 = self.vis(grid1, lb1.a, lb1.velocityField)
            grid2 = self.vis(grid2, lb2.a, lb2.velocityField)
            if i > 20:
                # unset the density value
                lb1.DensityField[5][25] = 1
                lb2.DensityField[5][25] = 1
                self.wait(0.1)
            else:
                self.wait(1)


    def vis(self, grid, a, velocityField):
        ft = True
        if grid is None:
            #grid = Square().get_grid(self.res,self.res,height=6, buff=.2).set_stroke(width=0)
            grid = Circle().get_grid(self.res,self.res,height=6, buff=.6).set_stroke(color=WHITE, width=0)
            #grid = RegularPolygon(6).get_grid(self.res,self.res,height=6, buff=.2).set_stroke(width=0)
            
            ft = False
        ma = 0
        for y in range(self.res):
            for x in range(self.res):
                c = a.Momentum(x,y,velocityField)
                c = math.sqrt(c[0]**2+c[1]**2)
                ma = max(ma,c)
        if ma == 0:
            ma = 1
        # setup a colormap
        cm = color_gradient([BLACK, BLUE_A], 256)
        for i in range(self.res*self.res):
            c = a.Momentum(i//self.res,i%self.res,velocityField)
            c = math.sqrt(c[0]**2+c[1]**2)/ma
            #if c > 1:
            #    c = .1

            #col = '#%02x%02x%02x' % (int(255.999 * math.pow(c, 1.0/2.2)),int(255.999 * math.pow(c, 1.0/2.2)),int(255.999 * math.pow(c, 1.0/2.2))) 
            col = cm[int(255*c)]
            grid[i].set_fill(col,1)
            x, y = i//self.res - self.res/2, i%self.res - self.res/2
            if math.sqrt(x**2 + y**2) >= self.res/2:
                grid[i].set_opacity(0.1)
        #self.wait(.1)
        if not(ft):
            self.add(grid)
        return grid
