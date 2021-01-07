import numpy as np


#when you try to create np array, you should provide a list, hence:'
#a = np.array(1,2,3,4)    # WRONG'
#a = np.array([1,2,3,4])  # RIGHT '
print('############################### Random sampling ###############################')
#https://docs.scipy.org/doc/np-1.14.0/reference/routines.random.html
print("List of supported distributions:", 'beta', 'binomial', 'bytes', 'chisquare', 'choice', 'dirichlet', 'exponential'
      , 'f', 'gamma', 'geometric', 'get_state', 'gumbel', 'hypergeometric', 'laplace', 'logistic', 'lognormal',
      'logseries', 'multinomial', 'multivariate_normal', 'negative_binomial', 'noncentral_chisquare', 'noncentral_f',
      'normal', 'pareto', 'permutation', 'poisson', 'power', 'rand', 'randint', 'randn', 'random', 'randint',
      'random_sample', 'ranf', 'rayleigh', 'sample', 'seed', 'set_state', 'shuffle', 'standard_cauchy',
      'standard_exponential', 'standard_gamma', 'standard_normal', 'standard_t', 'triangular', 'uniform', 'vonmises',
      'wald', 'weibull', 'zipf',)


print('############################### uniform sampling ###############################')

dim1=2
dim2=3
dimn=1
print("random values in shape of dim1={}, dim2={}, dimn={} with uniform distribution over [0, 1)".format(dim1, dim2, dimn))
print(np.random.rand(dim1,dim2,dimn))


low=1
high=10
size=4
print("{} random integers of type, between low={} and high={}, inclusive with uniform distribution".format(size,low, high))
print(np.random.randint(low,high,size))

print('############################### beta sampling ###############################')
a=1
b=5
size=3
print("{} random samples from a Beta distributionn with a={} and b={}".format(size,a, b))
print(np.random.beta(a=1,b=5,size=10))

print('############################### multivariate normal ###############################')
mean = [0, 0]
cov = [[1, 0], [0, 100]]
size=4
print("Draw random {} samples from a multivariate normal distribution with mean={} and cov={}".format(size,mean, cov))
print(np.random.multivariate_normal(mean,cov,size))

print('############################## Matrix Multiplication ##############################')
x=np.array([[2,1,1],[3,1,4]] )
y=np.random.randint(low=-1,high=4,size=[3,1])


#1)@: operator calls the array's __matmul__ method
#2)dot: For 2-D arrays it is equivalent to matrix multiplication, and for 1-D arrays to inner product of vectors
# (without complex conjugation). For N dimensions it is a sum product over the last axis of a and the
# second-to-last of b
print("For 1/2 D  Matrix @, matmul and dot are equal:")
print("x@y:\n",x@y)
print("matmul(x,y):\n",np.matmul(x,y) )
print("dot(x,y): \n",np.dot(x,y) )

a = np.random.rand(8,13,13)
b = np.random.rand(8,13,13)
np.matmul(a, b).shape
print(np.dot(a,b).shape )
print(np.matmul(a,b).shape )

print('############################## shape, reshape, ndim, axis ##############################')


#          axis 1  ------------------------►
#axis 0  |             |  col 0 | col 1 | col 2  |
#  |     +-------------+-------+--------+--------+
#  |     | row 0       |       |        |        |
#  |     +-------------+-------+--------+--------+
#  |     | row 1       |       |        |        |
#  ▼     +-------------+-------+--------+--------+
a=np.random.randint(low=1, high=4,size=[2,3])
print(a)
print("a ndim is: ",a.ndim)
print("a shape is: ",a.shape)
print("sum of matrix, column wise: ",np.sum(a,axis=0))
print("sum of matrix, row wise:  ",np.sum(a,axis=1))

print('############################### missing second dimension ###############################')

array = np.arange(3)
array.shape
print(array.tolist())
print(array.reshape(3,1).tolist())
# (3,) doesn't mean there's a missing dimension. The comma is part of the standard Python
# notation for a single element tuple.



print('############################### Broadcasting ###############################')
# broadcasting describes how np treats arrays with different shapes during arithmetic operations.
x = np.arange(4)
x = x.reshape(4,-1)
print("x:\n",x)

print('############################### View, Copy ###############################')
# copy is a new array, and the view is just a view of the original array.
# view does not own the data and any changes made to the view will affect the original array, and any changes
# made to the original array will affect the view.
x=np.array ([1,2,3,4,5])
y=x.view()
z=x.copy()

x[0]=-1
print("x:", x)
print("y:", y)
print("z:", z)
print(x.base)
print(y.base)
print(z.base)

print('############################### Boolean ###############################')
x=np.arange(10)
y=x>7
print(y)
print(x[y])

print('############################### ravel ###############################')
# Return a contiguous flattened array. A copy is made only if needed.
x=np.array([[2,4,1],[7,2,3]])
# 'C' means c style, row major
# 'F' means fortran style, column major
print(x)
print(x.ravel(order='C'))
print(x.ravel(order='F'))

print('############################### Flattern ###############################')
# Return a copy of the array collapsed into one dimension
print(x.flatten(order='F'))

print('################################# Reshape ##############################')
print(x.reshape((6,1),order='C'))


print('############################### Squeez ###############################')
# This function removes one-dimensional entry from the shape of the given array.
x=np.random.randint(5 ,size=(1,3,4))
print(x)
print(x.squeeze())


print('################################# Data type Object (dtype) in np Python #################################')

dt=np.dtype(np.int16)
print(dt)


# i4 represents integer of size 4 byte 
# > represents big-endian byte ordering and < represents little-endian encoding. 
# dt is a dtype object 
dt = np.dtype('>i4') 

print("Byte order is:",dt.byteorder) 
print("Size is:",dt.itemsize) 
print("Data type is:",dt.name)


#The type specifier (i4 in above case) can take different forms:
#b1, i1, i2, i4, i8, u1, u2, u4, u8, f2, f4, f8, c8, c16, a (representing bytes, ints, unsigned ints, floats, 
#complex and fixed length strings of specified byte lengths)
#int8,…,uint8,…,float16, float32, float64, complex64, complex128 (this time with bit sizes)

#one=np.ones(2,3,dtype=np.uint8)
#, lambda, np as array dtype ,dtype=np.float32



print("############################### concatenate, vstack, hstack ###############################")
mat1=np.array(np.random.randint(low=1, high=10,size=[3,4]))
mat2=np.array(np.random.randint(low=1, high=10,size=[3,4]))
print("mat1 is:\n",mat1)
print("mat2 is:\n",mat2)
print("hstack :\n ", np.hstack((mat1,mat2)))
print("concatenate axis=0:\n", np.concatenate((mat1,mat2),axis=0))

print("vstack :\n", np.vstack((mat1,mat2)))
print("concatenate axis=1:\n", np.concatenate((mat1,mat2),axis=1))


print("dstack, shape:\n", np.dstack((mat1,mat2)), "\n", np.dstack((mat1,mat2)).shape  )
print("np.dstack((mat1,mat2))[0,0]:\n",np.dstack((mat1,mat2))[0,0])


print("mat1 flatten:",mat1.flatten())


print("############################### operation on ndarray ###############################")
mat1=np.array(np.random.randint(low=1, high=10,size=5))
mat2=np.array(np.random.randint(low=1, high=10,size=5))
print(mat1)
print(mat2)
print(mat1/3)
print(mat1+mat2)
print(mat1-mat2)



print("############################### storing/ saving / load / reading np array ###############################")
#NPY file: It is a  binary file format for persisting np array on disk. Data cabn be reconstructed  on another machine with a different architecture. 


import time
import os



np_array_to_dump_on_disk=np.random.rand(1000000,2)
t1=time.time()
with open("tmp.csv","w") as file:
	file.write("filed1, field2 \n")
	for row in np_array_to_dump_on_disk:
		file.write(str(row[0]) + ","+ str(row[1]) + "\n")

np_array_to_dump_on_disk_reconstructed = np.genfromtxt('tmp.csv', delimiter=',',skip_header=1)
t2=time.time()
os.remove('tmp.csv')

print("Time to write/read with csv:",t2-t1)

t1=time.time()
np.save('tmp.npy', np_array_to_dump_on_disk)
np_array_to_dump_on_disk_reconstructed = np.load('tmp.npy')
t2=time.time()
print("Time to write/read with NPY:",t2-t1)
os.remove('tmp.npy')

