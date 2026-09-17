# RELAY_STATE.md — MODULE G WORK_ORDER_v1 relay

**Date:** 2026-09-17  
**Branch:** `module-g-wo-v1-grok-fix1`  
**Executor this leg:** Grok (xAI session starting 2026-09-17 ~20:40 UTC)  
**machine_sha:** 7ba7cd84b6d12c5b (sandbox hds-hty012ehbf6e)

## What died
- Previous Grok session (deceased ~2026-09-18, machine_sha unrecoverable).  
  It reached embedding + 8 windows on mitdb/100, fixed Bug 1 locally in memory, diagnosed Bug 2, then the session ended with artefacts only in the chat transcript (no push).

## What survived
- Diagnosis of two reference-implementation bugs (digitize OOB; 1-D velocity vs m-dim embedding space).  
- Confirmation that PhysioNet mitdb download works and the pipeline reaches the metrology stage before crashing.

## What this leg is doing (in order, per human constraints)
1. Confirmed no existing work-order-bug issue on LifeNode777/PHASE_1 (API + web UI empty).  
   → Issue body drafted (see below); cannot open without write credentials.  
2. Local branch `module-g-wo-v1-grok-fix1` created.  
3. Bug 1 fixed (clip digitize indices).  
4. Bug 2 fixed text-compliant (§4.3): SG applied coordinate-wise to embedded trajectory; v, a ∈ ℝ^{N'×m}.  
5. METHODS_NOTES.md cleaned (was corrupted by appended config.py) and deviation rows added.  
6. RELAY_STATE.md written (this file).  
7. **PUSH REQUIRED BEFORE ANY COMPUTE ON 101.**  
   Current sandbox has no GitHub token / write access.  
   Next human or authenticated runner must:  
   - open the issue (body ready)  
   - push this branch  
   - then continue with run on mitdb/101 under the five constraints.

## Draft issue body (for immediate opening)

**Title:**  
`[MODULE G] work-order-bug: reference implementation crashes at metrology (Bug 1 digitize OOB, Bug 2 1D velocity vs m-dim embedding space)`

**Body:**
```
finder = previous session @Grok (deceased 2026-09-18, machine_sha unrecoverable)
executor = current Grok session (machine_sha pending after push)

### Bug 1 – embedding.py → _histogram_mi
np.digitize returns index == bins when value lies exactly on the right edge of the last bin.
→ IndexError: index 64 is out of bounds for axis 0 with size 64

Fix applied on this branch: clip indices to [0, bins-1].

### Bug 2 – pipeline.py + embedding.sg_smooth_and_derivatives + metrology
sg_smooth_and_derivatives was called on the raw 1-D ECG segment.
Resulting velocity/acceleration are 1-D.
metrology.compute_phase_and_bin (and theta_*, anisotropy_proxy, bootstrap_cond_g) expect vectors in the m-dimensional embedding space and call np.linalg.norm(..., axis=1).

This violates WORK_ORDER_v1 §4.3:
“Smooth embedded trajectory with Savitzky–Golay (window 41, poly 3); velocities v and accelerations a from SG derivative coefficients.”

Fix applied on this branch: SG applied independently to each coordinate of the embedded trajectory; v and a now have shape (N', m).

### Log from previous partial run (mitdb/100, max_windows=8)
=== mitdb/100 ===
loaded: 231112 samples, 1805.6 s @ 128.0 Hz
embedding: m=6, τ=22 samples (0.172 s)
windows: 8 (max_windows=8)

### Environment (previous session)
numpy 1.26.4, scipy, wfdb, pandas, sklearn, tqdm (pinned from requirements.txt)

### Next steps on this branch
- Push RELAY_STATE + fixes before any further compute.
- Full single-record run on mitdb/101 (model c, n=100, first 20 accepted windows, blinding, seed 1618) after push.
```

## Status
- Local fixes complete.  
- Waiting for authenticated push + issue creation before any compute on 101 (REGUŁA ZERO).  
- Once pushed, next runner continues from here; cache will be written per-window and pushed.
