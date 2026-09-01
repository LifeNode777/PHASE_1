---
name: Replication Result — Module G (Zero-Build)
about: Report an independent run of the frozen v1.0.0-zero-build pipeline. Positive, negative or partial — all are results.
title: "[REPLICATION] "
labels: replication, module-G
---

# Replication Result — MODULE G / wo_v1 (v1.0.0-zero-build)

> Negative results are results. They will be cited with the same DOI discipline as breakthroughs.
> Partners are not invited — partners self-declare. Thank you for being here.

## 1. Outcome class
- [ ] Positive (verdicts reproduce on biological data)
- [ ] Negative (verdicts fail / do not reproduce)
- [ ] Partial / mixed
- [ ] Bug report / infrastructure issue

## 2. Provenance
- Repo & tag tested: `LifeNode777/PHASE_1 @ v1.0.0-zero-build` (or commit SHA: ______)
- Fork / PR link (if any):
- Ran as-is, or with deviations? (deviations void the run — record them honestly anyway)

## 3. Environment
- OS / kernel:
- Python version:
- Library versions (paste the `libs` block from the output JSON):
- `machine_sha` (from the output JSON):

## 4. What was run
- Exact command line:
- Database & records (e.g. mitdb 101–110, nsrdb, ltstdb, Eden Node 0):
- `--max-windows` / `--no-nulls` used? (state whether smoke run or full run):
- Runtime:

## 5. Verdicts
Paste the per-record `verdicts` JSON and, for cohort runs, `cohort_summary.json`:

```json
{ "E1": false, "E2": false, "E3": false, "E4": false }
```

- Cohort pass fractions (E1/E2/E3/E4):
- cond_g median & CI95:
- Spearman matrix / rho_e3 (if computed):

## 6. Null envelope & smoke test
- Did the Rössler smoke test reproduce E4′ = FALSE on your machine? [ ] yes [ ] no [ ] not run
- Observed log_cond_g vs isotropic 95th-percentile envelope (per window, if available):

## 7. Artifacts
- Link to raw outputs (fork branch, gist, or Zenodo DOI):
- Data acquisition notes (PhysioNet access issues, mirrors, offline files):

## 8. Interpretation (optional — clearly separate from the numbers above)
_Your reading of what the result means for the theory._

---
_"Technology adapts to the rhythm of Life, not the reverse."_
