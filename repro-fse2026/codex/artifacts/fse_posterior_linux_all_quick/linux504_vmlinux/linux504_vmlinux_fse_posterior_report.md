# linux504_vmlinux FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 25847 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n00258` (risk 0, %cost 0.02365).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n00258` (omega_cost 0.001631, %cost 0.02365).

Empirical cost/confidence Pareto front:

- `balanced_n00258`: posterior area 0.9963, risk 0.00207, %cost 0.01018, omega_cost 0.0001154
- `diversity_n00258`: posterior area 1, risk 0, %cost 0.02365, omega_cost 0.001631
- `uncertainty_n00258`: posterior area 0.9828, risk 0.0172, %cost 0.007955, omega_cost -0.01238
- `coverage_n00258`: posterior area 0.9976, risk 0.00236, %cost 0.0103, omega_cost 0.001367
- `cheapOracle_n00258`: posterior area 0.009982, risk 0.99, %cost 0.002092, omega_cost -0.9722
- `balanced_n00517`: posterior area 0.9981, risk 0.001625, %cost 0.02016, omega_cost -3.62e-06
- `SRSSampling_n00517`: posterior area 0.9986, risk 0.001045, %cost 0.02108, omega_cost 0.0004281
- `cheapOracle_n00517`: posterior area 0.02, risk 0.98, %cost 0.004501, omega_cost -0.9715

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `linux504_vmlinux:n00258` | `inconclusive` | 10.49 | 0.163 | large (0.1395) | median risks: random=0.00267, balanced=0.00207, diversity=0, uncertainty=0.0172, coverage=0.00236, SRSSampling=0.002592, cheapOracle=0.99, expensiveOracle=0; spread=0.99 |
| `FSE1` | `linux504_vmlinux:n00517` | `supports` | 16.51 | 0.0208 | large (0.3805) | median risks: random=0.001896, balanced=0.001625, diversity=0, uncertainty=0.003714, coverage=0.005552, SRSSampling=0.001045, cheapOracle=0.98, expensiveOracle=0; spread=0.98 |
| `FSE2` | `linux504_vmlinux:n00258` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n00258; best cost-normalized=diversity_n00258 |
| `FSE3` | `linux504_vmlinux:n00258` | `refutes` | 0 |  | moderate (0.001212) | best cost-normalized=diversity_n00258; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `linux504_vmlinux:n00258` | `supports` | 0.1667 |  | large frontier change (5) | count front=diversity_n00258,expensiveOracle_n00258; empirical front=balanced_n00258,cheapOracle_n00258,coverage_n00258,diversity_n00258,uncertainty_n00258 |
| `FSE5` | `linux504_vmlinux:n00258` | `inconclusive` | 20.5 | 0.958 | small (0.41) | A12<0.5 means SRS risks tend to be lower; median SRS=0.002592, median random=0.00267 |
| `FSE6` | `linux504_vmlinux:n00258` | `inconclusive` | 8 | 0.114 | large (0.84) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01248, median random=0.01032 |
| `FSE2` | `linux504_vmlinux:n00517` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n00517; best cost-normalized=diversity_n00517 |
| `FSE3` | `linux504_vmlinux:n00517` | `refutes` | 0 |  | small (0.0005018) | best cost-normalized=diversity_n00517; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `linux504_vmlinux:n00517` | `supports` | 0.1429 |  | large frontier change (6) | count front=diversity_n00517,expensiveOracle_n00517; empirical front=SRSSampling_n00517,balanced_n00517,cheapOracle_n00517,diversity_n00517,random_n00517,uncertainty_n00517 |
| `FSE5` | `linux504_vmlinux:n00517` | `inconclusive` | 19 | 0.814 | small (0.38) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001045, median random=0.001896 |
| `FSE6` | `linux504_vmlinux:n00517` | `supports` | 3 | 0.0282 | large (0.94) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02108, median random=0.01992 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n00258` | 258 | 0.009982 | 0.01032 | 0.00267 | 0.9962 | 9.33e-05 | -3.064e-05 |
| `balanced_n00258` | 258 | 0.009982 | 0.01018 | 0.00207 | 0.9963 | 0.00019 | 0.0001154 |
| `diversity_n00258` | 258 | 0.009982 | 0.02365 | 0 | 1 | 0.003846 | 0.001631 |
| `uncertainty_n00258` | 258 | 0.009982 | 0.007955 | 0.0172 | 0.9828 | -0.01335 | -0.01238 |
| `coverage_n00258` | 258 | 0.009982 | 0.0103 | 0.00236 | 0.9976 | 0.001486 | 0.001367 |
| `SRSSampling_n00258` | 258 | 0.009982 | 0.01248 | 0.002592 | 0.9973 | 0.001184 | 0.0004186 |
| `cheapOracle_n00258` | 258 | 0.009982 | 0.002092 | 0.99 | 0.009982 | -0.9862 | -0.9722 |
| `expensiveOracle_n00258` | 258 | 0.009982 | 0.08427 | 0 | 1 | 0.003846 | 0.0004587 |
| `random_n00517` | 517 | 0.02 | 0.01992 | 0.001896 | 0.9976 | -0.0004526 | -0.0004449 |
| `balanced_n00517` | 517 | 0.02 | 0.02016 | 0.001625 | 0.9981 | 1.167e-05 | -3.62e-06 |
| `diversity_n00517` | 517 | 0.02 | 0.04153 | 0 | 1 | 0.001927 | 0.0009299 |
| `uncertainty_n00517` | 517 | 0.02 | 0.01624 | 0.003714 | 0.9963 | -0.001787 | -0.001343 |
| `coverage_n00517` | 517 | 0.02 | 0.01933 | 0.005552 | 0.9944 | -0.003625 | -0.003558 |
| `SRSSampling_n00517` | 517 | 0.02 | 0.02108 | 0.001045 | 0.9986 | 0.0005262 | 0.0004281 |
| `cheapOracle_n00517` | 517 | 0.02 | 0.004501 | 0.98 | 0.02 | -0.9781 | -0.9715 |
| `expensiveOracle_n00517` | 517 | 0.02 | 0.1325 | 0 | 1 | 0.001927 | 0.0002917 |
