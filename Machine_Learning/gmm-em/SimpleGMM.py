import numpy as numpy
from sklearn import mixture
import matplotlib.pyplot as  pyplot



#ProbabilityThreshold=0.8
g = mixture.GMM(n_components=3)
#print help(mixture.GMM)
numpy.random.seed(0)
#obs = numpy.concatenate( (numpy.random.randn(200, 2)-2  ,  10 + numpy.random.randn(400, 2) ) )
obs = numpy.concatenate( (numpy.random.randn(100, 2) , 10 + numpy.random.randn(300, 2) , -5+numpy.random.randn(200, 2)))

g.fit(obs)

#print g.means[0]
#print numpy.exp( g.score([[-6,-6]]) )/numpy.exp( g.score([ g.means[0]]))
#numpy.argmax(a, axis)
#print g.predict([g.means[0]])

#print g.predict(obs)
#print "____________________________________________________________"
#print g.score(g.means[g.predict(obs)])
#g.score( g.means[g.predict(obs)])

#print numpy.exp( g.score(g.means))/numpy.exp( )
#PointsProbabilities=numpy.exp( g.score(obs) )/ numpy.exp(  g.score( g.means[g.predict(obs)]))
#PointsProbabilities=numpy.exp( g.score(obs) )/numpy.exp( g.score( g.means[g.predict(obs)]))
#print PointsProbabilities
#print numpy.where(PointsProbabilities==1)
#print len(numpy.where(PointsProbabilities>0.9)[0])
#print len(numpy.where(PointsProbabilities>0.6)[0])

#x=g.means[0].reshape(2,1)
#print x
#print g.predict(x)
#print numpy.array(g.means[0] )
#print g.predict_proba((g.means)) 
noise=[[-25,-5],[2,3],[12,1],[14,9],[3,18]]
#obs = numpy.concatenate( (numpy.random.randn(100, 2) , 10 + numpy.random.randn(300, 2) , -5+numpy.random.randn(200, 2) ))
#obs = np.concatenate( (np.random.randn(100, 1) , 10 + np.random.randn(300, 1) , -5+np.random.randn(200, 1) ) )
#means=numpy.array([[0,0],[10,10],[-5,-5]])
#means=means.reshape(3,2)
#g._set_means(means)
#g.fit(obs,init_params='wc')



#print g.means
#print noise
#print "g.predict_proba(noise)"
#print g.predict_proba(noise)
#print "g.decode(noise)"
#print g.decode(noise)
#print "g.score(noise)"
#print g.score(noise)
#print "numpy.exp(g.score(noise))"
#print numpy.exp(g.score(noise))
#
#Threshold=-numpy.exp(ProbabilityThreshold)
#print Threshold 
#print g.score([[-4.87676262, -5.00748854]])
#print g.score([[-100, -100]])

#print numpy.log(-g.score([[-4.87676262, -5.00748854]]))**-1
#print g.predict_proba([[-1000,-1000]])
#print g.score([[-1000,-1000]])
#print g.eval([[-1000,-1000]])
#
#noise=numpy.array(noise)
#
#
#
pyplot.scatter(obs[:,0],obs[:,1])
pyplot.scatter(g.means[:,0],g.means[:,1],color='red')
##
#for i in xrange(len(obs)):
#    if(g.score([obs[i]])<Threshold):
#        pyplot.scatter(obs[i][0],obs[i][1],color='black')
pyplot.show()
print "means"    
print g.means
print "weights"
print g.weights
print "covars"
print g.covars

