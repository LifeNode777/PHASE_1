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
REFERENCE_DIR = "reference"nie
