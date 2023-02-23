import matplotlib.pyplot as plt
import numpy as np
import math


####################################### figure ######################################

# Figure: It is the top most layer of the plot. Figure constitutes of subplots, sub axis, titles, subtitles, legends,..

# matplotlib.pyplot.figure(num=None, figsize(float, float))
# Create a new figure, or activate an existing figure.
# num: int or str, optional A unique identifier for the figure.

# If a figure with that identifier already exists, this figure is made active and returned. An integer refers to the
# Figure.number attribute, a string refers to the figure label.

plt.figure(1)
print ("current figure = " + str(plt.gcf().number))

plt.figure(2)
print ("current figure = " + str(plt.gcf().number))




# now switch back to figure 1 and make some changes
x=np.linspace(start=0, stop=10, num=50)
plt.figure(1)
plt.plot(x,x**2)

# now switch back to figure 2 and make some changes
plt.figure(1)
plt.plot(x,x**3)
# Get the current Axes instance on the current figure
ax = plt.gca()
ax.set_title('y=x**3')
plt.show()

print ("Figure numbers are = " + str(plt.get_fignums()))
####################################### ax  ######################################
# Axes: It’s a part of the Figure, nothing but a subplot. Axes define a subplot, we can write our
# own x-axis limits, y-axis limits, their labels, the type of graph. It controls every detail inside the subplot
# is the object that you can plot in, ax is actually a numpy array


####################################### subplot() ######################################
# pyplot.subplot(nrows, ncols, index)
# The subplot() command specifies numrows, numcols, fignum where fignum ranges from 1 to numrows*numcols.
# subplot(211) is identical to subplot(2, 1, 1).
# index starts at 1 in the upper left corner and increases to the right. index can also be a
# two-tuple specifying the (first, last) indices (1-based, and including last)
x=np.linspace(start=2, stop=20, num=50)
plt.figure()
plt.subplot(121)
plt.plot(x,np.log(x))

plt.subplot(122)
plt.plot(x,np.exp(x))
plt.show()

####################################### subplots() ######################################
# pyplot.subplots(nrows=1, ncols=1)
# subplots() is a function that returns a tuple containing a figure and axes.
#fig, ((ax1, ax2), (ax3, ax4)) = plt.subplot(2, 2)

# the code above can be written as
x=np.linspace(start=2, stop=20, num=50)
plt.figure()
fix,(ax1,ax2)=plt.subplots(nrows=1, ncols=2)
ax1.plot(x,np.log(x))
ax2.plot(x,np.exp(x))
plt.show()


####################################### add_subplot() ######################################
# matplotlib.pyplot.figure.add_subplot(nrows, ncols, index)
# fig.add_subplot(ax)

# fig = plt.figure()
# ax = fig.add_subplot(111)
# is equal to
# fig, ax = plt.subplots()











####################################### Example of accessing subplots(), ax ######################################

x=np.arange(1,10)
fig, ax=plt.subplots(nrows=2,ncols=1)
y=np.log(x)
ax[0].plot(x,y)
y=x*x*x
ax[1].plot(x,y)
plt.show()



fig, ax = plt.subplots(2, 2)
ax[0, 0].plot(range(10), 'r') #row=0, col=0
ax[1, 0].plot(range(10), 'b') #row=1, col=0
ax[0, 1].plot(range(10), 'g') #row=0, col=1
ax[1, 1].plot(range(10), 'k') #row=1, col=1
plt.show()

####################################### Example of add_subplot() to figure objcect ######################################

x=np.arange(1,10)
fig=plt.figure()

y=np.log(x)
ax_2_1=fig.add_subplot(2,1,1)#2 rows, 1 column, ax number
ax_2_1.plot(x,y)

ax_2_2=fig.add_subplot(2,1,2)#2 rows, 1 column, ax number
y=x*x
ax_2_2.plot(x,y)
plt.show()


###################################### axis, xlim, ylim limit ######################################

x=np.arange(-4*np.pi,4*np.pi,0.1)
y=np.sin(x)
y_shifted=np.sin(x-np.pi/4)

xmin=0
xmax=4*np.pi
ymin=0
ymax=2

#plt.xlim([ymin, ymax])
plt.axis([xmin,xmax,ymin,ymax])
plt.plot(x,y,color='r')
plt.plot(x,y_shifted,color='b')
plt.show()

####################################### Example of subplot() ######################################

def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 6.0, 0.02)

plt.figure()

ax1 = plt.subplot(1,2,1)#1 row, 2 columns, ax number 1
ax1.plot(t1, f(t1) )

ax2 = plt.subplot(1,2,2)#1 row, 2 columns, ax number 2
ax2.plot(t2, np.cos(2*np.pi*t2), 'r--')
plt.show()


####################### Example of suptitle, legend, set_title, set_xlabel, set_ylabel, gcf, ticks, grid #################################



x=np.arange(0.0, 5.0, 0.1)

fig,ax=plt.subplots(nrows=2,ncols=2)
fig.suptitle('fig title', fontsize=10)
ax[0,1].plot(x, np.sin(x), label="this is sin")
ax[0,1].legend(loc="upper left")
ax[0,1].set_aspect('equal')
ax[0,1].set_title('Line Collection with mapped colors')
ax[0,1].set_xlabel("this is x")
ax[0,1].set_ylabel("this is y")
ax[0,1].xaxis.set_ticks_position('top')
ax[0,1].yaxis.set_ticks_position('right')
ax[0,1].grid(True)
#ax[0,1].axis('off')


retrieved_ax=plt.gcf().get_axes()
retrieved_ax[1].legend(('updated!'))

plt.show()


####################################### legend, label #######################################
x=np.arange(10)
y1=np.power(x,2)
y2=np.power(x,3)
plt.plot(x,y1,label='x^2')
plt.plot(x,y2,label='x^3')
# Calling legend() with no arguments automatically fetches the legend handles and their associated labels.
plt.legend()
plt.show()

# For full control of what is being added to the legend, it is common to pass the appropriate handles directly to legend():
line_1,=plt.plot(x,y1,label='x^2')
line_2,=plt.plot(x,y2,label='x^3')
plt.legend(handles=[line_1, line_2])


plt.show()

####################################### scatter plot #######################################
x=np.random.random(100)
y=np.random.random(100)
plt.scatter(x,y)
plt.show()


####################################### Histogram #######################################
fig, ax=plt.subplots(1,1)

#x = np.random.randn(1000)
#bins = np.arange(-10, 10 , 1)

x = [1,1,12,3,8,5,3,4,5,6,7]
bins = np.arange(-10, 10 , 1)

ax.hist(x, bins=bins, orientation='horizontal')
plt.show()

####################################### stack/ bar / grouped bar #######################################

x=[1,2,4]
height=[5,1,2]
labels = ['G1', 'G2', 'G3']

fig,ax=plt.subplots(1,1)
ax.bar(x, height,width=0.25)

ax.set_xticks(x)
ax.set_xticklabels(labels)
plt.show()



####################################### live graph #######################################

import matplotlib.animation as animation
from matplotlib import style
import psutil

x=[]
y=[]
def animate(i):
	x.append(i)
	y.append(psutil.cpu_percent())
	ax.plot(x,y)


style.use('fivethirtyeight')

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ani = animation.FuncAnimation(fig, animate, interval=1000)
plt.show()

####################################### jupyter notebook #######################################
#%matplotlib notebook


####################################### plot surface/ 3D plots #######################################

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

##################### Example 1 #####################

X = np.arange(-10, 10, 0.25)
Y = np.arange(-10, 10, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt((X-1)**2 + (Y-3)**2)
Z = np.sin(R)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm, linewidth=0, antialiased=False)
ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()


###################### Example 2 ##################### 

mu_x = 0
sigma_x = np.sqrt(3)

mu_y = 0
sigma_y = np.sqrt(15)

#Create grid and multivariate normal
x = np.linspace(-15,15,500)
y = np.linspace(-15,15,500)

x = np.linspace(-1.5,1.5,500)
y = np.linspace(-1.5,1.5,500)

X, Y = np.meshgrid(x,y)

Z=np.sin(0.5*X**2-0.25*Y**2)*np.cos(2*x+1-np.exp(y))


#Make a 3D plot
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(X, Y, Z,linewidth=0,cmap='hot')
ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')
plt.show()


####################################### imshow() #######################################
import numpy as np
import matplotlib.pyplot as plt


x=np.random.randn(7,7)
farmers = ["Farmer Joe", "Upland Bros.", "Smith Gardening","Agrifun", "Organiculture", "BioGoods Ltd.", "Cornylee Corp."]
figure, ax=plt.subplots(1,1)
ax.imshow(x)
ax.set_xticklabels(farmers)
ax.set_xticks(np.arange(len(farmers)))
plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

plt.show()



####################################### contour #######################################

x = np.linspace(-20,20,100)
w = np.linspace(-50,50,50)
X, W = np.meshgrid(x,w)
Z=20*X**2+W**2
levels=np.arange(np.min(Z), np.max(Z),10)
plt.contourf(X,W,Z,levels=levels)
plt.show()
