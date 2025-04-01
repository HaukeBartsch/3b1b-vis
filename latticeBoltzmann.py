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

class LB(Scene):

    Weights = [ 1/36, 1/9, 1/36, 1/9, 4/9, 1/9, 1/36, 1/9, 1/36 ]
    DiscreteVelocityVectors = [ [-1,1], [0,1], [1,1], [-1,0], [0,0], [1,0], [-1,-1], [0,-1], [1,-1] ]
    res=50

    def construct(self):

        a = Field2D(self.res)
        velocityField=[]
        for DummyVariable in range(self.res):
            DummyList=[]
            for DummyVariable2 in range(self.res):
                DummyList.append([0,0])
            velocityField.append(DummyList[:])
        DensityField=[]
        for DummyVariable in range(self.res):
            DummyList=[]
            for DummyVariable2 in range(self.res):
                DummyList.append(1)
            DensityField.append(DummyList[:])
        grid = self.vis(None, a, velocityField)

        DensityField[5][25] = 1.5
        #DensityField[20][25]=4

        MaxSteps = 512
        #The speed of sound, specifically 1/sqrt(3) ~ 0.57
        SpeedOfSound=1/math.sqrt(3)
        #time relaxation constant supposed to be > 1/2
        TimeRelaxationConstant=0.7

        for s in range(MaxSteps):
            # Collision Step
            df=Field2D(self.res)
            for y in range(self.res):
                for x in range(self.res):
                    for v in range(9):
                        Velocity=a.field[y][x][v]
                        FirstTerm=Velocity
                        # The Flow Velocity
                        FlowVelocity=velocityField[y][x]
                        Dotted=FlowVelocity[0]*self.DiscreteVelocityVectors[v][0]+FlowVelocity[1]*self.DiscreteVelocityVectors[v][1]
                        # #The taylor expainsion of equilibrium term
                        taylor=1+((Dotted)/(SpeedOfSound**2))+((Dotted**2)/(2*SpeedOfSound**4))-((FlowVelocity[0]**2+FlowVelocity[1]**2)/(2*SpeedOfSound**2))
                        # The current density
                        density=DensityField[y][x]
                        # The equilibrium
                        equilibrium=density*taylor*self.Weights[v]
                        SecondTerm=(equilibrium-Velocity)/TimeRelaxationConstant
                        df.field[y][x][v]=FirstTerm+SecondTerm
            # Streaming Step
            #bc = "periodic"
            bc = "bounce-back"
            for y in range(0,self.res):
                for x in range(0,self.res):
                    for v in range(9):
                        # Target, the lattice point this iteration is solving
                        TargetY=y+self.DiscreteVelocityVectors[v][1]
                        TargetX=x+self.DiscreteVelocityVectors[v][0]
                        if bc == "periodic":
                            # Periodic Boundary
                            if TargetY == self.res and TargetX == self.res:
                                a.field[TargetY-self.res][TargetX-self.res][v]=df.field[y][x][v]
                            elif TargetX == self.res:
                                a.field[TargetY][TargetX-self.res][v]=df.field[y][x][v]
                            elif TargetY == self.res:
                                a.field[TargetY-self.res][TargetX][v]=df.field[y][x][v]
                            elif TargetY == -1 and TargetX == -1:
                                a.field[TargetY+self.res][TargetX+self.res][v]=df.field[y][x][v]   
                            elif TargetX == -1:
                                a.field[TargetY][TargetX+self.res][v]=df.field[y][x][v]
                            elif TargetY == -1:
                                a.field[TargetY+self.res][TargetX][v]=df.field[y][x][v]
                            else:
                                a.field[TargetY][TargetX][v]=df.field[y][x][v]
                        elif bc == "bounce-back":
                            # Bounce Back Boundary Conditions

                            vv = [8,7,6,5,4,3,2,1,0]
                            if TargetY == self.res and TargetX == self.res:
                                a.field[y][x][vv[v]] = df.field[y][x][v]
                            elif TargetX == self.res:
                                a.field[y][x][vv[v]] = df.field[y][x][v]
                            elif TargetY == self.res:
                                a.field[y][x][vv[v]] = df.field[y][x][v]
                            elif TargetY == -1 and TargetX == -1:
                                a.field[y][x][vv[v]] = df.field[y][x][v]
                            elif TargetX == -1:
                                a.field[y][x][vv[v]] = df.field[y][x][v]
                            elif TargetY == -1:
                                a.field[y][x][vv[v]] = df.field[y][x][v]
                            else:
                                a.field[TargetY][TargetX][v] = df.field[y][x][v]
            # Calculate macroscopic variables
            for y in range(self.res):
                for x in range(self.res):
                    # Recompute Density Field
                    DensityField[y][x]=sum(a.field[y][x])
                    # Recompute Flow Velocity
                    FlowVelocity=[0,0]
                    for DummyVariable in range(9):
                        FlowVelocity[0]=FlowVelocity[0]+self.DiscreteVelocityVectors[DummyVariable][0]*a.field[y][x][DummyVariable]
                    for DummyVariable in range(9):
                        FlowVelocity[1]=FlowVelocity[1]+self.DiscreteVelocityVectors[DummyVariable][1]*a.field[y][x][DummyVariable]
                    FlowVelocity[0]=FlowVelocity[0]/DensityField[y][x]
                    FlowVelocity[1]=FlowVelocity[1]/DensityField[y][x]
                    # Insert to Velocity Field
                    velocityField[y][x]=FlowVelocity
            grid = self.vis(grid, a, velocityField)


    def vis(self, grid, a, velocityField):
        ft = True
        if grid is None:
            grid = Square().get_grid(self.res,self.res,height=6, buff=.2).set_stroke(width=0)
            ft = False
        ma = 0
        for y in range(self.res):
            for x in range(self.res):
                c = a.Momentum(x,y,velocityField)
                c = math.sqrt(c[0]**2+c[1]**2)
                ma = max(ma,c)
        if ma == 0:
            ma = 1
        for i in range(self.res*self.res):
            c = a.Momentum(i//self.res,i%self.res,velocityField)
            c = math.sqrt(c[0]**2+c[1]**2)/ma
            if c > 1:
                c = .1

            col = '#%02x%02x%02x' % (int(255.999 * math.pow(c, 1.0/2.2)),int(255.999 * math.pow(c, 1.0/2.2)),int(255.999 * math.pow(c, 1.0/2.2))) 
            grid[i].set_fill(col,1)
        self.wait(.01)
        if not(ft):
            self.add(grid)
        return grid
