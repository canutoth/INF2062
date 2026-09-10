# lcbench__workload_volkert__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n20` (risk 0.001, %cost 0.01252).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n8` (omega_cost 0.07385, %cost 0.005592).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.998, risk 0.002, %cost 0.005592, omega_cost 0.07385
- `pairwise_n8`: posterior area 0.9465, risk 0.0535, %cost 0.00342, omega_cost 0.05963
- `pilotCost_n8`: posterior area 0.8949, risk 0.076, %cost 0.002148, omega_cost 0.05374
- `diversity_n20`: posterior area 0.999, risk 0.001, %cost 0.01252, omega_cost 0.03598
- `pilotCost_n20`: posterior area 0.9508, risk 0.04925, %cost 0.005543, omega_cost 0.0272

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n8` | `inconclusive` | 6.487 | 0.262 | large (0.01282) | median risks: random=0.0975, balanced=0.067, diversity=0.002, SRSSampling=0.085, pairwise=0.0535, pilotCost=0.076; spread=0.0955 |
| `FSE1` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n16` | `inconclusive` | 8.15 | 0.148 | moderate (0.02715) | median risks: random=0.03575, balanced=0.034, diversity=0.002, SRSSampling=0.03575, pairwise=0.03, pilotCost=0.05125; spread=0.04925 |
| `FSE1` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 5.764 | 0.33 | moderate (0.006582) | median risks: random=0.04625, balanced=0.034, diversity=0.001, SRSSampling=0.04875, pairwise=0.03, pilotCost=0.04925; spread=0.04825 |
| `FSE1` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n32` | `supports` | 11.19 | 0.0477 | moderate (0.0534) | median risks: random=0.0225, balanced=0.0255, diversity=0.001, SRSSampling=0.02475, pairwise=0.03, pilotCost=0.04725; spread=0.04625 |
| `FSE1` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n40` | `supports` | 18.85 | 0.00205 | moderate (0.1194) | median risks: random=0.012, balanced=0.011, diversity=0.001, SRSSampling=0.023, pairwise=0.03, pilotCost=0.048; spread=0.047 |
| `FSE1` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n64` | `supports` | 17.33 | 0.00392 | moderate (0.1063) | median risks: random=0.0115, balanced=0.00325, diversity=0.001, SRSSampling=0.012, pairwise=0.03, pilotCost=0.024; spread=0.029 |
| `FSE2` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n8; best cost-normalized=diversity_n8 |
| `FSE3` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.0937) | best cost-normalized=diversity_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n8; empirical front=diversity_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 426.5 | 0.879 | negligible (0.4739) | A12<0.5 means SRS risks tend to be lower; median SRS=0.085, median random=0.0975 |
| `FSE6` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 439.5 | 0.73 | negligible (0.4883) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003773, median random=0.003773 |
| `FSE2` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.04231) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n16; empirical front=diversity_n16,pairwise_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 443.5 | 0.686 | negligible (0.4928) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03575, median random=0.03575 |
| `FSE6` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 424.5 | 0.902 | negligible (0.5283) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0075, median random=0.007403 |
| `FSE2` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n20; best cost-normalized=diversity_n20 |
| `FSE3` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.04449) | best cost-normalized=diversity_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n20; empirical front=balanced_n20,diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 441 | 0.714 | negligible (0.51) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04875, median random=0.04625 |
| `FSE6` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 440.5 | 0.719 | negligible (0.4894) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009426, median random=0.009519 |
| `FSE2` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02848) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n32; empirical front=balanced_n32,diversity_n32,pilotCost_n32,random_n32 |
| `FSE5` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 446.5 | 0.654 | negligible (0.5039) | A12<0.5 means SRS risks tend to be lower; median SRS=0.02475, median random=0.0225 |
| `FSE6` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 399 | 0.799 | negligible (0.5567) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01543, median random=0.01474 |
| `FSE2` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n40; best cost-normalized=diversity_n40 |
| `FSE3` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.02147) | best cost-normalized=diversity_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n40; empirical front=balanced_n40,diversity_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 369 | 0.485 | small (0.59) | A12<0.5 means SRS risks tend to be lower; median SRS=0.023, median random=0.012 |
| `FSE6` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 403 | 0.845 | negligible (0.4478) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01946, median random=0.01992 |
| `FSE2` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.0002709) | best size-normalized=diversity_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01259) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n64; empirical front=balanced_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 411 | 0.939 | negligible (0.5433) | A12<0.5 means SRS risks tend to be lower; median SRS=0.012, median random=0.0115 |
| `FSE6` | `lcbench__workload_volkert__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 337 | 0.242 | small (0.3744) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03043, median random=0.03192 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003773 | 0.0975 | 0.8693 | -0.03073 | -0.02597 |
| `balanced_n8` | 8 | 0.004 | 0.003989 | 0.067 | 0.9181 | 0.01807 | 0.01828 |
| `diversity_n8` | 8 | 0.004 | 0.005592 | 0.002 | 0.998 | 0.098 | 0.07385 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003773 | 0.085 | 0.8754 | -0.02462 | -0.01985 |
| `pairwise_n8` | 8 | 0.004 | 0.00342 | 0.0535 | 0.9465 | 0.0465 | 0.05963 |
| `pilotCost_n8` | 8 | 0.004 | 0.002148 | 0.076 | 0.8949 | -0.005067 | 0.05374 |
| `random_n16` | 16 | 0.008 | 0.007403 | 0.03575 | 0.9419 | -0.002561 | 0.001384 |
| `balanced_n16` | 16 | 0.008 | 0.007323 | 0.034 | 0.9611 | 0.01667 | 0.02119 |
| `diversity_n16` | 16 | 0.008 | 0.008904 | 0.002 | 0.998 | 0.05356 | 0.04848 |
| `SRSSampling_n16` | 16 | 0.008 | 0.0075 | 0.03575 | 0.9474 | 0.002906 | 0.006171 |
| `pairwise_n16` | 16 | 0.008 | 0.007298 | 0.03 | 0.97 | 0.02556 | 0.03025 |
| `pilotCost_n16` | 16 | 0.008 | 0.00427 | 0.05125 | 0.9283 | -0.01611 | 0.02321 |
| `random_n20` | 20 | 0.01 | 0.009519 | 0.04625 | 0.9446 | -0.009979 | -0.007898 |
| `balanced_n20` | 20 | 0.01 | 0.008799 | 0.034 | 0.9591 | 0.004555 | 0.01012 |
| `diversity_n20` | 20 | 0.01 | 0.01252 | 0.001 | 0.999 | 0.04445 | 0.03598 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009426 | 0.04875 | 0.9435 | -0.01101 | -0.008511 |
| `pairwise_n20` | 20 | 0.01 | 0.009333 | 0.03 | 0.97 | 0.01545 | 0.01839 |
| `pilotCost_n20` | 20 | 0.01 | 0.005543 | 0.04925 | 0.9508 | -0.003762 | 0.0272 |
| `random_n32` | 32 | 0.016 | 0.01474 | 0.0225 | 0.9715 | 0.0009451 | 0.003301 |
| `balanced_n32` | 32 | 0.016 | 0.01399 | 0.0255 | 0.9706 | 1.176e-05 | 0.003947 |
| `diversity_n32` | 32 | 0.016 | 0.01891 | 0.001 | 0.999 | 0.02841 | 0.02411 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01543 | 0.02475 | 0.9652 | -0.005388 | -0.00437 |
| `pairwise_n32` | 32 | 0.016 | 0.01551 | 0.03 | 0.97 | -0.0005882 | 0.0002912 |
| `pilotCost_n32` | 32 | 0.016 | 0.008738 | 0.04725 | 0.9465 | -0.02407 | -0.002139 |
| `random_n40` | 40 | 0.02 | 0.01992 | 0.012 | 0.9806 | 0.00441 | 0.004504 |
| `balanced_n40` | 40 | 0.02 | 0.01693 | 0.011 | 0.9833 | 0.007093 | 0.01118 |
| `diversity_n40` | 40 | 0.02 | 0.02682 | 0.001 | 0.999 | 0.02281 | 0.01697 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01946 | 0.023 | 0.9711 | -0.005124 | -0.004493 |
| `pairwise_n40` | 40 | 0.02 | 0.0186 | 0.03 | 0.97 | -0.00619 | -0.004494 |
| `pilotCost_n40` | 40 | 0.02 | 0.01069 | 0.048 | 0.9593 | -0.01694 | 0.002016 |
| `random_n64` | 64 | 0.032 | 0.03192 | 0.0115 | 0.9853 | 0.0004848 | 0.0005226 |
| `balanced_n64` | 64 | 0.032 | 0.02663 | 0.00325 | 0.994 | 0.009102 | 0.01205 |
| `diversity_n64` | 64 | 0.032 | 0.03813 | 0.001 | 0.999 | 0.01415 | 0.01178 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03043 | 0.012 | 0.9836 | -0.001298 | -0.0005401 |
| `pairwise_n64` | 64 | 0.032 | 0.02984 | 0.03 | 0.97 | -0.01485 | -0.01379 |
| `pilotCost_n64` | 64 | 0.032 | 0.01801 | 0.024 | 0.9792 | -0.005682 | 0.005465 |
