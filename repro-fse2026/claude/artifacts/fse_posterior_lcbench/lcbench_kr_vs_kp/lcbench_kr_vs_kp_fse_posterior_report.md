# lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `expensiveOracle_n8` (risk 0.0015, %cost 0.0278).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pairwise_n8` (omega_cost 0.08439, %cost 0.003489).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9395, risk 0.037, %cost 0.002837, omega_cost 0.06976
- `diversity_n8`: posterior area 0.996, risk 0.004, %cost 0.005077, omega_cost 0.07828
- `pairwise_n8`: posterior area 0.973, risk 0.027, %cost 0.003489, omega_cost 0.08439
- `pilotCost_n8`: posterior area 0.8677, risk 0.1295, %cost 0.002311, omega_cost 0.01872
- `cheapOracle_n8`: posterior area 0.527, risk 0.473, %cost 0.001873, omega_cost -0.299
- `diversity_n20`: posterior area 0.9985, risk 0.0015, %cost 0.01257, omega_cost 0.03535

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n8` | `supports` | 19.14 | 0.00775 | large (0.1047) | median risks: random=0.097, balanced=0.037, diversity=0.004, SRSSampling=0.086, pairwise=0.027, pilotCost=0.1295, cheapOracle=0.473, expensiveOracle=0.0015; spread=0.4715 |
| `FSE1` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n16` | `supports` | 34.66 | 1.29e-05 | large (0.2385) | median risks: random=0.037, balanced=0.01, diversity=0.004, SRSSampling=0.037, pairwise=0.027, pilotCost=0.1068, cheapOracle=0.1895, expensiveOracle=0.0015; spread=0.188 |
| `FSE1` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n20` | `inconclusive` | 12.65 | 0.081 | large (0.04875) | median risks: random=0.035, balanced=0.027, diversity=0.0015, SRSSampling=0.03825, pairwise=0.027, pilotCost=0.075, cheapOracle=0.1895, expensiveOracle=0.0015; spread=0.188 |
| `FSE1` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n32` | `supports` | 21.09 | 0.00365 | large (0.1214) | median risks: random=0.0245, balanced=0.0155, diversity=0.0015, SRSSampling=0.0175, pairwise=0.006, pilotCost=0.0895, cheapOracle=0.143, expensiveOracle=0.0015; spread=0.1415 |
| `FSE1` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n40` | `supports` | 20.1 | 0.00536 | large (0.1129) | median risks: random=0.0155, balanced=0.01, diversity=0.0015, SRSSampling=0.0175, pairwise=0.006, pilotCost=0.075, cheapOracle=0.143, expensiveOracle=0.0015; spread=0.1415 |
| `FSE1` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 10.17 | 0.179 | large (0.02732) | median risks: random=0.006, balanced=0.006, diversity=0.0015, SRSSampling=0.0085, pairwise=0.006, pilotCost=0.004, cheapOracle=0.143, expensiveOracle=0.0015; spread=0.1415 |
| `FSE2` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.06853) | best size-normalized=expensiveOracle_n8; best cost-normalized=pairwise_n8 |
| `FSE3` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.08598) | best cost-normalized=pairwise_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n8; empirical front=balanced_n8,cheapOracle_n8,diversity_n8,expensiveOracle_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 433 | 0.804 | negligible (0.4811) | A12<0.5 means SRS risks tend to be lower; median SRS=0.086, median random=0.097 |
| `FSE6` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 438.5 | 0.741 | negligible (0.4872) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003754, median random=0.003828 |
| `FSE2` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.04535) | best size-normalized=expensiveOracle_n16; best cost-normalized=balanced_n16 |
| `FSE3` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.06239) | best cost-normalized=balanced_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16,expensiveOracle_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 423.5 | 0.915 | negligible (0.4706) | A12<0.5 means SRS risks tend to be lower; median SRS=0.037, median random=0.037 |
| `FSE6` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 436.5 | 0.764 | negligible (0.515) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007697, median random=0.00767 |
| `FSE2` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n20; best cost-normalized=diversity_n20 |
| `FSE3` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.04734) | best cost-normalized=diversity_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.1667 |  | large frontier change (5) | count front=diversity_n20,expensiveOracle_n20; empirical front=balanced_n20,cheapOracle_n20,diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 440 | 0.725 | negligible (0.5111) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03825, median random=0.035 |
| `FSE6` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 445.5 | 0.665 | negligible (0.495) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009816, median random=0.009816 |
| `FSE2` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.001871) | best size-normalized=diversity_n32; best cost-normalized=pairwise_n32 |
| `FSE3` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02236) | best cost-normalized=pairwise_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.1667 |  | large frontier change (5) | count front=diversity_n32,expensiveOracle_n32; empirical front=balanced_n32,cheapOracle_n32,diversity_n32,pairwise_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 379.5 | 0.586 | small (0.4217) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0175, median random=0.0245 |
| `FSE6` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 394 | 0.743 | small (0.5622) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01627, median random=0.01518 |
| `FSE2` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.004113) | best size-normalized=diversity_n40; best cost-normalized=pairwise_n40 |
| `FSE3` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.0177) | best cost-normalized=pairwise_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.1667 |  | large frontier change (5) | count front=diversity_n40,expensiveOracle_n40; empirical front=balanced_n40,cheapOracle_n40,diversity_n40,pairwise_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 431 | 0.827 | negligible (0.5211) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0175, median random=0.0155 |
| `FSE6` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 437 | 0.758 | negligible (0.4856) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0201, median random=0.02005 |
| `FSE2` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.004114) | best size-normalized=diversity_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01331) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kr_vs_kp__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.1667 |  | large frontier change (5) | count front=diversity_n64,expensiveOracle_n64; empirical front=balanced_n64,cheapOracle_n64,diversity_n64,pairwise_n64,pilotCost_n64 |
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
| `cheapOracle_n8` | 8 | 0.004 | 0.001873 | 0.473 | 0.527 | -0.373 | -0.299 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.0278 | 0.0015 | 0.9985 | 0.0985 | 0.01586 |
| `random_n16` | 16 | 0.008 | 0.00767 | 0.037 | 0.925 | -0.01943 | -0.01731 |
| `balanced_n16` | 16 | 0.008 | 0.005438 | 0.01 | 0.9755 | 0.03101 | 0.05312 |
| `diversity_n16` | 16 | 0.008 | 0.008008 | 0.004 | 0.996 | 0.05156 | 0.05151 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007697 | 0.037 | 0.9332 | -0.01121 | -0.009276 |
| `pairwise_n16` | 16 | 0.008 | 0.00759 | 0.027 | 0.973 | 0.02856 | 0.03121 |
| `pilotCost_n16` | 16 | 0.008 | 0.004606 | 0.1068 | 0.9011 | -0.04336 | -0.00973 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003938 | 0.1895 | 0.8105 | -0.1339 | -0.08824 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.05299 | 0.0015 | 0.9985 | 0.05406 | 0.007761 |
| `random_n20` | 20 | 0.01 | 0.009816 | 0.035 | 0.9433 | -0.01125 | -0.01047 |
| `balanced_n20` | 20 | 0.01 | 0.00659 | 0.027 | 0.9592 | 0.004671 | 0.0251 |
| `diversity_n20` | 20 | 0.01 | 0.01257 | 0.0015 | 0.9985 | 0.04395 | 0.03535 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009816 | 0.03825 | 0.9418 | -0.01276 | -0.01199 |
| `pairwise_n20` | 20 | 0.01 | 0.009257 | 0.027 | 0.973 | 0.01845 | 0.02175 |
| `pilotCost_n20` | 20 | 0.01 | 0.005845 | 0.075 | 0.9335 | -0.02106 | 0.006527 |
| `cheapOracle_n20` | 20 | 0.01 | 0.004983 | 0.1895 | 0.8105 | -0.144 | -0.1059 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.06423 | 0.0015 | 0.9985 | 0.04395 | 0.006165 |
| `random_n32` | 32 | 0.016 | 0.01518 | 0.0245 | 0.9666 | -0.003955 | -0.002461 |
| `balanced_n32` | 32 | 0.016 | 0.01054 | 0.0155 | 0.9794 | 0.008795 | 0.02271 |
| `diversity_n32` | 32 | 0.016 | 0.01985 | 0.0015 | 0.9985 | 0.02791 | 0.02249 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01627 | 0.0175 | 0.973 | 0.002462 | 0.002002 |
| `pairwise_n32` | 32 | 0.016 | 0.01547 | 0.006 | 0.994 | 0.02341 | 0.02436 |
| `pilotCost_n32` | 32 | 0.016 | 0.00936 | 0.0895 | 0.9349 | -0.03567 | -0.01682 |
| `cheapOracle_n32` | 32 | 0.016 | 0.008141 | 0.143 | 0.857 | -0.1136 | -0.0883 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.09462 | 0.0015 | 0.9985 | 0.02791 | 0.003729 |
| `random_n40` | 40 | 0.02 | 0.02005 | 0.0155 | 0.9777 | 0.00151 | 0.001448 |
| `balanced_n40` | 40 | 0.02 | 0.01343 | 0.01 | 0.9833 | 0.00716 | 0.018 |
| `diversity_n40` | 40 | 0.02 | 0.02915 | 0.0015 | 0.9985 | 0.02231 | 0.01508 |
| `SRSSampling_n40` | 40 | 0.02 | 0.0201 | 0.0175 | 0.9778 | 0.00161 | 0.001497 |
| `pairwise_n40` | 40 | 0.02 | 0.01884 | 0.006 | 0.994 | 0.01781 | 0.0192 |
| `pilotCost_n40` | 40 | 0.02 | 0.01158 | 0.075 | 0.945 | -0.03116 | -0.01522 |
| `cheapOracle_n40` | 40 | 0.02 | 0.01026 | 0.143 | 0.857 | -0.1192 | -0.09861 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.1124 | 0.0015 | 0.9985 | 0.02231 | 0.002911 |
| `random_n64` | 64 | 0.032 | 0.03272 | 0.006 | 0.9864 | 0.001568 | 0.001243 |
| `balanced_n64` | 64 | 0.032 | 0.02239 | 0.006 | 0.9932 | 0.008368 | 0.01459 |
| `diversity_n64` | 64 | 0.032 | 0.04075 | 0.0015 | 0.9985 | 0.01365 | 0.01048 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03235 | 0.0085 | 0.9863 | 0.001435 | 0.001278 |
| `pairwise_n64` | 64 | 0.032 | 0.0309 | 0.006 | 0.994 | 0.009152 | 0.009674 |
| `pilotCost_n64` | 64 | 0.032 | 0.01883 | 0.004 | 0.9891 | 0.004235 | 0.0143 |
| `cheapOracle_n64` | 64 | 0.032 | 0.0167 | 0.143 | 0.857 | -0.1278 | -0.1148 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.1613 | 0.0015 | 0.9985 | 0.01365 | 0.001581 |
