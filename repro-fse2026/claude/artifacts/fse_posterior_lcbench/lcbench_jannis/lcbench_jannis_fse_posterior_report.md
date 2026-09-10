# lcbench__workload_jannis__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `expensiveOracle_n16` (risk 0.0015, %cost 0.1002).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n8` (omega_cost 0.0771, %cost 0.00474).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9616, risk 0.036, %cost 0.004313, omega_cost 0.05571
- `diversity_n8`: posterior area 0.99, risk 0.01, %cost 0.00474, omega_cost 0.0771
- `SRSSampling_n8`: posterior area 0.8976, risk 0.0785, %cost 0.003537, omega_cost 0.007848
- `pairwise_n8`: posterior area 0.929, risk 0.071, %cost 0.003803, omega_cost 0.0331
- `pilotCost_n8`: posterior area 0.7927, risk 0.1965, %cost 0.002319, omega_cost -0.05665
- `cheapOracle_n8`: posterior area 0.5245, risk 0.4755, %cost 0.001796, omega_cost -0.2967
- `diversity_n16`: posterior area 0.9915, risk 0.0085, %cost 0.008025, omega_cost 0.0469
- `expensiveOracle_n16`: posterior area 0.9985, risk 0.0015, %cost 0.1002, omega_cost 0.003442
- `diversity_n20`: posterior area 0.998, risk 0.002, %cost 0.01151, omega_cost 0.03796

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n8` | `supports` | 49.46 | 1.85e-08 | large (0.366) | median risks: random=0.08625, balanced=0.036, diversity=0.01, SRSSampling=0.0785, pairwise=0.071, pilotCost=0.1965, cheapOracle=0.4755, expensiveOracle=0.0555; spread=0.4655 |
| `FSE1` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n16` | `supports` | 23.71 | 0.00128 | large (0.144) | median risks: random=0.03925, balanced=0.0285, diversity=0.0085, SRSSampling=0.03925, pairwise=0.0285, pilotCost=0.08725, cheapOracle=0.4755, expensiveOracle=0.0015; spread=0.474 |
| `FSE1` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n20` | `inconclusive` | 12.7 | 0.0798 | large (0.04914) | median risks: random=0.04425, balanced=0.0305, diversity=0.002, SRSSampling=0.05275, pairwise=0.0285, pilotCost=0.01925, cheapOracle=0.4755, expensiveOracle=0.0015; spread=0.474 |
| `FSE1` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n32` | `supports` | 26.15 | 4.73e-04 | large (0.1651) | median risks: random=0.02325, balanced=0.02275, diversity=0.002, SRSSampling=0.01625, pairwise=0.017, pilotCost=0.071, cheapOracle=0.4755, expensiveOracle=0.0015; spread=0.474 |
| `FSE1` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n40` | `supports` | 23.36 | 0.00147 | large (0.1411) | median risks: random=0.015, balanced=0.018, diversity=0.002, SRSSampling=0.019, pairwise=0.017, pilotCost=0.05525, cheapOracle=0.461, expensiveOracle=0.0015; spread=0.4595 |
| `FSE1` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 13.45 | 0.0618 | large (0.05565) | median risks: random=0.00975, balanced=0.0055, diversity=0.002, SRSSampling=0.0085, pairwise=0.017, pilotCost=0.01, cheapOracle=0.4285, expensiveOracle=0.0015; spread=0.427 |
| `FSE2` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n8; best cost-normalized=diversity_n8 |
| `FSE3` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.06925) | best cost-normalized=diversity_n8; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.1667 |  | large frontier change (5) | count front=diversity_n8; empirical front=SRSSampling_n8,balanced_n8,cheapOracle_n8,diversity_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 428.5 | 0.856 | negligible (0.4761) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0785, median random=0.08625 |
| `FSE6` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 434.5 | 0.787 | negligible (0.4828) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003537, median random=0.003637 |
| `FSE2` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.04346) | best size-normalized=expensiveOracle_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.05492) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n16; empirical front=cheapOracle_n16,diversity_n16,expensiveOracle_n16,pairwise_n16,pilotCost_n16,random_n16 |
| `FSE5` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 449.5 | 0.622 | negligible (0.4994) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03925, median random=0.03925 |
| `FSE6` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 427.5 | 0.867 | negligible (0.525) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007362, median random=0.007277 |
| `FSE2` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.03492) | best size-normalized=expensiveOracle_n20; best cost-normalized=diversity_n20 |
| `FSE3` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.04884) | best cost-normalized=diversity_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n20; empirical front=cheapOracle_n20,diversity_n20,expensiveOracle_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 437 | 0.758 | negligible (0.5144) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05275, median random=0.04425 |
| `FSE6` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 434.5 | 0.787 | negligible (0.4828) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009166, median random=0.009199 |
| `FSE2` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.02292) | best size-normalized=expensiveOracle_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.01894) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n32; empirical front=balanced_n32,cheapOracle_n32,diversity_n32,expensiveOracle_n32,pairwise_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 312.5 | 0.125 | medium (0.3472) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01625, median random=0.02325 |
| `FSE6` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 375 | 0.543 | small (0.5833) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01521, median random=0.01471 |
| `FSE2` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.01551) | best size-normalized=expensiveOracle_n40; best cost-normalized=diversity_n40 |
| `FSE3` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.01345) | best cost-normalized=diversity_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n40; empirical front=balanced_n40,cheapOracle_n40,diversity_n40,expensiveOracle_n40,pairwise_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 411.5 | 0.945 | negligible (0.5428) | A12<0.5 means SRS risks tend to be lower; median SRS=0.019, median random=0.015 |
| `FSE6` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 449 | 0.628 | negligible (0.4989) | A12>0.5 means SRS costs tend to be higher; median SRS=0.019, median random=0.01884 |
| `FSE2` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.009926) | best size-normalized=expensiveOracle_n64; best cost-normalized=diversity_n64 |
| `FSE3` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | moderate (0.006634) | best cost-normalized=diversity_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n64; empirical front=balanced_n64,cheapOracle_n64,diversity_n64,expensiveOracle_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 419 | 0.967 | negligible (0.4656) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0085, median random=0.00975 |
| `FSE6` | `lcbench__workload_jannis__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 401 | 0.822 | negligible (0.4456) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03048, median random=0.03074 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003637 | 0.08625 | 0.8936 | -0.006367 | 0.001452 |
| `balanced_n8` | 8 | 0.004 | 0.004313 | 0.036 | 0.9616 | 0.0616 | 0.05571 |
| `diversity_n8` | 8 | 0.004 | 0.00474 | 0.01 | 0.99 | 0.09 | 0.0771 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003537 | 0.0785 | 0.8976 | -0.002367 | 0.007848 |
| `pairwise_n8` | 8 | 0.004 | 0.003803 | 0.071 | 0.929 | 0.029 | 0.0331 |
| `pilotCost_n8` | 8 | 0.004 | 0.002319 | 0.1965 | 0.7927 | -0.1073 | -0.05665 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001796 | 0.4755 | 0.5245 | -0.3755 | -0.2967 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.07138 | 0.0555 | 0.9445 | 0.0445 | -0.04859 |
| `random_n16` | 16 | 0.008 | 0.007277 | 0.03925 | 0.9301 | -0.01436 | -0.009507 |
| `balanced_n16` | 16 | 0.008 | 0.007548 | 0.0285 | 0.971 | 0.02657 | 0.02951 |
| `diversity_n16` | 16 | 0.008 | 0.008025 | 0.0085 | 0.9915 | 0.04706 | 0.0469 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007362 | 0.03925 | 0.9322 | -0.01226 | -0.008024 |
| `pairwise_n16` | 16 | 0.008 | 0.007289 | 0.0285 | 0.9715 | 0.02706 | 0.03182 |
| `pilotCost_n16` | 16 | 0.008 | 0.004548 | 0.08725 | 0.8834 | -0.06099 | -0.02643 |
| `cheapOracle_n16` | 16 | 0.008 | 0.00369 | 0.4755 | 0.5245 | -0.4199 | -0.3689 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.1002 | 0.0015 | 0.9985 | 0.05406 | 0.003442 |
| `random_n20` | 20 | 0.01 | 0.009199 | 0.04425 | 0.9415 | -0.01308 | -0.009509 |
| `balanced_n20` | 20 | 0.01 | 0.008949 | 0.0305 | 0.9701 | 0.01559 | 0.02039 |
| `diversity_n20` | 20 | 0.01 | 0.01151 | 0.002 | 0.998 | 0.04345 | 0.03796 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009166 | 0.05275 | 0.9399 | -0.01461 | -0.01088 |
| `pairwise_n20` | 20 | 0.01 | 0.0089 | 0.0285 | 0.9715 | 0.01695 | 0.02201 |
| `pilotCost_n20` | 20 | 0.01 | 0.005948 | 0.01925 | 0.9351 | -0.01948 | 0.007033 |
| `cheapOracle_n20` | 20 | 0.01 | 0.004647 | 0.4755 | 0.5245 | -0.43 | -0.387 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.1092 | 0.0015 | 0.9985 | 0.04395 | 0.003037 |
| `random_n32` | 32 | 0.016 | 0.01471 | 0.02325 | 0.965 | -0.005588 | -0.003172 |
| `balanced_n32` | 32 | 0.016 | 0.01358 | 0.02275 | 0.9743 | 0.003678 | 0.008554 |
| `diversity_n32` | 32 | 0.016 | 0.01741 | 0.002 | 0.998 | 0.02741 | 0.02516 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01521 | 0.01625 | 0.9754 | 0.004795 | 0.00622 |
| `pairwise_n32` | 32 | 0.016 | 0.01509 | 0.017 | 0.983 | 0.01241 | 0.01407 |
| `pilotCost_n32` | 32 | 0.016 | 0.009176 | 0.071 | 0.9219 | -0.04869 | -0.02896 |
| `cheapOracle_n32` | 32 | 0.016 | 0.007556 | 0.4755 | 0.5245 | -0.4461 | -0.4171 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.1328 | 0.0015 | 0.9985 | 0.02791 | 0.002238 |
| `random_n40` | 40 | 0.02 | 0.01884 | 0.015 | 0.9788 | 0.002626 | 0.004016 |
| `balanced_n40` | 40 | 0.02 | 0.01649 | 0.018 | 0.9808 | 0.004626 | 0.009398 |
| `diversity_n40` | 40 | 0.02 | 0.02478 | 0.002 | 0.998 | 0.02181 | 0.01739 |
| `SRSSampling_n40` | 40 | 0.02 | 0.019 | 0.019 | 0.9789 | 0.002743 | 0.003939 |
| `pairwise_n40` | 40 | 0.02 | 0.01923 | 0.017 | 0.983 | 0.00681 | 0.007716 |
| `pilotCost_n40` | 40 | 0.02 | 0.01128 | 0.05525 | 0.9372 | -0.03902 | -0.02211 |
| `cheapOracle_n40` | 40 | 0.02 | 0.009511 | 0.461 | 0.539 | -0.4372 | -0.4134 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.1467 | 0.0015 | 0.9985 | 0.02231 | 0.001885 |
| `random_n64` | 64 | 0.032 | 0.03074 | 0.00975 | 0.985 | 0.0001515 | 0.0007545 |
| `balanced_n64` | 64 | 0.032 | 0.02569 | 0.0055 | 0.9918 | 0.006985 | 0.01057 |
| `diversity_n64` | 64 | 0.032 | 0.03707 | 0.002 | 0.998 | 0.01315 | 0.01113 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03048 | 0.0085 | 0.9886 | 0.003768 | 0.004501 |
| `pairwise_n64` | 64 | 0.032 | 0.02932 | 0.017 | 0.983 | -0.001848 | -0.0005077 |
| `pilotCost_n64` | 64 | 0.032 | 0.0185 | 0.01 | 0.974 | -0.01085 | -0.0003624 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01542 | 0.4285 | 0.5715 | -0.4133 | -0.3981 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.1836 | 0.0015 | 0.9985 | 0.01365 | 0.001209 |
