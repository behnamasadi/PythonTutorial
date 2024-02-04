import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import csv
import numpy as np

def make_label_dict(labels):
    l = {}
    for i, label in enumerate(labels):
        l[i] = label
    return l

input_data = pd.read_csv('data/adjacency_matrix.csv', index_col=0)
#print input_data.head
print input_data.values
G = nx.DiGraph(input_data.values)

with open('data/adjacency_matrix.csv', 'r') as f:
    d_reader = csv.DictReader(f)
    headers = d_reader.fieldnames

#print headers

labels=make_label_dict(headers)
#print labels

edge_labels = dict( ((u, v), d["weight"]) for u, v, d in G.edges(data=True) )
pos = nx.spring_layout(G)
nx.draw(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
nx.draw(G,pos,node_size=500, labels=labels, with_labels=True)
plt.show()


from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
X = csr_matrix(np.array(input_data.values) )
Tcsr = minimum_spanning_tree(X)
MST= Tcsr.toarray().astype(int)
print MST


G_MST = nx.DiGraph(MST)
edge_labels = dict( ((u, v), d["weight"]) for u, v, d in G_MST.edges(data=True) )
pos = nx.spring_layout(G_MST)
nx.draw(G_MST, pos)
nx.draw_networkx_edge_labels(G_MST, pos, edge_labels=edge_labels)
nx.draw(G_MST,pos,node_size=500, labels=labels, with_labels=True)
plt.show()