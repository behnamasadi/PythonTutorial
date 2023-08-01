# create np array


when you try to create np array, you should provide a list, hence:
```python
a = np.array(1,2,3,4)    # WRONG'
a = np.array([1,2,3,4])  # RIGHT '
```

### shape, reshape, ndim, axis

```
a=np.random.randint(low=1, high=4,size=[2,3])
print("a:\n",a)
print("a ndim is: ",a.ndim)
print("a shape is: ",a.shape)
```
which gives us:

```
a:
 [[2 2 1]
 [1 1 2]]
a ndim is:  2
a shape is:  (2, 3)
```


```python

         axis 1  --------------------------------►
axis 0 | row 0,col 0 | col 1 | col 2  |        |
 |     +-------------+-------+--------+--------+
 |     | row 0       |       |        |        |
 |     +-------------+-------+--------+--------+
 |     | row 1       |       |        |        |
 ▼     +-------------+-------+--------+--------+
```


```
print("sum of matrix, column wise: ",np.sum(a,axis=0))
print("sum of matrix, row wise:  ",np.sum(a,axis=1))
```
which gives us:

```
print("sum of matrix, column wise: ",np.sum(a,axis=0))
print("sum of matrix, row wise:  ",np.sum(a,axis=1))
```

### missing second dimension

 when we refer to an array missing a second dimension, we're generally talking about a one-dimensional array, often known as a 1D array or a vector. In other words, this is an array that has only one axis. 

Here's what it means:

1. **Shape**: If you query the shape of a 1D array, you'll get something like `(n,)` where `n` is the number of elements. The missing second dimension is evident by the single comma. For a 2D array, the shape would look like `(m, n)`.

2. **Accessing Elements**: For a 1D array, you only need one index to access its elements: `array[i]`. In contrast, for a 2D array, you'd use two indices: `array[i, j]`.

3. **Visualization**: You can think of a 1D array as a simple list or a linear set of items. A 2D array can be visualized as a grid or a matrix.

Example of a 1D array:

```python
array = np.arange(3)
print(array.shape)
print(array.tolist())
print(array.reshape(3,1).tolist())
```
Output: 
```
(3,)
[0, 1, 2]
[[0], [1], [2]]
```
It's worth noting that a 1D array is different from a 2D row or column vector. A column vector has a shape like `(n, 1)`, while a row vector has a shape like `(1, n)`. However, a 1D array's shape will just be `(n,)`.


### ravel

Return a contiguous flattened array. A copy is made only if needed.
```
x=np.array([[2,4,1],[7,2,3]])
# 'C' means c style, row major
# 'F' means fortran style, column major
print("x:\n",x)
print("x.ravel(order='C'):",x.ravel(order='C'))
print("x.ravel(order='F'):",x.ravel(order='F'))
```
outputs:

```
x:
 [[2 4 1]
 [7 2 3]]
x.ravel(order='C'): [2 4 1 7 2 3]
x.ravel(order='F'): [2 7 4 2 1 3]
```



### Flattern

Return a copy of the array collapsed into one dimension
```
print(x.flatten(order='F'))
```

### Reshape
```
print(x.reshape((6,1),order='C'))
```

### Squeez

This function removes one-dimensional entry from the shape of the given array.

```
x=np.random.randint(5 ,size=(1,3,2))
print("x.shape:",x.shape)
print("x.squeeze().shape:",x.squeeze().shape)
```

outputs:
```
x.shape: (1, 3, 2)
x.squeeze().shape: (3, 2)
```



### concatenate, vstack, hstack
```
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
```



# Random sampling 

```python
print("List of supported distributions:", 'beta', 'binomial', 'bytes', 'chisquare', 'choice', 'dirichlet', 'exponential'
      , 'f', 'gamma', 'geometric', 'get_state', 'gumbel', 'hypergeometric', 'laplace', 'logistic', 'lognormal',
      'logseries', 'multinomial', 'multivariate_normal', 'negative_binomial', 'noncentral_chisquare', 'noncentral_f',
      'normal', 'pareto', 'permutation', 'poisson', 'power', 'rand', 'randint', 'randn', 'random', 'randint',
      'random_sample', 'ranf', 'rayleigh', 'sample', 'seed', 'set_state', 'shuffle', 'standard_cauchy',
      'standard_exponential', 'standard_gamma', 'standard_normal', 'standard_t', 'triangular', 'uniform', 'vonmises',
      'wald', 'weibull', 'zipf',)
```

Refs: [1](https://docs.scipy.org/doc/np-1.14.0/reference/routines.random.html)


### uniform sampling

```python
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
```

### multivariate normal

```
mean = [0, 0]
cov = [[1, 0], [0, 100]]
size=4
print("Draw random {} samples from a multivariate normal distribution with mean={} and cov={}".format(size,mean, cov))
print(np.random.multivariate_normal(mean,cov,size))
```

# Matrix Multiplication
```
x=np.array([[2,1,1],[3,1,4]] )
y=np.random.randint(low=-1,high=4,size=[3,1])
```

so x and y are:
```
x: 
[[2 1 1]
 [3 1 4]]
 
y: 
[[2]
 [3]
 [0]]
```


1. `@` operator: calls the array's `__matmul__` method
2. `dot`: For 2-D arrays it is equivalent to matrix multiplication, and for 1-D arrays to inner product of vectors
 (without complex conjugation). 
``` 
print("x@y:\n",x@y)
print("np.matmul(x,y):\n",np.matmul(x,y) )
print("np.dot(x,y): \n",np.dot(x,y) )
```
which gives you 

```python
x@y:
 [[ 5]
 [11]]
matmul(x,y):
 [[ 5]
 [11]]
dot(x,y): 
 [[ 5]
 [11]]
```
For `N` dimensions it is a sum product over the last axis of a and the second-to-last of b

```
a = np.random.rand(8,13,13)
b = np.random.rand(8,13,13)
print(np.dot(a,b).shape )
print(np.matmul(a,b).shape )
```

### View, Copy 
copy is a new array, and the view is just a view of the original array.
 view does not own the data and any changes made to the view will affect the original array, and any changes
 made to the original array will affect the view.
```
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
```

### Broadcasting
broadcasting describes how np treats arrays with different shapes during arithmetic operations.
```
arr = np.arange(12).reshape(3,4)
col_vector = np.array([5,6,7])
```
now how do we add the vector to the array? 

```
#       arr         + col_vector

# [[ 0  1  2  3]     | 5  | 
#  [ 4  5  6  7]   + | 6  | = ?
#  [ 8  9 10 11]]    | 7  |
```

1. First solution, using loops:
```
num_cols = arr.shape[1]

for col in range(num_cols):
	arr[:, col] += col_vector

```

2. Second solution: column-stacking approach turning the col_vector into an array:

```
[[ 0  1  2  3]       [[5 5 5 5]
[4  5  6  7]     +   [6 6 6 6]
[8  9 10 11]]        [7 7 7 7]]
```

```
arr = np.arange(12).reshape(3,4)
add_matrix = np.array([col_vector,] * num_cols).T

arr += add_matrix
```


3. Third solution: Broadcasting
broadcasting allows operations to be performed on arrays of different shapes. Broadcasting automatically expands the smaller array's shape to match the larger array's shape so that they have compatible shapes for element-wise operations. It's a powerful feature that allows for efficient operations without actually copying any data.

Here's an example to illustrate broadcasting:

### Broadcasting a Scalar to a 2D Array:

```python
import numpy as np

# Create a 2D array
arr = np.array([[1, 2, 3],
                [4, 5, 6],
                [7, 8, 9]])

# Add a scalar (broadcasting the scalar to each element)
result = arr + 10

print(result)
# Output:
# [[11 12 13]
#  [14 15 16]
#  [17 18 19]]
```

Here, the scalar `10` is broadcasted to each element of the `arr`.

### Broadcasting a 1D Array to a 2D Array:

```python
import numpy as np

# Create a 2D array
arr_2d = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Create a 1D array
arr_1d = np.array([1, 0, 1])

# Add the 1D array to each row of the 2D array
result = arr_2d + arr_1d

print(result)
# Output:
# [[ 2  2  4]
#  [ 5  5  7]
#  [ 8  8 10]]
```

In this example, `arr_1d` is broadcasted to each row of `arr_2d`.

**Note**: Broadcasting has rules regarding the compatibility of shapes. For example, dimensions are considered compatible when:

- They are equal, or
- One of them is 1.

If these conditions are not met, a `ValueError` is raised, indicating that the arrays have incompatible shapes for the operation.


### np.vectorize
 `np.vectorize` is a class that converts an ordinary Python function, which accepts scalars and returns scalars, into a "vectorized" function that can operate on (and return) entire arrays. It provides a way to apply the function element-wise on input arrays.

However, it's worth noting that `np.vectorize` doesn't make your code inherently faster. Under the hood, it essentially uses a loop to apply the given function to each element in the input arrays. The primary purpose of `np.vectorize` is to transform a scalar function into one that can operate on and return arrays, making the code cleaner and more in line with NumPy's broadcasting semantics.

### Basic Usage:

```python
import numpy as np

def scalar_function(x):
    return x * x

vectorized_function = np.vectorize(scalar_function)

# Using the vectorized function on an array
arr = np.array([1, 2, 3, 4, 5])
print(vectorized_function(arr))
# Output: [ 1  4  9 16 25]
```

### With Multiple Input Arrays:

The vectorized function can also handle multiple input arrays:

```python
import numpy as np

def scalar_add(x, y):
    return x + y

vectorized_add = np.vectorize(scalar_add)

arr1 = np.array([1, 2, 3])
arr2 = np.array([4, 5, 6])

print(vectorized_add(arr1, arr2))
# Output: [5 7 9]
```

### When to Use:

1. **Function Transformation**: As mentioned, the primary purpose is to convert a scalar function into one that works with arrays.
2. **Readability**: It can make the code cleaner when working with NumPy arrays.

### When Not to Use:

1. **Performance**: If you're looking for performance gains, it's usually better to use native NumPy functions or operations that inherently support array computations, as they are implemented in optimized C or Fortran code.
2. **Complex Operations**: For more complicated operations where performance is critical, consider using NumPy's built-in functions or other optimized tools such as `numba` or Cython.

In essence, `np.vectorize` is a convenience function, but if performance is a concern, it's essential to be aware of its loop-like nature under the hood.



### Lambda functions

Lambda functions are anonymous functions defined using the `lambda` keyword in Python. They can be used in tandem with functions like `np.apply_along_axis()` to apply operations element-wise or along a specified axis of a NumPy array.

Here are a couple of examples demonstrating the use of lambda functions with NumPy arrays:

### 1. Applying a Lambda Function Element-wise to a 1D Array:

```python
import numpy as np

# Create a simple 1D array
arr = np.array([1, 2, 3, 4, 5])

# Use lambda to square each element
squared = np.vectorize(lambda x: x**2)(arr)

print(squared)  # Output: [ 1  4  9 16 25]
```

In this example, we use `np.vectorize()` to vectorize the lambda function, allowing it to operate on each element of the array.

### 2. Applying a Lambda Function Along an Axis of a 2D Array:

```python
import numpy as np

# Create a 2D array
arr_2d = np.array([[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]])

# Use lambda to compute the sum of each row
row_sum = np.apply_along_axis(lambda x: np.sum(x), axis=1, arr=arr_2d)

print(row_sum)  # Output: [ 6 15 24]
```

In this example, `np.apply_along_axis()` applies the lambda function (which computes the sum) along `axis=1`, thus computing the sum for each row.

Remember, while lambda functions offer a concise way to define simple functions, they might make the code less readable if the operations are complex. In such cases, it might be better to define a standalone function instead of using lambda.

### operation on numpy arrays

```
x=np.arange(5)
selected_index=[True,True,False, True,False]
print(x[selected_index])

y=x>3
print(y)
print(x[y])
```


