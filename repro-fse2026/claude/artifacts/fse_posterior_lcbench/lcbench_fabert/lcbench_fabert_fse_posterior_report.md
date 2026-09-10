# lcbench__workload_fabert__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n32` (risk 0.0075, %cost 0.01536).

Best integrated confidence after normalizing the prior baseline by empirical cost: `cheapOracle_n8` (omega_cost 0.2181, %cost 0.0004944).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.9535, risk 0.0465, %cost 0.003804, omega_cost 0.05758
- `pairwise_n8`: posterior area 0.9805, risk 0.0195, %cost 0.004717, omega_cost 0.06795
- `pilotCost_n8`: posterior area 0.8902, risk 0.1165, %cost 0.0005722, omega_cost 0.2083
- `cheapOracle_n8`: posterior area 0.8835, risk 0.1165, %cost 0.0004944, omega_cost 0.2181
- `pilotCost_n16`: posterior area 0.9027, risk 0.1067, %cost 0.001138, omega_cost 0.1366
- `pilotCost_n20`: posterior area 0.9164, risk 0.1067, %cost 0.001421, omega_cost 0.123
- `diversity_n32`: posterior area 0.9925, risk 0.0075, %cost 0.01536, omega_cost 0.02306

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n8` | `supports` | 18.38 | 0.0104 | large (0.09809) | median risks: random=0.0865, balanced=0.036, diversity=0.0465, SRSSampling=0.0865, pairwise=0.0195, pilotCost=0.1165, cheapOracle=0.1165, expensiveOracle=0.32; spread=0.3005 |
| `FSE1` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n16` | `supports` | 38.54 | 2.39e-06 | large (0.2719) | median risks: random=0.0405, balanced=0.0195, diversity=0.0465, SRSSampling=0.0405, pairwise=0.0195, pilotCost=0.1067, cheapOracle=0.1165, expensiveOracle=0.2925; spread=0.273 |
| `FSE1` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n20` | `supports` | 22.95 | 0.00174 | large (0.1375) | median risks: random=0.0405, balanced=0.0195, diversity=0.0465, SRSSampling=0.0405, pairwise=0.0195, pilotCost=0.1067, cheapOracle=0.1165, expensiveOracle=0.2925; spread=0.273 |
| `FSE1` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n32` | `supports` | 55.35 | 1.27e-09 | large (0.4168) | median risks: random=0.028, balanced=0.0125, diversity=0.0075, SRSSampling=0.0165, pairwise=0.0075, pilotCost=0.0875, cheapOracle=0.0875, expensiveOracle=0.2925; spread=0.285 |
| `FSE1` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n40` | `supports` | 62.87 | 4.02e-11 | large (0.4817) | median risks: random=0.0165, balanced=0.0075, diversity=0.0075, SRSSampling=0.0145, pairwise=0.0075, pilotCost=0.097, cheapOracle=0.0875, expensiveOracle=0.2925; spread=0.285 |
| `FSE1` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n64` | `supports` | 42.79 | 3.67e-07 | large (0.3085) | median risks: random=0.0075, balanced=0.0075, diversity=0.0075, SRSSampling=0.0075, pairwise=0.0075, pilotCost=0.057, cheapOracle=0.0875, expensiveOracle=0.028; spread=0.08 |
| `FSE2` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.1501) | best size-normalized=pairwise_n8; best cost-normalized=cheapOracle_n8 |
| `FSE3` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.232) | best cost-normalized=cheapOracle_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.25 |  | large frontier change (3) | count front=pairwise_n8; empirical front=cheapOracle_n8,diversity_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 449 | 0.628 | negligible (0.4989) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0865, median random=0.0865 |
| `FSE6` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 433.5 | 0.798 | negligible (0.4817) | A12>0.5 means SRS costs tend to be higher; median SRS=0.00425, median random=0.00434 |
| `FSE2` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n16` | `supports` | 1 |  | changed (0.1012) | best size-normalized=pairwise_n16; best cost-normalized=pilotCost_n16 |
| `FSE3` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.1352) | best cost-normalized=pilotCost_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.25 |  | large frontier change (3) | count front=pairwise_n16; empirical front=cheapOracle_n16,diversity_n16,pairwise_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 447.5 | 0.643 | negligible (0.4972) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0405, median random=0.0405 |
| `FSE6` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 437.5 | 0.753 | negligible (0.5139) | A12>0.5 means SRS costs tend to be higher; median SRS=0.008273, median random=0.008273 |
| `FSE2` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n20` | `supports` | 1 |  | changed (0.09917) | best size-normalized=pairwise_n20; best cost-normalized=pilotCost_n20 |
| `FSE3` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.1373) | best cost-normalized=pilotCost_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.2 |  | large frontier change (4) | count front=pairwise_n20; empirical front=balanced_n20,cheapOracle_n20,diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 447 | 0.649 | negligible (0.5033) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0405, median random=0.0405 |
| `FSE6` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 443.5 | 0.686 | negligible (0.4928) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01006, median random=0.01034 |
| `FSE2` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n32` | `supports` | 1 |  | changed (0.05298) | best size-normalized=diversity_n32; best cost-normalized=cheapOracle_n32 |
| `FSE3` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.07291) | best cost-normalized=cheapOracle_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n32,pairwise_n32; empirical front=cheapOracle_n32,diversity_n32,random_n32 |
| `FSE5` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 366 | 0.455 | small (0.4067) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0165, median random=0.028 |
| `FSE6` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 403 | 0.845 | negligible (0.5522) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01609, median random=0.01532 |
| `FSE2` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n40` | `supports` | 1 |  | changed (0.03627) | best size-normalized=diversity_n40; best cost-normalized=cheapOracle_n40 |
| `FSE3` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.04685) | best cost-normalized=cheapOracle_n40; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.2 |  | large frontier change (4) | count front=diversity_n40,pairwise_n40; empirical front=SRSSampling_n40,balanced_n40,cheapOracle_n40,diversity_n40 |
| `FSE5` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 409.5 | 0.919 | negligible (0.455) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0145, median random=0.0165 |
| `FSE6` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 405 | 0.869 | negligible (0.45) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01994, median random=0.02039 |
| `FSE2` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n64` | `supports` | 1 |  | changed (0.002913) | best size-normalized=diversity_n64; best cost-normalized=pilotCost_n64 |
| `FSE3` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | moderate (0.00656) | best cost-normalized=pilotCost_n64; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.1667 |  | large frontier change (5) | count front=diversity_n64,pairwise_n64; empirical front=SRSSampling_n64,cheapOracle_n64,diversity_n64,pilotCost_n64,random_n64 |
| `FSE5` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n64` | `inconclusive` | 394 | 0.739 | small (0.4378) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0075, median random=0.0075 |
| `FSE6` | `lcbench__workload_fabert__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 437 | 0.758 | negligible (0.5144) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03176, median random=0.03141 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.00434 | 0.0865 | 0.8905 | -0.009483 | -0.01585 |
| `balanced_n8` | 8 | 0.004 | 0.004499 | 0.036 | 0.9469 | 0.04693 | 0.03785 |
| `diversity_n8` | 8 | 0.004 | 0.003804 | 0.0465 | 0.9535 | 0.0535 | 0.05758 |
| `SRSSampling_n8` | 8 | 0.004 | 0.00425 | 0.0865 | 0.8909 | -0.009133 | -0.0139 |
| `pairwise_n8` | 8 | 0.004 | 0.004717 | 0.0195 | 0.9805 | 0.0805 | 0.06795 |
| `pilotCost_n8` | 8 | 0.004 | 0.0005722 | 0.1165 | 0.8902 | -0.00975 | 0.2083 |
| `cheapOracle_n8` | 8 | 0.004 | 0.0004944 | 0.1165 | 0.8835 | -0.0165 | 0.2181 |
| `expensiveOracle_n8` | 8 | 0.004 | 0.01129 | 0.32 | 0.68 | -0.22 | -0.2793 |
| `random_n16` | 16 | 0.008 | 0.008273 | 0.0405 | 0.947 | 0.002572 | 0.0009361 |
| `balanced_n16` | 16 | 0.008 | 0.008313 | 0.0195 | 0.9708 | 0.02639 | 0.02452 |
| `diversity_n16` | 16 | 0.008 | 0.007281 | 0.0465 | 0.9535 | 0.009056 | 0.01388 |
| `SRSSampling_n16` | 16 | 0.008 | 0.008273 | 0.0405 | 0.9475 | 0.003056 | 0.001419 |
| `pairwise_n16` | 16 | 0.008 | 0.008103 | 0.0195 | 0.9805 | 0.03606 | 0.03543 |
| `pilotCost_n16` | 16 | 0.008 | 0.001138 | 0.1067 | 0.9027 | -0.04171 | 0.1366 |
| `cheapOracle_n16` | 16 | 0.008 | 0.001009 | 0.1165 | 0.8835 | -0.06094 | 0.1324 |
| `expensiveOracle_n16` | 16 | 0.008 | 0.02052 | 0.2925 | 0.7075 | -0.2369 | -0.2693 |
| `random_n20` | 20 | 0.01 | 0.01034 | 0.0405 | 0.9408 | -0.01375 | -0.0151 |
| `balanced_n20` | 20 | 0.01 | 0.01039 | 0.0195 | 0.9746 | 0.02004 | 0.01846 |
| `diversity_n20` | 20 | 0.01 | 0.009789 | 0.0465 | 0.9535 | -0.001045 | -0.0001567 |
| `SRSSampling_n20` | 20 | 0.01 | 0.01006 | 0.0405 | 0.9405 | -0.01406 | -0.01431 |
| `pairwise_n20` | 20 | 0.01 | 0.01055 | 0.0195 | 0.9805 | 0.02595 | 0.02378 |
| `pilotCost_n20` | 20 | 0.01 | 0.001421 | 0.1067 | 0.9164 | -0.03811 | 0.123 |
| `cheapOracle_n20` | 20 | 0.01 | 0.001269 | 0.1165 | 0.8835 | -0.07105 | 0.1039 |
| `expensiveOracle_n20` | 20 | 0.01 | 0.02491 | 0.2925 | 0.7075 | -0.247 | -0.2732 |
| `random_n32` | 32 | 0.016 | 0.01532 | 0.028 | 0.9653 | -0.005288 | -0.004067 |
| `balanced_n32` | 32 | 0.016 | 0.01616 | 0.0125 | 0.9889 | 0.01831 | 0.01804 |
| `diversity_n32` | 32 | 0.016 | 0.01536 | 0.0075 | 0.9925 | 0.02191 | 0.02306 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01609 | 0.0165 | 0.9739 | 0.003295 | 0.003134 |
| `pairwise_n32` | 32 | 0.016 | 0.0175 | 0.0075 | 0.9925 | 0.02191 | 0.01953 |
| `pilotCost_n32` | 32 | 0.016 | 0.002253 | 0.0875 | 0.9109 | -0.05965 | 0.06462 |
| `cheapOracle_n32` | 32 | 0.016 | 0.002057 | 0.0875 | 0.9125 | -0.05809 | 0.07605 |
| `expensiveOracle_n32` | 32 | 0.016 | 0.0378 | 0.2925 | 0.7075 | -0.2631 | -0.2796 |
| `random_n40` | 40 | 0.02 | 0.02039 | 0.0165 | 0.9737 | -0.002524 | -0.002958 |
| `balanced_n40` | 40 | 0.02 | 0.02023 | 0.0075 | 0.9895 | 0.01326 | 0.013 |
| `diversity_n40` | 40 | 0.02 | 0.02066 | 0.0075 | 0.9925 | 0.01631 | 0.01559 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01994 | 0.0145 | 0.9811 | 0.004943 | 0.005008 |
| `pairwise_n40` | 40 | 0.02 | 0.0212 | 0.0075 | 0.9925 | 0.01631 | 0.01502 |
| `pilotCost_n40` | 40 | 0.02 | 0.00282 | 0.097 | 0.9057 | -0.07049 | 0.03657 |
| `cheapOracle_n40` | 40 | 0.02 | 0.002588 | 0.0875 | 0.9125 | -0.06369 | 0.05186 |
| `expensiveOracle_n40` | 40 | 0.02 | 0.04604 | 0.2925 | 0.7075 | -0.2687 | -0.2819 |
| `random_n64` | 64 | 0.032 | 0.03141 | 0.0075 | 0.9864 | 0.001585 | 0.001862 |
| `balanced_n64` | 64 | 0.032 | 0.03243 | 0.0075 | 0.9904 | 0.005568 | 0.005375 |
| `diversity_n64` | 64 | 0.032 | 0.03213 | 0.0075 | 0.9925 | 0.007652 | 0.007594 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03176 | 0.0075 | 0.9887 | 0.003835 | 0.003947 |
| `pairwise_n64` | 64 | 0.032 | 0.03226 | 0.0075 | 0.9925 | 0.007652 | 0.007531 |
| `pilotCost_n64` | 64 | 0.032 | 0.00619 | 0.057 | 0.941 | -0.04388 | 0.01051 |
| `cheapOracle_n64` | 64 | 0.032 | 0.004204 | 0.0875 | 0.9125 | -0.07235 | 0.008572 |
| `expensiveOracle_n64` | 64 | 0.032 | 0.06895 | 0.028 | 0.972 | -0.01285 | -0.02085 |
