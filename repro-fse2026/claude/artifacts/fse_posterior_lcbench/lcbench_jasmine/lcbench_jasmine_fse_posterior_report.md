# lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `balanced_n64` (risk 0.0015, %cost 0.02161).

Best integrated confidence after normalizing the prior baseline by empirical cost: `cheapOracle_n8` (omega_cost 0.1337, %cost 0.001522).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9658, risk 0.0065, %cost 0.002834, omega_cost 0.0962
- `pilotCost_n8`: posterior area 0.9632, risk 0.025, %cost 0.001955, omega_cost 0.1324
- `cheapOracle_n8`: posterior area 0.9355, risk 0.0645, %cost 0.001522, omega_cost 0.1337
- `balanced_n16`: posterior area 0.9907, risk 0.0065, %cost 0.005269, omega_cost 0.07041
- `pilotCost_n16`: posterior area 0.9699, risk 0.01575, %cost 0.003908, omega_cost 0.07183
- `balanced_n32`: posterior area 0.9942, risk 0.004, %cost 0.01036, omega_cost 0.03819
- `pilotCost_n40`: posterior area 0.9936, risk 0.0065, %cost 0.009745, omega_cost 0.04011
- `balanced_n64`: posterior area 0.9974, risk 0.0015, %cost 0.02161, omega_cost 0.01951
- `pilotCost_n64`: posterior area 0.9958, risk 0.0065, %cost 0.01647, omega_cost 0.02446

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n8` | `supports` | 23.87 | 0.0012 | large (0.1454) | median risks: random=0.0645, balanced=0.0065, diversity=0.0645, SRSSampling=0.0645, pairwise=0.0925, pilotCost=0.025, cheapOracle=0.0645, expensiveOracle=0.0645; spread=0.086 |
| `FSE1` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n16` | `supports` | 17.13 | 0.0166 | large (0.08729) | median risks: random=0.0065, balanced=0.0065, diversity=0.0645, SRSSampling=0.0065, pairwise=0.0925, pilotCost=0.01575, cheapOracle=0.0645, expensiveOracle=0.0065; spread=0.086 |
| `FSE1` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n20` | `supports` | 23.4 | 0.00145 | large (0.1414) | median risks: random=0.0065, balanced=0.004, diversity=0.0645, SRSSampling=0.0065, pairwise=0.0455, pilotCost=0.0065, cheapOracle=0.0645, expensiveOracle=0.0065; spread=0.0605 |
| `FSE1` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n32` | `supports` | 28.94 | 1.48e-04 | large (0.1892) | median risks: random=0.0065, balanced=0.004, diversity=0.025, SRSSampling=0.025, pairwise=0.0065, pilotCost=0.0065, cheapOracle=0.0645, expensiveOracle=0.0065; spread=0.0605 |
| `FSE1` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n40` | `supports` | 25.92 | 5.20e-04 | large (0.1631) | median risks: random=0.01575, balanced=0.004, diversity=0.025, SRSSampling=0.0065, pairwise=0.0065, pilotCost=0.0065, cheapOracle=0.0645, expensiveOracle=0.0065; spread=0.0605 |
| `FSE1` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n64` | `supports` | 29.03 | 1.43e-04 | small (0.1899) | median risks: random=0.0065, balanced=0.0015, diversity=0.0065, SRSSampling=0.0065, pairwise=0.0065, pilotCost=0.0065, cheapOracle=0.0065, expensiveOracle=0.0065; spread=0.005 |
| `FSE2` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.03753) | best size-normalized=balanced_n8; best cost-normalized=cheapOracle_n8 |
| `FSE3` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.1246) | best cost-normalized=cheapOracle_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.3333 |  | large frontier change (2) | count front=balanced_n8; empirical front=balanced_n8,cheapOracle_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 440.5 | 0.72 | negligible (0.4894) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0645, median random=0.0645 |
| `FSE6` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 434.5 | 0.787 | negligible (0.4828) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003692, median random=0.003827 |
| `FSE2` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.06858) | best size-normalized=expensiveOracle_n16; best cost-normalized=pilotCost_n16 |
| `FSE3` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.04908) | best cost-normalized=pilotCost_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.25 |  | large frontier change (3) | count front=expensiveOracle_n16; empirical front=balanced_n16,cheapOracle_n16,expensiveOracle_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 447.5 | 0.644 | negligible (0.4972) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0065, median random=0.0065 |
| `FSE6` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 436.5 | 0.764 | negligible (0.515) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007658, median random=0.007585 |
| `FSE2` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.05018) | best size-normalized=expensiveOracle_n20; best cost-normalized=pilotCost_n20 |
| `FSE3` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.03766) | best cost-normalized=pilotCost_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.25 |  | large frontier change (3) | count front=expensiveOracle_n20; empirical front=balanced_n20,cheapOracle_n20,expensiveOracle_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 450 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0065, median random=0.0065 |
| `FSE6` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 443.5 | 0.686 | negligible (0.4928) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01, median random=0.01 |
| `FSE2` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.009107) | best size-normalized=balanced_n32; best cost-normalized=pilotCost_n32 |
| `FSE3` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.04333) | best cost-normalized=pilotCost_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.3333 |  | large frontier change (2) | count front=balanced_n32; empirical front=balanced_n32,cheapOracle_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 375.5 | 0.527 | small (0.5828) | A12<0.5 means SRS risks tend to be lower; median SRS=0.025, median random=0.0065 |
| `FSE6` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 426 | 0.885 | negligible (0.5267) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01549, median random=0.01533 |
| `FSE2` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | unchanged (0) | best size-normalized=pilotCost_n40; best cost-normalized=pilotCost_n40 |
| `FSE3` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.03136) | best cost-normalized=pilotCost_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.5 |  | frontier change (1) | count front=pilotCost_n40; empirical front=cheapOracle_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 416 | 0.977 | negligible (0.4622) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0065, median random=0.01575 |
| `FSE6` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 329 | 0.197 | small (0.3656) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01873, median random=0.02061 |
| `FSE2` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.00712) | best size-normalized=balanced_n64; best cost-normalized=cheapOracle_n64 |
| `FSE3` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.02677) | best cost-normalized=cheapOracle_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.3333 |  | large frontier change (2) | count front=balanced_n64; empirical front=balanced_n64,cheapOracle_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 345 | 0.26 | small (0.6167) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0065, median random=0.0065 |
| `FSE6` | `lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy:n64` | `supports` | 272 | 0.033 | medium (0.3022) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0296, median random=0.03265 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003827 | 0.0645 | 0.898 | -0.002033 | 0.001552 |
| `balanced_n8` | 8 | 0.004 | 0.002834 | 0.0065 | 0.9658 | 0.06578 | 0.0962 |
| `diversity_n8` | 8 | 0.004 | 0.004961 | 0.0645 | 0.9355 | 0.0355 | 0.01938 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003692 | 0.0645 | 0.9026 | 0.002567 | 0.009127 |
| `pairwise_n8` | 8 | 0.004 | 0.003637 | 0.0925 | 0.9075 | 0.0075 | 0.01533 |
| `pilotCost_n8` | 8 | 0.004 | 0.001955 | 0.025 | 0.9632 | 0.06317 | 0.1324 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001522 | 0.0645 | 0.9355 | 0.0355 | 0.1337 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.0269 | 0.0645 | 0.9355 | 0.0355 | -0.04658 |
| `random_n16` | 16 | 0.008 | 0.007585 | 0.0065 | 0.9644 | 0.01992 | 0.02261 |
| `balanced_n16` | 16 | 0.008 | 0.005269 | 0.0065 | 0.9907 | 0.04621 | 0.07041 |
| `diversity_n16` | 16 | 0.008 | 0.008223 | 0.0645 | 0.9355 | -0.008944 | -0.01029 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007658 | 0.0065 | 0.965 | 0.02056 | 0.02275 |
| `pairwise_n16` | 16 | 0.008 | 0.008014 | 0.0925 | 0.9075 | -0.03694 | -0.03703 |
| `pilotCost_n16` | 16 | 0.008 | 0.003908 | 0.01575 | 0.9699 | 0.02551 | 0.07183 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003249 | 0.0645 | 0.9355 | -0.008944 | 0.05317 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.05029 | 0.0065 | 0.9935 | 0.04906 | 0.003248 |
| `random_n20` | 20 | 0.01 | 0.01 | 0.0065 | 0.9687 | 0.01412 | 0.01411 |
| `balanced_n20` | 20 | 0.01 | 0.006412 | 0.004 | 0.9793 | 0.02474 | 0.04674 |
| `diversity_n20` | 20 | 0.01 | 0.01263 | 0.0645 | 0.9355 | -0.01905 | -0.02781 |
| `SRSSampling_n20` | 20 | 0.01 | 0.01 | 0.0065 | 0.9687 | 0.01412 | 0.01411 |
| `pairwise_n20` | 20 | 0.01 | 0.01008 | 0.0455 | 0.9545 | -4.545e-05 | -0.0003879 |
| `pilotCost_n20` | 20 | 0.01 | 0.004913 | 0.0065 | 0.9672 | 0.01265 | 0.05177 |
| `cheapOracle_n20` | 20 | 0.01 | 0.004137 | 0.0645 | 0.9355 | -0.01905 | 0.03283 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.06083 | 0.0065 | 0.9935 | 0.03895 | 0.001587 |
| `random_n32` | 32 | 0.016 | 0.01533 | 0.0065 | 0.9746 | 0.004028 | 0.005234 |
| `balanced_n32` | 32 | 0.016 | 0.01036 | 0.004 | 0.9942 | 0.0236 | 0.03819 |
| `diversity_n32` | 32 | 0.016 | 0.01981 | 0.025 | 0.975 | 0.004412 | -0.0009756 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01549 | 0.025 | 0.9737 | 0.003062 | 0.00397 |
| `pairwise_n32` | 32 | 0.016 | 0.01624 | 0.0065 | 0.9935 | 0.02291 | 0.02251 |
| `pilotCost_n32` | 32 | 0.016 | 0.007777 | 0.0065 | 0.9903 | 0.01975 | 0.0473 |
| `cheapOracle_n32` | 32 | 0.016 | 0.006816 | 0.0645 | 0.9355 | -0.03509 | -0.0005281 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.08958 | 0.0065 | 0.9935 | 0.02291 | -0.0009798 |
| `random_n40` | 40 | 0.02 | 0.02061 | 0.01575 | 0.9809 | 0.004743 | 0.00407 |
| `balanced_n40` | 40 | 0.02 | 0.0131 | 0.004 | 0.9929 | 0.01666 | 0.02831 |
| `diversity_n40` | 40 | 0.02 | 0.02931 | 0.025 | 0.975 | -0.00119 | -0.008502 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01873 | 0.0065 | 0.9834 | 0.007226 | 0.008753 |
| `pairwise_n40` | 40 | 0.02 | 0.01961 | 0.0065 | 0.9935 | 0.01731 | 0.01776 |
| `pilotCost_n40` | 40 | 0.02 | 0.009745 | 0.0065 | 0.9936 | 0.01739 | 0.04011 |
| `cheapOracle_n40` | 40 | 0.02 | 0.008614 | 0.0645 | 0.9355 | -0.04069 | -0.01249 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.1069 | 0.0065 | 0.9935 | 0.01731 | -0.001867 |
| `random_n64` | 64 | 0.032 | 0.03265 | 0.0065 | 0.9909 | 0.006052 | 0.005759 |
| `balanced_n64` | 64 | 0.032 | 0.02161 | 0.0015 | 0.9974 | 0.01255 | 0.01951 |
| `diversity_n64` | 64 | 0.032 | 0.04101 | 0.0065 | 0.9935 | 0.008652 | 0.005403 |
| `SRSSampling_n64` | 64 | 0.032 | 0.0296 | 0.0065 | 0.9835 | -0.001332 | -0.0001417 |
| `pairwise_n64` | 64 | 0.032 | 0.03175 | 0.0065 | 0.9935 | 0.008652 | 0.008768 |
| `pilotCost_n64` | 64 | 0.032 | 0.01647 | 0.0065 | 0.9958 | 0.01098 | 0.02446 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01409 | 0.0065 | 0.9935 | 0.008652 | 0.02663 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.1545 | 0.0065 | 0.9935 | 0.008652 | -0.003285 |
