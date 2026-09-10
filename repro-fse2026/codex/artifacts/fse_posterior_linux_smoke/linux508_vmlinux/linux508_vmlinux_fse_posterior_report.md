# linux508_vmlinux FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 21923 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `expensiveOracle_n00219` (risk 0, %cost 0.08236).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n00219` (omega_cost 0.001868, %cost 0.0224).

Empirical cost/confidence Pareto front:

- `random_n00219`: posterior area 0.9965, risk 0.002349, %cost 0.01014, omega_cost 0.000967
- `balanced_n00219`: posterior area 0.9951, risk 0.004014, %cost 0.01001, omega_cost -0.0003576
- `diversity_n00219`: posterior area 0.9998, risk 0.0001596, %cost 0.0224, omega_cost 0.001868
- `uncertainty_n00219`: posterior area 0.9921, risk 0.007891, %cost 0.006844, omega_cost -0.001314
- `SRSSampling_n00219`: posterior area 0.9978, risk 0.001596, %cost 0.01175, omega_cost 0.001652
- `cheapOracle_n00219`: posterior area 0.00999, risk 0.99, %cost 0.002703, omega_cost -0.9737
- `expensiveOracle_n00219`: posterior area 1, risk 0, %cost 0.08236, omega_cost 0.0005532
- `balanced_n00438`: posterior area 0.9983, risk 0.001574, %cost 0.0201, omega_cost 0.0005306
- `diversity_n00438`: posterior area 1, risk 4.561e-05, %cost 0.04079, omega_cost 0.00107
- `cheapOracle_n00438`: posterior area 0.01998, risk 0.98, %cost 0.005749, omega_cost -0.9722

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `linux508_vmlinux:n00219` | `supports` | 15.46 | 0.0305 | large (0.3384) | median risks: random=0.002349, balanced=0.004014, diversity=0.0001596, uncertainty=0.007891, coverage=0.003832, SRSSampling=0.001596, cheapOracle=0.99, expensiveOracle=0; spread=0.99 |
| `FSE1` | `linux508_vmlinux:n00438` | `supports` | 15.87 | 0.0263 | large (0.355) | median risks: random=0.003398, balanced=0.001574, diversity=4.561e-05, uncertainty=0.01352, coverage=0.003558, SRSSampling=0.001596, cheapOracle=0.98, expensiveOracle=0; spread=0.98 |
| `FSE2` | `linux508_vmlinux:n00219` | `supports` | 1 |  | changed (0.001315) | best size-normalized=expensiveOracle_n00219; best cost-normalized=diversity_n00219 |
| `FSE3` | `linux508_vmlinux:n00219` | `refutes` | 0 |  | small (0.0002164) | best cost-normalized=diversity_n00219; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `linux508_vmlinux:n00219` | `supports` | 0.1429 |  | large frontier change (6) | count front=expensiveOracle_n00219; empirical front=SRSSampling_n00219,balanced_n00219,cheapOracle_n00219,diversity_n00219,expensiveOracle_n00219,random_n00219,uncertainty_n00219 |
| `FSE5` | `linux508_vmlinux:n00219` | `inconclusive` | 19.5 | 0.862 | small (0.39) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001596, median random=0.002349 |
| `FSE6` | `linux508_vmlinux:n00219` | `inconclusive` | 16 | 0.547 | medium (0.68) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01175, median random=0.01014 |
| `FSE2` | `linux508_vmlinux:n00438` | `supports` | 1 |  | changed (0.0007091) | best size-normalized=expensiveOracle_n00438; best cost-normalized=diversity_n00438 |
| `FSE3` | `linux508_vmlinux:n00438` | `refutes` | 0 |  | small (0.0008265) | best cost-normalized=diversity_n00438; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `linux508_vmlinux:n00438` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n00438; empirical front=balanced_n00438,cheapOracle_n00438,diversity_n00438,expensiveOracle_n00438,random_n00438,uncertainty_n00438 |
| `FSE5` | `linux508_vmlinux:n00438` | `inconclusive` | 16.5 | 0.587 | medium (0.33) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001596, median random=0.003398 |
| `FSE6` | `linux508_vmlinux:n00438` | `supports` | 4 | 0.0383 | large (0.92) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02158, median random=0.01923 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n00219` | 219 | 0.00999 | 0.01014 | 0.002349 | 0.9965 | 0.001035 | 0.000967 |
| `balanced_n00219` | 219 | 0.00999 | 0.01001 | 0.004014 | 0.9951 | -0.0003467 | -0.0003576 |
| `diversity_n00219` | 219 | 0.00999 | 0.0224 | 0.0001596 | 0.9998 | 0.004365 | 0.001868 |
| `uncertainty_n00219` | 219 | 0.00999 | 0.006844 | 0.007891 | 0.9921 | -0.003366 | -0.001314 |
| `coverage_n00219` | 219 | 0.00999 | 0.01038 | 0.003832 | 0.9962 | 0.0006933 | 0.0005229 |
| `SRSSampling_n00219` | 219 | 0.00999 | 0.01175 | 0.001596 | 0.9978 | 0.002326 | 0.001652 |
| `cheapOracle_n00219` | 219 | 0.00999 | 0.002703 | 0.99 | 0.00999 | -0.9855 | -0.9737 |
| `expensiveOracle_n00219` | 219 | 0.00999 | 0.08236 | 0 | 1 | 0.004525 | 0.0005532 |
| `random_n00438` | 438 | 0.01998 | 0.01923 | 0.003398 | 0.9962 | -0.001568 | -0.00148 |
| `balanced_n00438` | 438 | 0.01998 | 0.0201 | 0.001574 | 0.9983 | 0.0005439 | 0.0005306 |
| `diversity_n00438` | 438 | 0.01998 | 0.04079 | 4.561e-05 | 1 | 0.002227 | 0.00107 |
| `uncertainty_n00438` | 438 | 0.01998 | 0.01792 | 0.01352 | 0.9865 | -0.01125 | -0.01099 |
| `coverage_n00438` | 438 | 0.01998 | 0.02014 | 0.003558 | 0.9964 | -0.001285 | -0.001303 |
| `SRSSampling_n00438` | 438 | 0.01998 | 0.02158 | 0.001596 | 0.9981 | 0.0004117 | 0.0002436 |
| `cheapOracle_n00438` | 438 | 0.01998 | 0.005749 | 0.98 | 0.01998 | -0.9777 | -0.9722 |
| `expensiveOracle_n00438` | 438 | 0.01998 | 0.1263 | 0 | 1 | 0.002273 | 0.000361 |
