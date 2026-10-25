```python
#!/usr/bin/env python3
"""
MODULE H — L1 Analytical
gate1_runner.py  (Gate 1 instrument: SSFM S2 + Peak Suppression Guard)
Purpose
-------
Close the execution block recorded in LOG.md on 2026-10-04:
    Wire the Gate 1 runner: SSFM focusing (κ = −0.85) and defocusing
    (κ = +0.85), identical pipeline, saved slices with recorded
    n_saved_z / Δz_saved; evaluate the defocusing branch via
    peak_suppression_guard(); log the rerun with full provenance.
This file is measurement apparatus, not a soliton generator for downstream
use. A bug here is a calibration error of the instrument (ASYMMETRY_NOTE §1.1).
What this run is allowed to decide
-----------------------------------
- Focusing branch: η_self of the numerical field at z = 0 against the
  exact contract solution. Gate = THRESHOLDS.eta_self_consistency (0.98).
- Defocusing branch: Peak Suppression Guard ONLY (config.py §11).
  η on that branch is a diagnostic. It is not a verdict.
- Step-size: halving dz must change the focusing η by < 0.01
  (METHODS_NOTES §3.1 operational reading of "≪ 0.01").
- Integrator health: max relative L² drift along the trajectory.
  Reported. Pathological drift (> 1e-8) fails the run as apparatus
  failure, not as a soliton result. 1e-8 is an apparatus floor,
  not a theory threshold.
What this run deliberately does not do
---------------------------------------
- α-invariance. Next layer. Not smuggled into this verdict.
- F5 cross-correlation. Gate remains OPEN.
- K1/K2, noise, G_coh. Out of scope.
- No post-hoc fitting (Rule 6). No rescaling of ψ to lift η or to
  push the defocusing background onto 1. No threshold overrides.
Equation (METHODS_NOTES §3.1, EXPECTED_RESULTS §0) ★
----------------------------------------------------
    i ∂ψ/∂z = −½ ∂²ψ/∂τ² + κ |ψ|² ψ
    κ_focus   = −NOISE.defocusing_kappa     # −0.85, from config
    κ_defocus = +NOISE.defocusing_kappa     # +0.85, sign flip only
Split-step (Strang), symmetric:
    half-step linear  →  full-step nonlinear  →  half-step linear
Linear symbol, ω = 2π · fftfreq(N, d=Δτ):
    L(Δz) = exp(−i · ω²/2 · Δz)
Nonlinear symbol:
    N(Δz) = exp(−i · κ · |ψ|² · Δz)
The linear sign and the factor 1/2 are the contract. A propagator with
the opposite sign, or with ω²/4, solves a different PDE and is a failed
instrument even if η comes out high by accident.
Reference field ★ / ◇
---------------------
`analytic_peregrine` is exact at kappa = −1, where it is the formula
frozen in METHODS_NOTES / EXPECTED_RESULTS:
    ψ_P = [1 − 4(1 + 2iz) / (1 + 4τ² + 4z²)] exp(iz)
That formula solves the contract equation at κ = −1 only.
For κ < 0 the amplitude-only map
    ψ = analytic_peregrine(τ, z, kappa=−1) / sqrt(|κ|)
is the exact solution (background |κ|^{−1/2}, peak three times that).
Passing κ = −0.85 INTO analytic_peregrine is not used: that code path
scales (τ, z, amplitude) together and solves the equation with nonlinear
coefficient |κ|², not |κ|. Measured residual of that path against the
contract equation is O(1), not roundoff. Using it as the ruler would
make a correct solver look false. The map above calls the library only
at its exact point (kappa = −1) and applies the standard normalisation.
It is not a second Peregrine implementation and it is not a fit.
This runner does not edit config.py, the guard, METHODS or EXPECTED.
It calls the Peak Suppression Guard already in the repo (config §11,
amended 2026-10-04): max |B(z) − 1| ≤ ε_B. On that contract the
sandbox run of this file was OVERALL FAIL: focusing passed, no spike,
background failed because the κ = −0.85 solution sits near 1.085, not 1.
That is a result about the written reference "1", not a license to
change thresholds inside this file.
Propagation domain vs calibration grid
---------------------------------------
LOG 2026-10-04: L1_GRID (N_T = 2048, T_span = 32) is the metric
calibration window. The 2026-09-30 Gate 1 propagation domain was
T_span = 160.  are different roles and must not be merged.
This runner states its own propagation grid below and records
L1_GRID alongside it. z_start = −8 is the 2026-09-30 propagation
start, not a value tuned on this run.
Author: LifeNode Research Collective (synthesized instrument; Human Anchor commits)
License: CC-BY-NC-SA 4.0
Status: Gate 1 rerun instrument — written against config §11 amendment 2026-10-04
"""
from __future__ import annotations
import json
import platform
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Sequence
import numpy as np
# ---------------------------------------------------------------------------
# Single source of truth. Fail hard. No hardcoded thresholds below.
# ---------------------------------------------------------------------------
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parent))
try:
    from config import (
        L1_GRID,
        NOISE,
        THRESHOLDS,
        GUARDS,
        DEFOCUSING_CONTRACT,
        VERDICT_PASS,
        VERDICT_FAIL,
        VERDICT_WARNING,
        compute_verdict,
    )
    from Peregrine_metrics import analytic_peregrine, overlap_fidelity
    from defocusing_guard import peak_suppression_guard
except ImportError as e:
    raise SystemExit(
        "FATAL: cannot import config.py / Peregrine_metrics.py / defocusing_guard.py.\n"
        "Place this file in sim/L1_analytical/ and run it from anywhere.\n"
        f"Original error: {e}"
    )
# ---------------------------------------------------------------------------
# Propagation contract for THIS rerun.
# Not theory thresholds. Not fitted. Cited from LOG 2026-09-30 / 2026-10-04.
# One place, so a reader can see every numerical choice the PDE did not fix.
# ---------------------------------------------------------------------------
Z_START: float = -8.0          # LOG 2026-09-30 propagation start
Z_END: float = 0.0             # Peregrine focus of the contract solution
T_SPAN_PROP: float = 160.0     # LOG 2026-09-30 propagation window, NOT L1_GRID.t_span
N_T_PROP: int = 8192           # 2^k. dt = 160/8192 ≈ 0.0195. Stated, not fitted.
DZ: float = 0.002              # base step. Halved once inside the run for the η check.
DZ_SAVE: float = 0.05          # target cadence of saved slices (guard sees only these)
SEED: int = 20261025           # recorded. The PDE step uses no RNG.
# Apparatus floor for L² drift. Not a soliton threshold. Above this the
# integrator is not the contract PDE and the soliton verdict is void.
MAX_REL_DRIFT: float = 1e-8
# METHODS §3.1: "halving the step must change η by ≪ 0.01".
# Operational ceiling used here: |Δη| < 0.01. The measured Δη is reported.
STEP_HALVING_ETA_MAX: float = 0.01
# Reference self-check. If the closed form does not solve the contract
# equation on this grid, refuse to score anything.
REFERENCE_RESIDUAL_MAX: float = 1e-2
@dataclass
class BranchRecord:
    kappa: float
    n_steps: int
    dz: float
    n_saved_z: int
    dz_saved: float
    eta_vs_contract_focus: float
    eta_role: str
    norm_p0: float
    norm_drift_rel_max: float
    norm_drift_abs_max: float
    E_max: float
    B_dev_max: float
    guard_verdict: str
    guard_reason: str
    guard_is_binary: bool
@dataclass
class Gate1Result:
    overall: str
    exit_code: int
    focusing_verdict: str
    defocusing_verdict: str
    step_halving_verdict: str
    integrator_verdict: str
    eta_focus: float
    eta_focus_halved: float
    delta_eta_halving: float
    eta_focus_repeat: float
    eta_defocus_diagnostic: float
    reference_residual: float
    reason: str
    provenance: dict
    focusing: BranchRecord
    defocusing: BranchRecord
    gaps: List[str] = field(default_factory=list)
def contract_peregrine(tau: np.ndarray, z: float, kappa: float) -> np.ndarray:
    """Exact focusing solution of the contract NLSE at this kappa.
    Uses analytic_peregrine only at kappa = −1 (the frozen formula) and the
    amplitude-only normalisation ψ/√|κ|. See module docstring.
    """
    if not np.isfinite(kappa) or kappa >= 0.0:
        raise ValueError(
            f"contract_peregrine is the focusing solution; got kappa={kappa}"
        )
    return analytic_peregrine(tau, z, kappa=-1.0) / np.sqrt(-kappa)
def _grid():
    if N_T_PROP <= 0 or (N_T_PROP & (N_T_PROP - 1)) != 0:
        raise SystemExit(f"N_T_PROP={N_T_PROP} must be a power of two (SSFM/FFT).")
    dt = T_SPAN_PROP / N_T_PROP
    tau = np.linspace(-T_SPAN_PROP / 2.0, T_SPAN_PROP / 2.0, N_T_PROP, endpoint=False)
    omega = 2.0 * np.pi * np.fft.fftfreq(N_T_PROP, d=dt)
    return tau, dt, omega
def reference_residual(tau: np.ndarray, omega: np.ndarray, kappa: float, z: float = 0.0) -> float:
    """Relative PDE residual of contract_peregrine on this grid.
    i ψ_z  ?=?  −½ ψ_ττ + κ |ψ|² ψ
    Spectral τ-derivative, central z-difference. Apparatus check only.
    """
    dz = 1e-4
    def field(zz: float) -> np.ndarray:
        return contract_peregrine(tau, zz, kappa)
    psi = field(z)
    psi_z = (field(z + dz) - field(z - dz)) / (2.0 * dz)
    psi_tt = np.fft.ifft((-(omega ** 2)) * np.fft.fft(psi))
    lhs = 1j * psi_z
    rhs = -0.5 * psi_tt + kappa * (np.abs(psi) ** 2) * psi
    denom = np.linalg.norm(rhs)
    if denom == 0.0:
        return float("inf")
    return float(np.linalg.norm(lhs - rhs) / denom)
def propagate(
    psi0: np.ndarray,
    kappa: float,
    omega: np.ndarray,
    dt: float,
    z_start: float,
    z_end: float,
    dz: float,
    save_every: int,
):
    """Strang SSFM. Diagnostics do not feed back into ψ.
    Returns the final field, saved slices (including z_start), z coords,
    the dz that actually landed on z_end, step count, and L² drift.
    """
    n_steps = int(round((z_end - z_start) / dz))
    if n_steps < 1:
        raise ValueError(f"n_steps={n_steps} from dz={dz}, span={z_end - z_start}")
    dz_used = (z_end - z_start) / n_steps
    half = np.exp(-0.5j * (omega ** 2) * (dz_used / 2.0))
    psi = np.array(psi0, dtype=np.complex128, copy=True)
    p0 = float(np.sum(np.abs(psi) ** 2) * dt)
    if p0 <= 0.0:
        raise RuntimeError("Initial L² power is non-positive. Instrument abort.")
    max_abs = 0.0
    max_rel = 0.0
    slices: List[np.ndarray] = [psi.copy()]
    z_coords: List[float] = [z_start]
    for step in range(1, n_steps + 1):
        psi = np.fft.ifft(half * np.fft.fft(psi))
        psi = psi * np.exp(-1j * kappa * (np.abs(psi) ** 2) * dz_used)
        psi = np.fft.ifft(half * np.fft.fft(psi))
        p = float(np.sum(np.abs(psi) ** 2) * dt)
        max_abs = max(max_abs, abs(p - p0))
        max_rel = max(max_rel, abs(p - p0) / p0)
        if save_every > 0 and (step % save_every == 0 or step == n_steps):
            slices.append(psi.copy())
            z_coords.append(z_start + step * dz_used)
    return psi, slices, z_coords, dz_used, n_steps, max_rel, max_abs, p0
def _dz_saved(z_coords: Sequence[float]) -> float:
    if len(z_coords) < 2:
        return 0.0
    return float(np.mean(np.diff(np.asarray(z_coords, dtype=float))))
def _score_branch(
    psi_final: np.ndarray,
    slices: Sequence[np.ndarray],
    z_coords: Sequence[float],
    kappa: float,
    n_steps: int,
    dz_used: float,
    max_rel: float,
    max_abs: float,
    p0: float,
    ref_focus: np.ndarray,
    dt: float,
    guard_is_binary: bool,
) -> BranchRecord:
    eta = overlap_fidelity(psi_final, ref_focus, dt, min_norm=GUARDS.min_norm_eta)
    guard = peak_suppression_guard(slices, z_coords)
    return BranchRecord(
        kappa=float(kappa),
        n_steps=int(n_steps),
        dz=float(dz_used),
        n_saved_z=int(guard.n_saved_z),
        dz_saved=float(guard.dz_saved),
        eta_vs_contract_focus=float(eta),
        eta_role=("acceptance gate" if not guard_is_binary else "diagnostic only — not a verdict"),
        norm_p0=float(p0),
        norm_drift_rel_max=float(max_rel),
        norm_drift_abs_max=float(max_abs),
        E_max=float(guard.E_max),
        B_dev_max=float(guard.B_dev_max),
        guard_verdict=str(guard.verdict),
        guard_reason=str(guard.reason),
        guard_is_binary=bool(guard_is_binary),
    )
def run_gate1() -> Gate1Result:
    kappa_focus = -float(NOISE.defocusing_kappa)
    kappa_defocus = +float(NOISE.defocusing_kappa)
    if kappa_focus >= 0.0 or kappa_defocus <= 0.0:
        raise SystemExit(
            f"Sign error in κ pair: focus={kappa_focus}, defocus={kappa_defocus}. "
            "Refusing to run."
        )
    tau, dt, omega = _grid()
    resid = reference_residual(tau, omega, kappa_focus, z=0.0)
    if resid > REFERENCE_RESIDUAL_MAX:
        raise SystemExit(
            "FATAL: contract reference does not solve the contract NLSE "
            f"on this grid (relative residual {resid:.3e} > {REFERENCE_RESIDUAL_MAX}). "
            "No verdict emitted. Fix the ruler before scoring the solver."
        )
    ic = contract_peregrine(tau, Z_START, kappa_focus)
    ref = contract_peregrine(tau, Z_END, kappa_focus)
    save_every = max(1, int(round(DZ_SAVE / DZ)))
    psi_f, slices_f, z_f, dz_f, n_f, rel_f, abs_f, p0_f = propagate(
        ic, kappa_focus, omega, dt, Z_START, Z_END, DZ, save_every
    )
    # Deterministic repeat. Same dz, same IC. No RNG in the step, so this
    # must come back identical up to roundoff. A miss here is an instrument fault.
    psi_rep, _, _, _, _, _, _, _ = propagate(
        ic, kappa_focus, omega, dt, Z_START, Z_END, DZ, save_every=0
    )
    eta_repeat = overlap_fidelity(psi_f, psi_rep, dt, min_norm=GUARDS.min_norm_eta)
    # Step halving. Same IC, same κ, dz → dz/2. Criterion is the change in η.
    save_every_half = max(1, int(round(DZ_SAVE / (DZ / 2.0))))
    psi_h, _, _, dz_h, n_h, rel_h, _, _ = propagate(
        ic, kappa_focus, omega, dt, Z_START, Z_END, DZ / 2.0, save_every_half
    )
    focusing = _score_branch(
        psi_f, slices_f, z_f, kappa_focus, n_f, dz_f, rel_f, abs_f, p0_f,
        ref, dt, guard_is_binary=False,
    )
    eta_half = overlap_fidelity(psi_h, ref, dt, min_norm=GUARDS.min_norm_eta)
    delta_eta = abs(focusing.eta_vs_contract_focus - eta_half)
    psi_d, slices_d, z_d, dz_d, n_d, rel_d, abs_d, p0_d = propagate(
        ic, kappa_defocus, omega, dt, Z_START, Z_END, DZ, save_every
    )
    defocusing = _score_branch(
        psi_d, slices_d, z_d, kappa_defocus, n_d, dz_d, rel_d, abs_d, p0_d,
        ref, dt, guard_is_binary=True,
    )
    focusing_verdict = compute_verdict(
        focusing.eta_vs_contract_focus,
        THRESHOLDS.eta_self_consistency,
        higher_is_better=True,
    )
    step_ok = delta_eta < STEP_HALVING_ETA_MAX
    step_verdict = VERDICT_PASS if step_ok else "FAIL_STEP_HALVING"
    integ_ok = (
        focusing.norm_drift_rel_max <= MAX_REL_DRIFT
        and defocusing.norm_drift_rel_max <= MAX_REL_DRIFT
        and eta_repeat >= 1.0 - 1e-12
    )
    integ_verdict = VERDICT_PASS if integ_ok else "FAIL_INTEGRATOR"
    defocus_verdict = defocusing.guard_verdict  # binary, from the guard only
    gaps = [
        "analytic_peregrine(kappa≠−1) implements a similarity whose nonlinear "
        "coefficient is |κ|², not |κ|. This runner does not call that path. "
        "The κ=−1 formula in the library is the ruler; amplitude normalisation "
        "ψ/√|κ| is the contract solution.",
        "The repo guard still scores |B-1|, not distance from the launched floor. "
        "This file does not reimplement or amend that test.",
        "α-invariance is not applied to this verdict (next layer).",
        "F5 remains OPEN. Noisy K1/K2 excluded. G_coh not computed.",
        "L1_GRID is the calibration window and is not the propagation window. "
        f"Calibration N_T={L1_GRID.n_t}, T_span={L1_GRID.t_span}. "
        f"Propagation N_T={N_T_PROP}, T_span={T_SPAN_PROP}.",
    ]
    reasons = []
    if not integ_ok:
        reasons.append(
            f"integrator not the contract PDE: rel drift focus={focusing.norm_drift_rel_max:.3e} "
            f"defocus={defocusing.norm_drift_rel_max:.3e} (floor {MAX_REL_DRIFT:.1e}), "
            f"repeat η={eta_repeat:.16f}"
        )
    if not step_ok:
        reasons.append(
            f"|Δη| on step halving = {delta_eta:.6e} ≥ {STEP_HALVING_ETA_MAX} "
            f"(η(dz={dz_f})={focusing.eta_vs_contract_focus:.8f}, "
            f"η(dz={dz_h})={eta_half:.8f}, steps {n_f} vs {n_h})"
        )
    if focusing_verdict != VERDICT_PASS:
        reasons.append(
            f"focusing η={focusing.eta_vs_contract_focus:.8f} → {focusing_verdict} "
            f"against gate {THRESHOLDS.eta_self_consistency}"
        )
    if defocus_verdict != VERDICT_PASS:
        reasons.append(f"defocusing Peak Guard {defocus_verdict}: {defocusing.guard_reason}")
    # Apparatus failure voids the soliton verdict. Report it as its own overall.
    if not integ_ok or not step_ok:
        overall = "INVALID_STEP_OR_INTEGRATOR"
        exit_code = 2
    elif focusing_verdict == VERDICT_PASS and defocus_verdict == VERDICT_PASS:
        overall = VERDICT_PASS
        exit_code = 0
        reasons.append(
            f"focusing η={focusing.eta_vs_contract_focus:.8f} ≥ {THRESHOLDS.eta_self_consistency}; "
            f"defocusing guard PASS ({defocusing.guard_reason}); "
            f"|Δη|_halving={delta_eta:.3e}"
        )
    elif focusing_verdict == VERDICT_WARNING and defocus_verdict == VERDICT_PASS:
        overall = VERDICT_WARNING
        exit_code = 0
    else:
        overall = VERDICT_FAIL
        exit_code = 1
    provenance = {
        "seed": SEED,
        "seed_used_by_step": False,
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
        "equation": "i dpsi/dz = -0.5 d²psi/dtau² + kappa |psi|² psi",
        "splitting": "Strang L/2, N, L/2",
        "linear_operator": "exp(-i * omega**2 / 2 * dz/2), omega = 2*pi*fftfreq",
        "nonlinear_operator": "exp(-i * kappa * |psi|**2 * dz)",
        "reference": "analytic_peregrine(tau, z, kappa=-1) / sqrt(|kappa_focus|)",
        "kappa_focus": kappa_focus,
        "kappa_defocus": kappa_defocus,
        "kappa_source": "sign(NOISE.defocusing_kappa) from config.py; magnitude not hardcoded",
        "n_t": N_T_PROP,
        "t_span": T_SPAN_PROP,
        "dt": dt,
        "z_start": Z_START,
        "z_end": Z_END,
        "dz": dz_f,
        "dz_halved": dz_h,
        "n_steps": n_f,
        "n_steps_halved": n_h,
        "n_saved_z_focus": focusing.n_saved_z,
        "n_saved_z_defocus": defocusing.n_saved_z,
        "dz_saved_focus": focusing.dz_saved,
        "dz_saved_defocus": defocusing.dz_saved,
        "calibration_grid_not_used_for_propagation": {
            "n_t": int(L1_GRID.n_t),
            "t_span": float(L1_GRID.t_span),
            "dt": float(L1_GRID.dt),
        },
        "thresholds_from_config": {
            "eta_self_consistency": float(THRESHOLDS.eta_self_consistency),
            "epsilon_guard": float(DEFOCUSING_CONTRACT.epsilon_guard),
            "epsilon_b": float(DEFOCUSING_CONTRACT.epsilon_b),
            "warning_zone_pct": float(THRESHOLDS.warning_zone_pct),
            "min_norm_eta": float(GUARDS.min_norm_eta),
        },
        "rule_6_no_post_hoc_fit": True,
        "raw_slices_written": False,
    }
    return Gate1Result(
        overall=overall,
        exit_code=exit_code,
        focusing_verdict=focusing_verdict,
        defocusing_verdict=defocus_verdict,
        step_halving_verdict=step_verdict,
        integrator_verdict=integ_verdict,
        eta_focus=focusing.eta_vs_contract_focus,
        eta_focus_halved=float(eta_half),
        delta_eta_halving=float(delta_eta),
        eta_focus_repeat=float(eta_repeat),
        eta_defocus_diagnostic=defocusing.eta_vs_contract_focus,
        reference_residual=float(resid),
        reason="; ".join(reasons) if reasons else "no failing clause",
        provenance=provenance,
        focusing=focusing,
        defocusing=defocusing,
        gaps=gaps,
    )
def _human_report(result: Gate1Result) -> str:
    p = result.provenance
    f = result.focusing
    d = result.defocusing
    lines = [
        "MODULE H — Gate 1 rerun (SSFM S2 + Peak Suppression Guard)",
        f"OVERALL: {result.overall}  (exit {result.exit_code})",
        "",
        "Provenance",
        f"  time (UTC)     {p['timestamp_utc']}",
        f"  python / numpy {p['python']} / {p['numpy']}",
        f"  platform       {p['platform']}",
        f"  seed           {p['seed']} (not consumed by the step; repeat η = {result.eta_focus_repeat:.16f})",
        f"  grid           N_T={p['n_t']}  T_span={p['t_span']}  Δτ={p['dt']:.8f}",
        f"  calibration    N_T={p['calibration_grid_not_used_for_propagation']['n_t']}  "
        f"T_span={p['calibration_grid_not_used_for_propagation']['t_span']}  (not used to propagate)",
        f"  z              [{p['z_start']}, {p['z_end']}]  dz={p['dz']:.6f}  n_steps={p['n_steps']}",
        f"  κ              focus {p['kappa_focus']}   defocus {p['kappa_defocus']}   source: {p['kappa_source']}",
        f"  slices         n_saved_z focus/defocus {p['n_saved_z_focus']}/{p['n_saved_z_defocus']}"
        f"   Δz_saved {p['dz_saved_focus']:.6f}/{p['dz_saved_defocus']:.6f}",
        f"  reference      {p['reference']}",
        f"  ref residual   {result.reference_residual:.3e} (relative, contract PDE at z=0)",
        "",
        "Focusing  (binary = η_self, guard numbers are diagnostic only)",
        f"  η_self         {f.eta_vs_contract_focus:.10f}  → {result.focusing_verdict}"
        f"   gate ≥ {p['thresholds_from_config']['eta_self_consistency']}",
        f"  η halved dz    {result.eta_focus_halved:.10f}   |Δη| = {result.delta_eta_halving:.3e}"
        f"  → {result.step_halving_verdict}",
        f"  L² drift       rel {f.norm_drift_rel_max:.3e}   abs {f.norm_drift_abs_max:.3e}"
        f"  → integrator {result.integrator_verdict}",
        f"  E_max          {f.E_max:.6f}   |B−1|_max {f.B_dev_max:.6f}"
        f"   (not scored; focusing peak excess of the contract solution is 2)",
        "",
        "Defocusing  (binary = Peak Suppression Guard only; η is not a verdict)",
        f"  guard          {d.guard_verdict}   {d.guard_reason}",
        f"  ε              guard {p['thresholds_from_config']['epsilon_guard']}   "
        f"B {p['thresholds_from_config']['epsilon_b']}",
        f"  η diagnostic   {d.eta_vs_contract_focus:.10f}   vs focusing contract solution at z=0",
        f"  L² drift       rel {d.norm_drift_rel_max:.3e}   abs {d.norm_drift_abs_max:.3e}",
        f"  n_saved_z      {d.n_saved_z}   Δz_saved {d.dz_saved:.6f}",
        "",
        "Reason",
        f"  {result.reason}",
        "",
        "Gaps (not resolved in this file)",
    ]
    for g in result.gaps:
        lines.append(f"  - {g}")
    lines += [
        "",
        "LOG draft (do not commit until the Human Anchor accepts the artifact):",
        f"  Gate 1 rerun overall {result.overall}.",
        f"  Focusing κ={p['kappa_focus']}: η_self={f.eta_vs_contract_focus:.10f} ({result.focusing_verdict}), "
        f"|Δη| halving={result.delta_eta_halving:.3e} ({result.step_halving_verdict}), "
        f"rel L² drift={f.norm_drift_rel_max:.3e}.",
        f"  Defocusing κ={p['kappa_defocus']}: Peak Guard {d.guard_verdict} "
        f"(E_max={d.E_max:.6f}, |B−1|_max={d.B_dev_max:.6f}, "
        f"n_saved_z={d.n_saved_z}, Δz_saved={d.dz_saved:.6f}). "
        f"η diagnostic={d.eta_vs_contract_focus:.6f}, not used as a verdict.",
        f"  Grid N_T={p['n_t']}, T_span={p['t_span']}, z:[{p['z_start']},{p['z_end']}], dz={p['dz']}.",
        "  No threshold edited. No field rescaled. F5 still OPEN.",
        "",
    ]
    return "\n".join(lines)
def main() -> None:
    result = run_gate1()
    report = _human_report(result)
    print(report)
    out_dir = Path.cwd() / "gate1_results"
    out_dir.mkdir(exist_ok=True)
    stamp = result.provenance["timestamp_utc"].replace(":", "").replace("-", "")
    json_path = out_dir / f"gate1_run_{stamp}.json"
    txt_path = out_dir / f"gate1_run_{stamp}.txt"
    payload = asdict(result)
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    txt_path.write_text(report, encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {txt_path}")
    print("Raw slices were not written (heavy fields stay out of the repo).")
    raise SystemExit(result.exit_code)
if __name__ == "__main__":
    main()
```
