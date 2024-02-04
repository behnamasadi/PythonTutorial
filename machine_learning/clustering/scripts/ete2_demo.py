#https://en.wikipedia.org/wiki/Newick_format
#https://stackoverflow.com/questions/31033835/newick-tree-representation-to-scipy-cluster-hierarchy-linkage-matrix-format?rq=1
from ete2 import ClusterTree, TreeStyle
import scipy.cluster.hierarchy as sch
import scipy.spatial.distance
import matplotlib.pyplot as plt
import numpy as np
from itertools import combinations


tree = ClusterTree('(A:0.1,B:0.2,(C:0.3,D:0.4):0.5);')
leaves = tree.get_leaf_names()
ts = TreeStyle()
ts.show_leaf_name=True
ts.show_branch_length=True
ts.show_branch_support=True

idx_dict = {'A':0,'B':1,'C':2,'D':3}
idx_labels = [idx_dict.keys()[idx_dict.values().index(i)] for i in range(0, len(idx_dict))]

#just going through the construction in my head, this is what we should get in the end
my_link = [[0,1,0.3,2],
        [2,3,0.7,2],
        [4,5,1.0,4]]

my_link = np.array(my_link)


dmat = np.zeros((4,4))

for l1,l2 in combinations(leaves,2):
    d = tree.get_distance(l1,l2)
    dmat[idx_dict[l1],idx_dict[l2]] = dmat[idx_dict[l2],idx_dict[l1]] = d

print 'Distance:'
print dmat


schlink = sch.linkage(scipy.spatial.distance.squareform(dmat),method='average',metric='euclidean')

print 'Linkage from scipy:'
print schlink

print 'My link:'
print my_link

print 'Did it right?: ', schlink == my_link

dendro = sch.dendrogram(my_link,labels=idx_labels)
plt.show()

tree.show(tree_style=ts)
