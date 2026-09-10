# lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n8` (risk 0.0065, %cost 0.00434).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n8` (omega_cost 0.08714, %cost 0.00434).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9332, risk 0.0595, %cost 0.003913, omega_cost 0.03493
- `diversity_n8`: posterior area 0.9935, risk 0.0065, %cost 0.00434, omega_cost 0.08714
- `SRSSampling_n8`: posterior area 0.9248, risk 0.06625, %cost 0.002973, omega_cost 0.05065
- `pilotCost_n8`: posterior area 0.6935, risk 0.383, %cost 0.001918, omega_cost -0.1352
- `cheapOracle_n8`: posterior area 0.479, risk 0.521, %cost 0.00157, omega_cost -0.3264

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n8` | `inconclusive` | 10.62 | 0.156 | large (0.1007) | median risks: random=0.0695, balanced=0.0595, diversity=0.0065, SRSSampling=0.06625, pairwise=0.0475, pilotCost=0.383, cheapOracle=0.521, expensiveOracle=0.078; spread=0.5145 |
| `FSE1` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 5.959 | 0.545 | large (0) | median risks: random=0.06225, balanced=0.0365, diversity=0.0065, SRSSampling=0.0435, pairwise=0.0475, pilotCost=0.078, cheapOracle=0.521, expensiveOracle=0.078; spread=0.5145 |
| `FSE2` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n8; best cost-normalized=diversity_n8 |
| `FSE3` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.03649) | best cost-normalized=diversity_n8; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n8; empirical front=SRSSampling_n8,balanced_n8,cheapOracle_n8,diversity_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 47.5 | 0.756 | negligible (0.475) | A12<0.5 means SRS risks tend to be lower; median SRS=0.06625, median random=0.0695 |
| `FSE6` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 48.5 | 0.699 | negligible (0.485) | A12>0.5 means SRS costs tend to be higher; median SRS=0.002973, median random=0.003305 |
| `FSE2` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.03895) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n16; empirical front=SRSSampling_n16,balanced_n16,cheapOracle_n16,diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n16` | `inconclusive` | 42.5 | 0.945 | small (0.425) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0435, median random=0.06225 |
| `FSE6` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 48.5 | 0.699 | negligible (0.515) | A12>0.5 means SRS costs tend to be higher; median SRS=0.005814, median random=0.005814 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003305 | 0.0695 | 0.9204 | 0.02045 | 0.0366 |
| `balanced_n8` | 8 | 0.004 | 0.003913 | 0.0595 | 0.9332 | 0.03315 | 0.03493 |
| `diversity_n8` | 8 | 0.004 | 0.00434 | 0.0065 | 0.9935 | 0.0935 | 0.08714 |
| `SRSSampling_n8` | 8 | 0.004 | 0.002973 | 0.06625 | 0.9248 | 0.0248 | 0.05065 |
| `pairwise_n8` | 8 | 0.004 | 0.005938 | 0.0475 | 0.9525 | 0.0525 | 0.02457 |
| `pilotCost_n8` | 8 | 0.004 | 0.001918 | 0.383 | 0.6935 | -0.2066 | -0.1352 |
| `cheapOracle_n8` | 8 | 0.004 | 0.00157 | 0.521 | 0.479 | -0.421 | -0.3264 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.1301 | 0.078 | 0.922 | 0.022 | -0.07419 |
| `random_n16` | 16 | 0.008 | 0.005814 | 0.06225 | 0.9309 | -0.01354 | 0.004274 |
| `balanced_n16` | 16 | 0.008 | 0.006878 | 0.0365 | 0.9604 | 0.01591 | 0.02381 |
| `diversity_n16` | 16 | 0.008 | 0.007042 | 0.0065 | 0.9935 | 0.04906 | 0.05567 |
| `SRSSampling_n16` | 16 | 0.008 | 0.005814 | 0.0435 | 0.9434 | -0.001094 | 0.01672 |
| `pairwise_n16` | 16 | 0.008 | 0.008961 | 0.0475 | 0.9525 | 0.008056 | 0.002694 |
| `pilotCost_n16` | 16 | 0.008 | 0.003954 | 0.078 | 0.8359 | -0.1085 | -0.06318 |
| `cheapOracle_n16` | 16 | 0.008 | 0.00323 | 0.521 | 0.479 | -0.4654 | -0.4028 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.1767 | 0.078 | 0.922 | -0.02244 | -0.07519 |
