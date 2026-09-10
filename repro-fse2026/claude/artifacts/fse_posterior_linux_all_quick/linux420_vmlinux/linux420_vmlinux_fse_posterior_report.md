# linux420_vmlinux FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 23489 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n00235` (risk 0, %cost 0.0246).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n00235` (omega_cost 0.001725, %cost 0.0246).

Empirical cost/confidence Pareto front:

- `random_n00235`: posterior area 0.9929, risk 0.006492, %cost 0.00982, omega_cost -0.002765
- `balanced_n00235`: posterior area 0.9964, risk 0.002491, %cost 0.01023, omega_cost 0.0005195
- `diversity_n00235`: posterior area 1, risk 0, %cost 0.0246, omega_cost 0.001725
- `uncertainty_n00235`: posterior area 0.9782, risk 0.02184, %cost 0.006479, omega_cost -0.01535
- `SRSSampling_n00235`: posterior area 0.997, risk 0.002427, %cost 0.01104, omega_cost 0.0007948
- `cheapOracle_n00235`: posterior area 0.01, risk 0.99, %cost 0.002201, omega_cost -0.9714
- `random_n00470`: posterior area 0.9982, risk 0.001213, %cost 0.01975, omega_cost 0.0003156
- `balanced_n00470`: posterior area 0.9982, risk 0.001426, %cost 0.02029, omega_cost 0.0003357
- `cheapOracle_n00470`: posterior area 0.02001, risk 0.98, %cost 0.004711, omega_cost -0.9711

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `linux420_vmlinux:n00235` | `supports` | 16.58 | 0.0203 | large (0.3831) | median risks: random=0.006492, balanced=0.002491, diversity=0, uncertainty=0.02184, coverage=0.007088, SRSSampling=0.002427, cheapOracle=0.99, expensiveOracle=0; spread=0.99 |
| `FSE1` | `linux420_vmlinux:n00470` | `supports` | 17.7 | 0.0134 | large (0.4281) | median risks: random=0.001213, balanced=0.001426, diversity=0, uncertainty=0.01245, coverage=0.00679, SRSSampling=0.002427, cheapOracle=0.98, expensiveOracle=0; spread=0.98 |
| `FSE2` | `linux420_vmlinux:n00235` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n00235; best cost-normalized=diversity_n00235 |
| `FSE3` | `linux420_vmlinux:n00235` | `refutes` | 0 |  | small (0.0009299) | best cost-normalized=diversity_n00235; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `linux420_vmlinux:n00235` | `supports` | 0.1429 |  | large frontier change (6) | count front=diversity_n00235,expensiveOracle_n00235; empirical front=SRSSampling_n00235,balanced_n00235,cheapOracle_n00235,diversity_n00235,random_n00235,uncertainty_n00235 |
| `FSE5` | `linux420_vmlinux:n00235` | `inconclusive` | 11 | 0.225 | large (0.22) | A12<0.5 means SRS risks tend to be lower; median SRS=0.002427, median random=0.006492 |
| `FSE6` | `linux420_vmlinux:n00235` | `inconclusive` | 7 | 0.0883 | large (0.86) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01104, median random=0.00982 |
| `FSE2` | `linux420_vmlinux:n00470` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n00470; best cost-normalized=diversity_n00470 |
| `FSE3` | `linux420_vmlinux:n00470` | `refutes` | 0 |  | small (0.000813) | best cost-normalized=diversity_n00470; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `linux420_vmlinux:n00470` | `supports` | 0.1429 |  | large frontier change (6) | count front=diversity_n00470,expensiveOracle_n00470; empirical front=balanced_n00470,cheapOracle_n00470,coverage_n00470,diversity_n00470,random_n00470,uncertainty_n00470 |
| `FSE5` | `linux420_vmlinux:n00470` | `refutes` | 25 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.002427, median random=0.001213 |
| `FSE6` | `linux420_vmlinux:n00470` | `inconclusive` | 12 | 0.275 | large (0.76) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02101, median random=0.01975 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n00235` | 235 | 0.01 | 0.00982 | 0.006492 | 0.9929 | -0.002843 | -0.002765 |
| `balanced_n00235` | 235 | 0.01 | 0.01023 | 0.002491 | 0.9964 | 0.0006135 | 0.0005195 |
| `diversity_n00235` | 235 | 0.01 | 0.0246 | 0 | 1 | 0.004219 | 0.001725 |
| `uncertainty_n00235` | 235 | 0.01 | 0.006479 | 0.02184 | 0.9782 | -0.01762 | -0.01535 |
| `coverage_n00235` | 235 | 0.01 | 0.01072 | 0.007088 | 0.9929 | -0.002869 | -0.00315 |
| `SRSSampling_n00235` | 235 | 0.01 | 0.01104 | 0.002427 | 0.997 | 0.001188 | 0.0007948 |
| `cheapOracle_n00235` | 235 | 0.01 | 0.002201 | 0.99 | 0.01 | -0.9858 | -0.9714 |
| `expensiveOracle_n00235` | 235 | 0.01 | 0.0876 | 0 | 1 | 0.004219 | 0.0004855 |
| `random_n00470` | 470 | 0.02001 | 0.01975 | 0.001213 | 0.9982 | 0.000288 | 0.0003156 |
| `balanced_n00470` | 470 | 0.02001 | 0.02029 | 0.001426 | 0.9982 | 0.0003646 | 0.0003357 |
| `diversity_n00470` | 470 | 0.02001 | 0.04601 | 0 | 1 | 0.002119 | 0.0009235 |
| `uncertainty_n00470` | 470 | 0.02001 | 0.01532 | 0.01245 | 0.9875 | -0.01033 | -0.00969 |
| `coverage_n00470` | 470 | 0.02001 | 0.01971 | 0.00679 | 0.9932 | -0.004672 | -0.00464 |
| `SRSSampling_n00470` | 470 | 0.02001 | 0.02101 | 0.002427 | 0.9981 | 0.0002114 | 0.0001106 |
| `cheapOracle_n00470` | 470 | 0.02001 | 0.004711 | 0.98 | 0.02001 | -0.9779 | -0.9711 |
| `expensiveOracle_n00470` | 470 | 0.02001 | 0.1387 | 0 | 1 | 0.002119 | 0.0003068 |
