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
