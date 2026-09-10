# lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n20` (risk 0.0015, %cost 0.01257).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pairwise_n8` (omega_cost 0.08439, %cost 0.003489).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9395, risk 0.037, %cost 0.002837, omega_cost 0.06976
- `diversity_n8`: posterior area 0.996, risk 0.004, %cost 0.005077, omega_cost 0.07828
- `pairwise_n8`: posterior area 0.973, risk 0.027, %cost 0.003489, omega_cost 0.08439
- `pilotCost_n8`: posterior area 0.8677, risk 0.1295, %cost 0.002311, omega_cost 0.01872
- `diversity_n20`: posterior area 0.9985, risk 0.0015, %cost 0.01257, omega_cost 0.03535

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n8` | `supports` | 14.28 | 0.0139 | large (0.08004) | median risks: random=0.097, balanced=0.037, diversity=0.004, SRSSampling=0.086, pairwise=0.027, pilotCost=0.1295; spread=0.1255 |
| `FSE1` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n16` | `supports` | 30.93 | 9.69e-06 | large (0.2235) | median risks: random=0.037, balanced=0.01, diversity=0.004, SRSSampling=0.037, pairwise=0.027, pilotCost=0.1068; spread=0.1028 |
| `FSE1` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n20` | `inconclusive` | 8.039 | 0.154 | large (0.0262) | median risks: random=0.035, balanced=0.027, diversity=0.0015, SRSSampling=0.03825, pairwise=0.027, pilotCost=0.075; spread=0.0735 |
| `FSE1` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n32` | `supports` | 16.99 | 0.00453 | large (0.1033) | median risks: random=0.0245, balanced=0.0155, diversity=0.0015, SRSSampling=0.0175, pairwise=0.006, pilotCost=0.0895; spread=0.088 |
| `FSE1` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n40` | `supports` | 15.74 | 0.00764 | large (0.09255) | median risks: random=0.0155, balanced=0.01, diversity=0.0015, SRSSampling=0.0175, pairwise=0.006, pilotCost=0.075; spread=0.0735 |
| `FSE1` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 5.912 | 0.315 | small (0.00786) | median risks: random=0.006, balanced=0.006, diversity=0.0015, SRSSampling=0.0085, pairwise=0.006, pilotCost=0.004; spread=0.007 |
| `FSE2` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.006109) | best size-normalized=diversity_n8; best cost-normalized=pairwise_n8 |
| `FSE3` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.08598) | best cost-normalized=pairwise_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n8; empirical front=balanced_n8,diversity_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 433 | 0.804 | negligible (0.4811) | A12<0.5 means SRS risks tend to be lower; median SRS=0.086, median random=0.097 |
| `FSE6` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 438.5 | 0.741 | negligible (0.4872) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003754, median random=0.003828 |
| `FSE2` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.00161) | best size-normalized=diversity_n16; best cost-normalized=balanced_n16 |
| `FSE3` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.06239) | best cost-normalized=balanced_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n16; empirical front=balanced_n16,diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 423.5 | 0.915 | negligible (0.4706) | A12<0.5 means SRS risks tend to be lower; median SRS=0.037, median random=0.037 |
| `FSE6` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 436.5 | 0.764 | negligible (0.515) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007697, median random=0.00767 |
| `FSE2` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n20; best cost-normalized=diversity_n20 |
| `FSE3` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.04734) | best cost-normalized=diversity_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n20; empirical front=balanced_n20,diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 440 | 0.725 | negligible (0.5111) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03825, median random=0.035 |
| `FSE6` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 445.5 | 0.665 | negligible (0.495) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009816, median random=0.009816 |
| `FSE2` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.001871) | best size-normalized=diversity_n32; best cost-normalized=pairwise_n32 |
| `FSE3` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02236) | best cost-normalized=pairwise_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n32; empirical front=balanced_n32,diversity_n32,pairwise_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 379.5 | 0.586 | small (0.4217) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0175, median random=0.0245 |
| `FSE6` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 394 | 0.743 | small (0.5622) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01627, median random=0.01518 |
| `FSE2` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.004113) | best size-normalized=diversity_n40; best cost-normalized=pairwise_n40 |
| `FSE3` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.0177) | best cost-normalized=pairwise_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n40; empirical front=balanced_n40,diversity_n40,pairwise_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 431 | 0.827 | negligible (0.5211) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0175, median random=0.0155 |
| `FSE6` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 437 | 0.758 | negligible (0.4856) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0201, median random=0.02005 |
| `FSE2` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.004114) | best size-normalized=diversity_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01331) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n64; empirical front=balanced_n64,diversity_n64,pairwise_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 395 | 0.749 | small (0.5611) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0085, median random=0.006 |
| `FSE6` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 407 | 0.892 | negligible (0.4522) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03235, median random=0.03272 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003828 | 0.097 | 0.8899 | -0.01013 | -0.006561 |
| `balanced_n8` | 8 | 0.004 | 0.002837 | 0.037 | 0.9395 | 0.03945 | 0.06976 |
| `diversity_n8` | 8 | 0.004 | 0.005077 | 0.004 | 0.996 | 0.096 | 0.07828 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003754 | 0.086 | 0.8932 | -0.006767 | -0.001594 |
| `pairwise_n8` | 8 | 0.004 | 0.003489 | 0.027 | 0.973 | 0.073 | 0.08439 |
| `pilotCost_n8` | 8 | 0.004 | 0.002311 | 0.1295 | 0.8677 | -0.03228 | 0.01872 |
| `random_n16` | 16 | 0.008 | 0.00767 | 0.037 | 0.925 | -0.01943 | -0.01731 |
| `balanced_n16` | 16 | 0.008 | 0.005438 | 0.01 | 0.9755 | 0.03101 | 0.05312 |
| `diversity_n16` | 16 | 0.008 | 0.008008 | 0.004 | 0.996 | 0.05156 | 0.05151 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007697 | 0.037 | 0.9332 | -0.01121 | -0.009276 |
| `pairwise_n16` | 16 | 0.008 | 0.00759 | 0.027 | 0.973 | 0.02856 | 0.03121 |
| `pilotCost_n16` | 16 | 0.008 | 0.004606 | 0.1068 | 0.9011 | -0.04336 | -0.00973 |
| `random_n20` | 20 | 0.01 | 0.009816 | 0.035 | 0.9433 | -0.01125 | -0.01047 |
| `balanced_n20` | 20 | 0.01 | 0.00659 | 0.027 | 0.9592 | 0.004671 | 0.0251 |
| `diversity_n20` | 20 | 0.01 | 0.01257 | 0.0015 | 0.9985 | 0.04395 | 0.03535 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009816 | 0.03825 | 0.9418 | -0.01276 | -0.01199 |
| `pairwise_n20` | 20 | 0.01 | 0.009257 | 0.027 | 0.973 | 0.01845 | 0.02175 |
| `pilotCost_n20` | 20 | 0.01 | 0.005845 | 0.075 | 0.9335 | -0.02106 | 0.006527 |
| `random_n32` | 32 | 0.016 | 0.01518 | 0.0245 | 0.9666 | -0.003955 | -0.002461 |
| `balanced_n32` | 32 | 0.016 | 0.01054 | 0.0155 | 0.9794 | 0.008795 | 0.02271 |
| `diversity_n32` | 32 | 0.016 | 0.01985 | 0.0015 | 0.9985 | 0.02791 | 0.02249 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01627 | 0.0175 | 0.973 | 0.002462 | 0.002002 |
| `pairwise_n32` | 32 | 0.016 | 0.01547 | 0.006 | 0.994 | 0.02341 | 0.02436 |
| `pilotCost_n32` | 32 | 0.016 | 0.00936 | 0.0895 | 0.9349 | -0.03567 | -0.01682 |
| `random_n40` | 40 | 0.02 | 0.02005 | 0.0155 | 0.9777 | 0.00151 | 0.001448 |
| `balanced_n40` | 40 | 0.02 | 0.01343 | 0.01 | 0.9833 | 0.00716 | 0.018 |
| `diversity_n40` | 40 | 0.02 | 0.02915 | 0.0015 | 0.9985 | 0.02231 | 0.01508 |
| `SRSSampling_n40` | 40 | 0.02 | 0.0201 | 0.0175 | 0.9778 | 0.00161 | 0.001497 |
| `pairwise_n40` | 40 | 0.02 | 0.01884 | 0.006 | 0.994 | 0.01781 | 0.0192 |
| `pilotCost_n40` | 40 | 0.02 | 0.01158 | 0.075 | 0.945 | -0.03116 | -0.01522 |
| `random_n64` | 64 | 0.032 | 0.03272 | 0.006 | 0.9864 | 0.001568 | 0.001243 |
| `balanced_n64` | 64 | 0.032 | 0.02239 | 0.006 | 0.9932 | 0.008368 | 0.01459 |
| `diversity_n64` | 64 | 0.032 | 0.04075 | 0.0015 | 0.9985 | 0.01365 | 0.01048 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03235 | 0.0085 | 0.9863 | 0.001435 | 0.001278 |
| `pairwise_n64` | 64 | 0.032 | 0.0309 | 0.006 | 0.994 | 0.009152 | 0.009674 |
| `pilotCost_n64` | 64 | 0.032 | 0.01883 | 0.004 | 0.9891 | 0.004235 | 0.0143 |
