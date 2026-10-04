2026-09-29
L1 calibration core committed.
Decision (Human Anchor):
The first executable artifact of Module H is the pure calibration of the overlap fidelity η.
Scope of this step:
- Exact analytic Peregrine solution (S2) evaluated against itself.
- Same field with pure phase randomisation (mandatory null).
- η implemented strictly according to METHODS_NOTES.md §2.1 (identical support, measure factor Δt, absolute value of inner product, min_norm guard).
- All thresholds and guards taken exclusively from config.py.
- No SSFM, no remaining kernels, no noise models, no K1/K2, no G_coh, no α-invariance on real signals.
Rationale:
The measurement apparatus itself must be validated before any physics layer is added. If the discrete implementation of η cannot recognise the analytic ground truth and reject a pure-phase null, every subsequent result is meaningless.
Status:
peregrine_metrics.py placed in sim/L1_analytical/.
F5 gate remains OPEN.
Noisy K1/K2 variants remain excluded from binary verdicts.
No parameter fitting permitted.
Next gate:
Only after this calibration returns PASS may the pipeline proceed to SSFM generation and the remaining L1 layers.

---

2026-09-29 — L1 analytical calibration execution
Runner: executed in AI sandbox (ChatGPT) — AI leg as executor, human anchor: LifeNode777
Environment: Python 3.13.5, numpy 2.3.5, seed 20260904.
Source provenance: sandbox had no DNS access to raw.githubusercontent.com; no `git clone` was performed. The sources of `Peregrine_metrics.py` and `config.py` were verified against the current GitHub main content at run time and transcribed into the sandbox; this run is reproducible in code and parameters but is not a byte-verified clone execution.
Verdict: OVERALL `PASS`
- `η_self = 1.0000000000` → `PASS` (self-consistency gate ≥ 0.98)
- `η_null = 0.0102088868` → `PASS`; the pure-phase null is rejected by the metric
Determinism check: `η_null = 0.0102088868` in this run; this matches an earlier same-day sandbox run of the same seed, not a pre-registered value — only the thresholds (0.98 / 0.90 / 0.30) are pre-registered.
Provenance / gate annotations
- All calibration thresholds and guards are sourced exclusively from `sim/config.py`.
- F5 gate remains OPEN; this PASS does not freeze F5 cross-correlation thresholds.
- Next gate unchanged: proceed to SSFM generation and the remaining L1 layers.
- `EXPECTED_RESULTS.md` and `METHODS_NOTES.md` are frozen pre-registration documents and were not modified.
Reference execution artifacts
- `L1_calibration_run_2026-09-29.json` (machine-readable result dictionary)
- `L1_calibration_ENV_STDOUT_2026-09-29.txt` (verbatim environment + STDOUT)

---

2026-09-30 — L1 SSFM S2 Generation & Defocusing Null Diagnostic Failure
Runner: executed in AI sandbox — AI leg as executor, human anchor: LifeNode777

Execution summary:
- Gate 0 (η calibration via Peregrine_metrics.py): remains PASS.
- Gate 1 (SSFM S2 self-consistency, focusing κ = -0.85): PASS. 
  η_self = 0.9999989765 (meets η ≥ 0.98 gate). Step-size convergence, norm drift, and background stability all PASS.
- Defocusing null (current implementation): FAILS pre-registered contract.

Diagnostic / Root Cause:
The defocusing null definition in METHODS_NOTES.md §3.1 / §3.4 and EXPECTED_RESULTS.md §3 is physically inconsistent with the overlap fidelity metric defined in §2.1.
- Spec requires: "Exactly the same pipeline with κ = +0.85" and expects η < 0.10.
- Physics/Math reality: The analytic Peregrine at z_start (-8.0) is 99% flat background (amplitude ~1.0). Propagating this with κ = +0.85 simply maintains the flat background (no soliton forms). Comparing this flat output to the analytic focusing Peregrine at z=0 (which also sits on a flat background of amplitude 1.0 across T_span=160) yields a high overlap (η ≈ 0.95) because the metric integrates the identical backgrounds over the entire domain. 
- The test as written measures background similarity, not the absence of a localized soliton peak. 

Decision (Human Anchor):
Stop pipeline. Do not proceed to S1/S3-S5 or K1/K2. 
The SSFM solver is mathematically sound for the focusing case, but the measurement apparatus cannot reject the defocusing null under its own pre-registered rules because the rules conflate background overlap with peak formation.
No parameter adjustment, distance stretching, or threshold tuning was performed in the code to force a PASS (Rule 6: No parameter fitting to pass). Negative diagnostic recorded.

Next gate / Required Action:
The map must be updated publicly. 
METHODS_NOTES.md §3.4 and EXPECTED_RESULTS.md §3 require a versioned amendment to redefine the defocusing null acceptance criterion. 
Proposed fix for the docs: The null must explicitly check for the absence of a localized peak (e.g., max(|ψ|) remains near 1.0) rather than relying solely on global η dropping below 0.10 at short propagation distances.
Once docs are amended, code will be updated to match, and Gate 1 will be re-run.

---

2026-10-04 — L1 Metric Statistical Characterization (TEST-01/02) & Defocusing Null Contract Amendment
Runner: executed in AI sandbox — AI leg as executor, human anchor: LifeNode777

Execution summary:
To resolve the Defocusing Null failure (documented 2026-09-30) without violating Rule 6 (no parameter
fitting to pass), the overlap-fidelity metric η was characterized beyond the single preregistered
null realization. Full records: TEST-01 / TEST-02 characterization artifacts.

- TEST-01 (Phase-Randomized Null Characterization): 10,000 independent phase-randomized
  realizations at the current configured L1 calibration resolution (N_T=2048, T_span=32).
  - mean η_null ≈ 0.026 | median ≈ 0.025 | p95 ≈ 0.051 | p99 ≈ 0.063 | max ≈ 0.090.
  - All realizations well below the preregistered null boundary η_null < 0.30.
  - Resolution sweep: null overlap depends systematically on discretization (lower N_T → higher
    null overlap); T_span sweep shows a similar, weaker dependence.
- TEST-02 (Controlled Phase-Mismatch Calibration): ψ'(τ) = ψ(τ)·exp(i·δφ(τ)) sweep on the
  analytical S2 reference, 500 realizations per level, same resolution.
  - Mean η decreases monotonically: 1.000 (δ=0) → ≈0.882 (0.5) → ≈0.607 (1.0) → ≈0.326 (1.5)
    → ≈0.135 (2.0) → ≈0.049 (2.5).
  - Response points: η < 0.90 at δ ≈ 0.5; η < 0.70 at δ ≈ 0.9; η < 0.30 at δ ≈ 1.6.

Resolution provenance note (to prevent future misreading):
TEST-01/02 characterize η at the resolution currently frozen in config.py (N_T=2048, T_span=32.0,
verified 2026-10-04). The 2026-09-30 Gate 1 record cites the then-configured propagation domain
(T_span=160). These are distinct roles (metric calibration domain vs propagation domain) and
distinct values; they are not a contradiction and must not be silently merged. The Gate 1 rerun
must state its resolution explicitly and be interpreted at that resolution.

Diagnostic / Synthesis (resolving the 2026-09-30 block):
TEST-02 establishes η as a phase-sensitive global overlap metric: it responds monotonically to
phase-structure mismatch. The Sept 30 defocusing branch (κ=+0.85) preserved the flat CW background
(|ψ| ≈ 1.0) over the then-configured domain (T_span=160); compared against the analytic focusing
reference at z=0 — which also sits on the same unit background across the full support — the global
inner product is dominated by the identical backgrounds, yielding η ≈ 0.95. The original contract
(METHODS_NOTES §3.4 / EXPECTED_RESULTS §3) therefore asked a global background-sensitive integral to
certify the absence of a localized peak: a category error in the specification, not a solver defect.
η is blind to peak absence by construction; it was never the right instrument for that question.

Decision (Human Anchor):
1. The L1 metric calibration/characterization phase is CLOSED. Within the tested calibration
   domain, η behaves as a phase-sensitive global overlap metric with a strongly separated
   random-phase null. This is not a claim of full validation: SSFM, noise handling, G_coh,
   α-invariance and other supports remain unvalidated.
2. The conceptual block from 2026-09-30 is resolved at the specification level. Gate 1 remains
   BLOCKED in execution until the amended Defocusing Null contract is implemented and re-run.
3. Defocusing Null contract amendment (versioned change to METHODS_NOTES.md §3.4 and
   EXPECTED_RESULTS.md §3):
   - Primary criterion: Peak Suppression Guard — explicit test for absence of localized structure
     (definition below).
   - η is retained for the defocusing branch as a reported diagnostic only; the global η < 0.10
     acceptance criterion is withdrawn as physically inconsistent.
4. Pre-registration rule for the guard: functional form and thresholds are frozen in config.py
   BEFORE the Gate 1 rerun. No post-hoc adjustment (Rule 6).

Peak Suppression Guard — preregistration candidate (to be frozen in config.py pre-rerun):
- Background estimate per saved slice: B(z) = median_τ |ψ(τ, z)|  (robust: background dominates
  the support).
- Peak excess: E(z) = max_τ |ψ(τ, z)| / B(z) − 1, evaluated on every saved slice over
  z ∈ [z_start, 0] (trajectory-wide, to catch transient peak formation).
- Guard PASS iff max_z E(z) ≤ ε_guard, proposed ε_guard = 0.10.
- Companion background check: |B(z) − 1| ≤ ε_B for all saved z, proposed ε_B = 0.05 (rejects
  background blow-up or damping masquerading as a clean null).
- Threshold rationale (pre-rerun, not fitted to the defocusing result): ε_guard = 0.10 is defined
  as a 10% peak-excess ceiling relative to the local background, adopted a priori. The 2026-09-30
  convergence, norm-drift and background-stability checks established that numerical deviations are
  substantially smaller than this scale; their exact recorded values will be preserved with the
  rerun provenance. The focusing Peregrine reference has peak excess 2.0 over background
  (|ψ|_peak = 3·B), providing a large separation between the null guard and the target structure.
  Once frozen, ε_guard must not be revised on the grounds that Gate 1 fails.
- Slice-sampling caveat: the guard is evaluated on saved slices only; sufficiency of the saving
  cadence is not asserted here. The rerun provenance must record n_saved_z and Δz_saved so that
  the question "could a peak have formed between saved points?" is answerable from the record.

Next gate:
Commit the amended contract; freeze ε_guard / ε_B and the rerun resolution in config.py; implement
the guard; re-run Gate 1 (focusing + defocusing) at the stated resolution, recording n_saved_z and
Δz_saved in the provenance.

---

