# lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `random_n8` (risk 0.0005, %cost 0.003674).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_n8` (omega_cost 0.1132, %cost 0.003398).

Empirical cost/confidence Pareto front:

- `SRSSampling_n8`: posterior area 0.9995, risk 0.0005, %cost 0.003398, omega_cost 0.1132
- `pilotCost_n8`: posterior area 0.5656, risk 0.4315, %cost 0.002358, omega_cost -0.2855
- `cheapOracle_n8`: posterior area 0.1205, risk 0.8795, %cost 0.001953, omega_cost -0.7102

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n8` | `supports` | 33.47 | 2.17e-05 | large (0.7352) | median risks: random=0.0005, balanced=0.0005, diversity=0.0005, SRSSampling=0.0005, pairwise=0.0005, pilotCost=0.4315, cheapOracle=0.8795, expensiveOracle=0.0005; spread=0.879 |
| `FSE1` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n16` | `supports` | 26.16 | 4.72e-04 | large (0.5321) | median risks: random=0.0005, balanced=0.0005, diversity=0.0005, SRSSampling=0.0005, pairwise=0.0005, pilotCost=0.3998, cheapOracle=0.7605, expensiveOracle=0.0005; spread=0.76 |
| `FSE2` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.006725) | best size-normalized=random_n8; best cost-normalized=SRSSampling_n8 |
| `FSE3` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_n8; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.125 |  | large frontier change (7) | count front=SRSSampling_n8,balanced_n8,diversity_n8,expensiveOracle_n8,pairwise_n8,random_n8; empirical front=SRSSampling_n8,cheapOracle_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 50 |  | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0005, median random=0.0005 |
| `FSE6` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 46.5 | 0.815 | negligible (0.465) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003398, median random=0.003674 |
| `FSE2` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (2.372e-06) | best size-normalized=random_n16; best cost-normalized=balanced_n16 |
| `FSE3` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | moderate (0.001709) | best cost-normalized=balanced_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.125 |  | large frontier change (7) | count front=SRSSampling_n16,balanced_n16,diversity_n16,expensiveOracle_n16,pairwise_n16,random_n16; empirical front=balanced_n16,cheapOracle_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 50 |  | negligible (0.5) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0005, median random=0.0005 |
| `FSE6` | `lcbench__workload_Amazon_employee_access__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 44.5 | 0.934 | negligible (0.555) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007047, median random=0.006832 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003674 | 0.0005 | 0.9995 | 0.0995 | 0.1065 |
| `balanced_n8` | 8 | 0.004 | 0.003617 | 0.0005 | 0.9995 | 0.0995 | 0.1078 |
| `diversity_n8` | 8 | 0.004 | 0.004719 | 0.0005 | 0.9995 | 0.0995 | 0.08693 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003398 | 0.0005 | 0.9995 | 0.0995 | 0.1132 |
| `pairwise_n8` | 8 | 0.004 | 0.004535 | 0.0005 | 0.9995 | 0.0995 | 0.08983 |
| `pilotCost_n8` | 8 | 0.004 | 0.002358 | 0.4315 | 0.5656 | -0.3344 | -0.2855 |
| `cheapOracle_n8` | 8 | 0.004 | 0.001953 | 0.8795 | 0.1205 | -0.7795 | -0.7102 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.03397 | 0.0005 | 0.9995 | 0.0995 | 0.0138 |
| `random_n16` | 16 | 0.008 | 0.006832 | 0.0005 | 0.9995 | 0.05506 | 0.06334 |
| `balanced_n16` | 16 | 0.008 | 0.006832 | 0.0005 | 0.9995 | 0.05506 | 0.06334 |
| `diversity_n16` | 16 | 0.008 | 0.007761 | 0.0005 | 0.9995 | 0.05506 | 0.05657 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007047 | 0.0005 | 0.9995 | 0.05506 | 0.06163 |
| `pairwise_n16` | 16 | 0.008 | 0.008228 | 0.0005 | 0.9995 | 0.05506 | 0.05369 |
| `pilotCost_n16` | 16 | 0.008 | 0.004722 | 0.3998 | 0.7199 | -0.2245 | -0.1927 |
| `cheapOracle_n16` | 16 | 0.008 | 0.004019 | 0.7605 | 0.2395 | -0.7049 | -0.6609 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.05897 | 0.0005 | 0.9995 | 0.05506 | 0.007838 |
