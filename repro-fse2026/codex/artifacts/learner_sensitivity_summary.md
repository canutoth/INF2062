# Learner-sensitivity of the cost-vs-count significance (ridge / RF / CART)

Date: 2026-06-27. Addresses the **learning-algorithm sensitivity** threat: does the
cost-induced re-ranking depend on the prediction model? Computed via the matched
`kw_cost_vs_size.py --all-metrics` path (one cell-build per (family, learner) →
KW + flip + Pareto), for the **five non-Linux families** under three learners.
(Linux is handled separately — it had a feature-truncation bug; see handoff §10/C16.)
Generated families use `--seeds 10`; replications use the archives' ~100 real runs.
Reproduce: `scripts/stream_b_others.sh` (+ `learner_sensitivity_allmetrics.sh`).

## Headline — KW top-group change % (the cost-effect)
| family | ridge | RF | CART |
|---|---|---|---|
| ICSE19  | 9/21 = 43% | 11/21 = 52% | 9/21 = 43% |
| ICPE20 x264 | 28/51 = 55% | 31/51 = 61% | 30/51 = 59% |
| ENERGY  | 61/112 = 54% | 70/112 = 62% | 58/112 = 52% |
| LCBENCH | 149/350 = 43% | 175/350 = 50% | 150/350 = 43% |
| WORKLOAD | 398/846 = 47% | 401/846 = 47% | 424/846 = 50% |

**Every family × every learner lands at 43–62%.** The cost-induced change of the
statistically tied-best set is **learner-robust** — ridge, random forest, and CART all
agree. RF tends slightly higher; ridge/CART are close. **Threat neutralized.**

## Pareto choice-set — robustly differs (p_differ ≥ .95)
| family | ridge | RF | CART |
|---|---|---|---|
| ICSE19  | 6/7 | 7/7 | 7/7 |
| ICPE20 x264 | 16/17 | 17/17 | 17/17 |
| ENERGY  | 13/14 | 14/14 | 13/14 |
| LCBENCH | 32/35 | 35/35 | 32/35 |
| WORKLOAD | 62/93 | 75/93 | 77/93 |

Robust under all three; **often stronger** under RF/CART (e.g. workload 62→75–77).

## Top-1 flip (median agg) — significant / total
Mostly noise under all three learners (0–12 sig out of 7–163). The learner does not
rescue the flip — consistent with it being the weakest, near-tie metric.

## Fit quality (median MRE) — sanity check
| family | ridge | RF | CART |
|---|---|---|---|
| ICSE19  | — | 17.5% | 14.9% |
| ICPE20 x264 | — | 4.4% | 2.1% |
| ENERGY  | — | 21.9% | 15.7% |
| LCBENCH | — | 12.8% | 12.7% |
| WORKLOAD | 24.0% | 26.5% | 17.8% |
(ridge MRE mostly blank — those baseline runs predate the `median_mre` column.)
None catastrophic (unlike Linux-truncation ~30%). The higher values (energy, workload)
are inherently-hard systems (kanzi, lrzip), not learner artifacts. **The cost-effect
holds even where a learner fits less well** (e.g. energy RF 22% MRE → 62% top-group
change) — a *stronger* robustness statement than "the effect needs a good learner."

## Verdict
The cost-vs-count significance is **robust to the learning algorithm**: across ridge,
RF, and CART, the KW top-group changes 43–62% and the Pareto choice-set robustly
differs in nearly every scenario, while the top-1 flip stays noise. This directly
addresses the learner-sensitivity threat for the non-Linux families. GBT/HGBT were
omitted for the KW sweep (≈24× slower per fit — infeasible for the per-run fits);
RF + CART + ridge already span linear, bagged-tree, and single-tree model classes.

## Data files
`artifacts/lsens_<family>_{ridge,rf,cart}.csv` (KW + `best_mre`/`median_mre`),
`_flip.csv`, `_pareto.csv`. families = icse19, icpe20, energy, lcbench, workload.
