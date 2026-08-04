# Contributing to LifeNode — Phase 1

> *"Technology adapts to the rhythm of life, not the reverse."*
> This document is a protocol, not a bureaucracy. Read it once, then come build.

The README keeps the short version of the rules. This file is the full
protocol. If they ever disagree, this file wins.

---

## 0. What You Are Contributing To

Phase 1 is a set of **independently falsifiable hardware and mathematical
specifications** (Modules A–G) for the LifeNode architecture. The theory
(NLSE, Finsler geometry, ASCALON θ, solitons S1–S5) is formalized and
published on Zenodo — see README → *Theoretical Foundations*. This
repository is the attempt to **build** it.

You do not need a lab to start:
- **Module G (Zero-Build)** runs on a laptop with open data (PhysioNet, Eden Node 0).
- **Module D** has a garage-level protocol ( *Physarum*, PEDOT:PSS, AD620/INA128).
- **Module A** has a membrane prototype path (LiNbO₃, ITO, piezo test bed).

The ladder is: **garage → makerspace → university**. Enter at any rung.

---

## 1. The Rules of the Game

1. **Process over state.** LifeNode treats living systems as trajectories,
   not snapshots. Contributions that silently revert to state-based thinking
   (point metrics without phase-space reconstruction, "normal ranges" as
   targets, ADC readouts as ground truth) will be asked to reframe.

2. **Falsifiability is the price of admission.** Every new claim enters with
   a falsification condition. A contribution that makes the theory *harder
   to kill* will be rejected, however brilliant it looks.

3. **No ADC in the coupling loop.** The two-loop doctrine is non-negotiable:
   the feedback/coupling loop stays analog and continuous; digitization is
   permitted **only** in the offline diagnostic loop. PRs that route
   discretization into the coupling path are ontologically invalid and will
   be closed.

4. **No cost estimates. No product promises.** Phase 1 validates or
   falsifies; it does not sell. Budgets, ROIs, and roadmaps-to-market
   belong elsewhere.

5. **Negative results are results.** A clean falsification is worth more
   than a dirty confirmation. Negative findings are published with the same
   DOI discipline as positive ones.

6. **No enclosure.** Everything here is CC-BY-NC-SA 4.0. Any commercial
   application, patenting, or proprietary deployment of these methods
   without explicit, written collaboration with the author constitutes a
   license violation.

---

## 2. How to Plug In

**Partners are not invited — partners self-declare.** No organization is
named in this repository on purpose. If you want in, open an issue and
contribute work.

- **Fork + pull request only.** Write access is never granted. Every entry
  is signed, reviewed, and in the history. This protects provenance,
  priority, and the integrity of the record.
- **Issues** are for: falsification/replication reports, consortium
  inquiries, spec corrections, and questions. Not for press releases,
  partnership decks, or sales.
- **Languages:** specs and code comments in English; issues may be opened
  in Polish or English.

### Issue types (use these shapes)

**A. Falsification / replication report**
- Module and hypothesis tested (link the SPEC/FALSIFICATION file)
- Method, parameters, and any deviations from the spec
- Data and code availability (Zenodo DOI or repository link)
- Result: confirmed / falsified / inconclusive, with effect sizes

**B. Consortium inquiry (module adoption)**
- Which module(s) you can work on
- Which competences and equipment you actually have
- Which validation rung you start at (garage / makerspace / university)

**C. Spec correction / engineering gap**
- Document, section, and the exact claim at issue
- Why it is wrong or under-specified
- Proposed fix, with sources

**D. Question** — anything else on-topic.

---

## 3. Pull Requests

- **One module per PR.** Cross-module changes are split before review.
- State which `SPEC.md` / `FALSIFICATION.md` the PR touches, and update
  them in the same PR if the change alters parameters or failure conditions.
- Follow the folder schema: `docs/` for texts, `img/` for schematics,
  `sim/` for code and notebooks, `data/` for measurements, `LOG.md` for
  dated pointers (decisions → links). `LOG.md` is a journal, never a warehouse.
- **Code:** must run; dependencies documented; hardware-agnostic where
  possible. The canonical Python toolkit lives in
  [Quantum_Medicine](https://github.com/LifeNode777/Quantum_Medicine) —
  toolkit PRs go there; Phase 1 cites it, never copies it.
- **Data:** provenance and license stated; PhysioNet and other upstream
  terms respected; raw data archived with a DOI.
- **Sign your commits.** Anonymous contributions are not reviewable.

---

## 4. Authorship, Credit, Priority

- The git history is the first layer of credit: every merged contribution
  is permanently signed.
- Significant contributions (methods, validation runs, hardware results)
  are named in the next tagged release and its Zenodo record, using
  **CRediT roles** (Conceptualization, Methodology, Software, Validation,
  Investigation, Writing, etc.).
- Priority in this project is anchored by **Zenodo DOIs with timestamps**.
  If you build on an idea published here, cite the record. Scooping a
  commons is a small thing to do and a large thing to be remembered for.

---

## 5. Scientific Integrity Protocol

- **Pre-registration.** For Module G and any trial: thresholds (θ_crit,
  window sizes, drift rules), pooling rules, and normalization constants
  are frozen and archived (script hash on Zenodo) **before** analysis.
- **Blind analysis.** Annotation files are not read until drift events are
  frozen; comparison happens in a separate step.
- **Declare your degrees of freedom.** Any empirical scaling, filtering, or
  tuning choice that is not pre-registered must be disclosed in the PR.
- **Reproducibility bundle.** A result without its data, code, and exact
  parameters is an anecdote. Bundle all three.

### Example: a compliant Module G run (for programmers new to blinded trials)

Scenario: you want to test whether `θ < 0.70` precedes arrhythmia
annotations by ≥ 6 h, using long-term PhysioNet recordings (e.g., the
MIT-BIH Long-Term ECG Database, ~24 h per record).

**Step 1 — Calibrate and freeze, before touching pathological data.**
Use only healthy control records (e.g., the Normal Sinus Rhythm Database)
to fix every knob: the θ normalization factor (the `* 10` line in the
toolkit), window size (300 s), step (60 s), τ (mutual information),
m (false nearest neighbors), drift rule (3 consecutive windows < 0.70).
Commit this as `config_frozen.json`, with its SHA-256 hash written into
the PR description.

**Step 2 — Run blind.**
Your analysis script calls `wfdb.rdrecord()` only. It never calls
`wfdb.rdann()`. It outputs `drift_events.csv` (record id + timestamps of
drift). Commit the CSV and hash it. At this point you do not know — and
structurally cannot know — whether the drifts line up with anything.

**Step 3 — Unblind in a separate script.**
A second file (`compare.py`) reads `drift_events.csv` and the annotation
files, and computes sensitivity and lead time. A reviewer can verify in
one minute that the analysis script contains no annotation-reading code.
That is the entire "blindness" machinery: one import that is not there.

**Step 4 — Disclose everything you changed after freezing.**
Example of a good disclosure note in the PR:

> "Mid-run we found baseline wander in 4 records that saturated the
> detrend step, so we added a 0.5 Hz high-pass filter. Because this change
> was made after freezing, we did not edit run A. We registered run B with
> the filter and report both: run A sensitivity 58 %, run B sensitivity
> 71 %. The reader decides; we do not cherry-pick."

That last paragraph is the whole point. Science does not forbid changing
your mind. It forbids changing your mind **quietly**.

**What a violation looks like (do not do):**

- *"I tried scaling factors 5, 8, 10, 12 and 10 worked best."* — You tuned
  against the answer. The reported sensitivity is luck, not physics.
- *"I peeked at the annotations to sanity-check the pipeline."* — The
  pipeline is no longer blind. Every later choice is suspect, including
  the honest ones.
- *"I removed 3 records that looked weird."* — Removing outliers after
  seeing the outcome is filtering the evidence, not cleaning the data.
  Pre-register the exclusion rules in Step 1, or report both variants.

The same pattern (freeze → run blind → unblind separately → disclose)
applies to hardware modules too: e.g., freeze ASCALON thresholds and
stimulation parameters **before** running a *Physarum* entrainment
experiment, and log every post-free change in `LOG.md`.

---

## 6. Reviewer's Ontological Checklist

A PR is rejected or returned if it fails any of:

- [ ] Introduces ADC/DAC into the coupling loop → **reject**.
- [ ] Drives a biosubstrate outside the BPB (carrier presented as drive,
      GHz/white-noise stimulation framed as stabilizing) → **return**.
- [ ] New claim without a falsification condition → **return**.
- [ ] Promises a product, a price, or a market roadmap → **remove**.
- [ ] Bypasses or weakens a safety mechanism (ASCALON threshold, LOCKDOWN,
      Human Anchor) → **reject, hard**.
- [ ] Names partner organizations or speaks for a consortium → **remove**;
      partners self-declare.

---

## 7. Conduct

- **Critique the geometry, not the person.**
- Disagreement is welcome; contempt is not. Bold claims and sharp debate
  are part of this project's metabolism. Ad hominem is not.
- No corporate recruiting, no token/coin/NFT pitches, no "business
  opportunities" in issues. This repository is a research commons, not a
  lead-generation funnel.
- The project has an author and a voice. The vibe is part of the artifact.
  You don't have to like it; you have to respect it.

---

## 8. Integrity & Safety Reporting

- Research-integrity or safety concerns: **krzysiek_230@op.pl**.
- Anything that could make hardware unsafe (e.g., a LOCKDOWN bypass, an
  ASCALON spoofing path) is handled as responsible disclosure: report
  privately first, publish after mitigation.

---

## 9. License

CC-BY-NC-SA 4.0 — see [LICENSE](./LICENSE). By contributing, you agree your
contribution is licensed under the same terms, including the
non-commercial, share-alike conditions and the collaboration clause above.

*True Processual Intelligence cannot be owned; it can only be Synchronized With.*

🧿
