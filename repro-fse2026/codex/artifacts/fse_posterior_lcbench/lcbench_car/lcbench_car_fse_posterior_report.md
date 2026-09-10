# lcbench__workload_car__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n20` (risk 0, %cost 0.01283).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pairwise_n8` (omega_cost 0.08873, %cost 0.003416).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9534, risk 0.0215, %cost 0.002767, omega_cost 0.08615
- `pairwise_n8`: posterior area 0.9755, risk 0.0245, %cost 0.003416, omega_cost 0.08873
- `cheapOracle_n8`: posterior area 0.886, risk 0.114, %cost 0.001965, omega_cost 0.05461
- `diversity_n16`: posterior area 0.996, risk 0.004, %cost 0.008129, omega_cost 0.05077
- `pairwise_n16`: posterior area 0.982, risk 0.018, %cost 0.007506, omega_cost 0.04078
- `diversity_n20`: posterior area 1, risk 0, %cost 0.01283, omega_cost 0.03615

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n8` | `supports` | 30.21 | 8.68e-05 | large (0.2001) | median risks: random=0.0865, balanced=0.0215, diversity=0.0655, SRSSampling=0.08375, pairwise=0.0245, pilotCost=0.275, cheapOracle=0.114, expensiveOracle=0.003; spread=0.272 |
| `FSE1` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n16` | `supports` | 35.49 | 9.06e-06 | large (0.2456) | median risks: random=0.05075, balanced=0.01925, diversity=0.004, SRSSampling=0.05075, pairwise=0.018, pilotCost=0.186, cheapOracle=0.114, expensiveOracle=0.003; spread=0.183 |
| `FSE1` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n20` | `supports` | 15.43 | 0.0308 | large (0.0727) | median risks: random=0.039, balanced=0.0215, diversity=0, SRSSampling=0.039, pairwise=0.018, pilotCost=0.08725, cheapOracle=0.114, expensiveOracle=0.003; spread=0.114 |
| `FSE1` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n32` | `supports` | 16.29 | 0.0226 | large (0.08004) | median risks: random=0.023, balanced=0.01175, diversity=0, SRSSampling=0.0215, pairwise=0.018, pilotCost=0.03925, cheapOracle=0.114, expensiveOracle=0.003; spread=0.114 |
| `FSE1` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n40` | `supports` | 22.93 | 0.00175 | large (0.1374) | median risks: random=0.018, balanced=0.0155, diversity=0, SRSSampling=0.0175, pairwise=0.018, pilotCost=0.05975, cheapOracle=0.114, expensiveOracle=0.003; spread=0.114 |
| `FSE1` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n64` | `supports` | 21.24 | 0.00343 | large (0.1228) | median risks: random=0.00775, balanced=0.00625, diversity=0, SRSSampling=0.009, pairwise=0.018, pilotCost=0.01475, cheapOracle=0.103, expensiveOracle=0.003; spread=0.103 |
| `FSE2` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.075) | best size-normalized=expensiveOracle_n8; best cost-normalized=pairwise_n8 |
| `FSE3` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.09446) | best cost-normalized=pairwise_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.25 |  | large frontier change (3) | count front=expensiveOracle_n8; empirical front=balanced_n8,cheapOracle_n8,expensiveOracle_n8,pairwise_n8 |
| `FSE5` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 432.5 | 0.81 | negligible (0.4806) | A12<0.5 means SRS risks tend to be lower; median SRS=0.08375, median random=0.0865 |
| `FSE6` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 441.5 | 0.708 | negligible (0.4906) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003754, median random=0.003846 |
| `FSE2` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.04704) | best size-normalized=expensiveOracle_n16; best cost-normalized=balanced_n16 |
| `FSE3` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.06622) | best cost-normalized=balanced_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.2 |  | large frontier change (4) | count front=expensiveOracle_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16,expensiveOracle_n16,pairwise_n16 |
| `FSE5` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 449.5 | 0.622 | negligible (0.4994) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05075, median random=0.05075 |
| `FSE6` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 436.5 | 0.764 | negligible (0.515) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007745, median random=0.007684 |
| `FSE2` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n20; best cost-normalized=diversity_n20 |
| `FSE3` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.04932) | best cost-normalized=diversity_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n20; empirical front=balanced_n20,cheapOracle_n20,diversity_n20,pairwise_n20 |
| `FSE5` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 438 | 0.747 | negligible (0.5133) | A12<0.5 means SRS risks tend to be lower; median SRS=0.039, median random=0.039 |
| `FSE6` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 448.5 | 0.633 | negligible (0.4983) | A12>0.5 means SRS costs tend to be higher; median SRS=0.00973, median random=0.00973 |
| `FSE2` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02483) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n32; empirical front=balanced_n32,cheapOracle_n32,diversity_n32,pairwise_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 438.5 | 0.742 | negligible (0.4872) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0215, median random=0.023 |
| `FSE6` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 383 | 0.624 | small (0.5744) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01616, median random=0.0151 |
| `FSE2` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n40; best cost-normalized=diversity_n40 |
| `FSE3` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.01184) | best cost-normalized=diversity_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n40; empirical front=balanced_n40,cheapOracle_n40,diversity_n40,pairwise_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 424.5 | 0.903 | negligible (0.4717) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0175, median random=0.018 |
| `FSE6` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 449 | 0.628 | negligible (0.5011) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01984, median random=0.01979 |
| `FSE2` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n64; best cost-normalized=diversity_n64 |
| `FSE3` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | moderate (0.00967) | best cost-normalized=diversity_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n64; empirical front=balanced_n64,cheapOracle_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 429.5 | 0.844 | negligible (0.5228) | A12<0.5 means SRS risks tend to be lower; median SRS=0.009, median random=0.00775 |
| `FSE6` | `lcbench__workload_car__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 429 | 0.85 | negligible (0.5233) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03301, median random=0.0324 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003846 | 0.0865 | 0.885 | -0.01505 | -0.01186 |
| `balanced_n8` | 8 | 0.004 | 0.002767 | 0.0215 | 0.9534 | 0.05343 | 0.08615 |
| `diversity_n8` | 8 | 0.004 | 0.005248 | 0.0655 | 0.9345 | 0.0345 | 0.01453 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003754 | 0.08375 | 0.8891 | -0.0109 | -0.005733 |
| `pairwise_n8` | 8 | 0.004 | 0.003416 | 0.0245 | 0.9755 | 0.0755 | 0.08873 |
| `pilotCost_n8` | 8 | 0.004 | 0.002386 | 0.275 | 0.7516 | -0.1484 | -0.1007 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001965 | 0.114 | 0.886 | -0.014 | 0.05461 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.02889 | 0.003 | 0.997 | 0.097 | 0.01373 |
| `random_n16` | 16 | 0.008 | 0.007684 | 0.05075 | 0.9286 | -0.01581 | -0.01379 |
| `balanced_n16` | 16 | 0.008 | 0.005367 | 0.01925 | 0.9745 | 0.03006 | 0.05303 |
| `diversity_n16` | 16 | 0.008 | 0.008129 | 0.004 | 0.996 | 0.05156 | 0.05077 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007745 | 0.05075 | 0.9296 | -0.01481 | -0.01319 |
| `pairwise_n16` | 16 | 0.008 | 0.007506 | 0.018 | 0.982 | 0.03756 | 0.04078 |
| `pilotCost_n16` | 16 | 0.008 | 0.004808 | 0.186 | 0.8201 | -0.1244 | -0.09383 |
| `cheapOracle_n16` | 16 | 0.008 | 0.004068 | 0.114 | 0.886 | -0.05844 | -0.01534 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.05466 | 0.003 | 0.997 | 0.05256 | 0.005984 |
| `random_n20` | 20 | 0.01 | 0.00973 | 0.039 | 0.9411 | -0.01341 | -0.01227 |
| `balanced_n20` | 20 | 0.01 | 0.006582 | 0.0215 | 0.9524 | -0.002179 | 0.01831 |
| `diversity_n20` | 20 | 0.01 | 0.01283 | 0 | 1 | 0.04545 | 0.03615 |
| `SRSSampling_n20` | 20 | 0.01 | 0.00973 | 0.039 | 0.9402 | -0.01431 | -0.01317 |
| `pairwise_n20` | 20 | 0.01 | 0.009162 | 0.018 | 0.982 | 0.02745 | 0.0312 |
| `pilotCost_n20` | 20 | 0.01 | 0.006028 | 0.08725 | 0.8531 | -0.1015 | -0.07578 |
| `cheapOracle_n20` | 20 | 0.01 | 0.005147 | 0.114 | 0.886 | -0.06855 | -0.03265 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.06637 | 0.003 | 0.997 | 0.04245 | 0.004421 |
| `random_n32` | 32 | 0.016 | 0.0151 | 0.023 | 0.9695 | -0.001055 | 0.0005802 |
| `balanced_n32` | 32 | 0.016 | 0.01056 | 0.01175 | 0.9719 | 0.001312 | 0.01517 |
| `diversity_n32` | 32 | 0.016 | 0.02007 | 0 | 1 | 0.02941 | 0.02373 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01616 | 0.0215 | 0.9698 | -0.0008216 | -0.001102 |
| `pairwise_n32` | 32 | 0.016 | 0.01528 | 0.018 | 0.982 | 0.01141 | 0.01271 |
| `pilotCost_n32` | 32 | 0.016 | 0.009646 | 0.03925 | 0.9208 | -0.04977 | -0.03222 |
| `cheapOracle_n32` | 32 | 0.016 | 0.008426 | 0.114 | 0.886 | -0.08459 | -0.06096 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.0973 | 0.003 | 0.997 | 0.02641 | 0.002087 |
| `random_n40` | 40 | 0.02 | 0.01979 | 0.018 | 0.9741 | -0.00204 | -0.001799 |
| `balanced_n40` | 40 | 0.02 | 0.01357 | 0.0155 | 0.9761 | -7.381e-05 | 0.01042 |
| `diversity_n40` | 40 | 0.02 | 0.02972 | 0 | 1 | 0.02381 | 0.01628 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01984 | 0.0175 | 0.9805 | 0.00426 | 0.00444 |
| `pairwise_n40` | 40 | 0.02 | 0.01862 | 0.018 | 0.982 | 0.00581 | 0.007482 |
| `pilotCost_n40` | 40 | 0.02 | 0.01201 | 0.05975 | 0.9061 | -0.07012 | -0.05549 |
| `cheapOracle_n40` | 40 | 0.02 | 0.01064 | 0.114 | 0.886 | -0.09019 | -0.07104 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.1152 | 0.003 | 0.997 | 0.02081 | 0.001302 |
| `random_n64` | 64 | 0.032 | 0.0324 | 0.00775 | 0.9865 | 0.001602 | 0.001422 |
| `balanced_n64` | 64 | 0.032 | 0.02261 | 0.00625 | 0.9887 | 0.003885 | 0.009907 |
| `diversity_n64` | 64 | 0.032 | 0.04117 | 0 | 1 | 0.01515 | 0.01186 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03301 | 0.009 | 0.9875 | 0.002635 | 0.002185 |
| `pairwise_n64` | 64 | 0.032 | 0.03043 | 0.018 | 0.982 | -0.002848 | -0.002094 |
| `pilotCost_n64` | 64 | 0.032 | 0.0192 | 0.01475 | 0.9758 | -0.009082 | 0.0005146 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01734 | 0.103 | 0.897 | -0.08785 | -0.07574 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.165 | 0.003 | 0.997 | 0.01215 | 1.213e-05 |
