import matplotlib.pyplot as pyplot
import numpy as numpy
from sklearn import cluster
import math as math
import sys
from scipy.cluster.vq import vq, kmeans, whiten,kmeans2
import scipy as scipy
'''
please read this documentation for more info about kmean algorithm
http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans.html#scipy.cluster.vq.kmeans
http://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.vq.kmeans2.html#scipy.cluster.vq.kmeans2
'''


def Combination(n,r):
    if n<r: 
        return 0 
    else :
        return math.factorial(n)/( math.factorial(n-r) * math.factorial(r ))


def GenerateData():
    x1=numpy.random.randn(50,2)
    x2x=numpy.random.randn(80,1)+2
    x2y=numpy.random.randn(80,1)-2
    x2=numpy.column_stack((x2x,x2y))
    x3=numpy.random.randn(100,2)+8
    x4=numpy.random.randn(120,2)+15
    z=numpy.concatenate((x1,x2,x3,x4))
    return z




def ShowDataWithOptimalCenters(Data,OptimalCenters):
    pyplot.scatter(Data[:,0],Data[:,1])
    pyplot.scatter(OptimalCenters[:,0],OptimalCenters[:,1],color='red')
    pyplot.show()
    return


def oldClusteringWithC_Index(Data,NumberOfClusters,NumberofIterationsForCindex,DistanceBetweenAllPairNodesSorted,DistanceMethod='euclidean'):
    NumberOfClusters=NumberOfClusters
    x=Data
    NumberofIterationsForCindex=NumberofIterationsForCindex
    NUmberOfNodesInTheClusters=0
    D=DistanceBetweenAllPairNodesSorted
    OptimalCenter=[]
    
    C=1
    Old_C=sys.maxint
    Scl=0
    N=0
    Smin=0
    Smax=0


    for NumberofIterations in xrange(NumberofIterationsForCindex):
        #init : {'k-means++', 'random', 'points','matrix'}
        #'k-means++' : selects initial cluster centers for k-mean clustering in a smart way to speed up convergence
        # http://scikit-learn.sourceforge.net/modules/generated/scikits.learn.cluster.KMeans.html#scikits.learn.cluster.KMeans
        classifier=cluster.KMeans(k=NumberOfClusters, init='random', n_init=10, max_iter=300, tol=0.0001, verbose=0, random_state=None, copy_x=True)
        y=classifier.fit(x)
        for i in xrange( NumberOfClusters ):
#            print 'NumberofIterations'
#            print NumberofIterations
#            print 'NumberOfClusters'
#            print NumberOfClusters
#            print 'classifier.cluster_centers_'
#            print classifier.cluster_centers_
            NUmberOfNodesInTheClusters=len(x[numpy.where(classifier.labels_==i)])
            Scl=Scl+numpy.sum( scipy.spatial.distance.pdist(x[numpy.where(classifier.labels_==i)], DistanceMethod))
            N=N+Combination(NUmberOfNodesInTheClusters, 2)
        Smin=numpy.sum( D[0:N:1])
        Smax=numpy.sum(D[len(D)-N::1])
        if(Smax-Smin==0):
            continue
        
        C=(Scl-Smin)/(Smax-Smin)
        Scl=0
        N=0
        Smin=0
        Smax=0
        if(C<Old_C):
            Old_C=C
            OptimalCenter=classifier.cluster_centers_[:]

    
    return OptimalCenter,Old_C


def ClusteringWithC_Index(Data,NumberOfClusters,NumberofIterationsForCindex,DistanceBetweenAllPairNodesSorted,DistanceMethod='euclidean'):
    NumberOfClusters=NumberOfClusters
    x=Data
    NumberofIterationsForCindex=NumberofIterationsForCindex
    NUmberOfNodesInTheClusters=0
    D=DistanceBetweenAllPairNodesSorted
    OptimalCenter=[]
    C=1
    Old_C=sys.maxint
    Scl=0
    N=0
    Smin=0
    Smax=0


    for NumberofIterations in xrange(NumberofIterationsForCindex):
        centroid,labels=Classifier=kmeans2(Data, NumberOfClusters, iter=500, thresh=1e-05, minit='random', missing='warn')
        for i in xrange( NumberOfClusters ):
            NUmberOfNodesInTheClusters=len(x[numpy.where(labels==i)])
            Scl=Scl+numpy.sum( scipy.spatial.distance.pdist(x[numpy.where(labels==i)], DistanceMethod))
            N=N+Combination(NUmberOfNodesInTheClusters, 2)
        Smin=numpy.sum( D[0:N:1])
        Smax=numpy.sum(D[len(D)-N::1])
        if(Smax-Smin==0):
            continue
        C=(Scl-Smin)/(Smax-Smin)
        Scl=0
        N=0
        Smin=0
        Smax=0
        if(C<Old_C):
            Old_C=C
            OptimalCenter=centroid[:]
    return OptimalCenter,Old_C




Data=GenerateData()

NumberofIterationsForCindex=50
DistanceMethod='euclidean'
MaxNumberOfClusters=20

ListOfCindexes=[]
ListOfCenters=[]
MinimumOfCindexes=[]


CentersForCurrentCluster=[]
CindexForCurrentCluster=0


DistanceBetweenAllPairNodes = scipy.spatial.distance.pdist(Data, DistanceMethod)
DistanceBetweenAllPairNodesSorted= numpy.sort(DistanceBetweenAllPairNodes)

for NumberOfClusters in numpy.arange(1,MaxNumberOfClusters,1):
    CentersForCurrentCluster,CindexForCurrentCluster =ClusteringWithC_Index(Data, NumberOfClusters,NumberofIterationsForCindex,DistanceBetweenAllPairNodesSorted,DistanceMethod)
    ListOfCenters.append(CentersForCurrentCluster[:])
    ListOfCindexes.append(CindexForCurrentCluster)

IndexOfOptimalNumberOfComponents=numpy.argmin(ListOfCindexes)
Centers=ListOfCenters[IndexOfOptimalNumberOfComponents]


pyplot.figure()
pyplot.scatter(Data[:,0], Data[:,1]) 
pyplot.scatter( Centers[:,0], Centers[:,1],color='red')
pyplot.show()

print Centers

