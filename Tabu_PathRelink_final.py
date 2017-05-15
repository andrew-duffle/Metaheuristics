#hill climbing search


#need some python libraries
import copy
from random import Random
import numpy as np
import time

#to setup a random number generator, we will specify a "seed" value
seed = 12345
myPRNG = Random(seed)

#to get a random number between 0 and 1, write call this:             myPRNG.random()
#to get a random number between lwrBnd and upprBnd, write call this:  myPRNG.uniform(lwrBnd,upprBnd)
#to get a random integer between lwrBnd and upprBnd, write call this: myPRNG.randint(lwrBnd,upprBnd)


#number of elements in a solution
n = 100

      

#let's create an instance for the knapsack problem
values = []
for i in xrange(0,n):
    values.append(myPRNG.randint(10,100))
    
weights = []
for i in xrange(0,n):
    weights.append(myPRNG.randint(5,15))

#define max weight for the knapsack
maxWeight = 4*n


#monitor the number of solutions evaluated
solutionsChecked = 0


#function to evaluate a solution x
def evaluate(x):
    
    a=np.array(x)
    b=np.array(values)
    c=np.array(weights)

    value = np.dot(a,b)          #compute the cost value of the knapsack selection
    totalWeight = np.dot(a,c)    #compute the weight value of the knapsack selection

    if totalWeight > maxWeight:
        value =  maxWeight-totalWeight

    return [value,totalWeight]


#function to create a 1-flip neighborhood of solution x
def neighborhood(x):

    nbrhood = []
    
    for i in xrange(0,n):
        nbrhood.append(x[:])
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1

    return nbrhood

#We create 5 instances of a tabu solution and FIFO them through as we find a solution to move to. so teh tabu tenure is 5
tabu_1=[0]*n
tabu_2=[0]*n
tabu_3=[0]*n
tabu_4=[0]*n
tabu_5=[0]*n

def tabu_eval(x):
    for i in range(len(x)):
        if tabu_5[i]+tabu_4[i]+tabu_3[i]+tabu_2[i]+tabu_1[i]>=1 and x[i]==0:
            Solution_tabu.append(1)
            #print "tabu fail"
        else:
            Solution_tabu.append(0)
            #print "tabu good"

#functuon for Path Re-linking
def pathRelink (x1,x2): #This function requires two solution variables
    #diff = [] #An index of the indexes with differences between solutions
    #delta = [] #A list of solutions
    #initalize variables
    y = 0
    best = 0
    instance = 0
    sol_count = 0
    start = 0
    out = 0 # initialive exit variable
    #initialize containers
    p_best = []
    bes_sol = []
    xs = []
    xt = []
    xs = x1[:] #for convieniance in changing variables
    xt = x2[:] #for convieniance in changing variables
    #print xs
    #print xt
    diff = []
    while out == 0:  #continue until exit criteria met
        #internal variables that reset with every loop
        diff = [] #list of indexes
        delta = [] #list of possible path solutions
        big1 = [] #list of solution values
        big2 = 0 #holds a single solution value for comparison

        for i in xrange(0,n): #first loop compaires all elements in both functions and marks the index where differences occur

            if xs[i] != xt[i]:
                y = i
                diff.append(y)

        for r in range(len(diff)): #second loop creates an neighborhood that only contains solutions that are unique to both solutions
            delta.append(xs[:])
            flp = diff[r] #Index to be flipped
            if xs[flp] == 1 :
                delta[r][flp]=0
            else:
                delta[r][flp]=1
        g=0 #counting variable initalized just prior to entering the loop

        for s in delta: #third loop evaluates the solutions within delta
            sol_count = sol_count + 1
            big1.append(evaluate(s)[0])

            if big1[g] > big2: #is the next selected value greater than the last great value
                best = s[:]
                bes_sol.append(best)
                p_best.append(big1[g])
                big2 = big1[g]
            g=g+1
        xs = best

        if delta == [xt]: #exit criteria
            t=p_best.index(max(p_best))
            x_best = bes_sol[t]
            out =1
        instance = instance +1
      #  if instance == 100:
      #      t=p_best.index(max(p_best))
      #      x_best = bes_sol[t]
      #      print "A best path value ", max(p_best)
      #      out=1
    n_best = max(p_best) #best solution during pathRelinking
    print "A best path value ", n_best
    return [x_best,sol_count,n_best ]

#define the solution variables
x_curr = [] #x_curr will hold the current solution
x_dest = [] #this is the destination set

#start with a random solution
def randSolution (x):
    x=[]
    for i in xrange(0,n):

        if myPRNG.random() < 0.7:
            x.append(0)

        else:
            x.append(1)
    return x

#begin local search overall logic
#Initalize variables
done = 0 # initialive exit variable
x_best = 0 #x_best will hold the best solution
f_curr = 0 #f_curr will hold the "fitness" of the current soluton
f_best = 0 #f_best will hold the "fitness" of the best soluton
w_best = 0 #x_best will hold the "weight" of the best soluton
sol_add = 0 #carries solutions checked from pathRelink to Local Search solutions checked
n_best = 0 #the new best solution carried over from pathRelink
iterations = 0 #counts the number of iterations in a single loop. the value resets
Solution_tabu=[] #this is a list that hold the evaluated index of the lists
results = [] #carries the list of results from a single run of pathRelink
x_curr = randSolution(x_curr) #produces our first random solution

#Start Local Search with integrated Tabu Search
while done == 0:
    x_dest = randSolution(x_dest)
    Neigh = neighborhood(x_curr) #create a list of all neighbors in the neighborhood of x_curr
    
    for s in Neigh:              #evaluate only those members in the neighborhood from x_curr to y
        Solution_tabu=[] #this is here to reset the solutions tabu list since we use a sum below to evaluate if a solutions is tabu
        solutionsChecked = solutionsChecked + sol_add + 1
        iterations= iterations+1
        
        if iterations>=n/2:
            tabu_1=[0]*n
            tabu_2=[0]*n
            tabu_3=[0]*n
            tabu_4=[0]*n
            tabu_5=[0]*n
            iterations=0
        tabu_eval (s[:]) #tabu evaluation
        
        if evaluate(s)[0] > f_best and sum(Solution_tabu)==0 :   # This will now check to see if the solution we are evaluating is tabu
            x_best = s[:]               #find the best member and keep track of that solution
            f_best = evaluate(s)[0]     #and evaluation value
            w_best = evaluate(s)[1]
            tabu_1=tabu_2 #this is where we FIFO the solutions out as we find another viable option
            tabu_2=tabu_3
            tabu_3=tabu_4
            tabu_4=tabu_5
            tabu_5=(s)[:]
            print "Best value found: ", f_best
            print iterations
            
            if iterations>5: #criteria for entering pathRelink
                results = pathRelink(x_curr, x_dest)[:]
                x_curr = results[0]
                sol_add = results[1]
                n_best = results[2]
                iterations=0
                start=0
                
                if f_best < n_best:
                    f_curr = n_best
            continue
          
        else:
            x_curr = x_best
            
    if f_best == f_curr:#if there were no improving solutions in the neighborhood
        print "next"
        done = 1

    else:
        print "\nTotal number of solutions checked: ", solutionsChecked
        print "Best value found: ", f_best
        #print "Best solution: ", x_best
        x_curr = x_best[:]         #else: move to the neighbor solution and continue
        f_curr = f_best            #evalute the current solution
     
print "\nFinal: Total number of solutions checked: ", solutionsChecked
print "Best value found: ", f_best
print "Weight:", w_best
#print "Best solution: ", x_best
print "Number of items selected:", sum(x_best)

