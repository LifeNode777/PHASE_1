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
