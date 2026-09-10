# linux413_vmlinux FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 92562 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n00926` (risk 0, %cost 0.02368).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n00926` (omega_cost 0.0004548, %cost 0.02368).

Empirical cost/confidence Pareto front:

- `random_n00926`: posterior area 0.9988, risk 0.0007292, %cost 0.009944, omega_cost -0.0001383
- `balanced_n00926`: posterior area 0.999, risk 0.0006968, %cost 0.01005, omega_cost 4.755e-05
- `diversity_n00926`: posterior area 1, risk 0, %cost 0.02368, omega_cost 0.0004548
- `coverage_n00926`: posterior area 0.998, risk 0.001702, %cost 0.00983, omega_cost -0.0008599
- `SRSSampling_n00926`: posterior area 0.9991, risk 0.0006968, %cost 0.01019, omega_cost 0.0001266
- `cheapOracle_n00926`: posterior area 0.01, risk 0.99, %cost 0.00232, omega_cost -0.9854
- `random_n01851`: posterior area 0.9993, risk 0.0004483, %cost 0.01983, omega_cost -0.0001132
- `balanced_n01851`: posterior area 0.9995, risk 0.0003727, %cost 0.02002, omega_cost 1.995e-05
- `diversity_n01851`: posterior area 1, risk 0, %cost 0.04416, omega_cost 0.0002445
- `SRSSampling_n01851`: posterior area 0.9995, risk 0.0002917, %cost 0.02016, omega_cost 6.631e-05
- `cheapOracle_n01851`: posterior area 0.02, risk 0.98, %cost 0.005079, omega_cost -0.9779

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `linux413_vmlinux:n00926` | `supports` | 80.59 | 1.04e-14 | large (0.2079) | median risks: random=0.0007292, balanced=0.0006968, diversity=0, uncertainty=0.001718, coverage=0.001702, SRSSampling=0.0006968, cheapOracle=0.99, expensiveOracle=0; spread=0.99 |
| `FSE1` | `linux413_vmlinux:n01851` | `supports` | 86.9 | 5.36e-16 | large (0.2257) | median risks: random=0.0004483, balanced=0.0003727, diversity=0, uncertainty=0.0005402, coverage=0.0009777, SRSSampling=0.0002917, cheapOracle=0.98, expensiveOracle=0; spread=0.98 |
| `FSE1` | `linux413_vmlinux:n04628` | `supports` | 50.68 | 3.44e-09 | large (0.1334) | median risks: random=9.723e-05, balanced=0.0001783, uncertainty=0.0001188, coverage=0.000605, SRSSampling=0.0001296, cheapOracle=0.95, expensiveOracle=0; spread=0.95 |
| `FSE2` | `linux413_vmlinux:n00926` | `supports` | 1 |  | changed (0.000361) | best size-normalized=expensiveOracle_n00926; best cost-normalized=diversity_n00926 |
| `FSE3` | `linux413_vmlinux:n00926` | `refutes` | 0 |  | small (0.0003283) | best cost-normalized=diversity_n00926; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `linux413_vmlinux:n00926` | `supports` | 0.1429 |  | large frontier change (6) | count front=expensiveOracle_n00926; empirical front=SRSSampling_n00926,balanced_n00926,cheapOracle_n00926,coverage_n00926,diversity_n00926,expensiveOracle_n00926,random_n00926 |
| `FSE5` | `linux413_vmlinux:n00926` | `refutes` | 4697 | 0.81 | negligible (0.4697) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0006968, median random=0.0007292 |
| `FSE6` | `linux413_vmlinux:n00926` | `supports` | 3364 | 4.70e-04 | medium (0.6636) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01019, median random=0.009944 |
| `FSE2` | `linux413_vmlinux:n01851` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n01851; best cost-normalized=diversity_n01851 |
| `FSE3` | `linux413_vmlinux:n01851` | `refutes` | 0 |  | small (0.0001782) | best cost-normalized=diversity_n01851; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `linux413_vmlinux:n01851` | `supports` | 0.1429 |  | large frontier change (6) | count front=diversity_n01851,expensiveOracle_n01851; empirical front=SRSSampling_n01851,balanced_n01851,cheapOracle_n01851,coverage_n01851,diversity_n01851,random_n01851 |
| `FSE5` | `linux413_vmlinux:n01851` | `supports` | 3920 | 0.0325 | small (0.3921) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0002917, median random=0.0004483 |
| `FSE6` | `linux413_vmlinux:n01851` | `supports` | 3645 | 0.00494 | small (0.6355) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02016, median random=0.01983 |
| `FSE2` | `linux413_vmlinux:n04628` | `supports` | 1 |  | changed (9.109e-06) | best size-normalized=expensiveOracle_n04628; best cost-normalized=uncertainty_n04628 |
| `FSE3` | `linux413_vmlinux:n04628` | `refutes` | 0 |  | negligible (1.115e-06) | best cost-normalized=uncertainty_n04628; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `linux413_vmlinux:n04628` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n04628; empirical front=SRSSampling_n04628,cheapOracle_n04628,coverage_n04628,expensiveOracle_n04628,random_n04628,uncertainty_n04628 |
| `FSE5` | `linux413_vmlinux:n04628` | `refutes` | 4691 | 0.798 | negligible (0.5309) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0001296, median random=9.723e-05 |
| `FSE6` | `linux413_vmlinux:n04628` | `supports` | 3863 | 0.0227 | small (0.6137) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05052, median random=0.04999 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n00926` | 926 | 0.01 | 0.009944 | 0.0007292 | 0.9988 | -0.0001447 | -0.0001383 |
| `balanced_n00926` | 926 | 0.01 | 0.01005 | 0.0006968 | 0.999 | 5.254e-05 | 4.755e-05 |
| `diversity_n00926` | 926 | 0.01 | 0.02368 | 0 | 1 | 0.001077 | 0.0004548 |
| `uncertainty_n00926` | 926 | 0.01 | 0.01164 | 0.001718 | 0.9984 | -0.0005446 | -0.0006955 |
| `coverage_n00926` | 926 | 0.01 | 0.00983 | 0.001702 | 0.998 | -0.0008789 | -0.0008599 |
| `SRSSampling_n00926` | 926 | 0.01 | 0.01019 | 0.0006968 | 0.9991 | 0.000146 | 0.0001266 |
| `cheapOracle_n00926` | 926 | 0.01 | 0.00232 | 0.99 | 0.01 | -0.9889 | -0.9854 |
| `expensiveOracle_n00926` | 926 | 0.01 | 0.1152 | 0 | 1 | 0.001078 | 9.378e-05 |
| `random_n01851` | 1851 | 0.02 | 0.01983 | 0.0004483 | 0.9993 | -0.0001177 | -0.0001132 |
| `balanced_n01851` | 1851 | 0.02 | 0.02002 | 0.0003727 | 0.9995 | 2.045e-05 | 1.995e-05 |
| `diversity_n01851` | 1851 | 0.02 | 0.04416 | 0 | 1 | 0.0005397 | 0.0002445 |
| `uncertainty_n01851` | 1851 | 0.02 | 0.02271 | 0.0005402 | 0.9991 | -0.0003451 | -0.0004096 |
| `coverage_n01851` | 1851 | 0.02 | 0.0196 | 0.0009777 | 0.9989 | -0.0005672 | -0.0005564 |
| `SRSSampling_n01851` | 1851 | 0.02 | 0.02016 | 0.0002917 | 0.9995 | 7.057e-05 | 6.631e-05 |
| `cheapOracle_n01851` | 1851 | 0.02 | 0.005079 | 0.98 | 0.02 | -0.9795 | -0.9779 |
| `expensiveOracle_n01851` | 1851 | 0.02 | 0.1738 | 0 | 1 | 0.0005397 | 6.215e-05 |
| `random_n04628` | 4628 | 0.05 | 0.04999 | 9.723e-05 | 0.9998 | 3.686e-05 | 3.691e-05 |
| `balanced_n04628` | 4628 | 0.05 | 0.05012 | 0.0001783 | 0.9997 | -3.552e-05 | -3.604e-05 |
| `uncertainty_n04628` | 4628 | 0.05 | 0.05557 | 0.0001188 | 0.9999 | 6.905e-05 | 4.742e-05 |
| `coverage_n04628` | 4628 | 0.05 | 0.04894 | 0.000605 | 0.9994 | -0.0003793 | -0.0003746 |
| `SRSSampling_n04628` | 4628 | 0.05 | 0.05052 | 0.0001296 | 0.9998 | 4.853e-05 | 4.631e-05 |
| `cheapOracle_n04628` | 4628 | 0.05 | 0.01459 | 0.95 | 0.05 | -0.9498 | -0.9493 |
| `expensiveOracle_n04628` | 4628 | 0.05 | 0.282 | 0 | 1 | 0.000216 | 3.831e-05 |
