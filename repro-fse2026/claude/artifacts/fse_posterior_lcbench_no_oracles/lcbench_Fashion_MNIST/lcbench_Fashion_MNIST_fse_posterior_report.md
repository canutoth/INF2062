# lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n8` (risk 0.0025, %cost 0.003493).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pilotCost_n8` (omega_cost 0.1229, %cost 0.00111).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.9975, risk 0.0025, %cost 0.003493, omega_cost 0.1088
- `pilotCost_n8`: posterior area 0.8859, risk 0.0935, %cost 0.00111, omega_cost 0.1229
- `pilotCost_n16`: posterior area 0.8981, risk 0.08425, %cost 0.002213, omega_cost 0.05371
- `pilotCost_n20`: posterior area 0.9321, risk 0.067, %cost 0.002831, omega_cost 0.06258

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 5.029 | 0.412 | large (0.0002524) | median risks: random=0.0825, balanced=0.07675, diversity=0.0025, SRSSampling=0.07325, pairwise=0.0395, pilotCost=0.0935; spread=0.091 |
| `FSE1` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n16` | `supports` | 27.49 | 4.57e-05 | large (0.1939) | median risks: random=0.03875, balanced=0.043, diversity=0.0025, SRSSampling=0.03875, pairwise=0.0395, pilotCost=0.08425; spread=0.08175 |
| `FSE1` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n20` | `inconclusive` | 9.246 | 0.0996 | large (0.0366) | median risks: random=0.04525, balanced=0.0325, diversity=0.0025, SRSSampling=0.046, pairwise=0.0395, pilotCost=0.067; spread=0.0645 |
| `FSE1` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n32` | `supports` | 36.29 | 8.31e-07 | large (0.2697) | median risks: random=0.02225, balanced=0.0275, diversity=0.0025, SRSSampling=0.0195, pairwise=0.0395, pilotCost=0.067; spread=0.0645 |
| `FSE1` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n40` | `supports` | 60.46 | 9.78e-12 | large (0.4781) | median risks: random=0.013, balanced=0.01, diversity=0.0025, SRSSampling=0.01875, pairwise=0.021, pilotCost=0.067; spread=0.0645 |
| `FSE1` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n64` | `supports` | 47.42 | 4.66e-09 | moderate (0.3657) | median risks: random=0.009, balanced=0.0025, diversity=0.0025, SRSSampling=0.01375, pairwise=0.021, pilotCost=0.0515; spread=0.049 |
| `FSE2` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.01409) | best size-normalized=diversity_n8; best cost-normalized=pilotCost_n8 |
| `FSE3` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.1306) | best cost-normalized=pilotCost_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n8; empirical front=diversity_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 427.5 | 0.867 | negligible (0.475) | A12<0.5 means SRS risks tend to be lower; median SRS=0.07325, median random=0.0825 |
| `FSE6` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 432.5 | 0.809 | negligible (0.4806) | A12>0.5 means SRS costs tend to be higher; median SRS=0.004096, median random=0.004124 |
| `FSE2` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.05142) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n16; empirical front=diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 441.5 | 0.708 | negligible (0.4906) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03875, median random=0.03875 |
| `FSE6` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 433.5 | 0.798 | negligible (0.5183) | A12>0.5 means SRS costs tend to be higher; median SRS=0.008248, median random=0.008162 |
| `FSE2` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.01826) | best size-normalized=diversity_n20; best cost-normalized=pilotCost_n20 |
| `FSE3` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.07238) | best cost-normalized=pilotCost_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n20; empirical front=diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 449.5 | 0.622 | negligible (0.5006) | A12<0.5 means SRS risks tend to be lower; median SRS=0.046, median random=0.04525 |
| `FSE6` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 442.5 | 0.697 | negligible (0.4917) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01007, median random=0.01009 |
| `FSE2` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.03141) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n32; empirical front=diversity_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 405.5 | 0.874 | negligible (0.4506) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0195, median random=0.02225 |
| `FSE6` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 324 | 0.173 | medium (0.64) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01655, median random=0.01539 |
| `FSE2` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n40; best cost-normalized=diversity_n40 |
| `FSE3` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.01893) | best cost-normalized=diversity_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n40; empirical front=diversity_n40,pairwise_n40,pilotCost_n40,random_n40 |
| `FSE5` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 439.5 | 0.73 | negligible (0.5117) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01875, median random=0.013 |
| `FSE6` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 393 | 0.732 | small (0.5633) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02097, median random=0.02039 |
| `FSE2` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n64; best cost-normalized=diversity_n64 |
| `FSE3` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01494) | best cost-normalized=diversity_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n64; empirical front=diversity_n64,pairwise_n64,pilotCost_n64,random_n64 |
| `FSE5` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 442.5 | 0.697 | negligible (0.5083) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01375, median random=0.009 |
| `FSE6` | `lcbench__workload_Fashion_MNIST__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 305 | 0.1 | medium (0.6611) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03404, median random=0.0316 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.004124 | 0.0825 | 0.8884 | -0.0116 | -0.01401 |
| `balanced_n8` | 8 | 0.004 | 0.005417 | 0.07675 | 0.8926 | -0.007367 | -0.02945 |
| `diversity_n8` | 8 | 0.004 | 0.003493 | 0.0025 | 0.9975 | 0.0975 | 0.1088 |
| `SRSSampling_n8` | 8 | 0.004 | 0.004096 | 0.07325 | 0.8942 | -0.0058 | -0.007692 |
| `pairwise_n8` | 8 | 0.004 | 0.004233 | 0.0395 | 0.9605 | 0.0605 | 0.05606 |
| `pilotCost_n8` | 8 | 0.004 | 0.00111 | 0.0935 | 0.8859 | -0.01407 | 0.1229 |
| `random_n16` | 16 | 0.008 | 0.008162 | 0.03875 | 0.9467 | 0.002272 | 0.00129 |
| `balanced_n16` | 16 | 0.008 | 0.009661 | 0.043 | 0.9551 | 0.01066 | 0.002002 |
| `diversity_n16` | 16 | 0.008 | 0.00731 | 0.0025 | 0.9975 | 0.05306 | 0.05767 |
| `SRSSampling_n16` | 16 | 0.008 | 0.008248 | 0.03875 | 0.9522 | 0.007739 | 0.00625 |
| `pairwise_n16` | 16 | 0.008 | 0.007512 | 0.0395 | 0.9605 | 0.01606 | 0.01924 |
| `pilotCost_n16` | 16 | 0.008 | 0.002213 | 0.08425 | 0.8981 | -0.04636 | 0.05371 |
| `random_n20` | 20 | 0.01 | 0.01009 | 0.04525 | 0.9451 | -0.009462 | -0.009818 |
| `balanced_n20` | 20 | 0.01 | 0.01186 | 0.0325 | 0.9595 | 0.004921 | -0.00165 |
| `diversity_n20` | 20 | 0.01 | 0.009679 | 0.0025 | 0.9975 | 0.04295 | 0.04432 |
| `SRSSampling_n20` | 20 | 0.01 | 0.01007 | 0.046 | 0.945 | -0.009512 | -0.009798 |
| `pairwise_n20` | 20 | 0.01 | 0.009591 | 0.0395 | 0.9605 | 0.005955 | 0.007712 |
| `pilotCost_n20` | 20 | 0.01 | 0.002831 | 0.067 | 0.9321 | -0.02248 | 0.06258 |
| `random_n32` | 32 | 0.016 | 0.01539 | 0.02225 | 0.9715 | 0.0009118 | 0.001999 |
| `balanced_n32` | 32 | 0.016 | 0.01767 | 0.0275 | 0.9757 | 0.005128 | 0.002503 |
| `diversity_n32` | 32 | 0.016 | 0.01517 | 0.0025 | 0.9975 | 0.02691 | 0.02842 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01655 | 0.0195 | 0.9685 | -0.002072 | -0.002992 |
| `pairwise_n32` | 32 | 0.016 | 0.01681 | 0.0395 | 0.9605 | -0.01009 | -0.01143 |
| `pilotCost_n32` | 32 | 0.016 | 0.004398 | 0.067 | 0.9329 | -0.03769 | 0.02553 |
| `random_n40` | 40 | 0.02 | 0.02039 | 0.013 | 0.9801 | 0.00396 | 0.003527 |
| `balanced_n40` | 40 | 0.02 | 0.02171 | 0.01 | 0.9862 | 0.01001 | 0.008218 |
| `diversity_n40` | 40 | 0.02 | 0.02042 | 0.0025 | 0.9975 | 0.02131 | 0.02084 |
| `SRSSampling_n40` | 40 | 0.02 | 0.02097 | 0.01875 | 0.9791 | 0.00296 | 0.001911 |
| `pairwise_n40` | 40 | 0.02 | 0.02027 | 0.021 | 0.979 | 0.00281 | 0.002508 |
| `pilotCost_n40` | 40 | 0.02 | 0.005496 | 0.067 | 0.9328 | -0.04337 | 0.009784 |
| `random_n64` | 64 | 0.032 | 0.0316 | 0.009 | 0.9849 | 1.818e-05 | 0.0002057 |
| `balanced_n64` | 64 | 0.032 | 0.03361 | 0.0025 | 0.9949 | 0.01002 | 0.009313 |
| `diversity_n64` | 64 | 0.032 | 0.03194 | 0.0025 | 0.9975 | 0.01265 | 0.01268 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03404 | 0.01375 | 0.9835 | -0.001382 | -0.002265 |
| `pairwise_n64` | 64 | 0.032 | 0.03115 | 0.021 | 0.979 | -0.005848 | -0.005446 |
| `pilotCost_n64` | 64 | 0.032 | 0.01027 | 0.0515 | 0.9587 | -0.0262 | 0.002997 |
