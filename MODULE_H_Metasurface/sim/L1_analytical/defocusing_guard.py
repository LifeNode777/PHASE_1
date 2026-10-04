"""
MODULE H — sim/L1_analytical/defocusing_guard.py
Peak Suppression Guard for the defocusing null (kappa > 0).

Implements the contract frozen in config.py section 11
(DefocusingNullContract, amended 2026-10-04).
Thresholds read ONLY from DEFOCUSING_CONTRACT — no overrides (Rule 6).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from typing import List, Optional, Sequence

import numpy as np

# Makes "import config" work no matter which folder the script is run from.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import DEFOCUSING_CONTRACT, VERDICT_PASS, VERDICT_FAIL


@dataclass(frozen=True)
class PeakGuardResult:
    verdict: str
    peak_suppression_pass: bool
    background_stability_pass: bool
    E_max: float
    B_dev_max: float
    n_saved_z: int
    dz_saved: float
    z_coords: Optional[List[float]]
    epsilon_guard: float
    epsilon_b: float
    B: List[float] = field(default_factory=list)
    E: List[float] = field(default_factory=list)
    reason: str = ""


def peak_suppression_guard(
    psi_slices: Sequence[np.ndarray],
    z_coords: Optional[Sequence[float]] = None,
) -> PeakGuardResult:
    """
    Guard logic, verbatim from config.py section 11:
        B(z) = median over tau of |psi(tau, z)|
        E(z) = max over tau of |psi(tau, z)| / B(z) - 1
        PASS iff  max E(z) <= epsilon_guard  AND  max |B(z) - 1| <= epsilon_b
    """
    if len(psi_slices) == 0:
        raise ValueError("psi_slices is empty — cannot evaluate guard")
    if z_coords is not None and len(z_coords) != len(psi_slices):
        raise ValueError("len(z_coords) != len(psi_slices)")

    eps_g = DEFOCUSING_CONTRACT.epsilon_guard
    eps_b = DEFOCUSING_CONTRACT.epsilon_b

    n_saved_z = len(psi_slices)
    if z_coords is not None and n_saved_z > 1:
        dz_saved = float(np.mean(np.diff(np.asarray(z_coords, dtype=float))))
    else:
        dz_saved = 0.0

    B_list: List[float] = []
    E_list: List[float] = []

    for psi in psi_slices:
        psi = np.asarray(psi)
        if psi.ndim != 1:
            raise ValueError(f"Each slice must be 1-D; got shape {psi.shape}")
        amp = np.abs(psi)
        B = float(np.median(amp))
        if B <= 0.0:
            B_list.append(0.0)
            E_list.append(float("inf"))
            continue
        peak = float(np.max(amp))
        B_list.append(B)
        E_list.append(peak / B - 1.0)

    E_max = float(np.max(E_list))
    B_dev_max = float(np.max(np.abs(np.asarray(B_list) - 1.0)))

    peak_pass = bool(E_max <= eps_g)
    bg_pass = bool(B_dev_max <= eps_b)
    verdict = VERDICT_PASS if (peak_pass and bg_pass) else VERDICT_FAIL

    if verdict == VERDICT_PASS:
        reason = (f"E_max={E_max:.6f} <= eps_guard={eps_g} and "
                  f"|B-1|_max={B_dev_max:.6f} <= eps_b={eps_b}")
    else:
        parts = []
        if not peak_pass:
            parts.append(f"E_max={E_max:.6f} > eps_guard={eps_g}")
        if not bg_pass:
            parts.append(f"|B-1|_max={B_dev_max:.6f} > eps_b={eps_b}")
        reason = "; ".join(parts)

    return PeakGuardResult(
        verdict=verdict,
        peak_suppression_pass=peak_pass,
        background_stability_pass=bg_pass,
        E_max=E_max,
        B_dev_max=B_dev_max,
        n_saved_z=n_saved_z,
        dz_saved=dz_saved,
        z_coords=list(z_coords) if z_coords is not None else None,
        epsilon_guard=eps_g,
        epsilon_b=eps_b,
        B=B_list,
        E=E_list,
        reason=reason,
      )
