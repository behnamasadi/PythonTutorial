import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline

def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
mu=2
sig=4

x1=-10
x2=15
number_of_samples=200
x=np.linspace(x1,x2,number_of_samples)
y=gaussian(x, mu, sig)
plt.xlabel("x")
plt.ylabel("y=gaussian(x)")
line_1,=plt.plot(x,y,label='gaussian(x)')
plt.legend()
plt.legend(handles=[line_1])

a=5
b=10
x=np.linspace(a,b,number_of_samples)
y_min=np.zeros_like(x)
y_max=gaussian(x, mu, sig)
plt.vlines(x,y_min,y_max,colors='red')
observation=-2
plt.vlines(observation,0,gaussian(observation, mu, sig),colors='green')
plt.hlines(gaussian(observation, mu, sig),x1,observation,colors='green')
plt.show()

