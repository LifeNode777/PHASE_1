"""
§4.2 Embedding (Takens) + §4.3 Windows & derivatives.
- τ: first local minimum of mutual information (64-bin)
- m: False Nearest Neighbors, smallest m with FNN < 0.10, bounded 3..6
- Windows: 60 s, stride 15 s (75% overlap)
- Savitzky-Golay smoothing + derivatives
"""
from __future__ import annotations
import numpy as np
from scipy.signal import savgol_filter
from scipy.stats import spearmanr
from config import (
    MI_BINS, MAX_LAG_S, FNN_THRESHOLD, M_MIN, M_MAX,
    WINDOW_S, STRIDE_S, SG_WINDOW, SG_POLY, TARGET_FS,
)

# ─── Mutual information (histogram estimator) ───────────────────────────────
def _histogram_mi(x: np.ndarray, y: np.ndarray, bins: int = MI_BINS) -> float:
    """Histogram-based mutual information I(x; y) in nats."""
    cx = np.bincount(np.digitize(x, np.histogram_bin_edges(x, bins=bins)) - 1, minlength=bins).astype(float)
    cy = np.bincount(np.digitize(y, np.histogram_bin_edges(y, bins=bins)) - 1, minlength=bins).astype(float)
    cxy = np.zeros((bins, bins), dtype=float)
    ix = np.digitize(x, np.histogram_bin_edges(x, bins=bins)) - 1
    iy = np.digitize(y, np.histogram_bin_edges(y, bins=bins)) - 1
    np.add.at(cxy, (ix, iy), 1.0)
    n = cxy.sum()
    if n == 0:
        return 0.0
    pxy = cxy / n
    px = cx / n
    py = cy / n
    mi = 0.0
    for i in range(bins):
        for j in range(bins):
            if pxy[i, j] > 0 and px[i] > 0 and py[j] > 0:
                mi += pxy[i, j] * np.log(pxy[i, j] / (px[i] * py[j]))
    return mi

def mutual_information_lag(x: np.ndarray, fs: float) -> tuple[int, float]:
    """
    First local minimum of MI(x(t), x(t+lag)).
    Search lag ≤ MAX_LAG_S seconds.
    Returns (tau_samples, tau_seconds).
    """
    max_lag = int(MAX_LAG_S * fs)
    n = len(x)
    # Subsample for speed if signal is long
    step = max(1, n // 20000)
    xs = x[::step]
    max_lag_s = max_lag // step
    if max_lag_s < 2:
        max_lag_s = 2
    mis = []
    for lag in range(1, max_lag_s + 1):
        mis.append(_histogram_mi(xs[:-lag] if lag > 0 else xs, xs[lag:]))
    mis = np.array(mis)
    # First local minimum
    tau = 1
    for i in range(1, len(mis) - 1):
        if mis[i] < mis[i - 1] and mis[i] <= mis[i + 1]:
            tau = i + 1
            break
    tau_samples = tau * step
    tau_s = tau_samples / fs
    return tau_samples, tau_s

# ─── False Nearest Neighbors ────────────────────────────────────────────────
def false_nearest_neighbors(x: np.ndarray, tau: int) -> tuple[int, list[float]]:
    """
    Returns (m, fnn_fractions) where m is smallest embedding dim with FNN < FNN_THRESHOLD,
    bounded in [M_MIN, M_MAX].
    """
    fnn_fractions = []
    chosen_m = M_MAX
    for m in range(M_MIN, M_MAX + 1):
        emb = delay_embed(x, m, tau)
        if len(emb) < 20:
            fnn_fractions.append(1.0)
            continue
        # Use sklearn-style FNN via distance ratio
        from scipy.spatial import KDTree
        tree = KDTree(emb)
        dists, idxs = tree.query(emb, k=2)
        d1 = dists[:, 1]
        # Project to m+1 and recompute
        emb1 = delay_embed(x, m + 1, tau) if m + 1 <= M_MAX else None
        if emb1 is None or len(emb1) != len(emb):
            fnn_fractions.append(0.0)
            chosen_m = m
            break
        tree1 = KDTree(emb1)
        dists1, _ = tree1.query(emb1, k=2)
        d2 = dists1[:, 1]
        # FNN criterion: |d2 - d1| / d1 > threshold (R_TOL=10)
        with np.errstate(divide="ignore", invalid="ignore"):
            ratio = np.abs(d2 - d1) / np.where(d1 > 1e-12, d1, 1e-12)
        fnn_frac = float(np.mean(ratio > 10.0))
        fnn_fractions.append(fnn_frac)
        if fnn_frac < FNN_THRESHOLD:
            chosen_m = m
            break
    return chosen_m, fnn_fractions

# ─── Delay embedding ────────────────────────────────────────────────────────
def delay_embed(x: np.ndarray, m: int, tau: int) -> np.ndarray:
    """Returns array of shape (n - (m-1)*tau, m)."""
    n = len(x)
    length = n - (m - 1) * tau
    if length <= 0:
        return x.reshape(-1, 1)
    return np.column_stack([x[i * tau : i * tau + length] for i in range(m)])

# ─── Windows + Savitzky-Golay derivatives ───────────────────────────────────
def make_windows(x: np.ndarray, fs: float) -> list[tuple[int, int]]:
    """
    Returns list of (start_sample, end_sample) for 60 s windows with 15 s stride.
    """
    win = int(WINDOW_S * fs)
    stride = int(STRIDE_S * fs)
    n = len(x)
    windows = []
    start = 0
    while start + win <= n:
        windows.append((start, start + win))
        start += stride
    return windows

def sg_smooth_and_derivatives(segment: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Savitzky-Golay smoothing + 1st and 2nd derivatives.
    Returns (smoothed, velocity, acceleration).
    """
    # Ensure window length is odd and <= segment length
    w = SG_WINDOW
    if w > len(segment):
        w = len(segment) if len(segment) % 2 == 1 else len(segment) - 1
    if w < SG_POLY + 2:
        w = SG_POLY + 2 if (SG_POLY + 2) % 2 == 1 else SG_POLY + 3
    smoothed = savgol_filter(segment, w, SG_POLY, deriv=0)
    # Derivatives: savgol with dt=1/fs
    dt = 1.0 / TARGET_FS
    velocity = savgol_filter(segment, w, SG_POLY, deriv=1, delta=dt)
    acceleration = savgol_filter(segment, w, SG_POLY, deriv=2, delta=dt)
    return smoothed, velocity, acceleration
