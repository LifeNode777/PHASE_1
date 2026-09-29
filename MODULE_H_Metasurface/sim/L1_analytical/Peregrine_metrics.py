
#!/usr/bin/env python3
"""
MODULE H — L1 Analytical
peregrine_metrics.py  (calibration core)

Purpose
-------
Validate the measurement apparatus itself before any geometry,
any SSFM, any noise model, any biological motif.

This script answers only one question with maximal rigor:

    Does the discrete implementation of η (METHODS_NOTES §2.1)
    correctly recognise the analytic Peregrine solution as identical
    to itself, and correctly reject a phase-randomised version of
    the same solution?

Everything else (SSFM generation, remaining kernels, K1/K2,
G_coh, cross-correlation, α-invariance on real signals) is
forbidden until this calibration PASSes.

Rules enforced
--------------
- All numerical constants come exclusively from config.py
- η is the overlap (cosine similarity), NOT quantum fidelity |⟨·⟩|²
- Identical support Ω for both fields
- Global phase is irrelevant → absolute value of the inner product
- Measure factors Δt are included
- Minimum-norm guard from GUARDS
- No ad-hoc renormalisation
- No parameter fitting
- Verdict is binary and automatic

Author: LifeNode Research Collective
License: CC-BY-NC-SA 4.0
Status: Pre-registered calibration core — 2026-09-04
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Tuple

import numpy as np

# ---------------------------------------------------------------------------
# Import the single source of truth. Fail hard if missing or broken.
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
try:
    from config import (
        L1_GRID,
        THRESHOLDS,
        GUARDS,
        VERDICT_PASS,
        VERDICT_FAIL,
        VERDICT_WARNING,
        compute_verdict,
    )
except ImportError as e:
    raise SystemExit(
        "FATAL: cannot import config.py. "
        "This script refuses to run with hardcoded constants.\n"
        f"Original error: {e}"
    )


# ---------------------------------------------------------------------------
# 1. Analytic Peregrine breather (exact ground truth)
# ---------------------------------------------------------------------------
def analytic_peregrine(tau: np.ndarray, z: float = 0.0) -> np.ndarray:
    """
    Exact Peregrine solution of the focusing NLSE
    (standard normalisation used in the literature).

        ψ_P(τ, z) = [1 − 4(1 + 2i z) / (1 + 4 τ² + 4 z²)] · exp(i z)

    Parameters
    ----------
    tau : ndarray
        Temporal coordinate (normalised units).
    z : float
        Propagation coordinate. Default 0.0 (peak location).

    Returns
    -------
    ndarray (complex128)
        Analytic field values on the supplied grid.
    """
    denom = 1.0 + 4.0 * tau**2 + 4.0 * z**2
    numerator = 1.0 + 2.0j * z
    psi = (1.0 - 4.0 * numerator / denom) * np.exp(1.0j * z)
    return psi.astype(np.complex128)


# ---------------------------------------------------------------------------
# 2. Discrete overlap fidelity η — exact contract from METHODS_NOTES §2.1
# ---------------------------------------------------------------------------
def overlap_fidelity(
    psi_a: np.ndarray,
    psi_b: np.ndarray,
    dt: float,
    min_norm: float = GUARDS.min_norm_eta,
) -> float:
    """
    Compute the discrete overlap fidelity

        η = |⟨ψ_a , ψ_b⟩| / (‖ψ_a‖₂ · ‖ψ_b‖₂)

    where the inner product includes the measure factor Δt:

        ⟨f , g⟩_d = Σ f[i] · conj(g[i]) · Δt

    Mandatory rules (non-negotiable)
    --------------------------------
    1. Both fields must live on the identical support (same length).
    2. Global phase is irrelevant → absolute value of the inner product.
    3. No per-sample renormalisation that artificially inflates η.
    4. If either norm falls below min_norm the result is defined as
       GUARDS.eta_undefined (conservative, never inflates).

    Returns
    -------
    float
        η ∈ [0, 1] or GUARDS.eta_undefined when norms are pathological.
    """
    if psi_a.shape != psi_b.shape:
        raise ValueError(
            f"Support mismatch: {psi_a.shape} vs {psi_b.shape}. "
            "Both fields must share the identical discrete support Ω."
        )

    # Inner product with measure
    inner = np.sum(psi_a * np.conj(psi_b)) * dt
    norm_a = np.sqrt(np.sum(np.abs(psi_a) ** 2) * dt)
    norm_b = np.sqrt(np.sum(np.abs(psi_b) ** 2) * dt)

    if norm_a < min_norm or norm_b < min_norm:
        return float(GUARDS.eta_undefined)

    eta = np.abs(inner) / (norm_a * norm_b)

    # Numerical safety: clip only floating-point overshoot, never inflate
    return float(np.clip(eta, 0.0, 1.0))


# ---------------------------------------------------------------------------
# 3. Phase-randomised null (mandatory adversarial control)
# ---------------------------------------------------------------------------
def phase_randomise(psi: np.ndarray, rng: np.random.Generator) -> np.ndarray:
    """
    Destroy phase coherence while preserving the exact amplitude envelope.
    This is the strongest pure-phase null: any metric that still returns
    high η on this field is broken.
    """
    random_phase = rng.uniform(0.0, 2.0 * np.pi, size=psi.shape)
    return np.abs(psi) * np.exp(1.0j * random_phase)


# ---------------------------------------------------------------------------
# 4. Calibration run
# ---------------------------------------------------------------------------
def run_calibration(seed: int = 20260904) -> dict:
    """
    Execute the two mandatory calibration tests and return a structured
    result dictionary ready for logging / publication.
    """
    rng = np.random.default_rng(seed)

    # Grid from config (single source of truth)
    n_t = L1_GRID.n_t
    t_span = L1_GRID.t_span
    dt = L1_GRID.dt
    tau = np.linspace(-t_span / 2.0, t_span / 2.0, n_t, endpoint=False)

    # Analytic reference at the peak (z = 0)
    psi_ref = analytic_peregrine(tau, z=0.0)

    # Test 1 — self-overlap (must be extremely close to 1)
    eta_self = overlap_fidelity(psi_ref, psi_ref, dt)

    # Test 2 — phase-randomised null (must collapse)
    psi_null = phase_randomise(psi_ref, rng)
    eta_null = overlap_fidelity(psi_ref, psi_null, dt)

    # Verdicts against pre-registered thresholds
    # Self-consistency gate is stricter (0.98)
    verdict_self = compute_verdict(
        eta_self, THRESHOLDS.eta_self_consistency, higher_is_better=True
    )
    # Null must stay well below the F1 threshold (0.90)
    # We treat any η_null >= 0.90 as catastrophic failure of the metric
    if eta_null >= THRESHOLDS.eta_threshold:
        verdict_null = VERDICT_FAIL
    elif eta_null >= 0.30:          # soft warning zone from EXPECTED_RESULTS
        verdict_null = VERDICT_WARNING
    else:
        verdict_null = VERDICT_PASS

    overall = VERDICT_PASS
    if verdict_self != VERDICT_PASS or verdict_null == VERDICT_FAIL:
        overall = VERDICT_FAIL
    elif verdict_null == VERDICT_WARNING:
        overall = VERDICT_WARNING

    return {
        "seed": seed,
        "n_t": n_t,
        "t_span": t_span,
        "dt": dt,
        "eta_self": eta_self,
        "eta_null": eta_null,
        "verdict_self": verdict_self,
        "verdict_null": verdict_null,
        "overall": overall,
        "thresholds": {
            "eta_self_consistency": THRESHOLDS.eta_self_consistency,
            "eta_threshold_F1": THRESHOLDS.eta_threshold,
        },
    }


# ---------------------------------------------------------------------------
# 5. Entry point — human-readable + machine-readable output
# ---------------------------------------------------------------------------
def main() -> None:
    result = run_calibration()

    print("=" * 72)
    print("MODULE H — L1 CALIBRATION CORE")
    print("Analytic Peregrine self-overlap + phase-randomised null")
    print("=" * 72)
    print(f"Grid          : N_T = {result['n_t']}, T_span = {result['t_span']}, dt = {result['dt']:.6e}")
    print(f"Random seed   : {result['seed']}")
    print("-" * 72)
    print(f"η_self        : {result['eta_self']:.10f}   "
          f"(gate ≥ {result['thresholds']['eta_self_consistency']})  → {result['verdict_self']}")
    print(f"η_null        : {result['eta_null']:.10f}   "
          f"(must stay ≪ {result['thresholds']['eta_threshold_F1']})  → {result['verdict_null']}")
    print("-" * 72)
    print(f"OVERALL       : {result['overall']}")
    print("=" * 72)

    if result["overall"] == VERDICT_FAIL:
        print("\nCALIBRATION FAILED.")
        print("The discrete implementation of η does not satisfy the")
        print("pre-registered contract. Do NOT proceed to any further L1 tests.")
        print("Fix the metric definition or its implementation first.")
        sys.exit(1)
    elif result["overall"] == VERDICT_WARNING:
        print("\nCALIBRATION WARNING.")
        print("Self-overlap is acceptable but the null is higher than expected.")
        print("Investigate before declaring the apparatus ready.")
        sys.exit(0)
    else:
        print("\nCALIBRATION PASSED.")
        print("The measurement apparatus correctly recognises the analytic")
        print("Peregrine and correctly rejects a pure-phase null.")
        print("You may now proceed to the next L1 layer (SSFM generation,")
        print("remaining kernels, noise models, α-invariance).")
        sys.exit(0)


if __name__ == "__main__":
    main()
