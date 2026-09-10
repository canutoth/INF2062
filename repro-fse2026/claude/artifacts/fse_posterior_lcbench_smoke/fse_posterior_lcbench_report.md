# FSE 2026 posterior-risk revisit on LCBench

## Scope

This applies the FSE posterior-risk/posterior-confidence framework to LCBench measured pools.
Each OpenML dataset is a distinct reference universe, and each hyperparameter configuration is a sampled object.
The result is reference-relative posterior risk over the measured LCBench pool, not a configurable-software claim.

Source JSON: `/private/tmp/lcbench/data_2k_lw.json`.
Target column: `final_val_accuracy`. Cost column: `time_total`.
Datasets analyzed: `APSFailure, Amazon_employee_access, Australian, Fashion-MNIST, KDDCup09_appetency, MiniBooNE`.
SRS generated: `True` with `10` seeds per dataset/level.
Diagnostic oracles included: `True`.

## Headline

Strategy posterior-risk distributions differ in 5/12 dataset-level scopes.
SRS is the best empirical-cost-normalized recommendation in 1/12 scopes and appears on the empirical cost/confidence Pareto frontier in 5/12 scopes.
Cost-normalization changes the top recommendation in 9/12 scopes and changes the confidence Pareto frontier in 12/12 scopes.
SRS has lower posterior risk than random in 0/12 scopes; its empirical acquisition cost differs from random in 0/12 scopes.

Best empirical-cost-normalized pairs:

- `pilotCost_n16`: 2/12
- `balanced_n16`: 2/12
- `cheapOracle_n8`: 2/12
- `balanced_n8`: 1/12
- `SRSSampling_n8`: 1/12
- `cheapOracle_n16`: 1/12
- `pairwise_n8`: 1/12
- `diversity_n8`: 1/12
- `diversity_n16`: 1/12

## Dataset-Level Summary

| Dataset | Level | n | Best cost pair | SRS best? | SRS on front? | Jaccard |
|---|---|---:|---|---:|---:|---:|
| `APSFailure` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.2 |
| `APSFailure` | `n16` | 16 | `pilotCost_n16` | 0 | 0 | 0.1667 |
| `Amazon_employee_access` | `n8` | 8 | `SRSSampling_n8` | 1 | 1 | 0.125 |
| `Amazon_employee_access` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.125 |
| `Australian` | `n8` | 8 | `cheapOracle_n8` | 0 | 0 | 0.5 |
| `Australian` | `n16` | 16 | `cheapOracle_n16` | 0 | 0 | 0.25 |
| `Fashion-MNIST` | `n8` | 8 | `cheapOracle_n8` | 0 | 0 | 0.5 |
| `Fashion-MNIST` | `n16` | 16 | `pilotCost_n16` | 0 | 0 | 0.3333 |
| `KDDCup09_appetency` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.1429 |
| `KDDCup09_appetency` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.1667 |
| `MiniBooNE` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.2 |
| `MiniBooNE` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.2 |

## Budget Scaling

| Strategy | Risk non-increasing | Posterior area non-decreasing | Omega(size) >= 0 all datasets | Omega(cost) >= 0 all datasets |
|---|---:|---:|---:|---:|
| `random` | 6/6 | 5/6 | 2/6 | 3/6 |
| `balanced` | 6/6 | 6/6 | 6/6 | 5/6 |
| `diversity` | 6/6 | 6/6 | 6/6 | 5/6 |
| `SRSSampling` | 6/6 | 5/6 | 3/6 | 4/6 |
| `pairwise` | 6/6 | 6/6 | 5/6 | 5/6 |
| `pilotCost` | 6/6 | 6/6 | 1/6 | 3/6 |
| `cheapOracle` | 6/6 | 6/6 | 1/6 | 2/6 |
| `expensiveOracle` | 6/6 | 6/6 | 5/6 | 4/6 |

For SRS, posterior risk is non-increasing in 6/6 datasets and posterior area is non-decreasing in 5/6 datasets.

## Applicability

LCBench is applicable as an external-validation dataset for reference-relative posterior risk. It should not be merged directly with configurable-software systems: the sampled objects are ML hyperparameter configurations, and the contexts are OpenML datasets.

## Output Files

- `posterior_lcbench_dataset_summary.csv`: dataset-level posterior/cost decisions.
- `posterior_lcbench_budget_trends.csv`: budget-scaling trends per strategy.
- `posterior_hypothesis_tests.csv`: per-dataset/level FSE-style tests.
- per-dataset folders with CSVs, reports, and figures.
