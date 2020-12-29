import numpy


#when you try to create numpy array, you should provide a list, hence:'
#a = np.array(1,2,3,4)    # WRONG'
#a = np.array([1,2,3,4])  # RIGHT '
############################### Random sampling ###############################
#https://docs.scipy.org/doc/numpy-1.14.0/reference/routines.random.html
print("List of supported distributions:", 'beta', 'binomial', 'bytes', 'chisquare', 'choice', 'dirichlet', 'exponential'
      , 'f', 'gamma', 'geometric', 'get_state', 'gumbel', 'hypergeometric', 'laplace', 'logistic', 'lognormal',
      'logseries', 'multinomial', 'multivariate_normal', 'negative_binomial', 'noncentral_chisquare', 'noncentral_f',
      'normal', 'pareto', 'permutation', 'poisson', 'power', 'rand', 'randint', 'randn', 'random', 'randint',
      'random_sample', 'ranf', 'rayleigh', 'sample', 'seed', 'set_state', 'shuffle', 'standard_cauchy',
      'standard_exponential', 'standard_gamma', 'standard_normal', 'standard_t', 'triangular', 'uniform', 'vonmises',
      'wald', 'weibull', 'zipf',)


############################### uniform sampling ###############################

dim1=2
dim2=3
dimn=1
print("random values in shape of dim1={}, dim2={}, dimn={} with uniform distribution over [0, 1)".format(dim1, dim2, dimn))
print(numpy.random.rand(dim1,dim2,dimn))


low=1
high=10
size=4
print("{} random integers of type, between low={} and high={}, inclusive with uniform distribution".format(size,low, high))
print(numpy.random.randint(low,high,size))

############################### beta sampling ###############################
a=1
b=5
size=3
print("{} random samples from a Beta distributionn with a={} and b={}".format(size,a, b))
print(numpy.random.beta(a=1,b=5,size=10))

############################### multivariate normal ###############################
mean = [0, 0]
cov = [[1, 0], [0, 100]]
size=4
print("Draw random {} samples from a multivariate normal distribution with mean={} and cov={}".format(size,mean, cov))
print(numpy.random.multivariate_normal(mean,cov,size))

############################## Matrix Multiplication ##############################
x=numpy.array([[2,1,1],[3,1,4]] )
y=numpy.random.randint(low=-1,high=4,size=[3,1])


#1)@: operator calls the array's __matmul__ method
#2)dot: For 2-D arrays it is equivalent to matrix multiplication, and for 1-D arrays to inner product of vectors
# (without complex conjugation). For N dimensions it is a sum product over the last axis of a and the
# second-to-last of b
print("For 1/2 D  Matrix @, matmul and dot are equal:")
print("x@y:\n",x@y)
print("matmul(x,y):\n",numpy.matmul(x,y) )
print("dot(x,y): \n",numpy.dot(x,y) )

a = numpy.random.rand(8,13,13)
b = numpy.random.rand(8,13,13)
numpy.matmul(a, b).shape
print(numpy.dot(a,b).shape )
print(numpy.matmul(a,b).shape )

############################## shape, reshape, ndim, axis ##############################


#          axis 1  ------------------------►
#axis 0  |             |  col 0 | col 1 | col 2  |
#  |     +-------------+-------+--------+--------+
#  |     | row 0       |       |        |        |
#  |     +-------------+-------+--------+--------+
#  |     | row 1       |       |        |        |
#  ▼     +-------------+-------+--------+--------+
a=numpy.random.randint(low=1, high=4,size=[2,3])
print(a)
print("a ndim is: ",a.ndim)
print("a shape is: ",a.shape)
print("sum of matrix, column wise: ",numpy.sum(a,axis=0))
print("sum of matrix, row wise:  ",numpy.sum(a,axis=1))


################################# Reshape ##############################
#Here we want 2 rows and we set second dim as -1 which means python should calculate that for us
size=6
rows=2
print("matrix with {} element reshaped into {} rows: \n".format(size,rows),
      numpy.random.randint(low=1, high=10, size=size).reshape(rows,-1))


################################# Data type Object (dtype) in NumPy Python #################################

dt=numpy.dtype(numpy.int16)
print(dt)


# i4 represents integer of size 4 byte 
# > represents big-endian byte ordering and < represents little-endian encoding. 
# dt is a dtype object 
dt = numpy.dtype('>i4') 

print("Byte order is:",dt.byteorder) 
print("Size is:",dt.itemsize) 
print("Data type is:",dt.name)


#The type specifier (i4 in above case) can take different forms:
#b1, i1, i2, i4, i8, u1, u2, u4, u8, f2, f4, f8, c8, c16, a (representing bytes, ints, unsigned ints, floats, 
#complex and fixed length strings of specified byte lengths)
#int8,…,uint8,…,float16, float32, float64, complex64, complex128 (this time with bit sizes)

#one=numpy.ones(2,3,dtype=numpy.uint8)
#, lambda, numpy as array dtype ,dtype=numpy.float32



print("############################### concatenate, vstack, hstack ###############################")
mat1=numpy.array(numpy.random.randint(low=1, high=10,size=[3,4]))
mat2=numpy.array(numpy.random.randint(low=1, high=10,size=[3,4]))
print("mat1 is:\n",mat1)
print("mat2 is:\n",mat2)
print("hstack :\n ", numpy.hstack((mat1,mat2)))
print("concatenate axis=0:\n", numpy.concatenate((mat1,mat2),axis=0))

print("vstack :\n", numpy.vstack((mat1,mat2)))
print("concatenate axis=1:\n", numpy.concatenate((mat1,mat2),axis=1))


print("dstack, shape:\n", numpy.dstack((mat1,mat2)), "\n", numpy.dstack((mat1,mat2)).shape  )
print("numpy.dstack((mat1,mat2))[0,0]:\n",numpy.dstack((mat1,mat2))[0,0])


print("mat1 flatten:",mat1.flatten())


print("############################### operation on ndarray ###############################")
mat1=numpy.array(numpy.random.randint(low=1, high=10,size=5))
mat2=numpy.array(numpy.random.randint(low=1, high=10,size=5))
print(mat1)
print(mat2)
print(mat1/3)
print(mat1+mat2)
print(mat1-mat2)



print("############################### storing/ saving / load / reading numpy array ###############################")
#NPY file: It is a  binary file format for persisting NumPy array on disk. Data cabn be reconstructed  on another machine with a different architecture. 


import time
import os



np_array_to_dump_on_disk=numpy.random.rand(1000000,2)
t1=time.time()
with open("tmp.csv","w") as file:
	file.write("filed1, field2 \n")
	for row in np_array_to_dump_on_disk:
		file.write(str(row[0]) + ","+ str(row[1]) + "\n")

np_array_to_dump_on_disk_reconstructed = numpy.genfromtxt('tmp.csv', delimiter=',',skip_header=1)
t2=time.time()
os.remove('tmp.csv')

print("Time to write/read with csv:",t2-t1)

t1=time.time()
numpy.save('tmp.npy', np_array_to_dump_on_disk)
np_array_to_dump_on_disk_reconstructed = numpy.load('tmp.npy')
t2=time.time()
print("Time to write/read with NPY:",t2-t1)
os.remove('tmp.npy')

