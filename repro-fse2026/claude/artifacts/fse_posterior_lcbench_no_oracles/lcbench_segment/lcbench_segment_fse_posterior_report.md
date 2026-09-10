# lcbench__workload_segment__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n20` (risk 0, %cost 0.01257).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pairwise_n8` (omega_cost 0.08876, %cost 0.003395).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9258, risk 0.0775, %cost 0.002807, omega_cost 0.05713
- `diversity_n8`: posterior area 0.99, risk 0.01, %cost 0.005092, omega_cost 0.07207
- `pairwise_n8`: posterior area 0.975, risk 0.025, %cost 0.003395, omega_cost 0.08876
- `pilotCost_n8`: posterior area 0.9096, risk 0.0775, %cost 0.002333, omega_cost 0.05965
- `diversity_n16`: posterior area 0.9935, risk 0.0065, %cost 0.007926, omega_cost 0.04952
- `diversity_n20`: posterior area 1, risk 0, %cost 0.01257, omega_cost 0.03685

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n8` | `inconclusive` | 6.785 | 0.237 | large (0.01539) | median risks: random=0.0885, balanced=0.0775, diversity=0.01, SRSSampling=0.083, pairwise=0.025, pilotCost=0.0775; spread=0.0785 |
| `FSE1` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 5.277 | 0.383 | large (0.002386) | median risks: random=0.05125, balanced=0.028, diversity=0.0065, SRSSampling=0.04925, pairwise=0.015, pilotCost=0.064; spread=0.0575 |
| `FSE1` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n20` | `supports` | 14.42 | 0.0131 | large (0.08123) | median risks: random=0.051, balanced=0.0315, diversity=0, SRSSampling=0.051, pairwise=0.015, pilotCost=0.0175; spread=0.051 |
| `FSE1` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 7.711 | 0.173 | moderate (0.02337) | median risks: random=0.021, balanced=0.009, diversity=0, SRSSampling=0.01375, pairwise=0.015, pilotCost=0.0315; spread=0.0315 |
| `FSE1` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 4.706 | 0.453 | moderate (0) | median risks: random=0.01375, balanced=0.009, diversity=0, SRSSampling=0.0125, pairwise=0.015, pilotCost=0.02; spread=0.02 |
| `FSE1` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 6.691 | 0.245 | moderate (0.01457) | median risks: random=0.01125, balanced=0.0065, diversity=0, SRSSampling=0.008, pairwise=0.015, pilotCost=0.0045; spread=0.015 |
| `FSE2` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.01669) | best size-normalized=diversity_n8; best cost-normalized=pairwise_n8 |
| `FSE3` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.09925) | best cost-normalized=pairwise_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n8; empirical front=balanced_n8,diversity_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 429.5 | 0.844 | negligible (0.4772) | A12<0.5 means SRS risks tend to be lower; median SRS=0.083, median random=0.0885 |
| `FSE6` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 440.5 | 0.719 | negligible (0.4894) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003784, median random=0.00385 |
| `FSE2` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.04705) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n16; empirical front=balanced_n16,diversity_n16,pairwise_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 435.5 | 0.776 | negligible (0.4839) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04925, median random=0.05125 |
| `FSE6` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 437.5 | 0.753 | negligible (0.5139) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007704, median random=0.007663 |
| `FSE2` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n20; best cost-normalized=diversity_n20 |
| `FSE3` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.0578) | best cost-normalized=diversity_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n20; empirical front=diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 440 | 0.725 | negligible (0.5111) | A12<0.5 means SRS risks tend to be lower; median SRS=0.051, median random=0.051 |
| `FSE6` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 446.5 | 0.654 | negligible (0.4961) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009712, median random=0.009712 |
| `FSE2` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02145) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n32; empirical front=balanced_n32,diversity_n32,pairwise_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 338.5 | 0.25 | small (0.3761) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01375, median random=0.021 |
| `FSE6` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 446 | 0.659 | negligible (0.5044) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01564, median random=0.01513 |
| `FSE2` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n40; best cost-normalized=diversity_n40 |
| `FSE3` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.01561) | best cost-normalized=diversity_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n40; empirical front=balanced_n40,diversity_n40,pairwise_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 432.5 | 0.81 | negligible (0.5194) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0125, median random=0.01375 |
| `FSE6` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 326 | 0.182 | small (0.3622) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01844, median random=0.02019 |
| `FSE2` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.004081) | best size-normalized=diversity_n64; best cost-normalized=pilotCost_n64 |
| `FSE3` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01149) | best cost-normalized=pilotCost_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n64; empirical front=diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 386.5 | 0.659 | small (0.4294) | A12<0.5 means SRS risks tend to be lower; median SRS=0.008, median random=0.01125 |
| `FSE6` | `lcbench__workload_segment__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 305 | 0.1 | medium (0.3389) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03023, median random=0.03252 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.00385 | 0.0885 | 0.8789 | -0.0211 | -0.018 |
| `balanced_n8` | 8 | 0.004 | 0.002807 | 0.0775 | 0.9258 | 0.02578 | 0.05713 |
| `diversity_n8` | 8 | 0.004 | 0.005092 | 0.01 | 0.99 | 0.09 | 0.07207 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003784 | 0.083 | 0.885 | -0.01502 | -0.01049 |
| `pairwise_n8` | 8 | 0.004 | 0.003395 | 0.025 | 0.975 | 0.075 | 0.08876 |
| `pilotCost_n8` | 8 | 0.004 | 0.002333 | 0.0775 | 0.9096 | 0.009633 | 0.05965 |
| `random_n16` | 16 | 0.008 | 0.007663 | 0.05125 | 0.9398 | -0.004594 | -0.00243 |
| `balanced_n16` | 16 | 0.008 | 0.005405 | 0.028 | 0.9576 | 0.01316 | 0.03566 |
| `diversity_n16` | 16 | 0.008 | 0.007926 | 0.0065 | 0.9935 | 0.04906 | 0.04952 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007704 | 0.04925 | 0.945 | 0.0005722 | 0.002463 |
| `pairwise_n16` | 16 | 0.008 | 0.007299 | 0.015 | 0.985 | 0.04056 | 0.04525 |
| `pilotCost_n16` | 16 | 0.008 | 0.004689 | 0.064 | 0.9469 | 0.002456 | 0.03478 |
| `random_n20` | 20 | 0.01 | 0.009712 | 0.051 | 0.9334 | -0.02116 | -0.01994 |
| `balanced_n20` | 20 | 0.01 | 0.006559 | 0.0315 | 0.9592 | 0.004638 | 0.02533 |
| `diversity_n20` | 20 | 0.01 | 0.01257 | 0 | 1 | 0.04545 | 0.03685 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009712 | 0.051 | 0.9324 | -0.02216 | -0.02094 |
| `pairwise_n20` | 20 | 0.01 | 0.008977 | 0.015 | 0.985 | 0.03045 | 0.03511 |
| `pilotCost_n20` | 20 | 0.01 | 0.005929 | 0.0175 | 0.9619 | 0.007371 | 0.03407 |
| `random_n32` | 32 | 0.016 | 0.01513 | 0.021 | 0.9612 | -0.009355 | -0.007768 |
| `balanced_n32` | 32 | 0.016 | 0.01047 | 0.009 | 0.9724 | 0.001845 | 0.01601 |
| `diversity_n32` | 32 | 0.016 | 0.0198 | 0 | 1 | 0.02941 | 0.02404 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01564 | 0.01375 | 0.9725 | 0.001945 | 0.002583 |
| `pairwise_n32` | 32 | 0.016 | 0.01503 | 0.015 | 0.985 | 0.01441 | 0.0162 |
| `pilotCost_n32` | 32 | 0.016 | 0.009477 | 0.0315 | 0.9651 | -0.005488 | 0.01282 |
| `random_n40` | 40 | 0.02 | 0.02019 | 0.01375 | 0.9779 | 0.00176 | 0.001549 |
| `balanced_n40` | 40 | 0.02 | 0.01346 | 0.009 | 0.9762 | 2.619e-05 | 0.01079 |
| `diversity_n40` | 40 | 0.02 | 0.02953 | 0 | 1 | 0.02381 | 0.01638 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01844 | 0.0125 | 0.975 | -0.00114 | 0.0007674 |
| `pairwise_n40` | 40 | 0.02 | 0.0184 | 0.015 | 0.985 | 0.00881 | 0.01078 |
| `pilotCost_n40` | 40 | 0.02 | 0.01174 | 0.02 | 0.9743 | -0.001907 | 0.01353 |
| `random_n64` | 64 | 0.032 | 0.03252 | 0.01125 | 0.9855 | 0.0006348 | 0.0003983 |
| `balanced_n64` | 64 | 0.032 | 0.02248 | 0.0065 | 0.9879 | 0.003085 | 0.009231 |
| `diversity_n64` | 64 | 0.032 | 0.04105 | 0 | 1 | 0.01515 | 0.01189 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03023 | 0.008 | 0.9885 | 0.003618 | 0.004477 |
| `pairwise_n64` | 64 | 0.032 | 0.03031 | 0.015 | 0.985 | 0.0001515 | 0.0009704 |
| `pilotCost_n64` | 64 | 0.032 | 0.01896 | 0.0045 | 0.9909 | 0.006068 | 0.01597 |
