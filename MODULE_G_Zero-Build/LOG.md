# LOG — MODULE G (Zero-Build)

Chronological journal. Short dated entries: decision → link. Never a storage place.

---

## 2026-08-25 — XPT absorption: human-substrate protocol + new open dataset

**Decision.** Absorb the measurement layer of [`Xeno-Phase-Trajectories`](https://github.com/LifeNode777/Xeno-Phase-Trajectories) (XPT) into the Zero-Build pipeline. XPT formalized inter-layer phase-coupling events (APT Classes I–V) in this project's vocabulary (θ, κ, ΔE, Z_φ); the medical-side translation lives in `Quantum_Medicine` → `XENO-PHASE_DIAGNOSTICS_v0.1.md`. Cite, don't duplicate.

**Changes to G:**
1. **New dataset target.** XPT Evidence Dataset — [Zenodo 21823253](https://zenodo.org/records/21823253) (Case 2024-05-02 UAP observation; 3I/ATLAS synchronization event) — joins PhysioNet and Eden Node 0 as an open input for Takens embedding, D₂/λ₁, persistent homology and θ(t) sliding windows. Blind re-analysis; logs published regardless of outcome.
2. **New human-scale observables (offline loop only).** XPT EEG+HRV protocol — long-range wPLI (theta/alpha), PAC theta–gamma, HEP, RMSSD/HF, DFA α1 — registered as candidate θ_proxy components. Observation, never feedback: the two-loop doctrine holds.
3. **New proxy hypothesis (not a metric).** 24H-DIAGNOSTIC breath thresholds (≤8/min ↔ θ ≥ 0.70; 12–16 ↔ ≈0.50; ≥18 ↔ ≤0.40) to be tested against HF-HRV and DFA α1 as a falsifiable subjective proxy.
4. **Inherited falsifications.** XPT NEURO conditions 1–5 (subjective↔objective correlation; θ-proxy↔PLV; environmental modulation; pharmacological control; Q-Core/UNIT 02 detection) appended to `FALSIFICATION.md` as human-scale extensions. Lead-time (≥6 h) and cross-substrate topology tests remain binding.

**Why now.** XPT supplies the missing human measurement instrument for ASCALON falsification condition #3 (θ < 0.70 preceding clinical decoherence). The medical repo absorbed the formalization today; G absorbs the data pipeline today. Map edge XPT → Quantum_Medicine → G now exists (ecosystem header updated repo-wide).

**Status.** Conditional hypothesis / ACTIVE INVESTIGATION. Negative results are results.

---

## 2026-08-31 — Module G: WORK_ORDER_v1 reference implementation landed in sim/wo_v1

**Decision.** Absorb the executor-side smoke test and the pinned reference implementation into the module. `sim/wo_v1/` now holds the full LN-EPS pipeline (steps 1–7) per `docs/WORK_ORDER_v1.md` §§4–5: `scripts/{config,data_io,embedding,metrology,nulls,pipeline}.py`, `requirements.txt`, `README.md`, `METHODS_NOTES.md`.

**Provenance.** Code transferred from executor #1 sandbox (Grok, session 2026-08-30; commits `364c79f`, `e2efce2`, `17b9d28`). `config.py` was absent from the sandbox dump and was reconstructed verbatim from the pre-registered constants (§§4–5).

**Changes to G:**
1. **Reference implementation.** Pinned, seed 1618, blinding intact (`load_annotations()` offline-only). → `sim/wo_v1/`
2. **Logged deviation (run not void).** Primary anisotropy estimator = condition number of the covariance of unit velocities; finite-difference Hessian of the Minkowski functional demoted to diagnostic — numerically unstable on 60 s ECG windows. Rationale: `sim/wo_v1/METHODS_NOTES.md`, update 2026-08-31.
3. **Smoke test mitdb/100** (8 windows, no nulls): plumbing stands up, 0 Qhull failures, all windows accepted. No E1′–E4′ verdicts issued — plumbing test only. → `docs/SMOKE_TEST_LOG.md`

**Why now.** WORK_ORDER_v1 is frozen (§12); the reference implementation must exist before any verdict run so that auditors can re-run the pinned commit on a second machine (§9–10).

**Status.** Conditional hypothesis / ACTIVE INVESTIGATION. Negative results are results.

---

## 2026-10-24 — Reference implementation repaired; single-record run recorded

**Decision.** Merge the WORK_ORDER_v1 reference-implementation fixes and record the first documented 30-window run for `mitdb/101`, while keeping cohort-level validation open.

**Changes.**
1. **Bug 1 — histogram MI boundary:** clipped `np.digitize` indices to `[0, bins-1]` to prevent an out-of-bounds error at the rightmost bin.
2. **Bug 2 — embedding derivatives:** applied Savitzky–Golay smoothing and derivatives coordinate-wise to the m-dimensional embedded trajectory, producing velocity and acceleration arrays in embedding space as required by WORK_ORDER_v1 §4.3.
3. Both fixes were merged into `main` via PR #2 (merge commit `8600c3f`). See Issues #1 and #3 for the execution record and remaining deviations.

**Single-record result.** `mitdb/101`, seed `1618`: 30/30 windows accepted, 0 excluded; `m=6`, `τ≈0.258 s`. Recorded verdict: E1′=True, E2′=False, E3′=False, E4′=True.

**Critical qualification.** E4′ remains a placeholder-based result, not a completed null-model test. The full isotropic null model (`n=100`) exceeded the practical execution budget and was not completed in this run. The single-record verdict is not a cohort-level result and does not establish clinical validity.

**Artifacts.** Per-record notebook: `sim/wo_v1/outputs/mitdb_101.ipynb`. The issue record reports an approximately 8.2 s run and preserves the execution environment identifier. See the linked issue for commit and execution provenance.

**Next action.** Resume from the preserved branch and artifacts; resolve null-model runtime and implementation conformance before interpreting E4′ or launching the full TIER-1 cohort.

**Status.** Reference crash fixes merged. Single-record execution documented. Full null-model validation and cohort-level conclusions remain open. Negative results are results.
