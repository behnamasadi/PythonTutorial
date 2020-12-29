import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import csv


def make_label_dict(labels):
    l = {}
    for i, label in enumerate(labels):
        l[i] = label
    return l

input_data = pd.read_csv('data/adjacency_matrix.csv', index_col=0)
#print input_data.head
print (input_data.values)
G = nx.Graph(input_data.values)

with open('data/_adjacency_matrix.csv', 'r') as f:
    d_reader = csv.DictReader(f)
    headers = d_reader.fieldnames

#print headers

labels=make_label_dict(headers)
#print labels

edge_labels = dict( ((u, v), d["weight"]) for u, v, d in G.edges(data=True) )
pos = nx.spring_layout(G)
#pos = nx.draw_kamada_kawai(G)

graph_color_map=['blue','blue','red','blue','red','blue','blue','red','blue']
#graph_color_map.append(color)


print(labels)
print(edge_labels)
nx.draw(G,pos,edge_labels=edge_labels ,arrows=True,node_color =  graph_color_map )
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, arrows=True, arrowstyle='-|>', arrowsize=10)

labels = nx.get_edge_attributes(G,'weight')
print(labels)

plt.show()
