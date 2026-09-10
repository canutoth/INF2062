# lcbench__workload_albert__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n8` (risk 0.0005, %cost 0.00397).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n8` (omega_cost 0.1001, %cost 0.00397).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.9995, risk 0.0005, %cost 0.00397, omega_cost 0.1001
- `SRSSampling_n8`: posterior area 0.8661, risk 0.08, %cost 0.003235, omega_cost -0.01588
- `pilotCost_n8`: posterior area 0.8527, risk 0.161, %cost 0.001812, omega_cost 0.03054
- `cheapOracle_n8`: posterior area 0.806, risk 0.194, %cost 0.001318, omega_cost 0.02169
- `pilotCost_n16`: posterior area 0.881, risk 0.1575, %cost 0.00355, omega_cost -0.00915

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n8` | `inconclusive` | 8.179 | 0.317 | large (0.01017) | median risks: random=0.1, balanced=0.08, diversity=0.0005, SRSSampling=0.08, pairwise=0.052, pilotCost=0.161, cheapOracle=0.194, expensiveOracle=0.0875; spread=0.1935 |
| `FSE1` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n16` | `supports` | 17.51 | 0.0144 | large (0.09064) | median risks: random=0.033, balanced=0.05175, diversity=0.0005, SRSSampling=0.033, pairwise=0.052, pilotCost=0.1575, cheapOracle=0.194, expensiveOracle=0.0875; spread=0.1935 |
| `FSE1` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n20` | `inconclusive` | 10.21 | 0.177 | large (0.02765) | median risks: random=0.04625, balanced=0.0355, diversity=0.0005, SRSSampling=0.04625, pairwise=0.052, pilotCost=0.0215, cheapOracle=0.194, expensiveOracle=0.0865; spread=0.1935 |
| `FSE1` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n32` | `supports` | 19.79 | 0.00604 | large (0.1103) | median risks: random=0.023, balanced=0.024, diversity=0.0005, SRSSampling=0.02625, pairwise=0.052, pilotCost=0.1008, cheapOracle=0.123, expensiveOracle=0.0865; spread=0.1225 |
| `FSE1` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 8.423 | 0.297 | large (0.01226) | median risks: random=0.014, balanced=0.01, diversity=0.0005, SRSSampling=0.0245, pairwise=0.0165, pilotCost=0.0215, cheapOracle=0.123, expensiveOracle=0.0865; spread=0.1225 |
| `FSE1` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n64` | `supports` | 21.91 | 0.00263 | large (0.1286) | median risks: random=0.00925, balanced=0.0035, diversity=0.0005, SRSSampling=0.009, pairwise=0.0145, pilotCost=0.0005, cheapOracle=0.077, expensiveOracle=0.008; spread=0.0765 |
| `FSE2` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n8; best cost-normalized=diversity_n8 |
| `FSE3` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.116) | best cost-normalized=diversity_n8; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n8; empirical front=SRSSampling_n8,cheapOracle_n8,diversity_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 429.5 | 0.844 | negligible (0.4772) | A12<0.5 means SRS risks tend to be lower; median SRS=0.08, median random=0.1 |
| `FSE6` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 435 | 0.781 | negligible (0.4833) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003235, median random=0.003498 |
| `FSE2` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.04954) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n16; empirical front=cheapOracle_n16,diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 443.5 | 0.686 | negligible (0.4928) | A12<0.5 means SRS risks tend to be lower; median SRS=0.033, median random=0.033 |
| `FSE6` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 432.5 | 0.809 | negligible (0.5194) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007, median random=0.00674 |
| `FSE2` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n20; best cost-normalized=diversity_n20 |
| `FSE3` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.03922) | best cost-normalized=diversity_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n20; empirical front=balanced_n20,cheapOracle_n20,diversity_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 447.5 | 0.643 | negligible (0.5028) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04625, median random=0.04625 |
| `FSE6` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 443.5 | 0.686 | negligible (0.4928) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009403, median random=0.00955 |
| `FSE2` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.0211) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n32; empirical front=balanced_n32,cheapOracle_n32,diversity_n32,pilotCost_n32,random_n32 |
| `FSE5` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 419 | 0.967 | negligible (0.5344) | A12<0.5 means SRS risks tend to be lower; median SRS=0.02625, median random=0.023 |
| `FSE6` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 408 | 0.904 | negligible (0.5467) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01549, median random=0.01468 |
| `FSE2` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n40; best cost-normalized=diversity_n40 |
| `FSE3` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.01354) | best cost-normalized=diversity_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n40; empirical front=balanced_n40,cheapOracle_n40,diversity_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 388 | 0.677 | small (0.5689) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0245, median random=0.014 |
| `FSE6` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 429 | 0.85 | negligible (0.4767) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01872, median random=0.01949 |
| `FSE2` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.003436) | best size-normalized=diversity_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.0116) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n64; empirical front=balanced_n64,cheapOracle_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 433.5 | 0.798 | negligible (0.4817) | A12<0.5 means SRS risks tend to be lower; median SRS=0.009, median random=0.00925 |
| `FSE6` | `lcbench__workload_albert__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 350 | 0.328 | small (0.3889) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03184, median random=0.03375 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003498 | 0.1 | 0.8586 | -0.04142 | -0.03026 |
| `balanced_n8` | 8 | 0.004 | 0.004501 | 0.08 | 0.9154 | 0.01537 | 0.006256 |
| `diversity_n8` | 8 | 0.004 | 0.00397 | 0.0005 | 0.9995 | 0.0995 | 0.1001 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003235 | 0.08 | 0.8661 | -0.03393 | -0.01588 |
| `pairwise_n8` | 8 | 0.004 | 0.004265 | 0.052 | 0.948 | 0.048 | 0.04296 |
| `pilotCost_n8` | 8 | 0.004 | 0.001812 | 0.161 | 0.8527 | -0.04728 | 0.03054 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001318 | 0.194 | 0.806 | -0.094 | 0.02169 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.06188 | 0.0875 | 0.9125 | 0.0125 | -0.07955 |
| `random_n16` | 16 | 0.008 | 0.00674 | 0.033 | 0.9532 | 0.008772 | 0.01781 |
| `balanced_n16` | 16 | 0.008 | 0.007321 | 0.05175 | 0.943 | -0.001444 | 0.00309 |
| `diversity_n16` | 16 | 0.008 | 0.006365 | 0.0005 | 0.9995 | 0.05506 | 0.06739 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007 | 0.033 | 0.9554 | 0.01091 | 0.01785 |
| `pairwise_n16` | 16 | 0.008 | 0.007548 | 0.052 | 0.948 | 0.003556 | 0.006492 |
| `pilotCost_n16` | 16 | 0.008 | 0.00355 | 0.1575 | 0.881 | -0.06348 | -0.00915 |
| `cheapOracle_n16` | 16 | 0.008 | 0.002694 | 0.194 | 0.806 | -0.1384 | -0.05864 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.108 | 0.0875 | 0.9125 | -0.03194 | -0.08291 |
| `random_n20` | 20 | 0.01 | 0.00955 | 0.04625 | 0.9464 | -0.008112 | -0.006175 |
| `balanced_n20` | 20 | 0.01 | 0.008894 | 0.0355 | 0.9503 | -0.004245 | 0.0008351 |
| `diversity_n20` | 20 | 0.01 | 0.01375 | 0.0005 | 0.9995 | 0.04495 | 0.03339 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009403 | 0.04625 | 0.9461 | -0.008429 | -0.005821 |
| `pairwise_n20` | 20 | 0.01 | 0.0105 | 0.052 | 0.948 | -0.006545 | -0.008527 |
| `pilotCost_n20` | 20 | 0.01 | 0.004706 | 0.0215 | 0.9423 | -0.01226 | 0.02992 |
| `cheapOracle_n20` | 20 | 0.01 | 0.003397 | 0.194 | 0.806 | -0.1485 | -0.08029 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.1282 | 0.0865 | 0.9135 | -0.04105 | -0.08263 |
| `random_n32` | 32 | 0.016 | 0.01468 | 0.023 | 0.9744 | 0.003795 | 0.006272 |
| `balanced_n32` | 32 | 0.016 | 0.01342 | 0.024 | 0.9678 | -0.002788 | 0.002474 |
| `diversity_n32` | 32 | 0.016 | 0.02094 | 0.0005 | 0.9995 | 0.02891 | 0.02229 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01549 | 0.02625 | 0.9709 | 0.0002784 | 0.001193 |
| `pairwise_n32` | 32 | 0.016 | 0.01474 | 0.052 | 0.948 | -0.02259 | -0.02024 |
| `pilotCost_n32` | 32 | 0.016 | 0.007184 | 0.1008 | 0.9036 | -0.06697 | -0.03529 |
| `cheapOracle_n32` | 32 | 0.016 | 0.005558 | 0.123 | 0.877 | -0.09359 | -0.04676 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.1779 | 0.0865 | 0.9135 | -0.05709 | -0.08371 |
| `random_n40` | 40 | 0.02 | 0.01949 | 0.014 | 0.9819 | 0.00576 | 0.006352 |
| `balanced_n40` | 40 | 0.02 | 0.01608 | 0.01 | 0.9847 | 0.008493 | 0.01396 |
| `diversity_n40` | 40 | 0.02 | 0.03298 | 0.0005 | 0.9995 | 0.02331 | 0.01421 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01872 | 0.0245 | 0.9753 | -0.0008738 | 0.000674 |
| `pairwise_n40` | 40 | 0.02 | 0.018 | 0.0165 | 0.9835 | 0.00731 | 0.009816 |
| `pilotCost_n40` | 40 | 0.02 | 0.008783 | 0.0215 | 0.928 | -0.04822 | -0.02093 |
| `cheapOracle_n40` | 40 | 0.02 | 0.007021 | 0.123 | 0.877 | -0.09919 | -0.06066 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.2043 | 0.0865 | 0.9135 | -0.06269 | -0.08406 |
| `random_n64` | 64 | 0.032 | 0.03375 | 0.00925 | 0.9863 | 0.001452 | 0.0006864 |
| `balanced_n64` | 64 | 0.032 | 0.02526 | 0.0035 | 0.9948 | 0.009985 | 0.01387 |
| `diversity_n64` | 64 | 0.032 | 0.04471 | 0.0005 | 0.9995 | 0.01465 | 0.01044 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03184 | 0.009 | 0.987 | 0.002202 | 0.002276 |
| `pairwise_n64` | 64 | 0.032 | 0.02533 | 0.0145 | 0.9855 | 0.0006515 | 0.004489 |
| `pilotCost_n64` | 64 | 0.032 | 0.01435 | 0.0005 | 0.9795 | -0.005315 | 0.0121 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01147 | 0.077 | 0.923 | -0.06185 | -0.0369 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.2656 | 0.008 | 0.992 | 0.007152 | -0.006125 |
