# lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n20` (risk 0, %cost 0.0122).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pilotCost_n8` (omega_cost 0.1382, %cost 0.001707).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9657, risk 0.027, %cost 0.002974, omega_cost 0.09153
- `diversity_n8`: posterior area 0.998, risk 0.002, %cost 0.004792, omega_cost 0.08433
- `pilotCost_n8`: posterior area 0.9534, risk 0.027, %cost 0.001707, omega_cost 0.1382
- `cheapOracle_n8`: posterior area 0.9305, risk 0.0695, %cost 0.001499, omega_cost 0.1306
- `pilotCost_n16`: posterior area 0.9746, risk 0.027, %cost 0.003405, omega_cost 0.0881
- `diversity_n20`: posterior area 1, risk 0, %cost 0.0122, omega_cost 0.03788

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n8` | `supports` | 36.94 | 4.81e-06 | large (0.2581) | median risks: random=0.0865, balanced=0.027, diversity=0.002, SRSSampling=0.0865, pairwise=0.027, pilotCost=0.027, cheapOracle=0.0695, expensiveOracle=0.015; spread=0.0845 |
| `FSE1` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n16` | `supports` | 31.23 | 5.64e-05 | large (0.2089) | median risks: random=0.038, balanced=0.015, diversity=0.002, SRSSampling=0.027, pairwise=0.0085, pilotCost=0.027, cheapOracle=0.0695, expensiveOracle=0.015; spread=0.0675 |
| `FSE1` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n20` | `supports` | 14.16 | 0.0484 | large (0.06175) | median risks: random=0.027, balanced=0.015, diversity=0, SRSSampling=0.027, pairwise=0.0085, pilotCost=0.027, cheapOracle=0.0695, expensiveOracle=0.0085; spread=0.0695 |
| `FSE1` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n32` | `supports` | 22.75 | 0.00188 | moderate (0.1358) | median risks: random=0.021, balanced=0.0085, diversity=0, SRSSampling=0.015, pairwise=0.0085, pilotCost=0.027, cheapOracle=0.049, expensiveOracle=0.0085; spread=0.049 |
| `FSE1` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n40` | `supports` | 18.08 | 0.0116 | moderate (0.09553) | median risks: random=0.015, balanced=0.015, diversity=0, SRSSampling=0.015, pairwise=0.0085, pilotCost=0.027, cheapOracle=0.049, expensiveOracle=0.0085; spread=0.049 |
| `FSE1` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n64` | `supports` | 15.83 | 0.0267 | moderate (0.07611) | median risks: random=0.0085, balanced=0.002, diversity=0, SRSSampling=0.015, pairwise=0.0085, pilotCost=0.015, cheapOracle=0.027, expensiveOracle=0.0085; spread=0.027 |
| `FSE2` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.05382) | best size-normalized=diversity_n8; best cost-normalized=pilotCost_n8 |
| `FSE3` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.1583) | best cost-normalized=pilotCost_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n8; empirical front=balanced_n8,cheapOracle_n8,diversity_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 443.5 | 0.687 | negligible (0.4928) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0865, median random=0.0865 |
| `FSE6` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 441.5 | 0.708 | negligible (0.4906) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003798, median random=0.003798 |
| `FSE2` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.03425) | best size-normalized=diversity_n16; best cost-normalized=pilotCost_n16 |
| `FSE3` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.07253) | best cost-normalized=pilotCost_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n16; empirical front=balanced_n16,cheapOracle_n16,diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 421 | 0.949 | negligible (0.4678) | A12<0.5 means SRS risks tend to be lower; median SRS=0.027, median random=0.038 |
| `FSE6` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 436.5 | 0.764 | negligible (0.515) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007648, median random=0.007586 |
| `FSE2` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.02864) | best size-normalized=diversity_n20; best cost-normalized=pilotCost_n20 |
| `FSE3` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.06055) | best cost-normalized=pilotCost_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n20; empirical front=balanced_n20,cheapOracle_n20,diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 429.5 | 0.848 | negligible (0.5228) | A12<0.5 means SRS risks tend to be lower; median SRS=0.027, median random=0.027 |
| `FSE6` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 442.5 | 0.697 | negligible (0.4917) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009903, median random=0.009903 |
| `FSE2` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.01341) | best size-normalized=diversity_n32; best cost-normalized=pilotCost_n32 |
| `FSE3` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.03075) | best cost-normalized=pilotCost_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n32; empirical front=balanced_n32,cheapOracle_n32,diversity_n32,pairwise_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 322.5 | 0.157 | medium (0.3583) | A12<0.5 means SRS risks tend to be lower; median SRS=0.015, median random=0.021 |
| `FSE6` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 411 | 0.939 | negligible (0.5433) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0158, median random=0.0154 |
| `FSE2` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.0113) | best size-normalized=diversity_n40; best cost-normalized=pilotCost_n40 |
| `FSE3` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.02476) | best cost-normalized=pilotCost_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n40; empirical front=balanced_n40,cheapOracle_n40,diversity_n40,pairwise_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 422 | 0.936 | negligible (0.5311) | A12<0.5 means SRS risks tend to be lower; median SRS=0.015, median random=0.015 |
| `FSE6` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 339 | 0.254 | small (0.3767) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0186, median random=0.02058 |
| `FSE2` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.00516) | best size-normalized=diversity_n64; best cost-normalized=pilotCost_n64 |
| `FSE3` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01378) | best cost-normalized=pilotCost_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n64; empirical front=balanced_n64,cheapOracle_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 384 | 0.614 | small (0.5733) | A12<0.5 means SRS risks tend to be lower; median SRS=0.015, median random=0.0085 |
| `FSE6` | `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 314 | 0.131 | medium (0.3489) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02992, median random=0.03308 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003798 | 0.0865 | 0.8742 | -0.02582 | -0.02161 |
| `balanced_n8` | 8 | 0.004 | 0.002974 | 0.027 | 0.9657 | 0.0657 | 0.09153 |
| `diversity_n8` | 8 | 0.004 | 0.004792 | 0.002 | 0.998 | 0.098 | 0.08433 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003798 | 0.0865 | 0.8756 | -0.0244 | -0.02019 |
| `pairwise_n8` | 8 | 0.004 | 0.003753 | 0.027 | 0.973 | 0.073 | 0.0782 |
| `pilotCost_n8` | 8 | 0.004 | 0.001707 | 0.027 | 0.9534 | 0.05342 | 0.1382 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001499 | 0.0695 | 0.9305 | 0.0305 | 0.1306 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.02379 | 0.015 | 0.985 | 0.085 | 0.005168 |
| `random_n16` | 16 | 0.008 | 0.007586 | 0.038 | 0.952 | 0.007572 | 0.01025 |
| `balanced_n16` | 16 | 0.008 | 0.00547 | 0.015 | 0.9848 | 0.04037 | 0.0621 |
| `diversity_n16` | 16 | 0.008 | 0.007953 | 0.002 | 0.998 | 0.05356 | 0.05385 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007648 | 0.027 | 0.9577 | 0.01331 | 0.01557 |
| `pairwise_n16` | 16 | 0.008 | 0.008208 | 0.0085 | 0.9915 | 0.04706 | 0.0458 |
| `pilotCost_n16` | 16 | 0.008 | 0.003405 | 0.027 | 0.9746 | 0.03016 | 0.0881 |
| `cheapOracle_n16` | 16 | 0.008 | 0.003038 | 0.0695 | 0.9305 | -0.01394 | 0.05432 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.04517 | 0.015 | 0.985 | 0.04056 | -0.004171 |
| `random_n20` | 20 | 0.01 | 0.009903 | 0.027 | 0.9622 | 0.007605 | 0.008007 |
| `balanced_n20` | 20 | 0.01 | 0.006896 | 0.015 | 0.9788 | 0.0242 | 0.04208 |
| `diversity_n20` | 20 | 0.01 | 0.0122 | 0 | 1 | 0.04545 | 0.03788 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009903 | 0.027 | 0.9601 | 0.005571 | 0.005974 |
| `pairwise_n20` | 20 | 0.01 | 0.01037 | 0.0085 | 0.9915 | 0.03695 | 0.03547 |
| `pilotCost_n20` | 20 | 0.01 | 0.004238 | 0.027 | 0.9711 | 0.01652 | 0.06653 |
| `cheapOracle_n20` | 20 | 0.01 | 0.003817 | 0.0695 | 0.9305 | -0.02405 | 0.03431 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.05505 | 0.0085 | 0.9915 | 0.03695 | 0.0004208 |
| `random_n32` | 32 | 0.016 | 0.0154 | 0.021 | 0.9683 | -0.002305 | -0.001227 |
| `balanced_n32` | 32 | 0.016 | 0.01095 | 0.0085 | 0.9848 | 0.01416 | 0.02659 |
| `diversity_n32` | 32 | 0.016 | 0.01937 | 0 | 1 | 0.02941 | 0.02454 |
| `SRSSampling_n32` | 32 | 0.016 | 0.0158 | 0.015 | 0.9774 | 0.006845 | 0.007201 |
| `pairwise_n32` | 32 | 0.016 | 0.01678 | 0.0085 | 0.9915 | 0.02091 | 0.01962 |
| `pilotCost_n32` | 32 | 0.016 | 0.00677 | 0.027 | 0.9736 | 0.003012 | 0.03795 |
| `cheapOracle_n32` | 32 | 0.016 | 0.006175 | 0.049 | 0.951 | -0.01959 | 0.02069 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.08259 | 0.0085 | 0.9915 | 0.02091 | -0.002519 |
| `random_n40` | 40 | 0.02 | 0.02058 | 0.015 | 0.9765 | 0.0002762 | -0.0003594 |
| `balanced_n40` | 40 | 0.02 | 0.01379 | 0.015 | 0.9863 | 0.01013 | 0.02012 |
| `diversity_n40` | 40 | 0.02 | 0.02817 | 0 | 1 | 0.02381 | 0.01714 |
| `SRSSampling_n40` | 40 | 0.02 | 0.0186 | 0.015 | 0.9782 | 0.001976 | 0.003675 |
| `pairwise_n40` | 40 | 0.02 | 0.02017 | 0.0085 | 0.9915 | 0.01531 | 0.01512 |
| `pilotCost_n40` | 40 | 0.02 | 0.008457 | 0.027 | 0.9756 | -0.0006238 | 0.02844 |
| `cheapOracle_n40` | 40 | 0.02 | 0.007763 | 0.049 | 0.951 | -0.02519 | 0.008057 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.09907 | 0.0085 | 0.9915 | 0.01531 | -0.003503 |
| `random_n64` | 64 | 0.032 | 0.03308 | 0.0085 | 0.9899 | 0.005102 | 0.004623 |
| `balanced_n64` | 64 | 0.032 | 0.02263 | 0.002 | 0.9928 | 0.007968 | 0.01397 |
| `diversity_n64` | 64 | 0.032 | 0.0399 | 0 | 1 | 0.01515 | 0.01223 |
| `SRSSampling_n64` | 64 | 0.032 | 0.02992 | 0.015 | 0.9874 | 0.002585 | 0.003604 |
| `pairwise_n64` | 64 | 0.032 | 0.03223 | 0.0085 | 0.9915 | 0.006652 | 0.006549 |
| `pilotCost_n64` | 64 | 0.032 | 0.01432 | 0.015 | 0.9848 | -9.848e-05 | 0.01739 |
| `cheapOracle_n64` | 64 | 0.032 | 0.01258 | 0.027 | 0.973 | -0.01185 | 0.009814 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.1447 | 0.0085 | 0.9915 | 0.006652 | -0.005067 |
