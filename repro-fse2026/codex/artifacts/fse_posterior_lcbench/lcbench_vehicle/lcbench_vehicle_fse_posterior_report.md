# lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `cheapOracle_n8` (risk 0, %cost 0.001826).

Best integrated confidence after normalizing the prior baseline by empirical cost: `cheapOracle_n8` (omega_cost 0.177, %cost 0.001826).

Empirical cost/confidence Pareto front:

- `cheapOracle_n8`: posterior area 1, risk 0, %cost 0.001826, omega_cost 0.177

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n8` | `supports` | 28.79 | 1.58e-04 | large (0.1879) | median risks: random=0.109, balanced=0.0255, diversity=0.015, SRSSampling=0.096, pairwise=0.0685, pilotCost=0.01125, cheapOracle=0, expensiveOracle=0.0075; spread=0.109 |
| `FSE1` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n16` | `supports` | 35.49 | 9.04e-06 | moderate (0.2456) | median risks: random=0.0445, balanced=0.011, diversity=0.0035, SRSSampling=0.0445, pairwise=0.006, pilotCost=0.00675, cheapOracle=0, expensiveOracle=0.0075; spread=0.0445 |
| `FSE1` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n20` | `supports` | 21.62 | 0.00295 | moderate (0.126) | median risks: random=0.0355, balanced=0.011, diversity=0.0035, SRSSampling=0.0355, pairwise=0.006, pilotCost=0.011, cheapOracle=0, expensiveOracle=0.0075; spread=0.0355 |
| `FSE1` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n32` | `supports` | 54.14 | 2.20e-09 | moderate (0.4064) | median risks: random=0.0205, balanced=0.00925, diversity=0.0035, SRSSampling=0.022, pairwise=0.006, pilotCost=0.0015, cheapOracle=0, expensiveOracle=0.0075; spread=0.022 |
| `FSE1` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n40` | `supports` | 53.76 | 2.62e-09 | moderate (0.4031) | median risks: random=0.0205, balanced=0.006, diversity=0.0035, SRSSampling=0.019, pairwise=0.006, pilotCost=0, cheapOracle=0, expensiveOracle=0.0075; spread=0.0205 |
| `FSE1` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n64` | `supports` | 61.59 | 7.27e-11 | moderate (0.4706) | median risks: random=0.011, balanced=0.0035, diversity=0.0035, SRSSampling=0.013, pairwise=0.006, pilotCost=0, cheapOracle=0, expensiveOracle=0.0075; spread=0.013 |
| `FSE2` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | unchanged (0) | best size-normalized=cheapOracle_n8; best cost-normalized=cheapOracle_n8 |
| `FSE3` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.2085) | best cost-normalized=cheapOracle_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 1 |  | same frontier (0) | count front=cheapOracle_n8; empirical front=cheapOracle_n8 |
| `FSE5` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 438 | 0.747 | negligible (0.4867) | A12<0.5 means SRS risks tend to be lower; median SRS=0.096, median random=0.109 |
| `FSE6` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 441.5 | 0.708 | negligible (0.4906) | A12>0.5 means SRS costs tend to be higher; median SRS=0.00371, median random=0.003796 |
| `FSE2` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=cheapOracle_n16; best cost-normalized=cheapOracle_n16 |
| `FSE3` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.09628) | best cost-normalized=cheapOracle_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 1 |  | same frontier (0) | count front=cheapOracle_n16; empirical front=cheapOracle_n16 |
| `FSE5` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 446.5 | 0.654 | negligible (0.4961) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0445, median random=0.0445 |
| `FSE6` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 438.5 | 0.741 | negligible (0.5128) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007938, median random=0.007759 |
| `FSE2` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=cheapOracle_n20; best cost-normalized=cheapOracle_n20 |
| `FSE3` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.09116) | best cost-normalized=cheapOracle_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 1 |  | same frontier (0) | count front=cheapOracle_n20; empirical front=cheapOracle_n20 |
| `FSE5` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 447 | 0.649 | negligible (0.5033) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0355, median random=0.0355 |
| `FSE6` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 448.5 | 0.633 | negligible (0.4983) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009688, median random=0.009688 |
| `FSE2` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=cheapOracle_n32; best cost-normalized=cheapOracle_n32 |
| `FSE3` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.0564) | best cost-normalized=cheapOracle_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 1 |  | same frontier (0) | count front=cheapOracle_n32; empirical front=cheapOracle_n32 |
| `FSE5` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 447.5 | 0.643 | negligible (0.5028) | A12<0.5 means SRS risks tend to be lower; median SRS=0.022, median random=0.0205 |
| `FSE6` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 449 | 0.628 | negligible (0.4989) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01534, median random=0.01502 |
| `FSE2` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | unchanged (0) | best size-normalized=cheapOracle_n40; best cost-normalized=cheapOracle_n40 |
| `FSE3` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.04227) | best cost-normalized=cheapOracle_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 1 |  | same frontier (0) | count front=cheapOracle_n40; empirical front=cheapOracle_n40 |
| `FSE5` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 438 | 0.748 | negligible (0.4867) | A12<0.5 means SRS risks tend to be lower; median SRS=0.019, median random=0.0205 |
| `FSE6` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 335 | 0.23 | small (0.3722) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01892, median random=0.02004 |
| `FSE2` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | unchanged (0) | best size-normalized=cheapOracle_n64; best cost-normalized=cheapOracle_n64 |
| `FSE3` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.02536) | best cost-normalized=cheapOracle_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 1 |  | same frontier (0) | count front=cheapOracle_n64; empirical front=cheapOracle_n64 |
| `FSE5` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 419.5 | 0.963 | negligible (0.4661) | A12<0.5 means SRS risks tend to be lower; median SRS=0.013, median random=0.011 |
| `FSE6` | `lcbench__workload_vehicle__cost_time_total__target_final_val_accuracy:n64` | `supports` | 241 | 0.0096 | large (0.2678) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02936, median random=0.03242 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003796 | 0.109 | 0.8591 | -0.04087 | -0.03662 |
| `balanced_n8` | 8 | 0.004 | 0.00269 | 0.0255 | 0.9548 | 0.0548 | 0.09031 |
| `diversity_n8` | 8 | 0.004 | 0.005215 | 0.015 | 0.985 | 0.085 | 0.06545 |
| `SRSSampling_n8` | 8 | 0.004 | 0.00371 | 0.096 | 0.8623 | -0.03773 | -0.03159 |
| `pairwise_n8` | 8 | 0.004 | 0.003391 | 0.0685 | 0.9315 | 0.0315 | 0.04537 |
| `pilotCost_n8` | 8 | 0.004 | 0.00231 | 0.01125 | 0.9424 | 0.04235 | 0.09339 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001826 | 0 | 1 | 0.1 | 0.177 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.02949 | 0.0075 | 0.9925 | 0.0925 | 0.008896 |
| `random_n16` | 16 | 0.008 | 0.007759 | 0.0445 | 0.9464 | 0.001956 | 0.003483 |
| `balanced_n16` | 16 | 0.008 | 0.005263 | 0.011 | 0.9753 | 0.03089 | 0.05517 |
| `diversity_n16` | 16 | 0.008 | 0.008121 | 0.0035 | 0.9965 | 0.05206 | 0.05132 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007938 | 0.0445 | 0.9495 | 0.005072 | 0.005458 |
| `pairwise_n16` | 16 | 0.008 | 0.007527 | 0.006 | 0.994 | 0.04956 | 0.05264 |
| `pilotCost_n16` | 16 | 0.008 | 0.004648 | 0.00675 | 0.9753 | 0.03082 | 0.06379 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003914 | 0 | 1 | 0.05556 | 0.1017 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.05594 | 0.0075 | 0.9925 | 0.04806 | 0.001281 |
| `random_n20` | 20 | 0.01 | 0.009688 | 0.0355 | 0.9458 | -0.008712 | -0.007384 |
| `balanced_n20` | 20 | 0.01 | 0.006353 | 0.011 | 0.9738 | 0.0192 | 0.04175 |
| `diversity_n20` | 20 | 0.01 | 0.01286 | 0.0035 | 0.9965 | 0.04195 | 0.03258 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009688 | 0.0355 | 0.9456 | -0.008912 | -0.007584 |
| `pairwise_n20` | 20 | 0.01 | 0.00926 | 0.006 | 0.994 | 0.03945 | 0.04273 |
| `pilotCost_n20` | 20 | 0.01 | 0.005905 | 0.011 | 0.9724 | 0.01784 | 0.04479 |
| `cheapOracle_n20` | 20 | 0.01 | 0.004982 | 0 | 1 | 0.04545 | 0.08358 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.06773 | 0.0075 | 0.9925 | 0.03795 | -0.000225 |
| `random_n32` | 32 | 0.016 | 0.01502 | 0.0205 | 0.9639 | -0.006688 | -0.004886 |
| `balanced_n32` | 32 | 0.016 | 0.01027 | 0.00925 | 0.9865 | 0.01595 | 0.03089 |
| `diversity_n32` | 32 | 0.016 | 0.0202 | 0.0035 | 0.9965 | 0.02591 | 0.02008 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01534 | 0.022 | 0.9673 | -0.003255 | -0.002067 |
| `pairwise_n32` | 32 | 0.016 | 0.01548 | 0.006 | 0.994 | 0.02341 | 0.02435 |
| `pilotCost_n32` | 32 | 0.016 | 0.009384 | 0.0015 | 0.996 | 0.02543 | 0.04417 |
| `cheapOracle_n32` | 32 | 0.016 | 0.008203 | 0 | 1 | 0.02941 | 0.05433 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.0993 | 0.0075 | 0.9925 | 0.02191 | -0.002515 |
| `random_n40` | 40 | 0.02 | 0.02004 | 0.0205 | 0.979 | 0.002843 | 0.0028 |
| `balanced_n40` | 40 | 0.02 | 0.01328 | 0.006 | 0.9897 | 0.01349 | 0.02469 |
| `diversity_n40` | 40 | 0.02 | 0.03028 | 0.0035 | 0.9965 | 0.02031 | 0.01249 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01892 | 0.019 | 0.9766 | 0.0004262 | 0.001717 |
| `pairwise_n40` | 40 | 0.02 | 0.01889 | 0.006 | 0.994 | 0.01781 | 0.01914 |
| `pilotCost_n40` | 40 | 0.02 | 0.01168 | 0 | 0.9977 | 0.02151 | 0.03712 |
| `cheapOracle_n40` | 40 | 0.02 | 0.01037 | 0 | 1 | 0.02381 | 0.04398 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.1177 | 0.0075 | 0.9925 | 0.01631 | -0.003289 |
| `random_n64` | 64 | 0.032 | 0.03242 | 0.011 | 0.9835 | -0.001365 | -0.001556 |
| `balanced_n64` | 64 | 0.032 | 0.02218 | 0.0035 | 0.9933 | 0.008468 | 0.01488 |
| `diversity_n64` | 64 | 0.032 | 0.04196 | 0.0035 | 0.9965 | 0.01165 | 0.008139 |
| `SRSSampling_n64` | 64 | 0.032 | 0.02936 | 0.013 | 0.986 | 0.001202 | 0.00252 |
| `pairwise_n64` | 64 | 0.032 | 0.03066 | 0.006 | 0.994 | 0.009152 | 0.009793 |
| `pilotCost_n64` | 64 | 0.032 | 0.0189 | 0 | 0.9993 | 0.01445 | 0.02443 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01694 | 0 | 1 | 0.01515 | 0.02788 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.1683 | 0.0075 | 0.9925 | 0.007652 | -0.004547 |
