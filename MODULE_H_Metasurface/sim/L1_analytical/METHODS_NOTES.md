# MODULE H — `sim/L1_analytical/METHODS_NOTES.md`
**Layer:** L1 — Analytical (metrics pipeline on synthetic signals)
**Status:** Pre-code epistemic grounding
**Last updated:** 2026-09-04

> This document exists before any executable code.
> It defines the continuous quantities, their discrete approximations,
> null models, generation procedures, and the α-invariance gate.
> Code that does not implement what is written here is noise.
---
## 1. Purpose of L1
L1 validates the **measurement apparatus** itself, not the metasurface geometry.
It answers: "Can the metrics η and G_coh correctly distinguish focusing
soliton kernels from noise and from defocusing dynamics on synthetic data?"
Only after L1 PASSes is L2 (2D geometry) allowed.
---
## 2. Continuous Definitions and Discrete Approximations
### 2.1 Overlap fidelity η ★/◇
**Continuous definition (target):**
η = |⟨ψ_out , ψ_ref⟩| / (‖ψ_out‖₂ · ‖ψ_ref‖₂)
⟨f , g⟩ = ∫_Ω f(x,t) · conj(g(x,t)) dx dt
η ∈ [0, 1]. η = 1 means perfect overlap. η = 0 means orthogonal.
**NOTE:** This is overlap (cosine similarity), NOT quantum fidelity |·⟩|².
For classical EM fields in FDTD, the un-squared form is the correct convention.
**Discrete approximation (implementation contract):**
⟨ψ_out , ψ_ref⟩_d = Σ ψ_out[i,j,k] · conj(ψ_ref[i,j,k]) · Δx · Δy · Δt
‖ψ‖₂,d = sqrt(⟨ψ , ψ⟩_d)
η_d = |⟨ψ_out , ψ_ref⟩_d| / (‖ψ_out‖₂,d · ‖ψ_ref‖₂,d)
**Mandatory rules (non-negotiable):**
1. Both fields restricted to the **same support Ω** (declared and frozen in `config.py`).
2. Global phase irrelevant → absolute value of the inner product.
3. No ad-hoc per-sample renormalization that artificially inflates η.
4. If a tapered window is used, the identical window is applied to both fields.
5. A minimum-norm threshold is defined in `config.py` to avoid division by near-zero.
Any other normalization (cosine similarity on flattened vectors without
measure factors, peak-only correlation, etc.) is a different metric and
must not be called η.
### 2.2 Coherent gain G_coh ★/◇
**Continuous definition:**
G_coh = 10 · log₁₀(P_signal / P_adversary)   [dB]
where P is power collected in the designated probe region (∫ |ψ|² dV dt).
**Discrete approximation:**
P_d = Σ |ψ[i,j,k]|² · Δx · Δy · Δt   (probe support only)
G_coh,d = 10 · log₁₀(P_signal,d / P_adversary,d)
Probe support must be identical for signal and adversary runs.
If P_adversary,d falls below a configurable floor, G_coh is reported as "> X dB".
**Critical rule:** Every selectivity run includes BOTH white Gaussian noise
AND colored 1/f^α (α ≈ 1, flicker regime) at matched bandwidth.
### 2.3 Cross-correlation matrix (S1–S5)
**Purpose:** Test distinguishability of the five kernels (F5).
**Definition:**
C[i,j] = η(ψ_i , ψ_j)   (same discrete definition as §2.1)
Result is a 5×5 Hermitian matrix with C_ii ≈ 1 and C_ij (i≠j) lower.
**Separation gate (to be frozen after first clean L1 runs):**
The exact numerical gate (e.g. max off-diagonal ≤ 0.XX) will be determined
from the first clean L1 runs and then locked in `config.py` and in
`EXPECTED_RESULTS.md`. Until that gate is set, F5 remains open.
---
## 3. Signal Generation
### 3.1 Peregrine breather (S2) — primary test kernel
**Equation (focusing NLSE):**
i ∂ψ/∂z = −½ ∂²ψ/∂τ² + κ |ψ|² ψ
with κ = −0.85 (focusing).
**Exact Peregrine solution (analytic ground truth):**
ψ_P(τ, z) = [1 − 4(1 + 2iz) / (1 + 4τ² + 4z²)] · exp(iz)
(or equivalent standard normalization). This analytic expression serves as
the ground-truth reference against which numerical generation is validated.
**Numerical generation method (L1 contract):**
1. Domain: sufficiently large temporal window with absorbing or periodic
boundaries so the breather is well isolated.
2. Scheme: Split-Step Fourier Method (SSFM) or equivalent symplectic /
unitarity-preserving integrator. Generic Runge–Kutta discouraged unless
proven to preserve L² norm to high accuracy.
3. Step-size control: halving the step must change η by ≪ 0.01.
4. Background level and peak amplitude fixed in `config.py` and never
adjusted post-hoc.
5. Numerically generated S2 must achieve **η ≥ 0.98** against the analytic
Peregrine before acceptance as a reference kernel.
**Defocusing control:** Exactly the same pipeline with κ = +0.85 (or any κ > 0).
This is a mandatory null.
### 3.2 Remaining kernels S1, S3, S4, S5
Definitions and generation procedures taken from LifeNode Theory v4 §4
and SPEC.md. Each kernel must pass a self-consistency check
(η against its own analytic or high-accuracy reference ≥ 0.98 where available).
### 3.3 Biological motifs K1 / K2 (Adamatzky-style)
Two mandatory variants:
1. **Clean deterministic** — ground truth for binary F1 threshold (η ≥ 0.90).
2. **Noisy diagnostic** — same motif + matched-bandwidth 1/f^α (α ≈ 1)
+ white noise, amplitudes within 0.1–1 mV DC range.
Results on noisy variant reported as WARNING only, never binary verdict.
### 3.4 Mandatory null / adversarial controls
| Null model | What it tests | Expected outcome |
|------------|---------------|------------------|
| Shuffled null | Phase-randomized S2 | η < 0.30 |
| White Gaussian noise | Uncorrelated broadband | η < 0.20, G_coh < 3 dB |
| Colored 1/f^α noise (α ≈ 1) | Flicker noise | η < 0.20, G_coh < 3 dB |
| Defocusing κ > 0 | Soliton cannot exist | η < 0.10, G_coh < 0 dB |
| Rössler zombie (recommended) | Deterministic chaos | η < 0.30, must NOT trigger F1 |
All nulls must stay well below η = 0.90 and G_coh = 10 dB.
A metric that cannot reject them is broken.
---
## 4. Time-Scaling Doctrine (α)
Biological envelopes (Macro-BPB ~32 min) and optical carriers differ by
many orders of magnitude. Simulation uses uniform time compression:
t_sim = t_bio / α
**Honest justification (non-exact symmetry, documented mechanism):**
1. Adiabatic carrier–envelope separation preserved.
2. Materials treated as locally non-dispersive within simulated bandwidth.
3. Mechanism tested, not literal biology.
### 4.1 α_L1 — bio-window compression (L1; no carrier simulated)
Maps biological time into the numerical window of the L1 grid
(config: N_T = 2048, T_SPAN = 32.0). The NLSE is solved in normalized units;
the optical carrier never appears at L1. α_L1 is therefore a pure window
mapping, and its justification is the window arithmetic itself.
### 4.2 α_CE — carrier–envelope compression (L2/L3; carrier at true frequency)
The optical carrier is simulated at its TRUE frequency (the spring and mass
of the resonator, BPB doctrine); only the envelope is compressed. α_CE is
**derived**, not chosen by taste:
α_CE = f_carrier / (f_bio · N_target),   N_target = 10⁶ (default)
so that each envelope period contains ~N_target optical cycles
(tractable band 10⁵–10⁸ for FDTD).
### 4.3 Default values (single source of truth: `config.py`)
| Quantity | Scenario | Value | Arithmetic justification |
|----------|----------|-------|--------------------------|
| α_L1 | Macro-BPB (K1/K2, 32 min) | 10³ | 1920 s / 10³ = 1.92 s window |
| α_L1 | Micro-BPB (1 Hz) | 1 | 1 s period fits the native window; no compression needed |
| α_CE | Macro-BPB | 10¹² | 5.635e14 Hz · 1920 s / 10¹² ≈ 1.08e6 optical cycles @ 532 nm |
| α_CE | Micro-BPB (1 Hz) | ≈ 5.6e8 | 5.635e14 / (1 · 10⁶) |
| pair | every verdict metric | (α, α/2) | mandatory invariance gate, 5% tolerance |
**α-invariance gate (mandatory):**
Every verdict metric (η, G_coh, key entries of the cross-correlation matrix)
is computed at α and at α/2 **of the same quantity** (α_L1 pair at L1;
α_CE pair at L2/L3). If |Δmetric| > 5%, the run is declared **INVALID**
(time-discretization artifact) and published as a negative diagnostic.
No parameter tuning allowed to rescue an invalid run.
Non-uniform compression (envelope compressed, carrier not, or vice versa)
invalidates the run outright.
---
## 5. Two-Loop Separation
- **Coupling loop** = pure field evolution / kernel generation (no digital feedback).
- **Diagnostic loop** = extraction of η, G_coh, cross-correlations, plots, saving.
- Diagnostics never feed back into the field.
---
## 6. Solver Choice and Justification
**Primary solver: Meep ≥ 1.27 (FDTD)**
Chosen because the φ-spiral (golden angle 137.5°) is aperiodic by construction.
RCWA and any Fourier-modal method assume strict spatial periodicity and
MUST NOT be used for the full spiral geometry. RCWA reserved exclusively
for periodic unit-cell characterization of individual meta-atoms.
**Floquet time-modulation:** Implemented via `mp.CustomMedium` with
user-defined ε(t). L2 modulation stability micro-test (blank plate, no spiral)
MUST pass before any L3 run.
---
## 7. Numerical Guards (must be present in code)
1. **Minimum-norm threshold** before computing η (avoid division by near-zero).
2. **Power floor** for G_coh (report "> X dB" if adversary below floor).
3. **Support check:** explicit assertion that signal and reference share
the same support and the same window function.
4. **α-invariance auto-execution:** α and α/2 pair computed automatically;
invariance failure aborts the verdict.
5. **Random seeds** for noise generators recorded and stored in run metadata.
---
## 8. Markers
- ★ = anchored in existing literature / standard definition
- ◇ = LifeNode-specific integrative hypothesis or threshold
Unresolved conflicts or open choices listed in Gaps section. Never silently closed.
---
## 9. Gaps / Open Decisions (to be closed before code freeze)
| Gap | Status | Impact |
|-----|--------|--------|
| Exact numerical separation gate for S1–S5 cross-correlation matrix | OPEN | F5 cannot pass until frozen |
| Final list and precise definitions of S1, S3, S4, S5 | OPEN (ref: SPEC.md) | L1 kernel generation incomplete |
| Concrete values of working α and α/2 pair | DEFINED (α_L1 = 10³, α_CE = 10¹²; validated by `config.py` import asserts) | L1 verdicts use the α_L1 pair; L2/L3 will pre-register the α_CE pair in their own contracts |
| Rössler zombie: recommended → mandatory? | OPEN | Null model completeness |
| Precise probe-support geometry for G_coh | OPEN | Focal region vs full domain |
| Choice of window function (if any) and parameters | OPEN | Affects η computation |
| LiNbO₃ modulation depth vs soliton fidelity budget | OPEN | ◇ engineering question |
---
*This is a map of the measurement apparatus.*
*The territory is the code that will implement it.*
*When the two conflict, the map is updated publicly — the code is never allowed to drift in silence.*
