# Specification 01 — Phase 1: SRS Audit

Code under audit: `cost_sampling/srs.py`
Reference: the official FSE 2026 artifact SRS implementation (likely
`SRS-sampling.ipynb` or similarly named).
Output: an audit note embedded in the Phase 2–7 reports + optional test module.

See Spec 00 §6 for metric definitions and §11 for terminology.

---

## 1. Goal

Verify that `cost_sampling/srs.py` faithfully matches the FSE artifact behavior
relevant to these experiments, and classify the fidelity level.

## 2. Tasks

1. Locate the official FSE SRS implementation in `$FSE_ROOT`. Record the artifact
   source path and version in the run notes.
2. Compare defaults between `cost_sampling/srs.py` and the artifact:
   - step sample size;
   - Welch t-test usage;
   - p-value threshold;
   - target orientation (`max` / `min`);
   - recursion stop behavior;
   - random-fill behavior (fill to the requested sample size — matches the FSE footnote).
3. Add or run small tests covering:
   - exact sample size returned;
   - deterministic seed behavior;
   - fill-to-budget behavior;
   - no duplicate indices;
   - both `max` and `min` orientation.

## 3. Smoke check (must pass)

```bash
python3 - <<'PY'
import numpy as np
from cost_sampling.srs import srs_indices

rng = np.random.default_rng(0)
X = rng.integers(0, 2, size=(200, 12))
y = X[:, 0] * 10 + X[:, 1] * 3 + rng.normal(size=200)
idx = srs_indices(X, y, 32, rng=123)
print(len(idx), len(set(idx)), idx[:10].tolist())
assert len(idx) == 32
assert len(set(idx)) == 32
PY
```

Expectations: `srs_indices(X, y, k, rng=<int>)` returns exactly `k` indices, all
unique, deterministic for a fixed `rng` seed, valid for both extremes.

## 4. Deliverable

A short note (reused verbatim in every downstream corpus report) stating whether
SRS in this repo is:

- **exact artifact reuse**;
- **faithful reimplementation**; or
- **approximate adaptation requiring caveats** (list the caveats).

## 5. Libraries

`numpy`; `scipy.stats` (Welch t-test); the repo module `cost_sampling.srs`.
No new dependencies.
