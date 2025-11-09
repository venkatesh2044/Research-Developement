import numpy as np
import pandas as pd
from scipy.optimize import minimize
import sys
# Fix charmap encoding error in Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Load and analyze data
data = pd.read_csv('xy_data.csv')
x_data = data['x'].values
y_data = data['y'].values

print(f"Data range: x=[{x_data.min():.1f}, {x_data.max():.1f}], y=[{y_data.min():.1f}, {y_data.max():.1f}]")

def parametric_curve(t, theta, M, X):
    x = t * np.cos(theta) - np.exp(M * np.abs(t)) * np.sin(0.3 * t) * np.sin(theta) + X
    y = 42 + t * np.sin(theta) + np.exp(M * np.abs(t)) * np.sin(0.3 * t) * np.cos(theta)
    return x, y

def objective(params):
    theta, M, X = params
    
    # Use the same t values that likely generated the data
    t_vals = np.linspace(6, 60, len(x_data))
    x_pred, y_pred = parametric_curve(t_vals, theta, M, X)
    
    # Calculate total distance
    distance = np.mean(np.sqrt((x_pred - x_data)**2 + (y_pred - y_data)**2))
    return distance

# Run optimization with better bounds
bounds = [(0.7, 0.9), (0.06, 0.09), (15, 25)]
result = minimize(objective, [0.8, 0.075, 20], bounds=bounds, method='L-BFGS-B')

print(f"Optimized parameters: θ={result.x[0]:.4f}, M={result.x[1]:.4f}, X={result.x[2]:.4f}")
print(f"Average error: {result.fun:.4f}")

# Generate fitted curve for verification
t_vals_fine = np.linspace(6, 60, 200)
x_fit, y_fit = parametric_curve(t_vals_fine, result.x[0], result.x[1], result.x[2])

# Save results
results_dict = {
    'optimized_theta': float(result.x[0]),
    'optimized_M': float(result.x[1]), 
    'optimized_X': float(result.x[2]),
    'average_error': float(result.fun),
    'optimization_success': bool(result.success)
}

print("\nResults summary:")
for key, value in results_dict.items():
    print(f"  {key}: {value}")