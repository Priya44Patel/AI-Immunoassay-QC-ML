"""
Purpose

QC metrics: CV, recovery, outliers
"""

"""
qc_utils.py
-----------
Quality control metrics for immunoassays.
"""

import numpy as np
import pandas as pd


def compute_cv(signal_series: pd.Series) -> float:
    """
    Calculate % coefficient of variation.
    """
    if len(signal_series) < 2:
        return float("nan")
    return signal_series.std() / signal_series.mean() * 100


def compute_recovery(measured, expected):
    """
    Percent recovery.
    """
    if expected == 0 or pd.isna(expected):
        return float("nan")
    return measured / expected * 100


def flag_outliers(series: pd.Series, z_thresh=3):
    """
    Flag outliers using Z-score.
    """
    z = (series - series.mean()) / series.std()
    return abs(z) > z_thresh
