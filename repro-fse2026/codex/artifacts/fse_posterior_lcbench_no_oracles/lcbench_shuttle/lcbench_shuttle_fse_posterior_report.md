# lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n20` (risk 0.001, %cost 0.01192).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pairwise_n8` (omega_cost 0.09363, %cost 0.004148).

Empirical cost/confidence Pareto front:

- `random_n8`: posterior area 0.8921, risk 0.08875, %cost 0.003725, omega_cost -0.002108
- `balanced_n8`: posterior area 0.9294, risk 0.06575, %cost 0.004065, omega_cost 0.02812
- `SRSSampling_n8`: posterior area 0.8907, risk 0.0915, %cost 0.003647, omega_cost -0.001661
- `pairwise_n8`: posterior area 0.9965, risk 0.0035, %cost 0.004148, omega_cost 0.09363
- `pilotCost_n8`: posterior area 0.6607, risk 0.3938, %cost 0.0025, omega_cost -0.1965
- `diversity_n20`: posterior area 0.999, risk 0.001, %cost 0.01192, omega_cost 0.03769

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n8` | `supports` | 29.29 | 2.04e-05 | large (0.2094) | median risks: random=0.08875, balanced=0.06575, diversity=0.306, SRSSampling=0.0915, pairwise=0.0035, pilotCost=0.3938; spread=0.3903 |
| `FSE1` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n16` | `supports` | 29.33 | 2.00e-05 | large (0.2098) | median risks: random=0.029, balanced=0.057, diversity=0.018, SRSSampling=0.029, pairwise=0.0035, pilotCost=0.3073; spread=0.3038 |
| `FSE1` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n20` | `inconclusive` | 7.43 | 0.191 | large (0.02095) | median risks: random=0.037, balanced=0.05075, diversity=0.001, SRSSampling=0.03825, pairwise=0.0035, pilotCost=0.05675; spread=0.05575 |
| `FSE1` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n32` | `supports` | 30.11 | 1.40e-05 | large (0.2164) | median risks: random=0.02, balanced=0.0155, diversity=0.001, SRSSampling=0.03175, pairwise=0.0035, pilotCost=0.08825; spread=0.08725 |
| `FSE1` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n40` | `supports` | 30.17 | 1.37e-05 | large (0.217) | median risks: random=0.015, balanced=0.01175, diversity=0.001, SRSSampling=0.024, pairwise=0.0035, pilotCost=0.0735; spread=0.0725 |
| `FSE1` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 10.4 | 0.0646 | moderate (0.04656) | median risks: random=0.0145, balanced=0.0045, diversity=0.001, SRSSampling=0.0085, pairwise=0.0035, pilotCost=0.011; spread=0.0135 |
| `FSE2` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | unchanged (0) | best size-normalized=pairwise_n8; best cost-normalized=pairwise_n8 |
| `FSE3` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.09529) | best cost-normalized=pairwise_n8; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.2 |  | large frontier change (4) | count front=pairwise_n8; empirical front=SRSSampling_n8,balanced_n8,pairwise_n8,pilotCost_n8,random_n8 |
| `FSE5` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 440.5 | 0.719 | negligible (0.5106) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0915, median random=0.08875 |
| `FSE6` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 438.5 | 0.741 | negligible (0.4872) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003647, median random=0.003725 |
| `FSE2` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=pairwise_n16; best cost-normalized=pairwise_n16 |
| `FSE3` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.03388) | best cost-normalized=pairwise_n16; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.25 |  | large frontier change (3) | count front=pairwise_n16; empirical front=SRSSampling_n16,pairwise_n16,pilotCost_n16,random_n16 |
| `FSE5` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 442.5 | 0.697 | negligible (0.4917) | A12<0.5 means SRS risks tend to be lower; median SRS=0.029, median random=0.029 |
| `FSE6` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 426.5 | 0.879 | negligible (0.5261) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007357, median random=0.007185 |
| `FSE2` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.006885) | best size-normalized=diversity_n20; best cost-normalized=pairwise_n20 |
| `FSE3` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.04287) | best cost-normalized=pairwise_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n20; empirical front=balanced_n20,diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 439 | 0.736 | negligible (0.5122) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03825, median random=0.037 |
| `FSE6` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 443.5 | 0.686 | negligible (0.4928) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009488, median random=0.009488 |
| `FSE2` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.001524) | best size-normalized=diversity_n32; best cost-normalized=pairwise_n32 |
| `FSE3` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.03357) | best cost-normalized=pairwise_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n32; empirical front=balanced_n32,diversity_n32,pairwise_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 359 | 0.398 | small (0.6011) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03175, median random=0.02 |
| `FSE6` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 376 | 0.552 | small (0.5822) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01591, median random=0.0148 |
| `FSE2` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.004594) | best size-normalized=diversity_n40; best cost-normalized=pairwise_n40 |
| `FSE3` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.02171) | best cost-normalized=pairwise_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n40; empirical front=balanced_n40,diversity_n40,pairwise_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 423.5 | 0.914 | negligible (0.5294) | A12<0.5 means SRS risks tend to be lower; median SRS=0.024, median random=0.015 |
| `FSE6` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 439 | 0.736 | negligible (0.5122) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01977, median random=0.01999 |
| `FSE2` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.001078) | best size-normalized=diversity_n64; best cost-normalized=pairwise_n64 |
| `FSE3` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.0135) | best cost-normalized=pairwise_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n64; empirical front=balanced_n64,diversity_n64,pairwise_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 417 | 0.991 | negligible (0.4633) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0085, median random=0.0145 |
| `FSE6` | `lcbench__workload_shuttle__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 407 | 0.892 | negligible (0.4522) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03203, median random=0.0315 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003725 | 0.08875 | 0.8921 | -0.007933 | -0.002108 |
| `balanced_n8` | 8 | 0.004 | 0.004065 | 0.06575 | 0.9294 | 0.0294 | 0.02812 |
| `diversity_n8` | 8 | 0.004 | 0.005078 | 0.306 | 0.694 | -0.206 | -0.2237 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003647 | 0.0915 | 0.8907 | -0.009267 | -0.001661 |
| `pairwise_n8` | 8 | 0.004 | 0.004148 | 0.0035 | 0.9965 | 0.0965 | 0.09363 |
| `pilotCost_n8` | 8 | 0.004 | 0.0025 | 0.3938 | 0.6607 | -0.2393 | -0.1965 |
| `random_n16` | 16 | 0.008 | 0.007185 | 0.029 | 0.959 | 0.01454 | 0.02007 |
| `balanced_n16` | 16 | 0.008 | 0.00727 | 0.057 | 0.9474 | 0.002956 | 0.007863 |
| `diversity_n16` | 16 | 0.008 | 0.008171 | 0.018 | 0.982 | 0.03756 | 0.03652 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007357 | 0.029 | 0.9598 | 0.01537 | 0.01965 |
| `pairwise_n16` | 16 | 0.008 | 0.007767 | 0.0035 | 0.9965 | 0.05206 | 0.05353 |
| `pilotCost_n16` | 16 | 0.008 | 0.004943 | 0.3073 | 0.7371 | -0.2073 | -0.1787 |
| `random_n20` | 20 | 0.01 | 0.009488 | 0.037 | 0.955 | 0.0004212 | 0.002638 |
| `balanced_n20` | 20 | 0.01 | 0.008795 | 0.05075 | 0.9545 | -4.545e-05 | 0.005547 |
| `diversity_n20` | 20 | 0.01 | 0.01192 | 0.001 | 0.999 | 0.04445 | 0.03769 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009488 | 0.03825 | 0.954 | -0.0005121 | 0.001705 |
| `pairwise_n20` | 20 | 0.01 | 0.0094 | 0.0035 | 0.9965 | 0.04195 | 0.04458 |
| `pilotCost_n20` | 20 | 0.01 | 0.006157 | 0.05675 | 0.8176 | -0.1369 | -0.1125 |
| `random_n32` | 32 | 0.016 | 0.0148 | 0.02 | 0.9739 | 0.003362 | 0.005604 |
| `balanced_n32` | 32 | 0.016 | 0.01351 | 0.0155 | 0.9747 | 0.004095 | 0.009145 |
| `diversity_n32` | 32 | 0.016 | 0.018 | 0.001 | 0.999 | 0.02841 | 0.02531 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01591 | 0.03175 | 0.9637 | -0.006888 | -0.006732 |
| `pairwise_n32` | 32 | 0.016 | 0.01548 | 0.0035 | 0.9965 | 0.02591 | 0.02684 |
| `pilotCost_n32` | 32 | 0.016 | 0.009563 | 0.08825 | 0.8095 | -0.1611 | -0.1431 |
| `random_n40` | 40 | 0.02 | 0.01999 | 0.015 | 0.9758 | -0.0004238 | -0.0004121 |
| `balanced_n40` | 40 | 0.02 | 0.01645 | 0.01175 | 0.9827 | 0.00646 | 0.0113 |
| `diversity_n40` | 40 | 0.02 | 0.02618 | 0.001 | 0.999 | 0.02281 | 0.0174 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01977 | 0.024 | 0.9762 | 9.524e-06 | 0.0002774 |
| `pairwise_n40` | 40 | 0.02 | 0.01862 | 0.0035 | 0.9965 | 0.02031 | 0.02199 |
| `pilotCost_n40` | 40 | 0.02 | 0.0118 | 0.0735 | 0.8357 | -0.1405 | -0.1252 |
| `random_n64` | 64 | 0.032 | 0.0315 | 0.0145 | 0.9829 | -0.001982 | -0.00175 |
| `balanced_n64` | 64 | 0.032 | 0.02613 | 0.0045 | 0.9923 | 0.007452 | 0.01073 |
| `diversity_n64` | 64 | 0.032 | 0.03766 | 0.001 | 0.999 | 0.01415 | 0.01193 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03203 | 0.0085 | 0.9844 | -0.0004818 | -0.0004941 |
| `pairwise_n64` | 64 | 0.032 | 0.02928 | 0.0035 | 0.9965 | 0.01165 | 0.01301 |
| `pilotCost_n64` | 64 | 0.032 | 0.01923 | 0.011 | 0.962 | -0.02285 | -0.01328 |
