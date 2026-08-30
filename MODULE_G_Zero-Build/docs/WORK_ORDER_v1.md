# MODULE G — WORK ORDER v1
## Zero-Hardware Computational Validation of the EPS–Finsler Metrology (LN-EPS) on Open Physiological Data

**Author:** Krzysztof Baran / LifeNode Research Collective
**Version:** 1.0 · **Date:** 30 August 2026
**Status:** Pre-registered operational specification · **License:** CC-BY-NC-SA 4.0
**Parent project:** [LifeNode777](https://github.com/LifeNode777) · **Module:** [MODULE_G_Zero-Build](../)
**Contact:** krzysiek_230@op.pl

**Cites (do not duplicate):**
- LifeNode Theory v4.0 · DOI 10.5281/zenodo.2121990
- The ASCALON Framework · DOI 10.5281/zenodo.21471228
- Symplectic Trajectory Reconstruction + Python toolkit · DOI 10.5281/zenodo.19811561 · [Quantum_Medicine](https://github.com/LifeNode777/Quantum_Medicine)
- LifeNode Extensions, Whitepaper v1 + Documents 1/4–4/4 (29 Aug 2026)
- Phase 1 Roadmap + The Swarm and the Consortium (companion doc)

---

## 0. How to use this document

- **Executor (swarm):** you need a laptop, Python, and a few dozen hours. You produce **evidence**, not certification. Follow §4 exactly; report via §7.
- **Auditor (second executor):** re-run the executor's pinned code on a different machine; identical verdicts upgrade the result to *replicated* (§10).
- **Author/maintainer:** this file is **immutable once the first result is submitted**. Any change → `WORK_ORDER_v2.md` with a changelog (§12).
- **Consortium readers:** this is the swarm-side root of the critical path `G → A/B → C → D → E → F`. Blinded longitudinal clinical lead-time trials (n ≥ 100) remain **consortium-only** (Swarm doc §2–3); nothing here promises them.

**Motto:** no cost estimates, no product promises. Negative results are results.

---

## 1. Scope: what is tested, what is not

**Tested here (binary, pre-registered):** the four sub-conditions of Extensions Doc 4 §6 on open ECG data:

| ID | Claim under test | Null consequence (if fails) |
|----|------------------|------------------------------|
| **E1′** | empirical indicatrix is stably convex between repetitions → F is well-defined at this scale | Finsler postulate fails **at ECG scale** (estimator or ontology; §9 disambiguates) |
| **E2′** | the four circulating θ renderings are gauges/shadows of one invariant (θ_canon) | unification fails; θ_proj and θ_curv variants remain separate observables |
| **E3′** | degradation at low θ_canon co-occurs with cond(g) → ∞ (the threshold is geometric: loss of Finslerity, "The Flattening") | geometric reading of the 0.70 threshold fails; threshold returns to status of empirical constant |
| **E4′** | F reconstructed from data is statistically distinguishable from a direction-independent (Riemannian/isotropic) metric | Timescape anisotropy fails **at ECG scale** |

**Exploratory (reported, NOT pass/fail):** rank-based phase-drift lead time before annotated arrhythmia events on `mitdb` (§5.5). This feeds the consortium trial design; it is **not** falsification condition 4 of the theory (which requires blinded n ≥ 100 and the DRIVE-REM calibration).

**NOT tested here (by design):**
- absolute calibration of θ = 0.70 — requires τ_decay from **DRIVE-REM** (Doc 1 §4.5); until then, any absolute-threshold claim on open data is explicitly out of scope;
- torsion residuals H1′–H3′ (wet lab / ODMR) — holonomy step is **optional tier** here (§4.8);
- Kibble–Zurek scaling KZ1′–KZ3′ (QUENCH-RATE, wet lab);
- any hardware module (A–F, H).

**Doctrine compliance:** this work order is purely observational on archived data; all discretization is diagnostic and offline. It therefore trivially satisfies **P-HIH-1** and the two-loop doctrine (Extensions Doc 2 §3.3).

---

## 2. Epistemic rules

1. **Pre-registration.** This document (with its thresholds in §5) is the pre-registration. Mint a Zenodo DOI for this file **before** the first run is executed; cite that DOI in every submission. Optionally mirror on OSF/AsPredicted.
2. **Blinding.** Metrics are computed **before** clinical annotations are loaded. Implementation rule: the metric script MUST NOT import annotations; a separate `merge_annotations.py` step joins them afterwards. Executing both steps in one notebook run violates blinding → result void, re-run required.
3. **Seeds and pins.** Global random seed **1618**. Library versions recorded in every output JSON; exact pins live in `sim/reference/requirements.txt` once the reference implementation exists (§9).
4. **Negative results are results.** A cohort-level fail on any E′ is published with the same DOI discipline as a pass (Phase 1, Falsifiability). It localizes the scale at which the processual ontology loses support (Doc 4 §0.2) — that is information, not defeat.
5. **Credit.** The first executor of a complete, two-machine-reproducible run is offered co-authorship on the results preprint and a Zenodo credit record. Auditors are credited as auditors.
6. **No write access.** Work happens via fork + pull request; every entry signed (name/handle + machine hash). Participation is defined by work, not invitation.

---

## 3. Data (open, no login)

| Dataset | Content | Use | Tier |
|---|---|---|---|
| **nsrdb** (MIT-BIH Normal Sinus Rhythm) | 18 records × ~2 h, 128 Hz | E1′–E4′ cohort (healthy baseline) | TIER-1 (mandatory) |
| **mitdb** (MIT-BIH Arrhythmia) | 48 records × ~30 min, 360 Hz, beat + arrhythmia annotations | E1′–E4′ (first 10 records: 101–110) + exploratory lead-time | TIER-1 |
| **ltstdb** (Long-Term ST) | 24 h records, 250 Hz, ischemia annotations | exploratory long-horizon lead-time (5 records: 201–205) | TIER-2 (optional) |

Fetch with `wfdb.dl_database(...)`. Resample everything to **128 Hz** (anti-aliased). Use first available ECG channel per record; record the channel choice in JSON.

---

## 4. Pipeline (LN-EPS steps 1–7, operationalized)

### 4.0 Environment pins
Python ≥ 3.10; `numpy`, `scipy` ≥ 1.11 (Qhull via `scipy.spatial.ConvexHull`), `wfdb` ≥ 4.0, `giotto-tda` ≥ 0.6 (TIER-3 only), `pandas`, `matplotlib`. Record actual versions in output.

### 4.1 Load & resample
`x(t)` at 128 Hz; remove baseline wander with a 0.5 Hz high-pass (zero-phase); **no** notch filtering (50/60 Hz structure is part of the null-model comparison, and surrogates preserve it).

### 4.2 Embedding (Takens)
- τ: first local minimum of mutual information (64-bin estimator, search lag ≤ 2 s; fallback: first minimum of autocorrelation if MI has no minimum before 2 s — flag window).
- m: False Nearest Neighbors, smallest m with FNN fraction < 0.10; hard bounds **3 ≤ m ≤ 6**; if never < 0.10 by m = 6, use 6 and flag window.

### 4.3 Windows & derivatives
- Windows: **60 s** (7680 samples), stride **15 s** (75% overlap).
- Smooth embedded trajectory with Savitzky–Golay (window 41, poly 3); velocities `v` and accelerations `a` from SG derivative coefficients (same window/poly).

### 4.4 Phase binning & Reeb proxy R (per window)
- PCA on window points; phase φ(t) = Hilbert phase of PC1.
- **32 phase bins**; per bin: mean position (the empirical closed cycle) and mean unit velocity → **R(φ)** (Doc 4 §4.1).
- Window accepted iff every bin has ≥ 10 samples; else exclude and count exclusions in JSON.

### 4.5 The four θ renderings (per window)
Report **all four**, always (Doc 4 §4.4 corollary):
1. **θ_canon** (primary, bounded [0,1] by construction):
   θ_canon = mean over samples of ⟨v, R(φ)⟩_g / (F(v)·F(R(φ))), with g and F from §4.6.
2. **θ_proj** (v4 §6.2 shadow): ∫⟨v, R(φ)⟩₊ dt / ∫ ‖δγ‖ dt, where δγ = deviation of the point from the per-bin mean cycle position.
3. **θ_curv_TT** (TT Master §9.1 shadow): ∫ κv‖² dt /  ‖v‖² dt, κ = sqrt(‖v‖²‖a‖² − ⟨v,a⟩²)/‖v‖³ (m-dimensional curvature).
4. **θ_curv_ASC** (ASCALON.txt shadow): ∫ ‖a‖·‖v‖ dt / ∫ ‖v‖² dt.
Shadows are reported raw **and** rank-normalized per record; only θ_canon is used in E3′.

### 4.6 Indicatrix, F, g_ij, cond(g) (per window)
- I_x = convex hull (Qhull) of observed velocity vectors, subsampled to ≤ 1500 points; origin verified interior (else exclude window, count).
- F(w) = gauge (Minkowski functional) of I_x, evaluated via facet inequalities of the hull.
- g_ij = ½ ∂²F²/∂w^i∂w^j at w = R, by central finite differences on a random tangent 2-plane basis (20 directions); eigenvalues λ_min, λ_max of the projected metric.
- **cond(g) = λ_max/λ_min**; anisotropy index = log cond(g).
- Stability: bootstrap **B = 200** (resample hull points) → 95% CI of cond(g) per window.
- If Qhull fails on > 20% of windows of a record → **work-order bug** path (§9), not a null.

### 4.7 Null models (per record)
- **(a) FT surrogates:** phase-shuffled (spectrum preserved), n = 100.
- **(b) AR(1):** matched autocorrelation/spectrum, n = 100.
- **(c) isotropic renormalization:** per-sample velocity rotated by uniform random rotation in SO(m) (direction–speed pairing destroyed, speed distribution preserved), n = 100.
Nulls are evaluated on the **first 20 accepted windows** per record (runtime budget); envelope = 95th percentile of the null anisotropy index per window.

### 4.8 Optional tiers (do not gate E1′–E4′)
- **TIER-2:** ltstdb records 201–205, same pipeline, exploratory lead-time vs ischemia annotations (§5.5).
- **TIER-3:** torsion from holonomy of small I-loops (Doc 4 §3, step 6; H3′ estimator) and persistent homology defects β₁ (giotto-tda, Doc 3 step 8). Reported as research-grade, explicitly ◇ in the Extensions layering.

---

## 5. Pre-registered decision criteria

Cohort = TIER-1 records (18 nsrdb + 10 mitdb). **Per-record pass** thresholds below; **cohort pass** = ≥ 80% of records pass.

- **E4′ (anisotropy):** ≥ 80% of a record's accepted windows have log cond(g) above the 95% envelope of null (c).
- **E1′ (reconstructability):** ≥ 80% of accepted windows have bootstrap relative CI half-width of cond(g) < 0.5, **and** the two record halves' median-cond(g) 95% CIs overlap.
- **E2′ (unification):** pairwise Spearman ρ ≥ 0.9 across the record's windows among {θ_canon, θ_proj, θ_curv_TT, θ_curv_ASC} (all six pairs). Sensitivity at ρ ≥ 0.85 reported alongside.
- **E3′ (geometric threshold):** per-record Spearman(θ_canon, log cond(g)) ≤ −0.5.

### 5.5 Exploratory lead-time (mitdb; TIER-2 adds ltstdb)
Drift event = θ_canon below the record's 10th percentile for ≥ 3 consecutive windows. `lead_min` = time from drift onset to the next arrhythmia annotation (mitdb) / ischemia annotation (ltstdb). Report the full distribution (median, IQR, fraction of events preceded by drift). **No pass/fail.** Absolute 0.70 threshold and ≥ 6 h lead remain consortium-level (Swarm doc §3; Doc 1 §4.5).

---

## 6. Interpretation matrix (verdict → meaning)

| Outcome | Reading | Next action |
|---|---|---|
| E1′+E4′ pass | Finsler-anisotropic metrology is supportable at ECG scale | proceed to DRIVE-REM calibration; work order v2 adds torsion as mandatory |
| E4′ fail | Timescape anisotropy falsified **at this scale** (Doc 4 §0.2: null localizes the ontology's support scale) | publish negative; check other scales (mycelial Eden Node 0) before general claims |
| E2′ fail | θ_canon unification fails; shadows stay separate observables | clinical calibration must pick one shadow; Whitepaper v2 revises §4.3 |
| E3′ fail | 0.70 loses its geometric reading (returns to empirical constant) | ASCALON threshold re-labeled; Module E hardware rationale weakened |
| E1′ fail | estimator unstable → **no theory verdict yet** | work order v2 (estimator redesign), §9 |

---

## 7. Output schema & submission

Per record JSON:

    {
      "record": "mitdb/101", "m": 5, "tau_s": 0.09,
      "windows_accepted": 114, "windows_excluded": 6,
      "verdicts": {"E1": true, "E2": true, "E3": true, "E4": true},
      "spearman_matrix": {"canon_proj": 0.94, "...": "..."},
      "cond_g_median": 12.4, "cond_g_ci95": [9.1, 17.8],
      "lead_min_distribution": {"n_events": 3, "median": null},
      "libs": {"numpy": "1.26.4", "...": "..."},
      "seed": 1618, "machine_sha": "...", "executor": "@handle"
    }

Plus cohort summary JSON + one notebook per record + `METHODS_NOTES.md` (deviations = void run).

**Submit:** open an issue on `LifeNode777/PHASE_1`, label `module-G`, title:
`[MODULE G] WORK ORDER v1 result: E1=<T/F> E2=<T/F> E3=<T/F> E4=<T/F>`
Body: link to fork branch (`MODULE_G_Zero-Build/sim/wo_v1/`), runtime, RAM, versions.

---

## 8. Runtime budget & tiers

- **TIER-1:** ≈ 4–12 laptop-hours total (convex hulls dominate; m ≤ 6, ≤1500 hull points, 20 windows × 100 nulls per record). If your run exceeds 2× this, file `work-order-bug` (estimator too heavy), do not silently optimize.
- **TIER-2/3:** optional; reported separately.

---

## 9. Work-order bugs vs theory nulls

A sub-condition counts as a **theory null** only if the estimator is stable (E1′ machinery functional) and the run reproduces on a second machine. Qhull/numerical failure rates > 20%, CI widths always divergent, or schema ambiguities → `work-order-bug` issue with logs; theory verdict **suspended** for that sub-condition until v2. The first two-machine-reproducible implementation is merged as `sim/reference/` and pinned; on text/code conflict, **this text prevails** and the discrepancy is logged.

---

## 10. Registry entry & replication

Verdicts enter the Extensions falsification registry (Whitepaper v1, E1′–E4′) as *swarm-produced*. A verdict becomes *replicated* when an independent auditor reproduces it on different hardware. Per the consortium Rubicon (Swarm doc §4): replicated G lead-time/anisotropy evidence + two independent positive module coupons + absorbed negatives = **Proof of Inevitability**, the consortium's entry criterion. This work order is the first brick of that ramp.

---

## 11. References

1. Ehlers, Pirani, Schild (1972); Pfeifer, *Int. J. Geom. Meth. Mod. Phys.* 16, 1941004 (2019); Voicu (2026).
2. Takens (1981); Fraser & Swinney (1986).
3. Goldberger et al., PhysioNet (2000) — nsrdb, mitdb, ltstdb.
4. Baran K.: LifeNode Theory v4; ASCALON Framework; Symplectic Trajectory Reconstruction; Tonic Technologies Master V1; Multiperspective V2; LifeNode Extensions Docs 1/4–4/4 (Zenodo/GitHub 2026).
5. The Swarm and the Consortium (Phase 1 companion doc).

---

## 12. Changelog rule

v1 frozen on first submitted result. v2 candidates already logged (not active): mandatory torsion tier after DRIVE-REM calibration; exact-pins requirements; m = 7 allowance if runtime permits.

---

*"Technologia ma się dostosować do rytmu Życia, a nie odwrotnie."*
*"Technology adapts to the rhythm of Life, not the reverse."* 🧿
