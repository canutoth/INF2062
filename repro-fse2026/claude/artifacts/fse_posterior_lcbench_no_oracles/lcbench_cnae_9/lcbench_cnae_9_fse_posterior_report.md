# lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n20` (risk 0, %cost 0.009636).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pilotCost_n8` (omega_cost 0.3044, %cost 0.0004221).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.987, risk 0.013, %cost 0.00366, omega_cost 0.0943
- `pilotCost_n8`: posterior area 0.9528, risk 0.026, %cost 0.0004221, omega_cost 0.3044
- `pilotCost_n16`: posterior area 0.964, risk 0.026, %cost 0.0008489, omega_cost 0.2344
- `diversity_n20`: posterior area 1, risk 0, %cost 0.009636, omega_cost 0.04701
- `pilotCost_n20`: posterior area 0.967, risk 0.026, %cost 0.00106, omega_cost 0.2097
- `pilotCost_n32`: posterior area 0.9807, risk 0.013, %cost 0.001688, omega_cost 0.1667

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n8` | `supports` | 26.05 | 8.74e-05 | moderate (0.1814) | median risks: random=0.06, balanced=0.026, diversity=0.013, SRSSampling=0.06, pairwise=0.06, pilotCost=0.026; spread=0.047 |
| `FSE1` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 4.924 | 0.425 | moderate (0) | median risks: random=0.026, balanced=0.026, diversity=0.013, SRSSampling=0.026, pairwise=0.013, pilotCost=0.026; spread=0.013 |
| `FSE1` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n20` | `supports` | 17.84 | 0.00316 | moderate (0.1107) | median risks: random=0.026, balanced=0.013, diversity=0, SRSSampling=0.026, pairwise=0.013, pilotCost=0.026; spread=0.026 |
| `FSE1` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n32` | `supports` | 26.89 | 6.00e-05 | moderate (0.1887) | median risks: random=0.026, balanced=0.0045, diversity=0, SRSSampling=0.026, pairwise=0.013, pilotCost=0.013; spread=0.026 |
| `FSE1` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n40` | `supports` | 19.16 | 0.00179 | moderate (0.1221) | median risks: random=0.00875, balanced=0.0045, diversity=0, SRSSampling=0.013, pairwise=0.013, pilotCost=0.026; spread=0.026 |
| `FSE1` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n64` | `supports` | 15.27 | 0.00928 | moderate (0.08852) | median risks: random=0.0045, balanced=0.0045, diversity=0, SRSSampling=0.013, pairwise=0.013, pilotCost=0.013; spread=0.013 |
| `FSE2` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.2101) | best size-normalized=diversity_n8; best cost-normalized=pilotCost_n8 |
| `FSE3` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.3184) | best cost-normalized=pilotCost_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n8; empirical front=diversity_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 442 | 0.705 | negligible (0.4911) | A12<0.5 means SRS risks tend to be lower; median SRS=0.06, median random=0.06 |
| `FSE6` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 433.5 | 0.798 | negligible (0.4817) | A12>0.5 means SRS costs tend to be higher; median SRS=0.004098, median random=0.004235 |
| `FSE2` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.1859) | best size-normalized=diversity_n16; best cost-normalized=pilotCost_n16 |
| `FSE3` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.2205) | best cost-normalized=pilotCost_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n16,pairwise_n16; empirical front=diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 441 | 0.717 | negligible (0.49) | A12<0.5 means SRS risks tend to be lower; median SRS=0.026, median random=0.026 |
| `FSE6` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 447.5 | 0.643 | negligible (0.5028) | A12>0.5 means SRS costs tend to be higher; median SRS=0.008365, median random=0.008365 |
| `FSE2` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.1627) | best size-normalized=diversity_n20; best cost-normalized=pilotCost_n20 |
| `FSE3` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.2108) | best cost-normalized=pilotCost_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n20; empirical front=diversity_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 450 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.026, median random=0.026 |
| `FSE6` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 438.5 | 0.741 | negligible (0.4872) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01029, median random=0.01042 |
| `FSE2` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.1361) | best size-normalized=diversity_n32; best cost-normalized=pilotCost_n32 |
| `FSE3` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.158) | best cost-normalized=pilotCost_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.5 |  | frontier change (1) | count front=diversity_n32; empirical front=diversity_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 436.5 | 0.769 | negligible (0.485) | A12<0.5 means SRS risks tend to be lower; median SRS=0.026, median random=0.026 |
| `FSE6` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 378 | 0.572 | small (0.42) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01526, median random=0.01535 |
| `FSE2` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.1145) | best size-normalized=diversity_n40; best cost-normalized=pilotCost_n40 |
| `FSE3` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.1275) | best cost-normalized=pilotCost_n40; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n40; empirical front=SRSSampling_n40,balanced_n40,diversity_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 402.5 | 0.819 | negligible (0.5528) | A12<0.5 means SRS risks tend to be lower; median SRS=0.013, median random=0.00875 |
| `FSE6` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n40` | `supports` | 270 | 0.0307 | medium (0.3) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01814, median random=0.02025 |
| `FSE2` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.05201) | best size-normalized=diversity_n64; best cost-normalized=pilotCost_n64 |
| `FSE3` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.0654) | best cost-normalized=pilotCost_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n64; empirical front=diversity_n64,pilotCost_n64,random_n64 |
| `FSE5` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 331 | 0.189 | small (0.6322) | A12<0.5 means SRS risks tend to be lower; median SRS=0.013, median random=0.0045 |
| `FSE6` | `lcbench__workload_cnae_9__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 308 | 0.11 | medium (0.3422) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02951, median random=0.03121 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.004235 | 0.06 | 0.8868 | -0.0132 | -0.01769 |
| `balanced_n8` | 8 | 0.004 | 0.004316 | 0.026 | 0.9718 | 0.07182 | 0.06588 |
| `diversity_n8` | 8 | 0.004 | 0.00366 | 0.013 | 0.987 | 0.087 | 0.0943 |
| `SRSSampling_n8` | 8 | 0.004 | 0.004098 | 0.06 | 0.8879 | -0.01207 | -0.01399 |
| `pairwise_n8` | 8 | 0.004 | 0.004873 | 0.06 | 0.94 | 0.04 | 0.02514 |
| `pilotCost_n8` | 8 | 0.004 | 0.0004221 | 0.026 | 0.9528 | 0.0528 | 0.3044 |
| `random_n16` | 16 | 0.008 | 0.008365 | 0.026 | 0.9594 | 0.01499 | 0.01283 |
| `balanced_n16` | 16 | 0.008 | 0.007962 | 0.026 | 0.9736 | 0.02914 | 0.02937 |
| `diversity_n16` | 16 | 0.008 | 0.007134 | 0.013 | 0.987 | 0.04256 | 0.04847 |
| `SRSSampling_n16` | 16 | 0.008 | 0.008365 | 0.026 | 0.9606 | 0.01612 | 0.01396 |
| `pairwise_n16` | 16 | 0.008 | 0.008252 | 0.013 | 0.987 | 0.04256 | 0.04105 |
| `pilotCost_n16` | 16 | 0.008 | 0.0008489 | 0.026 | 0.964 | 0.01954 | 0.2344 |
| `random_n20` | 20 | 0.01 | 0.01042 | 0.026 | 0.9546 | 5.455e-05 | -0.001607 |
| `balanced_n20` | 20 | 0.01 | 0.01008 | 0.013 | 0.9838 | 0.02927 | 0.02893 |
| `diversity_n20` | 20 | 0.01 | 0.009636 | 0 | 1 | 0.04545 | 0.04701 |
| `SRSSampling_n20` | 20 | 0.01 | 0.01029 | 0.026 | 0.9546 | 5.455e-05 | -0.001125 |
| `pairwise_n20` | 20 | 0.01 | 0.01063 | 0.013 | 0.987 | 0.03245 | 0.02999 |
| `pilotCost_n20` | 20 | 0.01 | 0.00106 | 0.026 | 0.967 | 0.01244 | 0.2097 |
| `random_n32` | 32 | 0.016 | 0.01535 | 0.026 | 0.9759 | 0.005295 | 0.006471 |
| `balanced_n32` | 32 | 0.016 | 0.01566 | 0.0045 | 0.992 | 0.02138 | 0.02198 |
| `diversity_n32` | 32 | 0.016 | 0.01532 | 0 | 1 | 0.02941 | 0.03064 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01526 | 0.026 | 0.978 | 0.007378 | 0.008708 |
| `pairwise_n32` | 32 | 0.016 | 0.01783 | 0.013 | 0.987 | 0.01641 | 0.01356 |
| `pilotCost_n32` | 32 | 0.016 | 0.001688 | 0.013 | 0.9807 | 0.01011 | 0.1667 |
| `random_n40` | 40 | 0.02 | 0.02025 | 0.00875 | 0.9861 | 0.00996 | 0.009679 |
| `balanced_n40` | 40 | 0.02 | 0.01997 | 0.0045 | 0.9893 | 0.01309 | 0.01312 |
| `diversity_n40` | 40 | 0.02 | 0.02021 | 0 | 1 | 0.02381 | 0.02357 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01814 | 0.013 | 0.9845 | 0.008326 | 0.01064 |
| `pairwise_n40` | 40 | 0.02 | 0.02151 | 0.013 | 0.987 | 0.01081 | 0.009208 |
| `pilotCost_n40` | 40 | 0.02 | 0.002111 | 0.026 | 0.9774 | 0.001176 | 0.1381 |
| `random_n64` | 64 | 0.032 | 0.03121 | 0.0045 | 0.9916 | 0.006785 | 0.007156 |
| `balanced_n64` | 64 | 0.032 | 0.03221 | 0.0045 | 0.9902 | 0.005385 | 0.005289 |
| `diversity_n64` | 64 | 0.032 | 0.03193 | 0 | 1 | 0.01515 | 0.01518 |
| `SRSSampling_n64` | 64 | 0.032 | 0.02951 | 0.013 | 0.9854 | 0.0005515 | 0.00179 |
| `pairwise_n64` | 64 | 0.032 | 0.03267 | 0.013 | 0.987 | 0.002152 | 0.00185 |
| `pilotCost_n64` | 64 | 0.032 | 0.005201 | 0.013 | 0.9866 | 0.001718 | 0.06719 |
