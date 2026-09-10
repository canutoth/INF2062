# lcbench__workload_covertype__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `expensiveOracle_n40` (risk 0.0015, %cost 0.2031).

Best integrated confidence after normalizing the prior baseline by empirical cost: `balanced_n8` (omega_cost 0.05509, %cost 0.004209).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9591, risk 0.0385, %cost 0.004209, omega_cost 0.05509
- `diversity_n8`: posterior area 0.992, risk 0.008, %cost 0.007854, omega_cost 0.04847
- `SRSSampling_n8`: posterior area 0.8865, risk 0.09975, %cost 0.003243, omega_cost 0.004314
- `pilotCost_n8`: posterior area 0.7931, risk 0.2085, %cost 0.002209, omega_cost -0.05108
- `cheapOracle_n8`: posterior area 0.5495, risk 0.4505, %cost 0.001593, omega_cost -0.2576
- `diversity_n20`: posterior area 0.9925, risk 0.0075, %cost 0.02481, omega_cost 0.01187
- `expensiveOracle_n40`: posterior area 0.9985, risk 0.0015, %cost 0.2031, omega_cost 0.0009498
- `balanced_n64`: posterior area 0.9936, risk 0.00625, %cost 0.02657, omega_cost 0.01175

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n8` | `supports` | 34.6 | 1.33e-05 | large (0.238) | median risks: random=0.1103, balanced=0.0385, diversity=0.008, SRSSampling=0.09975, pairwise=0.1975, pilotCost=0.2085, cheapOracle=0.4505, expensiveOracle=0.045; spread=0.4425 |
| `FSE1` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n16` | `supports` | 19.52 | 0.0067 | large (0.1079) | median risks: random=0.03975, balanced=0.02925, diversity=0.008, SRSSampling=0.03975, pairwise=0.052, pilotCost=0.113, cheapOracle=0.3705, expensiveOracle=0.03; spread=0.3625 |
| `FSE1` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n20` | `inconclusive` | 10.55 | 0.16 | large (0.03058) | median risks: random=0.049, balanced=0.0305, diversity=0.0075, SRSSampling=0.054, pairwise=0.052, pilotCost=0.0235, cheapOracle=0.277, expensiveOracle=0.03; spread=0.2695 |
| `FSE1` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n32` | `supports` | 18.67 | 0.00928 | large (0.1006) | median risks: random=0.01925, balanced=0.02775, diversity=0.0075, SRSSampling=0.01925, pairwise=0.0275, pilotCost=0.093, cheapOracle=0.277, expensiveOracle=0.03; spread=0.2695 |
| `FSE1` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n40` | `supports` | 24.8 | 8.22e-04 | large (0.1535) | median risks: random=0.013, balanced=0.0095, diversity=0.0075, SRSSampling=0.01275, pairwise=0.0275, pilotCost=0.08525, cheapOracle=0.275, expensiveOracle=0.0015; spread=0.2735 |
| `FSE1` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n64` | `supports` | 23.13 | 0.00162 | large (0.1391) | median risks: random=0.00875, balanced=0.00625, diversity=0.0075, SRSSampling=0.0085, pairwise=0.0275, pilotCost=0.00825, cheapOracle=0.275, expensiveOracle=0.0015; spread=0.2735 |
| `FSE2` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.006616) | best size-normalized=diversity_n8; best cost-normalized=balanced_n8 |
| `FSE3` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.05077) | best cost-normalized=balanced_n8; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n8; empirical front=SRSSampling_n8,balanced_n8,cheapOracle_n8,diversity_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 429.5 | 0.844 | negligible (0.4772) | A12<0.5 means SRS risks tend to be lower; median SRS=0.09975, median random=0.1103 |
| `FSE6` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 432.5 | 0.809 | negligible (0.4806) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003243, median random=0.003301 |
| `FSE2` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.02755) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16,pairwise_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 449.5 | 0.622 | negligible (0.5006) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03975, median random=0.03975 |
| `FSE6` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 437.5 | 0.753 | negligible (0.5139) | A12>0.5 means SRS costs tend to be higher; median SRS=0.006825, median random=0.006772 |
| `FSE2` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.003973) | best size-normalized=diversity_n20; best cost-normalized=balanced_n20 |
| `FSE3` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.02928) | best cost-normalized=balanced_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n20; empirical front=balanced_n20,cheapOracle_n20,diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 429.5 | 0.844 | negligible (0.5228) | A12<0.5 means SRS risks tend to be lower; median SRS=0.054, median random=0.049 |
| `FSE6` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 432.5 | 0.809 | negligible (0.4806) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009557, median random=0.009834 |
| `FSE2` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (1.284e-05) | best size-normalized=diversity_n32; best cost-normalized=pairwise_n32 |
| `FSE3` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.01095) | best cost-normalized=pairwise_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n32; empirical front=cheapOracle_n32,diversity_n32,pairwise_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 446.5 | 0.654 | negligible (0.4961) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01925, median random=0.01925 |
| `FSE6` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 345 | 0.293 | small (0.6167) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01699, median random=0.01402 |
| `FSE2` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.009788) | best size-normalized=expensiveOracle_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | moderate (0.008769) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.1667 |  | large frontier change (5) | count front=expensiveOracle_n40; empirical front=balanced_n40,cheapOracle_n40,diversity_n40,expensiveOracle_n40,pairwise_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 424 | 0.908 | negligible (0.4711) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01275, median random=0.013 |
| `FSE6` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 384 | 0.634 | small (0.5733) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0199, median random=0.01795 |
| `FSE2` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.01126) | best size-normalized=expensiveOracle_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01029) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n64; empirical front=balanced_n64,cheapOracle_n64,expensiveOracle_n64,pairwise_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 440 | 0.725 | negligible (0.5111) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0085, median random=0.00875 |
| `FSE6` | `lcbench__workload_covertype__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 437 | 0.758 | negligible (0.4856) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03246, median random=0.03212 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003301 | 0.1103 | 0.8797 | -0.02028 | -0.004033 |
| `balanced_n8` | 8 | 0.004 | 0.004209 | 0.0385 | 0.9591 | 0.0591 | 0.05509 |
| `diversity_n8` | 8 | 0.004 | 0.007854 | 0.008 | 0.992 | 0.092 | 0.04847 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003243 | 0.09975 | 0.8865 | -0.01352 | 0.004314 |
| `pairwise_n8` | 8 | 0.004 | 0.003488 | 0.1975 | 0.8025 | -0.0975 | -0.08609 |
| `pilotCost_n8` | 8 | 0.004 | 0.002209 | 0.2085 | 0.7931 | -0.1069 | -0.05108 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001593 | 0.4505 | 0.5495 | -0.3505 | -0.2576 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.08551 | 0.045 | 0.955 | 0.055 | -0.03922 |
| `random_n16` | 16 | 0.008 | 0.006772 | 0.03975 | 0.9451 | 0.0006222 | 0.009399 |
| `balanced_n16` | 16 | 0.008 | 0.00795 | 0.02925 | 0.9678 | 0.02332 | 0.02363 |
| `diversity_n16` | 16 | 0.008 | 0.01061 | 0.008 | 0.992 | 0.04756 | 0.03508 |
| `SRSSampling_n16` | 16 | 0.008 | 0.006825 | 0.03975 | 0.9436 | -0.0008111 | 0.007528 |
| `pairwise_n16` | 16 | 0.008 | 0.006301 | 0.052 | 0.948 | 0.003556 | 0.01648 |
| `pilotCost_n16` | 16 | 0.008 | 0.004186 | 0.113 | 0.8464 | -0.09803 | -0.05718 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003283 | 0.3705 | 0.6295 | -0.3149 | -0.2537 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.1291 | 0.03 | 0.97 | 0.02556 | -0.02616 |
| `random_n20` | 20 | 0.01 | 0.009834 | 0.049 | 0.9421 | -0.01241 | -0.01171 |
| `balanced_n20` | 20 | 0.01 | 0.009222 | 0.0305 | 0.9669 | 0.01239 | 0.01585 |
| `diversity_n20` | 20 | 0.01 | 0.02481 | 0.0075 | 0.9925 | 0.03795 | 0.01187 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009557 | 0.054 | 0.9392 | -0.01535 | -0.01344 |
| `pairwise_n20` | 20 | 0.01 | 0.008193 | 0.052 | 0.948 | -0.006545 | 0.002387 |
| `pilotCost_n20` | 20 | 0.01 | 0.0061 | 0.0235 | 0.9192 | -0.03533 | -0.01036 |
| `cheapOracle_n20` | 20 | 0.01 | 0.004138 | 0.277 | 0.723 | -0.2315 | -0.1797 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.1455 | 0.03 | 0.97 | 0.01545 | -0.02659 |
| `random_n32` | 32 | 0.016 | 0.01402 | 0.01925 | 0.9725 | 0.001862 | 0.005732 |
| `balanced_n32` | 32 | 0.016 | 0.01381 | 0.02775 | 0.972 | 0.001395 | 0.005735 |
| `diversity_n32` | 32 | 0.016 | 0.03117 | 0.0075 | 0.9925 | 0.02191 | 0.008041 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01699 | 0.01925 | 0.9693 | -0.001272 | -0.002895 |
| `pairwise_n32` | 32 | 0.016 | 0.01306 | 0.0275 | 0.9725 | 0.001912 | 0.008053 |
| `pilotCost_n32` | 32 | 0.016 | 0.008231 | 0.093 | 0.8978 | -0.07277 | -0.04802 |
| `cheapOracle_n32` | 32 | 0.016 | 0.006729 | 0.277 | 0.723 | -0.2476 | -0.2123 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.1833 | 0.03 | 0.97 | -0.0005882 | -0.02729 |
| `random_n40` | 40 | 0.02 | 0.01795 | 0.013 | 0.9775 | 0.001343 | 0.003918 |
| `balanced_n40` | 40 | 0.02 | 0.0167 | 0.0095 | 0.9825 | 0.006293 | 0.01074 |
| `diversity_n40` | 40 | 0.02 | 0.04441 | 0.0075 | 0.9925 | 0.01631 | 0.00351 |
| `SRSSampling_n40` | 40 | 0.02 | 0.0199 | 0.01275 | 0.978 | 0.00186 | 0.001968 |
| `pairwise_n40` | 40 | 0.02 | 0.01556 | 0.0275 | 0.9725 | -0.00369 | 0.002694 |
| `pilotCost_n40` | 40 | 0.02 | 0.0102 | 0.08525 | 0.9161 | -0.06012 | -0.03927 |
| `cheapOracle_n40` | 40 | 0.02 | 0.008476 | 0.275 | 0.725 | -0.2512 | -0.2222 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.2031 | 0.0015 | 0.9985 | 0.02231 | 0.0009498 |
| `random_n64` | 64 | 0.032 | 0.03212 | 0.00875 | 0.9868 | 0.001902 | 0.001848 |
| `balanced_n64` | 64 | 0.032 | 0.02657 | 0.00625 | 0.9936 | 0.008768 | 0.01175 |
| `diversity_n64` | 64 | 0.032 | 0.05553 | 0.0075 | 0.9925 | 0.007652 | 0.001345 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03246 | 0.0085 | 0.9865 | 0.001668 | 0.001461 |
| `pairwise_n64` | 64 | 0.032 | 0.02411 | 0.0275 | 0.9725 | -0.01235 | -0.007588 |
| `pilotCost_n64` | 64 | 0.032 | 0.01693 | 0.00825 | 0.9669 | -0.01795 | -0.005207 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01375 | 0.275 | 0.725 | -0.2598 | -0.2411 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.2495 | 0.0015 | 0.9985 | 0.01365 | 0.0004959 |
