# MODULE G: ZERO-BUILD PROTOCOL (MATHEMATICAL VALIDATION)
## The Scientific Safety Fuse of the Project: Falsification Without Hardware

**Author:** Krzysztof Baran / LifeNode Research Collective
**Version:** 0.1 (Draft)
**Date:** 4 August 2026
**Status:** TRL 1 → TRL 3 roadmap
**License:** CC-BY-NC-SA 4.0
**Contact:** krzysiek_230@op.pl

**Epistemic note:** Module G makes no hardware claims — its claims are statistical and concern the predictive power of the θ metric. The component methods (Takens embedding, Grassberger–Procaccia, Rosenstein, persistent homology) are mature literature (★); the LifeNode hypothesis is solely that θ carries early-warning information **irreducible** to point metrics (◇). G is the only module that can falsify the entire theory at the cost of a few dozen laptop-hours — and that is exactly why it stands **first** on the critical path.

---

## ABSTRACT

Module G is the **operational falsification engine** of the LifeNode architecture: a validation protocol for the processual hypothesis **without any hardware**, on open datasets (PhysioNet, Eden Node 0) and — eventually — on Module D field logs. G does not build, control, or entrain. G **observes and judges**: whether the geometric trajectory purity θ, defined in *The ASCALON Framework* (Zenodo, DOI 10.5281/zenodo.21471228), precedes clinical decoherence by ≥ 6 h (target: 24–48 h) with sensitivity ≥ 60%, in a way irreducible to point statistics.

The document closes the three-layer contract of Module G: **mathematics** (ASCALON Framework — contract of definitions and thresholds), **code** (`LifeNodeTrajectoryAnalyzer` toolkit in the `Quantum_Medicine` repository, Zenodo DOI 10.5281/zenodo.19811561 — contract of implementation), **protocol** (this SPEC — contract of honesty: pre-registration, blinding, frozen thresholds). If G falls — the whole theory falls (overall falsification criterion #4: epiphenomenality of ASCALON). If G survives — the consortium gets the green light to build A–F with quantified confidence.

---

## 1. CONTEXT: WHY MATHEMATICS FIRST

### 1.1 The cheapest possible theory-killer
Every hardware module of Phase I costs orders of magnitude more than G. Yet G tests the **core claim** of the project — that the trajectory carries information the points do not — at the price of compute time. Building anything before G is therefore a logical and economic absurdity. The critical path does not start with G by accident: **G → A/B → C → D → E → F**.

### 1.2 G as consortium onboarding
G is the only module executable **today, by anyone, for zero money**: laptop + Python + open data. This makes it the natural entry test for the consortium: "if you cannot reproduce G's results from a pre-registered protocol, do not build Module C." G is also the consortium's first deliverable that is not a device — it is a **signed, pre-registered research protocol**.

### 1.3 Ontology of G: observer, not participant
In the two-loop doctrine, G lives **exclusively in the diagnostic loop**. It does not couple to biology, does not entrain, does not control — so discretization (ADC, files, CSV) is **not an ontological sin here**: G imposes no clock on anything, because it touches nothing. This asymmetry defines the difference between diagnostics and intervention: Modules A–F must remain analog in the coupling loop; Module G is **by definition** a digital observer of trajectories. G does not participate in Embiosis — G measures it.

---

## 2. THE THREE-LAYER CONTRACT OF MODULE G

| Layer | Document | Role |
|-------|----------|------|
| **Mathematics** | *The ASCALON Framework* (Zenodo, DOI 10.5281/zenodo.21471228) | Definitions: θ, thresholds (0.90/0.80/0.70/0.60), Cartan tensor, Symplectic Collapse, NLSE mapping |
| **Code** | `Quantum_Medicine` toolkit (Zenodo DOI 10.5281/zenodo.19811561) | Implementation: Takens, D₂, λ₁, θ(t), sliding window, PhysioNet integration (wfdb) |
| **Protocol** | This SPEC (§5) | Honesty: pre-registration, blinding, frozen thresholds, definition of n, negative publication |

"Cite, don't duplicate" principle: the `MODULE_G_Zero-Build/` folder **does not copy the code** — it points to the toolkit as the single source of truth, exactly as the Phase 1 repo cites the theory via DOIs.

---

## 3. HYPOTHESES AND PIPELINE

### 3.1 Hypotheses tested by G
- **H1 (lead time):** a drop θ < 0.70 precedes clinical manifestation (arrhythmia, seizure, decompensation) by ≥ 6 h; design target 24–48 h.
- **H2 (sensitivity):** phase-drift detection with sensitivity ≥ 60% (target: ≥ 70–80%).
- **H3 (irreducibility):** the predictive power of θ **cannot** be fully replicated (p > 0.05) by point metrics (mean HR, peak amplitude) without phase-space reconstruction.
- **H4 (topological signature, secondary):** healthy attractors exhibit non-trivial topology (β₁ ≈ 3–5, β₂ ≈ 1–2; D₂ ≈ 2.5–3.5; λ₁ ≈ 0.01–0.05); pathological states show homogenization (β₁ → 0) and/or smudging.

### 3.2 Pipeline (the stack as algorithm)
1. **Data layer:** PhysioNet (incl. MIT-BIH Arrhythmia, long-term EEG/ECG databases), Eden Node 0 (mycelial K1/K2 ~32 min, BPV; Zenodo DOI 10.5281/zenodo.18304107), own recordings ≥ 24 h @ ≥ 100 Hz; eventually Module D field logs (θ(t), I(t)) as an extension beyond clinical data.
2. **Reconstruction (★):** Takens embedding; τ — first minimum of mutual information (Fraser–Swinney); m — false nearest neighbors (m ≥ 2D₂+1). Dataset-specific parameters: ECG τ ≈ 10–100 ms; mycelium τ ≈ 5–10 min.
3. **Invariants (★):** D₂ — Grassberger–Procaccia; λ₁ — Rosenstein; persistent homology — β₀/β₁/β₂ (Giotto-TDA/ripser, pre-registered landmark subsampling).
4. **Metric θ (◇):** speed-weighted curvature, θ = ∫κ·s dt / ∫s² dt; sliding windows 5–10 min; drift rule: θ < 0.70 in ≥ 3 consecutive windows.
5. **Validation:** comparison of drift events with clinical annotations (wfdb); report: sensitivity, specificity, lead time with confidence intervals.

**Expected bands (per STR, to be frozen at pre-registration):** healthy θ 0.75–0.95; pre-pathological 0.60–0.70; clinical < 0.60.

---

## 4. POSITION IN THE SYSTEM

| Module | Depends on | Enables |
|--------|-----------|---------|
| **G** | — (after D is built: field logs as extension) | Theory validation before hardware (de-risks A–F) |

G is the **independent root** of the critical path and the only module whose outcome conditions the sense of building the rest. Its relation to Module E is mirror-symmetric: E is the physical phase fuse **inside** the coupling loop; G is the statistical fuse **outside** of it. Both exist so that the project can die early and cheaply — or survive honestly.

---

## 5. BLIND-TRIAL PROTOCOL (CONTRACT OF HONESTY)

This is the heart of Module G. Without it, θ is numerology; with it — science.

1. **Pre-registration:** protocol, thresholds (θ_crit = 0.70, 3-window rule, window sizes, pooling of databases, definition of n) and the **hash of the analysis script** deposited on Zenodo/OSF **before** running the analysis.
2. **Freezing the normalization:** the toolkit contains an empirical scaling factor for θ (clipping to [0,1]); this factor is **calibrated on the healthy control set only and frozen at pre-registration**. Any post-hoc correction on pathological data = invalidation of the trial. This is a consciously addressed researcher degree of freedom.
3. **Procedural blinding:** the analysis script **does not read annotation files**; drift events are frozen before annotations are unlocked; comparison is run by a separate script/person.
4. **Definition of n:** n ≥ 100 counted as **pathological events** (pooled across databases per the pre-registered rule), not as number of files; reported separately per database.
5. **Anti-circularity of artifact rejection:** noise filtering (motion, electrodes) **does not use θ** or any quantity derived from it; only independent criteria (amplitude, saturation, independent reference channels).
6. **Publication:** negative results go to Zenodo with the same DOI discipline as positive ones. A failure of G is published as "ASCALON is epiphenomenal" — and that is a success of the project's scientific method.

---

## 6. ENGINEERING GAPS AND LIMITATIONS (HONESTLY)

1. **Normalization of θ** — see §5.2: the only explicit degree of freedom; mitigated by freezing.
2. **Non-stationarity of long recordings** — electrode drift and circadian variability can imitate smudging; mitigated by pre-registered, θ-independent artifact filtering.
3. **Cost of PH on long windows** — persistent homology on full trajectories is computationally heavy; landmark subsampling must be pre-registered so it does not become another degree of freedom.
4. **Operationalization of "clinical manifestation"** — PhysioNet annotations are event-based; per database, pre-register what counts as an event (arrhythmia onset, seizure, decompensation).
5. **Availability of n ≥ 100** — MIT-BIH (48 recordings) is not enough on its own; pooling multiple databases is necessary and must be frozen before analysis.
6. **ASCALON condition #4 (frequency inversion)** — **is not tested in G** (requires biosubstrate stimulation); G tests conditions 1–3; inversion passes to hardware modules A/B/C. Explicit division of labor, not a gap.

---

## 7. FALSIFICATION CONDITIONS

Module G is considered **failed** if:

1. **In blinded tests (n ≥ 100)** a drop θ < 0.70 does not precede arrhythmia by ≥ 6 h. *Interpretation:* H1 falls; simultaneously overall falsification criterion #4 of the theory falls (epiphenomenality of ASCALON) — G is its trigger.
2. **Detection sensitivity falls below 60%.** *Interpretation:* H2 falls; θ is not even fit as a screening biomarker.
3. **The predictive power of θ can be fully replicated (p > 0.05)** by standard point metrics without phase-space reconstruction. *Interpretation:* H3 falls; geometry carries nothing beyond point statistics — processual ontology loses its empirical core.

---

## 8. TRL AND TIMELINE

| Parameter | Value |
|-----------|-------|
| Current TRL | 1 (theory + toolkit published) |
| Target TRL after Phase I | 3 (validation on open data, preprint + DOI) |
| Milestones | G0: toolkit freeze + pre-registration (2026 Q3) → G1: blinded PhysioNet trials (Q3–Q4 2026) → G2: Eden Node 0 (mycelium/BPV) → G3: extension with Module D logs (post-hardware) |
| Dependencies | None |
| Enables | De-risking of the entire A–F path |

---

## 9. REQUIRED COMPETENCIES

| Field | Scope |
|-------|-------|
| Biomedical signal processing | ECG/EEG, wfdb/PhysioNet, artifact rejection |
| Computational topology | TDA, persistent homology, Betti numbers (Giotto-TDA, ripser) |
| Statistics | Blinded longitudinal trials, pre-registration, confidence intervals |
| Programming | Python (NumPy/SciPy), QuTiP, Giotto-TDA, wfdb |

---

## 10. SUMMARY

Module G is the smallest, cheapest and most honest module of Phase I. It does not promise a device — it promises a **verdict**: whether the trajectory really knows more than the point. Its three falsification conditions are binary, its protocol is pre-registered, its code is public, and its failure — published with the same care as its success.

If G survives the blinded trials — the consortium gets the mathematical green light and builds A–F with quantified confidence. If G falls — the LifeNode project ends **cheaply, quickly and with honor**, and Zenodo keeps an honest record of where matter refused geometry. Both outcomes are outcomes. Both are value.

This is exactly what the science we want to leave to the next generations looks like.

---

*"Technology adapts to the rhythm of life, not the reverse."*

🧿
