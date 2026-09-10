# lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n20` (risk 0.002, %cost 0.01).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n8` (omega_cost 0.08714, %cost 0.00434).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9352, risk 0.06, %cost 0.003995, omega_cost 0.03532
- `diversity_n8`: posterior area 0.9935, risk 0.0065, %cost 0.00434, omega_cost 0.08714
- `SRSSampling_n8`: posterior area 0.8937, risk 0.07525, %cost 0.003174, omega_cost 0.01343
- `pilotCost_n8`: posterior area 0.7175, risk 0.348, %cost 0.002029, omega_cost -0.1174
- `diversity_n20`: posterior area 0.998, risk 0.002, %cost 0.01, omega_cost 0.04344

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n8` | `supports` | 24.12 | 2.06e-04 | large (0.1648) | median risks: random=0.07625, balanced=0.06, diversity=0.0065, SRSSampling=0.07525, pairwise=0.0475, pilotCost=0.348; spread=0.3415 |
| `FSE1` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n16` | `inconclusive` | 6.941 | 0.225 | large (0.01673) | median risks: random=0.04425, balanced=0.0365, diversity=0.0065, SRSSampling=0.04425, pairwise=0.0475, pilotCost=0.2675; spread=0.261 |
| `FSE1` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 3.731 | 0.589 | moderate (0) | median risks: random=0.04225, balanced=0.034, diversity=0.002, SRSSampling=0.0405, pairwise=0.0475, pilotCost=0.0225; spread=0.0455 |
| `FSE1` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n32` | `supports` | 23.1 | 3.23e-04 | large (0.156) | median risks: random=0.02025, balanced=0.0255, diversity=0.002, SRSSampling=0.024, pairwise=0.0475, pilotCost=0.1038; spread=0.1018 |
| `FSE1` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n40` | `supports` | 21.97 | 5.31e-04 | moderate (0.1463) | median risks: random=0.01575, balanced=0.009, diversity=0.002, SRSSampling=0.018, pairwise=0.0285, pilotCost=0.0475; spread=0.0455 |
| `FSE1` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n64` | `supports` | 13.59 | 0.0184 | moderate (0.07408) | median risks: random=0.01075, balanced=0.00425, diversity=0.002, SRSSampling=0.0055, pairwise=0.017, pilotCost=0.0065; spread=0.015 |
| `FSE2` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n8; best cost-normalized=diversity_n8 |
| `FSE3` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.07371) | best cost-normalized=diversity_n8; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n8; empirical front=SRSSampling_n8,balanced_n8,diversity_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 442.5 | 0.697 | negligible (0.4917) | A12<0.5 means SRS risks tend to be lower; median SRS=0.07525, median random=0.07625 |
| `FSE6` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 433.5 | 0.798 | negligible (0.4817) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003174, median random=0.003237 |
| `FSE2` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.04488) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n16; empirical front=SRSSampling_n16,balanced_n16,diversity_n16,pilotCost_n16,random_n16 |
| `FSE5` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 442.5 | 0.697 | negligible (0.4917) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04425, median random=0.04425 |
| `FSE6` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 432.5 | 0.809 | negligible (0.5194) | A12>0.5 means SRS costs tend to be higher; median SRS=0.006625, median random=0.006526 |
| `FSE2` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n20; best cost-normalized=diversity_n20 |
| `FSE3` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.04248) | best cost-normalized=diversity_n20; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n20; empirical front=SRSSampling_n20,balanced_n20,diversity_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 442.5 | 0.697 | negligible (0.4917) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0405, median random=0.04225 |
| `FSE6` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 433.5 | 0.798 | negligible (0.4817) | A12>0.5 means SRS costs tend to be higher; median SRS=0.008164, median random=0.008318 |
| `FSE2` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02291) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n32; empirical front=balanced_n32,diversity_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 426.5 | 0.879 | negligible (0.4739) | A12<0.5 means SRS risks tend to be lower; median SRS=0.024, median random=0.02025 |
| `FSE6` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 362 | 0.423 | small (0.5978) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01398, median random=0.01319 |
| `FSE2` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n40; best cost-normalized=diversity_n40 |
| `FSE3` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.01982) | best cost-normalized=diversity_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n40; empirical front=balanced_n40,diversity_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 420 | 0.955 | negligible (0.5333) | A12<0.5 means SRS risks tend to be lower; median SRS=0.018, median random=0.01575 |
| `FSE6` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 414 | 0.974 | negligible (0.54) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01744, median random=0.01684 |
| `FSE2` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (8.721e-05) | best size-normalized=diversity_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | moderate (0.008449) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n64; empirical front=balanced_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 389.5 | 0.693 | small (0.4328) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0055, median random=0.01075 |
| `FSE6` | `lcbench__workload_MiniBooNE__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 430 | 0.838 | negligible (0.4778) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0315, median random=0.02823 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003237 | 0.07625 | 0.8922 | -0.00775 | 0.01027 |
| `balanced_n8` | 8 | 0.004 | 0.003995 | 0.06 | 0.9352 | 0.03522 | 0.03532 |
| `diversity_n8` | 8 | 0.004 | 0.00434 | 0.0065 | 0.9935 | 0.0935 | 0.08714 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003174 | 0.07525 | 0.8937 | -0.00635 | 0.01343 |
| `pairwise_n8` | 8 | 0.004 | 0.005938 | 0.0475 | 0.9525 | 0.0525 | 0.02457 |
| `pilotCost_n8` | 8 | 0.004 | 0.002029 | 0.348 | 0.7175 | -0.1825 | -0.1174 |
| `random_n16` | 16 | 0.008 | 0.006526 | 0.04425 | 0.9431 | -0.001328 | 0.009549 |
| `balanced_n16` | 16 | 0.008 | 0.007008 | 0.0365 | 0.9556 | 0.01117 | 0.01806 |
| `diversity_n16` | 16 | 0.008 | 0.007042 | 0.0065 | 0.9935 | 0.04906 | 0.05567 |
| `SRSSampling_n16` | 16 | 0.008 | 0.006625 | 0.04425 | 0.9452 | 0.0007722 | 0.01079 |
| `pairwise_n16` | 16 | 0.008 | 0.008961 | 0.0475 | 0.9525 | 0.008056 | 0.002694 |
| `pilotCost_n16` | 16 | 0.008 | 0.004075 | 0.2675 | 0.7892 | -0.1552 | -0.1122 |
| `random_n20` | 20 | 0.01 | 0.008318 | 0.04225 | 0.9453 | -0.009212 | -0.001005 |
| `balanced_n20` | 20 | 0.01 | 0.008426 | 0.034 | 0.9593 | 0.004771 | 0.01236 |
| `diversity_n20` | 20 | 0.01 | 0.01 | 0.002 | 0.998 | 0.04345 | 0.04344 |
| `SRSSampling_n20` | 20 | 0.01 | 0.008164 | 0.0405 | 0.9464 | -0.008145 | 0.000963 |
| `pairwise_n20` | 20 | 0.01 | 0.01034 | 0.0475 | 0.9525 | -0.002045 | -0.003414 |
| `pilotCost_n20` | 20 | 0.01 | 0.005246 | 0.0225 | 0.8629 | -0.0917 | -0.0571 |
| `random_n32` | 32 | 0.016 | 0.01319 | 0.02025 | 0.9727 | 0.002078 | 0.007892 |
| `balanced_n32` | 32 | 0.016 | 0.01276 | 0.0255 | 0.973 | 0.002412 | 0.009337 |
| `diversity_n32` | 32 | 0.016 | 0.01521 | 0.002 | 0.998 | 0.02741 | 0.02884 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01398 | 0.024 | 0.9725 | 0.001945 | 0.005922 |
| `pairwise_n32` | 32 | 0.016 | 0.01557 | 0.0475 | 0.9525 | -0.01809 | -0.01732 |
| `pilotCost_n32` | 32 | 0.016 | 0.007992 | 0.1038 | 0.8228 | -0.1478 | -0.1216 |
| `random_n40` | 40 | 0.02 | 0.01684 | 0.01575 | 0.9811 | 0.004893 | 0.009106 |
| `balanced_n40` | 40 | 0.02 | 0.01517 | 0.009 | 0.9829 | 0.006676 | 0.01378 |
| `diversity_n40` | 40 | 0.02 | 0.02154 | 0.002 | 0.998 | 0.02181 | 0.02018 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01744 | 0.018 | 0.9732 | -0.00294 | 0.0003623 |
| `pairwise_n40` | 40 | 0.02 | 0.01826 | 0.0285 | 0.9715 | -0.00469 | -0.002536 |
| `pilotCost_n40` | 40 | 0.02 | 0.009967 | 0.0475 | 0.8361 | -0.14 | -0.1183 |
| `random_n64` | 64 | 0.032 | 0.02823 | 0.01075 | 0.985 | 0.0002015 | 0.002157 |
| `balanced_n64` | 64 | 0.032 | 0.02369 | 0.00425 | 0.992 | 0.007168 | 0.01227 |
| `diversity_n64` | 64 | 0.032 | 0.03426 | 0.002 | 0.998 | 0.01315 | 0.01218 |
| `SRSSampling_n64` | 64 | 0.032 | 0.0315 | 0.0055 | 0.9884 | 0.003585 | 0.003818 |
| `pairwise_n64` | 64 | 0.032 | 0.02713 | 0.017 | 0.983 | -0.001848 | 0.0007777 |
| `pilotCost_n64` | 64 | 0.032 | 0.01663 | 0.0065 | 0.9819 | -0.002998 | 0.01021 |
