# lcbench__workload_nomao__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n20` (risk 0, %cost 0.01227).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pairwise_n8` (omega_cost 0.08567, %cost 0.003601).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.9975, risk 0.0025, %cost 0.005067, omega_cost 0.07992
- `pairwise_n8`: posterior area 0.977, risk 0.023, %cost 0.003601, omega_cost 0.08567
- `pilotCost_n8`: posterior area 0.7867, risk 0.206, %cost 0.002214, omega_cost -0.05773
- `cheapOracle_n8`: posterior area 0.4975, risk 0.5025, %cost 0.001852, omega_cost -0.3272
- `diversity_n20`: posterior area 1, risk 0, %cost 0.01227, omega_cost 0.03768

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n8` | `supports` | 24.75 | 8.39e-04 | large (0.153) | median risks: random=0.08, balanced=0.066, diversity=0.0025, SRSSampling=0.077, pairwise=0.023, pilotCost=0.206, cheapOracle=0.5025, expensiveOracle=0.004; spread=0.5 |
| `FSE1` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n16` | `supports` | 17.63 | 0.0138 | large (0.0916) | median risks: random=0.0435, balanced=0.0475, diversity=0.0025, SRSSampling=0.0435, pairwise=0.023, pilotCost=0.0705, cheapOracle=0.3065, expensiveOracle=0.004; spread=0.304 |
| `FSE1` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n20` | `inconclusive` | 8.375 | 0.301 | large (0.01185) | median risks: random=0.053, balanced=0.035, diversity=0, SRSSampling=0.053, pairwise=0.023, pilotCost=0.0455, cheapOracle=0.2625, expensiveOracle=0.004; spread=0.2625 |
| `FSE1` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n32` | `supports` | 23.61 | 0.00133 | large (0.1432) | median risks: random=0.02275, balanced=0.018, diversity=0, SRSSampling=0.0255, pairwise=0.023, pilotCost=0.068, cheapOracle=0.1275, expensiveOracle=0.004; spread=0.1275 |
| `FSE1` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n40` | `supports` | 28.19 | 2.03e-04 | large (0.1827) | median risks: random=0.015, balanced=0.015, diversity=0, SRSSampling=0.021, pairwise=0.023, pilotCost=0.049, cheapOracle=0.1275, expensiveOracle=0.004; spread=0.1275 |
| `FSE1` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n64` | `supports` | 14.31 | 0.046 | large (0.063) | median risks: random=0.015, balanced=0.0025, diversity=0, SRSSampling=0.0115, pairwise=0.023, pilotCost=0.0025, cheapOracle=0.1275, expensiveOracle=0.004; spread=0.1275 |
| `FSE2` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.005751) | best size-normalized=diversity_n8; best cost-normalized=pairwise_n8 |
| `FSE3` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.0778) | best cost-normalized=pairwise_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n8; empirical front=cheapOracle_n8,diversity_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 429.5 | 0.844 | negligible (0.4772) | A12<0.5 means SRS risks tend to be lower; median SRS=0.077, median random=0.08 |
| `FSE6` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 439.5 | 0.73 | negligible (0.4883) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003919, median random=0.003919 |
| `FSE2` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.0528) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16,pairwise_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 439 | 0.736 | negligible (0.4878) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0435, median random=0.0435 |
| `FSE6` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 425.5 | 0.891 | negligible (0.5272) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007616, median random=0.007488 |
| `FSE2` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n20; best cost-normalized=diversity_n20 |
| `FSE3` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.05379) | best cost-normalized=diversity_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n20; empirical front=balanced_n20,cheapOracle_n20,diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 449.5 | 0.622 | negligible (0.4994) | A12<0.5 means SRS risks tend to be lower; median SRS=0.053, median random=0.053 |
| `FSE6` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 440.5 | 0.719 | negligible (0.4894) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009607, median random=0.009613 |
| `FSE2` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02567) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n32; empirical front=balanced_n32,cheapOracle_n32,diversity_n32,pairwise_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 424 | 0.908 | negligible (0.4711) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0255, median random=0.02275 |
| `FSE6` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 338 | 0.248 | small (0.6244) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01681, median random=0.01514 |
| `FSE2` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n40; best cost-normalized=diversity_n40 |
| `FSE3` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.02111) | best cost-normalized=diversity_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n40; empirical front=balanced_n40,cheapOracle_n40,diversity_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 390.5 | 0.704 | small (0.5661) | A12<0.5 means SRS risks tend to be lower; median SRS=0.021, median random=0.015 |
| `FSE6` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 426 | 0.885 | negligible (0.4733) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02013, median random=0.02107 |
| `FSE2` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n64; best cost-normalized=diversity_n64 |
| `FSE3` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01203) | best cost-normalized=diversity_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n64; empirical front=balanced_n64,cheapOracle_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 443.5 | 0.686 | negligible (0.4928) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0115, median random=0.015 |
| `FSE6` | `lcbench__workload_nomao__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 445 | 0.67 | negligible (0.5056) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03223, median random=0.03232 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003919 | 0.08 | 0.9019 | 0.001883 | 0.003537 |
| `balanced_n8` | 8 | 0.004 | 0.003683 | 0.066 | 0.9213 | 0.02133 | 0.0281 |
| `diversity_n8` | 8 | 0.004 | 0.005067 | 0.0025 | 0.9975 | 0.0975 | 0.07992 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003919 | 0.077 | 0.9062 | 0.006217 | 0.007871 |
| `pairwise_n8` | 8 | 0.004 | 0.003601 | 0.023 | 0.977 | 0.077 | 0.08567 |
| `pilotCost_n8` | 8 | 0.004 | 0.002214 | 0.206 | 0.7867 | -0.1133 | -0.05773 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001852 | 0.5025 | 0.4975 | -0.4025 | -0.3272 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.03134 | 0.004 | 0.996 | 0.096 | 0.01146 |
| `random_n16` | 16 | 0.008 | 0.007488 | 0.0435 | 0.9382 | -0.006244 | -0.002892 |
| `balanced_n16` | 16 | 0.008 | 0.006714 | 0.0475 | 0.9557 | 0.01127 | 0.02053 |
| `diversity_n16` | 16 | 0.008 | 0.008283 | 0.0025 | 0.9975 | 0.05306 | 0.05136 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007616 | 0.0435 | 0.9405 | -0.003911 | -0.001433 |
| `pairwise_n16` | 16 | 0.008 | 0.007623 | 0.023 | 0.977 | 0.03256 | 0.03498 |
| `pilotCost_n16` | 16 | 0.008 | 0.004444 | 0.0705 | 0.8452 | -0.09923 | -0.06294 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003737 | 0.3065 | 0.6935 | -0.2509 | -0.201 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.05195 | 0.004 | 0.996 | 0.05156 | 0.005444 |
| `random_n20` | 20 | 0.01 | 0.009613 | 0.053 | 0.9367 | -0.01785 | -0.01619 |
| `balanced_n20` | 20 | 0.01 | 0.00805 | 0.035 | 0.9594 | 0.004855 | 0.01465 |
| `diversity_n20` | 20 | 0.01 | 0.01227 | 0 | 1 | 0.04545 | 0.03768 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009607 | 0.053 | 0.9367 | -0.0178 | -0.01611 |
| `pairwise_n20` | 20 | 0.01 | 0.00946 | 0.023 | 0.977 | 0.02245 | 0.0248 |
| `pilotCost_n20` | 20 | 0.01 | 0.005831 | 0.0455 | 0.9192 | -0.03531 | -0.007575 |
| `cheapOracle_n20` | 20 | 0.01 | 0.004691 | 0.2625 | 0.7375 | -0.217 | -0.1746 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.06104 | 0.004 | 0.996 | 0.04145 | 0.004059 |
| `random_n32` | 32 | 0.016 | 0.01514 | 0.02275 | 0.9708 | 0.0001618 | 0.001728 |
| `balanced_n32` | 32 | 0.016 | 0.0126 | 0.018 | 0.972 | 0.001445 | 0.008806 |
| `diversity_n32` | 32 | 0.016 | 0.01888 | 0 | 1 | 0.02941 | 0.02515 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01681 | 0.0255 | 0.9714 | 0.0008118 | -0.0005189 |
| `pairwise_n32` | 32 | 0.016 | 0.01574 | 0.023 | 0.977 | 0.006412 | 0.006861 |
| `pilotCost_n32` | 32 | 0.016 | 0.008953 | 0.068 | 0.9205 | -0.05012 | -0.0293 |
| `cheapOracle_n32` | 32 | 0.016 | 0.007615 | 0.1275 | 0.8725 | -0.09809 | -0.06946 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.08669 | 0.004 | 0.996 | 0.02541 | 0.001702 |
| `random_n40` | 40 | 0.02 | 0.02107 | 0.015 | 0.9784 | 0.00221 | 0.001055 |
| `balanced_n40` | 40 | 0.02 | 0.01544 | 0.015 | 0.9814 | 0.005193 | 0.01179 |
| `diversity_n40` | 40 | 0.02 | 0.02687 | 0 | 1 | 0.02381 | 0.01794 |
| `SRSSampling_n40` | 40 | 0.02 | 0.02013 | 0.021 | 0.9732 | -0.003024 | -0.003168 |
| `pairwise_n40` | 40 | 0.02 | 0.01902 | 0.023 | 0.977 | 0.0008095 | 0.001975 |
| `pilotCost_n40` | 40 | 0.02 | 0.01105 | 0.049 | 0.9376 | -0.03859 | -0.02092 |
| `cheapOracle_n40` | 40 | 0.02 | 0.009593 | 0.1275 | 0.8725 | -0.1037 | -0.0803 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.1021 | 0.004 | 0.996 | 0.01981 | 0.0008508 |
| `random_n64` | 64 | 0.032 | 0.03232 | 0.015 | 0.9843 | -0.0005818 | -0.0007257 |
| `balanced_n64` | 64 | 0.032 | 0.02486 | 0.0025 | 0.9932 | 0.008385 | 0.01257 |
| `diversity_n64` | 64 | 0.032 | 0.03849 | 0 | 1 | 0.01515 | 0.01266 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03223 | 0.0115 | 0.9856 | 0.0007348 | 0.0006293 |
| `pairwise_n64` | 64 | 0.032 | 0.03042 | 0.023 | 0.977 | -0.007848 | -0.007087 |
| `pilotCost_n64` | 64 | 0.032 | 0.01857 | 0.0025 | 0.9798 | -0.005065 | 0.005334 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01558 | 0.1275 | 0.8725 | -0.1123 | -0.09734 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.144 | 0.004 | 0.996 | 0.01115 | -0.0005514 |
