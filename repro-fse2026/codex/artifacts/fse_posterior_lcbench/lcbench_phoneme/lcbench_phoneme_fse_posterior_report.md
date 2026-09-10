# lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `expensiveOracle_n8` (risk 0.0005, %cost 0.02938).

Best integrated confidence after normalizing the prior baseline by empirical cost: `balanced_n8` (omega_cost 0.07868, %cost 0.002962).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9525, risk 0.0425, %cost 0.002962, omega_cost 0.07868
- `diversity_n8`: posterior area 0.99, risk 0.01, %cost 0.005018, omega_cost 0.07308
- `pairwise_n8`: posterior area 0.959, risk 0.041, %cost 0.003282, omega_cost 0.07577
- `pilotCost_n8`: posterior area 0.7017, risk 0.396, %cost 0.00243, omega_cost -0.1525
- `cheapOracle_n8`: posterior area 0.6665, risk 0.3335, %cost 0.002107, omega_cost -0.1725
- `expensiveOracle_n8`: posterior area 0.9995, risk 0.0005, %cost 0.02938, omega_cost 0.01596
- `diversity_n16`: posterior area 0.993, risk 0.007, %cost 0.007976, omega_cost 0.0487
- `diversity_n20`: posterior area 0.999, risk 0.001, %cost 0.01242, omega_cost 0.03625

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n8` | `supports` | 25.72 | 5.66e-04 | large (0.1613) | median risks: random=0.09275, balanced=0.0425, diversity=0.01, SRSSampling=0.0805, pairwise=0.041, pilotCost=0.396, cheapOracle=0.3335, expensiveOracle=0.0005; spread=0.3955 |
| `FSE1` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n16` | `supports` | 21.4 | 0.00323 | large (0.1241) | median risks: random=0.044, balanced=0.0315, diversity=0.007, SRSSampling=0.044, pairwise=0.0155, pilotCost=0.257, cheapOracle=0.156, expensiveOracle=0.0005; spread=0.2565 |
| `FSE1` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n20` | `supports` | 16.24 | 0.023 | large (0.07967) | median risks: random=0.03675, balanced=0.035, diversity=0.001, SRSSampling=0.0425, pairwise=0.0155, pilotCost=0.045, cheapOracle=0.156, expensiveOracle=0.0005; spread=0.1555 |
| `FSE1` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n32` | `supports` | 21.05 | 0.0037 | large (0.1211) | median risks: random=0.0255, balanced=0.01, diversity=0.001, SRSSampling=0.02175, pairwise=0.0155, pilotCost=0.06625, cheapOracle=0.156, expensiveOracle=0.0005; spread=0.1555 |
| `FSE1` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n40` | `supports` | 18.42 | 0.0102 | large (0.09843) | median risks: random=0.01, balanced=0.006, diversity=0.001, SRSSampling=0.0155, pairwise=0.0155, pilotCost=0.037, cheapOracle=0.156, expensiveOracle=0.0005; spread=0.1555 |
| `FSE1` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n64` | `supports` | 17.99 | 0.012 | large (0.09474) | median risks: random=0.013, balanced=0.004, diversity=0.001, SRSSampling=0.0095, pairwise=0.0155, pilotCost=0.01, cheapOracle=0.1475, expensiveOracle=0.0005; spread=0.147 |
| `FSE2` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.06273) | best size-normalized=expensiveOracle_n8; best cost-normalized=balanced_n8 |
| `FSE3` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.0869) | best cost-normalized=balanced_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n8; empirical front=balanced_n8,cheapOracle_n8,diversity_n8,expensiveOracle_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 424.5 | 0.902 | negligible (0.4717) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0805, median random=0.09275 |
| `FSE6` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 441.5 | 0.708 | negligible (0.4906) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003834, median random=0.003876 |
| `FSE2` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.04023) | best size-normalized=expensiveOracle_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.05278) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16,expensiveOracle_n16,pairwise_n16 |
| `FSE5` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 439.5 | 0.731 | negligible (0.4883) | A12<0.5 means SRS risks tend to be lower; median SRS=0.044, median random=0.044 |
| `FSE6` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 429.5 | 0.844 | negligible (0.5228) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007783, median random=0.007684 |
| `FSE2` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.02965) | best size-normalized=expensiveOracle_n20; best cost-normalized=balanced_n20 |
| `FSE3` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.04186) | best cost-normalized=balanced_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n20; empirical front=balanced_n20,cheapOracle_n20,diversity_n20,expensiveOracle_n20,pairwise_n20 |
| `FSE5` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 432.5 | 0.81 | negligible (0.5194) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0425, median random=0.03675 |
| `FSE6` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 448.5 | 0.633 | negligible (0.4983) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009761, median random=0.009761 |
| `FSE2` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.01875) | best size-normalized=expensiveOracle_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02229) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n32; empirical front=balanced_n32,cheapOracle_n32,diversity_n32,expensiveOracle_n32,pairwise_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 385.5 | 0.649 | small (0.4283) | A12<0.5 means SRS risks tend to be lower; median SRS=0.02175, median random=0.0255 |
| `FSE6` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 390 | 0.699 | small (0.5667) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0162, median random=0.01509 |
| `FSE2` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.01512) | best size-normalized=expensiveOracle_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.01434) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n40; empirical front=balanced_n40,cheapOracle_n40,diversity_n40,expensiveOracle_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 439 | 0.736 | negligible (0.4878) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0155, median random=0.01 |
| `FSE6` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 430 | 0.838 | negligible (0.4778) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01945, median random=0.02023 |
| `FSE2` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.009315) | best size-normalized=expensiveOracle_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01052) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n64; empirical front=balanced_n64,cheapOracle_n64,diversity_n64,expensiveOracle_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 381 | 0.602 | small (0.4233) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0095, median random=0.013 |
| `FSE6` | `lcbench__workload_phoneme__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 421 | 0.943 | negligible (0.4678) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0325, median random=0.0322 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003876 | 0.09275 | 0.88 | -0.02 | -0.01746 |
| `balanced_n8` | 8 | 0.004 | 0.002962 | 0.0425 | 0.9525 | 0.0525 | 0.07868 |
| `diversity_n8` | 8 | 0.004 | 0.005018 | 0.01 | 0.99 | 0.09 | 0.07308 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003834 | 0.0805 | 0.8883 | -0.01165 | -0.008222 |
| `pairwise_n8` | 8 | 0.004 | 0.003282 | 0.041 | 0.959 | 0.059 | 0.07577 |
| `pilotCost_n8` | 8 | 0.004 | 0.00243 | 0.396 | 0.7017 | -0.1983 | -0.1525 |
| `cheapOracle_n8` | 8 | 0.004 | 0.002107 | 0.3335 | 0.6665 | -0.2335 | -0.1725 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.02938 | 0.0005 | 0.9995 | 0.0995 | 0.01596 |
| `random_n16` | 16 | 0.008 | 0.007684 | 0.044 | 0.9357 | -0.008761 | -0.006738 |
| `balanced_n16` | 16 | 0.008 | 0.005648 | 0.0315 | 0.9695 | 0.02502 | 0.04468 |
| `diversity_n16` | 16 | 0.008 | 0.007976 | 0.007 | 0.993 | 0.04856 | 0.0487 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007783 | 0.044 | 0.939 | -0.005444 | -0.004074 |
| `pairwise_n16` | 16 | 0.008 | 0.007256 | 0.0155 | 0.9845 | 0.04006 | 0.04506 |
| `pilotCost_n16` | 16 | 0.008 | 0.004864 | 0.257 | 0.7789 | -0.1655 | -0.1358 |
| `cheapOracle_n16` | 16 | 0.008 | 0.00428 | 0.156 | 0.844 | -0.1004 | -0.06131 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.05474 | 0.0005 | 0.9995 | 0.05506 | 0.008471 |
| `random_n20` | 20 | 0.01 | 0.009761 | 0.03675 | 0.9514 | -0.003145 | -0.002134 |
| `balanced_n20` | 20 | 0.01 | 0.006894 | 0.035 | 0.9733 | 0.01872 | 0.0366 |
| `diversity_n20` | 20 | 0.01 | 0.01242 | 0.001 | 0.999 | 0.04445 | 0.03625 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009761 | 0.0425 | 0.9483 | -0.006262 | -0.005251 |
| `pairwise_n20` | 20 | 0.01 | 0.008963 | 0.0155 | 0.9845 | 0.02995 | 0.03469 |
| `pilotCost_n20` | 20 | 0.01 | 0.006058 | 0.045 | 0.8259 | -0.1286 | -0.1032 |
| `cheapOracle_n20` | 20 | 0.01 | 0.005374 | 0.156 | 0.844 | -0.1105 | -0.07756 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.0661 | 0.0005 | 0.9995 | 0.04495 | 0.006952 |
| `random_n32` | 32 | 0.016 | 0.01509 | 0.0255 | 0.9655 | -0.005105 | -0.003438 |
| `balanced_n32` | 32 | 0.016 | 0.01096 | 0.01 | 0.9743 | 0.003745 | 0.01615 |
| `diversity_n32` | 32 | 0.016 | 0.01951 | 0.001 | 0.999 | 0.02841 | 0.02337 |
| `SRSSampling_n32` | 32 | 0.016 | 0.0162 | 0.02175 | 0.972 | 0.001428 | 0.001086 |
| `pairwise_n32` | 32 | 0.016 | 0.01525 | 0.0155 | 0.9845 | 0.01391 | 0.01528 |
| `pilotCost_n32` | 32 | 0.016 | 0.009592 | 0.06625 | 0.8447 | -0.1259 | -0.1081 |
| `cheapOracle_n32` | 32 | 0.016 | 0.008678 | 0.156 | 0.844 | -0.1266 | -0.1043 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.09658 | 0.0005 | 0.9995 | 0.02891 | 0.004624 |
| `random_n40` | 40 | 0.02 | 0.02023 | 0.01 | 0.9787 | 0.002526 | 0.002265 |
| `balanced_n40` | 40 | 0.02 | 0.01391 | 0.006 | 0.9854 | 0.00921 | 0.01893 |
| `diversity_n40` | 40 | 0.02 | 0.02888 | 0.001 | 0.999 | 0.02281 | 0.01573 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01945 | 0.0155 | 0.9801 | 0.00396 | 0.004595 |
| `pairwise_n40` | 40 | 0.02 | 0.01855 | 0.0155 | 0.9845 | 0.00831 | 0.01007 |
| `pilotCost_n40` | 40 | 0.02 | 0.01204 | 0.037 | 0.8548 | -0.1214 | -0.1069 |
| `cheapOracle_n40` | 40 | 0.02 | 0.0109 | 0.156 | 0.844 | -0.1322 | -0.114 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.1148 | 0.0005 | 0.9995 | 0.02331 | 0.003817 |
| `random_n64` | 64 | 0.032 | 0.0322 | 0.013 | 0.9833 | -0.001565 | -0.001657 |
| `balanced_n64` | 64 | 0.032 | 0.02308 | 0.004 | 0.9911 | 0.006235 | 0.01185 |
| `diversity_n64` | 64 | 0.032 | 0.04055 | 0.001 | 0.999 | 0.01415 | 0.01103 |
| `SRSSampling_n64` | 64 | 0.032 | 0.0325 | 0.0095 | 0.9864 | 0.001552 | 0.001325 |
| `pairwise_n64` | 64 | 0.032 | 0.03031 | 0.0155 | 0.9845 | -0.0003485 | 0.0004713 |
| `pilotCost_n64` | 64 | 0.032 | 0.01935 | 0.01 | 0.9844 | -0.0004652 | 0.00895 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01763 | 0.1475 | 0.8525 | -0.1323 | -0.1207 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.1638 | 0.0005 | 0.9995 | 0.01465 | 0.002534 |
