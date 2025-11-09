# -*- coding: utf-8 -*-
"""
Parametric Curve Fitting using L1 Minimization
----------------------------------------------
Fits (θ, M, X) for the curve:
x = t*cos(θ) - e^{M|t|}*sin(0.3t)*sin(θ) + X
y = 42 + t*sin(θ) + e^{M|t|}*sin(0.3t)*cos(θ)

Author: Venkatesh
Date: November 2025
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize
import sys
# Handle special characters (e.g., θ)
sys.stdout.reconfigure(encoding="utf-8")

# -------------------------------
# 1. Load data
# -------------------------------
data = pd.read_csv('xy_data.csv')
x_data = data['x'].values
y_data = data['y'].values
N = len(x_data)

# -------------------------------
# 2. Define the parametric model
# -------------------------------
def curve(t, theta, M, X):
    """Return x, y coordinates for given t."""
    x = t * np.cos(theta) - np.exp(M * np.abs(t)) * np.sin(0.3 * t) * np.sin(theta) + X
    y = 42 + t * np.sin(theta) + np.exp(M * np.abs(t)) * np.sin(0.3 * t) * np.cos(theta)
    return x, y

# -------------------------------
# 3. For each observed point, find best t ∈ [6, 60]
# -------------------------------
def best_t_for_point(x_obs, y_obs, theta, M, X, t0):
    def dist_sq(t_val):
        # Ensure scalar t
        t = t_val[0] if isinstance(t_val, (list, np.ndarray)) else t_val
        x, y = curve(t, theta, M, X)
        return (x - x_obs) ** 2 + (y - y_obs) ** 2

    res = minimize(dist_sq, [t0], bounds=[(6, 60)], method='L-BFGS-B')
    return float(res.x[0])

# -------------------------------
# 4. Define total L1 loss
# -------------------------------
def total_l1(params):
    theta, M, X = params
    total = 0.0

    # Initial t guesses
    sin_t = np.sin(theta)
    cos_t = np.cos(theta)
    if abs(sin_t) > 0.1:
        t_guess = (y_data - 42) / sin_t
    else:
        t_guess = (x_data - X) / (cos_t + 1e-8)

    t_guess = np.clip(t_guess, 6, 60)

    # Compute L1 distance
    for i in range(N):
        t_opt = best_t_for_point(x_data[i], y_data[i], theta, M, X, t_guess[i])
        x_pred, y_pred = curve(t_opt, theta, M, X)
        total += abs(x_pred - x_data[i]) + abs(y_pred - y_data[i])

    return total

# -------------------------------
# 5. Optimization setup
# -------------------------------
initial_guess = [0.826, 0.0742, 11.58]
bounds = [
    (np.deg2rad(0.1), np.deg2rad(50)),  # theta: 0.1° to 50°
    (0.06, 0.09),                       # M: around 0.0742
    (5, 20)                             # X: near 11.5
]

print("🚀 Optimizing... Please wait (may take up to a minute)...")

result = minimize(
    total_l1,
    initial_guess,
    method='L-BFGS-B',
    bounds=bounds,
    options={'ftol': 1e-12, 'maxfun': 5000}
)

theta_opt, M_opt, X_opt = result.x
l1_score = result.fun

# -------------------------------
# 6. Print results
# -------------------------------
print("\n✅ Optimization Complete!")
print(f"θ = {theta_opt:.6f} rad ({np.degrees(theta_opt):.4f}°)")
print(f"M = {M_opt:.6f}")
print(f"X = {X_opt:.6f}")
print(f"Total L1 Distance = {l1_score:.6f}")

# -------------------------------
# 7. Generate clean LaTeX string
# -------------------------------
latex_str = (
    f"\\left(t\\cos({theta_opt:.6f}) - e^{{{M_opt:.6f}\\left|t\\right|}}"
    f"\\sin(0.3t)\\sin({theta_opt:.6f}) + {X_opt:.4f}, "
    f"42 + t\\sin({theta_opt:.6f}) + e^{{{M_opt:.6f}\\left|t\\right|}}"
    f"\\sin(0.3t)\\cos({theta_opt:.6f})\\right)"
)

print("\n" + "=" * 80)
print("📋 FINAL LATEX OUTPUT (Copy this for Desmos Submission):")
print("=" * 80)
print(latex_str)
print("=" * 80)

# -------------------------------
# 8. Save to file
# -------------------------------
with open('submission.txt', 'w', encoding='utf-8') as f:
    f.write(latex_str + '\n')

print("\n✅ Saved to 'submission.txt'")
