# lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `balanced_n64` (risk 0.002, %cost 0.02552).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n8` (omega_cost 0.07291, %cost 0.004854).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.9875, risk 0.0125, %cost 0.004854, omega_cost 0.07291
- `pilotCost_n8`: posterior area 0.9121, risk 0.08475, %cost 0.00229, omega_cost 0.06405
- `pilotCost_n16`: posterior area 0.9425, risk 0.0475, %cost 0.004552, omega_cost 0.03255
- `balanced_n40`: posterior area 0.9878, risk 0.003, %cost 0.01649, omega_cost 0.01641
- `balanced_n64`: posterior area 0.9948, risk 0.002, %cost 0.02552, omega_cost 0.01361

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 6.055 | 0.301 | large (0.009096) | median risks: random=0.0925, balanced=0.0735, diversity=0.0125, SRSSampling=0.0925, pairwise=0.0925, pilotCost=0.08475; spread=0.08 |
| `FSE1` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 2.99 | 0.701 | large (0) | median risks: random=0.057, balanced=0.05475, diversity=0.0125, SRSSampling=0.0615, pairwise=0.0925, pilotCost=0.0475; spread=0.08 |
| `FSE1` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 4.195 | 0.522 | moderate (0) | median risks: random=0.03525, balanced=0.0255, diversity=0.0125, SRSSampling=0.03525, pairwise=0.024, pilotCost=0.0385; spread=0.026 |
| `FSE1` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 4.294 | 0.508 | moderate (0) | median risks: random=0.02075, balanced=0.013, diversity=0.0125, SRSSampling=0.018, pairwise=0.024, pilotCost=0.03225; spread=0.01975 |
| `FSE1` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n40` | `supports` | 20.29 | 0.0011 | moderate (0.1318) | median risks: random=0.02025, balanced=0.003, diversity=0.0125, SRSSampling=0.0145, pairwise=0.024, pilotCost=0.03625; spread=0.03325 |
| `FSE1` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n64` | `supports` | 18.01 | 0.00294 | moderate (0.1121) | median risks: random=0.00775, balanced=0.002, diversity=0.0125, SRSSampling=0.0115, pairwise=0.024, pilotCost=0.0085; spread=0.022 |
| `FSE2` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n8; best cost-normalized=diversity_n8 |
| `FSE3` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.08606) | best cost-normalized=diversity_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n8; empirical front=diversity_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 446.5 | 0.654 | negligible (0.4961) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0925, median random=0.0925 |
| `FSE6` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 434.5 | 0.787 | negligible (0.4828) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003468, median random=0.003494 |
| `FSE2` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.04906) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n16; empirical front=diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 435 | 0.781 | negligible (0.5167) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0615, median random=0.057 |
| `FSE6` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 430.5 | 0.832 | negligible (0.5217) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007264, median random=0.007127 |
| `FSE2` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.01423) | best size-normalized=diversity_n20; best cost-normalized=pairwise_n20 |
| `FSE3` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.02519) | best cost-normalized=pairwise_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n20; empirical front=diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 445.5 | 0.665 | negligible (0.495) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03525, median random=0.03525 |
| `FSE6` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 436.5 | 0.764 | negligible (0.485) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009077, median random=0.009204 |
| `FSE2` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.008511) | best size-normalized=diversity_n32; best cost-normalized=pilotCost_n32 |
| `FSE3` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.01329) | best cost-normalized=pilotCost_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n32; empirical front=balanced_n32,diversity_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 437.5 | 0.753 | negligible (0.4861) | A12<0.5 means SRS risks tend to be lower; median SRS=0.018, median random=0.02075 |
| `FSE6` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 447 | 0.649 | negligible (0.5033) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01517, median random=0.01497 |
| `FSE2` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | unchanged (0) | best size-normalized=balanced_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | moderate (0.009791) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.5 |  | frontier change (1) | count front=balanced_n40; empirical front=balanced_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 368 | 0.476 | small (0.4089) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0145, median random=0.02025 |
| `FSE6` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 344 | 0.286 | small (0.3822) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01815, median random=0.01958 |
| `FSE2` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | unchanged (0) | best size-normalized=balanced_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01329) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.5 |  | frontier change (1) | count front=balanced_n64; empirical front=balanced_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 409 | 0.915 | negligible (0.5456) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0115, median random=0.00775 |
| `FSE6` | `lcbench__workload_numerai28_6__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 324 | 0.173 | medium (0.36) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03081, median random=0.03344 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003494 | 0.0925 | 0.8739 | -0.02612 | -0.01485 |
| `balanced_n8` | 8 | 0.004 | 0.004475 | 0.0735 | 0.9075 | 0.007467 | -0.001213 |
| `diversity_n8` | 8 | 0.004 | 0.004854 | 0.0125 | 0.9875 | 0.0875 | 0.07291 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003468 | 0.0925 | 0.8749 | -0.02507 | -0.01315 |
| `pairwise_n8` | 8 | 0.004 | 0.00371 | 0.0925 | 0.9075 | 0.0075 | 0.01366 |
| `pilotCost_n8` | 8 | 0.004 | 0.00229 | 0.08475 | 0.9121 | 0.01207 | 0.06405 |
| `random_n16` | 16 | 0.008 | 0.007127 | 0.057 | 0.9379 | -0.006511 | -0.0005406 |
| `balanced_n16` | 16 | 0.008 | 0.007607 | 0.05475 | 0.9362 | -0.008228 | -0.005694 |
| `diversity_n16` | 16 | 0.008 | 0.007781 | 0.0125 | 0.9875 | 0.04306 | 0.04444 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007264 | 0.0615 | 0.9349 | -0.009561 | -0.004616 |
| `pairwise_n16` | 16 | 0.008 | 0.006971 | 0.0925 | 0.9075 | -0.03694 | -0.02977 |
| `pilotCost_n16` | 16 | 0.008 | 0.004552 | 0.0475 | 0.9425 | -0.001944 | 0.03255 |
| `random_n20` | 20 | 0.01 | 0.009204 | 0.03525 | 0.9534 | -0.001179 | 0.002368 |
| `balanced_n20` | 20 | 0.01 | 0.008885 | 0.0255 | 0.9635 | 0.008955 | 0.01408 |
| `diversity_n20` | 20 | 0.01 | 0.01778 | 0.0125 | 0.9875 | 0.03295 | 0.01413 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009077 | 0.03525 | 0.9536 | -0.0009955 | 0.003166 |
| `pairwise_n20` | 20 | 0.01 | 0.00855 | 0.024 | 0.976 | 0.02145 | 0.02836 |
| `pilotCost_n20` | 20 | 0.01 | 0.005913 | 0.0385 | 0.9558 | 0.001305 | 0.02817 |
| `random_n32` | 32 | 0.016 | 0.01497 | 0.02075 | 0.9692 | -0.001372 | 0.0005183 |
| `balanced_n32` | 32 | 0.016 | 0.01363 | 0.013 | 0.9775 | 0.006895 | 0.01165 |
| `diversity_n32` | 32 | 0.016 | 0.02322 | 0.0125 | 0.9875 | 0.01691 | 0.008144 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01517 | 0.018 | 0.9724 | 0.001845 | 0.003362 |
| `pairwise_n32` | 32 | 0.016 | 0.01433 | 0.024 | 0.976 | 0.005412 | 0.008617 |
| `pilotCost_n32` | 32 | 0.016 | 0.008867 | 0.03225 | 0.966 | -0.004605 | 0.01665 |
| `random_n40` | 40 | 0.02 | 0.01958 | 0.02025 | 0.9702 | -0.00599 | -0.00551 |
| `balanced_n40` | 40 | 0.02 | 0.01649 | 0.003 | 0.9878 | 0.01163 | 0.01641 |
| `diversity_n40` | 40 | 0.02 | 0.04125 | 0.0125 | 0.9875 | 0.01131 | -0.0006648 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01815 | 0.0145 | 0.9805 | 0.004326 | 0.00662 |
| `pairwise_n40` | 40 | 0.02 | 0.01859 | 0.024 | 0.976 | -0.0001905 | 0.001525 |
| `pilotCost_n40` | 40 | 0.02 | 0.01089 | 0.03625 | 0.9671 | -0.009074 | 0.009177 |
| `random_n64` | 64 | 0.032 | 0.03344 | 0.00775 | 0.9884 | 0.003535 | 0.0029 |
| `balanced_n64` | 64 | 0.032 | 0.02552 | 0.002 | 0.9948 | 0.009902 | 0.01361 |
| `diversity_n64` | 64 | 0.032 | 0.05371 | 0.0125 | 0.9875 | 0.002652 | -0.003362 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03081 | 0.0115 | 0.9846 | -0.0002485 | 0.0003191 |
| `pairwise_n64` | 64 | 0.032 | 0.02829 | 0.024 | 0.976 | -0.008848 | -0.00693 |
| `pilotCost_n64` | 64 | 0.032 | 0.01782 | 0.0085 | 0.9851 | 0.0002182 | 0.01164 |
