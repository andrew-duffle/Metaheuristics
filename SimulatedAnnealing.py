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
m_temp = 10

#Defining minimum and maximum temperature
temp_min = 5
temp_max = 50

#We initialize the temperature with the maximum
k_temp = temp_max 

#Stopping Criterion: # of iterations using Simulated Annealing
MaxIterations = 500

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
    # m_temp is the current temperature
    # It begins with our max temp and cools down with each iteration
    while m <= m_temp:
        #Counter for solutions checked thus far
        solutionsChecked = solutionsChecked + 1
        
        #Generate a random solution from Neighborhood
        
        #Establish the neighborhoood for the current solution
        Neighborhood = neighborhood(x_curr) 
        #Get the length of the Neighborhood for the current solution
        nbrhood_length = len(Neighborhood)          
        #Pick a random solution in the neighborhood using random selection
        s_rand = myPRNG.randint(0,nbrhood_length-1)  
        #Random solution in neighborhood becomes s
        s = Neighborhood[s_rand]            
        
        #Check if solution is better than current (better = larger number)
        if evaluate(s)[0] >= evaluate(x_curr)[0]:
            #Random neighborhood solution becomes our current solution
            x_curr = s   
            f_curr = evaluate(s)[0]       
            w_curr = evaluate(s)[1]
            print "\Total number of solutions checked: ", solutionsChecked
            print "Best value found: ", f_best
            print "Weight: ", w_best            
        else:
            #Calculate evaluation difference b/w s and current solution
            delta = abs(evaluate(s)[0] - evaluate(x_curr)[0])   
            #Select a random number between 0 and 1
            E = myPRNG.random()
            
            #First k_temp is Max temperature, decreasing w/ each iteration
            if E <= exp(delta*-1/k_temp):    
                x_curr = s
                f_curr = evaluate(s)[0]       
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
print "Current Temperature ", k_temp
print "E: ", E



