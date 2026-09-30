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
