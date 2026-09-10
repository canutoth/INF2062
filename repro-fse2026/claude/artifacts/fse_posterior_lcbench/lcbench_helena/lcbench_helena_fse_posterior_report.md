# lcbench__workload_helena__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `expensiveOracle_n16` (risk 0.002, %cost 0.06454).

Best integrated confidence after normalizing the prior baseline by empirical cost: `cheapOracle_n8` (omega_cost 0.1001, %cost 0.001949).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.996, risk 0.004, %cost 0.004718, omega_cost 0.08344
- `cheapOracle_n8`: posterior area 0.9305, risk 0.0695, %cost 0.001949, omega_cost 0.1001
- `cheapOracle_n16`: posterior area 0.936, risk 0.064, %cost 0.003993, omega_cost 0.03615
- `expensiveOracle_n16`: posterior area 0.998, risk 0.002, %cost 0.06454, omega_cost 0.005629

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n8` | `supports` | 15.02 | 0.0358 | large (0.06913) | median risks: random=0.09675, balanced=0.0935, diversity=0.004, SRSSampling=0.0865, pairwise=0.2285, pilotCost=0.036, cheapOracle=0.0695, expensiveOracle=0.4415; spread=0.4375 |
| `FSE1` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n16` | `supports` | 19.03 | 0.0081 | large (0.1037) | median risks: random=0.052, balanced=0.045, diversity=0.004, SRSSampling=0.052, pairwise=0.0565, pilotCost=0.01675, cheapOracle=0.064, expensiveOracle=0.002; spread=0.062 |
| `FSE1` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n20` | `supports` | 15.09 | 0.0349 | large (0.06973) | median risks: random=0.02725, balanced=0.01975, diversity=0.004, SRSSampling=0.02825, pairwise=0.0565, pilotCost=0.012, cheapOracle=0.064, expensiveOracle=0.002; spread=0.062 |
| `FSE1` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n32` | `supports` | 19.01 | 0.00814 | large (0.1036) | median risks: random=0.02075, balanced=0.03975, diversity=0.004, SRSSampling=0.0305, pairwise=0.0565, pilotCost=0.01175, cheapOracle=0.064, expensiveOracle=0.002; spread=0.062 |
| `FSE1` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 12.08 | 0.0979 | large (0.0438) | median risks: random=0.0135, balanced=0.017, diversity=0.004, SRSSampling=0.019, pairwise=0.02, pilotCost=0.01, cheapOracle=0.0535, expensiveOracle=0.002; spread=0.0515 |
| `FSE1` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n64` | `supports` | 28.98 | 1.46e-04 | moderate (0.1895) | median risks: random=0.01, balanced=0.004, diversity=0.004, SRSSampling=0.0105, pairwise=0.02, pilotCost=0.004, cheapOracle=0.0405, expensiveOracle=0.002; spread=0.0385 |
| `FSE2` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.01661) | best size-normalized=diversity_n8; best cost-normalized=cheapOracle_n8 |
| `FSE3` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.1033) | best cost-normalized=cheapOracle_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n8; empirical front=cheapOracle_n8,diversity_n8 |
| `FSE5` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 432.5 | 0.809 | negligible (0.4806) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0865, median random=0.09675 |
| `FSE6` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 434.5 | 0.787 | negligible (0.4828) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003679, median random=0.003763 |
| `FSE2` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.04604) | best size-normalized=expensiveOracle_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.06432) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.25 |  | large frontier change (3) | count front=expensiveOracle_n16; empirical front=cheapOracle_n16,diversity_n16,expensiveOracle_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 443 | 0.692 | negligible (0.4922) | A12<0.5 means SRS risks tend to be lower; median SRS=0.052, median random=0.052 |
| `FSE6` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 428.5 | 0.856 | negligible (0.5239) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007423, median random=0.007282 |
| `FSE2` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.03352) | best size-normalized=expensiveOracle_n20; best cost-normalized=pilotCost_n20 |
| `FSE3` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.03362) | best cost-normalized=pilotCost_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.25 |  | large frontier change (3) | count front=expensiveOracle_n20; empirical front=cheapOracle_n20,diversity_n20,expensiveOracle_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 449 | 0.628 | negligible (0.5011) | A12<0.5 means SRS risks tend to be lower; median SRS=0.02825, median random=0.02725 |
| `FSE6` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 437.5 | 0.753 | negligible (0.4861) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009564, median random=0.009646 |
| `FSE2` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.02166) | best size-normalized=expensiveOracle_n32; best cost-normalized=pilotCost_n32 |
| `FSE3` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02945) | best cost-normalized=pilotCost_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.25 |  | large frontier change (3) | count front=expensiveOracle_n32; empirical front=cheapOracle_n32,diversity_n32,expensiveOracle_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 421.5 | 0.937 | negligible (0.5317) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0305, median random=0.02075 |
| `FSE6` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 427 | 0.873 | negligible (0.4744) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01487, median random=0.01496 |
| `FSE2` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.02203) | best size-normalized=expensiveOracle_n40; best cost-normalized=pilotCost_n40 |
| `FSE3` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.02198) | best cost-normalized=pilotCost_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.25 |  | large frontier change (3) | count front=expensiveOracle_n40; empirical front=cheapOracle_n40,diversity_n40,expensiveOracle_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 415 | 0.986 | negligible (0.5389) | A12<0.5 means SRS risks tend to be lower; median SRS=0.019, median random=0.0135 |
| `FSE6` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 289 | 0.0601 | medium (0.3211) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01837, median random=0.01979 |
| `FSE2` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.01801) | best size-normalized=expensiveOracle_n64; best cost-normalized=pilotCost_n64 |
| `FSE3` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.0146) | best cost-normalized=pilotCost_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.25 |  | large frontier change (3) | count front=expensiveOracle_n64; empirical front=cheapOracle_n64,diversity_n64,expensiveOracle_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 440.5 | 0.719 | negligible (0.5106) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0105, median random=0.01 |
| `FSE6` | `lcbench__workload_helena__cost_time_total__target_final_val_accuracy:n64` | `supports` | 133 | 2.83e-05 | large (0.1478) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02825, median random=0.03153 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003763 | 0.09675 | 0.8852 | -0.01475 | -0.009769 |
| `balanced_n8` | 8 | 0.004 | 0.004068 | 0.0935 | 0.9059 | 0.0059 | 0.004554 |
| `diversity_n8` | 8 | 0.004 | 0.004718 | 0.004 | 0.996 | 0.096 | 0.08344 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003679 | 0.0865 | 0.8899 | -0.0101 | -0.003239 |
| `pairwise_n8` | 8 | 0.004 | 0.00419 | 0.2285 | 0.7715 | -0.1285 | -0.1322 |
| `pilotCost_n8` | 8 | 0.004 | 0.002429 | 0.036 | 0.9209 | 0.02092 | 0.06673 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001949 | 0.0695 | 0.9305 | 0.0305 | 0.1001 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.03803 | 0.4415 | 0.5585 | -0.3415 | -0.4287 |
| `random_n16` | 16 | 0.008 | 0.007282 | 0.052 | 0.9248 | -0.01961 | -0.01479 |
| `balanced_n16` | 16 | 0.008 | 0.007197 | 0.045 | 0.9486 | 0.004172 | 0.009617 |
| `diversity_n16` | 16 | 0.008 | 0.007982 | 0.004 | 0.996 | 0.05156 | 0.05167 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007423 | 0.052 | 0.928 | -0.01646 | -0.01266 |
| `pairwise_n16` | 16 | 0.008 | 0.007899 | 0.0565 | 0.9435 | -0.0009444 | -0.0003119 |
| `pilotCost_n16` | 16 | 0.008 | 0.004851 | 0.01675 | 0.9639 | 0.01946 | 0.04936 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003993 | 0.064 | 0.936 | -0.008444 | 0.03615 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.06454 | 0.002 | 0.998 | 0.05356 | 0.005629 |
| `random_n20` | 20 | 0.01 | 0.009646 | 0.02725 | 0.9572 | 0.002671 | 0.004182 |
| `balanced_n20` | 20 | 0.01 | 0.008707 | 0.01975 | 0.9576 | 0.003005 | 0.009062 |
| `diversity_n20` | 20 | 0.01 | 0.01395 | 0.004 | 0.996 | 0.04145 | 0.02945 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009564 | 0.02825 | 0.9571 | 0.002605 | 0.004481 |
| `pairwise_n20` | 20 | 0.01 | 0.009637 | 0.0565 | 0.9435 | -0.01105 | -0.009495 |
| `pilotCost_n20` | 20 | 0.01 | 0.006376 | 0.012 | 0.9703 | 0.01577 | 0.03811 |
| `cheapOracle_n20` | 20 | 0.01 | 0.005033 | 0.064 | 0.936 | -0.01855 | 0.01888 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.07489 | 0.002 | 0.998 | 0.04345 | 0.004589 |
| `random_n32` | 32 | 0.016 | 0.01496 | 0.02075 | 0.9678 | -0.002822 | -0.0008978 |
| `balanced_n32` | 32 | 0.016 | 0.0134 | 0.03975 | 0.9614 | -0.009222 | -0.003919 |
| `diversity_n32` | 32 | 0.016 | 0.02008 | 0.004 | 0.996 | 0.02541 | 0.01972 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01487 | 0.0305 | 0.9637 | -0.006922 | -0.00482 |
| `pairwise_n32` | 32 | 0.016 | 0.01546 | 0.0565 | 0.9435 | -0.02709 | -0.02612 |
| `pilotCost_n32` | 32 | 0.016 | 0.00956 | 0.01175 | 0.9773 | 0.006695 | 0.02463 |
| `cheapOracle_n32` | 32 | 0.016 | 0.008187 | 0.064 | 0.936 | -0.03459 | -0.009576 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.09945 | 0.002 | 0.998 | 0.02741 | 0.002977 |
| `random_n40` | 40 | 0.02 | 0.01979 | 0.0135 | 0.9777 | 0.00151 | 0.001753 |
| `balanced_n40` | 40 | 0.02 | 0.01622 | 0.017 | 0.9813 | 0.005126 | 0.01035 |
| `diversity_n40` | 40 | 0.02 | 0.02714 | 0.004 | 0.996 | 0.01981 | 0.01377 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01837 | 0.019 | 0.9766 | 0.0004262 | 0.002429 |
| `pairwise_n40` | 40 | 0.02 | 0.01875 | 0.02 | 0.98 | 0.00381 | 0.005315 |
| `pilotCost_n40` | 40 | 0.02 | 0.01182 | 0.01 | 0.9854 | 0.00921 | 0.02441 |
| `cheapOracle_n40` | 40 | 0.02 | 0.0103 | 0.0535 | 0.9465 | -0.02969 | -0.009265 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.1132 | 0.002 | 0.998 | 0.02181 | 0.002378 |
| `random_n64` | 64 | 0.032 | 0.03153 | 0.01 | 0.985 | 0.0001682 | 0.0003871 |
| `balanced_n64` | 64 | 0.032 | 0.02588 | 0.004 | 0.9937 | 0.008835 | 0.01228 |
| `diversity_n64` | 64 | 0.032 | 0.03925 | 0.004 | 0.996 | 0.01115 | 0.008421 |
| `SRSSampling_n64` | 64 | 0.032 | 0.02825 | 0.0105 | 0.9876 | 0.002768 | 0.004713 |
| `pairwise_n64` | 64 | 0.032 | 0.02924 | 0.02 | 0.98 | -0.004848 | -0.003466 |
| `pilotCost_n64` | 64 | 0.032 | 0.01951 | 0.004 | 0.9949 | 0.01008 | 0.01931 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01672 | 0.0405 | 0.9595 | -0.02535 | -0.01228 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.1505 | 0.002 | 0.998 | 0.01315 | 0.001301 |
