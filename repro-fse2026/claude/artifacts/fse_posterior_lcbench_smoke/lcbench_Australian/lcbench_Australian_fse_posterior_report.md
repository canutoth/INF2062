# lcbench__workload_Australian__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `expensiveOracle_n8` (risk 0.001, %cost 0.02935).

Best integrated confidence after normalizing the prior baseline by empirical cost: `cheapOracle_n8` (omega_cost 0.1382, %cost 0.001887).

Empirical cost/confidence Pareto front:

- `cheapOracle_n8`: posterior area 0.965, risk 0.035, %cost 0.001887, omega_cost 0.1382
- `balanced_n16`: posterior area 0.978, risk 0.001, %cost 0.005232, omega_cost 0.05828
- `diversity_n16`: posterior area 0.999, risk 0.001, %cost 0.007771, omega_cost 0.056

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 4.23 | 0.753 | large (0) | median risks: random=0.035, balanced=0.05475, diversity=0.035, SRSSampling=0.035, pairwise=0.035, pilotCost=0.035, cheapOracle=0.035, expensiveOracle=0.001; spread=0.05375 |
| `FSE1` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 6.84 | 0.446 | moderate (0) | median risks: random=0.035, balanced=0.001, diversity=0.001, SRSSampling=0.035, pairwise=0.035, pilotCost=0.035, cheapOracle=0.035, expensiveOracle=0.001; spread=0.034 |
| `FSE2` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.1227) | best size-normalized=expensiveOracle_n8; best cost-normalized=cheapOracle_n8 |
| `FSE3` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.1007) | best cost-normalized=cheapOracle_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.5 |  | frontier change (1) | count front=expensiveOracle_n8; empirical front=cheapOracle_n8,expensiveOracle_n8 |
| `FSE5` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 46.5 | 0.827 | negligible (0.535) | A12<0.5 means SRS risks tend to be lower; median SRS=0.035, median random=0.035 |
| `FSE6` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 47.5 | 0.756 | negligible (0.475) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003215, median random=0.003523 |
| `FSE2` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.009741) | best size-normalized=diversity_n16; best cost-normalized=cheapOracle_n16 |
| `FSE3` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.06202) | best cost-normalized=cheapOracle_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n16,expensiveOracle_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16 |
| `FSE5` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 48.5 | 0.703 | negligible (0.485) | A12<0.5 means SRS risks tend to be lower; median SRS=0.035, median random=0.035 |
| `FSE6` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 44.5 | 0.934 | negligible (0.555) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007792, median random=0.007479 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003523 | 0.035 | 0.9397 | 0.0397 | 0.05024 |
| `balanced_n8` | 8 | 0.004 | 0.002615 | 0.05475 | 0.9453 | 0.04525 | 0.08356 |
| `diversity_n8` | 8 | 0.004 | 0.004894 | 0.035 | 0.965 | 0.065 | 0.04983 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003215 | 0.035 | 0.9188 | 0.01885 | 0.03748 |
| `pairwise_n8` | 8 | 0.004 | 0.003314 | 0.035 | 0.965 | 0.065 | 0.08091 |
| `pilotCost_n8` | 8 | 0.004 | 0.00232 | 0.035 | 0.923 | 0.023 | 0.07358 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001887 | 0.035 | 0.965 | 0.065 | 0.1382 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.02935 | 0.001 | 0.999 | 0.099 | 0.01547 |
| `random_n16` | 16 | 0.008 | 0.007479 | 0.035 | 0.9405 | -0.003894 | -0.0004819 |
| `balanced_n16` | 16 | 0.008 | 0.005232 | 0.001 | 0.978 | 0.03361 | 0.05828 |
| `diversity_n16` | 16 | 0.008 | 0.007771 | 0.001 | 0.999 | 0.05456 | 0.056 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007792 | 0.035 | 0.9468 | 0.002406 | 0.003722 |
| `pairwise_n16` | 16 | 0.008 | 0.007416 | 0.035 | 0.965 | 0.02056 | 0.02441 |
| `pilotCost_n16` | 16 | 0.008 | 0.00471 | 0.035 | 0.9497 | 0.005306 | 0.03731 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003963 | 0.035 | 0.965 | 0.02056 | 0.06575 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.05589 | 0.001 | 0.999 | 0.05456 | 0.00779 |
