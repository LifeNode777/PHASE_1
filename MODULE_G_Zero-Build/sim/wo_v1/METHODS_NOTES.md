# METHODS_NOTES.md — MODULE G WORK_ORDER_v1

Any deviation from the pre-registered text voids the run. Record deviations here.

## Implementation notes (reference code)

1. **Mutual information estimator**  
   Histogram MI (64 bins) with fallback to first ACF minimum. Continuous MI via sklearn was considered but histogram matches the work-order wording more closely.

2. **Finsler cosine in θ_canon**  
   Uses Euclidean inner product after normalisation by F(v)·F(R). Full g-inner product at every sample is computationally heavier; the Euclidean proxy is the leading term and is documented here as an implementation choice. If this is judged material, a work-order-bug / v2 clarification is required.

3. **Null models**  
   Isotropic renormalisation (null c) is the primary envelope used for E4′. FT and AR(1) are implemented but not required for the binary decision.

4. **Window mapping**  
   Embedding length is shorter than the original signal by (m−1)·τ. Windows are clipped conservatively to the embedding array.

5. **Bootstrap**  
   B = 200 resamples of the velocity cloud; windows with < 10 successful hulls receive NaN CI and are treated as failing the E1′ CI criterion.

6. **Runtime**  
   Full TIER-1 (18 nsrdb + 10 mitdb) with nulls is expected to take several laptop-hours. Use `--max-windows` for development smoke tests.

7. **SG edge effects (Bug 2 fix)**  
   Savitzky–Golay (window 41, poly 3) applied independently to each coordinate of the embedded trajectory. Edge samples use the default SciPy boundary handling (no extra padding). Accepted as implementation note; no alternative (reflect/constant) was chosen silently.

## Deviations log

| Date       | Executor                          | Description                                                                 | Status      |
|------------|-----------------------------------|-----------------------------------------------------------------------------|-------------|
| 2026-09-17 | @Grok (session 2026-09-17, 7ba7cd84b6d12c5b) | Bug 1: np.digitize OOB on right edge → clip indices to [0, bins-1] in _histogram_mi | fixed       |
| 2026-09-17 | @Grok (session 2026-09-17, 7ba7cd84b6d12c5b) | Bug 2: SG derivatives applied to 1-D raw signal instead of m-dim embedded trajectory (per §4.3 text). Fixed: SG per coordinate of emb_seg; v,a now shape (N', m) | fixed       |

## Update 2026-08-31 — numerical stability of cond(g)

The finite-difference Hessian of the Minkowski functional on 60 s ECG windows produced extreme condition numbers (capped at 1e6).  
**Operational decision:** the primary reported `cond_g` and anisotropy index are now the condition number of the sample covariance of unit velocities.  
Qhull hull construction and F evaluation remain active for θ_canon and for the origin-interior acceptance test.  
This estimator change is recorded here so that any later auditor can reproduce the exact numerical path. A future WORK_ORDER_v2 may restore a regularised Finsler Hessian if desired.

## Update 2026-09-18 — G-v2 RC1 candidate, open drift, disclosures, credit ledger (append-only)

Continuation of the Deviations log (same columns; append-only edit, phone-safe).

| Date       | Executor | Description | Status |
|------------|----------|-------------|--------|
| 2026-09-18 | @LifeNode777 (maintainer) | Leg mitdb/101 (2026-09-17, executor @Grok, machine_sha 7ba7cd84b6d12c5b): max_windows=30 cap applied; full isotropic nulls n=100 deferred (sandbox timeout); E4 reported as reference placeholder (median_log_cond > 1.0), not a null-envelope verdict. | disclosed; pending nulls leg |
| 2026-09-18 | @LifeNode777 (maintainer) | E1' second conjunct (overlap of record-halves' median-cond 95% CIs, §5) is stubbed `e1_overlap = True` in the reference pipeline (v1 and G-v2 copy). All E1 verdicts to date rest on the CI-half-width conjunct only. | open; close in nulls leg (implement overlap) or re-label E1 |
| 2026-09-18 | @ChatGPT (constructor; RC1 self-test) | 6D provenance drift found during RC1 self-test before handoff: harness reproduces 2D+p-sweep and convergence goldens to 1e-6, but 6D FAILs: A calculated 1.116029 vs golden 1.118495; B calculated 2.935498 vs golden 2.934295. Goldens frozen; do NOT adjust. Runner probes: (a) directions seed 1618 vs 20260918; (b) direction draw before/after cloud RNG consumption; (c) legacy single-direction-per-rep convention; (d) direction normalisation order. | open; drift investigation assigned to next runner |
| 2026-09-18 | @Qwen (auditor) | Audit of 2026-09-18 on the G-v2 candidate targeted a stale transfer snapshot lacking smooth_finsler_metric / bootstrap_finsler_cond_g wrappers; superseded by RC1 manifest hash below once TEST ZERO passes on the runner. | closed-by-hash, pending runner TEST ZERO |

### Credit ledger (doctrine §2: participation is defined by work)
- Constructor, G-v2 smooth Finsler candidate + RC1 transfer package: @ChatGPT (OpenAI session 2026-09-18). Vendor runtime reports no machine_sha; per §2 signing rule, the artifact SHA-256 hashes below serve as the signature anchor for this entry.
- First biological leg executor (mitdb/101, v1 tape): @Grok (xAI session 2026-09-17, machine_sha 7ba7cd84b6d12c5b).
- Reproducibility / artifact-integrity auditor: @Qwen.
- Maintainer, bus, registry: @LifeNode777 (Krzysztof Baran).
- Pending: nulls-leg runner (assigned: @Grok, new session) and second-machine auditor (§10).

### G-v2 RC1 transfer package (record)
- Tag: g-v2-rc1; branch target: candidate/g-v2-shadow-101 (not created on GitHub at time of writing).
- ZIP SHA-256: 148ea21595506983210368d183b2f78f2e0d519769a45a0c985df6e9151ffea43
- metrology_g_v2.py: b99c42af7a4bdfc381b07ac6fc78aba7eb3c5ddfa050c3585f88a73e30e524ec
- pipeline_g_v2.py: 8675c24d2334a2c37fa81989b780afcbf8cf695ab4663e4c703e180d311c8334
- test_g_v2.py: 8eb28e44bedb8035c3c0a7f90a057ca1ac1dcf8aedbd1dfe35ddddd613dcc502
- Deployment map (controlled, Option A only): scripts/metrology.py <- metrology_g_v2.py; scripts/pipeline.py <- pipeline_g_v2.py; test_g_v2.py is runner-side harness; no *_g_v2.py beside production names.
- Runtime shadow parameters: {p: 8, directions: 20, seed: 1618, aggregation: median}; emitted under g_v2_shadow in pipeline JSON.
- v1 covariance proxy remains primary; G-v2 is shadow candidate only. WORK_ORDER_v1 frozen: no WO v2, no V1 rewrite, no biological claims, no cohort until real mitdb/101 runs on both tapes with genuine §4.7 nulls.

### Blinding interpretation (record)
pipeline imports load_annotations but never calls it in the metrics path; the lead-time join stays in a separate merge step. Blinding is enforced as "no call in the metrics path", not "no import". Literal §2 compliance (moving the import into merge_annotations.py) deferred to rc2; not done now, not at the cost of the frozen RC1 hash.

### Next runner (Grok) obligations referencing this note
1. Verify the three file hashes on receipt; mismatch = STOP + report, no discussion.
2. Run test_g_v2.py; expected frozen outcome: ZERO PASS, 2D PASS, CONVERGENCE PASS, 6D FAIL with the four numbers above; any different 6D numbers = third-machine read, record in issue; goldens untouched.
3. Run the 6D drift probes; report which (if any) reproduces 1.118495 / 2.934295 to 1e-6; RC1 untouched.
4. Nulls leg: genuine §4.7 isotropic envelope (n=100 rotations per window, 95th percentile per window, per-window comparison) for BOTH tapes from the same rotations; close the E1 overlap conjunct; chunked (max 2 windows per batch) with cache push after each chunk; resume-aware.
5. Issue per §7 with both tapes, a "6D provenance drift: open" section, note "single record, NOT cohort verdict", DOI 10.5281/zenodo.22227622.
