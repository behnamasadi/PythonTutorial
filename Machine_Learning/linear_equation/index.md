# Linear matrix equation
system of equations 
```
x0 + 2 * x1 = 1 
3 * x0 + 5 * x1 = 2:
```


```python
a = np.array([[1, 2], [3, 5]])
b = np.array([1, 2])
x = np.linalg.solve(a, b)
```

Checking the correct of solution :

```
np.allclose(np.dot(a, x), b)
```
`a` must be square and of full-rank, i.e., all rows (or, equivalently, columns) must be linearly independent; if either is not true, use `lstsq` for the least-squares best “solution” of the system/equation.


Refs: [1](https://numpy.org/doc/stable/reference/generated/numpy.linalg.solve.html)





# Least-Squares Solution
Computes the vector x that approximately solves the equation `a @ x = b`. The equation may be under-, well-, or over-determined


```python


```


Ref: [1](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html#numpy.linalg.lstsq)
