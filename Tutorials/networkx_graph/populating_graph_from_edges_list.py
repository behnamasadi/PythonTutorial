import networkx as nx
import matplotlib.pyplot as plt

G = nx.read_edgelist("data/edges.txt", delimiter=",", data=[("weight", int)]) 
G.edges(data=True)

edge_labels = dict( ((u, v), d["weight"]) for u, v, d in G.edges(data=True) )
pos = nx.random_layout(G)
nx.draw(G, pos)
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.show()