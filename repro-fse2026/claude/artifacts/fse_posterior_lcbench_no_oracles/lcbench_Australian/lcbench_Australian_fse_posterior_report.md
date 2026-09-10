# lcbench__workload_Australian__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `balanced_n16` (risk 0.001, %cost 0.005228).

Best integrated confidence after normalizing the prior baseline by empirical cost: `balanced_n8` (omega_cost 0.08254, %cost 0.002671).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9463, risk 0.035, %cost 0.002671, omega_cost 0.08254
- `pairwise_n8`: posterior area 0.965, risk 0.035, %cost 0.003314, omega_cost 0.08091
- `pilotCost_n8`: posterior area 0.884, risk 0.1085, %cost 0.00234, omega_cost 0.0337
- `balanced_n16`: posterior area 0.9736, risk 0.001, %cost 0.005228, omega_cost 0.05383
- `diversity_n16`: posterior area 0.999, risk 0.001, %cost 0.007771, omega_cost 0.056
- `balanced_n20`: posterior area 0.9771, risk 0.018, %cost 0.006391, omega_cost 0.04475

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n8` | `inconclusive` | 8.436 | 0.134 | large (0.02962) | median risks: random=0.035, balanced=0.035, diversity=0.035, SRSSampling=0.035, pairwise=0.035, pilotCost=0.1085; spread=0.0735 |
| `FSE1` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n16` | `inconclusive` | 10.33 | 0.0664 | moderate (0.04594) | median risks: random=0.035, balanced=0.001, diversity=0.001, SRSSampling=0.035, pairwise=0.035, pilotCost=0.035; spread=0.034 |
| `FSE1` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 5.501 | 0.358 | moderate (0.004322) | median risks: random=0.001, balanced=0.018, diversity=0.001, SRSSampling=0.001, pairwise=0.001, pilotCost=0.035; spread=0.034 |
| `FSE1` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n32` | `supports` | 14.47 | 0.0129 | moderate (0.08162) | median risks: random=0.001, balanced=0.001, diversity=0.001, SRSSampling=0.001, pairwise=0.001, pilotCost=0.035; spread=0.034 |
| `FSE1` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n40` | `supports` | 20.48 | 0.00101 | moderate (0.1335) | median risks: random=0.001, balanced=0.001, diversity=0.001, SRSSampling=0.001, pairwise=0.001, pilotCost=0.035; spread=0.034 |
| `FSE1` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n64` | `supports` | 11.65 | 0.0399 | negligible (0.05733) | median risks: random=0.001, balanced=0.001, diversity=0.001, SRSSampling=0.001, pairwise=0.001, pilotCost=0.001; spread=0 |
| `FSE2` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.0327) | best size-normalized=diversity_n8; best cost-normalized=balanced_n8 |
| `FSE3` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.0648) | best cost-normalized=balanced_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n8,pairwise_n8; empirical front=balanced_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 450 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.035, median random=0.035 |
| `FSE6` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 441.5 | 0.708 | negligible (0.4906) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003682, median random=0.003819 |
| `FSE2` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.03828) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n16; empirical front=balanced_n16,diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 437.5 | 0.766 | negligible (0.4861) | A12<0.5 means SRS risks tend to be lower; median SRS=0.035, median random=0.035 |
| `FSE6` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 436.5 | 0.764 | negligible (0.515) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007792, median random=0.007684 |
| `FSE2` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.01328) | best size-normalized=diversity_n20; best cost-normalized=pairwise_n20 |
| `FSE3` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.03112) | best cost-normalized=pairwise_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n20,pairwise_n20; empirical front=balanced_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 450 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001, median random=0.001 |
| `FSE6` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 448.5 | 0.633 | negligible (0.4983) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009722, median random=0.009722 |
| `FSE2` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.009902) | best size-normalized=diversity_n32; best cost-normalized=balanced_n32 |
| `FSE3` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.01627) | best cost-normalized=balanced_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n32,pairwise_n32; empirical front=balanced_n32,pairwise_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 435 | 0.807 | negligible (0.5167) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001, median random=0.001 |
| `FSE6` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 379 | 0.583 | small (0.5789) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01633, median random=0.01516 |
| `FSE2` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.01203) | best size-normalized=diversity_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.01057) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n40,pairwise_n40; empirical front=balanced_n40,pairwise_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 395 | 0.546 | small (0.5611) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001, median random=0.001 |
| `FSE6` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 366 | 0.458 | small (0.4067) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01844, median random=0.02002 |
| `FSE2` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.004484) | best size-normalized=diversity_n64; best cost-normalized=pairwise_n64 |
| `FSE3` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | moderate (0.002612) | best cost-normalized=pairwise_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n64,pairwise_n64; empirical front=balanced_n64,pairwise_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 450 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001, median random=0.001 |
| `FSE6` | `lcbench__workload_Australian__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 366 | 0.458 | small (0.4067) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03092, median random=0.03225 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003819 | 0.035 | 0.9109 | 0.01093 | 0.01469 |
| `balanced_n8` | 8 | 0.004 | 0.002671 | 0.035 | 0.9463 | 0.04632 | 0.08254 |
| `diversity_n8` | 8 | 0.004 | 0.004894 | 0.035 | 0.965 | 0.065 | 0.04983 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003682 | 0.035 | 0.9109 | 0.01093 | 0.01774 |
| `pairwise_n8` | 8 | 0.004 | 0.003314 | 0.035 | 0.965 | 0.065 | 0.08091 |
| `pilotCost_n8` | 8 | 0.004 | 0.00234 | 0.1085 | 0.884 | -0.01602 | 0.0337 |
| `random_n16` | 16 | 0.008 | 0.007684 | 0.035 | 0.9563 | 0.01186 | 0.01387 |
| `balanced_n16` | 16 | 0.008 | 0.005228 | 0.001 | 0.9736 | 0.02911 | 0.05383 |
| `diversity_n16` | 16 | 0.008 | 0.007771 | 0.001 | 0.999 | 0.05456 | 0.056 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007792 | 0.035 | 0.9608 | 0.01641 | 0.01772 |
| `pairwise_n16` | 16 | 0.008 | 0.007416 | 0.035 | 0.965 | 0.02056 | 0.02441 |
| `pilotCost_n16` | 16 | 0.008 | 0.00476 | 0.035 | 0.962 | 0.01756 | 0.0488 |
| `random_n20` | 20 | 0.01 | 0.009722 | 0.001 | 0.9713 | 0.01672 | 0.0179 |
| `balanced_n20` | 20 | 0.01 | 0.006391 | 0.018 | 0.9771 | 0.02255 | 0.04475 |
| `diversity_n20` | 20 | 0.01 | 0.01261 | 0.001 | 0.999 | 0.04445 | 0.03574 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009722 | 0.001 | 0.9713 | 0.01672 | 0.0179 |
| `pairwise_n20` | 20 | 0.01 | 0.008996 | 0.001 | 0.999 | 0.04445 | 0.04902 |
| `pilotCost_n20` | 20 | 0.01 | 0.005901 | 0.035 | 0.9654 | 0.01085 | 0.03785 |
| `random_n32` | 32 | 0.016 | 0.01516 | 0.001 | 0.9853 | 0.01473 | 0.01625 |
| `balanced_n32` | 32 | 0.016 | 0.01031 | 0.001 | 0.9886 | 0.01803 | 0.03282 |
| `diversity_n32` | 32 | 0.016 | 0.01991 | 0.001 | 0.999 | 0.02841 | 0.02292 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01633 | 0.001 | 0.9877 | 0.01711 | 0.01655 |
| `pairwise_n32` | 32 | 0.016 | 0.0151 | 0.001 | 0.999 | 0.02841 | 0.03005 |
| `pilotCost_n32` | 32 | 0.016 | 0.00951 | 0.035 | 0.9693 | -0.001255 | 0.0169 |
| `random_n40` | 40 | 0.02 | 0.02002 | 0.001 | 0.9945 | 0.01834 | 0.01832 |
| `balanced_n40` | 40 | 0.02 | 0.01321 | 0.001 | 0.9922 | 0.01601 | 0.02739 |
| `diversity_n40` | 40 | 0.02 | 0.02955 | 0.001 | 0.999 | 0.02281 | 0.01537 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01844 | 0.001 | 0.9911 | 0.01491 | 0.01682 |
| `pairwise_n40` | 40 | 0.02 | 0.01849 | 0.001 | 0.999 | 0.02281 | 0.02465 |
| `pilotCost_n40` | 40 | 0.02 | 0.01187 | 0.035 | 0.9786 | 0.00241 | 0.01744 |
| `random_n64` | 64 | 0.032 | 0.03225 | 0.001 | 0.9968 | 0.01198 | 0.01187 |
| `balanced_n64` | 64 | 0.032 | 0.02223 | 0.001 | 0.9934 | 0.008518 | 0.01489 |
| `diversity_n64` | 64 | 0.032 | 0.04201 | 0.001 | 0.999 | 0.01415 | 0.01062 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03092 | 0.001 | 0.9968 | 0.01198 | 0.0125 |
| `pairwise_n64` | 64 | 0.032 | 0.03004 | 0.001 | 0.999 | 0.01415 | 0.01511 |
| `pilotCost_n64` | 64 | 0.032 | 0.01908 | 0.001 | 0.9888 | 0.003952 | 0.01371 |
