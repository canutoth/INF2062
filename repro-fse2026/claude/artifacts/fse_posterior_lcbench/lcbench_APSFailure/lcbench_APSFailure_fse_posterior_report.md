# lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `expensiveOracle_n16` (risk 0, %cost 0.09872).

Best integrated confidence after normalizing the prior baseline by empirical cost: `balanced_n8` (omega_cost 0.04536, %cost 0.004036).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9461, risk 0.05, %cost 0.004036, omega_cost 0.04536
- `SRSSampling_n8`: posterior area 0.8786, risk 0.095, %cost 0.0035, omega_cost -0.01027
- `pilotCost_n8`: posterior area 0.8669, risk 0.094, %cost 0.002042, omega_cost 0.03123
- `cheapOracle_n8`: posterior area 0.6265, risk 0.3735, %cost 0.00166, omega_cost -0.1855
- `balanced_n16`: posterior area 0.9658, risk 0.0395, %cost 0.007382, omega_cost 0.02542
- `diversity_n16`: posterior area 0.989, risk 0.011, %cost 0.01065, omega_cost 0.0319
- `pilotCost_n16`: posterior area 0.9341, risk 0.0555, %cost 0.004034, omega_cost 0.0334
- `expensiveOracle_n16`: posterior area 1, risk 0, %cost 0.09872, omega_cost 0.005014
- `pilotCost_n20`: posterior area 0.9492, risk 0.02675, %cost 0.005308, omega_cost 0.02846
- `pilotCost_n40`: posterior area 0.9748, risk 0.0175, %cost 0.01014, omega_cost 0.0197
- `balanced_n64`: posterior area 0.9927, risk 0.006, %cost 0.0262, omega_cost 0.01112

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n8` | `supports` | 21.14 | 0.00357 | large (0.1219) | median risks: random=0.11, balanced=0.05, diversity=0.0765, SRSSampling=0.095, pairwise=0.347, pilotCost=0.094, cheapOracle=0.3735, expensiveOracle=0.0325; spread=0.341 |
| `FSE1` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n16` | `inconclusive` | 12.27 | 0.0919 | large (0.04545) | median risks: random=0.03725, balanced=0.0395, diversity=0.011, SRSSampling=0.0345, pairwise=0.0535, pilotCost=0.0555, cheapOracle=0.3735, expensiveOracle=0; spread=0.3735 |
| `FSE1` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 7.775 | 0.353 | large (0.006682) | median risks: random=0.01925, balanced=0.038, diversity=0.011, SRSSampling=0.01925, pairwise=0.0535, pilotCost=0.02675, cheapOracle=0.3065, expensiveOracle=0; spread=0.3065 |
| `FSE1` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 10.67 | 0.154 | large (0.03162) | median risks: random=0.03025, balanced=0.02475, diversity=0.011, SRSSampling=0.02475, pairwise=0.049, pilotCost=0.03075, cheapOracle=0.229, expensiveOracle=0; spread=0.229 |
| `FSE1` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 11.54 | 0.117 | large (0.03913) | median risks: random=0.015, balanced=0.008, diversity=0.011, SRSSampling=0.02425, pairwise=0.049, pilotCost=0.0175, cheapOracle=0.229, expensiveOracle=0; spread=0.229 |
| `FSE1` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n64` | `supports` | 24.94 | 7.79e-04 | large (0.1546) | median risks: random=0.00825, balanced=0.006, diversity=0.011, SRSSampling=0.01025, pairwise=0.049, pilotCost=0.017, cheapOracle=0.1525, expensiveOracle=0; spread=0.1525 |
| `FSE2` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.0704) | best size-normalized=expensiveOracle_n8; best cost-normalized=balanced_n8 |
| `FSE3` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.05564) | best cost-normalized=balanced_n8; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n8; empirical front=SRSSampling_n8,balanced_n8,cheapOracle_n8,expensiveOracle_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 439.5 | 0.73 | negligible (0.4883) | A12<0.5 means SRS risks tend to be lower; median SRS=0.095, median random=0.11 |
| `FSE6` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 438.5 | 0.741 | negligible (0.4872) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0035, median random=0.003507 |
| `FSE2` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.02839) | best size-normalized=expensiveOracle_n16; best cost-normalized=pilotCost_n16 |
| `FSE3` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.03266) | best cost-normalized=pilotCost_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16,expensiveOracle_n16,pairwise_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 436 | 0.77 | negligible (0.4844) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0345, median random=0.03725 |
| `FSE6` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 424.5 | 0.902 | negligible (0.5283) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007447, median random=0.007367 |
| `FSE2` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.02398) | best size-normalized=expensiveOracle_n20; best cost-normalized=pilotCost_n20 |
| `FSE3` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.02154) | best cost-normalized=pilotCost_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n20; empirical front=balanced_n20,cheapOracle_n20,diversity_n20,expensiveOracle_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 448 | 0.638 | negligible (0.4978) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01925, median random=0.01925 |
| `FSE6` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 430.5 | 0.832 | negligible (0.4783) | A12>0.5 means SRS costs tend to be higher; median SRS=0.008919, median random=0.008995 |
| `FSE2` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.009551) | best size-normalized=expensiveOracle_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.01334) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n32; empirical front=balanced_n32,cheapOracle_n32,diversity_n32,expensiveOracle_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 416.5 | 0.996 | negligible (0.4628) | A12<0.5 means SRS risks tend to be lower; median SRS=0.02475, median random=0.03025 |
| `FSE6` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 309 | 0.113 | medium (0.6567) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01572, median random=0.01423 |
| `FSE2` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.01645) | best size-normalized=expensiveOracle_n40; best cost-normalized=pilotCost_n40 |
| `FSE3` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.02086) | best cost-normalized=pilotCost_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n40; empirical front=balanced_n40,cheapOracle_n40,diversity_n40,expensiveOracle_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 399 | 0.799 | negligible (0.5567) | A12<0.5 means SRS risks tend to be lower; median SRS=0.02425, median random=0.015 |
| `FSE6` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 394 | 0.743 | small (0.5622) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01925, median random=0.01893 |
| `FSE2` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.008514) | best size-normalized=expensiveOracle_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | moderate (0.008682) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.25 |  | large frontier change (3) | count front=expensiveOracle_n64; empirical front=balanced_n64,cheapOracle_n64,expensiveOracle_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 415 | 0.986 | negligible (0.5389) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01025, median random=0.00825 |
| `FSE6` | `lcbench__workload_APSFailure__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 437 | 0.758 | negligible (0.5144) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03233, median random=0.03145 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003507 | 0.11 | 0.8745 | -0.0255 | -0.01456 |
| `balanced_n8` | 8 | 0.004 | 0.004036 | 0.05 | 0.9461 | 0.04608 | 0.04536 |
| `diversity_n8` | 8 | 0.004 | 0.007585 | 0.0765 | 0.9235 | 0.0235 | -0.01826 |
| `SRSSampling_n8` | 8 | 0.004 | 0.0035 | 0.095 | 0.8786 | -0.02138 | -0.01027 |
| `pairwise_n8` | 8 | 0.004 | 0.003658 | 0.347 | 0.653 | -0.247 | -0.2397 |
| `pilotCost_n8` | 8 | 0.004 | 0.002042 | 0.094 | 0.8669 | -0.03315 | 0.03123 |
| `cheapOracle_n8` | 8 | 0.004 | 0.00166 | 0.3735 | 0.6265 | -0.2735 | -0.1855 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.06602 | 0.0325 | 0.9675 | 0.0675 | -0.02504 |
| `random_n16` | 16 | 0.008 | 0.007367 | 0.03725 | 0.9374 | -0.007094 | -0.002889 |
| `balanced_n16` | 16 | 0.008 | 0.007382 | 0.0395 | 0.9658 | 0.02132 | 0.02542 |
| `diversity_n16` | 16 | 0.008 | 0.01065 | 0.011 | 0.989 | 0.04456 | 0.0319 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007447 | 0.0345 | 0.9415 | -0.002894 | 0.0007391 |
| `pairwise_n16` | 16 | 0.008 | 0.007207 | 0.0535 | 0.9465 | 0.002056 | 0.007422 |
| `pilotCost_n16` | 16 | 0.008 | 0.004034 | 0.0555 | 0.9341 | -0.01038 | 0.0334 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003395 | 0.3735 | 0.6265 | -0.3179 | -0.2597 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.09872 | 0 | 1 | 0.05556 | 0.005014 |
| `random_n20` | 20 | 0.01 | 0.008995 | 0.01925 | 0.956 | 0.001488 | 0.00606 |
| `balanced_n20` | 20 | 0.01 | 0.008623 | 0.038 | 0.9636 | 0.009055 | 0.01556 |
| `diversity_n20` | 20 | 0.01 | 0.01404 | 0.011 | 0.989 | 0.03445 | 0.02226 |
| `SRSSampling_n20` | 20 | 0.01 | 0.008919 | 0.01925 | 0.9565 | 0.001971 | 0.006923 |
| `pairwise_n20` | 20 | 0.01 | 0.008981 | 0.0535 | 0.9465 | -0.008045 | -0.003404 |
| `pilotCost_n20` | 20 | 0.01 | 0.005308 | 0.02675 | 0.9492 | -0.005345 | 0.02846 |
| `cheapOracle_n20` | 20 | 0.01 | 0.00427 | 0.3065 | 0.6935 | -0.261 | -0.2116 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.1105 | 0 | 1 | 0.04545 | 0.004486 |
| `random_n32` | 32 | 0.016 | 0.01423 | 0.03025 | 0.9631 | -0.007455 | -0.004043 |
| `balanced_n32` | 32 | 0.016 | 0.01408 | 0.02475 | 0.9731 | 0.002495 | 0.006245 |
| `diversity_n32` | 32 | 0.016 | 0.01971 | 0.011 | 0.989 | 0.01841 | 0.01315 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01572 | 0.02475 | 0.9699 | -0.0006882 | -0.0001948 |
| `pairwise_n32` | 32 | 0.016 | 0.01472 | 0.049 | 0.951 | -0.01959 | -0.0172 |
| `pilotCost_n32` | 32 | 0.016 | 0.008241 | 0.03075 | 0.9587 | -0.01187 | 0.01282 |
| `cheapOracle_n32` | 32 | 0.016 | 0.006921 | 0.229 | 0.771 | -0.1996 | -0.1659 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.1381 | 0 | 1 | 0.02941 | 0.003595 |
| `random_n40` | 40 | 0.02 | 0.01893 | 0.015 | 0.9793 | 0.003143 | 0.004425 |
| `balanced_n40` | 40 | 0.02 | 0.01694 | 0.008 | 0.9819 | 0.005676 | 0.009736 |
| `diversity_n40` | 40 | 0.02 | 0.02862 | 0.011 | 0.989 | 0.01281 | 0.005883 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01925 | 0.02425 | 0.9741 | -0.00204 | -0.00116 |
| `pairwise_n40` | 40 | 0.02 | 0.01769 | 0.049 | 0.951 | -0.02519 | -0.02225 |
| `pilotCost_n40` | 40 | 0.02 | 0.01014 | 0.0175 | 0.9748 | -0.00139 | 0.0197 |
| `cheapOracle_n40` | 40 | 0.02 | 0.008709 | 0.229 | 0.771 | -0.2052 | -0.1775 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.153 | 0 | 1 | 0.02381 | 0.003247 |
| `random_n64` | 64 | 0.032 | 0.03145 | 0.00825 | 0.9871 | 0.002285 | 0.002541 |
| `balanced_n64` | 64 | 0.032 | 0.0262 | 0.006 | 0.9927 | 0.007885 | 0.01112 |
| `diversity_n64` | 64 | 0.032 | 0.0403 | 0.011 | 0.989 | 0.004152 | 0.001107 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03233 | 0.01025 | 0.9874 | 0.002585 | 0.002437 |
| `pairwise_n64` | 64 | 0.032 | 0.02784 | 0.049 | 0.951 | -0.03385 | -0.03166 |
| `pilotCost_n64` | 64 | 0.032 | 0.01745 | 0.017 | 0.9819 | -0.002898 | 0.009043 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01413 | 0.1525 | 0.8475 | -0.1373 | -0.1195 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.191 | 0 | 1 | 0.01515 | 0.002604 |
