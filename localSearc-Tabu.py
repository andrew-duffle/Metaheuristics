#hill climbing search


#need some python libraries
import copy
from random import Random
import numpy as np


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


# This is the evaluation functions to check if a sultion is tabu based on if we put it in the sack we have to keep it in for 5 solutions attempted
# It will summ ever bit in each tabu list and if the results is 1 or greater you know the item was placed in the bag within the time limit 
#this is then compared to the possition in the solution we are evaluating and if that position is 0 we add a 1 to the Solution_tabu list
#when we sum the list if it is greater than 0 we know at leat one position is tabu making the entire solution tabu. 

def tabu_eval(x):
    for i in range(len(x)):
        if tabu_5[i]+tabu_4[i]+tabu_3[i]+tabu_2[i]+tabu_1[i]>=1 and x[i]==0:
            Solution_tabu.append(1)
            #print "tabu fail"
        else:
            Solution_tabu.append(0)
            #print "tabu good"




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
iterations =0
x_best = x_curr[:]   
f_curr = evaluate(x_curr)[0]
f_best = f_curr
w_best = evaluate(x_curr)[1]

Solution_tabu=[]    #this is a list that hold the evaluated index of the lists

#We create 5 instances of a tabu solution and FIFO them through as we find a solution to move to. so teh tabu tenure is 5
tabu_1=[0]*n
tabu_2=[0]*n
tabu_3=[0]*n
tabu_4=[0]*n 
tabu_5=[0]*n 

#g = open('localSearchResults.csv','w')    #optional: to write results out to a file
     
    
    
while done == 0:
     
    
    Neighborhood = neighborhood(x_curr)   #create a list of all neighbors in the neighborhood of x_curr
    
    for s in Neighborhood:             #evaluate every member in the neighborhood of x_curr
        Solution_tabu=[] #this is here to reset the solutions tabu list since we use a sum below to evaluate if a solutions is tabu
        solutionsChecked = solutionsChecked + 1
        iterations= iterations+1
        if iterations>=n/2:
            tabu_1=[0]*n
            tabu_2=[0]*n
            tabu_3=[0]*n
            tabu_4=[0]*n 
            tabu_5=[0]*n 
            iterations=0
        tabu_eval (s[:]) #tabu evaluation
        #if sum(Solution_tabu)<>0: # this is just to check adn see if solutions are failing 
         #   print "tabu failed"
        if evaluate(s)[0] > f_best and sum(Solution_tabu)==0 :   # This will now check to see if the solution we are evaluating is tabu 
            x_best = s[:]              #find the best member and keep track of that solution
            f_best = evaluate(s)[0]       #and evaluation value
            w_best = evaluate(s)[1]
            #print f_best
            tabu_1=tabu_2 #this is where we FIFO the solutions out as we find another viable option 
            tabu_2=tabu_3
            tabu_3=tabu_4 
            tabu_4=tabu_5 
            tabu_5=(s)[:]
# the else is only need if you do not require the code to find a solution but just evaluate X solutions        
        #else:
         #   tabu_1=tabu_2
          #  tabu_2=tabu_3
           # tabu_3=tabu_4 
            #tabu_4=tabu_5 
            #tabu_5=(s)[:]            
           
    #solutionsChecked>=8000: We might want to try making try X number of times
    if  f_best == f_curr:   #if there were no improving solutions in the neighborhood 
        done = 1
        #print tabu_1
        #print tabu_2
        #print tabu_3
        #print tabu_4
        #print tabu_5
        
    else:
        print "\nTotal number of solutions checked: ", solutionsChecked
        print "Best value found: ", f_best
        print "Best solution: ", x_best
        x_curr = x_best[:]         #else: move to the neighbor solution and continue
        f_curr = f_best            #evalute the current solution
        #g.write('{},{}\n'.format(solutionsChecked, f_best))   #optional: to write out results to a file
    
print "\nFinal: Total number of solutions checked: ", solutionsChecked
print "Best value found: ", f_best
print "Weight:", w_best
#print "Weight of knapsack: ", totalWeight
print "Best solution: ", x_best
print "Number of items selected:", sum(x_best)


#g.close() #optional: to close the external file with results