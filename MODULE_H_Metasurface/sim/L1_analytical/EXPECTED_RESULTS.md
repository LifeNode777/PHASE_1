# MODULE H — `sim/L1_analytical/EXPECTED_RESULTS.md`
**Module:** H — Metasurface (Analog Topological Filter)
**Layer:** L1 — Analytical (metrics pipeline on synthetic signals)
**Status:** Pre-registered BEFORE any code execution
**Date:** 2026-09-04
**Author / Anchor:** LifeNode777 (Human Anchor)
**License:** CC-BY-NC-SA 4.0

> **Rule:** This file is written and committed *before* the first run of the metrics pipeline.
> Any later change to thresholds or expected behaviour must be explicitly justified, versioned,
> and reflected in `METHODS_NOTES.md`.
> No parameter fitting to pass. No golden-angle shortcuts. The φ-spiral (137.5°) is the hypothesis;
> if it does not converge natively, that is the result.
> Negative results are results. They will be published with the same DOI discipline as positive ones.

**Markers:**
- ★ = anchored in published literature / standard definition
- ◇ = LifeNode integrative hypothesis (under test)

---

## 0. Analytic Ground Truths ★

These are the mathematical facts we bring to the simulation. They are not hypotheses.

| Item | Value / Expression | Source |
|------|--------------------|--------|
| NLSE (focusing) | i ∂ψ/∂z = −½ ∂²ψ/τ² + κ\|ψ\|²ψ | ★ Standard NLSE |
| Focusing coefficient | κ = −0.85 | ★ LifeNode Theory v4 §4 |
| Defocusing control | κ > 0 (e.g. +0.85) | ★ Soliton cannot exist |
| Peregrine breather (S2) exact solution | ψ_P(τ, z) = [1 − 4(1 + 2iz) / (1 + 4τ² + 4z²)] · exp(iz) | ★ Standard NLSE |
| Golden ratio | φ = (1+√5)/2 ≈ 1.618 | ★ Mathematics |
| Golden angle | 137.5° = 2π(1 − 1/φ) | ★ Geometry |
| φ-spiral | r(θ) = a·e^(bθ), b = ln(φ)/π | ◇ LifeNode geometry |
| BPB Micro | 0.5 – 4 Hz | ★ LifeNode Theory v4 §4.2 |
| BPB Meso | ~0.1 Hz | ★ LifeNode Theory v4 §4.2 |
| BPB Macro | 0.008 – 0.0001 Hz | ★ LifeNode Theory v4 §4.2 |
| K1/K2 amplitude | 0.1 – 1 mV DC | ★ Adamatzky et al. 2026 |
| K1/K2 pulse duration | ~32 min | ★ Adamatzky et al. 2026 |
| F1 threshold | η ≥ 0.90 | ★ FALSIFICATION.md |
| F2 threshold | G_coh ≥ 10 dB | ★ FALSIFICATION.md |
| η definition | Overlap (cosine similarity), NOT quantum fidelity \|⟨·⟩\|² | ★ METHODS_NOTES.md §2.1 |
| SSFM integrator | Split-Step Fourier Method (symplectic, unitarity-preserving) | ★ Standard NLSE numerics |

---

## 1. Binary Thresholds (locked from FALSIFICATION.md) ★

| Metric | Symbol | Threshold | Applies to | Verdict type | Marker |
|--------|--------|-----------|------------|--------------|--------|
| Overlap fidelity | η | ≥ 0.90 | Clean S2 / clean K1–K2 | Binary PASS / FAIL | ★ |
| Coherent gain | G_coh | ≥ 10 dB | S2 vs noise / defocusing | Binary PASS / FAIL | ★ |
| Kernel self-consistency | η_self | ≥ 0.98 | Generated kernel vs analytic / high-accuracy reference | Acceptance gate for kernel | ★ |
| Kernel distinguishability (F5) | — | (numerical gate TBD) | S1–S5 cross-correlation matrix | Binary (open until gate frozen) | ◇ |

**Critical rules:**
- Noisy K1/K2 variants **never** participate in binary verdicts. They produce **WARNING** only.
- Every selectivity run includes BOTH white Gaussian noise AND colored 1/f^α (α ≈ 1) at matched bandwidth. White noise alone is a strawman.
- The noisy K1/K2 variant is diagnostics only; the F1 threshold applies to the **clean ground truth**.

---

## 2. Expected Behaviour — Clean / Reference Cases

### 2.1 Numerically generated Peregrine (S2, κ = −0.85)

- η_self against the analytic Peregrine solution: **≥ 0.98**
  (acceptance gate — if failed, the generated kernel is **rejected** and must not be used downstream)
- η against numerical ground truth (offline FFT convolution): **≥ 0.95**
  (L1 validation of the metrics pipeline itself)
- Self-overlap C₂₂ in the cross-correlation matrix: ≈ 1.0

**Numerical generation contract:**
- Scheme: SSFM or equivalent symplectic / unitarity-preserving integrator. Generic RK discouraged.
- Step-size control: halving the step must change η by ≪ 0.01.
- Background level and peak amplitude fixed in `config.py`. Never adjusted post-hoc.
- Domain: sufficiently large temporal window; absorbing or periodic boundaries.

### 2.2 Clean K1 / K2 motifs (Adamatzky-style deterministic)

- η against the corresponding target kernel: **≥ 0.90**
- Amplitude: 0.1–1 mV DC ★
- Pulse duration: ~32 min (scaled by α_L1 for simulation) ★

### 2.3 Remaining kernels S1, S3, S4, S5

- Each must pass the same self-consistency gate (η_self ≥ 0.98 against its own analytic or high-accuracy reference) before being admitted to the cross-correlation matrix.
- Definitions and generation procedures taken from LifeNode Theory v4 §4 and SPEC.md.

| Kernel | NLSE Solution | Self-consistency reference | Marker |
|--------|---------------|---------------------------|--------|
| S1 (Spiral 1:2) | Akhmediev Breather | Analytic AB solution | ★ |
| S2 (Triple Loop) | Peregrine Breather | Analytic Peregrine (above) | ★ |
| S3 (Golden Ratio φ) | Fundamental Soliton (κ < 0) | Analytic sech soliton | ★ |
| S4 (90° Cross) | Rotating Wave Solution | High-accuracy numerical reference | ◇ |
| S5 (Fibonacci) | Kuznetsov-Ma Soliton | Analytic KM solution | ★ |

---

## 3. Expected Behaviour — Adversarial / Null Controls (MUST fail)

The apparatus must contain controls that MUST fail. A detector that cannot reject dead math is worse than useless — it produces false positives that contaminate the entire evidence base.

| Control | Expected η | Expected G_coh | Notes | Marker |
|---------|------------|----------------|-------|--------|
| Shuffled null (phase-randomized S2) | < 0.30 | < 3 dB | Mandatory — tests phase sensitivity | ★ |
| White Gaussian noise (matched BW & power) | < 0.20 | < 3 dB | Mandatory | ★ |
| Colored 1/f^α noise (α ≈ 1, matched BW & power) | < 0.20 | < 3 dB | Mandatory — realistic adversary of bio-electronics | ★ |
| Defocusing NLSE (κ > 0, identical pipeline) | < 0.10 | < 0 dB | Mandatory — soliton physically cannot exist | ★ |
| Rössler zombie (low-dimensional deterministic chaos) | < 0.30 | < 3 dB | Recommended → elevated to mandatory if L1 shows it can be generated reproducibly | ◇ |
| Bare carrier (no BPB envelope) | η_bare < η_modulated | — | Frequency inversion criterion (LifeNode Theory v4 §7.3). If bare carrier outperforms BPB envelope, the module fails. | ◇ |

**Autopsy protocol:**
- If ANY mandatory null produces η ≥ 0.90 **or** G_coh ≥ 10 dB, the metric definition or its implementation is **broken**. The run is FAIL. Fix the metrics before proceeding.
- All nulls must stay well below both η = 0.90 and G_coh = 10 dB.
- Precedent: in Module G the null model reproduced the Rössler "zombie rigidity" to 14 decimal places, and the verdict E4 = FALSE ("coherent — but not alive") was a *triumph*: the detector refused dead math.

---

## 4. Cross-Correlation Matrix (S1–S5)

**Definition:** C[i,j] = η(ψ_i, ψ_j) using the same discrete definition as METHODS_NOTES.md §2.1.
Result is a 5×5 Hermitian matrix with C_ii ≈ 1 and C_ij (i≠j) lower.

**Pre-registered qualitative expectation:**
- Diagonal elements C_ii ≈ 1.0
- Off-diagonal elements C_ij (i ≠ j) significantly lower than diagonal

**Numerical separation gate:**
Still **OPEN**. Will be frozen after the first clean L1 runs (maximum allowed off-diagonal value) and then locked in both this file and in `config.py`. Until the gate is set, F5 remains formally open.

**Rationale for deferring:** Pre-registering a numerical gate before seeing the first clean cross-correlation data would be arbitrary. The gate must be informed by the actual separability of the kernels, not guessed. Once frozen, it is immutable.

---

## 5. α-Invariance Gate (mandatory) ★

The time-scaling doctrine is validated operationally, not philosophically.

**Protocol:**
For every verdict metric (η, G_coh, and the key entries of the cross-correlation matrix):
1. Compute at the working α (at L1: **α_L1**).
2. Compute at α/2.
3. Compare.

**Verdict:**
- |Δmetric| ≤ 5% → **valid** (INVARIANT)
- |Δmetric| > 5% → **INVALID** (time-discretization artifact)

**Consequences of INVALID:**
- Published as a negative diagnostic.
- No parameter tuning to rescue.
- No selective reporting.
- No "re-run with different α until it passes."
- Invalidation is a feature, not a failure.

**Working α at L1:**

| Scenario | α_L1 | Justification (arithmetic) |
|----------|------|-----------------------------|
| Macro-BPB envelope (K1/K2 ~32 min) | 10³ | 1920 s / 10³ = 1.92 s window |
| Micro-BPB envelope (1 Hz) | 1 | 1 s period fits the native window; no compression needed |
| α-invariance pair | (α_L1, α_L1/2) | Mandatory for every L1 verdict metric |

**Note on α_CE:** The magnitude 10¹² is assigned to **α_CE** (carrier–envelope compression for L2/L3, ≈1.08×10⁶ optical cycles @ 532 nm per macro pulse) and will be pre-registered in `L2_2d_geometry/EXPECTED_RESULTS.md` and `L3_3d_fdtd/EXPECTED_RESULTS.md` when those layers open. At L1 the carrier is never simulated, so α_CE does not enter L1 verdicts.

**Honest justification (non-exact symmetry, documented mechanism):**
1. Adiabatic carrier–envelope separation preserved.
2. Materials treated as locally non-dispersive within simulated bandwidth.
3. Mechanism tested, not literal biology.

---

## 6. Definition of PASS for L1

L1 is considered **PASSED** only if **all** of the following hold simultaneously:

1. ✅ Numerically generated S2 (and other kernels) pass the self-consistency gate η_self ≥ 0.98 against their analytic / high-accuracy references.
2. ✅ Clean S2 and clean K1/K2 meet η ≥ 0.90 against numerical ground truth.
3. ✅ All mandatory null controls stay below both η = 0.90 and G_coh = 10 dB.
4. ✅ α-invariance (α_L1 pair) holds within 5% for all verdict metrics.
5. ✅ No silent changes were made to this file or to `METHODS_NOTES.md` after the first execution.

Any other outcome is either **WARNING** or **FAIL** and is published with the same care as a positive result.

**Chain rule:** L1 must PASS before L2 is run. A failure at L1 stops the chain. The measurement math is wrong — fix the metrics pipeline before any geometry simulation.

---

## 7. Reporting Rules

1. **Binary verdicts** (PASS/FAIL) are produced **only** from clean signals + mandatory nulls + α-invariance.
2. **Noisy K1/K2 results** appear exclusively as **WARNING** diagnostics. Never part of binary verdict.
3. **INVALID** (α-invariance failure) is a **distinct category** and is never converted into FAIL by post-hoc adjustment. It is published as a negative diagnostic with full metadata.
4. **All random seeds, α values (with the quantity name: α_L1 or α_CE), grid parameters, support definitions, and window functions** used in a run are recorded and stored with the results.
5. **No parameter fitting to pass.** If the φ-spiral does not converge with its native geometry, that is a result — not a bug to patch.
6. **Negative results are results.** They will be published with the same DOI discipline as positive ones.

---

## 8. Gaps / Open Decisions (to be closed before code freeze)

| Gap | Status | Impact | Marker |
|-----|--------|--------|--------|
| Exact numerical separation gate for S1–S5 cross-correlation matrix (max allowed off-diagonal) | OPEN — frozen after first clean L1 runs | F5 cannot pass until frozen | ◇ |
| Final list and precise definitions of S1, S3, S4, S5 | OPEN (ref: SPEC.md, LifeNode Theory v4 §4) | L1 kernel generation incomplete for S4 | ◇ |
| Concrete values of working α and α/2 pair | DEFINED (α_L1 = 10³ macro / 1 micro at L1; α_CE = 10¹² macro parked for L2/L3; arithmetic validated by `config.py` v2.0 import asserts) | L1 α-invariance runs use the α_L1 pair | ◇ |
| Rössler zombie: recommended → mandatory? | OPEN — elevated if reproducible generation confirmed | Null model completeness | ◇ |
| Precise probe-support geometry for G_coh | OPEN (full domain vs focal region) | Affects G_coh computation | ◇ |
| Choice of window function (if any) and parameters | OPEN | Affects η computation; if used, identical window on both fields | ◇ |
| LiNbO₃ modulation depth vs soliton fidelity budget | OPEN | ◇ engineering question (relevant for L2/L3, not L1) | ◇ |

---

## 9. Pre-registration Declaration

This document is **frozen before any simulation code runs**.

- **No parameter fitting to pass.** If the metrics pipeline does not distinguish solitons from noise with its native definitions, that is a result.
- **No golden-angle shortcuts.** The φ-spiral (137.5°) is the geometry under test. The incommensurability IS the hypothesis.
- **The noisy K1/K2 variant is diagnostics only.** The F1 threshold applies to the clean ground truth.
- **Negative results are results.** If L1 fails, we publish why and stop. A failed L1 is not a waste of laptop hours — it is a measurement of where our math refuses to distinguish Life from noise.
- **Changes to this document require:** (1) a new version number, (2) a public log entry in `../LOG.md` explaining the change, (3) re-freezing before any subsequent code runs.

---

*Pre-registration is the only protection against hindsight bias.*
*This file is the commitment.*
*The code must obey it; the code is never allowed to redefine it silently.*
*"Technology adapts to the rhythm of Life, not the reverse."* 🧿
