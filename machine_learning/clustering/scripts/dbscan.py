'''
Created on Jun 14, 2011

@author: behnam

DBSCAN (Density-Based Spatial Clustering of Applications with Noise) is a data clustering algorithm
It is a density-based clustering algorithm because it finds a number of clusters starting from the 
estimated density distribution of corresponding nodes.

DBSCAN requires two parameters: epsilon (eps) and the minimum number of points required to form a 
cluster (minPts).
It starts with an arbitrary starting point that has not been visited. This point's epsilon-neighborhood 
is retrieved, and if it contains sufficiently many points, a cluster is started. Otherwise, 
the point is labeled as noise.
Note that this point might later be found in a sufficiently sized epsilon-environment of a 
different point and hence be made part of a cluster.
If a point is found to be part of a cluster, its epsilon-neighborhood is also part of that cluster.
Hence, all points that are found within the epsilon-neighborhood are added, as is their own 
epsilon-neighborhood. This process continues until the cluster is completely found. 
Then, a new unvisited point is retrieved and processed, leading to the discovery of a further cluster or noise.


#this is the pseudo code of dbscan which has been implemented:  
#DBSCAN(D, eps, MinPts)
#   C = 0
#   for each unvisited point P in dataset D
#      mark P as visited
#      N = getNeighbors (P, eps)
#      if sizeof(N) < MinPts
#         mark P as NOISE
#      else
#         C = next cluster
#         expandCluster(P, N, C, eps, MinPts)

#expandCluster(P, N, C, eps, MinPts)
#   add P to cluster C
#   for each point P' in N 
#      if P' is not visited
#         mark P' as visited
#         N' = getNeighbors(P', eps)
#         if sizeof(N') >= MinPts
#            N = N joined with N'
#      if P' is not yet member of any cluster
#         add P' to cluster C
'''
import numpy as numpy
import scipy as scipy
from sklearn import cluster
import matplotlib.pyplot as plt



def set2List(NumpyArray):
    list = []
    for item in NumpyArray:
        list.append(item.tolist())
    return list


def GenerateData():
    x1=numpy.random.randn(50,2)
    x2x=numpy.random.randn(80,1)+12
    x2y=numpy.random.randn(80,1)
    x2=numpy.column_stack((x2x,x2y))
    x3=numpy.random.randn(100,2)+8
    x4=numpy.random.randn(120,2)+15
    z=numpy.concatenate((x1,x2,x3,x4))
    return z


def DBSCAN(Dataset, Epsilon,MinumumPoints,DistanceMethod = 'euclidean'):
#    Dataset is a mxn matrix, m is number of item and n is the dimension of data
    m,n=Dataset.shape
    Visited=numpy.zeros(m,'int')
    Type=numpy.zeros(m)
#   -1 noise, outlier
#    0 border
#    1 core
    ClustersList=[]
    Cluster=[]
    PointClusterNumber=numpy.zeros(m)
    PointClusterNumberIndex=1
    PointNeighbors=[]
    DistanceMatrix = scipy.spatial.distance.squareform(scipy.spatial.distance.pdist(Dataset, DistanceMethod))
    for i in xrange(m):
        if Visited[i]==0:
            Visited[i]=1
            PointNeighbors=numpy.where(DistanceMatrix[i]<Epsilon)[0]
            if len(PointNeighbors)<MinumumPoints:
                Type[i]=-1
            else:
                for k in xrange(len(Cluster)):
                    Cluster.pop()
                Cluster.append(i)
                PointClusterNumber[i]=PointClusterNumberIndex
                
                
                PointNeighbors=set2List(PointNeighbors)    
                ExpandClsuter(Dataset[i], PointNeighbors,Cluster,MinumumPoints,Epsilon,Visited,DistanceMatrix,PointClusterNumber,PointClusterNumberIndex  )
                Cluster.append(PointNeighbors[:])
                ClustersList.append(Cluster[:])
                PointClusterNumberIndex=PointClusterNumberIndex+1
                 
                    
    return PointClusterNumber 



def ExpandClsuter(PointToExapnd, PointNeighbors,Cluster,MinumumPoints,Epsilon,Visited,DistanceMatrix,PointClusterNumber,PointClusterNumberIndex  ):
    Neighbors=[]

    for i in PointNeighbors:
        if Visited[i]==0:
            Visited[i]=1
            Neighbors=numpy.where(DistanceMatrix[i]<Epsilon)[0]
            if len(Neighbors)>=MinumumPoints:
#                Neighbors merge with PointNeighbors
                for j in Neighbors:
                    try:
                        PointNeighbors.index(j)
                    except ValueError:
                        PointNeighbors.append(j)
                    
        if PointClusterNumber[i]==0:
            Cluster.append(i)
            PointClusterNumber[i]=PointClusterNumberIndex
    return

#Generating some data with normal distribution at 
#(0,0)
#(8,8)
#(12,0)
#(15,15)
Data=GenerateData()

#Adding some noise with uniform distribution 
#X between [-3,17],
#Y between [-3,17]
noise=scipy.rand(50,2)*20 -3

Noisy_Data=numpy.concatenate((Data,noise))
size=20


fig = plt.figure()
ax1=fig.add_subplot(2,1,1) #row, column, figure number
ax2 = fig.add_subplot(212)

ax1.scatter(Data[:,0],Data[:,1], alpha =  0.5 )
ax1.scatter(noise[:,0],noise[:,1],color='red' ,alpha =  0.5)
ax2.scatter(noise[:,0],noise[:,1],color='red' ,alpha =  0.5)


Epsilon=1
MinumumPoints=20
result =DBSCAN(Data,Epsilon,MinumumPoints)

#printed numbers are cluster numbers
print result
#print "Noisy_Data"
#print Noisy_Data.shape
#print Noisy_Data

for i in xrange(len(result)):
    ax2.scatter(Noisy_Data[i][0],Noisy_Data[i][1],color='yellow' ,alpha =  0.5)
      
plt.show()
