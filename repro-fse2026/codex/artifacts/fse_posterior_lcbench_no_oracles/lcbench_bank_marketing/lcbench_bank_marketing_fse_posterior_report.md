# lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n16` (risk 0, %cost 0.007694).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pairwise_n8` (omega_cost 0.1114, %cost 0.003103).

Empirical cost/confidence Pareto front:

- `pairwise_n8`: posterior area 0.9895, risk 0.0105, %cost 0.003103, omega_cost 0.1114
- `pilotCost_n8`: posterior area 0.7353, risk 0.2645, %cost 0.002308, omega_cost -0.1135
- `diversity_n16`: posterior area 1, risk 0, %cost 0.007694, omega_cost 0.05751

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n8` | `supports` | 41.87 | 6.26e-08 | large (0.3179) | median risks: random=0.082, balanced=0.0105, diversity=0.0105, SRSSampling=0.08825, pairwise=0.0105, pilotCost=0.2645; spread=0.254 |
| `FSE1` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n16` | `supports` | 52.28 | 4.72e-10 | large (0.4076) | median risks: random=0.0105, balanced=0.0105, diversity=0, SRSSampling=0.0105, pairwise=0.0105, pilotCost=0.161; spread=0.161 |
| `FSE1` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n20` | `supports` | 46.51 | 7.14e-09 | large (0.3579) | median risks: random=0.0105, balanced=0.0105, diversity=0, SRSSampling=0.0105, pairwise=0.0105, pilotCost=0.0925; spread=0.0925 |
| `FSE1` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n32` | `supports` | 63.61 | 2.17e-12 | large (0.5053) | median risks: random=0.0105, balanced=0.0105, diversity=0, SRSSampling=0.0105, pairwise=0.0105, pilotCost=0.1115; spread=0.1115 |
| `FSE1` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n40` | `supports` | 34.84 | 1.62e-06 | large (0.2573) | median risks: random=0.0105, balanced=0.0105, diversity=0, SRSSampling=0.0105, pairwise=0.0105, pilotCost=0.108; spread=0.108 |
| `FSE1` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n64` | `supports` | 31.96 | 6.04e-06 | large (0.2325) | median risks: random=0.00875, balanced=0.0095, diversity=0, SRSSampling=0.0105, pairwise=0.005, pilotCost=0.07; spread=0.07 |
| `FSE2` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.03373) | best size-normalized=diversity_n8; best cost-normalized=pairwise_n8 |
| `FSE3` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.102) | best cost-normalized=pairwise_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n8,pairwise_n8; empirical front=pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 432.5 | 0.81 | negligible (0.5194) | A12<0.5 means SRS risks tend to be lower; median SRS=0.08825, median random=0.082 |
| `FSE6` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 435.5 | 0.775 | negligible (0.4839) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003677, median random=0.003901 |
| `FSE2` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.05816) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n16; empirical front=diversity_n16,pairwise_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 450 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0105, median random=0.0105 |
| `FSE6` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 434.5 | 0.787 | negligible (0.5172) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007611, median random=0.007313 |
| `FSE2` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.003596) | best size-normalized=diversity_n20; best cost-normalized=balanced_n20 |
| `FSE3` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.02942) | best cost-normalized=balanced_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n20; empirical front=balanced_n20,diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 450 | 1 | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0105, median random=0.0105 |
| `FSE6` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 432.5 | 0.809 | negligible (0.4806) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009364, median random=0.009396 |
| `FSE2` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.001128) | best size-normalized=diversity_n32; best cost-normalized=balanced_n32 |
| `FSE3` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.01938) | best cost-normalized=balanced_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n32; empirical front=balanced_n32,diversity_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 405 | 0.824 | negligible (0.45) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0105, median random=0.0105 |
| `FSE6` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 287 | 0.0562 | medium (0.6811) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01653, median random=0.01475 |
| `FSE2` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.003619) | best size-normalized=diversity_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.02206) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n40; empirical front=balanced_n40,diversity_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 378.5 | 0.511 | small (0.5794) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0105, median random=0.0105 |
| `FSE6` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 333 | 0.219 | small (0.63) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02185, median random=0.02003 |
| `FSE2` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n64; best cost-normalized=diversity_n64 |
| `FSE3` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01014) | best cost-normalized=diversity_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n64; empirical front=balanced_n64,diversity_n64,pairwise_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 399.5 | 0.773 | negligible (0.5561) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0105, median random=0.00875 |
| `FSE6` | `lcbench__workload_bank_marketing__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 421 | 0.943 | negligible (0.5322) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03309, median random=0.03135 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003901 | 0.082 | 0.9079 | 0.007917 | 0.009946 |
| `balanced_n8` | 8 | 0.004 | 0.00391 | 0.0105 | 0.9793 | 0.07932 | 0.08115 |
| `diversity_n8` | 8 | 0.004 | 0.004673 | 0.0105 | 0.9895 | 0.0895 | 0.07763 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003677 | 0.08825 | 0.9025 | 0.002483 | 0.009379 |
| `pairwise_n8` | 8 | 0.004 | 0.003103 | 0.0105 | 0.9895 | 0.0895 | 0.1114 |
| `pilotCost_n8` | 8 | 0.004 | 0.002308 | 0.2645 | 0.7353 | -0.1647 | -0.1135 |
| `random_n16` | 16 | 0.008 | 0.007313 | 0.0105 | 0.9413 | -0.003161 | 0.001428 |
| `balanced_n16` | 16 | 0.008 | 0.007134 | 0.0105 | 0.986 | 0.04152 | 0.04744 |
| `diversity_n16` | 16 | 0.008 | 0.007694 | 0 | 1 | 0.05556 | 0.05751 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007611 | 0.0105 | 0.9413 | -0.003161 | -0.0006524 |
| `pairwise_n16` | 16 | 0.008 | 0.006752 | 0.0105 | 0.9895 | 0.04506 | 0.054 |
| `pilotCost_n16` | 16 | 0.008 | 0.004763 | 0.161 | 0.8251 | -0.1194 | -0.08818 |
| `random_n20` | 20 | 0.01 | 0.009396 | 0.0105 | 0.9657 | 0.01114 | 0.01378 |
| `balanced_n20` | 20 | 0.01 | 0.00857 | 0.0105 | 0.9911 | 0.03655 | 0.04335 |
| `diversity_n20` | 20 | 0.01 | 0.01158 | 0 | 1 | 0.04545 | 0.03975 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009364 | 0.0105 | 0.9657 | 0.01114 | 0.01393 |
| `pairwise_n20` | 20 | 0.01 | 0.008355 | 0.0105 | 0.9895 | 0.03495 | 0.04295 |
| `pilotCost_n20` | 20 | 0.01 | 0.006255 | 0.0925 | 0.8651 | -0.0894 | -0.06594 |
| `random_n32` | 32 | 0.016 | 0.01475 | 0.0105 | 0.969 | -0.001588 | 0.0007499 |
| `balanced_n32` | 32 | 0.016 | 0.01306 | 0.0105 | 0.9922 | 0.02166 | 0.02782 |
| `diversity_n32` | 32 | 0.016 | 0.01773 | 0 | 1 | 0.02941 | 0.02669 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01653 | 0.0105 | 0.9799 | 0.009328 | 0.008436 |
| `pairwise_n32` | 32 | 0.016 | 0.01449 | 0.0105 | 0.9895 | 0.01891 | 0.02177 |
| `pilotCost_n32` | 32 | 0.016 | 0.009483 | 0.1115 | 0.8484 | -0.1222 | -0.1039 |
| `random_n40` | 40 | 0.02 | 0.02003 | 0.0105 | 0.9868 | 0.01061 | 0.01058 |
| `balanced_n40` | 40 | 0.02 | 0.01595 | 0.0105 | 0.9929 | 0.01673 | 0.02242 |
| `diversity_n40` | 40 | 0.02 | 0.0256 | 0 | 1 | 0.02381 | 0.0188 |
| `SRSSampling_n40` | 40 | 0.02 | 0.02185 | 0.0105 | 0.9785 | 0.002293 | 0.0003606 |
| `pairwise_n40` | 40 | 0.02 | 0.01759 | 0.0105 | 0.9895 | 0.01331 | 0.0164 |
| `pilotCost_n40` | 40 | 0.02 | 0.01152 | 0.108 | 0.8885 | -0.08769 | -0.07157 |
| `random_n64` | 64 | 0.032 | 0.03135 | 0.00875 | 0.9912 | 0.006352 | 0.006654 |
| `balanced_n64` | 64 | 0.032 | 0.02511 | 0.0095 | 0.9921 | 0.007268 | 0.01127 |
| `diversity_n64` | 64 | 0.032 | 0.0376 | 0 | 1 | 0.01515 | 0.01295 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03309 | 0.0105 | 0.9881 | 0.003302 | 0.002816 |
| `pairwise_n64` | 64 | 0.032 | 0.02822 | 0.005 | 0.995 | 0.01015 | 0.01211 |
| `pilotCost_n64` | 64 | 0.032 | 0.01871 | 0.07 | 0.9298 | -0.05507 | -0.04485 |
