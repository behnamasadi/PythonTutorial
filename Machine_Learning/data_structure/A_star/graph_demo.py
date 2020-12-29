import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout


def coloring_tree(G):

    visited_list=[]
    for i in G.nodes():
        visited_list.append( g.nodes[i]['visited'] )
    
    graph_color_map=[]
    for i  in visited_list:
        if i:
            color='blue'
        else:
            color='red'
        graph_color_map.append(color)
    pos =graphviz_layout(G, prog='dot')
    nx.draw(G, pos, with_labels=True, arrows=True,node_color =  graph_color_map)
    #plt.savefig('nx_test.png')
    plt.show()
    
    return

def DFS_travrse(N,G):
    neighbors =G.neighbors(N)
    size=len( list(neighbors))
    if size==0:
        return
    neighbors =G.neighbors(N)
    for neighbor in neighbors:
        G.nodes[neighbor]['visited']=True
        coloring_tree(G)
        DFS_travrse(neighbor,G)
    return

def BFS_travrse(Q,G):
    if len(Q)==0:
        return
    Root=Q[0]
    Q=Q[1:len(Q)]
    neighbors =G.neighbors(Root)
    for neighbor in neighbors:
        print neighbor
        coloring_tree(G)
        G.nodes[neighbor]['visited']=True
        Q.append(neighbor)
 
    BFS_travrse(Q,G)
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


g.add_edge('a','b')
g.add_edge('a','c')
g.add_edge('b','e')
g.add_edge('b','d')
g.add_edge('e','h')
g.add_edge('c','f')
g.add_edge('c','g')




#Root='a'
#g.nodes[Root]['visited']=True
#print Root 
#Q=[Root]
#BFS_travrse(Q,g)


Root='a'
print Root
g.nodes[Root]['visited']=True
coloring_tree(g)
DFS_travrse(Root,g)




    
    
    