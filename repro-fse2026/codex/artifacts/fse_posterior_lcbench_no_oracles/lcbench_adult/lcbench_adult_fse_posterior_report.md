# lcbench__workload_adult__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n64` (risk 0, %cost 0.03611).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n8` (omega_cost 0.07718, %cost 0.004575).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.9875, risk 0.0125, %cost 0.004575, omega_cost 0.07718
- `pairwise_n8`: posterior area 0.949, risk 0.051, %cost 0.003057, omega_cost 0.07223
- `pilotCost_n8`: posterior area 0.8776, risk 0.0775, %cost 0.002338, omega_cost 0.02742
- `balanced_n64`: posterior area 0.9915, risk 0.0085, %cost 0.02521, omega_cost 0.01056
- `diversity_n64`: posterior area 1, risk 0, %cost 0.03611, omega_cost 0.01347

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 5.506 | 0.357 | large (0.004363) | median risks: random=0.0855, balanced=0.067, diversity=0.0125, SRSSampling=0.08275, pairwise=0.051, pilotCost=0.0775; spread=0.073 |
| `FSE1` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n16` | `supports` | 11.6 | 0.0407 | moderate (0.0569) | median risks: random=0.0455, balanced=0.02425, diversity=0.0125, SRSSampling=0.0455, pairwise=0.051, pilotCost=0.042; spread=0.0385 |
| `FSE1` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n20` | `inconclusive` | 6.675 | 0.246 | moderate (0.01444) | median risks: random=0.037, balanced=0.01475, diversity=0.0125, SRSSampling=0.037, pairwise=0.051, pilotCost=0.014; spread=0.0385 |
| `FSE1` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n32` | `supports` | 15.63 | 0.008 | moderate (0.0916) | median risks: random=0.02525, balanced=0.014, diversity=0.0125, SRSSampling=0.01975, pairwise=0.0435, pilotCost=0.038; spread=0.031 |
| `FSE1` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n40` | `supports` | 13.47 | 0.0194 | moderate (0.07299) | median risks: random=0.01325, balanced=0.0085, diversity=0.0125, SRSSampling=0.01875, pairwise=0.0435, pilotCost=0.02125; spread=0.035 |
| `FSE1` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n64` | `supports` | 13.42 | 0.0197 | moderate (0.07263) | median risks: random=0.01, balanced=0.0085, diversity=0, SRSSampling=0.00975, pairwise=0.0435, pilotCost=0.0125; spread=0.0435 |
| `FSE2` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n8; best cost-normalized=diversity_n8 |
| `FSE3` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.05967) | best cost-normalized=diversity_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n8; empirical front=diversity_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 427.5 | 0.867 | negligible (0.475) | A12<0.5 means SRS risks tend to be lower; median SRS=0.08275, median random=0.0855 |
| `FSE6` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 436.5 | 0.764 | negligible (0.485) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003636, median random=0.003819 |
| `FSE2` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.05639) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n16; empirical front=balanced_n16,diversity_n16,pairwise_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 445 | 0.67 | negligible (0.4944) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0455, median random=0.0455 |
| `FSE6` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 430.5 | 0.832 | negligible (0.5217) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007315, median random=0.007036 |
| `FSE2` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.003033) | best size-normalized=diversity_n20; best cost-normalized=pilotCost_n20 |
| `FSE3` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.03028) | best cost-normalized=pilotCost_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n20; empirical front=balanced_n20,diversity_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 446 | 0.659 | negligible (0.5044) | A12<0.5 means SRS risks tend to be lower; median SRS=0.037, median random=0.037 |
| `FSE6` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 442.5 | 0.697 | negligible (0.4917) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009297, median random=0.009297 |
| `FSE2` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.002821) | best size-normalized=diversity_n32; best cost-normalized=balanced_n32 |
| `FSE3` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02875) | best cost-normalized=balanced_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n32; empirical front=balanced_n32,diversity_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 416 | 0.998 | negligible (0.5378) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01975, median random=0.02525 |
| `FSE6` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 381 | 0.603 | small (0.5767) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01587, median random=0.01458 |
| `FSE2` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.009762) | best size-normalized=diversity_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.01867) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n40; empirical front=balanced_n40,diversity_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 360 | 0.406 | small (0.6) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01875, median random=0.01325 |
| `FSE6` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 425 | 0.896 | negligible (0.4722) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01946, median random=0.01995 |
| `FSE2` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n64; best cost-normalized=diversity_n64 |
| `FSE3` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01013) | best cost-normalized=diversity_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n64; empirical front=balanced_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 420 | 0.955 | negligible (0.4667) | A12<0.5 means SRS risks tend to be lower; median SRS=0.00975, median random=0.01 |
| `FSE6` | `lcbench__workload_adult__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 449 | 0.628 | negligible (0.5011) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03217, median random=0.03192 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003819 | 0.0855 | 0.9038 | 0.003833 | 0.007585 |
| `balanced_n8` | 8 | 0.004 | 0.004109 | 0.067 | 0.9201 | 0.0201 | 0.01796 |
| `diversity_n8` | 8 | 0.004 | 0.004575 | 0.0125 | 0.9875 | 0.0875 | 0.07718 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003636 | 0.08275 | 0.9097 | 0.009667 | 0.01751 |
| `pairwise_n8` | 8 | 0.004 | 0.003057 | 0.051 | 0.949 | 0.049 | 0.07223 |
| `pilotCost_n8` | 8 | 0.004 | 0.002338 | 0.0775 | 0.8776 | -0.02238 | 0.02742 |
| `random_n16` | 16 | 0.008 | 0.007036 | 0.0455 | 0.9256 | -0.01879 | -0.01213 |
| `balanced_n16` | 16 | 0.008 | 0.0071 | 0.02425 | 0.9633 | 0.01882 | 0.02499 |
| `diversity_n16` | 16 | 0.008 | 0.007625 | 0.0125 | 0.9875 | 0.04306 | 0.04547 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007315 | 0.0455 | 0.9289 | -0.01549 | -0.01092 |
| `pairwise_n16` | 16 | 0.008 | 0.00661 | 0.051 | 0.949 | 0.004556 | 0.01471 |
| `pilotCost_n16` | 16 | 0.008 | 0.004667 | 0.042 | 0.9102 | -0.03421 | -0.001544 |
| `random_n20` | 20 | 0.01 | 0.009297 | 0.037 | 0.9528 | -0.001745 | 0.001356 |
| `balanced_n20` | 20 | 0.01 | 0.008565 | 0.01475 | 0.9747 | 0.02014 | 0.02696 |
| `diversity_n20` | 20 | 0.01 | 0.0114 | 0.0125 | 0.9875 | 0.03295 | 0.02781 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009297 | 0.037 | 0.952 | -0.002545 | 0.0005563 |
| `pairwise_n20` | 20 | 0.01 | 0.008328 | 0.051 | 0.949 | -0.005545 | 0.002602 |
| `pilotCost_n20` | 20 | 0.01 | 0.006202 | 0.014 | 0.9614 | 0.006871 | 0.03084 |
| `random_n32` | 32 | 0.016 | 0.01458 | 0.02525 | 0.9707 | 0.0001118 | 0.002802 |
| `balanced_n32` | 32 | 0.016 | 0.01301 | 0.014 | 0.9816 | 0.01103 | 0.01731 |
| `diversity_n32` | 32 | 0.016 | 0.01752 | 0.0125 | 0.9875 | 0.01691 | 0.01449 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01587 | 0.01975 | 0.9589 | -0.01165 | -0.01143 |
| `pairwise_n32` | 32 | 0.016 | 0.01448 | 0.0435 | 0.9565 | -0.01409 | -0.0112 |
| `pilotCost_n32` | 32 | 0.016 | 0.009277 | 0.038 | 0.95 | -0.02055 | -0.001315 |
| `random_n40` | 40 | 0.02 | 0.01995 | 0.01325 | 0.9803 | 0.004093 | 0.004145 |
| `balanced_n40` | 40 | 0.02 | 0.01595 | 0.0085 | 0.9868 | 0.01063 | 0.01631 |
| `diversity_n40` | 40 | 0.02 | 0.02525 | 0.0125 | 0.9875 | 0.01131 | 0.006545 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01946 | 0.01875 | 0.9732 | -0.00299 | -0.002366 |
| `pairwise_n40` | 40 | 0.02 | 0.01756 | 0.0435 | 0.9565 | -0.01969 | -0.01656 |
| `pilotCost_n40` | 40 | 0.02 | 0.01145 | 0.02125 | 0.9703 | -0.005907 | 0.01043 |
| `random_n64` | 64 | 0.032 | 0.03192 | 0.01 | 0.9813 | -0.003582 | -0.003545 |
| `balanced_n64` | 64 | 0.032 | 0.02521 | 0.0085 | 0.9915 | 0.006635 | 0.01056 |
| `diversity_n64` | 64 | 0.032 | 0.03611 | 0 | 1 | 0.01515 | 0.01347 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03217 | 0.00975 | 0.9883 | 0.003418 | 0.003338 |
| `pairwise_n64` | 64 | 0.032 | 0.02854 | 0.0435 | 0.9565 | -0.02835 | -0.02657 |
| `pilotCost_n64` | 64 | 0.032 | 0.01885 | 0.0125 | 0.9811 | -0.003698 | 0.006335 |
