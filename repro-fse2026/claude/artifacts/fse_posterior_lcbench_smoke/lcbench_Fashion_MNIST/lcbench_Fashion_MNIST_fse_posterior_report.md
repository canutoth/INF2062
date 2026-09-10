# lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n8` (risk 0.0025, %cost 0.003493).

Best integrated confidence after normalizing the prior baseline by empirical cost: `cheapOracle_n8` (omega_cost 0.1224, %cost 0.000958).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.9975, risk 0.0025, %cost 0.003493, omega_cost 0.1088
- `cheapOracle_n8`: posterior area 0.867, risk 0.133, %cost 0.000958, omega_cost 0.1224
- `pilotCost_n16`: posterior area 0.9135, risk 0.0825, %cost 0.002178, omega_cost 0.07081
- `cheapOracle_n16`: posterior area 0.871, risk 0.129, %cost 0.001936, omega_cost 0.04131

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n8` | `inconclusive` | 9.486 | 0.22 | large (0.06905) | median risks: random=0.07025, balanced=0.07175, diversity=0.0025, SRSSampling=0.07025, pairwise=0.0395, pilotCost=0.096, cheapOracle=0.133, expensiveOracle=0.007; spread=0.1305 |
| `FSE1` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n16` | `inconclusive` | 12 | 0.101 | large (0.1389) | median risks: random=0.0455, balanced=0.04825, diversity=0.0025, SRSSampling=0.03875, pairwise=0.0395, pilotCost=0.0825, cheapOracle=0.129, expensiveOracle=0.007; spread=0.1265 |
| `FSE2` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.01357) | best size-normalized=diversity_n8; best cost-normalized=cheapOracle_n8 |
| `FSE3` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.1314) | best cost-normalized=cheapOracle_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n8; empirical front=cheapOracle_n8,diversity_n8 |
| `FSE5` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 48.5 | 0.699 | negligible (0.485) | A12<0.5 means SRS risks tend to be lower; median SRS=0.07025, median random=0.07025 |
| `FSE6` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 45.5 | 0.874 | negligible (0.455) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0041, median random=0.004255 |
| `FSE2` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.01314) | best size-normalized=diversity_n16; best cost-normalized=pilotCost_n16 |
| `FSE3` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.0806) | best cost-normalized=pilotCost_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n16; empirical front=cheapOracle_n16,diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 45.5 | 0.874 | negligible (0.455) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03875, median random=0.0455 |
| `FSE6` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 47.5 | 0.756 | negligible (0.525) | A12>0.5 means SRS costs tend to be higher; median SRS=0.008057, median random=0.008004 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.004255 | 0.07025 | 0.8812 | -0.0188 | -0.02365 |
| `balanced_n8` | 8 | 0.004 | 0.005417 | 0.07175 | 0.9103 | 0.01025 | -0.01184 |
| `diversity_n8` | 8 | 0.004 | 0.003493 | 0.0025 | 0.9975 | 0.0975 | 0.1088 |
| `SRSSampling_n8` | 8 | 0.004 | 0.0041 | 0.07025 | 0.893 | -0.00705 | -0.009018 |
| `pairwise_n8` | 8 | 0.004 | 0.004233 | 0.0395 | 0.9605 | 0.0605 | 0.05606 |
| `pilotCost_n8` | 8 | 0.004 | 0.001121 | 0.096 | 0.848 | -0.05195 | 0.08381 |
| `cheapOracle_n8` | 8 | 0.004 | 0.000958 | 0.133 | 0.867 | -0.033 | 0.1224 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.01531 | 0.007 | 0.993 | 0.093 | 0.02366 |
| `random_n16` | 16 | 0.008 | 0.008004 | 0.0455 | 0.9175 | -0.02694 | -0.02697 |
| `balanced_n16` | 16 | 0.008 | 0.009542 | 0.04825 | 0.955 | 0.01056 | 0.00243 |
| `diversity_n16` | 16 | 0.008 | 0.00731 | 0.0025 | 0.9975 | 0.05306 | 0.05767 |
| `SRSSampling_n16` | 16 | 0.008 | 0.008057 | 0.03875 | 0.935 | -0.009444 | -0.009794 |
| `pairwise_n16` | 16 | 0.008 | 0.007512 | 0.0395 | 0.9605 | 0.01606 | 0.01924 |
| `pilotCost_n16` | 16 | 0.008 | 0.002178 | 0.0825 | 0.9135 | -0.03094 | 0.07081 |
| `cheapOracle_n16` | 16 | 0.008 | 0.001936 | 0.129 | 0.871 | -0.07344 | 0.04131 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.02517 | 0.007 | 0.993 | 0.04856 | 0.0121 |
