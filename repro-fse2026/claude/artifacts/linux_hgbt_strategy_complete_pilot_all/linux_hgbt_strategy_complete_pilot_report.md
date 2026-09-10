# Linux HGBT strategy-complete pilot

## Scope

This is a one-budget, one-seed pilot over all seven Linux releases. It restores `coverage`, `diversity`, and `uncertainty` for the all-feature `sk-hgbt-log` Linux setting. It is useful for checking whether the narrow HGBT Linux panel missed important decision behavior, but it is not a replacement for the full multi-budget, multi-seed Linux experiment.

## Strategy-level summary

| Strategy | Median cost/random | Cost range | Median MRE | MRE range | Median %cost/%n |
|---|---:|---:|---:|---:|---:|
| `balanced` | 1.01 | 0.981-1.16 | 0.231 | 0.14-0.267 | 1.03 |
| `cheapOracle` | 0.217 | 0.206-0.274 | 0.62 | 0.604-0.663 | 0.224 |
| `coverage` | 1 | 0.993-1.05 | 0.232 | 0.14-0.289 | 1.02 |
| `diversity` | 1.32 | 1.15-1.62 | 0.62 | 0.47-0.756 | 1.32 |
| `expensiveOracle` | 8.27 | 6.87-11.2 | 9.62 | 7.68-10.3 | 8.26 |
| `random` | 1 | 1-1 | 0.233 | 0.142-0.249 | 0.995 |
| `uncertainty` | 0.519 | 0.434-0.644 | 0.322 | 0.173-0.381 | 0.497 |

## Decision-level summary

Across releases and lambdas, top-1 recommendations change in 45/49 count-cost versus empirical-cost comparisons. The Pareto set changes in 7/7 releases.

| Release | Top-1 flips | Count top-1 mode | Empirical top-1 mode | Pareto Jaccard | Empirical Pareto |
|---|---:|---|---|---:|---|
| `413` | 7/7 | `coverage_n01000` | `uncertainty_n01000` | 0.25 | `balanced_n01000, cheapOracle_n01000, coverage_n01000, uncertainty_n01000` |
| `415` | 7/7 | `coverage_n00425` | `cheapOracle_n00425` | 0.2 | `balanced_n00425, cheapOracle_n00425, coverage_n00425, random_n00425, uncertainty_n00425` |
| `420` | 7/7 | `balanced_n00254` | `cheapOracle_n00254` | 0.25 | `balanced_n00254, cheapOracle_n00254, random_n00254, uncertainty_n00254` |
| `500` | 6/7 | `random_n00215` | `uncertainty_n00215` | 0.333 | `cheapOracle_n00215, random_n00215, uncertainty_n00215` |
| `504` | 6/7 | `coverage_n00279` | `uncertainty_n00279` | 0.333 | `cheapOracle_n00279, coverage_n00279, uncertainty_n00279` |
| `507` | 6/7 | `balanced_n00218` | `uncertainty_n00218` | 0.333 | `balanced_n00218, cheapOracle_n00218, uncertainty_n00218` |
| `508` | 6/7 | `coverage_n00237` | `uncertainty_n00237` | 0.25 | `cheapOracle_n00237, coverage_n00237, random_n00237, uncertainty_n00237` |

## Interpretation

The best single observed MRE is `coverage` on Linux 413 with MRE 0.14. The cheapest observed strategy is `cheapOracle` on Linux 507 at 0.206x random cost, but its MRE is 0.657.

`coverage` is competitive with `random` and `balanced` on MRE at this budget, and it is often the count-cost winner. `uncertainty` often buys lower empirical cost, but with worse MRE in this pilot. `diversity` is consistently costly and inaccurate here. The immediate paper implication is that the previous all-feature HGBT Linux run should not be presented as a complete strategy-panel result: restoring the omitted strategies changes RQ3/RQ4 decision evidence even at one budget.
