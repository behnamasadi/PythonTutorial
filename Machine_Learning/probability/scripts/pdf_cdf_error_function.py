import numpy as numpy
from scipy.stats import norm
import pylab as pylab
from scipy.special import *

#Functions related to probability distributions are located in scipy.stats.
# The general pattern is 
#scipy.stats.<distribution family>.<function>

start=-10
end=-start
step=0.01


mu=2
sigma=5


x=numpy.arange(start,end,step)

y=norm.pdf(x,mu,sigma)

pylab.scatter(x, y,color='green',alpha =0.5)

y=0.5*(1+erf((x-mu)/(sigma*pow(2,0.5))))
pylab.scatter(x,y,color='pink' ,alpha =  0.5)


y=norm.cdf(x,mu,sigma)
pylab.scatter(x,y, color='yellow',alpha =  0.5)

#in our case yellow and pink graph are exactly maped on each other

pylab.show()