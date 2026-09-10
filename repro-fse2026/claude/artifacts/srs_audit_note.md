# Phase 1: SRS Audit Against the FSE 2026 Artifact

Date: 2026-07-02.
Reference: `SRS-sampling.ipynb` from the FSE 2026 artifact
"Risk and Confidence in Performance Bounds of Configuration Sampling
Strategies --- Sources and Data", doi:10.5281/zenodo.19682296
(Weis, Maggio, Siegmund, Apel; paper doi:10.1145/3808147, `references/WMS+26.pdf`).
Audited implementation: `cost_sampling/srs.py` (`srs_indices`).
Audit harness: `scripts/audit_srs_vs_artifact.py` (embeds the notebook's
`SRS_sampling` verbatim; run with `python3.13 scripts/audit_srs_vs_artifact.py`).

## Verdict

`cost_sampling/srs.py` is a **faithful reimplementation** of the artifact's
SRS — not exact artifact reuse, and not a mere approximation. All protocol
constants and control flow match; two deliberate deviations are documented
below and both are conservative for our cost-normalized use.

## Defaults compared

| Aspect | Artifact notebook | `srs_indices` | Match |
|---|---|---|---|
| Step sample size | 25 | 25 (`step_sample_size`) | yes |
| Significance test | Welch's t-test (`ttest_ind`, `equal_var=False`), two-sided | same via SciPy | yes |
| p threshold | 0.05 | 0.05 (`p_threshold`) | yes |
| Target orientation | hardcoded `ascending=False` (max / worst case) | `extreme="max"` default, `min` supported | yes |
| Decision rule | common decisions of two best in the *new* batch; keep if enabled/disabled means differ significantly | identical, on the new batch only | yes |
| Recursion stop | no noteworthy decisions, or <2 new samples | same (iterative form) | yes |
| Random fill to budget | yes (FSE paper footnote) | yes | yes (see deviation 1) |
| Step cap near budget | step reduced to remaining budget | `min(step, remaining)` per iteration | yes |
| Budget > pool | returns whole pool | clamps to pool size | yes |

Notebook quirks that are neutralized rather than reproduced:

- `candidate_decision not in decision_set` in the notebook compares a column
  name against (feature, value) tuples, so it never fires; already-decided
  features are actually excluded by the recursive filtering (empty "disabled"
  group -> NaN p-value -> not noteworthy). `srs_indices` excludes decided
  features explicitly — same outcome, no behavioral difference.
- `if index in nfp` in the notebook is a substring test on the NFP column
  name; in `srs_indices` the target vector is separate from the feature
  matrix, so no feature column can be accidentally skipped.

## Documented deviations

1. **No duplicate configurations.** The artifact's random fill draws from the
   *current-level* measurement pool, which still contains configurations
   already selected in the current call. On a synthetic 3000-config system
   (40 seeds, budget 300), the artifact sampler returned duplicated
   configurations in 14/40 runs (296–300 unique of 300). `srs_indices` fills
   from the not-yet-selected pool and never duplicates. For cost-normalized
   analysis this is the safer convention: duplicates would double-count
   acquisition cost for a configuration measured once.
2. **RNG stream and tie-breaking.** The notebook uses the global NumPy seed
   (`np.random.seed(i)`) through `DataFrame.sample` and an unstable sort;
   `srs_indices` uses `np.random.default_rng` and a stable mergesort. Samples
   are therefore statistically equivalent but not bitwise identical to the
   artifact's CSVs.

## Behavioral equivalence evidence

`scripts/audit_srs_vs_artifact.py`, synthetic system with 3000 configs,
16 features, interaction effects, budget 300, 40 seeds each:

- posterior risk of the sampled max bound: ours 0.00132±0.00248 vs artifact
  0.00113±0.00158; Mann-Whitney U two-sided p = 0.951 — no detectable
  difference between the two implementations.
- both dominate uniform random sampling (ours 0.00132 vs random 0.00366,
  one-sided p = 6.9e-06), consistent with the paper's headline result.

Roadmap smoke checks all pass: exact requested sample size, deterministic
for equal seed, seed-sensitivity, no duplicate indices, `max`/`min`
orientation, clamping when budget exceeds the pool.

## Confirmation in the artifact's shipped data

The duplicate-fill behavior is visible in the artifact's own
`sampledConfigurations_SRSSampling_t2.csv` files: after mapping sampled rows
to unique configurations of the measured universe, the SRS t2 sample is
short of the requested size in 2–42% of the 100 runs per system (unique
sizes: 7z 599–600 of 600, BerkeleyDBC 96–97 of 97, Dune 260–265 of 265,
Hipacc 840–843 of 843, JavaGC 467–468 of 468, LLVM 54–56 of 56, Polly
344–345 of 345; from `posterior_records.csv` of the Phase 2 run). The
deficit is bounded by ~5 configurations, so downstream conclusions are
unaffected, but "SRS returns exactly the requested sample size" holds for
the artifact data only up to these duplicates.

## Artifact protocol facts recorded for Phase 2

From `main.ipynb`/`SRS-sampling.ipynb` cell parameters (systems, dropped
extra-NFP columns, per-system t2 sizes):

| System | NFP | Dropped columns | t2 size |
|---|---|---|---:|
| 7z | Performance | Variable Features, Size | 600 |
| BerkeleyDBC | Performance | (none) | 97 |
| Dune | Performance | Variable Features | 265 |
| Hipacc | Performance | Variable Features | 843 |
| JavaGC | Performance | Variable Features | 468 |
| LLVM | Performance | MainMemory | 56 |
| Polly | Performance | Variable Features, ElapsedTime | 345 |

Fixed-size protocol: 300 samples, 100 repetitions, seeds 1..100 via
`np.random.seed(i)`.
