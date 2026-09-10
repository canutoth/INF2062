# linux413_vmlinux FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 92562 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n00926` (risk 0, %cost 0.02392).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_n00926` (omega_cost 0.0007137, %cost 0.01079).

Empirical cost/confidence Pareto front:

- `random_n00926`: posterior area 0.9988, risk 0.0008805, %cost 0.009963, omega_cost -0.0001464
- `balanced_n00926`: posterior area 0.9994, risk 0.0004051, %cost 0.01004, omega_cost 0.0004829
- `diversity_n00926`: posterior area 1, risk 0, %cost 0.02392, omega_cost 0.0004512
- `coverage_n00926`: posterior area 0.9943, risk 0.005688, %cost 0.009316, omega_cost -0.004531
- `SRSSampling_n00926`: posterior area 0.9997, risk 0.0002701, %cost 0.01079, omega_cost 0.0007137
- `cheapOracle_n00926`: posterior area 0.01, risk 0.99, %cost 0.00232, omega_cost -0.9854
- `cheapOracle_n01851`: posterior area 0.02, risk 0.98, %cost 0.005079, omega_cost -0.9779

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `linux413_vmlinux:n00926` | `supports` | 18.51 | 0.00987 | large (0.4603) | median risks: random=0.0008805, balanced=0.0004051, diversity=0, uncertainty=0.001183, coverage=0.005688, SRSSampling=0.0002701, cheapOracle=0.99, expensiveOracle=0; spread=0.99 |
| `FSE1` | `linux413_vmlinux:n01851` | `supports` | 14.78 | 0.0389 | large (0.3113) | median risks: random=0.0002593, balanced=0.0004592, diversity=0, uncertainty=0.0003133, coverage=0.001631, SRSSampling=0.0002701, cheapOracle=0.98, expensiveOracle=0; spread=0.98 |
| `FSE2` | `linux413_vmlinux:n00926` | `supports` | 1 |  | changed (0.0002625) | best size-normalized=diversity_n00926; best cost-normalized=SRSSampling_n00926 |
| `FSE3` | `linux413_vmlinux:n00926` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_n00926; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `linux413_vmlinux:n00926` | `supports` | 0.1429 |  | large frontier change (6) | count front=diversity_n00926,expensiveOracle_n00926; empirical front=SRSSampling_n00926,balanced_n00926,cheapOracle_n00926,coverage_n00926,diversity_n00926,random_n00926 |
| `FSE5` | `linux413_vmlinux:n00926` | `inconclusive` | 7 | 0.0883 | large (0.14) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0002701, median random=0.0008805 |
| `FSE6` | `linux413_vmlinux:n00926` | `inconclusive` | 13 | 0.332 | large (0.74) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01079, median random=0.009963 |
| `FSE2` | `linux413_vmlinux:n01851` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n01851; best cost-normalized=diversity_n01851 |
| `FSE3` | `linux413_vmlinux:n01851` | `refutes` | 0 |  | small (0.000161) | best cost-normalized=diversity_n01851; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `linux413_vmlinux:n01851` | `supports` | 0.1429 |  | large frontier change (6) | count front=diversity_n01851,expensiveOracle_n01851; empirical front=balanced_n01851,cheapOracle_n01851,coverage_n01851,diversity_n01851,random_n01851,uncertainty_n01851 |
| `FSE5` | `linux413_vmlinux:n01851` | `refutes` | 22.5 | 0.847 | negligible (0.55) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0002701, median random=0.0002593 |
| `FSE6` | `linux413_vmlinux:n01851` | `inconclusive` | 6 | 0.0677 | large (0.88) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02079, median random=0.02017 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n00926` | 926 | 0.01 | 0.009963 | 0.0008805 | 0.9988 | -0.0001508 | -0.0001464 |
| `balanced_n00926` | 926 | 0.01 | 0.01004 | 0.0004051 | 0.9994 | 0.0004866 | 0.0004829 |
| `diversity_n00926` | 926 | 0.01 | 0.02392 | 0 | 1 | 0.001078 | 0.0004512 |
| `uncertainty_n00926` | 926 | 0.01 | 0.01212 | 0.001183 | 0.9988 | -0.0001054 | -0.0002929 |
| `coverage_n00926` | 926 | 0.01 | 0.009316 | 0.005688 | 0.9943 | -0.00461 | -0.004531 |
| `SRSSampling_n00926` | 926 | 0.01 | 0.01079 | 0.0002701 | 0.9997 | 0.0007924 | 0.0007137 |
| `cheapOracle_n00926` | 926 | 0.01 | 0.00232 | 0.99 | 0.01 | -0.9889 | -0.9854 |
| `expensiveOracle_n00926` | 926 | 0.01 | 0.1152 | 0 | 1 | 0.001078 | 9.378e-05 |
| `random_n01851` | 1851 | 0.02 | 0.02017 | 0.0002593 | 0.9996 | 0.0001313 | 0.0001266 |
| `balanced_n01851` | 1851 | 0.02 | 0.01983 | 0.0004592 | 0.9995 | 7.727e-05 | 8.189e-05 |
| `diversity_n01851` | 1851 | 0.02 | 0.04434 | 0 | 1 | 0.0005397 | 0.0002435 |
| `uncertainty_n01851` | 1851 | 0.02 | 0.02373 | 0.0003133 | 0.9997 | 0.0002264 | 0.0001415 |
| `coverage_n01851` | 1851 | 0.02 | 0.01946 | 0.001631 | 0.9984 | -0.001092 | -0.001077 |
| `SRSSampling_n01851` | 1851 | 0.02 | 0.02079 | 0.0002701 | 0.9996 | 0.0001032 | 8.257e-05 |
| `cheapOracle_n01851` | 1851 | 0.02 | 0.005079 | 0.98 | 0.02 | -0.9795 | -0.9779 |
| `expensiveOracle_n01851` | 1851 | 0.02 | 0.1738 | 0 | 1 | 0.0005397 | 6.215e-05 |
