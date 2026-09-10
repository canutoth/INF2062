# lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n32` (risk 0.0005, %cost 0.01992).

Best integrated confidence after normalizing the prior baseline by empirical cost: `balanced_n8` (omega_cost 0.06898, %cost 0.002719).

Empirical cost/confidence Pareto front:

- `random_n8`: posterior area 0.9349, risk 0.0315, %cost 0.003852, omega_cost 0.03797
- `balanced_n8`: posterior area 0.9345, risk 0.0665, %cost 0.002719, omega_cost 0.06898
- `diversity_n8`: posterior area 0.987, risk 0.013, %cost 0.005238, omega_cost 0.06715
- `pilotCost_n8`: posterior area 0.8353, risk 0.1515, %cost 0.002372, omega_cost -0.01646
- `balanced_n20`: posterior area 0.9891, risk 0.00975, %cost 0.006446, omega_cost 0.05625
- `diversity_n32`: posterior area 0.9995, risk 0.0005, %cost 0.01992, omega_cost 0.0234
- `balanced_n40`: posterior area 0.9927, risk 0.0065, %cost 0.01328, omega_cost 0.02771

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n8` | `supports` | 17.16 | 0.00421 | large (0.1048) | median risks: random=0.0315, balanced=0.0665, diversity=0.013, SRSSampling=0.0615, pairwise=0.0795, pilotCost=0.1515; spread=0.1385 |
| `FSE1` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n16` | `supports` | 37.52 | 4.72e-07 | large (0.2803) | median risks: random=0.013, balanced=0.013, diversity=0.013, SRSSampling=0.013, pairwise=0.0795, pilotCost=0.1515; spread=0.1385 |
| `FSE1` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n20` | `supports` | 28.87 | 2.46e-05 | large (0.2058) | median risks: random=0.013, balanced=0.00975, diversity=0.013, SRSSampling=0.013, pairwise=0.0795, pilotCost=0.137; spread=0.1273 |
| `FSE1` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n32` | `supports` | 37.11 | 5.68e-07 | large (0.2768) | median risks: random=0.013, balanced=0.0065, diversity=0.0005, SRSSampling=0.013, pairwise=0.013, pilotCost=0.082; spread=0.0815 |
| `FSE1` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n40` | `supports` | 47.61 | 4.26e-09 | large (0.3674) | median risks: random=0.0065, balanced=0.0065, diversity=0.0005, SRSSampling=0.00975, pairwise=0.013, pilotCost=0.09675; spread=0.09625 |
| `FSE1` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n64` | `supports` | 37.31 | 5.19e-07 | moderate (0.2785) | median risks: random=0.013, balanced=0.0035, diversity=0.0005, SRSSampling=0.0065, pairwise=0.013, pilotCost=0.013; spread=0.0125 |
| `FSE2` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.001827) | best size-normalized=diversity_n8; best cost-normalized=balanced_n8 |
| `FSE3` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.03232) | best cost-normalized=balanced_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n8; empirical front=balanced_n8,diversity_n8,pilotCost_n8,random_n8 |
| `FSE5` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 441 | 0.715 | negligible (0.51) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0615, median random=0.0315 |
| `FSE6` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 440 | 0.725 | negligible (0.4889) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003783, median random=0.003852 |
| `FSE2` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.01391) | best size-normalized=diversity_n16; best cost-normalized=balanced_n16 |
| `FSE3` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.04228) | best cost-normalized=balanced_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n16; empirical front=balanced_n16,diversity_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 443 | 0.693 | negligible (0.5078) | A12<0.5 means SRS risks tend to be lower; median SRS=0.013, median random=0.013 |
| `FSE6` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 436.5 | 0.764 | negligible (0.515) | A12>0.5 means SRS costs tend to be higher; median SRS=0.007772, median random=0.007626 |
| `FSE2` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=balanced_n20; best cost-normalized=balanced_n20 |
| `FSE3` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.06258) | best cost-normalized=balanced_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.5 |  | frontier change (1) | count front=balanced_n20; empirical front=balanced_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 438 | 0.75 | negligible (0.4867) | A12<0.5 means SRS risks tend to be lower; median SRS=0.013, median random=0.013 |
| `FSE6` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 448.5 | 0.633 | negligible (0.4983) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009876, median random=0.009876 |
| `FSE2` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.009611) | best size-normalized=diversity_n32; best cost-normalized=balanced_n32 |
| `FSE3` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.01755) | best cost-normalized=balanced_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n32; empirical front=balanced_n32,diversity_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 362 | 0.367 | small (0.4022) | A12<0.5 means SRS risks tend to be lower; median SRS=0.013, median random=0.013 |
| `FSE6` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 355 | 0.366 | small (0.6056) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01641, median random=0.01529 |
| `FSE2` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.0121) | best size-normalized=diversity_n40; best cost-normalized=balanced_n40 |
| `FSE3` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.02332) | best cost-normalized=balanced_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n40; empirical front=balanced_n40,diversity_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n40` | `inconclusive` | 375.5 | 0.51 | small (0.5828) | A12<0.5 means SRS risks tend to be lower; median SRS=0.00975, median random=0.0065 |
| `FSE6` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 402 | 0.834 | negligible (0.5533) | A12>0.5 means SRS costs tend to be higher; median SRS=0.02152, median random=0.02011 |
| `FSE2` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.004869) | best size-normalized=diversity_n64; best cost-normalized=balanced_n64 |
| `FSE3` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01226) | best cost-normalized=balanced_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n64; empirical front=balanced_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 310 | 0.0939 | medium (0.3444) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0065, median random=0.013 |
| `FSE6` | `lcbench__workload_blood_transfusion_service_center__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 359 | 0.398 | small (0.6011) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03292, median random=0.03206 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003852 | 0.0315 | 0.9349 | 0.03492 | 0.03797 |
| `balanced_n8` | 8 | 0.004 | 0.002719 | 0.0665 | 0.9345 | 0.03455 | 0.06898 |
| `diversity_n8` | 8 | 0.004 | 0.005238 | 0.013 | 0.987 | 0.087 | 0.06715 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003783 | 0.0615 | 0.9321 | 0.03213 | 0.03666 |
| `pairwise_n8` | 8 | 0.004 | 0.003434 | 0.0795 | 0.9205 | 0.0205 | 0.03326 |
| `pilotCost_n8` | 8 | 0.004 | 0.002372 | 0.1515 | 0.8353 | -0.06475 | -0.01646 |
| `random_n16` | 16 | 0.008 | 0.007626 | 0.013 | 0.9567 | 0.01229 | 0.0147 |
| `balanced_n16` | 16 | 0.008 | 0.005294 | 0.013 | 0.9764 | 0.03191 | 0.0558 |
| `diversity_n16` | 16 | 0.008 | 0.00811 | 0.013 | 0.987 | 0.04256 | 0.04188 |
| `SRSSampling_n16` | 16 | 0.008 | 0.007772 | 0.013 | 0.9565 | 0.01207 | 0.01352 |
| `pairwise_n16` | 16 | 0.008 | 0.007467 | 0.0795 | 0.9205 | -0.02394 | -0.02045 |
| `pilotCost_n16` | 16 | 0.008 | 0.004791 | 0.1515 | 0.864 | -0.08048 | -0.04969 |
| `random_n20` | 20 | 0.01 | 0.009876 | 0.013 | 0.9437 | -0.01081 | -0.01029 |
| `balanced_n20` | 20 | 0.01 | 0.006446 | 0.00975 | 0.9891 | 0.03455 | 0.05625 |
| `diversity_n20` | 20 | 0.01 | 0.01278 | 0.013 | 0.987 | 0.03245 | 0.02329 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009876 | 0.013 | 0.9477 | -0.006845 | -0.006326 |
| `pairwise_n20` | 20 | 0.01 | 0.008952 | 0.0795 | 0.9205 | -0.03405 | -0.02926 |
| `pilotCost_n20` | 20 | 0.01 | 0.005956 | 0.137 | 0.865 | -0.08953 | -0.06311 |
| `random_n32` | 32 | 0.016 | 0.01529 | 0.013 | 0.9803 | 0.009695 | 0.01098 |
| `balanced_n32` | 32 | 0.016 | 0.01039 | 0.0065 | 0.9891 | 0.01851 | 0.03302 |
| `diversity_n32` | 32 | 0.016 | 0.01992 | 0.0005 | 0.9995 | 0.02891 | 0.0234 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01641 | 0.013 | 0.9868 | 0.01616 | 0.01546 |
| `pairwise_n32` | 32 | 0.016 | 0.01517 | 0.013 | 0.987 | 0.01641 | 0.01791 |
| `pilotCost_n32` | 32 | 0.016 | 0.00957 | 0.082 | 0.9115 | -0.05909 | -0.0412 |
| `random_n40` | 40 | 0.02 | 0.02011 | 0.0065 | 0.9911 | 0.01491 | 0.01479 |
| `balanced_n40` | 40 | 0.02 | 0.01328 | 0.0065 | 0.9927 | 0.01651 | 0.02771 |
| `diversity_n40` | 40 | 0.02 | 0.03004 | 0.0005 | 0.9995 | 0.02331 | 0.01561 |
| `SRSSampling_n40` | 40 | 0.02 | 0.02152 | 0.00975 | 0.9822 | 0.005993 | 0.004389 |
| `pairwise_n40` | 40 | 0.02 | 0.01855 | 0.013 | 0.987 | 0.01081 | 0.01257 |
| `pilotCost_n40` | 40 | 0.02 | 0.01193 | 0.09675 | 0.8964 | -0.07974 | -0.06488 |
| `random_n64` | 64 | 0.032 | 0.03206 | 0.013 | 0.9871 | 0.002218 | 0.002189 |
| `balanced_n64` | 64 | 0.032 | 0.02246 | 0.0035 | 0.9948 | 0.009918 | 0.01608 |
| `diversity_n64` | 64 | 0.032 | 0.04169 | 0.0005 | 0.9995 | 0.01465 | 0.01121 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03292 | 0.0065 | 0.9891 | 0.004235 | 0.003824 |
| `pairwise_n64` | 64 | 0.032 | 0.03097 | 0.013 | 0.987 | 0.002152 | 0.002639 |
| `pilotCost_n64` | 64 | 0.032 | 0.0191 | 0.013 | 0.9511 | -0.03375 | -0.02402 |
