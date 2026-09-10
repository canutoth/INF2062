# lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `random_n8` (risk 0.0005, %cost 0.003885).

Best integrated confidence after normalizing the prior baseline by empirical cost: `balanced_n8` (omega_cost 0.1031, %cost 0.003825).

Empirical cost/confidence Pareto front:

- `balanced_n8`: posterior area 0.9995, risk 0.0005, %cost 0.003825, omega_cost 0.1031
- `SRSSampling_n8`: posterior area 0.9716, risk 0.0005, %cost 0.003779, omega_cost 0.07622
- `pilotCost_n8`: posterior area 0.6624, risk 0.3942, %cost 0.002375, omega_cost -0.1894
- `random_n64`: posterior area 0.9995, risk 0.0005, %cost 0.03175, omega_cost 0.01478

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n8` | `supports` | 60.83 | 8.19e-12 | large (0.4813) | median risks: random=0.0005, balanced=0.0005, diversity=0.0005, SRSSampling=0.0005, pairwise=0.0005, pilotCost=0.3942; spread=0.3937 |
| `FSE1` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n16` | `supports` | 59.63 | 1.45e-11 | large (0.471) | median risks: random=0.0005, balanced=0.0005, diversity=0.0005, SRSSampling=0.0005, pairwise=0.0005, pilotCost=0.358; spread=0.3575 |
| `FSE1` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n20` | `supports` | 36.66 | 6.99e-07 | negligible (0.273) | median risks: random=0.0005, balanced=0.0005, diversity=0.0005, SRSSampling=0.0005, pairwise=0.0005, pilotCost=0.0005; spread=0 |
| `FSE1` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n32` | `supports` | 29.5 | 1.85e-05 | negligible (0.2112) | median risks: random=0.0005, balanced=0.0005, diversity=0.0005, SRSSampling=0.0005, pairwise=0.0005, pilotCost=0.0005; spread=0 |
| `FSE1` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n40` | `supports` | 40.34 | 1.28e-07 | negligible (0.3046) | median risks: random=0.0005, balanced=0.0005, diversity=0.0005, SRSSampling=0.0005, pairwise=0.0005, pilotCost=0.0005; spread=0 |
| `FSE1` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 4.033 | 0.545 | negligible (0) | median risks: random=0.0005, balanced=0.0005, diversity=0.0005, SRSSampling=0.0005, pairwise=0.0005, pilotCost=0.0005; spread=0 |
| `FSE2` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | unchanged (0) | best size-normalized=balanced_n8; best cost-normalized=balanced_n8 |
| `FSE3` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.02692) | best cost-normalized=balanced_n8; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.2 |  | large frontier change (4) | count front=balanced_n8,diversity_n8,pairwise_n8; empirical front=SRSSampling_n8,balanced_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 436 | 0.946 | negligible (0.5156) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0005, median random=0.0005 |
| `FSE6` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 438 | 0.747 | negligible (0.4867) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003779, median random=0.003885 |
| `FSE2` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.004652) | best size-normalized=random_n16; best cost-normalized=balanced_n16 |
| `FSE3` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | moderate (0.006206) | best cost-normalized=balanced_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.1667 |  | large frontier change (5) | count front=SRSSampling_n16,balanced_n16,diversity_n16,pairwise_n16,random_n16; empirical front=balanced_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 450 |  | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0005, median random=0.0005 |
| `FSE6` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 430.5 | 0.832 | negligible (0.5217) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007675, median random=0.007447 |
| `FSE2` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.007275) | best size-normalized=random_n20; best cost-normalized=balanced_n20 |
| `FSE3` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | moderate (0.007275) | best cost-normalized=balanced_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.1667 |  | large frontier change (5) | count front=SRSSampling_n20,balanced_n20,diversity_n20,pairwise_n20,random_n20; empirical front=balanced_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 450 |  | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0005, median random=0.0005 |
| `FSE6` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 440.5 | 0.719 | negligible (0.4894) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009677, median random=0.009677 |
| `FSE2` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.005395) | best size-normalized=random_n32; best cost-normalized=balanced_n32 |
| `FSE3` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | moderate (0.007564) | best cost-normalized=balanced_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.1667 |  | large frontier change (5) | count front=SRSSampling_n32,balanced_n32,diversity_n32,pairwise_n32,random_n32; empirical front=balanced_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 450 |  | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0005, median random=0.0005 |
| `FSE6` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 333 | 0.219 | small (0.63) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0163, median random=0.0151 |
| `FSE2` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.006706) | best size-normalized=random_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | moderate (0.006993) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.1667 |  | large frontier change (5) | count front=SRSSampling_n40,balanced_n40,diversity_n40,pairwise_n40,random_n40; empirical front=balanced_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 450 |  | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0005, median random=0.0005 |
| `FSE6` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 384 | 0.634 | small (0.5733) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02076, median random=0.02049 |
| `FSE2` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.003838) | best size-normalized=random_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | moderate (0.004564) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.3333 |  | large frontier change (2) | count front=random_n64; empirical front=balanced_n64,pilotCost_n64,random_n64 |
| `FSE5` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 435 | 0.617 | negligible (0.5167) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0005, median random=0.0005 |
| `FSE6` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 339 | 0.254 | small (0.6233) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03335, median random=0.03175 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003885 | 0.0005 | 0.9834 | 0.08342 | 0.08578 |
| `balanced_n8` | 8 | 0.004 | 0.003825 | 0.0005 | 0.9995 | 0.0995 | 0.1031 |
| `diversity_n8` | 8 | 0.004 | 0.004719 | 0.0005 | 0.9995 | 0.0995 | 0.08693 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003779 | 0.0005 | 0.9716 | 0.07158 | 0.07622 |
| `pairwise_n8` | 8 | 0.004 | 0.004535 | 0.0005 | 0.9995 | 0.0995 | 0.08983 |
| `pilotCost_n8` | 8 | 0.004 | 0.002375 | 0.3942 | 0.6624 | -0.2376 | -0.1894 |
| `random_n16` | 16 | 0.008 | 0.007447 | 0.0005 | 0.9995 | 0.05506 | 0.05869 |
| `balanced_n16` | 16 | 0.008 | 0.006832 | 0.0005 | 0.9995 | 0.05506 | 0.06334 |
| `diversity_n16` | 16 | 0.008 | 0.007761 | 0.0005 | 0.9995 | 0.05506 | 0.05657 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007675 | 0.0005 | 0.9995 | 0.05506 | 0.05714 |
| `pairwise_n16` | 16 | 0.008 | 0.008228 | 0.0005 | 0.9995 | 0.05506 | 0.05369 |
| `pilotCost_n16` | 16 | 0.008 | 0.004924 | 0.358 | 0.7582 | -0.1863 | -0.1574 |
| `random_n20` | 20 | 0.01 | 0.009677 | 0.0005 | 0.9995 | 0.04495 | 0.04633 |
| `balanced_n20` | 20 | 0.01 | 0.008241 | 0.0005 | 0.9995 | 0.04495 | 0.05361 |
| `diversity_n20` | 20 | 0.01 | 0.01183 | 0.0005 | 0.9995 | 0.04495 | 0.03846 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009677 | 0.0005 | 0.9995 | 0.04495 | 0.04633 |
| `pairwise_n20` | 20 | 0.01 | 0.009821 | 0.0005 | 0.9995 | 0.04495 | 0.0457 |
| `pilotCost_n20` | 20 | 0.01 | 0.00623 | 0.0005 | 0.8483 | -0.1063 | -0.08258 |
| `random_n32` | 32 | 0.016 | 0.0151 | 0.0005 | 0.9995 | 0.02891 | 0.03056 |
| `balanced_n32` | 32 | 0.016 | 0.01271 | 0.0005 | 0.9995 | 0.02891 | 0.03596 |
| `diversity_n32` | 32 | 0.016 | 0.01812 | 0.0005 | 0.9995 | 0.02891 | 0.02566 |
| `SRSSampling_n32` | 32 | 0.016 | 0.0163 | 0.0005 | 0.9995 | 0.02891 | 0.02839 |
| `pairwise_n32` | 32 | 0.016 | 0.01606 | 0.0005 | 0.9995 | 0.02891 | 0.0288 |
| `pilotCost_n32` | 32 | 0.016 | 0.009617 | 0.0005 | 0.8896 | -0.08097 | -0.06329 |
| `random_n40` | 40 | 0.02 | 0.02049 | 0.0005 | 0.9995 | 0.02331 | 0.02277 |
| `balanced_n40` | 40 | 0.02 | 0.01568 | 0.0005 | 0.9995 | 0.02331 | 0.02947 |
| `diversity_n40` | 40 | 0.02 | 0.02679 | 0.0005 | 0.9995 | 0.02331 | 0.01749 |
| `SRSSampling_n40` | 40 | 0.02 | 0.02076 | 0.0005 | 0.9995 | 0.02331 | 0.02248 |
| `pairwise_n40` | 40 | 0.02 | 0.01926 | 0.0005 | 0.9995 | 0.02331 | 0.02417 |
| `pilotCost_n40` | 40 | 0.02 | 0.01198 | 0.0005 | 0.8489 | -0.1273 | -0.1126 |
| `random_n64` | 64 | 0.032 | 0.03175 | 0.0005 | 0.9995 | 0.01467 | 0.01478 |
| `balanced_n64` | 64 | 0.032 | 0.02515 | 0.0005 | 0.9995 | 0.01465 | 0.01862 |
| `diversity_n64` | 64 | 0.032 | 0.03829 | 0.0005 | 0.9995 | 0.01465 | 0.01223 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03335 | 0.0005 | 0.9995 | 0.01465 | 0.01406 |
| `pairwise_n64` | 64 | 0.032 | 0.03028 | 0.0005 | 0.9995 | 0.01465 | 0.01548 |
| `pilotCost_n64` | 64 | 0.032 | 0.01933 | 0.0005 | 0.9876 | 0.002735 | 0.01218 |
