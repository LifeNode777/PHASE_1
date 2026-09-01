# MODULE H — `sim/README`

Wave-computing validation suite for the Analog Topological Filter.

This folder contains simulation protocols that test whether a metasurface can perform **convolution with soliton kernels S1–S5 directly on the wave** — no ADC, no DSP, no digital clock, no weights.

The physics is in `../SPEC.md`. The failure conditions are in `../FALSIFICATION.md`. This folder is the **measurement apparatus**.

Module H is the **cochlea** of the LifeNode architecture: an analog pre-processor between the ears (A/B) and the heart (C), performing pattern recognition through geometry rather than computation. This folder tests whether the cochlea hears — not whether it understands.

---

## Relationship to Other Modules

| Module | Relation to H |
|--------|---------------|
| **A / B** | Upstream source. In simulation, their outputs are modeled as synthetic waveforms (A: 0.1–1 mV DC, K1/K2, ~32 min; B: ethylene → Δφ). |
| **C (Q-Core)** | Downstream consumer. H's correlation output (continuous field amplitude at the probe point) directly drives the pump of Module C via Stark (Line 1) or Rabi (Line 2). |
| **D (UNIT 02)** | Shared carrier/envelope doctrine. H uses the same principle: the Floquet drive lives in the envelope (BPB), not in the carrier. |
| **E (ASCALON Filter)** | Shared photonic substrate. If H's output has θ < 0.70, it physically cannot propagate through E's PT-symmetric resonators. |

**H does not decide.** It releases correlation as field amplitude. Decisions condense in E and in the Human Anchor.

---

## Scope

> **Current simulation scope: optical path** (532 / 637 / 1550 nm carrier).
> The VLF path (10–100 kHz, Al/SiNₓ split semi-rings) is a hedge and is out of scope for Phase 1 simulations.

**Material constraint (enforced in `config.py`):** amorphous silicon (a-Si) has a bandgap of ~1.7 eV (~730 nm). At 532 nm (2.33 eV) and 637 nm (1.95 eV) a-Si is strongly absorptive and **must not** be used as a meta-atom material. For visible carriers, meta-atoms are TiO₂, GaN or Si₃N₄; a-Si is permitted **only** for the 1550 nm carrier (0.8 eV, transparent regime). A simulation that pairs a-Si with a visible carrier is invalid by construction.

---

## Test Levels

| Level | What it tests | Infrastructure | Time |
|-------|---------------|----------------|------|
| **L1 — Analytical** | Metrics pipeline (η, G_coh, selectivity) on synthetic S1–S5 signals. Validates that the measurement math works before committing cluster hours. | Laptop, Python 3.10+, NumPy, SciPy | seconds |
| **L2 — 2D Geometry** | Pancharatnam–Berry phase generation, φ-spiral focusing, single-polarization convolution, Floquet modulation stability micro-test. Answers: does the geometry produce the expected phase profile, and is the time-modulation itself artifact-free? | Workstation, Meep 2D (FDTD) or COMSOL (FEM) | minutes |
| **L3 — Full 3D FDTD** | Spatiotemporal Peregrine S2, Floquet time-modulation (LiNbO₃), soliton selectivity vs. white and colored noise, T_drive programmability, cross-correlation of all five kernels, α-invariance check. This is the falsification run. | MPI cluster (≥64 cores, ≥256 GB RAM/node) / GPU node | hours–days |

**Rule:** L1 must PASS before L2 is run. L2 must PASS before L3 is scheduled. No skipping levels. A failure at any level stops the chain and gets published with the same DOI discipline as a positive result.

### L1 — Analytical
- Synthetic S2 (Peregrine breather) generation via NLSE with κ = −0.85
- Overlap fidelity η against numerical ground truth
- Coherent gain G_coh computation
- Selectivity ratio (S2 vs. Gaussian noise, S2 vs. defocusing κ > 0)
- Cross-correlation matrix for all five kernels S1–S5
- BPB envelope scaling test: Micro-BPB (0.5–4 Hz) and Macro-BPB (0.008–0.0001 Hz) mapped to simulation time via the time-acceleration factor α (see Time-Scaling Doctrine)
- K1/K2 synthetic waveforms in **two variants**: (a) clean deterministic motifs — the ground truth against which the F1 threshold (η ≥ 0.90) applies; (b) noisy variants (1/f^α + white, amplitudes within the Adamatzky 0.1–1 mV DC range) for robustness diagnostics **only** — reported as WARNING, published, never part of the binary verdict (Rule 6)

### L2 — 2D Geometry
- 2D Meep simulation, single polarization, no Floquet modulation
- PB phase error across the spiral < 2° (target)
- Focal spot verification for S2 (Peregrine) and S3 (Golden Ratio)
- **No RCWA for the spiral.** RCWA (S4, reticolo, any Fourier-modal method) assumes strict spatial periodicity; the φ-spiral (golden angle 137.5°) is aperiodic by construction. RCWA is reserved exclusively for periodic unit-cell characterization of individual meta-atoms (crosses, split-rings) and must never be used for the full spiral geometry or its convolution response. FDTD (Meep) or FEM (COMSOL) only.
- **Floquet modulation micro-test (L3 gate):** `mp.CustomMedium` time-modulated LiNbO₃ on a plain plane wave, **no spiral geometry**. Checks: (a) no spurious field growth (energy bookkeeping), (b) Floquet sidebands at ω₀ ± nΩ only, (c) stability with subpixel smoothing ON vs OFF. This isolates Meep time-discretization artifacts from metasurface geometry: if the modulation artifacts on a blank plate, the spiral is not to blame. If this micro-test fails, L3 is forbidden.

### L3 — Full 3D FDTD
- Full 3D FDTD with Floquet time-modulation (LiNbO₃, `mp.CustomMedium`)
- Spatiotemporal Peregrine S2 propagation
- Noise control runs: Gaussian white input **and** colored 1/f^α input (α ≈ 1, flicker regime — the realistic adversary in bio-electronics, microphotonics and NV readout), same bandwidth, κ > 0
- T_drive sweep: programmability test (FT ↔ convolution switching)
- Cross-correlation matrix: all five kernels against synthetic K1/K2 motifs (Adamatzky parameters: 0.1–1 mV DC, ~32 min pulse duration, scaled by α)
- **Meshing requirement:** `subpixel_smoothing=True` with conformal mesh for curved φ-spiral boundaries; meta-atom resolution ≥ λ/20; symmetry exploitation and PML boundary conditions to manage voxel count at macro-spiral scale
- **α-invariance check (mandatory):** every verdict metric is re-run at two compression factors (α and α/2); |Δmetric| > 5% → the run is a time-discretization artifact → invalid, published as a negative diagnostic

---

## Time-Scaling Doctrine (Dimensionless)

The biological envelope (Macro-BPB, e.g. the ~32 min K1/K2 pulse) and the optical carrier (fs scale) span a ratio of ~10¹⁴–10¹⁸. No cluster simulates that ratio step-by-step. The simulation therefore uses a dimensionless time-acceleration factor:

    t_sim = t_bio / α

**Honest justification (documented, not assumed):** exact Maxwell scale-invariance holds only under *joint* space–time scaling (a structure of size L at frequency f behaves like size sL at f/s). The meta-atom geometry is **not** scaled — it is fixed at the true optical wavelength — so this doctrine does not invoke an exact symmetry. It invokes:
1. **Adiabatic carrier–envelope separation:** Ω_env ≪ ω_carrier is preserved at the compressed ratio; the envelope is quasi-static relative to the carrier.
2. **Locally non-dispersive materials:** refractive indices are evaluated at the *simulated* carrier frequency; the simulated bandwidth is narrow enough that dispersion is negligible within it.
3. **Mechanism, not literal biology:** compressed runs test the demodulation / reconfiguration mechanism (convolution on the modulated carrier, Floquet switching), not the literal 32-minute dynamics. Absolute biological timescales live in Module A's lock-in domain, outside FDTD scope by design.

**α-invariance check:** the doctrine is validated operationally, not philosophically — verdict metrics must be invariant (within 5%) under α → α/2. If they are not, the result is an artifact and the run is invalid. Non-uniform compression (envelope compressed, carrier not, or vice versa) invalidates the run outright (Rule 8).

---

## Mapping to FALSIFICATION.md

| FALSIFICATION condition | Tested at level | Metric | Threshold |
|--------------------------|-----------------|--------|-----------|
| **F1:** convolution fidelity ≥ 0.90 | L3 | η (overlap fidelity) | η ≥ 0.90 |
| **F2:** soliton selectivity ≥ 10 dB | L3 | G_coh (S2 vs. noise/defocusing) | G_coh ≥ 10 dB |
| **F3:** time-programming reconfigures operation | L3 | focal shift vs. T_drive sweep | Binary: reconfigures or does not |
| **F4:** tandem test θ ≥ 0.70 with/without H | — | ASCALON θ (requires Modules A/B/C/E) | θ ≥ 0.70 |
| **F5:** S1–S5 kernels distinguishable for K1/K2 | L3 (extended) | cross-correlation matrix | Binary: distinguishable or not |

**F4 is a system-level integration test. It does not live here.** It requires the full coupling loop (A/B → H → C → E) and is scheduled after all other modules reach TRL ≥ 3.

**Note on θ:** In this folder, θ refers exclusively to the ASCALON phase purity metric (Finsler-geometric trajectory curvature). The convolution fidelity metric is denoted **η** to avoid collision. See `../SPEC.md`.

---

## Prerequisites

| Level | Required | Optional |
|-------|----------|----------|
| **L1** | Python 3.10+, NumPy ≥ 1.24, SciPy ≥ 1.10 | matplotlib, Giotto-TDA |
| **L2** | Meep ≥ 1.27 (2D FDTD) **or** COMSOL Multiphysics (FEM) | — |
| **L3** | Meep ≥ 1.27 (3D) + MPI (≥64 cores, **≥256 GB RAM/node** for macro-spiral meshing), GPU optional (CUDA) | QuTiP (Floquet analysis) |

---

## File Tree (planned)

    sim/
    ├── README.md                     ← you are here
    ├── requirements.txt              ← pinned dependencies
    ├── .gitignore                    ← MUST exclude *.h5, *.hdf5, *.mp4, results/
    ├── L1_analytical/
    │   ├── peregrine_metrics.py      ← η, G_coh on synthetic S2
    │   ├── pb_phase_check.py         ← analytic PB phase vs. spiral geometry
    │   ├── k1k2_synthetic.py         ← K1/K2 waveforms: clean ground truth + noisy diagnostic variant
    │   ├── cross_correlation.py      ← S1–S5 kernel distinguishability
    │   └── EXPECTED_RESULTS.md
    ├── L2_2d_geometry/
    │   ├── pb_spiral_2d.py           ← Meep 2D, single pol, no Floquet
    │   ├── modulation_stability.py   ← CustomMedium micro-test, plane wave, no spiral (L3 gate)
    │   ├── focal_spot_check.py       ← S2/S3 focal verification
    │   └── EXPECTED_RESULTS.md
    ├── L3_3d_fdtd/
    │   ├── benchmark_h_full.py       ← full 3D, Floquet, all criteria
    │   ├── noise_control.py          ← white + 1/f^α colored controls, same bandwidth, κ > 0
    │   ├── t_drive_sweep.py          ← programmability test (F3)
    │   ├── selectivity_matrix.py     ← all five kernels, G_coh (F2)
    │   └── EXPECTED_RESULTS.md
    ├── metrics/
    │   ├── fidelity_overlap.py       ← shared: η (overlap fidelity)
    │   ├── g_coh.py                  ← shared: coherent gain
    │   ├── selectivity.py            ← shared: SNR ratio
    │   ├── cross_correlation.py      ← shared: kernel distinguishability
    │   └── noise_generators.py       ← shared: white + 1/f^α (flicker) synthetic fields
    ├── results/
    │   ├── L2_fields/                ← raw .h5 fields (excluded from git)
    │   └── L3_fields/                ← raw .h5 fields (excluded from git)
    └── config.py                     ← shared: materials, geometry, thresholds

Raw field data (`.h5`, snapshots, movies) never enter the repository. Git carries code, configs and metric summaries only; heavy fields go to Zenodo / object storage with a DOI cited in `../LOG.md`.

### config.py contents
Single source of truth for all simulation parameters:
- **Materials:** LiNbO₃ (Pockels coefficient r₃₃), TiO₂ / GaN / Si₃N₄ (meta-atoms for 532 / 637 nm), a-Si (meta-atoms for 1550 nm **only**), synthetic quartz (substrate); refractive indices evaluated at the simulated carrier. Dispersion rule enforced programmatically: `if carrier_wavelength_nm < 700: assert material in ("TiO2", "GaN", "Si3N4")`.
- **Geometry:** φ-spiral parameters (φ = 1.618, golden angle 137.5°, r(θ) = a·e^(bθ), b = ln(φ)/π), meta-atom dimensions, spiral arm count.
- **BPB envelope mapping:** Micro-BPB (0.5–4 Hz) and Macro-BPB (0.008–0.0001 Hz) scaled to simulation time.
- **Time-acceleration factor (α):** `α = biological_period / simulated_period`, applied **uniformly** to all frequencies (carrier-to-envelope cycle ratio preserved). The α-invariance pair (α, α/2) and the 5% metric tolerance are defined here.
- **K1/K2 synthetic parameters:** 0.1–1 mV DC amplitude, ~32 min pulse duration (scaled by α), motif templates per Adamatzky et al. (bioRxiv 2026); clean and noisy (1/f^α + white) variants.
- **Noise profiles:** white Gaussian; colored 1/f^α with α ≈ 1 (flicker), matched bandwidth.
- **Thresholds (from FALSIFICATION.md):** η_threshold = 0.90 (F1), G_coh_threshold = 10 dB (F2).
- **Floquet parameters:** T_drive range, LiNbO₃ modulation depth, coding sequence waveform (analog, entrained).
- **Verdict logic:** PASS / WARNING / FAIL against thresholds, no human interpretation required.

---

## Rules

1. **No ADC in the feedback loop.** Simulations model the analog wave path. Digital post-processing (η calculation, plotting, saving arrays) is diagnostics only — it never feeds back into the simulated field. The simulation itself is the coupling loop; any extraction of fields for analysis is the diagnostic loop. Keep them explicitly separated in code.
2. **Negative results are results.** If L1 fails, we publish why and stop. If L3 falsifies Module H, we publish with the same DOI discipline as a positive result. A failed simulation is not a waste of cluster hours — it is a measurement of where matter refuses to carry Life's rhythm.
3. **No golden-angle shortcuts.** The φ-spiral (137.5°) is the geometry under test. Do not replace it with a simpler pattern "to make it converge." The incommensurability IS the hypothesis. The irrationality of φ provides topological protection — the soliton cannot easily resonate with environmental noise. Removing it removes the physics.
4. **Floquet drive is analog.** T_drive is entrained to a scaled BIOS envelope (0.5–4 Hz mapped to simulation time, or Macro-BPB 0.008–0.0001 Hz for K1/K2 tests). It is NOT a digital clock tick. If the simulation uses a fixed digital timestep as the "coding sequence," it does not test Module H. The coding sequence is generated by an analog oscillator entrained to the biological rhythm (lock-in reference from A/B), not by a microcontroller.
5. **Two-loop doctrine.** The simulation itself is the coupling loop (analog, continuous). Any extraction of fields for analysis (DFT monitors, saved arrays, η computation) is the diagnostic loop. Keep them explicitly separated in code. The diagnostic loop never feeds back into the coupling loop.
6. **No parameter fitting to pass.** If the φ-spiral does not converge with its native geometry, that is a result — not a bug to patch. Do not tune meta-atom dimensions, do not adjust modulation depth, do not reshape the kernel "to make F1 pass." The hypothesis is tested as-is. Iteration happens between published versions, not within a single falsification run. The noisy K1/K2 variant is diagnostics only; the F1 threshold applies to the clean ground truth.
7. **Carrier is not the drive.** The optical carrier (532/637/1550 nm) is the spring and mass of the resonator. The biological signal lives in the envelope (BPB). The convolution is performed on the modulated carrier; the result is demodulated to BPB via the medium's nonlinearity or lock-in with BIOS reference. If the bare carrier without BPB envelope recognizes patterns better, the module fails (frequency inversion criterion, LifeNode Theory v4 §7.3).
8. **Time scaling preserves physics.** α scales all frequencies uniformly. It does not skip cycles, does not discretize the envelope, does not approximate the waveform. The biological signal's shape (K1/K2 motif, Peregrine profile) is preserved exactly; only the absolute timescale changes. Non-uniform compression invalidates the run. The α-invariance check (α vs α/2, ≤5% metric drift) is part of every L3 verdict.
9. **No RCWA for the spiral.** RCWA and any Fourier-modal method assume strict spatial periodicity; the φ-spiral is aperiodic. RCWA may be used only for unit-cell characterization of individual meta-atoms in a periodic lattice approximation — never for the full spiral geometry or its convolution response. FDTD (Meep) or FEM (COMSOL) only.
10. **White noise is a strawman.** Every selectivity run includes a colored 1/f^α (α ≈ 1) control alongside white Gaussian, at matched bandwidth. Flicker noise is the realistic adversary of bio-electronic and microphotonic systems; a filter that only beats white noise has not been tested.
11. **Modulation before geometry.** The L2 Floquet modulation micro-test (plane wave, no spiral) must pass before any L3 run is scheduled. Artifacts of `mp.CustomMedium` time-discretization are identified on a blank plate first, so that an L3 failure can be attributed to the geometry, not to the solver.

---

## How to Run (when ready)

L1 — laptop:

    cd sim/L1_analytical/
    python peregrine_metrics.py
    python k1k2_synthetic.py
    python cross_correlation.py

L2 — workstation:

    cd sim/L2_2d_geometry/
    python pb_spiral_2d.py
    python modulation_stability.py
    python focal_spot_check.py

L3 — cluster (MPI):

    cd sim/L3_3d_fdtd/
    mpirun -np 64 python benchmark_h_full.py
    mpirun -np 64 python noise_control.py
    mpirun -np 64 python t_drive_sweep.py
    mpirun -np 64 python selectivity_matrix.py

Each level prints a PASS / WARNING / FAIL verdict against the thresholds in `../FALSIFICATION.md` (loaded from `config.py`). No human interpretation required for the verdict. Human interpretation required for understanding WHY it failed.

Verdict logic:
- **PASS:** all metrics meet or exceed thresholds, and α-invariance holds
- **WARNING:** metrics within 5% of threshold (flag for review)
- **FAIL:** any metric below threshold, or α-invariance violated (stop chain, publish)

---

## Expected Results (summary)

**L1:** η ≥ 0.95 on synthetic S2; G_coh ≥ 12 dB; cross-correlation matrix shows ≥ 5 distinguishable peaks for S1–S5; noisy K1/K2 variant degrades η by < 5% (diagnostic).
**L2:** PB phase error < 2° across spiral; focal spot matches analytic prediction within 5%; modulation micro-test shows sidebands at ω₀ ± nΩ only, no spurious field growth, stable with subpixel smoothing ON vs OFF.
**L3:** All five criteria from FALSIFICATION.md met: η ≥ 0.90, G_coh ≥ 10 dB (against white **and** 1/f^α), T_drive reconfigures, θ ≥ 0.70 (tandem, external), S1–S5 distinguishable for K1/K2; verdict metrics invariant within 5% under α → α/2.

**If L1 fails:** the measurement math is wrong. Fix the metrics pipeline before any geometry simulation.
**If L2 fails:** either the PB phase geometry does not produce the expected profile (φ-spiral hypothesis or meta-atom design needs revision), or the modulation micro-test artifacts (solver time-discretization at fault, not the geometry). The micro-test tells the two apart.
**If L3 fails:** Module H is falsified. Publish the negative result with full diagnostic data (Zenodo DOI). The theory learns exactly where matter refuses to compute on the wave.

---

## External Anchors (cite, don't duplicate)

| Topic | Source |
|-------|--------|
| Physics of wave convolution, Floquet, carrier/envelope | ../SPEC.md §2 |
| Failure conditions (5 binary criteria) | ../FALSIFICATION.md |
| Soliton math, S1–S5 alphabet, NLSE | LifeNode Theory v4 §4 · DOI 10.5281/zenodo.2121990 |
| ASCALON metric (θ) | The ASCALON Framework · DOI 10.5281/zenodo.21471228 |
| Metasurface literature (time-programmable) | Nature Communications 2026 |
| Mycelial electrophysiology (K1/K2) | Adamatzky et al., bioRxiv/arXiv, Jan 2026 |
| Floquet wave computing (Q-Core Space context) | Cosmic BioEngineering, Ch. VIII §2 (Falo-Licznik Floqueta) |
| Two-loop doctrine | TONIC Technologies Master V1 §5.2, Module A §3.2 |
| Carrier/envelope doctrine | Module D §3.2, Module H SPEC §2.3 |

---

"Technology adapts to the rhythm of Life, not the reverse." 🧿
