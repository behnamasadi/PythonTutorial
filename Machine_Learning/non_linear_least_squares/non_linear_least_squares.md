# Non-linear least squares
Non-linear least squares (NLS) problems arise when the objective function to be minimized is nonlinear in the parameters. These problems are prevalent in various fields, including optimization, data fitting, computer vision, and machine learning. Solving NLS problems often involves finding the values of the parameters that minimize the sum of squares of residuals (the differences between observed and predicted values). There are several methods for solving non-linear least squares problems:

1. Gauss-Newton Method:
   - The Gauss-Newton method is an iterative optimization technique used to solve non-linear least squares problems. It linearizes the objective function using first-order Taylor series expansion and updates the parameters in each iteration to minimize the sum of squares of residuals. It's fast and suitable for well-behaved problems.

2. Levenberg-Marquardt Method:
   - The Levenberg-Marquardt algorithm is an extension of the Gauss-Newton method that adds a damping term to the normal equations. It balances the gradient descent step with a step in the Gauss-Newton direction. This makes it more robust and able to handle ill-conditioned problems.

3. Trust Region Methods:
   - Trust region methods construct a quadratic approximation of the objective function in the vicinity of the current iterate. It limits the step size based on a trust region, which is a region within which the quadratic approximation is expected to be accurate. These methods are suitable for both convex and non-convex problems.

4. Quasi-Newton Methods:
   - Quasi-Newton methods use approximations to the Hessian matrix (second derivatives of the objective function) to update the parameters iteratively. These approximations are computationally cheaper than calculating the exact Hessian. Broyden-Fletcher-Goldfarb-Shanno (BFGS) and Limited-memory BFGS (L-BFGS) are popular quasi-Newton methods.

5. Gauss-Seidel Method:
   - The Gauss-Seidel method is an iterative approach that solves the non-linear least squares problem by updating the parameters sequentially. It is more suitable for problems with a large number of variables.

6. Non-linear Conjugate Gradient:
   - Non-linear conjugate gradient methods combine the conjugate gradient method from linear optimization with the Gauss-Newton or other non-linear methods to solve NLS problems.

7. Genetic Algorithms and Particle Swarm Optimization:
   - These are population-based optimization algorithms that can handle non-linear least squares problems without explicit gradients. They are useful when the objective function is noisy or highly non-convex.
   

# Example   
   
The `scipy.optimize.least_squares` function is a versatile tool for solving non-linear least squares problems. This means that you can use it to fit a model to data such that the sum of the squared differences (residuals) between the observed and predicted values is minimized.

Here's a basic example: let's fit a simple sinusoidal function to some noisy data.

1. **Problem setup**: 

Given noisy data from a sine wave \( y = A \sin(B(x + C)) \), estimate the parameters \( A \), \( B \), and \( C \).

2. **Python code**:

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

# Define the function to compute residuals.
def residuals(params, x, y_observed):
    A, B, C = params
    y_predicted = A * np.sin(B * x + C)
    return y_predicted - y_observed

# Generate synthetic noisy data
x = np.linspace(0, 2 * np.pi, 100)
A_true = 2.0
B_true = 1.0
C_true = 0.5
y_true = A_true * np.sin(B_true * x + C_true)
y_noisy = y_true + 0.5 * np.random.randn(y_true.shape[0])

# Initial guess for A, B, and C
initial_guess = [1.0, 1.0, 0.0]

# Use least_squares to fit the model
result = least_squares(residuals, initial_guess, args=(x, y_noisy))

# Extract fitted parameters
A_fit, B_fit, C_fit = result.x

# Plot
plt.plot(x, y_noisy, 'o', label='Noisy data')
plt.plot(x, y_true, 'k-', label='True data')
plt.plot(x, A_fit * np.sin(B_fit * x + C_fit), 'r-', label='Fitted data')
plt.legend()
plt.show()
```

In this example:
- `residuals` is a function that computes the difference between the observed data and the data predicted by the model for a given set of parameters.
- We generate some synthetic data with noise (`y_noisy`).
- The `least_squares` function is called to fit the model (the sine function) to the noisy data.
- We then extract the estimated parameters from the `result` object.
- Finally, we plot the true data, noisy data, and the fitted model.

Adjusting the initial guess and other parameters of `least_squares` can affect the speed and accuracy of the fitting process.   
