# lcbench__workload_dionis__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n8` (risk 0.004, %cost 0.006349).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pilotCost_n8` (omega_cost 0.09402, %cost 0.002093).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.996, risk 0.004, %cost 0.006349, omega_cost 0.06404
- `pilotCost_n8`: posterior area 0.9324, risk 0.0475, %cost 0.002093, omega_cost 0.09402
- `pilotCost_n16`: posterior area 0.9543, risk 0.041, %cost 0.004121, omega_cost 0.05193
- `pilotCost_n20`: posterior area 0.9744, risk 0.0215, %cost 0.005507, omega_cost 0.0512

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n8` | `supports` | 14.33 | 0.0137 | large (0.08041) | median risks: random=0.08625, balanced=0.094, diversity=0.004, SRSSampling=0.07875, pairwise=0.201, pilotCost=0.0475; spread=0.197 |
| `FSE1` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n16` | `inconclusive` | 10.35 | 0.0658 | large (0.04616) | median risks: random=0.03875, balanced=0.0515, diversity=0.004, SRSSampling=0.03875, pairwise=0.093, pilotCost=0.041; spread=0.089 |
| `FSE1` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n20` | `supports` | 16.33 | 0.00595 | large (0.09771) | median risks: random=0.04225, balanced=0.028, diversity=0.004, SRSSampling=0.04325, pairwise=0.093, pilotCost=0.0215; spread=0.089 |
| `FSE1` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 9.35 | 0.0959 | large (0.0375) | median risks: random=0.0215, balanced=0.0265, diversity=0.004, SRSSampling=0.025, pairwise=0.093, pilotCost=0.0155; spread=0.089 |
| `FSE1` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 4.145 | 0.529 | moderate (0) | median risks: random=0.0145, balanced=0.00975, diversity=0.004, SRSSampling=0.01525, pairwise=0.019, pilotCost=0.0155; spread=0.015 |
| `FSE1` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n64` | `supports` | 20.43 | 0.00104 | moderate (0.1331) | median risks: random=0.0095, balanced=0.004, diversity=0.004, SRSSampling=0.01225, pairwise=0.019, pilotCost=0.00425; spread=0.015 |
| `FSE2` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.02998) | best size-normalized=diversity_n8; best cost-normalized=pilotCost_n8 |
| `FSE3` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.1143) | best cost-normalized=pilotCost_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n8; empirical front=diversity_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 440.5 | 0.719 | negligible (0.4894) | A12<0.5 means SRS risks tend to be lower; median SRS=0.07875, median random=0.08625 |
| `FSE6` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 435 | 0.781 | negligible (0.4833) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003574, median random=0.003656 |
| `FSE2` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.005105) | best size-normalized=diversity_n16; best cost-normalized=pilotCost_n16 |
| `FSE3` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.0401) | best cost-normalized=pilotCost_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n16; empirical front=diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 449.5 | 0.622 | negligible (0.5006) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03875, median random=0.03875 |
| `FSE6` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 434.5 | 0.787 | negligible (0.5172) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007394, median random=0.007254 |
| `FSE2` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.02247) | best size-normalized=diversity_n20; best cost-normalized=pilotCost_n20 |
| `FSE3` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.05549) | best cost-normalized=pilotCost_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n20; empirical front=diversity_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 438.5 | 0.741 | negligible (0.5128) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04325, median random=0.04225 |
| `FSE6` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 433.5 | 0.798 | negligible (0.4817) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009678, median random=0.009924 |
| `FSE2` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.01259) | best size-normalized=diversity_n32; best cost-normalized=pilotCost_n32 |
| `FSE3` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02984) | best cost-normalized=pilotCost_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n32; empirical front=diversity_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 426 | 0.885 | negligible (0.5267) | A12<0.5 means SRS risks tend to be lower; median SRS=0.025, median random=0.0215 |
| `FSE6` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 351 | 0.335 | small (0.39) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01436, median random=0.01527 |
| `FSE2` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.01728) | best size-normalized=diversity_n40; best cost-normalized=pilotCost_n40 |
| `FSE3` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.02683) | best cost-normalized=pilotCost_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n40; empirical front=diversity_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 397 | 0.777 | negligible (0.5589) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01525, median random=0.0145 |
| `FSE6` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n40` | `supports` | 253 | 0.0158 | large (0.2811) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01715, median random=0.02032 |
| `FSE2` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.01081) | best size-normalized=diversity_n64; best cost-normalized=pilotCost_n64 |
| `FSE3` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01574) | best cost-normalized=pilotCost_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n64; empirical front=balanced_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 393 | 0.731 | small (0.5633) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01225, median random=0.0095 |
| `FSE6` | `lcbench__workload_dionis__cost_time_total__target_final_val_accuracy:n64` | `supports` | 197 | 0.00119 | large (0.2189) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02661, median random=0.03424 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003656 | 0.08625 | 0.868 | -0.03197 | -0.02457 |
| `balanced_n8` | 8 | 0.004 | 0.004345 | 0.094 | 0.8816 | -0.0184 | -0.02485 |
| `diversity_n8` | 8 | 0.004 | 0.006349 | 0.004 | 0.996 | 0.096 | 0.06404 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003574 | 0.07875 | 0.8704 | -0.0296 | -0.02029 |
| `pairwise_n8` | 8 | 0.004 | 0.004005 | 0.201 | 0.799 | -0.101 | -0.1011 |
| `pilotCost_n8` | 8 | 0.004 | 0.002093 | 0.0475 | 0.9324 | 0.03237 | 0.09402 |
| `random_n16` | 16 | 0.008 | 0.007254 | 0.03875 | 0.9528 | 0.008322 | 0.01335 |
| `balanced_n16` | 16 | 0.008 | 0.007458 | 0.0515 | 0.9304 | -0.01401 | -0.01045 |
| `diversity_n16` | 16 | 0.008 | 0.008837 | 0.004 | 0.996 | 0.05156 | 0.04683 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007394 | 0.03875 | 0.9523 | 0.007822 | 0.01183 |
| `pairwise_n16` | 16 | 0.008 | 0.007175 | 0.093 | 0.907 | -0.03744 | -0.03184 |
| `pilotCost_n16` | 16 | 0.008 | 0.004121 | 0.041 | 0.9543 | 0.009856 | 0.05193 |
| `random_n20` | 20 | 0.01 | 0.009924 | 0.04225 | 0.9502 | -0.004395 | -0.004081 |
| `balanced_n20` | 20 | 0.01 | 0.008538 | 0.028 | 0.9463 | -0.008295 | -0.001329 |
| `diversity_n20` | 20 | 0.01 | 0.01428 | 0.004 | 0.996 | 0.04145 | 0.02873 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009678 | 0.04325 | 0.9489 | -0.005662 | -0.00429 |
| `pairwise_n20` | 20 | 0.01 | 0.01124 | 0.093 | 0.907 | -0.04755 | -0.05217 |
| `pilotCost_n20` | 20 | 0.01 | 0.005507 | 0.0215 | 0.9744 | 0.01982 | 0.0512 |
| `random_n32` | 32 | 0.016 | 0.01527 | 0.0215 | 0.9715 | 0.0008784 | 0.002203 |
| `balanced_n32` | 32 | 0.016 | 0.01325 | 0.0265 | 0.9589 | -0.01172 | -0.006056 |
| `diversity_n32` | 32 | 0.016 | 0.02118 | 0.004 | 0.996 | 0.02541 | 0.01854 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01436 | 0.025 | 0.9687 | -0.001855 | 0.001291 |
| `pairwise_n32` | 32 | 0.016 | 0.0154 | 0.093 | 0.907 | -0.06359 | -0.06251 |
| `pilotCost_n32` | 32 | 0.016 | 0.008379 | 0.0155 | 0.9778 | 0.007228 | 0.03113 |
| `random_n40` | 40 | 0.02 | 0.02032 | 0.0145 | 0.9791 | 0.00296 | 0.002601 |
| `balanced_n40` | 40 | 0.02 | 0.01681 | 0.00975 | 0.9822 | 0.00606 | 0.01033 |
| `diversity_n40` | 40 | 0.02 | 0.03389 | 0.004 | 0.996 | 0.01981 | 0.01033 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01715 | 0.01525 | 0.9732 | -0.002957 | 0.000777 |
| `pairwise_n40` | 40 | 0.02 | 0.01896 | 0.019 | 0.981 | 0.00481 | 0.006051 |
| `pilotCost_n40` | 40 | 0.02 | 0.01016 | 0.0155 | 0.9828 | 0.006626 | 0.02761 |
| `random_n64` | 64 | 0.032 | 0.03424 | 0.0095 | 0.9846 | -0.0002152 | -0.001177 |
| `balanced_n64` | 64 | 0.032 | 0.02596 | 0.004 | 0.9949 | 0.01 | 0.01339 |
| `diversity_n64` | 64 | 0.032 | 0.04511 | 0.004 | 0.996 | 0.01115 | 0.006844 |
| `SRSSampling_n64` | 64 | 0.032 | 0.02661 | 0.01225 | 0.9838 | -0.001048 | 0.001907 |
| `pairwise_n64` | 64 | 0.032 | 0.02638 | 0.019 | 0.981 | -0.003848 | -0.0007396 |
| `pilotCost_n64` | 64 | 0.032 | 0.01705 | 0.00425 | 0.9899 | 0.005102 | 0.01765 |
