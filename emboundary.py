import random
import math
import string
import time

class position:
    def __init__(self, xt, yt):
        self.x = xt
        self.y = yt
        
    def distance(self,pos):
        xsq = math.pow(pos.x - self.x,2.0)
        ysq = math.pow(pos.y - self.y,2.0)
        dist = math.sqrt(xsq + ysq)
        return dist
        
    def move(self,pos):
        xt = self.x + pos.x
        yt = self.y + pos.y
        return position(xt, yt)
        
    def inverse(self):
        xt = -self.x
        yt = -self.y
        return position(xt,yt)
    
    def add(self,pos):
        return position(self.x + pos.x, self.y + pos.y)

    def subtract(self,pos):
        return position(self.x - pos.x, self.y - pos.y)
    
    def hasNorm(self, pos):
        self.norm = pos
        
    def dot(self,pos):
        return self.x*pos.x + self.y*pos.y

class particle:
    curPotential = 0
    oldPotential = 0
    
    def __init__(self, pos):
        self.position = pos

        
    def move(self,mova):
        self.position = self.position.move(mova)
        self.lastmov = mova
        
    def revert(self):
        self.position = self.position.move(self.lastmov.inverse())

    
    def potentialContribution(self,pos):
        dist = self.position.distance(pos)
        if dist == 0:
            return 1e10
        return 0.1/dist

class particlearray:
    def __init__(self,numparticles,fixedpos,boundaryx,boundaryy):
        self.boundX = boundaryx
        self.boundY = boundaryy
        self.fixedparticles = [particle(ppos) for ppos in fixedpos]
        self.particles = [particle(position(random.random()*boundaryx,random.random()*boundaryy)) for each in range(numparticles)]
        
    def calcStartingPotentials(self):
        for i in range(len(particles)):
            for j in range(len(fixedparticles)):
                padd = particles(i).potentialContribution(particles[j].position)
                particles(i).curPotential += padd
            for j in range(i,len(particles)):
                padd = particles(i).potentialContribution(particles[j].position)
                particles(i).curPotential += padd
                particles(j).curPotential += padd

    def calcPotentialChange(self,curPar,curMov):
        for i in range(len(self.particles)):
            if(i is not curPar):
                self.particles[i].oldPotential = self.particles[i].curPotential
                self.particles[i].curPotential -= self.particles[i].potentialContribution(self.particles[curPar].position)

        self.particles[curPar].oldPotential = self.particles[curPar].curPotential
        self.particles[curPar].curPotential = 0
        self.particles[curPar].move(curMov)
        for i in range(len(self.particles)):
            if(i is not curPar):
                pot = self.particles[i].potentialContribution(self.particles[curPar].position)
                self.particles[i].curPotential += pot
                self.particles[curPar].curPotential += pot

        for i in range(len(self.fixedparticles)):
            if(i is not curPar):
                self.particles[curPar].curPotential += self.particles[curPar].potentialContribution(self.fixedparticles[i].position)

        return self.particles[curPar].curPotential - self.particles[curPar].oldPotential
                
    def revertPotentials(self):
        for i in range(len(self.particles)):
            self.particles[i].curPotential = self.particles[i].oldPotential
            
        

class simulatedAnnealing:
    def __init__(self,numparticles,fixedpos,bx,by,stepsize,Tstart,Tend,nStep,vList):
        self.parray = particlearray(numparticles,fixedpos,bx,by)
        self.boundX = bx
        self.boundY = by
        self.mSize = stepsize
        self.Temp = Tstart
        self.numSteps = nStep
        self.Tstep = math.exp((math.log(Tend) - math.log(Tstart))/self.numSteps)
        self.vertexList = vList
        zeromove = position(0,0)
        for i in range(len(self.parray.particles)):
            while(not self.checkBoundary(i,zeromove)):
                self.parray.particles[i].position = position(random.random()*bx,random.random()*by)
        
    def move(self, curPar, curMov):
        self.parray.particles[curPar].move(curMov)        

    def chooseParticle(self):
        return random.randint(0,len(self.parray.particles) - 1)
        
    def chooseMove(self):
        if(random.random() > 0.5):
            return position(random.random()*2*self.mSize - self.mSize,random.random()*2*self.mSize - self.mSize)
        else:
            return position(random.random()*2*self.mSize*5 - self.mSize*5,random.random()*2*self.mSize*5 - self.mSize*5)

    def revertMove(self, curPar, curMove):
        movet = curMove.inverse()
        self.move(curPar,movet)
    
    def checkBoundary(self,curPar,curMov):
        curpos = self.parray.particles[curPar].position.add(curMov)
        if(curpos.x < 0 or curpos.x > self.boundX):
            return False
        if(curpos.y < 0 or curpos.y > self.boundY):
            return False

        return self.insidePoly(curpos)

    def insidePoly(self,pos):
        n = len(self.vertexList)
        pos1 = self.vertexList[0]
        flag = False
        for i in range(n + 1):
            pos2 = self.vertexList[i % n]
            minimum = self.minval(pos1,pos2)
            maximum = self.maxval(pos1,pos2)
            if pos.y > minimum.y:
                if pos.y <= maximum.y:
                    if pos.x <= maximum.x:
                        if pos1.y is not pos2.y:
                            xinters = (pos.y - pos1.y)*(pos2.x - pos1.x)/(pos2.y - pos1.y) + pos1.x
                        if pos1.x == pos2.x or pos.x <=xinters:
                            flag = not flag
            pos1 = pos2
        return not flag
    
    def minval(self,pos1,pos2):
        if(pos1.x <= pos2.x):
            x = pos1.x
        else:
            x = pos2.x

        if(pos1.y <= pos2.y):
            y = pos1.y
        else:
            y = pos2.y

        return position(x,y)

    def maxval(self,pos1,pos2):
        if(pos1.x >= pos2.x):
            x = pos1.x
        else:
            x = pos2.x

        if(pos1.y >= pos2.y):
            y = pos1.y
        else:
            y = pos2.y

        return position(x,y)
        
    def evaluateMove(self,curPar,curMov):
        val = -self.parray.calcPotentialChange(curPar,curMov)/self.Temp

        if(val > 0):
            return True
        if(math.exp(val) >= random.random()):
            return True
        else:
            return False
        
    def revertPotential(self):
        self.parray.revertPotentials()

    def saStep(self):
        curPar = self.chooseParticle()
        curMov = self.chooseMove()
        while(not self.checkBoundary(curPar,curMov)):
            curMov = self.chooseMove()
            
        if(not self.evaluateMove(curPar,curMov)):
            self.revertMove(curPar,curMov)
            self.revertPotential()

    def saLoop(self):
        for i in range(self.numSteps):
            self.saStep()
            self.reduceTemp()
        return

    def reduceTemp(self):
        self.Temp = self.Temp*self.Tstep

vList = [position(0.6,0), position(0.4,0), position(0.4,0.6), position(0.2, 1), position(0.3,1), position(0.5,0.6), position(0.7,1), position(0.8,1), position(0.6,0.6)]




fixedpospars = []
#fixedpospars = [position(0.6,0), position(0.4,0), position(0.4,0.6), position(0.2, 1), position(0.3,1), position(0.5,0.75), position(0.7,1), position(0.8,1), position(0.6,0.6)]
attemptone = simulatedAnnealing(500,fixedpospars,1,1,0.1,1e10,1e-6,10000000,vList)
t0 = time.time()
attemptone.saLoop()
t1 = time.time()
timeTot = t1 - t0
print timeTot

f = open('dataX.txt','w')
for each in attemptone.parray.particles:
    f.write("%f\n" % each.position.x)
for each in attemptone.parray.fixedparticles:
    f.write("%f\n" % each.position.x)
f.close()

f = open('dataY.txt','w')
for each in attemptone.parray.particles:
    f.write("%f\n" % each.position.y)
for each in attemptone.parray.fixedparticles:
    f.write("%f\n" % each.position.y)
f.close()


        
            

    
    
