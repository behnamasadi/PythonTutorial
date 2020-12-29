import numpy as numpy


#Number of rows
N=7 

#Number of cols
M=6 

F=numpy.zeros((N,M))
G=numpy.zeros((N,M))
H=numpy.zeros((N,M))

start_point_n=3
start_point_m=2


goal_point_n=6
goal_point_m=5



blocked_points = numpy.array([[5, 2], [5,4], [6,4] ,[3, 4]])

#print blocked_points.shape
#print blocked_points[1]
#print blocked_points
#print F[blocked_points]
for i in blocked_points:
#    print i[0]
#    print i[1]
    print F[i[0],i[1]]

#m =  numpy.array([[0, 64], [0, 79], [0, 165], [0, 50]])
#print m.shape
#print(m[3, 1])
#print(m[3])

open_list=[]
close_list=[]




import pylab as plt

# Load the image
img = plt.imread("/home/behnam/Pictures/Strasburg/DSC_0064.JPG")

# Grid lines at these intervals (in pixels)
# dx and dy can be different
dx, dy = 100,100

# Custom (rgb) grid color
grid_color = [0,0,0]

# Modify the image to include the grid
img[:,::dy,:] = grid_color
img[::dx,:,:] = grid_color

# Show the result
plt.imshow(img)
plt.show()



