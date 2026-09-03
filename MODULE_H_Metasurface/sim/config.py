"""
MODULE H — sim/config.py
Single source of truth for all Module H simulation parameters.

Every script in L1/, L2/, L3/ imports from this file.
Do NOT hardcode parameters in individual scripts.
Do NOT override these values at runtime.

Honesty markers:
  ★ = anchored in published literature
  ◇ = LifeNode integrative hypothesis (under test)

License: CC-BY-NC-SA 4.0
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple

# =============================================================================
# 0. UNIVERSAL CONSTANTS AND EXACT GEOMETRY
# =============================================================================
C0: float = 299792458.0                      # ★ speed of light [m/s]

PHI: float = (1.0 + np.sqrt(5.0)) / 2.0      # ★ golden ratio ≈ 1.6180339887

# ★ EXACT golden angle, computed from PHI. Never rounded in source.
#   Incommensurability IS the hypothesis; 137.5 is a label, not a value.
GOLDEN_ANGLE_DEG: float = 360.0 * (1.0 - 1.0 / PHI)   # 137.50776405003785
GOLDEN_ANGLE_RAD: float = 2.0 * np.pi * (1.0 - 1.0 / PHI)  # 2.3999632297286533

SUPPORTED_CARRIERS_NM: Tuple[float, ...] = (532.0, 637.0, 1550.0)  # ★


# =============================================================================
# 1. MATERIALS (dispersion rule enforced at import)
# =============================================================================
# ★ a-Si is strongly absorptive below ~700 nm (bandgap ~1.7 eV).
#   Pairing a-Si with a visible carrier is INVALID BY CONSTRUCTION.

MATERIALS: Dict[str, Dict] = {
    "LiNbO3": {"role": "Pockels modulation layer",
               "r33": 30.8e-12,                    # ★ m/V
               "n": {532.0: 2.33, 637.0: 2.29, 1550.0: 2.14}},   # ★
    "TiO2":   {"role": "meta-atom (visible)",
               "n": {532.0: 2.57, 637.0: 2.46},
               "permitted_carriers_nm": [532.0, 637.0]},
    "GaN":    {"role": "meta-atom (visible)",
               "n": {532.0: 2.50, 637.0: 2.40},
               "permitted_carriers_nm": [532.0, 637.0]},
    "Si3N4":  {"role": "meta-atom (visible)",
               "n": {532.0: 2.08, 637.0: 2.02},
               "permitted_carriers_nm": [532.0, 637.0]},
    "a-Si":   {"role": "meta-atom (IR ONLY)",
               "n": {1550.0: 3.48},
               "permitted_carriers_nm": [1550.0]},   # ★ NEVER visible
    "quartz": {"role": "substrate (Z-cut)",
               "n": {532.0: 1.55, 637.0: 1.54, 1550.0: 1.53}},
}

META_ATOM_MATERIALS: Tuple[str, ...] = ("TiO2", "GaN", "Si3N4", "a-Si")


def validate_material_for_carrier(material: str, carrier_wavelength_nm: float) -> None:
    """Hard rule: meta-atom material must permit the carrier wavelength."""
    if material not in META_ATOM_MATERIALS:
        raise ValueError(
            f"MATERIAL VIOLATION: {material} is not a meta-atom material. "
            f"Meta-atoms: {META_ATOM_MATERIALS}."
        )
    permitted = MATERIALS[material]["permitted_carriers_nm"]
    if carrier_wavelength_nm not in permitted:
        raise AssertionError(
            f"MATERIAL VIOLATION: {material} not permitted at "
            f"{carrier_wavelength_nm} nm. Permitted: {permitted}. "
            f"See config.py §1 (dispersion rule)."
        )


# =============================================================================
# 2. L1 NUMERICAL GRID
# =============================================================================
@dataclass
class L1Grid:
    """L1 analytical grid. Power-of-two N_T for SSFM/FFT. ◇ design choice."""
    n_t: int = 2048
    t_span: float = 32.0     # compressed sim-seconds at ALPHA_L1 (≈16.7 macro pulses)

    @property
    def dt(self) -> float:
        return self.t_span / self.n_t

L1_GRID = L1Grid()


# =============================================================================
# 3. GEOMETRY — φ-spiral
# =============================================================================
@dataclass
class PhiSpiralGeometry:
    """
    r(θ) = a·e^(bθ).
    ◇ b = ln(φ)/π is the REGISTERED value (METHODS_NOTES §0).
    NOTE: the 'true' golden spiral (φ per quarter turn, b = 2·ln(φ)/π) is a
    different convention and is NOT the registered hypothesis. Changing b
    requires a versioned amendment, not a code edit.
    The spiral is aperiodic by construction → RCWA forbidden for full geometry.
    """
    a: float = 0.5e-6                              # ◇ initial radius [m]
    b: float = np.log(PHI) / np.pi                 # ◇ registered value
    arm_count: int = 5                             # ◇ one arm per kernel S1–S5
    meta_atom_type: str = "cross"                  # ◇
    meta_atom_size_nm: float = 200.0               # ◇
    resolution_per_wavelength: int = 20            # ★ ≥ λ/20 (README L3)

    def r(self, theta: float) -> float:
        return self.a * np.exp(self.b * theta)

    def meta_atom_positions(self, theta_max: float, n_points: int) -> np.ndarray:
        thetas = np.linspace(0.0, theta_max, n_points)
        rs = self.r(thetas)
        return np.column_stack([rs * np.cos(thetas), rs * np.sin(thetas)])

SPIRAL = PhiSpiralGeometry()


# =============================================================================
# 4. CARRIER AND ENVELOPE (BPB doctrine)
# =============================================================================
@dataclass
class CarrierEnvelope:
    """★ Carrier = spring and mass; biology lives in the envelope (BPB).
    Frequency-inversion criterion: if the bare carrier (no BPB envelope)
    recognizes patterns better, the module FAILS (LifeNode Theory v4 §7.3)."""
    carrier_wavelength_nm: float = 532.0

    @property
    def carrier_frequency_hz(self) -> float:      # ★ computed, not prose
        return C0 / (self.carrier_wavelength_nm * 1e-9)

    micro_bpb_hz: Tuple[float, float] = (0.5, 4.0)          # ★
    meso_bpb_hz: float = 0.1                                 # ★
    macro_bpb_hz: Tuple[float, float] = (0.0001, 0.008)     # ★

    def validate_envelope_in_bpb(self, f_hz: float) -> bool:
        return (self.micro_bpb_hz[0] <= f_hz <= self.micro_bpb_hz[1]
                or abs(f_hz - self.meso_bpb_hz) < 0.05
                or self.macro_bpb_hz[0] <= f_hz <= self.macro_bpb_hz[1])

CARRIER = CarrierEnvelope()


# =============================================================================
# 5. TIME-SCALING DOCTRINE — TWO NAMED QUANTITIES
# =============================================================================
@dataclass
class TimeScaling:
    """
    ALPHA_L1 (bio-window): compresses biological time into the L1 numerical
      window. 1920 s / 1e3 = 1.92 s. Carrier is NOT simulated at L1.
    ALPHA_CE (carrier–envelope): compresses the envelope relative to a carrier
      simulated at its TRUE optical frequency (L2/L3). Derived from a target
      optical-cycle count, so the justification is arithmetic, not prose.

    Honest justification (non-exact symmetry; see METHODS_NOTES §1.5/§4):
      1. adiabatic carrier–envelope separation preserved;
      2. materials locally non-dispersive within simulated bandwidth;
      3. mechanism tested, not literal biology.
    Non-uniform compression invalidates the run outright.
    """
    alpha_l1_macro: float = 1e3       # 32 min → 1.92 s window
    alpha_ce_macro: float = 1e12      # ≈1.08e6 optical cycles at 532 nm (computed)
    target_optical_cycles: float = 1e6    # ◇ tractability target for FDTD
    alpha_invariance_tolerance: float = 0.05   # ★ 5% drift → INVALID

    def derive_alpha_ce(self, f_bio_hz: float,
                        f_carrier_hz: Optional[float] = None,
                        target_cycles: Optional[float] = None) -> float:
        """α_CE = f_carrier / (f_bio · N_target).  ★ arithmetic, not guess."""
        fc = CARRIER.carrier_frequency_hz if f_carrier_hz is None else f_carrier_hz
        nt = self.target_optical_cycles if target_cycles is None else target_cycles
        return fc / (f_bio_hz * nt)

    def optical_cycles_per_macro_pulse(self, alpha_ce: float) -> float:
        """Computed check: cycles = f_carrier · T_bio / α."""
        t_bio = K1K2.pulse_duration_min * 60.0
        return CARRIER.carrier_frequency_hz * t_bio / alpha_ce

    def alpha_pair(self, kind: str) -> Tuple[float, float]:
        """(α, α/2) invariance pair. kind ∈ {'L1_macro', 'CE_macro'}."""
        a = {"L1_macro": self.alpha_l1_macro,
             "CE_macro": self.alpha_ce_macro}[kind]
        return (a, a / 2.0)

    def check_invariance(self, m_alpha: float, m_half: float) -> bool:
        if m_alpha == 0.0:
            return m_half == 0.0
        return abs(m_alpha - m_half) / abs(m_alpha) <= self.alpha_invariance_tolerance

TIME_SCALING = TimeScaling()


# =============================================================================
# 6. K1/K2 SYNTHETIC WAVEFORMS
# =============================================================================
@dataclass
class K1K2Synthetic:
    amplitude_range_mv: Tuple[float, float] = (0.1, 1.0)   # ★ Adamatzky 2026
    pulse_duration_min: float = 32.0                        # ★ Adamatzky 2026
    motif_k1: str = "directional_spike_train_rising"        # ★ simplified
    motif_k2: str = "directional_spike_train_falling"       # ★ simplified
    noise_flicker_alpha: float = 1.0                        # ★ 1/f^α flicker
    noise_white_snr_db: float = 10.0                        # ◇ noisy variant ONLY

K1K2 = K1K2Synthetic()


# =============================================================================
# 7. NOISE PROFILES
# =============================================================================
@dataclass
class NoiseProfiles:
    """★ Every selectivity run: white AND 1/f^α at matched bandwidth.
    White noise alone is a strawman."""
    white_gaussian: bool = True
    flicker_alpha: float = 1.0
    matched_bandwidth: bool = True
    defocusing_kappa: float = 0.85      # ★ κ > 0 control (focusing = −0.85)

NOISE = NoiseProfiles()


# =============================================================================
# 8. THRESHOLDS (locked from FALSIFICATION.md; pre-registered)
# =============================================================================
@dataclass
class Thresholds:
    eta_threshold: float = 0.90              # ★ F1
    g_coh_threshold_db: float = 10.0         # ★ F2
    eta_self_consistency: float = 0.98       # ★ kernel acceptance gate
    theta_ascalon_ref: float = 0.70          # ★ F4 reference (external test)

    # F5 gate: OPEN. Frozen ONLY after first clean L1 runs, via versioned
    # amendment + LOG.md entry. None = not frozen; verdict code must refuse.
    cross_corr_offdiag_max: Optional[float] = None
    cross_corr_diagonal_min: Optional[float] = None

    pb_phase_error_max_deg: float = 2.0      # ★ L2
    focal_spot_tolerance_pct: float = 5.0    # ★ L2
    warning_zone_pct: float = 0.05           # ◇ WARNING band

    def assert_f5_gate_frozen(self) -> None:
        if self.cross_corr_offdiag_max is None or self.cross_corr_diagonal_min is None:
            raise RuntimeError(
                "F5 GATE OPEN: cross-correlation thresholds are None. "
                "Freeze them via versioned amendment after first clean L1 runs. "
                "No verdict may be computed on an open gate."
            )

THRESHOLDS = Thresholds()


# =============================================================================
# 9. FLOQUET PARAMETERS
# =============================================================================
@dataclass
class FloquetParameters:
    modulation_layer: str = "LiNbO3"
    pockels_r33: float = 30.8e-12                 # ★ m/V
    modulation_depth: float = 0.1                 # ◇ Δn/n
    coding_sequence_type: str = "analog_entrained"  # ◇ BIOS-entrained, no MCU
    t_drive_range_bio_s: Tuple[float, float] = (60.0, 3600.0)   # ◇
    subharmonic_ratio: int = 2                    # ◇ T_resp = 2·T_drive

FLOQUET = FloquetParameters()


# =============================================================================
# 10. NUMERICAL GUARDS (apparatus calibration, NOT theory thresholds)
# =============================================================================
@dataclass
class NumericalGuards:
    min_norm_eta: float = 1e-12        # ◇ L² power floor; below → η undefined
    power_floor_gcoh: float = 1e-12    # ◇ adversary floor; report "> X dB"
    eta_undefined: float = 0.0         # conservative; never inflates

GUARDS = NumericalGuards()


# =============================================================================
# 11. VERDICT ENGINE
# =============================================================================
VERDICT_PASS = "PASS"
VERDICT_WARNING = "WARNING"
VERDICT_FAIL = "FAIL"
VERDICT_INVARIANT = "INVARIANT"
VERDICT_INVALID = "INVALID_TIME_DISCRETIZATION_ARTIFACT"

def compute_verdict(value: float, threshold: float,
                    higher_is_better: bool = True) -> str:
    band = THRESHOLDS.warning_zone_pct * threshold
    if higher_is_better:
        if value >= threshold: return VERDICT_PASS
        if value >= threshold - band: return VERDICT_WARNING
        return VERDICT_FAIL
    if value <= threshold: return VERDICT_PASS
    if value <= threshold + band: return VERDICT_WARNING
    return VERDICT_FAIL

def compute_alpha_invariance_verdict(m_alpha: float, m_half: float) -> str:
    return (VERDICT_INVARIANT if TIME_SCALING.check_invariance(m_alpha, m_half)
            else VERDICT_INVALID)


# =============================================================================
# 12. IMPORT-TIME VALIDATION (fail fast, fail loud)
# =============================================================================
def _validate_config() -> None:
    # geometry identities
    assert abs(GOLDEN_ANGLE_DEG - 360.0 * (1.0 - 1.0 / PHI)) < 1e-12
    assert abs(GOLDEN_ANGLE_RAD - np.radians(GOLDEN_ANGLE_DEG)) < 1e-12
    # grid
    assert L1_GRID.n_t > 0 and (L1_GRID.n_t & (L1_GRID.n_t - 1)) == 0, "N_T must be 2^k"
    # dispersion rule
    validate_material_for_carrier("TiO2", 532.0)
    validate_material_for_carrier("a-Si", 1550.0)
    try:
        validate_material_for_carrier("a-Si", 532.0)
        raise SystemExit("CONFIG ERROR: a-Si accepted at 532 nm")
    except AssertionError as e:
        assert "MATERIAL VIOLATION" in str(e)
    # thresholds
    assert 0.0 < THRESHOLDS.eta_threshold <= 1.0
    assert 0.0 < THRESHOLDS.eta_self_consistency <= 1.0
    assert THRESHOLDS.g_coh_threshold_db > 0.0
    assert THRESHOLDS.cross_corr_offdiag_max is None, "F5 gate must stay OPEN until amendment"
    # α doctrine: justification must be arithmetic
    cyc = TIME_SCALING.optical_cycles_per_macro_pulse(TIME_SCALING.alpha_ce_macro)
    assert 1e5 <= cyc <= 1e8, f"α_CE gives {cyc:.3e} optical cycles — outside tractable band"
    assert abs(TIME_SCALING.alpha_l1_macro * 1.92 - 1920.0) < 1e-6, "α_L1 must map 32 min → 1.92 s"
    assert GUARDS.min_norm_eta > 0.0 and GUARDS.power_floor_gcoh > 0.0

_validate_config()


__all__ = [
    "C0", "PHI", "GOLDEN_ANGLE_DEG", "GOLDEN_ANGLE_RAD", "SUPPORTED_CARRIERS_NM",
    "MATERIALS", "META_ATOM_MATERIALS", "validate_material_for_carrier",
    "L1Grid", "L1_GRID", "PhiSpiralGeometry", "SPIRAL",
    "CarrierEnvelope", "CARRIER", "TimeScaling", "TIME_SCALING",
    "K1K2Synthetic", "K1K2", "NoiseProfiles", "NOISE",
    "Thresholds", "THRESHOLDS", "FloquetParameters", "FLOQUET",
    "NumericalGuards", "GUARDS",
    "VERDICT_PASS", "VERDICT_WARNING", "VERDICT_FAIL",
    "VERDICT_INVARIANT", "VERDICT_INVALID",
    "compute_verdict", "compute_alpha_invariance_verdict",
      ]
