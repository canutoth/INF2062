# lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `expensiveOracle_n64` (risk 0, %cost 0.1648).

Best integrated confidence after normalizing the prior baseline by empirical cost: `balanced_n8` (omega_cost 0.09923, %cost 0.002725).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.965, risk 0.023, %cost 0.002725, omega_cost 0.09923
- `diversity_n8`: posterior area 0.977, risk 0.023, %cost 0.005124, omega_cost 0.05864
- `cheapOracle_n8`: posterior area 0.9205, risk 0.0795, %cost 0.001893, omega_cost 0.09332
- `diversity_n16`: posterior area 0.9885, risk 0.0115, %cost 0.008034, omega_cost 0.04385
- `pairwise_n40`: posterior area 0.992, risk 0.008, %cost 0.01883, omega_cost 0.01722
- `diversity_n64`: posterior area 0.9975, risk 0.0025, %cost 0.04105, omega_cost 0.009391
- `expensiveOracle_n64`: posterior area 1, risk 0, %cost 0.1648, omega_cost 0.003016

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n8` | `supports` | 15.67 | 0.0283 | large (0.07471) | median risks: random=0.042, balanced=0.023, diversity=0.023, SRSSampling=0.042, pairwise=0.0795, pilotCost=0.13, cheapOracle=0.0795, expensiveOracle=0.13; spread=0.107 |
| `FSE1` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 7.996 | 0.333 | large (0.00859) | median risks: random=0.042, balanced=0.023, diversity=0.0115, SRSSampling=0.042, pairwise=0.042, pilotCost=0.042, cheapOracle=0.0795, expensiveOracle=0.0115; spread=0.068 |
| `FSE1` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 3.818 | 0.8 | large (0) | median risks: random=0.023, balanced=0.042, diversity=0.0115, SRSSampling=0.023, pairwise=0.042, pilotCost=0.042, cheapOracle=0.0795, expensiveOracle=0.0115; spread=0.068 |
| `FSE1` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 8.475 | 0.293 | large (0.01271) | median risks: random=0.023, balanced=0.023, diversity=0.0115, SRSSampling=0.023, pairwise=0.042, pilotCost=0.023, cheapOracle=0.0795, expensiveOracle=0.005; spread=0.0745 |
| `FSE1` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 8.989 | 0.253 | moderate (0.01715) | median risks: random=0.0115, balanced=0.0115, diversity=0.0115, SRSSampling=0.0115, pairwise=0.008, pilotCost=0.042, cheapOracle=0.042, expensiveOracle=0.005; spread=0.037 |
| `FSE1` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 7.937 | 0.338 | moderate (0.008076) | median risks: random=0.008, balanced=0.005, diversity=0.0025, SRSSampling=0.00975, pairwise=0.008, pilotCost=0.0115, cheapOracle=0.0115, expensiveOracle=0; spread=0.0115 |
| `FSE2` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.04059) | best size-normalized=diversity_n8; best cost-normalized=balanced_n8 |
| `FSE3` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.0794) | best cost-normalized=balanced_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n8; empirical front=balanced_n8,cheapOracle_n8,diversity_n8 |
| `FSE5` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 448.5 | 0.633 | negligible (0.4983) | A12<0.5 means SRS risks tend to be lower; median SRS=0.042, median random=0.042 |
| `FSE6` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 439.5 | 0.73 | negligible (0.4883) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003707, median random=0.003824 |
| `FSE2` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.0281) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n16,expensiveOracle_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 433 | 0.808 | negligible (0.4811) | A12<0.5 means SRS risks tend to be lower; median SRS=0.042, median random=0.042 |
| `FSE6` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 436.5 | 0.764 | negligible (0.515) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007678, median random=0.007626 |
| `FSE2` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n20; best cost-normalized=diversity_n20 |
| `FSE3` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.01801) | best cost-normalized=diversity_n20; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.1429 |  | large frontier change (6) | count front=diversity_n20,expensiveOracle_n20; empirical front=SRSSampling_n20,balanced_n20,cheapOracle_n20,diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 440.5 | 0.722 | negligible (0.4894) | A12<0.5 means SRS risks tend to be lower; median SRS=0.023, median random=0.023 |
| `FSE6` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 448.5 | 0.633 | negligible (0.4983) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009753, median random=0.009753 |
| `FSE2` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.01493) | best size-normalized=expensiveOracle_n32; best cost-normalized=balanced_n32 |
| `FSE3` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.0109) | best cost-normalized=balanced_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n32; empirical front=balanced_n32,cheapOracle_n32,diversity_n32,expensiveOracle_n32,pilotCost_n32,random_n32 |
| `FSE5` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 440.5 | 0.722 | negligible (0.4894) | A12<0.5 means SRS risks tend to be lower; median SRS=0.023, median random=0.023 |
| `FSE6` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 405 | 0.869 | negligible (0.55) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01576, median random=0.01519 |
| `FSE2` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.01788) | best size-normalized=expensiveOracle_n40; best cost-normalized=pairwise_n40 |
| `FSE3` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.0103) | best cost-normalized=pairwise_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n40; empirical front=balanced_n40,cheapOracle_n40,expensiveOracle_n40,pairwise_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 439 | 0.738 | negligible (0.5122) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0115, median random=0.0115 |
| `FSE6` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 424 | 0.908 | negligible (0.4711) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01949, median random=0.02007 |
| `FSE2` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.01354) | best size-normalized=expensiveOracle_n64; best cost-normalized=cheapOracle_n64 |
| `FSE3` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01316) | best cost-normalized=cheapOracle_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n64; empirical front=balanced_n64,cheapOracle_n64,diversity_n64,expensiveOracle_n64,pairwise_n64 |
| `FSE5` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 408 | 0.896 | negligible (0.5467) | A12<0.5 means SRS risks tend to be lower; median SRS=0.00975, median random=0.008 |
| `FSE6` | `lcbench__workload_credit_g__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 418 | 0.979 | negligible (0.4644) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03238, median random=0.03243 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003824 | 0.042 | 0.9135 | 0.01348 | 0.01712 |
| `balanced_n8` | 8 | 0.004 | 0.002725 | 0.023 | 0.965 | 0.06498 | 0.09923 |
| `diversity_n8` | 8 | 0.004 | 0.005124 | 0.023 | 0.977 | 0.077 | 0.05864 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003707 | 0.042 | 0.9136 | 0.0136 | 0.01983 |
| `pairwise_n8` | 8 | 0.004 | 0.0034 | 0.0795 | 0.9205 | 0.0205 | 0.03415 |
| `pilotCost_n8` | 8 | 0.004 | 0.00234 | 0.13 | 0.879 | -0.021 | 0.02869 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001893 | 0.0795 | 0.9205 | 0.0205 | 0.09332 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.02872 | 0.13 | 0.87 | -0.03 | -0.1132 |
| `random_n16` | 16 | 0.008 | 0.007626 | 0.042 | 0.9568 | 0.01237 | 0.01478 |
| `balanced_n16` | 16 | 0.008 | 0.005267 | 0.023 | 0.9618 | 0.01734 | 0.04156 |
| `diversity_n16` | 16 | 0.008 | 0.008034 | 0.0115 | 0.9885 | 0.04406 | 0.04385 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007678 | 0.042 | 0.9581 | 0.01369 | 0.01575 |
| `pairwise_n16` | 16 | 0.008 | 0.007525 | 0.042 | 0.958 | 0.01356 | 0.01665 |
| `pilotCost_n16` | 16 | 0.008 | 0.00468 | 0.042 | 0.9264 | -0.01808 | 0.0144 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003945 | 0.0795 | 0.9205 | -0.02394 | 0.02161 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.05424 | 0.0115 | 0.9885 | 0.04406 | -0.002449 |
| `random_n20` | 20 | 0.01 | 0.009753 | 0.023 | 0.9598 | 0.005288 | 0.006332 |
| `balanced_n20` | 20 | 0.01 | 0.006452 | 0.042 | 0.9536 | -0.0009455 | 0.02069 |
| `diversity_n20` | 20 | 0.01 | 0.01272 | 0.0115 | 0.9885 | 0.03395 | 0.02494 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009753 | 0.023 | 0.9604 | 0.005888 | 0.006932 |
| `pairwise_n20` | 20 | 0.01 | 0.009237 | 0.042 | 0.958 | 0.003455 | 0.006844 |
| `pilotCost_n20` | 20 | 0.01 | 0.005846 | 0.042 | 0.9416 | -0.01293 | 0.01466 |
| `cheapOracle_n20` | 20 | 0.01 | 0.004987 | 0.0795 | 0.9205 | -0.03405 | 0.004012 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.06595 | 0.0115 | 0.9885 | 0.03395 | -0.004032 |
| `random_n32` | 32 | 0.016 | 0.01519 | 0.023 | 0.9755 | 0.004928 | 0.006408 |
| `balanced_n32` | 32 | 0.016 | 0.01037 | 0.023 | 0.9711 | 0.0004951 | 0.01508 |
| `diversity_n32` | 32 | 0.016 | 0.02 | 0.0115 | 0.9885 | 0.01791 | 0.01231 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01576 | 0.023 | 0.9744 | 0.003762 | 0.004182 |
| `pairwise_n32` | 32 | 0.016 | 0.01543 | 0.042 | 0.958 | -0.01259 | -0.01157 |
| `pilotCost_n32` | 32 | 0.016 | 0.009401 | 0.023 | 0.9669 | -0.003655 | 0.015 |
| `cheapOracle_n32` | 32 | 0.016 | 0.008156 | 0.0795 | 0.9205 | -0.05009 | -0.02489 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.09616 | 0.005 | 0.995 | 0.02441 | 0.0001463 |
| `random_n40` | 40 | 0.02 | 0.02007 | 0.0115 | 0.9805 | 0.004276 | 0.004192 |
| `balanced_n40` | 40 | 0.02 | 0.01331 | 0.0115 | 0.9784 | 0.002176 | 0.01332 |
| `diversity_n40` | 40 | 0.02 | 0.02944 | 0.0115 | 0.9885 | 0.01231 | 0.004923 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01949 | 0.0115 | 0.9825 | 0.006326 | 0.006917 |
| `pairwise_n40` | 40 | 0.02 | 0.01883 | 0.008 | 0.992 | 0.01581 | 0.01722 |
| `pilotCost_n40` | 40 | 0.02 | 0.0117 | 0.042 | 0.9684 | -0.007807 | 0.007752 |
| `cheapOracle_n40` | 40 | 0.02 | 0.0103 | 0.042 | 0.958 | -0.01819 | 0.002239 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.1143 | 0.005 | 0.995 | 0.01881 | -0.0006638 |
| `random_n64` | 64 | 0.032 | 0.03243 | 0.008 | 0.9902 | 0.005402 | 0.005207 |
| `balanced_n64` | 64 | 0.032 | 0.02231 | 0.005 | 0.9913 | 0.006502 | 0.0128 |
| `diversity_n64` | 64 | 0.032 | 0.04105 | 0.0025 | 0.9975 | 0.01265 | 0.009391 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03238 | 0.00975 | 0.9884 | 0.003568 | 0.003394 |
| `pairwise_n64` | 64 | 0.032 | 0.03071 | 0.008 | 0.992 | 0.007152 | 0.00777 |
| `pilotCost_n64` | 64 | 0.032 | 0.0189 | 0.0115 | 0.9873 | 0.002435 | 0.01241 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01682 | 0.0115 | 0.9885 | 0.003652 | 0.01656 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.1648 | 0 | 1 | 0.01515 | 0.003016 |
