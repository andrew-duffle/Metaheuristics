#hill climbing search
#ISE 5113 HW 4
#Andrew Duffle, Edward Ellsworth, & Ana Santiago

#need some python libraries
import copy
from random import Random
import numpy as np


#to setup a random number generator, we will specify a "seed" value
seed = 12345
myPRNG = Random(seed)

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
          

#Start random restart here

restarts=15 #set the number of restarts we want to attempt

best_restart_Objective = 0  #this will hold the best solution we find out of all the iterations
best_restart_iterations = 0 #this will hold the number of iterations in teh best solution 
best_Objesctive_stoe = []   #this will hold a list of best solution values from each iteration
total_iterations_all = 0    #this will count all the iteration performed


for r in xrange (0,restarts):
    
    #define the solution variables
    x_curr = [] #x_curr will hold the current solution 
    
    #f_curr will hold the "fitness" of the current soluton 
    #x_best will hold the best solution    
    
    #start with a random solution
    for i in xrange(0,n):
        #x_curr.append(myPRNG.randint(0,1))
        
        if myPRNG.random() < 0.7:
            x_curr.append(0)
        else:
            x_curr.append(1)
        
    
    #begin local search overall logic
    
    done = 0
    
    x_best = x_curr[:]   
    f_curr = evaluate(x_curr)[0]
    f_best = f_curr
    w_best = evaluate(x_curr)[1]
        
             
    while done == 0:
                
        Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr
        
        for s in Neighborhood:             #evaluate every member in the neighborhood of x_curr
            solutionsChecked = solutionsChecked + 1
            if evaluate(s)[0] > f_best:   
                x_best = s[:]              #find the best member and keep track of that solution
                f_best = evaluate(s)[0]       #and evaluation value
                w_best = evaluate(s)[1]
        
        if f_best == f_curr:               #if there were no improving solutions in the neighborhood
            done = 1
        else:
            #print "\nTotal number of solutions checked: ", solutionsChecked
            #print "Best value found: ", f_best
            #print "Best solution: ", x_best        
            x_curr = x_best[:]         #else: move to the neighbor solution and continue
            f_curr = f_best            #evalute the current solution
        
    
    if f_best > best_restart_Objective:
        best_Objesctive_stoe.append(f_best) # keep track of best values
        best_restart_Objective = max( best_Objesctive_stoe)# best value produced during iterations
    print " \nFinal:Total number of solutions checked: ", solutionsChecked
    print "Best value found: ", f_best
   
    
    #print "Weight:", w_best
    #print "Weight of knapsack: ", totalWeight
    #print "Best solution: ", x_best
    #print "Number of items selected:", sum(x_best)
    


print "\nFinal:Best value found: ",best_restart_Objective 
print "Final:Total number of solutions checked: ", solutionsChecked
#print "Total solutions checked over all restarts",total_iterations_all
#print "Weight of knapsack: ", totalWeight
print "Number of restarts",restarts

