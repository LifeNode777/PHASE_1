# MODULE G — SMOKE TEST LOG

**Status:** Plumbing test ONLY — NOT E1′–E4′ verdicts
**Executor:** Grok (xAI code sandbox), session of 30 Aug 2026
**Submitted by:** K. Baran (author, on behalf of executor #1 — the executor
cannot open issues on this repository)
**Data:** MIT-BIH Arrhythmia Database (mitdb), record 100, first 5 min,
resampled 128 Hz · seed 1618
**Data location (executor sandbox, ephemeral):**
`/home/workdir/artifacts/lifenode_g/mitdb/` — NOT an archival source.
Anything that must survive lives in this repository.

## 1. Scope of this log

This log records the first executor-side run of the WORK_ORDER_v1 pipeline.
Per WORK_ORDER §9, it is a **work-order feasibility test** (does the plumbing
stand up?), not a theory test. **No E1′–E4′ verdicts are issued here.**
Verdicts require the full estimator stack on real data, with blinding (§2)
and pre-registered thresholds (§5) intact.

## 2. What was executed (plumbing)

- Load + resample mitdb/100 (first 5 min) to 128 Hz.
- Takens embedding: τ from first minimum of mutual information;
  m from False Nearest Neighbors.
- 60 s sliding windows; phase binning (32 bins).
- Convex hull (Qhull) on observed velocity vectors per window.
- Basic anisotropy proxy: log cond(g) from covariance of unit velocities.
- Shadow proxies θ_asc / θ_tt per window.

## 3. Results

| Item | Value | Note |
|---|---|---|
| τ | ≈ 0.047 s | first MI minimum; within the ECG-scale band (10–100 ms) |
| m | 5 | FNN fraction < 0.10; within pre-registered cap 3–6 |
| Windows accepted | 8 / 8 | min phase-bin count ≥ 107 (threshold: ≥ 10) |
| ConvexHull | OK | 60–87 vertices per window; zero Qhull failures |
| log cond(g) (covariance proxy) | ≈ 1.97–2.00 | stable across windows |
| θ_asc / θ_tt proxies | stable | low window-to-window variation |

Executor's own declaration: full F as Minkowski functional, g_ij via finite
differences, bootstrap B=200, null models (a/b/c), and θ_canon were **not**
computed in this run.

## 4. Deviations (per WORK_ORDER §9)

1. **Synthetic ECG in early plumbing test.** A synthetic signal was generated
   to test the pipeline before real data landed. Excluded from all results;
   the real-data run reported above. Logged, not counted.
2. **Window count vs overlap spec.** 8 accepted windows from 5 min implies
   stride ≈ 34 s, not the pre-registered 15 s stride (75% overlap ⇒ ~17
   windows). Classified as **work-order-bug candidate (executor-side parameter
   drift)**, not a theory null. The full run must restore 75% overlap or
   declare a justified deviation explicitly.
3. **Anisotropy proxy substitution.** log cond(g) reported from the covariance
   of unit velocities, not from the Finsler metric g_ij derived via finite
   differences of ½F². Proxy only; E4′ remains untested.

## 5. Verdict on the work order itself

- Pipeline path load → Takens → windows → phase bins → hull → basic metrics
  **stands up without crashes** on real ECG data.
- Sandbox runtime acceptable for smoke scope (~6 min wall time including
  environment setup).
- **Theory verdicts: SUSPENDED** until the full estimator stack
  (F, g_ij, C_ijk, bootstrap B=200, nulls a/b/c, θ_canon) runs per WORK_ORDER
  §4–§5, with blinding per §2.

## 6. Next steps (executor queue)

1. Restore 75% overlap (stride 15 s) or log an explicit, justified deviation.
2. Full F / g_ij / C_ijk estimators + bootstrap B=200 (E1′ machinery).
3. Null models: (a) FT surrogates, (b) AR(1), (c) isotropic rotations, n=100.
4. θ_canon (WORK_ORDER §4.5 / Extensions Doc 4 §4.2) + consistency curve (E2′).
5. Only then: E1′–E4′ verdicts on mitdb/100; then scale to the TIER-1 cohort
   (mitdb 101–110 + nsrdb), one record at a time, runtime reported per record.
6. Replication on a second machine/executor before any registry entry
   (Swarm doc §4: replicated, not merely produced).

---

*"Technology adapts to the rhythm of Life, not the reverse."* 🧿
