# lcbench__workload_higgs__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n20` (risk 0.001, %cost 0.01901).

Best integrated confidence after normalizing the prior baseline by empirical cost: `diversity_n8` (omega_cost 0.08964, %cost 0.004311).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.9955, risk 0.0045, %cost 0.004311, omega_cost 0.08964
- `SRSSampling_n8`: posterior area 0.8755, risk 0.09775, %cost 0.003475, omega_cost -0.01274
- `pairwise_n8`: posterior area 0.9785, risk 0.0215, %cost 0.003926, omega_cost 0.08001
- `pilotCost_n8`: posterior area 0.8717, risk 0.1435, %cost 0.002198, omega_cost 0.02805
- `diversity_n20`: posterior area 0.999, risk 0.001, %cost 0.01901, omega_cost 0.02399

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n8` | `inconclusive` | 7.619 | 0.178 | large (0.02258) | median risks: random=0.09925, balanced=0.063, diversity=0.0045, SRSSampling=0.09775, pairwise=0.0215, pilotCost=0.1435; spread=0.139 |
| `FSE1` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n16` | `inconclusive` | 8.419 | 0.135 | large (0.02947) | median risks: random=0.0435, balanced=0.045, diversity=0.0045, SRSSampling=0.04175, pairwise=0.0215, pilotCost=0.1295; spread=0.125 |
| `FSE1` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n20` | `inconclusive` | 8.201 | 0.145 | large (0.0276) | median risks: random=0.05125, balanced=0.045, diversity=0.001, SRSSampling=0.056, pairwise=0.0215, pilotCost=0.00625; spread=0.055 |
| `FSE1` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n32` | `supports` | 11.3 | 0.0458 | large (0.05428) | median risks: random=0.02275, balanced=0.02875, diversity=0.001, SRSSampling=0.02325, pairwise=0.0215, pilotCost=0.061; spread=0.06 |
| `FSE1` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n40` | `supports` | 17.01 | 0.00449 | moderate (0.1035) | median risks: random=0.01325, balanced=0.0145, diversity=0.001, SRSSampling=0.02075, pairwise=0.0215, pilotCost=0.04425; spread=0.04325 |
| `FSE1` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n64` | `supports` | 18.37 | 0.00252 | moderate (0.1153) | median risks: random=0.014, balanced=0.0025, diversity=0.001, SRSSampling=0.01275, pairwise=0.0215, pilotCost=0.0045; spread=0.0205 |
| `FSE2` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n8; best cost-normalized=diversity_n8 |
| `FSE3` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.1024) | best cost-normalized=diversity_n8; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n8; empirical front=SRSSampling_n8,diversity_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 426.5 | 0.879 | negligible (0.4739) | A12<0.5 means SRS risks tend to be lower; median SRS=0.09775, median random=0.09925 |
| `FSE6` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 434.5 | 0.787 | negligible (0.4828) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003475, median random=0.003493 |
| `FSE2` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.04591) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n16; empirical front=SRSSampling_n16,diversity_n16,pilotCost_n16,random_n16 |
| `FSE5` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 433.5 | 0.798 | negligible (0.4817) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04175, median random=0.0435 |
| `FSE6` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 432.5 | 0.809 | negligible (0.5194) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007149, median random=0.007048 |
| `FSE2` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.005809) | best size-normalized=diversity_n20; best cost-normalized=pairwise_n20 |
| `FSE3` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.04999) | best cost-normalized=pairwise_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n20; empirical front=diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 446.5 | 0.654 | negligible (0.5039) | A12<0.5 means SRS risks tend to be lower; median SRS=0.056, median random=0.05125 |
| `FSE6` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 435.5 | 0.775 | negligible (0.4839) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009167, median random=0.00922 |
| `FSE2` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.01306) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n32; empirical front=balanced_n32,diversity_n32,pairwise_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 402 | 0.834 | negligible (0.4467) | A12<0.5 means SRS risks tend to be lower; median SRS=0.02325, median random=0.02275 |
| `FSE6` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 435 | 0.781 | negligible (0.5167) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01507, median random=0.01497 |
| `FSE2` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.0002107) | best size-normalized=diversity_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | moderate (0.007889) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n40; empirical front=balanced_n40,diversity_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 385 | 0.644 | small (0.5722) | A12<0.5 means SRS risks tend to be lower; median SRS=0.02075, median random=0.01325 |
| `FSE6` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 354 | 0.358 | small (0.3933) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01817, median random=0.01907 |
| `FSE2` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.004821) | best size-normalized=diversity_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | moderate (0.009364) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n64; empirical front=balanced_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 435.5 | 0.775 | negligible (0.4839) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01275, median random=0.014 |
| `FSE6` | `lcbench__workload_higgs__cost_time_total__target_final_val_accuracy:n64` | `supports` | 276 | 0.0382 | medium (0.3067) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02957, median random=0.03448 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003493 | 0.09925 | 0.868 | -0.03195 | -0.02068 |
| `balanced_n8` | 8 | 0.004 | 0.004387 | 0.063 | 0.9067 | 0.0067 | -0.0004832 |
| `diversity_n8` | 8 | 0.004 | 0.004311 | 0.0045 | 0.9955 | 0.0955 | 0.08964 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003475 | 0.09775 | 0.8755 | -0.02448 | -0.01274 |
| `pairwise_n8` | 8 | 0.004 | 0.003926 | 0.0215 | 0.9785 | 0.0785 | 0.08001 |
| `pilotCost_n8` | 8 | 0.004 | 0.002198 | 0.1435 | 0.8717 | -0.02832 | 0.02805 |
| `random_n16` | 16 | 0.008 | 0.007048 | 0.0435 | 0.9444 | -6.111e-05 | 0.006512 |
| `balanced_n16` | 16 | 0.008 | 0.007456 | 0.045 | 0.9529 | 0.008506 | 0.01208 |
| `diversity_n16` | 16 | 0.008 | 0.007199 | 0.0045 | 0.9955 | 0.05106 | 0.05648 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007149 | 0.04175 | 0.9492 | 0.004772 | 0.01057 |
| `pairwise_n16` | 16 | 0.008 | 0.007208 | 0.0215 | 0.9785 | 0.03406 | 0.03942 |
| `pilotCost_n16` | 16 | 0.008 | 0.004681 | 0.1295 | 0.8979 | -0.04653 | -0.01407 |
| `random_n20` | 20 | 0.01 | 0.00922 | 0.05125 | 0.9313 | -0.02323 | -0.01976 |
| `balanced_n20` | 20 | 0.01 | 0.008978 | 0.045 | 0.9524 | -0.002179 | 0.002478 |
| `diversity_n20` | 20 | 0.01 | 0.01901 | 0.001 | 0.999 | 0.04445 | 0.02399 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009167 | 0.056 | 0.9306 | -0.02391 | -0.02019 |
| `pairwise_n20` | 20 | 0.01 | 0.008746 | 0.0215 | 0.9785 | 0.02395 | 0.0298 |
| `pilotCost_n20` | 20 | 0.01 | 0.005849 | 0.00625 | 0.9473 | -0.007229 | 0.02031 |
| `random_n32` | 32 | 0.016 | 0.01497 | 0.02275 | 0.9704 | -0.0001716 | 0.001723 |
| `balanced_n32` | 32 | 0.016 | 0.01355 | 0.02875 | 0.9688 | -0.001755 | 0.003197 |
| `diversity_n32` | 32 | 0.016 | 0.02454 | 0.001 | 0.999 | 0.02841 | 0.01858 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01507 | 0.02325 | 0.9744 | 0.003812 | 0.00552 |
| `pairwise_n32` | 32 | 0.016 | 0.01483 | 0.0215 | 0.9785 | 0.007912 | 0.01009 |
| `pilotCost_n32` | 32 | 0.016 | 0.008954 | 0.061 | 0.9237 | -0.04687 | -0.02605 |
| `random_n40` | 40 | 0.02 | 0.01907 | 0.01325 | 0.9781 | 0.00196 | 0.003065 |
| `balanced_n40` | 40 | 0.02 | 0.01635 | 0.0145 | 0.9816 | 0.005443 | 0.01046 |
| `diversity_n40` | 40 | 0.02 | 0.04345 | 0.001 | 0.999 | 0.02281 | 0.01025 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01817 | 0.02075 | 0.9765 | 0.0002929 | 0.00257 |
| `pairwise_n40` | 40 | 0.02 | 0.01899 | 0.0215 | 0.9785 | 0.00231 | 0.00351 |
| `pilotCost_n40` | 40 | 0.02 | 0.01095 | 0.04425 | 0.9299 | -0.04631 | -0.02829 |
| `random_n64` | 64 | 0.032 | 0.03448 | 0.014 | 0.9836 | -0.001232 | -0.00229 |
| `balanced_n64` | 64 | 0.032 | 0.02562 | 0.0025 | 0.9938 | 0.008968 | 0.0126 |
| `diversity_n64` | 64 | 0.032 | 0.05594 | 0.001 | 0.999 | 0.01415 | 0.007781 |
| `SRSSampling_n64` | 64 | 0.032 | 0.02957 | 0.01275 | 0.9869 | 0.002035 | 0.003237 |
| `pairwise_n64` | 64 | 0.032 | 0.02884 | 0.0215 | 0.9785 | -0.006348 | -0.004741 |
| `pilotCost_n64` | 64 | 0.032 | 0.01776 | 0.0045 | 0.9852 | 0.0003515 | 0.01186 |
