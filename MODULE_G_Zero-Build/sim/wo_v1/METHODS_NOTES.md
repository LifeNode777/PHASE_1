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
