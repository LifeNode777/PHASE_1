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
