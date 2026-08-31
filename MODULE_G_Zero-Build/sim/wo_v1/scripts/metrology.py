"""
§4.4 Phase binning & Reeb proxy R
§4.5 Four θ renderings
§4.6 Indicatrix, F, g_ij, cond(g) (with covariance proxy fallback)
"""
from __future__ import annotations
import numpy as np
from scipy.spatial import ConvexHull, KDTree
from scipy.stats import bootstrap as scipy_bootstrap
from config import (
    N_PHASE_BINS, MIN_SAMPLES_PER_BIN, MAX_HULL_POINTS,
    BOOTSTRAP_B, FD_DIRECTIONS, QHULL_FAIL_RATE_LIMIT,
)

# ─── Phase binning ──────────────────────────────────────────────────────────
def compute_phase_and_bin(
    emb: np.ndarray, velocities: np.ndarray
) -> tuple[np.ndarray, np.ndarray, list[dict]]:
    """
    PCA → PC1 → Hilbert phase → 32 bins.
    Returns (phases, bin_indices, bin_stats).
    bin_stats: list of dicts with mean_position, mean_unit_velocity, count.
    """
    # PCA via SVD
    centered = emb - emb.mean(axis=0)
    U, S, Vt = np.linalg.svd(centered, full_matrices=False)
    pc1 = U[:, 0] * S[0]
    # Hilbert phase
    analytic = np.fft.hilbert(pc1)
    phases = np.angle(analytic)  # (-pi, pi]
    # Bin
    bin_edges = np.linspace(-np.pi, np.pi, N_PHASE_BINS + 1)
    bin_indices = np.digitize(phases, bin_edges) - 1
    bin_indices = np.clip(bin_indices, 0, N_PHASE_BINS - 1)
    # Per-bin stats
    bin_stats = []
    for b in range(N_PHASE_BINS):
        mask = bin_indices == b
        count = int(mask.sum())
        if count > 0:
            mean_pos = emb[mask].mean(axis=0)
            vels = velocities[mask]
            norms = np.linalg.norm(vels, axis=1, keepdims=True)
            norms = np.where(norms > 1e-12, norms, 1.0)
            unit_vels = vels / norms
            mean_unit_vel = unit_vels.mean(axis=0)
            nrm = np.linalg.norm(mean_unit_vel)
            if nrm > 1e-12:
                mean_unit_vel = mean_unit_vel / nrm
        else:
            mean_pos = np.zeros(emb.shape[1])
            mean_unit_vel = np.zeros(emb.shape[1])
        bin_stats.append({
            "bin": b, "count": count,
            "mean_position": mean_pos, "mean_unit_velocity": mean_unit_vel,
        })
    return phases, bin_indices, bin_stats

def check_window_accepted(bin_stats: list[dict]) -> bool:
    return all(s["count"] >= MIN_SAMPLES_PER_BIN for s in bin_stats)

# ─── Reeb proxy R(φ) ────────────────────────────────────────────────────────
def reeb_cycle(bin_stats: list[dict]) -> np.ndarray:
    """Mean positions per bin → closed cycle (N_PHASE_BINS, m)."""
    return np.array([s["mean_position"] for s in bin_stats])

# ─── Convex hull & Minkowski functional ─────────────────────────────────────
def build_indicatrix(velocities: np.ndarray) -> tuple[ConvexHull | None, np.ndarray]:
    """
    Subsample to MAX_HULL_POINTS, build convex hull of velocity vectors.
    Returns (hull, subsampled_velocities). hull is None if Qhull fails.
    """
    n = len(velocities)
    if n > MAX_HULL_POINTS:
        idx = np.random.choice(n, MAX_HULL_POINTS, replace=False)
        vsub = velocities[idx]
    else:
        vsub = velocities
    try:
        hull = ConvexHull(vsub)
        return hull, vsub
    except Exception:
        return None, vsub

def minkowski_gauge(hull: ConvexHull, points: np.ndarray) -> np.ndarray:
    """
    F(w) = gauge of convex hull at points.
    Using facet inequalities: hull.equations are A x + b <= 0.
    F(w) = max over facets of (A w) / (-b)  [for b < 0].
    """
    A = hull.equations[:, :-1]
    b = hull.equations[:, -1]
    # For each point, F = max_i (A_i · w) / (-b_i) where b_i < 0
    # Normalize so that points on hull have F ≈ 1
    Aw = points @ A.T  # (n_points, n_facets)
    # For facets with b < 0: ratio = Aw / (-b)
    neg_b = -b
    valid = neg_b > 1e-12
    if not valid.any():
        return np.ones(len(points))
    ratios = Aw[:, valid] / neg_b[valid]
    F = ratios.max(axis=1)
    return np.where(F > 1e-12, F, 1e-12)

def origin_interior(hull: ConvexHull) -> bool:
    """Check if origin is inside the convex hull."""
    try:
        # Test: all facet equations satisfied at origin → b <= 0
        return bool(np.all(hull.equations[:, -1] <= 1e-9))
    except Exception:
        return False

# ─── θ renderings (§4.5) ────────────────────────────────────────────────────
def theta_canon(
    velocities: np.ndarray, bin_stats: list[dict], bin_indices: np.ndarray
) -> np.ndarray:
    """
    θ_canon = mean over samples of ⟨v, R(φ)⟩ / (F(v)·F(R(φ))).
    Using Euclidean inner product after normalisation (see METHODS_NOTES.md).
    Returns scalar in [0, 1].
    """
    n = len(velocities)
    if n == 0:
        return np.nan
    # Per-sample: look up R(φ) from bin
    R_phi = np.array([bin_stats[b]["mean_unit_velocity"] for b in bin_indices])
    v_norms = np.linalg.norm(velocities, axis=1, keepdims=True)
    v_norms = np.where(v_norms > 1e-12, v_norms, 1.0)
    v_unit = velocities / v_norms
    # Cosine similarity
    cos = np.sum(v_unit * R_phi, axis=1)
    cos = np.clip(cos, -1.0, 1.0)
    # Map [-1, 1] → [0, 1]
    theta = 0.5 * (cos + 1.0)
    return float(np.mean(theta))

def theta_proj(
    velocities: np.ndarray, emb: np.ndarray, bin_stats: list[dict], bin_indices: np.ndarray
) -> float:
    """
    θ_proj = ∫⟨v, R(φ)⟩₊ dt / ∫‖δγ‖ dt
    δγ = deviation from per-bin mean cycle position.
    """
    n = len(velocities)
    if n == 0:
        return np.nan
    R_phi = np.array([bin_stats[b]["mean_position"] for b in bin_indices])
    delta_gamma = emb - R_phi
    numerator = np.sum(np.maximum(np.sum(velocities * R_phi, axis=1), 0.0))
    denominator = np.sum(np.linalg.norm(delta_gamma, axis=1))
    if denominator < 1e-12:
        return np.nan
    return float(numerator / denominator)

def theta_curv_TT(velocities: np.ndarray, accelerations: np.ndarray) -> float:
    """
    θ_curv_TT = ∫ κ²‖v² dt / ∫ ‖v‖² dt
    κ = sqrt(‖v‖²‖a‖² − ⟨v,a⟩²) / ‖v‖³
    """
    n = len(velocities)
    if n == 0:
        return np.nan
    v2 = np.sum(velocities ** 2, axis=1)
    a2 = np.sum(accelerations ** 2, axis=1)
    va = np.sum(velocities * accelerations, axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        kappa2 = np.maximum(v2 * a2 - va ** 2, 0.0) / np.where(v2 > 1e-24, v2 ** 3, 1e-24)
    num = np.sum(kappa2 * v2)
    den = np.sum(v2)
    if den < 1e-12:
        return np.nan
    return float(num / den)

def theta_curv_ASC(velocities: np.ndarray, accelerations: np.ndarray) -> float:
    """
    θ_curv_ASC = ∫ ‖a‖·‖v dt / ∫ ‖v‖² dt
    """
    n = len(velocities)
    if n == 0:
        return np.nan
    v_norm = np.linalg.norm(velocities, axis=1)
    a_norm = np.linalg.norm(accelerations, axis=1)
    num = np.sum(a_norm * v_norm)
    den = np.sum(v_norm ** 2)
    if den < 1e-12:
        return np.nan
    return float(num / den)

# ─── Anisotropy proxy: cond(g) from covariance of unit velocities ───────────
def anisotropy_proxy(velocities: np.ndarray) -> dict:
    """
    Primary reported cond(g): condition number of covariance of unit velocities.
    Returns dict with cond_g, eigenvalues, log_cond_g.
    """
    norms = np.linalg.norm(velocities, axis=1, keepdims=True)
    norms = np.where(norms > 1e-12, norms, 1.0)
    unit_v = velocities / norms
    cov = np.cov(unit_v, rowvar=False)
    if cov.ndim == 0:
        cov = np.array([[cov]])
    eigvals = np.linalg.eigvalsh(cov)
    eigvals = np.sort(eigvals)[::-1]
    lam_max = max(eigvals[0], 1e-12)
    lam_min = max(eigvals[-1], 1e-12)
    cond = lam_max / lam_min
    return {
        "cond_g": float(cond),
        "log_cond_g": float(np.log(cond)),
        "lambda_max": float(lam_max),
        "lambda_min": float(lam_min),
        "eigenvalues": [float(e) for e in eigvals],
    }

def bootstrap_cond_g(velocities: np.ndarray, B: int = BOOTSTRAP_B) -> dict:
    """
    Bootstrap B=200 resamples of velocity cloud → 95% CI of cond(g).
    Returns dict with median, ci95_lo, ci95_hi.
    """
    n = len(velocities)
    if n < 10:
        return {"cond_g_bootstrap_median": np.nan, "cond_g_ci95": (np.nan, np.nan)}
    conds = []
    rng = np.random.default_rng(1618)
    for _ in range(B):
        idx = rng.choice(n, size=n, replace=True)
        res = anisotropy_proxy(velocities[idx])
        conds.append(res["cond_g"])
    conds = np.array(conds)
    lo, hi = np.percentile(conds, [2.5, 97.5])
    return {
        "cond_g_bootstrap_median": float(np.median(conds)),
        "cond_g_ci95": (float(lo), float(hi)),
        "cond_g_bootstrap_samples": conds.tolist(),
    }
