from ete2 import ClusterTree, TreeStyle
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations
from scipy.spatial.distance import pdist
from scipy.spatial import distance_matrix

#https://en.wikipedia.org/wiki/Newick_format
#The tree, in string format (the corresponding graph is drawn in the image/NewickExample.png)
tree = ClusterTree('(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);')

#Distance matrix for this example is:
#distance_matrix=
# [[0.0, 0.3, 0.9, 1.0],
#  [0.3, 0.0, 1.0, 1.1],
#  [0.9, 1.0, 0.0, 0.7],
#  [1.0, 1.1, 0.1, 0.0]]

#the distance_matrix can be easlily made up by the following lines:
data=[ [0.1],[0.2],[0.3],[0.4],[0.5] ]
#print distance_matrix(data,data)

#the linkage matrix can be easlily made up by the following lines:
#print pdist(data)

leaves = tree.get_leaf_names()
ts = TreeStyle()
ts.show_leaf_name=True
ts.show_branch_length=True
ts.show_branch_support=True

tree.show(tree_style=ts)
