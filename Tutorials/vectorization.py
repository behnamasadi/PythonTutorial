# https://numpy.org/doc/stable/reference/generated/numpy.vectorize.html
# https://datascience.blog.wzb.eu/2018/02/02/vectorization-and-parallelization-in-python-with-numpy-and-pandas/
# https://blog.paperspace.com/numpy-optimization-vectorization-and-broadcasting/
# https://realpython.com/numpy-array-programming/
import numpy as np
import time

# perf_counter():
# should measure the real amount of time for a process to take, as if you used a stop watch.
#
# process_time(): will give you the time spent by the computer for the current process, a computer with an OS
# usually won’t spend 100% of the time on any given process.

print("*************************** Summation  ***************************")

n=10000000

total = 0

tic=time.perf_counter()
for i in np.arange(n):
    total = i + total
toc=time.perf_counter()
print("summation via looping: ",toc-tic)


tic=time.perf_counter()
np.sum(np.arange(n))
toc=time.perf_counter()
print("vectorized sum",toc-tic)

print("*************************** dot multiplication   ***************************")

dot = 0.0;


a=np.random.rand(1000,1)
b=np.random.rand(1000,1)
c=np.zeros(1000)

tic=time.perf_counter()
for i in range(len(a)):
    dot += a[i] * b[i]
toc=time.perf_counter()
print("dot multiplication via looping: ",toc-tic)

tic=time.perf_counter()
dot =np.dot( a[i], b[i])
toc=time.perf_counter()
print("dot multiplication vectorized", toc-tic)

print("*************************** element wise multiplication   ***************************")


tic=time.perf_counter()
for i in range(len(a)):
    c[i] = a[i] * b[i]
toc=time.perf_counter()
print("element wise multiplication looping time: ",toc-tic)



tic=time.perf_counter()
c =a*b
toc=time.perf_counter()
print(toc-tic)
print("element wise multiplication vectorized: ",toc-tic)


print("*************************** Broadcasting  ***************************")



arr = np.arange(12).reshape(3,4)
col_vector = np.array([5,6,7])

#       arr         + col_vector

# [[ 0  1  2  3]     [ 5
#  [ 4  5  6  7]   +   6     =?
#  [ 8  9 10 11]]      7  ]


#1) First solution, using loops:
num_cols = arr.shape[1]

for col in range(num_cols):
	arr[:, col] += col_vector

#2) Second solution: column-stacking approach
# turning the col_vector into an array:

#[[ 0  1  2  3]       [[5 5 5 5]
#[4  5  6  7]     +   [6 6 6 6]
#[8  9 10 11]]        [7 7 7 7]]


arr = np.arange(12).reshape(3,4)
add_matrix = np.array([col_vector,] * num_cols).T

arr += add_matrix

#3) Third solution: Broadcasting
# if we want to vectorize a loop where we are dealing with arrays that don't have similar sizes
# the smaller array is “broadcast” across the larger array so that they have compatible shapes. Broadcasting
# provides a means of vectorizing array operations so that looping occurs in C instead of Python

# Rules of Broadcasting:
# The rank is the total number of dimensions a NumPy array has. For example,
# an array of shape (3, 4) has a rank of 2 and array of shape (3, 4, 3) has a rank of 3.

# 1) To deem which two arrays are suitable for operations, NumPy compares the shape of the two arrays
# dimension-by-dimension starting from the from right to left

# 2) Two dimensions are said to be compatible if both of them are equal, or either one of them is 1.

# 3) If both the dimensions are unequal and neither of them is 1, then NumPy will throw an error and halt.


# Example Arrays with Equal Ranks

# random array of shape (3,4,6,2)
array_a = np.random.rand(3,4,6,2)
array_b = np.random.rand(3,5,1,2)

# array_a + array_b will raise an exception, since from right to left,

# 2=2 is okay
# 6,1 is okay (rule number 2)
# 5,4 is NOT okay (rule number 2)


# Example Arrays with Unequal Ranks
array_a = np.random.rand(3,4,6,2)
array_b = np.random.rand(4,6,2)


array_a = np.random.rand(3,4,1,2)
array_b = np.random.rand(8,2)
print((array_a+array_b).shape)

# this will raise an exception:
array_a = np.random.rand(3,4,6,2)
array_b = np.random.rand(3,4,6)
# print((array_a+array_b).shape)


arr = np.arange(12).reshape(3,4)
col_vector = np.array([5,6,7])
arr += add_matrix

# print(arr.shape )
# print(col_vector.shape )



# ref: https://blog.paperspace.com/numpy-optimization-vectorization-and-broadcasting/




print("*************************** numpy.vectorize  ***************************")
# https://numpy.org/doc/stable/reference/generated/numpy.vectorize.html
def myfunc(a, b):
    "Return a-b if a>b, otherwise return a+b"
    if a > b:
        return a - b
    else:
        return a + b



vfunc = np.vectorize(myfunc)
print(vfunc([1, 2, 3, 4], 2))
