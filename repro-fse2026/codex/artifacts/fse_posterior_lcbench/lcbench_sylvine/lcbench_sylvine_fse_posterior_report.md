# lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `balanced_n64` (risk 0.0015, %cost 0.02279).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pairwise_n8` (omega_cost 0.09277, %cost 0.003357).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9339, risk 0.0345, %cost 0.002954, omega_cost 0.06032
- `pairwise_n8`: posterior area 0.978, risk 0.022, %cost 0.003357, omega_cost 0.09277
- `pilotCost_n8`: posterior area 0.8619, risk 0.139, %cost 0.002375, omega_cost 0.01009
- `cheapOracle_n8`: posterior area 0.7435, risk 0.2565, %cost 0.002027, omega_cost -0.0913
- `expensiveOracle_n8`: posterior area 0.9945, risk 0.0055, %cost 0.02815, omega_cost 0.01165
- `diversity_n16`: posterior area 0.993, risk 0.007, %cost 0.008015, omega_cost 0.04846
- `balanced_n64`: posterior area 0.9938, risk 0.0015, %cost 0.02279, omega_cost 0.01477

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n8` | `supports` | 20.22 | 0.00512 | large (0.1139) | median risks: random=0.07625, balanced=0.0345, diversity=0.024, SRSSampling=0.07625, pairwise=0.022, pilotCost=0.139, cheapOracle=0.2565, expensiveOracle=0.0055; spread=0.251 |
| `FSE1` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n16` | `supports` | 41.96 | 5.29e-07 | large (0.3014) | median risks: random=0.04, balanced=0.01775, diversity=0.007, SRSSampling=0.03725, pairwise=0.022, pilotCost=0.0915, cheapOracle=0.2565, expensiveOracle=0.0055; spread=0.251 |
| `FSE1` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n20` | `supports` | 15.74 | 0.0276 | large (0.07539) | median risks: random=0.04, balanced=0.028, diversity=0.007, SRSSampling=0.04, pairwise=0.022, pilotCost=0.06275, cheapOracle=0.139, expensiveOracle=0.0055; spread=0.1335 |
| `FSE1` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n32` | `supports` | 26.53 | 4.05e-04 | large (0.1683) | median risks: random=0.024, balanced=0.007, diversity=0.007, SRSSampling=0.024, pairwise=0.022, pilotCost=0.08375, cheapOracle=0.139, expensiveOracle=0.0055; spread=0.1335 |
| `FSE1` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n40` | `supports` | 24.57 | 9.06e-04 | large (0.1514) | median risks: random=0.0165, balanced=0.003, diversity=0.0055, SRSSampling=0.022, pairwise=0.022, pilotCost=0.0855, cheapOracle=0.024, expensiveOracle=0.0055; spread=0.0825 |
| `FSE1` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n64` | `supports` | 27.24 | 3.02e-04 | moderate (0.1745) | median risks: random=0.00875, balanced=0.0015, diversity=0.0055, SRSSampling=0.0105, pairwise=0.022, pilotCost=0.019, cheapOracle=0.024, expensiveOracle=0.0055; spread=0.0225 |
| `FSE2` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.08112) | best size-normalized=expensiveOracle_n8; best cost-normalized=pairwise_n8 |
| `FSE3` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.07954) | best cost-normalized=pairwise_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n8; empirical front=balanced_n8,cheapOracle_n8,expensiveOracle_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 440.5 | 0.719 | negligible (0.4894) | A12<0.5 means SRS risks tend to be lower; median SRS=0.07625, median random=0.07625 |
| `FSE6` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 439.5 | 0.73 | negligible (0.4883) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003728, median random=0.003881 |
| `FSE2` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.04567) | best size-normalized=expensiveOracle_n16; best cost-normalized=balanced_n16 |
| `FSE3` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.05555) | best cost-normalized=balanced_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16,expensiveOracle_n16,pairwise_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 431 | 0.827 | negligible (0.4789) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03725, median random=0.04 |
| `FSE6` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 432.5 | 0.809 | negligible (0.5194) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007746, median random=0.00766 |
| `FSE2` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.03085) | best size-normalized=expensiveOracle_n20; best cost-normalized=balanced_n20 |
| `FSE3` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.04298) | best cost-normalized=balanced_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n20; empirical front=balanced_n20,cheapOracle_n20,diversity_n20,expensiveOracle_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 443.5 | 0.686 | negligible (0.5072) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04, median random=0.04 |
| `FSE6` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 446.5 | 0.654 | negligible (0.4961) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009644, median random=0.009644 |
| `FSE2` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.02418) | best size-normalized=expensiveOracle_n32; best cost-normalized=balanced_n32 |
| `FSE3` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02184) | best cost-normalized=balanced_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n32; empirical front=balanced_n32,cheapOracle_n32,diversity_n32,expensiveOracle_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 447.5 | 0.643 | negligible (0.4972) | A12<0.5 means SRS risks tend to be lower; median SRS=0.024, median random=0.024 |
| `FSE6` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 409 | 0.915 | negligible (0.5456) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01597, median random=0.01507 |
| `FSE2` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.009638) | best size-normalized=diversity_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.02097) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n40,expensiveOracle_n40; empirical front=balanced_n40,cheapOracle_n40,diversity_n40 |
| `FSE5` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 390 | 0.697 | small (0.5667) | A12<0.5 means SRS risks tend to be lower; median SRS=0.022, median random=0.0165 |
| `FSE6` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 395 | 0.754 | small (0.4389) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0196, median random=0.02008 |
| `FSE2` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.008309) | best size-normalized=diversity_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01109) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n64,expensiveOracle_n64; empirical front=balanced_n64,cheapOracle_n64,diversity_n64 |
| `FSE5` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 448.5 | 0.633 | negligible (0.5017) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0105, median random=0.00875 |
| `FSE6` | `lcbench__workload_sylvine__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 407 | 0.892 | negligible (0.4522) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0323, median random=0.03231 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003881 | 0.07625 | 0.9056 | 0.00565 | 0.008091 |
| `balanced_n8` | 8 | 0.004 | 0.002954 | 0.0345 | 0.9339 | 0.03385 | 0.06032 |
| `diversity_n8` | 8 | 0.004 | 0.005075 | 0.024 | 0.976 | 0.076 | 0.05831 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003728 | 0.07625 | 0.9075 | 0.007483 | 0.01323 |
| `pairwise_n8` | 8 | 0.004 | 0.003357 | 0.022 | 0.978 | 0.078 | 0.09277 |
| `pilotCost_n8` | 8 | 0.004 | 0.002375 | 0.139 | 0.8619 | -0.03807 | 0.01009 |
| `cheapOracle_n8` | 8 | 0.004 | 0.002027 | 0.2565 | 0.7435 | -0.1565 | -0.0913 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.02815 | 0.0055 | 0.9945 | 0.0945 | 0.01165 |
| `random_n16` | 16 | 0.008 | 0.00766 | 0.04 | 0.9312 | -0.01328 | -0.01109 |
| `balanced_n16` | 16 | 0.008 | 0.005555 | 0.01775 | 0.9732 | 0.02874 | 0.04946 |
| `diversity_n16` | 16 | 0.008 | 0.008015 | 0.007 | 0.993 | 0.04856 | 0.04846 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007746 | 0.03725 | 0.9367 | -0.007694 | -0.006082 |
| `pairwise_n16` | 16 | 0.008 | 0.007372 | 0.022 | 0.978 | 0.03356 | 0.03772 |
| `pilotCost_n16` | 16 | 0.008 | 0.004711 | 0.0915 | 0.8842 | -0.06021 | -0.02821 |
| `cheapOracle_n16` | 16 | 0.008 | 0.004137 | 0.2565 | 0.7435 | -0.2009 | -0.1592 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.05278 | 0.0055 | 0.9945 | 0.05006 | 0.003796 |
| `random_n20` | 20 | 0.01 | 0.009644 | 0.04 | 0.9443 | -0.01025 | -0.008726 |
| `balanced_n20` | 20 | 0.01 | 0.006837 | 0.028 | 0.9692 | 0.01465 | 0.033 |
| `diversity_n20` | 20 | 0.01 | 0.01264 | 0.007 | 0.993 | 0.03845 | 0.02967 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009644 | 0.04 | 0.9431 | -0.0115 | -0.009976 |
| `pairwise_n20` | 20 | 0.01 | 0.008999 | 0.022 | 0.978 | 0.02345 | 0.02801 |
| `pilotCost_n20` | 20 | 0.01 | 0.006 | 0.06275 | 0.9277 | -0.02681 | -0.0008373 |
| `cheapOracle_n20` | 20 | 0.01 | 0.005208 | 0.139 | 0.861 | -0.09355 | -0.05847 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.06431 | 0.0055 | 0.9945 | 0.03995 | 0.002156 |
| `random_n32` | 32 | 0.016 | 0.01507 | 0.024 | 0.9703 | -0.0003216 | 0.001372 |
| `balanced_n32` | 32 | 0.016 | 0.0108 | 0.007 | 0.9815 | 0.01095 | 0.02391 |
| `diversity_n32` | 32 | 0.016 | 0.01972 | 0.007 | 0.993 | 0.02241 | 0.01713 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01597 | 0.024 | 0.9726 | 0.002012 | 0.002068 |
| `pairwise_n32` | 32 | 0.016 | 0.01519 | 0.022 | 0.978 | 0.007412 | 0.008874 |
| `pilotCost_n32` | 32 | 0.016 | 0.0096 | 0.08375 | 0.9289 | -0.04172 | -0.02397 |
| `cheapOracle_n32` | 32 | 0.016 | 0.008444 | 0.139 | 0.861 | -0.1096 | -0.08606 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.0946 | 0.0055 | 0.9945 | 0.02391 | -0.0002697 |
| `random_n40` | 40 | 0.02 | 0.02008 | 0.0165 | 0.9764 | 0.0002262 | 0.0001396 |
| `balanced_n40` | 40 | 0.02 | 0.01374 | 0.003 | 0.9868 | 0.01058 | 0.02069 |
| `diversity_n40` | 40 | 0.02 | 0.0292 | 0.0055 | 0.9945 | 0.01831 | 0.01106 |
| `SRSSampling_n40` | 40 | 0.02 | 0.0196 | 0.022 | 0.9755 | -0.0007405 | -0.0002784 |
| `pairwise_n40` | 40 | 0.02 | 0.01854 | 0.022 | 0.978 | 0.00181 | 0.003593 |
| `pilotCost_n40` | 40 | 0.02 | 0.0119 | 0.0855 | 0.9435 | -0.03272 | -0.01777 |
| `cheapOracle_n40` | 40 | 0.02 | 0.01062 | 0.024 | 0.976 | -0.0001905 | 0.01904 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.1129 | 0.0055 | 0.9945 | 0.01831 | -0.001111 |
| `random_n64` | 64 | 0.032 | 0.03231 | 0.00875 | 0.9849 | 1.515e-06 | -0.000138 |
| `balanced_n64` | 64 | 0.032 | 0.02279 | 0.0015 | 0.9938 | 0.008902 | 0.01477 |
| `diversity_n64` | 64 | 0.032 | 0.04082 | 0.0055 | 0.9945 | 0.009652 | 0.006456 |
| `SRSSampling_n64` | 64 | 0.032 | 0.0323 | 0.0105 | 0.9887 | 0.003818 | 0.00368 |
| `pairwise_n64` | 64 | 0.032 | 0.03005 | 0.022 | 0.978 | -0.006848 | -0.005899 |
| `pilotCost_n64` | 64 | 0.032 | 0.01914 | 0.019 | 0.9715 | -0.01335 | -0.003672 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01721 | 0.024 | 0.976 | -0.008848 | 0.003458 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.1621 | 0.0055 | 0.9945 | 0.009652 | -0.002435 |
