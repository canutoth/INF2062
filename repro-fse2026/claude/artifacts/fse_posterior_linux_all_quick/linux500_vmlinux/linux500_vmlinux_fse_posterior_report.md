# linux500_vmlinux FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 19952 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `expensiveOracle_n00200` (risk 0, %cost 0.08478).

Best integrated confidence after normalizing the prior baseline by empirical cost: `uncertainty_n00200` (omega_cost 0.00415, %cost 0.008764).

Empirical cost/confidence Pareto front:

- `diversity_n00200`: posterior area 0.9999, risk 5.012e-05, %cost 0.01977, omega_cost 0.002472
- `uncertainty_n00200`: posterior area 0.9985, risk 0.001504, %cost 0.008764, omega_cost 0.00415
- `cheapOracle_n00200`: posterior area 0.01002, risk 0.99, %cost 0.002234, omega_cost -0.9685
- `expensiveOracle_n00200`: posterior area 1, risk 0, %cost 0.08478, omega_cost 0.0005905
- `diversity_n00399`: posterior area 1, risk 2.506e-05, %cost 0.04287, omega_cost 0.001141
- `cheapOracle_n00399`: posterior area 0.02, risk 0.98, %cost 0.004751, omega_cost -0.9697

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `linux500_vmlinux:n00200` | `supports` | 16.88 | 0.0182 | large (0.3952) | median risks: random=0.005062, balanced=0.002757, diversity=5.012e-05, uncertainty=0.001504, coverage=0.004786, SRSSampling=0.001002, cheapOracle=0.99, expensiveOracle=0; spread=0.99 |
| `FSE1` | `linux500_vmlinux:n00399` | `supports` | 21.63 | 0.00294 | large (0.5852) | median risks: random=0.002506, balanced=0.002306, diversity=2.506e-05, uncertainty=0.01554, coverage=0.001579, SRSSampling=0.0002506, cheapOracle=0.98, expensiveOracle=0; spread=0.98 |
| `FSE2` | `linux500_vmlinux:n00200` | `supports` | 1 |  | changed (0.00356) | best size-normalized=expensiveOracle_n00200; best cost-normalized=uncertainty_n00200 |
| `FSE3` | `linux500_vmlinux:n00200` | `refutes` | 0 |  | moderate (0.00147) | best cost-normalized=uncertainty_n00200; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `linux500_vmlinux:n00200` | `supports` | 0.25 |  | large frontier change (3) | count front=expensiveOracle_n00200; empirical front=cheapOracle_n00200,diversity_n00200,expensiveOracle_n00200,uncertainty_n00200 |
| `FSE5` | `linux500_vmlinux:n00200` | `inconclusive` | 6 | 0.0677 | large (0.12) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001002, median random=0.005062 |
| `FSE6` | `linux500_vmlinux:n00200` | `supports` | 3 | 0.0282 | large (0.94) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01128, median random=0.009838 |
| `FSE2` | `linux500_vmlinux:n00399` | `supports` | 1 |  | changed (0.00145) | best size-normalized=expensiveOracle_n00399; best cost-normalized=SRSSampling_n00399 |
| `FSE3` | `linux500_vmlinux:n00399` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_n00399; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `linux500_vmlinux:n00399` | `supports` | 0.1429 |  | large frontier change (6) | count front=expensiveOracle_n00399; empirical front=SRSSampling_n00399,balanced_n00399,cheapOracle_n00399,coverage_n00399,diversity_n00399,expensiveOracle_n00399,uncertainty_n00399 |
| `FSE5` | `linux500_vmlinux:n00399` | `supports` | 1 | 0.0147 | large (0.02) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0002506, median random=0.002506 |
| `FSE6` | `linux500_vmlinux:n00399` | `inconclusive` | 7 | 0.0883 | large (0.86) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02234, median random=0.0205 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n00200` | 200 | 0.01002 | 0.009838 | 0.005062 | 0.9934 | -0.00162 | -0.001527 |
| `balanced_n00200` | 200 | 0.01002 | 0.01056 | 0.002757 | 0.997 | 0.001928 | 0.001679 |
| `diversity_n00200` | 200 | 0.01002 | 0.01977 | 5.012e-05 | 0.9999 | 0.0049 | 0.002472 |
| `uncertainty_n00200` | 200 | 0.01002 | 0.008764 | 0.001504 | 0.9985 | 0.003447 | 0.00415 |
| `coverage_n00200` | 200 | 0.01002 | 0.009547 | 0.004786 | 0.9952 | 0.000164 | 0.0004091 |
| `SRSSampling_n00200` | 200 | 0.01002 | 0.01128 | 0.001002 | 0.9983 | 0.003226 | 0.002681 |
| `cheapOracle_n00200` | 200 | 0.01002 | 0.002234 | 0.99 | 0.01002 | -0.985 | -0.9685 |
| `expensiveOracle_n00200` | 200 | 0.01002 | 0.08478 | 0 | 1 | 0.00495 | 0.0005905 |
| `random_n00399` | 399 | 0.02 | 0.0205 | 0.002506 | 0.9972 | -0.0002629 | -0.0003232 |
| `balanced_n00399` | 399 | 0.02 | 0.02004 | 0.002306 | 0.9973 | -0.0001877 | -0.000193 |
| `diversity_n00399` | 399 | 0.02 | 0.04287 | 2.506e-05 | 1 | 0.002469 | 0.001141 |
| `uncertainty_n00399` | 399 | 0.02 | 0.01773 | 0.01554 | 0.9845 | -0.01304 | -0.01273 |
| `coverage_n00399` | 399 | 0.02 | 0.02042 | 0.001579 | 0.9984 | 0.000915 | 0.0008637 |
| `SRSSampling_n00399` | 399 | 0.02 | 0.02234 | 0.0002506 | 0.9996 | 0.002083 | 0.001822 |
| `cheapOracle_n00399` | 399 | 0.02 | 0.004751 | 0.98 | 0.02 | -0.9775 | -0.9697 |
| `expensiveOracle_n00399` | 399 | 0.02 | 0.1346 | 0 | 1 | 0.002494 | 0.000372 |
