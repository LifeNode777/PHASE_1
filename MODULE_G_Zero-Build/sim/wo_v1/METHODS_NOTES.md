```markdown
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

## Deviations log

| Date       | Executor   | Description                          | Status      |
|------------|------------|--------------------------------------|-------------|
| (none yet) |            |                                      |             |

## Update 2026-08-31 — numerical stability of cond(g)

The finite-difference Hessian of the Minkowski functional on 60 s ECG windows produced extreme condition numbers (capped at 1e6).  
**Operational decision:** the primary reported `cond_g` and anisotropy index are now the condition number of the sample covariance of unit velocities.  
Qhull hull construction and F evaluation remain active for θ_canon and for the origin-interior acceptance test.  
This estimator change is recorded here so that any later auditor can reproduce the exact numerical path. A future WORK_ORDER_v2 may restore a regularised Finsler Hessian if desired.

"""
MODULE G — WORK_ORDER_v1 configuration
Pre-registered constants from §§4–5. Do not change without creating WORK_ORDER_v2.
"""

SEED = 1618

# Sampling
TARGET_FS = 128.0          # Hz
HIGHPASS_CUTOFF = 0.5      # Hz, zero-phase baseline wander removal

# Takens embedding (§4.2)
MI_BINS = 64
MAX_LAG_S = 2.0            # search lag ≤ 2 s
FNN_THRESHOLD = 0.10
M_MIN, M_MAX = 3, 6

# Windows (§4.3)
WINDOW_S = 60.0            # 60 s
STRIDE_S = 15.0            # 75% overlap
SG_WINDOW = 41             # Savitzky–Golay
SG_POLY = 3

# Phase binning (§4.4)
N_PHASE_BINS = 32
MIN_SAMPLES_PER_BIN = 10

# Indicatrix / F / g (§4.6)
MAX_HULL_POINTS = 1500
BOOTSTRAP_B = 200
FD_DIRECTIONS = 20         # random tangent directions for finite differences
QHULL_FAIL_RATE_LIMIT = 0.20

# Null models (§4.7)
N_NULLS = 100
NULL_WINDOWS_PER_RECORD = 20   # runtime budget

# Decision criteria (§5)
COHORT_PASS_FRACTION = 0.80
E4_WINDOW_FRACTION = 0.80
E1_CI_HALFWIDTH = 0.5
E2_SPEARMAN = 0.90
E2_SPEARMAN_SENS = 0.85
E3_SPEARMAN = -0.50

# Data
NSRDB_RECORDS = None       # all 18
MITDB_RECORDS = [f"{i}" for i in range(101, 111)]  # first 10: 101–110
LTSTDB_RECORDS = ["201", "202", "203", "204", "205"]  # TIER-2 optional

# Paths (relative to sim/wo_v1/)
DATA_DIR = "data"
OUTPUT_DIR = "outputs"
REFERENCE_DIR = "reference"
