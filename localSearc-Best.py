


#need some python libraries
import copy
from random import Random
import numpy as np


#to setup a random number generator, we will specify a "seed" value
seed = 12345
myPRNG = Random(seed)

#number of elements in a solution
n = 100

#Create an instance for the knapsack problem
values = []
for i in xrange(0,n):
    values.append(myPRNG.randint(10,100))
    #values.append(myPRNG.uniform(10,100))
    #instead of random, we try uniform distribution
    
weights = []
for i in xrange(0,n):
    weights.append(myPRNG.randint(5,15))
    #weights.append(myPRNG.gauss(15,15))
    
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
        value = maxWeight - totalWeight  
    return [value, totalWeight] #Returning the list

               
#function to create a 1-flip neighborhood of solution x         
def neighborhood(x):
        
    nbrhood = []                 #start with an empty list
    
    for i in xrange(0,n):
        nbrhood.append(x[:])     #Making a copy of the solution, whatever it was
        #Appending the copy to the neibohrhood, each solution stored as a list of neighbors
        if nbrhood[i][i] == 1:   
            nbrhood[i][i] = 0    
        else:
            nbrhood[i][i] = 1
      
    return nbrhood
          


#define the solution variables
x_curr = [] #x_curr will hold the current solution 

#f_curr will hold the "fitness" of the current soluton 
#x_best will hold the best solution 

#Initialize the first random solution
#For every one of the 200 elements, we have a random generator
#So we'll append 200 zeros and ones and append them as a random initial solution
for i in xrange(0,n):
    #x_curr.append(myPRNG.randint(0,1))
    
    #70% chance that it'll be a 0
    if myPRNG.random() < 0.7:
        x_curr.append(0)
    else:
        x_curr.append(1)
        
    
#begin local search overall logic

done = 0

x_best = x_curr[:]   
f_curr = evaluate(x_curr)[0] #first element of the list, because the function returns two values.
w_best = evaluate(x_curr)[1] #now we're evaluating the second value returned
f_best = f_curr
 
 
#Initialize Best Search   
while done == 0:
     
    
    Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr
    
    #This will go through every solution in the neighborhood
    for s in Neighborhood:             #evaluate every member in the neighborhood of x_curr
        solutionsChecked = solutionsChecked + 1
        if evaluate(s)[0] > f_best:   
            x_best = s[:]              #find the best member and keep track of that solution
            f_best = evaluate(s)[0]       #and evaluation value
            w_best = evaluate(s)[1]
    if f_best == f_curr:               #if there were no improving solutions in the neighborhood
        done = 1
    else:
        print "\nTotal number of solutions checked: ", solutionsChecked
        print "Best value found: ", f_best
        print "Best solution: ", x_best        
        x_curr = x_best[:]         #else: move to the neighbor solution and continue
        f_curr = f_best            #evalute the current solution

    
print "\nFinal: Total number of solutions checked: ", solutionsChecked
print "Best value found: ", f_best
print "Weight: ", w_best
#print "Weight of knapsack: ", totalWeight
print "Best solution: ", x_best
print "Number of items selected: ", sum(x_best)

