"""Purpose

Fit 4PL curves to standards

Plot fitted curves
"""
"""
curve_fit.py
------------
4-parameter logistic (4PL) curve fitting.
"""

import numpy as np
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score


def four_pl(x, A, B, C, D):
    """
    4PL equation.
    """
    return A + (D - A) / (1 + (x / C) ** B)


def fit_4pl(conc, signal):
    """
    Fit a 4PL curve to standards.
    """
    x = np.array(conc, dtype=float)
    y = np.array(signal, dtype=float)

    p0 = [min(y), 1.0, np.median(x), max(y)]
    params, _ = curve_fit(four_pl, x, y, p0=p0, maxfev=10000)

    y_pred = four_pl(x, *params)
    r2 = r2_score(y, y_pred)

    return params, r2


def generate_curve(params, xmin=0.1, xmax=20, points=200):
    """
    Generate fitted curve values.
    """
    x = np.logspace(np.log10(xmin), np.log10(xmax), points)
    y = four_pl(x, *params)
    return x, y
