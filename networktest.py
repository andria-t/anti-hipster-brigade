import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import networkx as nx #Importing libraries
from networkx.algorithms import bipartite


N = 5000 #Number of edges to show 
with open('edge') as f: #opening edges file (users and biz ids)
    lines = f.readlines() #read lines in file
edgelist = [line.strip().split() for line in lines] #create list of edges

G = nx.Graph() #Create empty graph 
#G.add_nodes_from(usernodes, bipartite = 0)
#G.add_nodes_from(biznodes, bipartite = 0)
G.add_edges_from(edgelist)

#Is the graph bipartite?
print(bipartite.is_bipartite(G))


#make list of degrees of all user nodes
usernodes = []
for pair in G.degree: 
    if "user" in pair[0]:
        usernodes.append(pair[1]) 

#Plot degree histogram of users
plt.hist(usernodes, 500)

plt.show()
