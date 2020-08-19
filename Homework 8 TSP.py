#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import math
import numpy as np
import csv


# In[2]:


distance = []

with open('distance matrix.txt') as f:
    for line in f:
        inner_list = [dis.strip() for dis in line.split('	')]
        distance.append(inner_list)

n = len(distance) 
#convert distances to numeric values:
for i in range(1,n):
    for j in range(1,n):
        distance[i][j] = float(distance[i][j])


# In[3]:


#distance before normalizing:
print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in distance]))


# In[4]:


#now we normalize:
for i in range(1,n):
    m = max(distance[i][1:])
    for j in range(1,n):
        distance[i][j] = round(((distance[i][j]/m) * 2000.0), 5)


# In[5]:


#distance after normalizing:
print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in distance]))


# In[6]:


penalty = [[] for i in distance]
penalty[0].append("	")
for i in range(1,n):
    penalty[0].append("Day_" + str(i))


# In[7]:


# choose a random element from a list
from random import seed
from random import choice
# seed random number generator
values = [0,1]
for i in range(1, n):
    penalty[i].append(distance[i][0])
    for j in range(1, n):
        seed(i+j**2)
        penalty[i].append(choice(values))
        
# or: random.randint(0,1) 


# In[8]:


print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in penalty]))


# In[9]:


#assuming a range of 1-100, I design my penalties as follows
pen_values = [1000, 800, 700, 700]
#pen_a = 1000 this has a high penalty because the point of the problem is to visit all cities
#pen_b = 700 this is relatively high but not as high because skipping a day would lead to inefficiency
#pen_c = 700 also a medium penalty
#pen_d = 700 might be allowed to visit two cities in a day but not too much!


# In[10]:


def calc_penalty(penalty_matrix, distance_matrix, penalty_values):
    n = len(distance_matrix)
    total_penalty = 0
    count_a = 0
    penalty_a = 0
    count_b = 0
    penalty_b = 0
    count_c = 0
    penalty_c = 0
    count_d = 0
    penalty_d = 0
    penalty_e = 0
    
    #Calculate penalty a & c
    for row in range(1,n):
        sum = 0
        for col in range(1,n):
            sum += penalty_matrix[row][col]
        if sum == 0:
            penalty_a += penalty_values[0]
            count_a += 1
            total_penalty += penalty_values[0]
        if sum >= 2:
            penalty_c += penalty_values[2] * (sum - 1)
            count_c += 1
            total_penalty += penalty_values[2] * (sum - 1)
            
            
    #Calculate penalty b & d
    for col in range(1,n):
        sum = 0
        for row in range(1,n):
            sum += penalty_matrix[row][col]
        if sum == 0:
            penalty_b += penalty_values[1]
            count_b += 1
            total_penalty += penalty_values[1]
        if sum >= 2:
            penalty_d += penalty_values[3] * (sum - 1)
            count_d += 1
            total_penalty += penalty_values[3] * (sum - 1)
            
    #calculate penalty e
    for col in range(1,n-1):
        for row in range(1,n):
            for next_day_row in range(1,n):
                if row == next_day_row:
                    continue
                elif penalty_matrix[next_day_row][col+1] == 1:
                    penalty_e += distance_matrix[row][next_day_row]
    total_penalty += penalty_e
    
    print("Penalty A: ", penalty_a, count_a)
    print("Penalty B: ", penalty_b, count_b)
    print("Penalty C: ", penalty_c, count_c)
    print("Penalty D: ", penalty_d, count_d)
    print("Penalty E: ", penalty_e)
    print("Total Penalty: ", total_penalty)
    
    return total_penalty


# In[11]:


def flip(i):
    if i == 0:
        i = 1
    elif i == 1:
        i = 0
    return i


# In[12]:


def annealing_training(t, learning_rate, penalty_matrix, distance_matrix, penalty_values):
    initial_penalty = calc_penalty(penalty_matrix, distance_matrix, penalty_values)
    
    #now we flip a random bit:
    i = random.randint(1,10)
    j = random.randint(1,10)
    penalty_matrix[i][j] = flip(penalty_matrix[i][j])
    
    new_penalty = calc_penalty(penalty_matrix, distance_matrix, penalty_values)
    
    random_number = random.uniform(0,1)
    
    change_in_cost = round((new_penalty - initial_penalty),5)
    try:
        a = 1/(1+math.exp((-1 * change_in_cost)/t))
    except OverflowError:
        a = math.inf
    
    state = "Accept"
    
    if random_number <= a:
        penalty_matrix[i][j] = flip(penalty_matrix[i][j])
        state = "Reject"
        
    t -= round((t * learning_rate),5)
    
    return t, penalty_matrix, state


# In[13]:


def TSP(t, learning_rate, penalty_matrix, distance_matrix, penalty_values):
    iteration = 1
    count = 0
    while count <= 100:
        print("\nNew Iteration: ",  iteration)
        t, penalty_matrix, state = annealing_training(t, learning_rate, penalty_matrix, distance_matrix, penalty_values)
        print(state)
        print("t = ", t)
        if state == "Accept":
            count = 0
        count += 1
        if t <= 0:
            break
        iteration += 1
        
    return penalty_matrix


# In[14]:


#now we implement
t = 5000
learn_rate = 0.01
TSP(t, learn_rate, penalty, distance, pen_values)


# In[15]:


print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in penalty]))

