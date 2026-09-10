# lcbench__workload_christine__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `balanced_n64` (risk 0.002, %cost 0.03261).

Best integrated confidence after normalizing the prior baseline by empirical cost: `cheapOracle_n16` (omega_cost 0.3052, %cost 0.0002734).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.9665, risk 0.0335, %cost 0.003509, omega_cost 0.07739
- `cheapOracle_n8`: posterior area 0.8305, risk 0.1695, %cost 0.0001328, omega_cost 0.2719
- `expensiveOracle_n8`: posterior area 0.994, risk 0.006, %cost 0.009686, omega_cost 0.04079
- `balanced_n16`: posterior area 0.9682, risk 0.0165, %cost 0.008221, omega_cost 0.02244
- `cheapOracle_n16`: posterior area 0.9125, risk 0.0875, %cost 0.0002734, omega_cost 0.3052
- `pilotCost_n20`: posterior area 0.9142, risk 0.0735, %cost 0.0003886, omega_cost 0.2743

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n8` | `supports` | 25.16 | 7.11e-04 | large (0.1565) | median risks: random=0.0735, balanced=0.0365, diversity=0.0335, SRSSampling=0.0735, pairwise=0.1695, pilotCost=0.1255, cheapOracle=0.1695, expensiveOracle=0.006; spread=0.1635 |
| `FSE1` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n16` | `supports` | 26.44 | 4.20e-04 | large (0.1676) | median risks: random=0.0335, balanced=0.0165, diversity=0.0335, SRSSampling=0.0335, pairwise=0.1695, pilotCost=0.0875, cheapOracle=0.0875, expensiveOracle=0.006; spread=0.1635 |
| `FSE1` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n20` | `supports` | 21.95 | 0.0026 | large (0.1288) | median risks: random=0.027, balanced=0.0255, diversity=0.0335, SRSSampling=0.027, pairwise=0.147, pilotCost=0.0735, cheapOracle=0.0875, expensiveOracle=0.006; spread=0.141 |
| `FSE1` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n32` | `supports` | 48.7 | 2.60e-08 | large (0.3595) | median risks: random=0.0095, balanced=0.0165, diversity=0.013, SRSSampling=0.0165, pairwise=0.0735, pilotCost=0.1045, cheapOracle=0.0875, expensiveOracle=0.006; spread=0.0985 |
| `FSE1` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n40` | `supports` | 58.15 | 3.52e-10 | large (0.441) | median risks: random=0.006, balanced=0.01475, diversity=0.013, SRSSampling=0.01475, pairwise=0.0735, pilotCost=0.0735, cheapOracle=0.0875, expensiveOracle=0.006; spread=0.0815 |
| `FSE1` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n64` | `supports` | 50.98 | 9.27e-09 | large (0.3791) | median risks: random=0.006, balanced=0.002, diversity=0.006, SRSSampling=0.006, pairwise=0.006, pilotCost=0.0735, cheapOracle=0.0875, expensiveOracle=0.006; spread=0.0855 |
| `FSE2` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.2311) | best size-normalized=expensiveOracle_n8; best cost-normalized=cheapOracle_n8 |
| `FSE3` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.2694) | best cost-normalized=cheapOracle_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.3333 |  | large frontier change (2) | count front=expensiveOracle_n8; empirical front=cheapOracle_n8,diversity_n8,expensiveOracle_n8 |
| `FSE5` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 441 | 0.714 | negligible (0.51) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0735, median random=0.0735 |
| `FSE6` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 432.5 | 0.809 | negligible (0.4806) | A12>0.5 means SRS costs tend to be higher; median SRS=0.004112, median random=0.00418 |
| `FSE2` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.2862) | best size-normalized=expensiveOracle_n16; best cost-normalized=cheapOracle_n16 |
| `FSE3` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.3042) | best cost-normalized=cheapOracle_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.25 |  | large frontier change (3) | count front=expensiveOracle_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16,expensiveOracle_n16 |
| `FSE5` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 439.5 | 0.731 | negligible (0.5117) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0335, median random=0.0335 |
| `FSE6` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 442.5 | 0.697 | negligible (0.5083) | A12>0.5 means SRS costs tend to be higher; median SRS=0.008331, median random=0.008331 |
| `FSE2` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.2701) | best size-normalized=expensiveOracle_n20; best cost-normalized=cheapOracle_n20 |
| `FSE3` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.2808) | best cost-normalized=cheapOracle_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n20; empirical front=balanced_n20,cheapOracle_n20,diversity_n20,expensiveOracle_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 436 | 0.77 | negligible (0.5156) | A12<0.5 means SRS risks tend to be lower; median SRS=0.027, median random=0.027 |
| `FSE6` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 440.5 | 0.719 | negligible (0.4894) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01031, median random=0.01041 |
| `FSE2` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.2256) | best size-normalized=expensiveOracle_n32; best cost-normalized=cheapOracle_n32 |
| `FSE3` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.2311) | best cost-normalized=cheapOracle_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.3333 |  | large frontier change (2) | count front=expensiveOracle_n32; empirical front=cheapOracle_n32,diversity_n32,expensiveOracle_n32 |
| `FSE5` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 381.5 | 0.602 | small (0.5761) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0165, median random=0.0095 |
| `FSE6` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 373 | 0.523 | small (0.5856) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01591, median random=0.01542 |
| `FSE2` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.2008) | best size-normalized=expensiveOracle_n40; best cost-normalized=cheapOracle_n40 |
| `FSE3` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.2026) | best cost-normalized=cheapOracle_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.3333 |  | large frontier change (2) | count front=expensiveOracle_n40; empirical front=cheapOracle_n40,diversity_n40,expensiveOracle_n40 |
| `FSE5` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 402 | 0.829 | negligible (0.5533) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01475, median random=0.006 |
| `FSE6` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 406 | 0.88 | negligible (0.4511) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01978, median random=0.0202 |
| `FSE2` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.1361) | best size-normalized=diversity_n64; best cost-normalized=cheapOracle_n64 |
| `FSE3` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.142) | best cost-normalized=cheapOracle_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n64,expensiveOracle_n64,pairwise_n64; empirical front=cheapOracle_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 419.5 | 0.964 | negligible (0.4661) | A12<0.5 means SRS risks tend to be lower; median SRS=0.006, median random=0.006 |
| `FSE6` | `lcbench__workload_christine__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 383 | 0.624 | small (0.5744) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03242, median random=0.03113 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.00418 | 0.0735 | 0.9081 | 0.008117 | 0.004634 |
| `balanced_n8` | 8 | 0.004 | 0.004488 | 0.0365 | 0.9352 | 0.0352 | 0.0263 |
| `diversity_n8` | 8 | 0.004 | 0.003509 | 0.0335 | 0.9665 | 0.0665 | 0.07739 |
| `SRSSampling_n8` | 8 | 0.004 | 0.004112 | 0.0735 | 0.9047 | 0.004683 | 0.002485 |
| `pairwise_n8` | 8 | 0.004 | 0.004857 | 0.1695 | 0.8305 | -0.0695 | -0.08413 |
| `pilotCost_n8` | 8 | 0.004 | 0.000155 | 0.1255 | 0.8232 | -0.07675 | 0.2562 |
| `cheapOracle_n8` | 8 | 0.004 | 0.0001328 | 0.1695 | 0.8305 | -0.0695 | 0.2719 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.009686 | 0.006 | 0.994 | 0.094 | 0.04079 |
| `random_n16` | 16 | 0.008 | 0.008331 | 0.0335 | 0.9483 | 0.003806 | 0.001833 |
| `balanced_n16` | 16 | 0.008 | 0.008221 | 0.0165 | 0.9682 | 0.02377 | 0.02244 |
| `diversity_n16` | 16 | 0.008 | 0.006941 | 0.0335 | 0.9665 | 0.02206 | 0.02946 |
| `SRSSampling_n16` | 16 | 0.008 | 0.008331 | 0.0335 | 0.9473 | 0.002889 | 0.0009168 |
| `pairwise_n16` | 16 | 0.008 | 0.008147 | 0.1695 | 0.8305 | -0.1139 | -0.1148 |
| `pilotCost_n16` | 16 | 0.008 | 0.000308 | 0.0875 | 0.8937 | -0.05073 | 0.276 |
| `cheapOracle_n16` | 16 | 0.008 | 0.0002734 | 0.0875 | 0.9125 | -0.03194 | 0.3052 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.01905 | 0.006 | 0.994 | 0.04956 | 0.01894 |
| `random_n20` | 20 | 0.01 | 0.01041 | 0.027 | 0.9604 | 0.005821 | 0.004191 |
| `balanced_n20` | 20 | 0.01 | 0.0104 | 0.0255 | 0.9719 | 0.01735 | 0.01576 |
| `diversity_n20` | 20 | 0.01 | 0.009292 | 0.0335 | 0.9665 | 0.01195 | 0.01508 |
| `SRSSampling_n20` | 20 | 0.01 | 0.01031 | 0.027 | 0.9595 | 0.004905 | 0.00364 |
| `pairwise_n20` | 20 | 0.01 | 0.01064 | 0.147 | 0.853 | -0.1015 | -0.104 |
| `pilotCost_n20` | 20 | 0.01 | 0.0003886 | 0.0735 | 0.9142 | -0.04038 | 0.2743 |
| `cheapOracle_n20` | 20 | 0.01 | 0.0003442 | 0.0875 | 0.9125 | -0.04205 | 0.2845 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.02361 | 0.006 | 0.994 | 0.03945 | 0.01431 |
| `random_n32` | 32 | 0.016 | 0.01542 | 0.0095 | 0.9815 | 0.01086 | 0.01191 |
| `balanced_n32` | 32 | 0.016 | 0.01607 | 0.0165 | 0.9811 | 0.01053 | 0.0104 |
| `diversity_n32` | 32 | 0.016 | 0.01479 | 0.013 | 0.987 | 0.01641 | 0.01866 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01591 | 0.0165 | 0.9725 | 0.001928 | 0.002085 |
| `pairwise_n32` | 32 | 0.016 | 0.01749 | 0.0735 | 0.9265 | -0.04409 | -0.04645 |
| `pilotCost_n32` | 32 | 0.016 | 0.0006191 | 0.1045 | 0.8888 | -0.08175 | 0.1976 |
| `cheapOracle_n32` | 32 | 0.016 | 0.000559 | 0.0875 | 0.9125 | -0.05809 | 0.2332 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.0356 | 0.006 | 0.994 | 0.02341 | 0.007662 |
| `random_n40` | 40 | 0.02 | 0.0202 | 0.006 | 0.9857 | 0.00946 | 0.009231 |
| `balanced_n40` | 40 | 0.02 | 0.02038 | 0.01475 | 0.983 | 0.006843 | 0.006416 |
| `diversity_n40` | 40 | 0.02 | 0.01955 | 0.013 | 0.987 | 0.01081 | 0.01134 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01978 | 0.01475 | 0.9793 | 0.003143 | 0.003399 |
| `pairwise_n40` | 40 | 0.02 | 0.02101 | 0.0735 | 0.9265 | -0.04969 | -0.05078 |
| `pilotCost_n40` | 40 | 0.02 | 0.0007701 | 0.0735 | 0.9108 | -0.06542 | 0.1932 |
| `cheapOracle_n40` | 40 | 0.02 | 0.0007035 | 0.0875 | 0.9125 | -0.06369 | 0.206 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.04348 | 0.006 | 0.994 | 0.01781 | 0.005242 |
| `random_n64` | 64 | 0.032 | 0.03113 | 0.006 | 0.9861 | 0.001218 | 0.001626 |
| `balanced_n64` | 64 | 0.032 | 0.03261 | 0.002 | 0.99 | 0.005168 | 0.004892 |
| `diversity_n64` | 64 | 0.032 | 0.03107 | 0.006 | 0.994 | 0.009152 | 0.009593 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03242 | 0.006 | 0.9887 | 0.003885 | 0.003694 |
| `pairwise_n64` | 64 | 0.032 | 0.03192 | 0.006 | 0.994 | 0.009152 | 0.00919 |
| `pilotCost_n64` | 64 | 0.032 | 0.003524 | 0.0735 | 0.9378 | -0.04708 | 0.04828 |
| `cheapOracle_n64` | 64 | 0.032 | 0.001144 | 0.0875 | 0.9125 | -0.07235 | 0.1457 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.06674 | 0.006 | 0.994 | 0.009152 | 0.001381 |
