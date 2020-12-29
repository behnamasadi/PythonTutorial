import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout


def coloring_tree(G):

    visited_list=[]
    for i in G.nodes():
        visited_list.append( g.nodes[i]['visited'] )
    
    graph_color_map=[]
    for i  in visited_list:
        graph_color_map.append('red')
        
    pos =graphviz_layout(G, prog='dot')
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw(G,pos,with_labels=True, arrows=True, node_color =  graph_color_map)
    nx.draw_networkx_edge_labels(G, pos,edge_labels=labels)
    plt.show()
    
    return

g=nx.DiGraph()
g.add_node('a',visited=False)
g.add_node('b',visited=False)
g.add_node('c',visited=False)
g.add_node('d',visited=False)
g.add_node('e',visited=False)
g.add_node('f',visited=False)
g.add_node('g',visited=False)
g.add_node('h',visited=False)
g.add_node('i',visited=False)


g.add_edge('a','b',weight=4)
g.add_edge('a','h',weight=8)


g.add_edge('b','a',weight=4)
g.add_edge('b','c',weight=8)
g.add_edge('b','h',weight=11)


g.add_edge('c','b',weight=8)
g.add_edge('c','d',weight=7)
g.add_edge('c','f',weight=4)
g.add_edge('c','i',weight=2)

g.add_edge('d','d',weight=7)
g.add_edge('d','e',weight=9)
g.add_edge('d','f',weight=14)

g.add_edge('e','d',weight=9)
g.add_edge('e','f',weight=10)

g.add_edge('f','c',weight=4)
g.add_edge('f','d',weight=14)
g.add_edge('f','e',weight=10)
g.add_edge('f','g',weight=2)

g.add_edge('g','f',weight=2)
g.add_edge('g','h',weight=1)
g.add_edge('g','i',weight=6)


g.add_edge('h','a',weight=8)
g.add_edge('g','b',weight=11)
g.add_edge('h','g',weight=1)
g.add_edge('h','i',weight=7)

g.add_edge('i','c',weight=2)
g.add_edge('i','g',weight=6)
g.add_edge('i','h',weight=7)

coloring_tree(g)

