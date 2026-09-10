# linux415_vmlinux FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 39391 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `expensiveOracle_n00394` (risk 0, %cost 0.08554).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n00394` (omega_cost 0.0009973, %cost 0.02417).

Empirical cost/confidence Pareto front:

- `random_n00394`: posterior area 0.9983, risk 0.001269, %cost 0.009932, omega_cost 0.0008396
- `diversity_n00394`: posterior area 0.9999, risk 5.077e-05, %cost 0.02417, omega_cost 0.0009973
- `uncertainty_n00394`: posterior area 0.9978, risk 0.002171, %cost 0.009003, omega_cost 0.0006335
- `SRSSampling_n00394`: posterior area 0.9986, risk 0.001422, %cost 0.01512, omega_cost 0.0002614
- `cheapOracle_n00394`: posterior area 0.01, risk 0.99, %cost 0.002033, omega_cost -0.9778
- `expensiveOracle_n00394`: posterior area 1, risk 0, %cost 0.08554, omega_cost 0.0002966
- `random_n00788`: posterior area 0.9995, risk 0.000457, %cost 0.0201, omega_cost 0.0007901
- `coverage_n00788`: posterior area 0.9991, risk 0.0009266, %cost 0.01986, omega_cost 0.0003483
- `cheapOracle_n00788`: posterior area 0.02, risk 0.98, %cost 0.004422, omega_cost -0.9743

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `linux415_vmlinux:n00394` | `inconclusive` | 11.16 | 0.132 | large (0.1664) | median risks: random=0.001269, balanced=0.002361, diversity=5.077e-05, uncertainty=0.002171, coverage=0.002323, SRSSampling=0.001422, cheapOracle=0.99, expensiveOracle=0; spread=0.99 |
| `FSE1` | `linux415_vmlinux:n00788` | `supports` | 15.81 | 0.0269 | large (0.3525) | median risks: random=0.000457, balanced=0.0006854, diversity=5.077e-05, uncertainty=0.00311, coverage=0.0009266, SRSSampling=0.0006347, cheapOracle=0.98, expensiveOracle=0; spread=0.98 |
| `FSE2` | `linux415_vmlinux:n00394` | `supports` | 1 |  | changed (0.0007006) | best size-normalized=expensiveOracle_n00394; best cost-normalized=diversity_n00394 |
| `FSE3` | `linux415_vmlinux:n00394` | `refutes` | 0 |  | small (0.0007359) | best cost-normalized=diversity_n00394; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `linux415_vmlinux:n00394` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n00394; empirical front=SRSSampling_n00394,cheapOracle_n00394,diversity_n00394,expensiveOracle_n00394,random_n00394,uncertainty_n00394 |
| `FSE5` | `linux415_vmlinux:n00394` | `refutes` | 24.5 | 0.661 | negligible (0.49) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001422, median random=0.001269 |
| `FSE6` | `linux415_vmlinux:n00394` | `supports` | 0 | 0.0104 | large (1) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01512, median random=0.009932 |
| `FSE2` | `linux415_vmlinux:n00788` | `supports` | 1 |  | changed (0.0006071) | best size-normalized=expensiveOracle_n00788; best cost-normalized=random_n00788 |
| `FSE3` | `linux415_vmlinux:n00788` | `refutes` | 0 |  | small (0.0005297) | best cost-normalized=random_n00788; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `linux415_vmlinux:n00788` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n00788; empirical front=cheapOracle_n00788,coverage_n00788,diversity_n00788,expensiveOracle_n00788,random_n00788,uncertainty_n00788 |
| `FSE5` | `linux415_vmlinux:n00788` | `inconclusive` | 17.5 | 0.675 | medium (0.65) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0006347, median random=0.000457 |
| `FSE6` | `linux415_vmlinux:n00788` | `supports` | 3 | 0.0282 | large (0.94) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02317, median random=0.0201 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n00394` | 394 | 0.01 | 0.009932 | 0.001269 | 0.9983 | 0.0008218 | 0.0008396 |
| `balanced_n00394` | 394 | 0.01 | 0.009818 | 0.002361 | 0.9966 | -0.0008664 | -0.0008193 |
| `diversity_n00394` | 394 | 0.01 | 0.02417 | 5.077e-05 | 0.9999 | 0.002474 | 0.0009973 |
| `uncertainty_n00394` | 394 | 0.01 | 0.009003 | 0.002171 | 0.9978 | 0.0003547 | 0.0006335 |
| `coverage_n00394` | 394 | 0.01 | 0.01058 | 0.002323 | 0.9977 | 0.0002024 | 6.465e-05 |
| `SRSSampling_n00394` | 394 | 0.01 | 0.01512 | 0.001422 | 0.9986 | 0.001114 | 0.0002614 |
| `cheapOracle_n00394` | 394 | 0.01 | 0.002033 | 0.99 | 0.01 | -0.9875 | -0.9778 |
| `expensiveOracle_n00394` | 394 | 0.01 | 0.08554 | 0 | 1 | 0.002525 | 0.0002966 |
| `random_n00788` | 788 | 0.02 | 0.0201 | 0.000457 | 0.9995 | 0.0007962 | 0.0007901 |
| `balanced_n00788` | 788 | 0.02 | 0.0201 | 0.0006854 | 0.999 | 0.0002199 | 0.0002141 |
| `diversity_n00788` | 788 | 0.02 | 0.04366 | 5.077e-05 | 0.9999 | 0.001215 | 0.00053 |
| `uncertainty_n00788` | 788 | 0.02 | 0.01922 | 0.00311 | 0.9969 | -0.001844 | -0.001792 |
| `coverage_n00788` | 788 | 0.02 | 0.01986 | 0.0009266 | 0.9991 | 0.0003392 | 0.0003483 |
| `SRSSampling_n00788` | 788 | 0.02 | 0.02317 | 0.0006347 | 0.9992 | 0.0004331 | 0.0002604 |
| `cheapOracle_n00788` | 788 | 0.02 | 0.004422 | 0.98 | 0.02 | -0.9787 | -0.9743 |
| `expensiveOracle_n00788` | 788 | 0.02 | 0.1386 | 0 | 1 | 0.001266 | 0.000183 |
