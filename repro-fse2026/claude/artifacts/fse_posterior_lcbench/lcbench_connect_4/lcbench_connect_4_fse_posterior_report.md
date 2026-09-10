# lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n20` (risk 0, %cost 0.01513).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pairwise_n8` (omega_cost 0.08486, %cost 0.003933).

Empirical cost/confidence Pareto front:

- `random_n8`: posterior area 0.95, risk 0.0165, %cost 0.003638, omega_cost 0.0578
- `balanced_n8`: posterior area 0.9842, risk 0.0165, %cost 0.004177, omega_cost 0.08076
- `diversity_n8`: posterior area 0.9915, risk 0.0085, %cost 0.004671, omega_cost 0.07967
- `SRSSampling_n8`: posterior area 0.9414, risk 0.0165, %cost 0.003547, omega_cost 0.05131
- `pairwise_n8`: posterior area 0.9835, risk 0.0165, %cost 0.003933, omega_cost 0.08486
- `pilotCost_n8`: posterior area 0.6503, risk 0.4475, %cost 0.002231, omega_cost -0.195
- `cheapOracle_n8`: posterior area 0.2625, risk 0.7375, %cost 0.001789, omega_cost -0.5582
- `diversity_n16`: posterior area 0.996, risk 0.004, %cost 0.007931, omega_cost 0.05199
- `diversity_n20`: posterior area 1, risk 0, %cost 0.01513, omega_cost 0.031

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n8` | `supports` | 31.8 | 4.43e-05 | large (0.2138) | median risks: random=0.0165, balanced=0.0165, diversity=0.0085, SRSSampling=0.0165, pairwise=0.0165, pilotCost=0.4475, cheapOracle=0.7375, expensiveOracle=0.0165; spread=0.729 |
| `FSE1` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n16` | `inconclusive` | 14 | 0.0513 | large (0.06031) | median risks: random=0.0165, balanced=0.0165, diversity=0.004, SRSSampling=0.0165, pairwise=0.0165, pilotCost=0.4515, cheapOracle=0.4325, expensiveOracle=0.0165; spread=0.4475 |
| `FSE1` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n20` | `inconclusive` | 10.14 | 0.181 | large (0.02704) | median risks: random=0.0165, balanced=0.0165, diversity=0, SRSSampling=0.0165, pairwise=0.0165, pilotCost=0.00975, cheapOracle=0.4325, expensiveOracle=0.003; spread=0.4325 |
| `FSE1` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n32` | `supports` | 18.01 | 0.0119 | large (0.09491) | median risks: random=0.0165, balanced=0.0165, diversity=0, SRSSampling=0.0165, pairwise=0.0165, pilotCost=0.1303, cheapOracle=0.374, expensiveOracle=0.003; spread=0.374 |
| `FSE1` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n40` | `supports` | 29.85 | 1.01e-04 | large (0.197) | median risks: random=0.0135, balanced=0.0165, diversity=0, SRSSampling=0.0165, pairwise=0.0165, pilotCost=0.278, cheapOracle=0.374, expensiveOracle=0.003; spread=0.374 |
| `FSE1` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n64` | `supports` | 15.69 | 0.0281 | large (0.07494) | median risks: random=0.0105, balanced=0.00625, diversity=0, SRSSampling=0.008, pairwise=0.0165, pilotCost=0.0085, cheapOracle=0.374, expensiveOracle=0.003; spread=0.374 |
| `FSE2` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.005183) | best size-normalized=diversity_n8; best cost-normalized=pairwise_n8 |
| `FSE3` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.03355) | best cost-normalized=pairwise_n8; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.1429 |  | large frontier change (6) | count front=diversity_n8; empirical front=SRSSampling_n8,balanced_n8,cheapOracle_n8,diversity_n8,pairwise_n8,pilotCost_n8,random_n8 |
| `FSE5` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 435 | 0.886 | negligible (0.5167) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0165, median random=0.0165 |
| `FSE6` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 438.5 | 0.741 | negligible (0.4872) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003547, median random=0.003638 |
| `FSE2` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | moderate (0.007345) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16,pilotCost_n16,random_n16 |
| `FSE5` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 450 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0165, median random=0.0165 |
| `FSE6` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 425.5 | 0.891 | negligible (0.5272) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007304, median random=0.007144 |
| `FSE2` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.006294) | best size-normalized=diversity_n20; best cost-normalized=balanced_n20 |
| `FSE3` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | moderate (0.002945) | best cost-normalized=balanced_n20; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n20; empirical front=SRSSampling_n20,balanced_n20,cheapOracle_n20,diversity_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 450 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0165, median random=0.0165 |
| `FSE6` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 435.5 | 0.775 | negligible (0.4839) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009367, median random=0.00939 |
| `FSE2` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | moderate (0.008264) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.1667 |  | large frontier change (5) | count front=diversity_n32; empirical front=SRSSampling_n32,balanced_n32,cheapOracle_n32,diversity_n32,pilotCost_n32,random_n32 |
| `FSE5` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 449.5 | 0.623 | negligible (0.5006) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0165, median random=0.0165 |
| `FSE6` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n32` | `supports` | 281 | 0.0457 | medium (0.6878) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01728, median random=0.01442 |
| `FSE2` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.001576) | best size-normalized=diversity_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | moderate (0.006508) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n40; empirical front=balanced_n40,cheapOracle_n40,diversity_n40,pilotCost_n40,random_n40 |
| `FSE5` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 411.5 | 0.91 | negligible (0.5428) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0165, median random=0.0135 |
| `FSE6` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 295 | 0.0732 | medium (0.6722) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02184, median random=0.01965 |
| `FSE2` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.0015) | best size-normalized=diversity_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | moderate (0.007929) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n64; empirical front=balanced_n64,cheapOracle_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 408.5 | 0.905 | negligible (0.4539) | A12<0.5 means SRS risks tend to be lower; median SRS=0.008, median random=0.0105 |
| `FSE6` | `lcbench__workload_connect_4__cost_time_total__target_final_val_accuracy:n64` | `supports` | 278 | 0.0411 | medium (0.6911) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03737, median random=0.03329 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003638 | 0.0165 | 0.95 | 0.04998 | 0.0578 |
| `balanced_n8` | 8 | 0.004 | 0.004177 | 0.0165 | 0.9842 | 0.08418 | 0.08076 |
| `diversity_n8` | 8 | 0.004 | 0.004671 | 0.0085 | 0.9915 | 0.0915 | 0.07967 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003547 | 0.0165 | 0.9414 | 0.04135 | 0.05131 |
| `pairwise_n8` | 8 | 0.004 | 0.003933 | 0.0165 | 0.9835 | 0.0835 | 0.08486 |
| `pilotCost_n8` | 8 | 0.004 | 0.002231 | 0.4475 | 0.6503 | -0.2497 | -0.195 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001789 | 0.7375 | 0.2625 | -0.6375 | -0.5582 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.04728 | 0.0165 | 0.9835 | 0.0835 | -0.006145 |
| `random_n16` | 16 | 0.008 | 0.007144 | 0.0165 | 0.9844 | 0.03999 | 0.04583 |
| `balanced_n16` | 16 | 0.008 | 0.007163 | 0.0165 | 0.9845 | 0.04004 | 0.04573 |
| `diversity_n16` | 16 | 0.008 | 0.007931 | 0.004 | 0.996 | 0.05156 | 0.05199 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007304 | 0.0165 | 0.9844 | 0.03999 | 0.04464 |
| `pairwise_n16` | 16 | 0.008 | 0.007575 | 0.0165 | 0.9835 | 0.03906 | 0.04181 |
| `pilotCost_n16` | 16 | 0.008 | 0.004565 | 0.4515 | 0.6883 | -0.2562 | -0.2219 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003656 | 0.4325 | 0.5675 | -0.3769 | -0.3251 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.08261 | 0.0165 | 0.9835 | 0.03906 | -0.01052 |
| `random_n20` | 20 | 0.01 | 0.00939 | 0.0165 | 0.9861 | 0.03157 | 0.03424 |
| `balanced_n20` | 20 | 0.01 | 0.008607 | 0.0165 | 0.9852 | 0.0307 | 0.03729 |
| `diversity_n20` | 20 | 0.01 | 0.01513 | 0 | 1 | 0.04545 | 0.031 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009367 | 0.0165 | 0.9861 | 0.03157 | 0.03435 |
| `pairwise_n20` | 20 | 0.01 | 0.009269 | 0.0165 | 0.9835 | 0.02895 | 0.03219 |
| `pilotCost_n20` | 20 | 0.01 | 0.006176 | 0.00975 | 0.8272 | -0.1273 | -0.1031 |
| `cheapOracle_n20` | 20 | 0.01 | 0.004612 | 0.4325 | 0.5675 | -0.387 | -0.3434 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.09571 | 0.003 | 0.997 | 0.04245 | 0.00217 |
| `random_n32` | 32 | 0.016 | 0.01442 | 0.0165 | 0.9859 | 0.01533 | 0.01835 |
| `balanced_n32` | 32 | 0.016 | 0.01339 | 0.0165 | 0.985 | 0.01438 | 0.01971 |
| `diversity_n32` | 32 | 0.016 | 0.02111 | 0 | 1 | 0.02941 | 0.02261 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01728 | 0.0165 | 0.987 | 0.01641 | 0.01435 |
| `pairwise_n32` | 32 | 0.016 | 0.01521 | 0.0165 | 0.9835 | 0.01291 | 0.01435 |
| `pilotCost_n32` | 32 | 0.016 | 0.009035 | 0.1303 | 0.7861 | -0.1845 | -0.1641 |
| `cheapOracle_n32` | 32 | 0.016 | 0.007495 | 0.374 | 0.626 | -0.3446 | -0.3151 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.1247 | 0.003 | 0.997 | 0.02641 | 0.0009784 |
| `random_n40` | 40 | 0.02 | 0.01965 | 0.0135 | 0.989 | 0.01278 | 0.01318 |
| `balanced_n40` | 40 | 0.02 | 0.01601 | 0.0165 | 0.987 | 0.01086 | 0.01645 |
| `diversity_n40` | 40 | 0.02 | 0.03263 | 0 | 1 | 0.02381 | 0.01487 |
| `SRSSampling_n40` | 40 | 0.02 | 0.02184 | 0.0165 | 0.988 | 0.01186 | 0.009937 |
| `pairwise_n40` | 40 | 0.02 | 0.01832 | 0.0165 | 0.9835 | 0.00731 | 0.009374 |
| `pilotCost_n40` | 40 | 0.02 | 0.01121 | 0.278 | 0.7579 | -0.2183 | -0.2011 |
| `cheapOracle_n40` | 40 | 0.02 | 0.009434 | 0.374 | 0.626 | -0.3502 | -0.3261 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.1402 | 0.003 | 0.997 | 0.02081 | 0.0005401 |
| `random_n64` | 64 | 0.032 | 0.03329 | 0.0105 | 0.9904 | 0.005585 | 0.005014 |
| `balanced_n64` | 64 | 0.032 | 0.02516 | 0.00625 | 0.9934 | 0.008535 | 0.01249 |
| `diversity_n64` | 64 | 0.032 | 0.04448 | 0 | 1 | 0.01515 | 0.01099 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03737 | 0.008 | 0.9915 | 0.006685 | 0.004566 |
| `pairwise_n64` | 64 | 0.032 | 0.02849 | 0.0165 | 0.9835 | -0.001348 | 0.0004563 |
| `pilotCost_n64` | 64 | 0.032 | 0.01842 | 0.0085 | 0.9241 | -0.06072 | -0.05012 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01531 | 0.374 | 0.626 | -0.3588 | -0.3433 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.181 | 0.003 | 0.997 | 0.01215 | -0.000253 |
