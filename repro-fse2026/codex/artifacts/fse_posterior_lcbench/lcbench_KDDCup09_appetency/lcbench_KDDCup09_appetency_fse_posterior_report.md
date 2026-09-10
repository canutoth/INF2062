# lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `random_n8` (risk 0, %cost 0.003703).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pairwise_n8` (omega_cost 0.1089, %cost 0.003592).

Empirical cost/confidence Pareto front:

- `pairwise_n8`: posterior area 1, risk 0, %cost 0.003592, omega_cost 0.1089
- `pilotCost_n8`: posterior area 0.6134, risk 0.374, %cost 0.001992, omega_cost -0.2195
- `cheapOracle_n8`: posterior area 0.2175, risk 0.7825, %cost 0.001704, omega_cost -0.5976

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n8` | `supports` | 86.1 | 7.79e-16 | large (0.6819) | median risks: random=0, balanced=0, diversity=0, SRSSampling=0, pairwise=0, pilotCost=0.374, cheapOracle=0.7825, expensiveOracle=0; spread=0.7825 |
| `FSE1` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n16` | `supports` | 96.24 | 6.44e-18 | large (0.7693) | median risks: random=0, balanced=0, diversity=0, SRSSampling=0, pairwise=0, pilotCost=0.309, cheapOracle=0.7825, expensiveOracle=0; spread=0.7825 |
| `FSE1` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n20` | `supports` | 81.02 | 8.55e-15 | large (0.6381) | median risks: random=0, balanced=0, diversity=0, SRSSampling=0, pairwise=0, pilotCost=0.299, cheapOracle=0.7825, expensiveOracle=0; spread=0.7825 |
| `FSE1` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n32` | `supports` | 107.7 | 2.80e-20 | large (0.8678) | median risks: random=0, balanced=0, diversity=0, SRSSampling=0, pairwise=0, pilotCost=0.2865, cheapOracle=0.7825, expensiveOracle=0; spread=0.7825 |
| `FSE1` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n40` | `supports` | 101.4 | 5.59e-19 | large (0.8136) | median risks: random=0, balanced=0, diversity=0, SRSSampling=0, pairwise=0, pilotCost=0.2865, cheapOracle=0.7825, expensiveOracle=0; spread=0.7825 |
| `FSE1` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n64` | `supports` | 80.06 | 1.34e-14 | large (0.6298) | median risks: random=0, balanced=0, diversity=0, SRSSampling=0, pairwise=0, pilotCost=0.173, cheapOracle=0.7095, expensiveOracle=0; spread=0.7095 |
| `FSE2` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.006646) | best size-normalized=balanced_n8; best cost-normalized=pairwise_n8 |
| `FSE3` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.04069) | best cost-normalized=pairwise_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.1667 |  | large frontier change (5) | count front=balanced_n8,diversity_n8,expensiveOracle_n8,pairwise_n8; empirical front=cheapOracle_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 434 | 0.905 | negligible (0.5178) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 436.5 | 0.764 | negligible (0.485) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003593, median random=0.003703 |
| `FSE2` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.0004882) | best size-normalized=balanced_n16; best cost-normalized=pairwise_n16 |
| `FSE3` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.01529) | best cost-normalized=pairwise_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.1429 |  | large frontier change (6) | count front=balanced_n16,diversity_n16,expensiveOracle_n16,pairwise_n16; empirical front=cheapOracle_n16,pairwise_n16,pilotCost_n16,random_n16 |
| `FSE5` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 450 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 428.5 | 0.856 | negligible (0.5239) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007337, median random=0.007275 |
| `FSE2` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=balanced_n20; best cost-normalized=balanced_n20 |
| `FSE3` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.01498) | best cost-normalized=balanced_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.1667 |  | large frontier change (5) | count front=balanced_n20,diversity_n20,expensiveOracle_n20,pairwise_n20; empirical front=balanced_n20,cheapOracle_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 450 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 432.5 | 0.809 | negligible (0.4806) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009327, median random=0.009407 |
| `FSE2` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=balanced_n32; best cost-normalized=balanced_n32 |
| `FSE3` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | moderate (0.005131) | best cost-normalized=balanced_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.1429 |  | large frontier change (6) | count front=SRSSampling_n32,balanced_n32,diversity_n32,expensiveOracle_n32,pairwise_n32; empirical front=balanced_n32,cheapOracle_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 435 | 0.617 | negligible (0.4833) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n32` | `supports` | 219 | 0.00355 | large (0.7567) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0169, median random=0.01446 |
| `FSE2` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.003074) | best size-normalized=random_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | moderate (0.006792) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.125 |  | large frontier change (7) | count front=SRSSampling_n40,balanced_n40,diversity_n40,expensiveOracle_n40,pairwise_n40,random_n40; empirical front=balanced_n40,cheapOracle_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 450 |  | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n40` | `supports` | 209 | 0.00219 | large (0.7678) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02294, median random=0.01932 |
| `FSE2` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.002997) | best size-normalized=random_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | moderate (0.006184) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.125 |  | large frontier change (7) | count front=SRSSampling_n64,balanced_n64,diversity_n64,expensiveOracle_n64,pairwise_n64,random_n64; empirical front=balanced_n64,cheapOracle_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 450 |  | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `lcbench__workload_KDDCup09_appetency__cost_time_total__target_final_val_accuracy:n64` | `supports` | 163 | 1.82e-04 | large (0.8189) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03987, median random=0.03142 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003703 | 0 | 0.9662 | 0.06623 | 0.07256 |
| `balanced_n8` | 8 | 0.004 | 0.00389 | 0 | 1 | 0.1 | 0.1022 |
| `diversity_n8` | 8 | 0.004 | 0.005375 | 0 | 1 | 0.1 | 0.07843 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003593 | 0 | 0.9594 | 0.05935 | 0.0682 |
| `pairwise_n8` | 8 | 0.004 | 0.003592 | 0 | 1 | 0.1 | 0.1089 |
| `pilotCost_n8` | 8 | 0.004 | 0.001992 | 0.374 | 0.6134 | -0.2866 | -0.2195 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001704 | 0.7825 | 0.2175 | -0.6825 | -0.5976 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.05849 | 0 | 1 | 0.1 | 0.008405 |
| `random_n16` | 16 | 0.008 | 0.007275 | 0 | 0.985 | 0.04052 | 0.04539 |
| `balanced_n16` | 16 | 0.008 | 0.00737 | 0 | 1 | 0.05556 | 0.05974 |
| `diversity_n16` | 16 | 0.008 | 0.008536 | 0 | 1 | 0.05556 | 0.05243 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007337 | 0 | 0.985 | 0.04052 | 0.04494 |
| `pairwise_n16` | 16 | 0.008 | 0.007302 | 0 | 1 | 0.05556 | 0.06023 |
| `pilotCost_n16` | 16 | 0.008 | 0.00404 | 0.309 | 0.6884 | -0.2561 | -0.2124 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003467 | 0.7825 | 0.2175 | -0.7269 | -0.6706 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.08462 | 0 | 1 | 0.05556 | 0.00584 |
| `random_n20` | 20 | 0.01 | 0.009407 | 0 | 0.9886 | 0.03409 | 0.03668 |
| `balanced_n20` | 20 | 0.01 | 0.00861 | 0 | 1 | 0.04545 | 0.05203 |
| `diversity_n20` | 20 | 0.01 | 0.01198 | 0 | 1 | 0.04545 | 0.03852 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009327 | 0 | 0.9886 | 0.03409 | 0.03705 |
| `pairwise_n20` | 20 | 0.01 | 0.009495 | 0 | 1 | 0.04545 | 0.04764 |
| `pilotCost_n20` | 20 | 0.01 | 0.005105 | 0.299 | 0.7382 | -0.2163 | -0.1798 |
| `cheapOracle_n20` | 20 | 0.01 | 0.004355 | 0.7825 | 0.2175 | -0.737 | -0.6891 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.09371 | 0 | 1 | 0.04545 | 0.005279 |
| `random_n32` | 32 | 0.016 | 0.01446 | 0 | 0.9948 | 0.02416 | 0.02708 |
| `balanced_n32` | 32 | 0.016 | 0.01412 | 0 | 1 | 0.02941 | 0.03307 |
| `diversity_n32` | 32 | 0.016 | 0.01794 | 0 | 1 | 0.02941 | 0.0264 |
| `SRSSampling_n32` | 32 | 0.016 | 0.0169 | 0 | 1 | 0.02941 | 0.02794 |
| `pairwise_n32` | 32 | 0.016 | 0.01554 | 0 | 1 | 0.02941 | 0.03023 |
| `pilotCost_n32` | 32 | 0.016 | 0.007984 | 0.2865 | 0.7204 | -0.2502 | -0.224 |
| `cheapOracle_n32` | 32 | 0.016 | 0.007041 | 0.7825 | 0.2175 | -0.7531 | -0.7203 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.1171 | 0 | 1 | 0.02941 | 0.004235 |
| `random_n40` | 40 | 0.02 | 0.01932 | 0 | 1 | 0.02381 | 0.02461 |
| `balanced_n40` | 40 | 0.02 | 0.01706 | 0 | 1 | 0.02381 | 0.02768 |
| `diversity_n40` | 40 | 0.02 | 0.02515 | 0 | 1 | 0.02381 | 0.01912 |
| `SRSSampling_n40` | 40 | 0.02 | 0.02294 | 0 | 1 | 0.02381 | 0.02089 |
| `pairwise_n40` | 40 | 0.02 | 0.01873 | 0 | 1 | 0.02381 | 0.02534 |
| `pilotCost_n40` | 40 | 0.02 | 0.01011 | 0.2865 | 0.7565 | -0.2197 | -0.1985 |
| `cheapOracle_n40` | 40 | 0.02 | 0.008856 | 0.7825 | 0.2175 | -0.7587 | -0.7318 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.1314 | 0 | 1 | 0.02381 | 0.003778 |
| `random_n64` | 64 | 0.032 | 0.03142 | 0 | 1 | 0.01515 | 0.01542 |
| `balanced_n64` | 64 | 0.032 | 0.02615 | 0 | 1 | 0.01515 | 0.01842 |
| `diversity_n64` | 64 | 0.032 | 0.03803 | 0 | 1 | 0.01515 | 0.01281 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03987 | 0 | 1 | 0.01515 | 0.01223 |
| `pairwise_n64` | 64 | 0.032 | 0.02917 | 0 | 1 | 0.01515 | 0.01657 |
| `pilotCost_n64` | 64 | 0.032 | 0.01718 | 0.173 | 0.8338 | -0.151 | -0.1387 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01436 | 0.7095 | 0.2905 | -0.6943 | -0.6769 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.1689 | 0 | 1 | 0.01515 | 0.002942 |
