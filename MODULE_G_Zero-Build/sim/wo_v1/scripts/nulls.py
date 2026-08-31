"""
§4.7 Null models
(a) FT surrogates (phase-shuffled, spectrum preserved)
(b) AR(1) matched autocorrelation
(c) Isotropic renormalization (random SO(m) rotations of velocities)
"""
from __future__ import annotations
import numpy as np
from config import N_NULLS

# ─── (a) FT surrogates ──────────────────────────────────────────────────────
def ft_surrogate(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """
    Phase-randomized surrogate: preserve amplitude spectrum, randomize phases.
    """
    X = np.fft.rfft(x)
    phases = rng.uniform(0, 2 * np.pi, size=len(X))
    phases[0] = 0.0  # DC component stays
    if len(X) > 1 and len(x) % 2 == 0:
        phases[-1] = 0.0  # Nyquist stays real
    X_surr = np.abs(X) * np.exp(1j * phases)
    return np.fft.irfft(X_surr, n=len(x))

def generate_ft_surrogates(x: np.ndarray, n: int = N_NULLS, seed_offset: int = 0) -> list[np.ndarray]:
    rng = np.random.default_rng(1618 + seed_offset)
    return [ft_surrogate(x, rng) for _ in range(n)]

# ─── (b) AR(1) ──────────────────────────────────────────────────────────────
def ar1_surrogate(x: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """
    AR(1) with matched lag-1 autocorrelation and variance.
    """
    n = len(x)
    x_centered = x - x.mean()
    var = x_centered.var()
    if var < 1e-12:
        return np.zeros_like(x)
    rho = float(np.corrcoef(x_centered[:-1], x_centered[1:])[0, 1])
    rho = np.clip(rho, -0.999, 0.999)
    sigma = np.sqrt(var * (1 - rho ** 2))
    noise = rng.normal(0, sigma, size=n)
    y = np.zeros(n)
    y[0] = noise[0]
    for i in range(1, n):
        y[i] = rho * y[i - 1] + noise[i]
    return y + x.mean()

def generate_ar1_surrogates(x: np.ndarray, n: int = N_NULLS, seed_offset: int = 0) -> list[np.ndarray]:
    rng = np.random.default_rng(1618 + 1000 + seed_offset)
    return [ar1_surrogate(x, rng) for _ in range(n)]

# ─── (c) Isotropic renormalization ─────────────────────────────────────────
def isotropic_rotate(velocities: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """
    Per-sample velocity rotated by uniform random rotation in SO(m).
    Preserves speed distribution, destroys direction-speed pairing.
    """
    m = velocities.shape[1]
    norms = np.linalg.norm(velocities, axis=1, keepdims=True)
    norms = np.where(norms > 1e-12, norms, 1.0)
    unit_v = velocities / norms
    n = len(velocities)
    rotated = np.zeros_like(unit_v)
    for i in range(n):
        Q = random_rotation(m, rng)
        rotated[i] = Q @ unit_v[i]
    return rotated * norms

def random_rotation(m: int, rng: np.random.Generator) -> np.ndarray:
    """
    Haar-distributed random rotation in SO(m) via QR of random Gaussian.
    """
    Z = rng.standard_normal((m, m))
    Q, R = np.linalg.qr(Z)
    # Make it proper rotation (det = +1)
    signs = np.sign(np.diag(R))
    signs[signs == 0] = 1.0
    Q = Q * signs
    if np.linalg.det(Q) < 0:
        Q[:, 0] = -Q[:, 0]
    return Q

def generate_isotropic_surrogates(
    velocities: np.ndarray, n: int = N_NULLS, seed_offset: int = 0
) -> list[np.ndarray]:
    rng = np.random.default_rng(1618 + 2000 + seed_offset)
    return [isotropic_rotate(velocities, rng) for _ in range(n)]

# ─── Null envelope for E4′ ──────────────────────────────────────────────────
def null_envelope_isotropic(
    velocities_per_window: list[np.ndarray], n_per_window: int = N_NULLS
) -> np.ndarray:
    """
    For each window, generate n isotropic surrogates, compute cond(g) proxy,
    take 95th percentile across surrogates → envelope per window.
    Returns array of shape (n_windows,).
    """
    from metrology import anisotropy_proxy
    envelopes = []
    for v in velocities_per_window:
        if len(v) < 10:
            envelopes.append(np.nan)
            continue
        conds = []
        rng = np.random.default_rng(1618)
        for _ in range(n_per_window):
            v_surr = isotropic_rotate(v, rng)
            conds.append(anisotropy_proxy(v_surr)["log_cond_g"])
        envelopes.append(np.percentile(conds, 95))
    return np.array(envelopes)
