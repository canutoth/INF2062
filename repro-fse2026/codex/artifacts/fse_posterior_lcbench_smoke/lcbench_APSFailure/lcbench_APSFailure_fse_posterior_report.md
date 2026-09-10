# lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `expensiveOracle_n16` (risk 0, %cost 0.09872).

Best integrated confidence after normalizing the prior baseline by empirical cost: `balanced_n8` (omega_cost 0.05204, %cost 0.003898).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9499, risk 0.051, %cost 0.003898, omega_cost 0.05204
- `SRSSampling_n8`: posterior area 0.8887, risk 0.088, %cost 0.003205, omega_cost 0.007612
- `pilotCost_n8`: posterior area 0.8438, risk 0.116, %cost 0.002052, omega_cost 0.007649
- `cheapOracle_n8`: posterior area 0.6265, risk 0.3735, %cost 0.00166, omega_cost -0.1855
- `balanced_n16`: posterior area 0.9708, risk 0.0215, %cost 0.00744, omega_cost 0.02999
- `diversity_n16`: posterior area 0.989, risk 0.011, %cost 0.01065, omega_cost 0.0319
- `expensiveOracle_n16`: posterior area 1, risk 0, %cost 0.09872, omega_cost 0.005014

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n8` | `inconclusive` | 11.69 | 0.111 | large (0.1302) | median risks: random=0.1475, balanced=0.051, diversity=0.0765, SRSSampling=0.088, pairwise=0.347, pilotCost=0.116, cheapOracle=0.3735, expensiveOracle=0.0325; spread=0.341 |
| `FSE1` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n16` | `supports` | 17.25 | 0.0158 | large (0.2848) | median risks: random=0.109, balanced=0.0215, diversity=0.011, SRSSampling=0.086, pairwise=0.0535, pilotCost=0.06475, cheapOracle=0.3735, expensiveOracle=0; spread=0.3735 |
| `FSE2` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.07708) | best size-normalized=expensiveOracle_n8; best cost-normalized=balanced_n8 |
| `FSE3` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.04443) | best cost-normalized=balanced_n8; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n8; empirical front=SRSSampling_n8,balanced_n8,cheapOracle_n8,expensiveOracle_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n8` | `inconclusive` | 43.5 | 0.994 | small (0.435) | A12<0.5 means SRS risks tend to be lower; median SRS=0.088, median random=0.1475 |
| `FSE6` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 46.5 | 0.815 | negligible (0.465) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003205, median random=0.003398 |
| `FSE2` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.02944) | best size-normalized=expensiveOracle_n16; best cost-normalized=pilotCost_n16 |
| `FSE3` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.07463) | best cost-normalized=pilotCost_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16,expensiveOracle_n16,pairwise_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n16` | `inconclusive` | 43.5 | 0.994 | small (0.435) | A12<0.5 means SRS risks tend to be lower; median SRS=0.086, median random=0.109 |
| `FSE6` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n16` | `inconclusive` | 43.5 | 0.994 | small (0.565) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007588, median random=0.007443 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003398 | 0.1475 | 0.8706 | -0.02935 | -0.01567 |
| `balanced_n8` | 8 | 0.004 | 0.003898 | 0.051 | 0.9499 | 0.04995 | 0.05204 |
| `diversity_n8` | 8 | 0.004 | 0.007585 | 0.0765 | 0.9235 | 0.0235 | -0.01826 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003205 | 0.088 | 0.8887 | -0.0113 | 0.007612 |
| `pairwise_n8` | 8 | 0.004 | 0.003658 | 0.347 | 0.653 | -0.247 | -0.2397 |
| `pilotCost_n8` | 8 | 0.004 | 0.002052 | 0.116 | 0.8438 | -0.0562 | 0.007649 |
| `cheapOracle_n8` | 8 | 0.004 | 0.00166 | 0.3735 | 0.6265 | -0.2735 | -0.1855 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.06602 | 0.0325 | 0.9675 | 0.0675 | -0.02504 |
| `random_n16` | 16 | 0.008 | 0.007443 | 0.109 | 0.8881 | -0.05634 | -0.05268 |
| `balanced_n16` | 16 | 0.008 | 0.00744 | 0.0215 | 0.9708 | 0.02631 | 0.02999 |
| `diversity_n16` | 16 | 0.008 | 0.01065 | 0.011 | 0.989 | 0.04456 | 0.0319 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007588 | 0.086 | 0.9016 | -0.04284 | -0.04018 |
| `pairwise_n16` | 16 | 0.008 | 0.007207 | 0.0535 | 0.9465 | 0.002056 | 0.007422 |
| `pilotCost_n16` | 16 | 0.008 | 0.003963 | 0.06475 | 0.9337 | -0.01074 | 0.03445 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003395 | 0.3735 | 0.6265 | -0.3179 | -0.2597 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.09872 | 0 | 1 | 0.05556 | 0.005014 |
