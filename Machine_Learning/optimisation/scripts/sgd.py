import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm


# The cost function that we want to minimize in nn is diffeerence between the output of nn and expected output.
# this should be near zero. We have a set of training data and their corresponding output from a function that we dont have
# just like regression that we might use linear regression or polynominal. since computational graphs
# can calculate any function, we use them to estimate the function that we dont have but we have some samples of that.
# theparameters of the nn are W, b but the parameters of the cost function are X,W,b and outpput is (y_nn-y_lable)

# imagine your network has only one weight and input is only 1 dimension x we, cost function might look something like this:


x = np.linspace(-1,1,50)
w = np.linspace(-1,1,50)

X, W = np.meshgrid(x,w)
Z=W*X**3+X*W**2

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, W, Z,linewidth=0,cmap='viridis')
ax.set_xlabel('X')
ax.set_ylabel('W')
ax.set_zlabel('Error function')
plt.show()


# This surface will show you if you choose a specific item from training set and you choose different w what would be
# the lost:

x = np.linspace(-0.5,-0.51,50)
w = np.linspace(-1,1,50)

X, W = np.meshgrid(x,w)
Z=W*X**3+X*W**2



fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, W, Z,linewidth=0,cmap='viridis')
ax.set_xlabel('X')
ax.set_ylabel('W')
ax.set_zlabel('Error function')
plt.show()



# now if you select a random w for your model and you can see for this w what would be the loss value:

x = np.linspace(-1,1,50)
w = np.linspace(-0.5,-0.51,50)

X, W = np.meshgrid(x,w)
Z=W*X**3+X*W**2

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, W, Z,linewidth=0,cmap='viridis')
ax.set_xlabel('X')
ax.set_ylabel('W')
ax.set_zlabel('Error function')
plt.show()

# in practice we have a few samples from x and we are looking for right w to minimize the lost. If we have more than one
# dimension for w  (i.e. 2) we have iterate over all of them (bruteforce) to find a right one which in practice
# impossible. Also we dont have all values for x and we have only few samples from that (imagine x in higher dimension
# which could be photos of a doge, ony know for some cetain values in x the output could be a dog)
# so in practice we have something like this

fig = plt.figure()
ax = fig.gca(projection='3d')

ax.set_xlabel('X')
ax.set_ylabel('W')
ax.set_zlabel('Error function')


X=np.linspace(-5,5,10)
w=-1.0
#w=-0.0
W=np.linspace(w,w,10)

x_s=[]
w_s=[]
z_s=[]

for x in X:
        for w in W:
                z=w*x**3+x*w**2
                z_s.append(z)
                x_s.append(x)
                w_s.append(w)
                # print(x)

ax.scatter(x_s, w_s, z_s)
plt.show()


# as it can be seen, for this fixed w, for some of input the output error is small and for others it is big, we need
# to find a new w such that for all x the loss function is small.

# First we have to estimate the error function (i.e by selecting different number of hidden layer and size of them for instance)
# or in this simple case by some polynominal, so we will have a function f(w,x)=error


# we compute the derivative f w.r.t w (df/dw), we set some random value for w, and plug all x in the training set into
# derivative function to calculate
#
# then we make average over all values and update the w"
#
# w_n+1=w_n +learning_rate* (average of df/dw for all x in training set)