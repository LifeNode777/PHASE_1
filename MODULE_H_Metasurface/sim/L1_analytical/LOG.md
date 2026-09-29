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
