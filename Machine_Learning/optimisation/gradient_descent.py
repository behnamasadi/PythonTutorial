# Behnam Asadi 
# http://ros-developer.com
# To see the function that we are working on visit:
# http://ros-developer.com/2017/05/07/gradient-descent-method-for-finding-the-minimum/
# or simply put the following latex code in a latex doc:
# $$ z= -( 4 \times e^{- ( (x-4)^2 +(y-4)^2 ) }+ 2 \times e^{- ( (x-2)^2 +(y-2)^2 ) } )$$

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np



def objective_function(x,y):
    z=-( 4*np.exp(-(x-4)**2 - (y-4)**2)+2*np.exp(-(x-2)**2 - (y-2)**2) )
    return z


def f_prim(x,y):
    f_x=-( (-2)*(x-4)*4*np.exp(-(x-4)**2 - (y-4)**2)    +   (-2)*(x-2)*2*np.exp(-(x-2)**2 - (y-2)**2) )
    f_y=-( (-2)*(y-4)*4*np.exp(-(x-4)**2 - (y-4)**2)    +   (-2)*(y-2)*2*np.exp(-(x-2)**2 - (y-2)**2) )
    return [f_x,f_y]

 
x = np.linspace(-2,10,200)
y = np.linspace(-2,10,200)

X, Y = np.meshgrid(x,y)

Z=objective_function(X,Y)


#Make a 3D plot
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, Z,linewidth=0,cmap='coolwarm')

ax.set_xlabel('X axis')
ax.set_ylabel('Y axis')
ax.set_zlabel('Z axis')


X_old=-2
Y_old=0


# The starts point for the algorithm:
X_new=4
Y_new=2.2

# step size
epsilon=0.1

# stop criteria
precision = 0.00001



x_path_to_max=[]
y_path_to_max=[]
z_path_to_max=[]



while np.sqrt( (X_new-X_old)**2 + (Y_new-Y_old)**2 ) > precision:
    X_old=X_new
    Y_old=Y_new
    
    #[X_new,Y_new]=f_prim(X_new,Y_new)
    #print f_prim(X_new,Y_new)
    x_path_to_max.append(X_new )
    y_path_to_max.append(Y_new )
    z=objective_function(X_new,Y_new)
    z_path_to_max.append(z)
    
    ret_val=f_prim(X_old,Y_old)
    X_new=X_old-epsilon*ret_val[0]
    Y_new=Y_old-epsilon*ret_val[1]
#    print X_new
#    print Y_new
    
    

line1=plt.plot(x_path_to_max,y_path_to_max,z_path_to_max)
plt.setp(line1,color='g',linewidth=0.5)


#print X_new
#print Y_new
plt.show()


