# lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `random_n8` (risk 0, %cost 0.003681).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pairwise_n8` (omega_cost 0.1089, %cost 0.003592).

Empirical cost/confidence Pareto front:

- `SRSSampling_n8`: posterior area 0.9842, risk 0, %cost 0.003444, omega_cost 0.09676
- `pairwise_n8`: posterior area 1, risk 0, %cost 0.003592, omega_cost 0.1089
- `pilotCost_n8`: posterior area 0.5916, risk 0.372, %cost 0.001986, omega_cost -0.241
- `cheapOracle_n8`: posterior area 0.2175, risk 0.7825, %cost 0.001704, omega_cost -0.5976

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n8` | `supports` | 32.67 | 3.05e-05 | large (0.7131) | median risks: random=0, balanced=0, diversity=0, SRSSampling=0, pairwise=0, pilotCost=0.372, cheapOracle=0.7825, expensiveOracle=0; spread=0.7825 |
| `FSE1` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n16` | `supports` | 37.66 | 3.51e-06 | large (0.8518) | median risks: random=0, balanced=0, diversity=0, SRSSampling=0, pairwise=0, pilotCost=0.353, cheapOracle=0.7825, expensiveOracle=0; spread=0.7825 |
| `FSE2` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.004647) | best size-normalized=balanced_n8; best cost-normalized=pairwise_n8 |
| `FSE3` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.01213) | best cost-normalized=pairwise_n8; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.1429 |  | large frontier change (6) | count front=balanced_n8,diversity_n8,expensiveOracle_n8,pairwise_n8; empirical front=SRSSampling_n8,cheapOracle_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 50 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 48.5 | 0.699 | negligible (0.485) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003444, median random=0.003681 |
| `FSE2` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=balanced_n16; best cost-normalized=balanced_n16 |
| `FSE3` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.01834) | best cost-normalized=balanced_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.1667 |  | large frontier change (5) | count front=balanced_n16,diversity_n16,expensiveOracle_n16,pairwise_n16; empirical front=balanced_n16,cheapOracle_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 50 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 45.5 | 0.874 | negligible (0.545) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007386, median random=0.007097 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003681 | 0 | 0.9842 | 0.08425 | 0.09106 |
| `balanced_n8` | 8 | 0.004 | 0.003797 | 0 | 1 | 0.1 | 0.1042 |
| `diversity_n8` | 8 | 0.004 | 0.005375 | 0 | 1 | 0.1 | 0.07843 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003444 | 0 | 0.9842 | 0.08425 | 0.09676 |
| `pairwise_n8` | 8 | 0.004 | 0.003592 | 0 | 1 | 0.1 | 0.1089 |
| `pilotCost_n8` | 8 | 0.004 | 0.001986 | 0.372 | 0.5916 | -0.3085 | -0.241 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001704 | 0.7825 | 0.2175 | -0.6825 | -0.5976 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.05849 | 0 | 1 | 0.1 | 0.008405 |
| `random_n16` | 16 | 0.008 | 0.007097 | 0 | 0.9839 | 0.03951 | 0.0457 |
| `balanced_n16` | 16 | 0.008 | 0.007077 | 0 | 1 | 0.05556 | 0.06191 |
| `diversity_n16` | 16 | 0.008 | 0.008536 | 0 | 1 | 0.05556 | 0.05243 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007386 | 0 | 0.9839 | 0.03951 | 0.04357 |
| `pairwise_n16` | 16 | 0.008 | 0.007302 | 0 | 1 | 0.05556 | 0.06023 |
| `pilotCost_n16` | 16 | 0.008 | 0.003993 | 0.353 | 0.6387 | -0.3057 | -0.2611 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003467 | 0.7825 | 0.2175 | -0.7269 | -0.6706 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.08462 | 0 | 1 | 0.05556 | 0.00584 |
