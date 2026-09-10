# lcbench__workload_airlines__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `balanced_n64` (risk 0.00375, %cost 0.02397).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n8` (omega_cost 0.1116, %cost 0.003307).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.9955, risk 0.0045, %cost 0.003307, omega_cost 0.1116
- `pairwise_n8`: posterior area 0.928, risk 0.072, %cost 0.003018, omega_cost 0.05245
- `pilotCost_n8`: posterior area 0.8344, risk 0.1953, %cost 0.00191, omega_cost 0.00618

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 6.151 | 0.292 | large (0.00992) | median risks: random=0.07925, balanced=0.04525, diversity=0.0045, SRSSampling=0.09425, pairwise=0.072, pilotCost=0.1953; spread=0.1908 |
| `FSE1` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n16` | `supports` | 17.55 | 0.00357 | large (0.1082) | median risks: random=0.03075, balanced=0.0555, diversity=0.0045, SRSSampling=0.03075, pairwise=0.06, pilotCost=0.1862; spread=0.1817 |
| `FSE1` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 5.959 | 0.31 | large (0.00827) | median risks: random=0.0525, balanced=0.0595, diversity=0.0045, SRSSampling=0.0525, pairwise=0.06, pilotCost=0.018; spread=0.0555 |
| `FSE1` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n32` | `supports` | 12.35 | 0.0303 | large (0.06338) | median risks: random=0.017, balanced=0.029, diversity=0.0045, SRSSampling=0.01425, pairwise=0.06, pilotCost=0.055; spread=0.0555 |
| `FSE1` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n40` | `supports` | 11.42 | 0.0437 | moderate (0.05533) | median risks: random=0.017, balanced=0.0115, diversity=0.0045, SRSSampling=0.016, pairwise=0.0205, pilotCost=0.025; spread=0.0205 |
| `FSE1` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n64` | `supports` | 17.19 | 0.00415 | moderate (0.1051) | median risks: random=0.01125, balanced=0.00375, diversity=0.0045, SRSSampling=0.0085, pairwise=0.0175, pilotCost=0.0075; spread=0.01375 |
| `FSE2` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n8; best cost-normalized=diversity_n8 |
| `FSE3` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.1319) | best cost-normalized=diversity_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n8; empirical front=diversity_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 439.5 | 0.73 | negligible (0.5117) | A12<0.5 means SRS risks tend to be lower; median SRS=0.09425, median random=0.07925 |
| `FSE6` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 438.5 | 0.741 | negligible (0.4872) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003365, median random=0.003419 |
| `FSE2` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.06932) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n16; empirical front=diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 444.5 | 0.675 | negligible (0.5061) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03075, median random=0.03075 |
| `FSE6` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 430 | 0.838 | negligible (0.5222) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007406, median random=0.007188 |
| `FSE2` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n20; best cost-normalized=diversity_n20 |
| `FSE3` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.04674) | best cost-normalized=diversity_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n20; empirical front=balanced_n20,diversity_n20,pilotCost_n20,random_n20 |
| `FSE5` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 446.5 | 0.654 | negligible (0.5039) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0525, median random=0.0525 |
| `FSE6` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 449.5 | 0.622 | negligible (0.4994) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009772, median random=0.009772 |
| `FSE2` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.01521) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n32; empirical front=SRSSampling_n32,balanced_n32,diversity_n32,pilotCost_n32,random_n32 |
| `FSE5` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 431.5 | 0.821 | negligible (0.4794) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01425, median random=0.017 |
| `FSE6` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 361 | 0.415 | small (0.5989) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01591, median random=0.01461 |
| `FSE2` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.001152) | best size-normalized=diversity_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | moderate (0.008931) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n40; empirical front=balanced_n40,diversity_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 435 | 0.781 | negligible (0.4833) | A12<0.5 means SRS risks tend to be lower; median SRS=0.016, median random=0.017 |
| `FSE6` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 436 | 0.77 | negligible (0.5156) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02015, median random=0.01945 |
| `FSE2` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.006292) | best size-normalized=diversity_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01134) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n64; empirical front=balanced_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 370.5 | 0.499 | small (0.4117) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0085, median random=0.01125 |
| `FSE6` | `lcbench__workload_airlines__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 431 | 0.827 | negligible (0.4789) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03276, median random=0.03322 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003419 | 0.07925 | 0.8679 | -0.03213 | -0.01899 |
| `balanced_n8` | 8 | 0.004 | 0.004412 | 0.04525 | 0.9051 | 0.005117 | -0.00249 |
| `diversity_n8` | 8 | 0.004 | 0.003307 | 0.0045 | 0.9955 | 0.0955 | 0.1116 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003365 | 0.09425 | 0.8651 | -0.03487 | -0.02032 |
| `pairwise_n8` | 8 | 0.004 | 0.003018 | 0.072 | 0.928 | 0.028 | 0.05245 |
| `pilotCost_n8` | 8 | 0.004 | 0.00191 | 0.1953 | 0.8344 | -0.06562 | 0.00618 |
| `random_n16` | 16 | 0.008 | 0.007188 | 0.03075 | 0.947 | 0.002539 | 0.008051 |
| `balanced_n16` | 16 | 0.008 | 0.007616 | 0.0555 | 0.9172 | -0.02723 | -0.02475 |
| `diversity_n16` | 16 | 0.008 | 0.005847 | 0.0045 | 0.9955 | 0.05106 | 0.06852 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007406 | 0.03075 | 0.9397 | -0.004728 | -0.0008 |
| `pairwise_n16` | 16 | 0.008 | 0.01015 | 0.06 | 0.94 | -0.004444 | -0.01514 |
| `pilotCost_n16` | 16 | 0.008 | 0.003978 | 0.1862 | 0.8485 | -0.09599 | -0.0511 |
| `random_n20` | 20 | 0.01 | 0.009772 | 0.0525 | 0.9407 | -0.01383 | -0.01286 |
| `balanced_n20` | 20 | 0.01 | 0.008786 | 0.0595 | 0.9337 | -0.02085 | -0.01521 |
| `diversity_n20` | 20 | 0.01 | 0.01224 | 0.0045 | 0.9955 | 0.04095 | 0.03328 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009772 | 0.0525 | 0.9401 | -0.01443 | -0.01346 |
| `pairwise_n20` | 20 | 0.01 | 0.01258 | 0.06 | 0.94 | -0.01455 | -0.02317 |
| `pilotCost_n20` | 20 | 0.01 | 0.005075 | 0.018 | 0.9275 | -0.02701 | 0.009843 |
| `random_n32` | 32 | 0.016 | 0.01461 | 0.017 | 0.9749 | 0.004312 | 0.006927 |
| `balanced_n32` | 32 | 0.016 | 0.01318 | 0.029 | 0.9683 | -0.002288 | 0.003554 |
| `diversity_n32` | 32 | 0.016 | 0.01753 | 0.0045 | 0.9955 | 0.02491 | 0.02248 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01591 | 0.01425 | 0.9777 | 0.007112 | 0.007267 |
| `pairwise_n32` | 32 | 0.016 | 0.01756 | 0.06 | 0.94 | -0.03059 | -0.03306 |
| `pilotCost_n32` | 32 | 0.016 | 0.007796 | 0.055 | 0.9042 | -0.06642 | -0.03899 |
| `random_n40` | 40 | 0.02 | 0.01945 | 0.017 | 0.9782 | 0.00206 | 0.002704 |
| `balanced_n40` | 40 | 0.02 | 0.0161 | 0.0115 | 0.985 | 0.008843 | 0.01427 |
| `diversity_n40` | 40 | 0.02 | 0.02737 | 0.0045 | 0.9955 | 0.01931 | 0.01312 |
| `SRSSampling_n40` | 40 | 0.02 | 0.02015 | 0.016 | 0.9817 | 0.00551 | 0.005343 |
| `pairwise_n40` | 40 | 0.02 | 0.02013 | 0.0205 | 0.9795 | 0.00331 | 0.003159 |
| `pilotCost_n40` | 40 | 0.02 | 0.009468 | 0.025 | 0.9264 | -0.04976 | -0.0258 |
| `random_n64` | 64 | 0.032 | 0.03322 | 0.01125 | 0.9846 | -0.0002152 | -0.0007536 |
| `balanced_n64` | 64 | 0.032 | 0.02397 | 0.00375 | 0.9949 | 0.01003 | 0.0149 |
| `diversity_n64` | 64 | 0.032 | 0.03713 | 0.0045 | 0.9955 | 0.01065 | 0.008611 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03276 | 0.0085 | 0.9888 | 0.003902 | 0.003562 |
| `pairwise_n64` | 64 | 0.032 | 0.02816 | 0.0175 | 0.9825 | -0.002348 | -0.0003505 |
| `pilotCost_n64` | 64 | 0.032 | 0.01554 | 0.0075 | 0.9792 | -0.005682 | 0.009392 |
