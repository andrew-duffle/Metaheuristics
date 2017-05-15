#particle swarm optimization for Schwefel minimization problem


#need some python libraries
import copy
import math
from random import Random
import time

seedX=[30554,48492,34905,33356,29798,40946,34716,25963,11254,48020,48044,28806,47279,41160,35473,28783,23165,27176,20359,39121,18439,47371,26878,31679,28366,27718,49722,43331,16035,28637]

number=0

for sx in seedX:

      start_time=time.time()
      
      #to setup a random number generator, we will specify a "seed" value
      seed = sx
      myPRNG = Random(seed)
      
      #to get a random number between 0 and 1, write call this:             myPRNG.random()
      #to get a random number between lwrBnd and upprBnd, write call this:  myPRNG.uniform(lwrBnd,upprBnd)
      #to get a random integer between lwrBnd and upprBnd, write call this: myPRNG.randint(lwrBnd,upprBnd)
      
      
      #number of dimensions of problem
      n = 100
      
      #number of particles in swarm
      swarmSize = 15
      
            
      #Schwefel function to evaluate a real-valued solution x    
      # note: the feasible space is an n-dimensional hypercube centered at the origin with side length = 2 * 500
                     
      def evaluate(x):          
            val = 0
            d = len(x)
            for i in xrange(d):
                  val = val + x[i]*math.sin(math.sqrt(abs(x[i])))
                                              
            val = 418.9829*d - val         
                          
            return val          
                
                
      
      #the swarm will be represented as a list of positions, velocities, values, pbest, and pbest values
      
      pos = [[] for _ in xrange(swarmSize)]      #position of particles -- will be a list of lists
      vel = [[] for _ in xrange(swarmSize)]      #velocity of particles -- will be a list of lists
      
      curValue = [] #value of current position  -- will be a list of real values
      pBest = []    #particles' best historical position -- will be a list of lists
      pBestVal = [] #value of pbest position  -- will be a list of real values
      
      
      
      #initialize the swarm randomly
      for i in xrange(swarmSize):
            for j in xrange(n):
                  pos[i].append(myPRNG.uniform(-500,500))    #assign random value between -500 and 500
                  vel[i].append(myPRNG.uniform(-1,1))        #assign random value between -1 and 1
                  
            curValue.append(evaluate(pos[i]))   #evaluate the current position
                                                       
      pBest = pos[:]  # initialize pbest to the starting position
      pBestVal = curValue[:]  # initialize pbest to the starting position
      
      #------------------------------------------------Where we start coding------------------------------------
      # this is to make adding the 2 lists of lists easier we could also use np.matrix but i cant get the matrixs txt off the start
      def addPV(p, v):
            res = []
            for i in range(len(p)):
                  row = []
                  for j in range(len(p[0])):
                        row.append(p[i][j]+v[i][j])
                  res.append(row)
            return res
      
      
      #------Stopping Criteria--------------#
      Improv = 0
      OLDgBestVal = 0.0
      count = 0   #dummy variable
      ImprovCount = 0
      
      
      random1 = myPRNG.random()    # randomizations
      random2 = myPRNG.random()
      
      Inertia=.95  #this controls how much the inertia form the prior velocity factors in
      Social=.95
      Cognitive=.85
      
      solutions_checked=0
      iterations=0
      
      Maxpos=500
      MaxVelocity=500
      
      gBestPos= pBest[pBestVal.index(min(pBestVal))]
      gBestVal= min(pBestVal) #this will be the global best 
      
      Done = 0
      #print vel
      while Done == 0:
      
            for y in range(len(pos)):
                  for i in range(len(pos[0])):
                        vel[y][i]=(Inertia*vel[y][i])+(Cognitive*random1*(pBest[y][i]-pos[y][i]))+(Social*random2*(gBestPos[i]- pos[y][i]))
                        
            #print vel  
            for sublist_v in vel:
                  for v, velocity in enumerate(sublist_v):
                        if velocity>MaxVelocity:
                              sublist_v[v]=MaxVelocity
                        if velocity<-MaxVelocity:
                              sublist_v[v]=-MaxVelocity
            #print vel
      
            # Calculate the next position
            # Add velocity to current positions, and new position is evaluated
            pos=addPV(pos,vel) 
            for sublist in pos:
                  for i, item in enumerate(sublist):
                        if item>Maxpos:
                              sublist[i]=Maxpos
                        if item<-Maxpos:
                              sublist[i]=-Maxpos
                              
                              
                #print "pos",pos     
                        
      
            #evaluate new positions 
            for i in xrange(swarmSize):
                  solutions_checked=solutions_checked+1
                  #print gBestVal
                  curValue[i]=evaluate(pos[i]) #set curValue for partical to the evaluated pos of i
                  #print curValue[i]
                  if curValue[i]<pBestVal[i]: #if the new value of i is less than the current best
                        pBestVal[i]=curValue[i] # set the pbestVal to the curent value
                        pBest[i]=pos[i] #and if the current evaluation is less than pbest value record the current best solution
            
                  
                  if curValue[i]<gBestVal: #evaluate if we have a new global best                 
                        gBestVal=curValue[i] #if it is better update gBest
                        gBestPos=pos[i] #set the global best position
                   
                   
            # ------------------Stopping Criteria------------------------    
            Improv = OLDgBestVal-gBestVal
            #print "OLDgBestVal: ",OLDgBestVal
            #print "gBestVal: ", gBestVal
            OLDgBestVal = gBestVal
            #print "Improvement:",Improv
            # if the improvement in distance is small enough:
            if Improv < 1e-10:
                  # And this also happened on the last iteration 
                  if (iterations - count) == 1:
                        # Then we start counting how many times in a row
                        ImprovCount = ImprovCount + 1
                  else:
                        ImprovCount = 0
                  #We recond what iteration this small change took place, if there was even a change at all
                  count = iterations
                  #If the improvements have been less than 1e-5 for longer than 200 iterations, we exit
                  if ImprovCount > 200:
                        Done = 1
                        #print "ImprovCount: ", ImprovCount 
            else:
                  ImprovCount = 0
                  count = 0
      
      
      
                        
            iterations=iterations+1  #just a counter to know when to stop might want ot base on a criteria
                  
      
      
      
      #print pBest
      #print pBestVal.index(min(pBestVal))
      #print "POS",pos
      #print "VEL",vel
      
      number=number+1
      print number,"-----",seed
      #print gBestPos
      print gBestVal
      print solutions_checked
      #print iterations          
      print( (time.time() - start_time))
      print solutions_checked
                
                                                                          


