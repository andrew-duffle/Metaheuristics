#hill climbing search


#need some python libraries
import copy
from random import Random
import numpy as np
from math import exp, expm1 

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
        value = maxWeight - totalWeight   
    return [value, totalWeight] #Returning the list

          
       
#function to create a 1-flip neighborhood of solution x         
def neighborhood(x):
        
    nbrhood = []                 #start with an empty list
    
    for i in xrange(0,n):
        nbrhood.append(x[:])     
        if nbrhood[i][i] == 1:   
            nbrhood[i][i] = 0    
        else:
            nbrhood[i][i] = 1
      
    return nbrhood


#Define cooling schedule
def cooling(x):
    k_temp = 0.98*(x)
    return k_temp

#Define number of iterations per temperature
m_temp = 20

#Defining minimum and maximum temperature
temp_min = 500
temp_max = 50000

#We initialize the temperature with the maximum
k_temp = temp_max 

#Stopping Criterion: # of iterations using Simulated Annealing
MaxIterations = 300

#define the solution variables
x_curr = [] #x_curr will hold the current solution 

#f_curr will hold the "fitness" of the current soluton 
#x_best will hold the best solution 

#Initialize the first random solution
for i in xrange(0,n):
    if myPRNG.random() < 0.7:
        x_curr.append(0)
    else:
        x_curr.append(1)

x_best = x_curr[:]   
f_curr = evaluate(x_curr)[0] #first element of the list, because the function returns two values.
w_best = evaluate(x_curr)[1] #now we're evaluating the second value returned
f_best = f_curr

#Begin the Simulated Annealing Iterations
k = 0
while k <= MaxIterations:
    m = 0
    while m <= m_temp:
        solutionsChecked = solutionsChecked + 1
        #Generate a random solution from Neighborhood
        Neighborhood = neighborhood(x_curr) #Establish the neighborhoood for the current solution
        nbrhood_length = len(Neighborhood)  #Get the length of the Neighborhood for the current solution
        s_rand = myPRNG.randint(0,nbrhood_length-1)  #Pick a random solution in the neighborhood using random selection
        s = Neighborhood[s_rand]            #Random solution in neighborhood becomes s
        if evaluate(s)[0] >= evaluate(x_curr)[0]:  #if this solution is better than our current solution (better = larger number)
            x_curr = s   #Random neighborhood solution becomes our current solution
            f_curr = evaluate(s)[0]       #and evaluation value
            w_curr = evaluate(s)[1] 
        else:
            delta = abs(evaluate(s)[0] - evaluate(x_curr)[0])   #Calculate evaluation difference between Random Nbor solution and current solution
            E = myPRNG.random()     #Select a random number between 0 and 1
            if E <= exp(delta*-1/k_temp):    #First k_temp is Maximum temperature, value will change for the next iteration
                x_curr = s
                f_curr = evaluate(s)[0]       #and evaluation value
                w_curr = evaluate(s)[1]                 
                k_temp = cooling(k_temp)  #Return next cooling temperature
                
        m = m + 1
    k = k + 1

x_best = x_curr
f_best = f_curr
w_best = w_curr

print "\nFinal: Total number of solutions checked: ", solutionsChecked
print "Best value found: ", f_best
print "Weight: ", w_best
print "Best solution: ", x_best
print "Number of items selected: ", sum(x_best)
print "delta: ", delta
print "E: ", E



