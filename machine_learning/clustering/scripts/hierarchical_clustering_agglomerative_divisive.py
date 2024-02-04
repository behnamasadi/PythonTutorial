#https://stackoverflow.com/questions/21638130/tutorial-for-scipy-cluster-hierarchy
import scipy.cluster.hierarchy as hierarchal_clustering
import matplotlib.pyplot as plt
 
data=[ [0],[1],[2],[3],[4] ]
data_dict = {'A':0,'B':1,'C':2,'D':3,'E':4}
data_labels = [data_dict.keys()[data_dict.values().index(i)] for i in range(0, len(data_dict))]
 
metric='euclidean' 
method='complete'
plt.title(method)
hierarchal_clusteringlink = hierarchal_clustering.linkage(data,method,metric)
dendro = hierarchal_clustering.dendrogram(hierarchal_clusteringlink,labels=data_labels)
plt.show()
 
method='centroid'
plt.title(method)
hierarchal_clusteringlink = hierarchal_clustering.linkage(data,method,metric)
dendro = hierarchal_clustering.dendrogram(hierarchal_clusteringlink,labels=data_labels)
plt.show()