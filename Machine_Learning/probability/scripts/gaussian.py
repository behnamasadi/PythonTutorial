import numpy as np
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import norm

#-------------------------------------------------------------------------------------------------------------------------------

def bivariate_normal(X, Y, sigmax=1.0, sigmay=1.0,
                     mux=0.0, muy=0.0, sigmaxy=0.0):
    """
    Bivariate Gaussian distribution for equal shape *X*, *Y*.
    See `bivariate normal
    <http://mathworld.wolfram.com/BivariateNormalDistribution.html>`_
    at mathworld.
    """
    Xmu = X-mux
    Ymu = Y-muy

    rho = sigmaxy/(sigmax*sigmay)
    z = Xmu**2/sigmax**2 + Ymu**2/sigmay**2 - 2*rho*Xmu*Ymu/(sigmax*sigmay)
    denom = 2*np.pi*sigmax*sigmay*np.sqrt(1-rho**2)
    return np.exp(-z/(2*(1-rho**2))) / denom


#mu=0
#sigma=1

mu=5.855
sigma=(3.5e-2)**(0.5)


pi=np.pi
e=np.e

x=np.arange(2,7,0.1)
denominator=1/((2*pi*sigma**2)**0.5 )
y=denominator  * e** (-(x-mu)**2/(2*sigma**2)) 

plt.plot(x,y)
plt.show()

x=6
print (denominator  * e** (-(x-mu)**2/(2*sigma**2)))


#-------------------------------------------------------------------------------------------------------------------------------

#initialize a normal distribution with frozen in mean=-1, std. dev.= 1
rv = norm(loc = -1., scale = 1.0)
rv1 = norm(loc = 0., scale = 2.0)
rv2 = norm(loc = 2., scale = 3.0)

x = np.arange(-10, 10, .1)

#plot the pdfs of these normal distributions 
plt.plot(x, rv.pdf(x), x, rv1.pdf(x), x, rv2.pdf(x))
plt.show()



#-----------------------------------generation Gaussian, normal, histogram ---------------------------------------

#Draw random samples from a normal (Gaussian) distribution.
#x=np.arange(-2,2,)

mu=0
sigma=1

s1=np.random.normal(mu,sigma,100)


count, bins, ignored = plt.hist(s1, 30, normed=True)
#plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) * np.exp( - (bins - mu)**2 / (2 * sigma**2) ),linewidth=2, color='r')
plt.show()






#----------------------------------random gen multivariate normal, multi dimentional Gaussian-------------------------------------
mean=[0,0]
cov=[[1,0],[0,1]]
x1,y1=np.random.multivariate_normal(mean,cov,500).T


mean=[4,4]
cov=[[1,0],[0,1]]

x2,y2=np.random.multivariate_normal(mean,cov,500).T





#x=np.stack((x1, x2),axis=1)
#y=np.stack((y1, y2),axis=1)


x=np.concatenate((x1, x2), axis=0)
y=np.concatenate((y1, y2), axis=0)

print (x.shape)
print (y.shape)

plt.scatter(x,y)
plt.axis('equal')
plt.show()


#----------------------------------plotting pdf, surface plot gaussian, multi variant-------------------------------------
mu_x=0
mu_y=0

sigma_x=1
sigma_y=1
sigma_xy=[]

x=np.arange(-5,5,0.05)
y=np.arange(-5,5,0.05)

X,Y=np.meshgrid(x,y)
Z=bivariate_normal(X, Y, sigma_x, sigma_y, mu_x, mu_y)
plt.contour(X,Y,Z)
plt.show()


fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, Z,linewidth=0,cmap='hot')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
plt.show()



# import matplotlib.pyplot as plt
# import numpy as np
# from scipy.stats import multivariate_normal
#
# def gaussian(x, mu, sigma):
#         #return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))
#         #return (1/(sigma*np.power(2*np.pi)))*np.exp(-0.5* np.power((x-mu/sigma),2) )
#         return   np.exp(-0.5 * np.power((x - mu / sigma), 2))/(sigma * np.power(2 * np.pi,0.5))
#
#
# x1=-10
# x2=10
# number_of_samples=200
# mu=0
# var=500
# sigma=np.power(var,0.5)
# print(sigma)
# x=np.linspace(x1,x2,number_of_samples)
# #y=gaussian(x, mu, sigma)
# y = multivariate_normal.pdf(x, mean=0, cov=sigma)
#
#
# plt.xlabel("x")
# plt.ylabel("y=gaussian(x)")
# line_1,=plt.plot(x,y,label='gaussian(x)')
# plt.legend()
# plt.legend(handles=[line_1])
# plt.show()
#
# number_of_samples=500
# x=np.random.randn(number_of_samples)
# mu=np.sum(x)/number_of_samples
# var=np.sum(np.power(x-mu,2))/number_of_samples
# print(mu)
# print(var)
# bins=np.linspace(-5,5,200)
# plt.hist(x,bins=bins,orientation='vertical')
# plt.show()


