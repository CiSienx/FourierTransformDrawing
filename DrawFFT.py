import numpy as np
import json

size = (700, 700)
Switch = True
load = True
coord = []
position = (350,350)
aqurcy = 100
file = open("venv/coordinate_love.txt","r")

pg.init()
screen = pg.display.set_mode((size))
trail = pg.Surface((size))
epicircle = pg.Surface((size))


def FFT(coords):
    N = len(coords)
    phi = -np.pi/N
    A_F_P = []          #Amplitude, Frequency, Phase
    for i in range(1-N,N):
        F = i
        ansX = 0
        ansY = 0
        for j in range(1-N,N):
            ansX += coords[j][0]*np.cos(phi*j*i) - coords[j][1]*np.sin(phi*i*j)
            ansY += coords[j][1]*np.cos(phi*i*j) + coords[j][0]*np.sin(phi*j*i)
        ansX /= 2*N
        ansY /= 2*N
        A = np.sqrt(ansY**2 + ansX**2)
        P = np.arctan2(ansY,ansX) + np.pi
        A_F_P.append([A,F,P])
    return A_F_P

class Arms:
    def __init__(self,pos,amp,color,phase,fre):
        self.pos = pos
        self.amp = amp
        self.color = color
        self.phase = phase
        self.time = 0
        self.fre = fre
        self.dt = 0.001
    def rotate(self,pos):
            self.c = pg.draw.circle(epicircle, self.color, pos, self.amp, 1)
            self.l = pg.draw.line(epicircle, self.color, pos, (pos[0] + np.cos(self.phase + self.fre*self.time) * self.amp,pos[1] + np.sin(self.phase + self.fre*self.time) * self.amp))
            self.time += self.dt
            self.pos = pos

    def position(self):
        return ((self.pos[0] + np.cos(self.phase + self.fre*(self.time-self.dt)) * self.amp,self.pos[1] + np.sin(self.phase + self.fre*(self.time-self.dt)) * self.amp))

def Loading(x,position):
    A_F_P = FFT(x)
    A_F_P.sort(reverse=True)
    color = (220,220,0,255)
    for i in range(len(A_F_P)):
        globals()["arm"+str(i)] = Arms(position,A_F_P[i][0],color,A_F_P[i][2],A_F_P[i][1])
        if i > 0:
            position = globals()["arm"+str(i-1)].position()
    return len(A_F_P)

while Switch:
                            # beginning position
    if load:
        new_coord = []
        coord = []
        coord = np.asarray(json.load(file))
        #coord.resize((200,2))
        print("No. of coordnates"+str(len(coord)))
        for i in range(0, int(len(coord))):
            new_coord.append((250 - coord[i][0],250 - coord[i][1]))
        arm_no = Loading(new_coord,position)
        aqurcy = int(arm_no*(100-aqurcy)/100)
        print("No. of circles "+str(arm_no - aqurcy))
        load = False

                            # update rotation
    screen.fill((0, 0, 0))
    epicircle.fill((0,0,0))
    epicircle.set_alpha(110)
    for i in range(arm_no-aqurcy):
        if i > 0:
            globals()["arm"+str(i)].rotate(globals()["arm"+str(i-1)].position())
            if i == arm_no - aqurcy - 1:
                pg.draw.circle(trail,(0,200,220),globals()["arm"+str(i)].position(),1)
        else:
            globals()["arm"+str(i)].rotate(position)
    screen.blit(trail, (0, 0))
    screen.blit(epicircle,(0,0))
    pg.display.flip()
