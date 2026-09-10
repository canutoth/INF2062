# linux507_vmlinux FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 20159 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `expensiveOracle_n00202` (risk 0, %cost 0.07712).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_n00202` (omega_cost 0.002249, %cost 0.01146).

Empirical cost/confidence Pareto front:

- `random_n00202`: posterior area 0.9967, risk 0.002555, %cost 0.01019, omega_cost 0.001549
- `balanced_n00202`: posterior area 0.9935, risk 0.005109, %cost 0.009884, omega_cost -0.001569
- `diversity_n00202`: posterior area 0.9995, risk 0.0004961, %cost 0.02063, omega_cost 0.001897
- `uncertainty_n00202`: posterior area 0.9758, risk 0.02416, %cost 0.00673, omega_cost -0.01689
- `SRSSampling_n00202`: posterior area 0.998, risk 0.001439, %cost 0.01146, omega_cost 0.002249
- `cheapOracle_n00202`: posterior area 0.01002, risk 0.99, %cost 0.002243, omega_cost -0.9688
- `expensiveOracle_n00202`: posterior area 1, risk 0, %cost 0.07712, omega_cost 0.0006424
- `diversity_n00403`: posterior area 0.9999, risk 0.000124, %cost 0.0403, omega_cost 0.001104
- `cheapOracle_n00403`: posterior area 0.01999, risk 0.98, %cost 0.004788, omega_cost -0.9699

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `linux507_vmlinux:n00202` | `inconclusive` | 11.62 | 0.114 | large (0.1848) | median risks: random=0.002555, balanced=0.005109, diversity=0.0004961, uncertainty=0.02416, coverage=0.004737, SRSSampling=0.001439, cheapOracle=0.99, expensiveOracle=0; spread=0.99 |
| `FSE1` | `linux507_vmlinux:n00403` | `supports` | 15.75 | 0.0275 | large (0.35) | median risks: random=0.002455, balanced=0.001761, diversity=0.000124, uncertainty=0.01793, coverage=0.002629, SRSSampling=0.0004961, cheapOracle=0.98, expensiveOracle=0; spread=0.98 |
| `FSE2` | `linux507_vmlinux:n00202` | `supports` | 1 |  | changed (0.001606) | best size-normalized=expensiveOracle_n00202; best cost-normalized=SRSSampling_n00202 |
| `FSE3` | `linux507_vmlinux:n00202` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_n00202; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `linux507_vmlinux:n00202` | `supports` | 0.1429 |  | large frontier change (6) | count front=expensiveOracle_n00202; empirical front=SRSSampling_n00202,balanced_n00202,cheapOracle_n00202,diversity_n00202,expensiveOracle_n00202,random_n00202,uncertainty_n00202 |
| `FSE5` | `linux507_vmlinux:n00202` | `inconclusive` | 19 | 0.814 | small (0.38) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001439, median random=0.002555 |
| `FSE6` | `linux507_vmlinux:n00202` | `inconclusive` | 7 | 0.0883 | large (0.86) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01146, median random=0.01019 |
| `FSE2` | `linux507_vmlinux:n00403` | `supports` | 1 |  | changed (0.0006938) | best size-normalized=expensiveOracle_n00403; best cost-normalized=diversity_n00403 |
| `FSE3` | `linux507_vmlinux:n00403` | `refutes` | 0 |  | small (0.0003638) | best cost-normalized=diversity_n00403; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `linux507_vmlinux:n00403` | `supports` | 0.1429 |  | large frontier change (6) | count front=expensiveOracle_n00403; empirical front=SRSSampling_n00403,balanced_n00403,cheapOracle_n00403,coverage_n00403,diversity_n00403,expensiveOracle_n00403,uncertainty_n00403 |
| `FSE5` | `linux507_vmlinux:n00403` | `inconclusive` | 11.5 | 0.248 | large (0.23) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0004961, median random=0.002455 |
| `FSE6` | `linux507_vmlinux:n00403` | `inconclusive` | 9 | 0.144 | large (0.82) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02122, median random=0.01989 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n00202` | 202 | 0.01002 | 0.01019 | 0.002555 | 0.9967 | 0.001628 | 0.001549 |
| `balanced_n00202` | 202 | 0.01002 | 0.009884 | 0.005109 | 0.9935 | -0.001636 | -0.001569 |
| `diversity_n00202` | 202 | 0.01002 | 0.02063 | 0.0004961 | 0.9995 | 0.004406 | 0.001897 |
| `uncertainty_n00202` | 202 | 0.01002 | 0.00673 | 0.02416 | 0.9758 | -0.01926 | -0.01689 |
| `coverage_n00202` | 202 | 0.01002 | 0.01038 | 0.004737 | 0.9953 | 0.0001646 | -1.675e-06 |
| `SRSSampling_n00202` | 202 | 0.01002 | 0.01146 | 0.001439 | 0.998 | 0.002858 | 0.002249 |
| `cheapOracle_n00202` | 202 | 0.01002 | 0.002243 | 0.99 | 0.01002 | -0.9851 | -0.9688 |
| `expensiveOracle_n00202` | 202 | 0.01002 | 0.07712 | 0 | 1 | 0.004902 | 0.0006424 |
| `random_n00403` | 403 | 0.01999 | 0.01989 | 0.002455 | 0.9966 | -0.0009537 | -0.0009407 |
| `balanced_n00403` | 403 | 0.01999 | 0.01998 | 0.001761 | 0.9979 | 0.0004155 | 0.0004165 |
| `diversity_n00403` | 403 | 0.01999 | 0.0403 | 0.000124 | 0.9999 | 0.002345 | 0.001104 |
| `uncertainty_n00403` | 403 | 0.01999 | 0.01364 | 0.01793 | 0.9821 | -0.01546 | -0.01432 |
| `coverage_n00403` | 403 | 0.01999 | 0.01957 | 0.002629 | 0.9974 | -0.00016 | -0.0001075 |
| `SRSSampling_n00403` | 403 | 0.01999 | 0.02122 | 0.0004961 | 0.9984 | 0.0008818 | 0.0007399 |
| `cheapOracle_n00403` | 403 | 0.01999 | 0.004788 | 0.98 | 0.01999 | -0.9775 | -0.9699 |
| `expensiveOracle_n00403` | 403 | 0.01999 | 0.1209 | 0 | 1 | 0.002469 | 0.0004099 |
