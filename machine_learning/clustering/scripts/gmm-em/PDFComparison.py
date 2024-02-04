'''
Created on Sep 30, 2011

@author: behnam
'''
import numpy as numpy
from sklearn import mixture
import matplotlib.pyplot as pyplot


obs1 = numpy.concatenate((numpy.random.randn(100, 2) , 10 + numpy.random.randn(300, 2) , -5+numpy.random.randn(200, 2)))
g1 = mixture.GMM(n_components=3,cvtype='diag')

g1.fit(obs1)
#print "First Observation"
#print "means"    
#print g1.means
#print "weights"
#print g1.weights
#print "covars"
#print len(g1.covars)

obs2 = numpy.concatenate((numpy.random.randn(200, 2) , 5 + numpy.random.randn(100, 2) ))
g2 = mixture.GMM(n_components=2,cvtype='diag')
g2.fit(obs2)

#print "______________________________________________________________________________________________________________________________"
#print "Second Observation"
#print "means"    
#print g2.means
#print "weights"
#print g2.weights
#print "covars"
#print len(g2.covars)


#pyplot.scatter(obs1[:,0],obs1[:,1])
#pyplot.scatter(g1.means[:,0],g1.means[:,1],color='red')
#pyplot.show()
#
#pyplot.scatter(obs2[:,0],obs2[:,1])
#pyplot.scatter(g2.means[:,0],g2.means[:,1],color='red')
#
#pyplot.show()

#Base GMM
Means=g1.means
Weights=g1.weights
#print g1.covars

#Input GMM
Means_Prime=g2.means
Weights_Prime=g2.weights
#print len(g1.covars)



CovarianceMatrix=g1.covars 
CovarianceMatrix_Prime=g2.covars


def VIJ_Determinant(I,J,CovarianceMatrix,CovarianceMatrix_Prime):
    Covariance_I_Inverse=numpy.linalg.inv(CovarianceMatrix)
    Covariance_Prime_J_Inverse=numpy.linalg.inv(CovarianceMatrix_Prime)
    return numpy.linalg.det(Covariance_I_Inverse+Covariance_Prime_J_Inverse)

def e_Power_KIJ(I,J,CovarianceMatrix,CovarianceMatrix_Prime,Means,Means_Prime):
    Covariance_I_Inverse=numpy.linalg.inv(CovarianceMatrix)
    Covariance_Prime_J_Inverse=numpy.linalg.inv(CovarianceMatrix_Prime)
   
    Mu_I=Means[I]
    Mu_Prime_J=Means_Prime[J]
    
    Mu_I.shape=Mu_I.shape[0],1
    Mu_Prime_J.shape=Mu_Prime_J.shape[0],1
    KIJ_LeftSide=numpy.dot( numpy.dot(Mu_I.transpose(),Covariance_I_Inverse),Mu_I-Mu_Prime_J)
    KIJ_RightSide=numpy.dot( numpy.dot(Mu_Prime_J.transpose(),Covariance_Prime_J_Inverse),Mu_Prime_J-Mu_I)
    KIJ=KIJ_RightSide+KIJ_LeftSide  
    return numpy.exp(KIJ)

def SigmaIterator(Covariance_I,Covariance_J,Means_I,Means_J,Pi_I,Pi_J,I,J):
    Covariance_I_Determinant=numpy.linalg.det(Covariance_I)
    Covariance_J_Determinant=numpy.linalg.det(Covariance_J)
    Second_Root=numpy.power(VIJ_Determinant(I,J,Covariance_I,Covariance_J)/(e_Power_KIJ(I,J,Covariance_I,Covariance_J,Means_I,Means_J)* Covariance_I_Determinant*Covariance_J_Determinant),0.5)
    return Pi_I*Pi_J*Second_Root

#def Summation(Weights,Weights_Prime,Covariance,Covariance_Prime):
def Summation(Pis,Pis_Prime,Covariance,Covariance_Prime,Means_I,Means_J):
    Sum=0
    for I in range(len(Pis)):
#        print "I"
#        print I
        for J in  range(len(Pis_Prime)):
#            print "J"
#            print J
            Sum=Sum+SigmaIterator(Covariance[I],Covariance_Prime[J],Means_I,Means_J,Pis[I],Pis_Prime[J],I,J)            
    return Sum


Numerator=2*Summation(Weights,Weights_Prime,CovarianceMatrix,CovarianceMatrix_Prime,Means,Means_Prime)
#print "Numerator done"
Denominator=Summation(Weights,Weights,CovarianceMatrix,CovarianceMatrix,Means,Means)+Summation(Weights_Prime,Weights_Prime,CovarianceMatrix_Prime,CovarianceMatrix_Prime,Means_Prime,Means_Prime)
PDF_Distance=-numpy.log(Numerator/Denominator)
print PDF_Distance 





#print numpy.power(2,3)
#print 4**0.5