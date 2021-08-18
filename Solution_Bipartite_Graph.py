#!/usr/bin/env python
# coding: utf-8

# In[30]:


from gurobipy import *
import numpy as np
import random
from random import randint
import networkx as nx 
from networkx.algorithms import bipartite
import numpy as np 
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings("ignore", category=UserWarning)


# In[2]:


total_number_of_vertices = int(input("Enter the total number of vertices: "))


# In[3]:


G=nx.Graph()   #Generating the Graph

range_of_vertices= range(total_number_of_vertices) 
vertices_in_list= [*range_of_vertices] 


random.shuffle(vertices_in_list) #Shuffling the vertices

set_1 = vertices_in_list[:total_number_of_vertices//2] #Vertices in Set 1
set_2 = vertices_in_list[total_number_of_vertices//2:] #Vertices in Set 2

print("Set 1: " + str(set_1)) 
print("Set 2: " + str(set_2))
    
random.seed(1)
 
temp_edge0=[]           # Randomnly choosing vertex from set 1 and choosing each vertex from set 2.
for _ in set_1:
    for each in set_2: 
        temp_edge0.append((random.choice(set_1), each))

temp_edge1=[]         #Choosing each vertex from set 1 and randomly choosing vertex from set 2.
for each in set_1:
    for _ in set_2:
        temp_edge1.append((each, random.choice(set_2)))
        
temp_edge = temp_edge0 + temp_edge1       #Combining two list so that we can get a list of edges.

set_of_edges=set(temp_edge)     #Converting to set to avoid duplicate edges if there are any.
edges=(list(set_of_edges))      #Converting set to edges. This is our final edges.
print()
print("Edges: \n" + str(edges)) 
print ()
weighted_edges, cost = multidict ({(i,j): (randint(1,50)) for i,j in edges} #Edges with thier respective random weights or costs.
print("Edges with weight: \n" + str(cost) + str("\t"))


# In[4]:


def MyBipartiteGraph(N):            #Function which returns the graph  
    

    G=nx.Graph() 
    G.add_nodes_from(set_1, bipartite = 0)
    G.add_nodes_from(set_2, bipartite = 0)
    G.add_edges_from(edges) 
    
    
    return (nx.draw_networkx(G, with_labels = True))

    


# In[5]:


def TestBipartiteGraph(G): #Function which return boolean value whether the graph is bipartite or not. 
    
    return ("Is the Graph Bipartite?: " + str(bipartite.is_bipartite(G))) 


# In[28]:


#Calling both the functions.

MyBipartiteGraph(total_number_of_vertices)  #If graph didn't generate, please run this cell again.

TestBipartiteGraph(G)  


# In[7]:


#Gurobi Model

m = Model("Bipartite Graph")  


# In[58]:


#Variables

V={}

for w in weighted_edges: 
    V[w]= m.addVar(vtype=GRB.BINARY, name= "Choose Edge: " + str(w) + " Cost is "+ str(cost[w])) 
    


# In[59]:


#Objectives 

total_cost=0 
for c in weighted_edges: 
    total_cost += V[c] * cost[c]   

m.setObjective(total_cost, GRB.MAXIMIZE) 


# In[60]:


#Constraints for set 1 

for v1 in set_1: 
    sum_v1=0
    for edge in weighted_edges:
        if edge[0] == v1:  
            sum_v1 += V[edge] 
            m.addConstr(sum_v1 <= 1)


# In[61]:


#Constraints for set 2

for v2 in set_2: 
    sum_v2=0   
    for edge in weighted_edges:
        if edge[1] == v2:
            sum_v2 += V[edge] 
            m.addConstr(sum_v2 <=1 ) 


# In[62]:


m.optimize()


# In[65]:


for v in m.getVars():
    if (abs(v.x)> 1e-6):       #Choosing only the valid answers
        print(v.varName, v.x) 


# In[66]:


active_edge = [edge for edge in weighted_edges if V[edge].x == 1 ]

xc= np.random.rand(total_number_of_vertices) * 200
yc= np.random.rand(total_number_of_vertices) * 200

plt.scatter(xc[:], yc[:], c='b') 
for i,j in active_edge:
    plt.plot([xc[i],xc[j]], [yc[i],yc[j]], label = (i,j)) 


# In[ ]:




