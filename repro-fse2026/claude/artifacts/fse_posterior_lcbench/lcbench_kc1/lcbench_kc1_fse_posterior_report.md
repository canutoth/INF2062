# lcbench__workload_kc1__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `balanced_n32` (risk 0.001, %cost 0.01045).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pairwise_n8` (omega_cost 0.08666, %cost 0.003342).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9507, risk 0.043, %cost 0.002781, omega_cost 0.08297
- `pairwise_n8`: posterior area 0.9715, risk 0.0285, %cost 0.003342, omega_cost 0.08666
- `cheapOracle_n8`: posterior area 0.8445, risk 0.1555, %cost 0.00194, omega_cost 0.01455
- `balanced_n16`: posterior area 0.9718, risk 0.0385, %cost 0.005352, omega_cost 0.05053
- `balanced_n20`: posterior area 0.9816, risk 0.0165, %cost 0.006527, omega_cost 0.04798
- `balanced_n32`: posterior area 0.9872, risk 0.001, %cost 0.01045, omega_cost 0.03093
- `balanced_n64`: posterior area 0.9881, risk 0.008, %cost 0.02244, omega_cost 0.009429

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n8` | `supports` | 24.64 | 8.80e-04 | large (0.152) | median risks: random=0.048, balanced=0.043, diversity=0.056, SRSSampling=0.06325, pairwise=0.0285, pilotCost=0.178, cheapOracle=0.1555, expensiveOracle=0.111; spread=0.1495 |
| `FSE1` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n16` | `supports` | 45.56 | 1.06e-07 | large (0.3324) | median risks: random=0.0645, balanced=0.0385, diversity=0.021, SRSSampling=0.0645, pairwise=0.0285, pilotCost=0.1555, cheapOracle=0.1555, expensiveOracle=0.1045; spread=0.1345 |
| `FSE1` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n20` | `supports` | 62.54 | 4.69e-11 | large (0.4788) | median risks: random=0.043, balanced=0.0165, diversity=0.021, SRSSampling=0.04175, pairwise=0.0285, pilotCost=0.1555, cheapOracle=0.1555, expensiveOracle=0.083; spread=0.139 |
| `FSE1` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n32` | `supports` | 66.01 | 9.43e-12 | large (0.5087) | median risks: random=0.014, balanced=0.001, diversity=0.021, SRSSampling=0.013, pairwise=0.0285, pilotCost=0.1517, cheapOracle=0.1555, expensiveOracle=0.083; spread=0.1545 |
| `FSE1` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n40` | `supports` | 49.62 | 1.71e-08 | large (0.3674) | median risks: random=0.0245, balanced=0.013, diversity=0.021, SRSSampling=0.008, pairwise=0.0285, pilotCost=0.1325, cheapOracle=0.059, expensiveOracle=0.083; spread=0.1245 |
| `FSE1` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n64` | `supports` | 45.58 | 1.05e-07 | large (0.3326) | median risks: random=0.012, balanced=0.008, diversity=0.014, SRSSampling=0.008, pairwise=0.0285, pilotCost=0.0695, cheapOracle=0.059, expensiveOracle=0.0645; spread=0.0615 |
| `FSE2` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | unchanged (0) | best size-normalized=pairwise_n8; best cost-normalized=pairwise_n8 |
| `FSE3` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.08577) | best cost-normalized=pairwise_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.3333 |  | large frontier change (2) | count front=pairwise_n8; empirical front=balanced_n8,cheapOracle_n8,pairwise_n8 |
| `FSE5` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 435 | 0.781 | negligible (0.5167) | A12<0.5 means SRS risks tend to be lower; median SRS=0.06325, median random=0.048 |
| `FSE6` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 437.5 | 0.753 | negligible (0.4861) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003704, median random=0.003852 |
| `FSE2` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.01619) | best size-normalized=diversity_n16; best cost-normalized=balanced_n16 |
| `FSE3` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.06466) | best cost-normalized=balanced_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 440 | 0.725 | negligible (0.5111) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0645, median random=0.0645 |
| `FSE6` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 437.5 | 0.753 | negligible (0.5139) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007826, median random=0.007723 |
| `FSE2` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=balanced_n20; best cost-normalized=balanced_n20 |
| `FSE3` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.05319) | best cost-normalized=balanced_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.3333 |  | large frontier change (2) | count front=balanced_n20; empirical front=balanced_n20,cheapOracle_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 438.5 | 0.742 | negligible (0.4872) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04175, median random=0.043 |
| `FSE6` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 449.5 | 0.622 | negligible (0.4994) | A12>0.5 means SRS costs tend to be higher; median SRS=0.00969, median random=0.00969 |
| `FSE2` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=balanced_n32; best cost-normalized=balanced_n32 |
| `FSE3` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02175) | best cost-normalized=balanced_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.3333 |  | large frontier change (2) | count front=balanced_n32; empirical front=balanced_n32,cheapOracle_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 435.5 | 0.776 | negligible (0.5161) | A12<0.5 means SRS risks tend to be lower; median SRS=0.013, median random=0.014 |
| `FSE6` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 360 | 0.406 | small (0.6) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01644, median random=0.01513 |
| `FSE2` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | unchanged (0) | best size-normalized=balanced_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.02102) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.5 |  | frontier change (1) | count front=balanced_n40; empirical front=balanced_n40,cheapOracle_n40 |
| `FSE5` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 371.5 | 0.503 | small (0.4128) | A12<0.5 means SRS risks tend to be lower; median SRS=0.008, median random=0.0245 |
| `FSE6` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 446 | 0.659 | negligible (0.4956) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02021, median random=0.0201 |
| `FSE2` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | unchanged (0) | best size-normalized=balanced_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | moderate (0.00769) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.5 |  | frontier change (1) | count front=balanced_n64; empirical front=balanced_n64,cheapOracle_n64 |
| `FSE5` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 393.5 | 0.726 | small (0.4372) | A12<0.5 means SRS risks tend to be lower; median SRS=0.008, median random=0.012 |
| `FSE6` | `lcbench__workload_kc1__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 410 | 0.927 | negligible (0.5444) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03269, median random=0.03229 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003852 | 0.048 | 0.9034 | 0.003433 | 0.006482 |
| `balanced_n8` | 8 | 0.004 | 0.002781 | 0.043 | 0.9507 | 0.05075 | 0.08297 |
| `diversity_n8` | 8 | 0.004 | 0.005138 | 0.056 | 0.944 | 0.044 | 0.02546 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003704 | 0.06325 | 0.8946 | -0.0054 | 0.0008889 |
| `pairwise_n8` | 8 | 0.004 | 0.003342 | 0.0285 | 0.9715 | 0.0715 | 0.08666 |
| `pilotCost_n8` | 8 | 0.004 | 0.002351 | 0.178 | 0.7999 | -0.1001 | -0.05094 |
| `cheapOracle_n8` | 8 | 0.004 | 0.00194 | 0.1555 | 0.8445 | -0.0555 | 0.01455 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.02943 | 0.111 | 0.889 | -0.011 | -0.09457 |
| `random_n16` | 16 | 0.008 | 0.007723 | 0.0645 | 0.9308 | -0.01366 | -0.0119 |
| `balanced_n16` | 16 | 0.008 | 0.005352 | 0.0385 | 0.9718 | 0.02737 | 0.05053 |
| `diversity_n16` | 16 | 0.008 | 0.008036 | 0.021 | 0.979 | 0.03456 | 0.03434 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007826 | 0.0645 | 0.9292 | -0.01523 | -0.01413 |
| `pairwise_n16` | 16 | 0.008 | 0.007432 | 0.0285 | 0.9715 | 0.02706 | 0.0308 |
| `pilotCost_n16` | 16 | 0.008 | 0.004698 | 0.1555 | 0.8579 | -0.08656 | -0.05437 |
| `cheapOracle_n16` | 16 | 0.008 | 0.004013 | 0.1555 | 0.8445 | -0.09994 | -0.05576 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.05522 | 0.1045 | 0.8955 | -0.04894 | -0.09561 |
| `random_n20` | 20 | 0.01 | 0.00969 | 0.043 | 0.947 | -0.007562 | -0.006244 |
| `balanced_n20` | 20 | 0.01 | 0.006527 | 0.0165 | 0.9816 | 0.027 | 0.04798 |
| `diversity_n20` | 20 | 0.01 | 0.01254 | 0.021 | 0.979 | 0.02445 | 0.01592 |
| `SRSSampling_n20` | 20 | 0.01 | 0.00969 | 0.04175 | 0.948 | -0.006529 | -0.005211 |
| `pairwise_n20` | 20 | 0.01 | 0.009158 | 0.0285 | 0.9715 | 0.01695 | 0.02072 |
| `pilotCost_n20` | 20 | 0.01 | 0.005927 | 0.1555 | 0.8519 | -0.1027 | -0.07593 |
| `cheapOracle_n20` | 20 | 0.01 | 0.005076 | 0.1555 | 0.8445 | -0.11 | -0.07321 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.06681 | 0.083 | 0.917 | -0.03755 | -0.07563 |
| `random_n32` | 32 | 0.016 | 0.01513 | 0.014 | 0.9774 | 0.006812 | 0.008403 |
| `balanced_n32` | 32 | 0.016 | 0.01045 | 0.001 | 0.9872 | 0.01666 | 0.03093 |
| `diversity_n32` | 32 | 0.016 | 0.01977 | 0.021 | 0.979 | 0.008412 | 0.003077 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01644 | 0.013 | 0.9805 | 0.009928 | 0.009181 |
| `pairwise_n32` | 32 | 0.016 | 0.01534 | 0.0285 | 0.9715 | 0.0009118 | 0.002106 |
| `pilotCost_n32` | 32 | 0.016 | 0.009496 | 0.1517 | 0.8716 | -0.09902 | -0.08079 |
| `cheapOracle_n32` | 32 | 0.016 | 0.008301 | 0.1555 | 0.8445 | -0.1261 | -0.1017 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.09786 | 0.083 | 0.917 | -0.05359 | -0.07794 |
| `random_n40` | 40 | 0.02 | 0.0201 | 0.0245 | 0.9726 | -0.003574 | -0.003685 |
| `balanced_n40` | 40 | 0.02 | 0.01339 | 0.013 | 0.9864 | 0.01024 | 0.02118 |
| `diversity_n40` | 40 | 0.02 | 0.0293 | 0.021 | 0.979 | 0.00281 | -0.004501 |
| `SRSSampling_n40` | 40 | 0.02 | 0.02021 | 0.008 | 0.9766 | 0.0003929 | 0.0001534 |
| `pairwise_n40` | 40 | 0.02 | 0.01869 | 0.0285 | 0.9715 | -0.00469 | -0.003109 |
| `pilotCost_n40` | 40 | 0.02 | 0.01183 | 0.1325 | 0.8841 | -0.09207 | -0.07693 |
| `cheapOracle_n40` | 40 | 0.02 | 0.01047 | 0.059 | 0.941 | -0.03519 | -0.0154 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.1162 | 0.083 | 0.917 | -0.05919 | -0.07874 |
| `random_n64` | 64 | 0.032 | 0.03229 | 0.012 | 0.9853 | 0.0004515 | 0.0003194 |
| `balanced_n64` | 64 | 0.032 | 0.02244 | 0.008 | 0.9881 | 0.003252 | 0.009429 |
| `diversity_n64` | 64 | 0.032 | 0.04144 | 0.014 | 0.986 | 0.001152 | -0.002219 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03269 | 0.008 | 0.9869 | 0.002052 | 0.001739 |
| `pairwise_n64` | 64 | 0.032 | 0.03032 | 0.0285 | 0.9715 | -0.01335 | -0.01254 |
| `pilotCost_n64` | 64 | 0.032 | 0.01912 | 0.0695 | 0.9246 | -0.06025 | -0.05054 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01704 | 0.059 | 0.941 | -0.04385 | -0.03129 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.1663 | 0.0645 | 0.9355 | -0.04935 | -0.06151 |
