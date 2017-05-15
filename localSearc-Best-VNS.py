

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

#Function to create a 2 flip Neighborhood  
def neighborhood1(x):
    nbrhood = []  
    for i in xrange(0,n):
        nbrhood.append(x[:])
        #First Flip for solution i, index i
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1            
    return nbrhood

#Function to create a 2 flip Neighborhood  
def neighborhood2(x):
    nbrhood = []  
    for i in xrange(0,n):
        nbrhood.append(x[:])
        #First Flip for solution i, index i
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1         
    #Second Flip for soltuion i, index i+1
    start = 0
    finish = 1
    while start < finish:
            if nbrhood[start][finish] == 1:
                nbrhood[start][finish] = 0
            else:
                nbrhood[start][finish] = 1    
            start = start + 1
            finish = finish + 1
            if finish == 5:
                if nbrhood[start][0] == 1:
                    nbrhood[start][0] = 0
                else:
                    nbrhood[start][0] = 1             
                start = finish    
    return nbrhood

#Function to create a 3 flip Neighborhood  
def neighborhood3(x):
    nbrhood = []  
    for i in xrange(0,n):
        nbrhood.append(x[:])
        #First Flip for solution i, index i
        if nbrhood[i][i] == 1:
            nbrhood[i][i] = 0
        else:
            nbrhood[i][i] = 1         
    #Second Flip for soltuion i, index i+1
    start = 0
    finish = 1
    while start < finish:
            if nbrhood[start][finish] == 1:
                nbrhood[start][finish] = 0
            else:
                nbrhood[start][finish] = 1    
            start = start + 1
            finish = finish + 1
            if finish == 5:
                if nbrhood[start][0] == 1:
                    nbrhood[start][0] = 0
                else:
                    nbrhood[start][0] = 1             
                start = finish 
    #Third Flip for soltuion i, index i+1
    start = 0
    finish = 2
    while start < finish:
            if nbrhood[start][finish] == 1:
                nbrhood[start][finish] = 0
            else:
                nbrhood[start][finish] = 1    
            start = start + 1
            finish = finish + 1
            if finish == n:
                if nbrhood[start][0] == 1:
                    nbrhood[start][0] = 0
                else:
                    nbrhood[start][0] = 1
                start = start + 1
                if nbrhood[start][1] == 1:
                    nbrhood[start][1] = 0
                else:
                    nbrhood[start][1] = 1                 
                start = finish
     
    return nbrhood



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
     
    print"x_curr", x_curr
    Neighborhood1 = neighborhood1(x_curr)   #create a list of all neighbors in the neighborhood1 of x_curr
    Neighborhood2 = neighborhood2(x_curr)   #create a list of all neighbors in the neighborhood2 of x_curr
    Neighborhood3 = neighborhood3(x_curr)   #create a list of all neighbors in the neighborhood3 of x_curr
    print"Neighborhood1", Neighborhood1
    print"Neighborhood2", Neighborhood2
    print"Neighborhood3", Neighborhood3
    #evaluate every member in the FIRST neighborhood of x_curr
    for s in Neighborhood1:
        solutionsChecked = solutionsChecked + 1
        if evaluate(s)[0] > f_best: 
            #find the best member and keep track of that solution
            x_best = s[:]              
            f_best = evaluate(s)[0]       #and evaluation value
            w_best = evaluate(s)[1]
    #evaluate every member in the SECOND neighborhood of x_curr
    for s in Neighborhood2:
        solutionsChecked = solutionsChecked + 1
        if evaluate(s)[0] > f_best: 
            #find the best member and keep track of that solution
            x_best = s[:]              
            f_best = evaluate(s)[0]       #and evaluation value
            w_best = evaluate(s)[1]
    #evaluate every member in the THIRD neighborhood of x_curr
    for s in Neighborhood3:
        solutionsChecked = solutionsChecked + 1
        if evaluate(s)[0] > f_best: 
            #find the best member and keep track of that solution
            x_best = s[:]              
            f_best = evaluate(s)[0]       #and evaluation value
            w_best = evaluate(s)[1]     
    
    if f_best == f_curr:               #if there were no improving solutions in the neighborhood
        done = 1
        
    else:
        print "\nTotal number of solutions checked: ", solutionsChecked
        print "Best value found: ", f_best
        x_curr = x_best[:]         #else: move to the neighbor solution and continue
        f_curr = f_best            #evalute the current solution
        
    
print "\nFinal: Total number of solutions checked: ", solutionsChecked
print "Best value found: ", f_best
print "Weight:", w_best
print "Number of items selected:", sum(x_best)

