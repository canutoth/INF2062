# lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `diversity_n20` (risk 0, %cost 0.01154).

Best integrated confidence after normalizing the prior baseline by empirical cost: `pairwise_n8` (omega_cost 0.09207, %cost 0.003217).

Empirical cost/confidence Pareto front:

- `diversity_n8`: posterior area 0.992, risk 0.008, %cost 0.004592, omega_cost 0.08141
- `pairwise_n8`: posterior area 0.9735, risk 0.0265, %cost 0.003217, omega_cost 0.09207
- `pilotCost_n8`: posterior area 0.7283, risk 0.1917, %cost 0.002397, omega_cost -0.1245
- `diversity_n16`: posterior area 0.9955, risk 0.0045, %cost 0.007625, omega_cost 0.05347
- `diversity_n20`: posterior area 1, risk 0, %cost 0.01154, omega_cost 0.03987

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n8` | `supports` | 15.33 | 0.00905 | large (0.08903) | median risks: random=0.085, balanced=0.0595, diversity=0.008, SRSSampling=0.08175, pairwise=0.0265, pilotCost=0.1917; spread=0.1837 |
| `FSE1` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n16` | `inconclusive` | 7.543 | 0.183 | large (0.02192) | median risks: random=0.04775, balanced=0.0475, diversity=0.0045, SRSSampling=0.04775, pairwise=0.0265, pilotCost=0.155; spread=0.1505 |
| `FSE1` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 4.615 | 0.465 | large (0) | median risks: random=0.048, balanced=0.0475, diversity=0, SRSSampling=0.05725, pairwise=0.0265, pilotCost=0.014; spread=0.05725 |
| `FSE1` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n32` | `supports` | 14.01 | 0.0156 | large (0.07764) | median risks: random=0.026, balanced=0.0165, diversity=0, SRSSampling=0.0205, pairwise=0.0265, pilotCost=0.06675; spread=0.06675 |
| `FSE1` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n40` | `supports` | 18.1 | 0.00283 | large (0.1129) | median risks: random=0.01275, balanced=0.01125, diversity=0, SRSSampling=0.02475, pairwise=0.0265, pilotCost=0.062; spread=0.062 |
| `FSE1` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n64` | `supports` | 19.88 | 0.00132 | moderate (0.1283) | median risks: random=0.01125, balanced=0.004, diversity=0, SRSSampling=0.01275, pairwise=0.0265, pilotCost=0.008; spread=0.0265 |
| `FSE2` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n8` | `supports` | 1 |  | changed (0.01066) | best size-normalized=diversity_n8; best cost-normalized=pairwise_n8 |
| `FSE3` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 0 |  | large (0.09506) | best cost-normalized=pairwise_n8; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n8` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n8; empirical front=diversity_n8,pairwise_n8,pilotCost_n8 |
| `FSE5` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 429.5 | 0.844 | negligible (0.4772) | A12<0.5 means SRS risks tend to be lower; median SRS=0.08175, median random=0.085 |
| `FSE6` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n8` | `refutes` | 434.5 | 0.787 | negligible (0.4828) | A12>0.5 means SRS costs tend to be higher; median SRS=0.003756, median random=0.003946 |
| `FSE2` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n16; best cost-normalized=diversity_n16 |
| `FSE3` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 0 |  | large (0.05288) | best cost-normalized=diversity_n16; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n16` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n16; empirical front=diversity_n16,pairwise_n16,pilotCost_n16 |
| `FSE5` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 447.5 | 0.643 | negligible (0.4972) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04775, median random=0.04775 |
| `FSE6` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n16` | `refutes` | 430.5 | 0.832 | negligible (0.5217) | A12>0.5 means SRS costs tend to be higher; median SRS=0.00775, median random=0.007485 |
| `FSE2` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n20; best cost-normalized=diversity_n20 |
| `FSE3` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 0 |  | large (0.05176) | best cost-normalized=diversity_n20; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n20` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n20; empirical front=diversity_n20,pairwise_n20,pilotCost_n20 |
| `FSE5` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 439.5 | 0.73 | negligible (0.5117) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05725, median random=0.048 |
| `FSE6` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n20` | `refutes` | 435.5 | 0.775 | negligible (0.4839) | A12>0.5 means SRS costs tend to be higher; median SRS=0.009495, median random=0.009549 |
| `FSE2` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n32; best cost-normalized=diversity_n32 |
| `FSE3` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 0 |  | large (0.02581) | best cost-normalized=diversity_n32; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n32` | `supports` | 0.25 |  | large frontier change (3) | count front=diversity_n32; empirical front=balanced_n32,diversity_n32,pairwise_n32,pilotCost_n32 |
| `FSE5` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n32` | `refutes` | 400 | 0.811 | negligible (0.4444) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0205, median random=0.026 |
| `FSE6` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n32` | `inconclusive` | 360 | 0.406 | small (0.6) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01615, median random=0.01494 |
| `FSE2` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n40; best cost-normalized=diversity_n40 |
| `FSE3` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 0 |  | large (0.02223) | best cost-normalized=diversity_n40; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n40` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n40; empirical front=balanced_n40,diversity_n40,pilotCost_n40 |
| `FSE5` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 400 | 0.811 | negligible (0.5556) | A12<0.5 means SRS risks tend to be lower; median SRS=0.02475, median random=0.01275 |
| `FSE6` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n40` | `refutes` | 407 | 0.892 | negligible (0.4522) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01964, median random=0.02014 |
| `FSE2` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | unchanged (0) | best size-normalized=diversity_n64; best cost-normalized=diversity_n64 |
| `FSE3` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 0 |  | large (0.01484) | best cost-normalized=diversity_n64; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n64` | `supports` | 0.3333 |  | large frontier change (2) | count front=diversity_n64; empirical front=balanced_n64,diversity_n64,pilotCost_n64 |
| `FSE5` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 431 | 0.827 | negligible (0.5211) | A12<0.5 means SRS risks tend to be lower; median SRS=0.01275, median random=0.01125 |
| `FSE6` | `lcbench__workload_jungle_chess_2pcs_raw_endgame_complete__cost_time_total__target_final_val_accuracy:n64` | `refutes` | 420 | 0.955 | negligible (0.4667) | A12>0.5 means SRS costs tend to be higher; median SRS=0.03171, median random=0.03167 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_n8` | 8 | 0.004 | 0.003946 | 0.085 | 0.8886 | -0.01143 | -0.01034 |
| `balanced_n8` | 8 | 0.004 | 0.004038 | 0.0595 | 0.9195 | 0.01952 | 0.01876 |
| `diversity_n8` | 8 | 0.004 | 0.004592 | 0.008 | 0.992 | 0.092 | 0.08141 |
| `SRSSampling_n8` | 8 | 0.004 | 0.003756 | 0.08175 | 0.8919 | -0.008117 | -0.002987 |
| `pairwise_n8` | 8 | 0.004 | 0.003217 | 0.0265 | 0.9735 | 0.0735 | 0.09207 |
| `pilotCost_n8` | 8 | 0.004 | 0.002397 | 0.1917 | 0.7283 | -0.1717 | -0.1245 |
| `random_n16` | 16 | 0.008 | 0.007485 | 0.04775 | 0.9427 | -0.001744 | 0.001627 |
| `balanced_n16` | 16 | 0.008 | 0.007168 | 0.0475 | 0.9552 | 0.01072 | 0.01638 |
| `diversity_n16` | 16 | 0.008 | 0.007625 | 0.0045 | 0.9955 | 0.05106 | 0.05347 |
| `SRSSampling_n16` | 16 | 0.008 | 0.00775 | 0.04775 | 0.9435 | -0.0009944 | 0.0005928 |
| `pairwise_n16` | 16 | 0.008 | 0.006914 | 0.0265 | 0.9735 | 0.02906 | 0.03668 |
| `pilotCost_n16` | 16 | 0.008 | 0.004983 | 0.155 | 0.7549 | -0.1895 | -0.1615 |
| `random_n20` | 20 | 0.01 | 0.009549 | 0.048 | 0.9425 | -0.01208 | -0.01014 |
| `balanced_n20` | 20 | 0.01 | 0.008677 | 0.0475 | 0.9522 | -0.002312 | 0.003905 |
| `diversity_n20` | 20 | 0.01 | 0.01154 | 0 | 1 | 0.04545 | 0.03987 |
| `SRSSampling_n20` | 20 | 0.01 | 0.009495 | 0.05725 | 0.9405 | -0.01408 | -0.01189 |
| `pairwise_n20` | 20 | 0.01 | 0.008619 | 0.0265 | 0.9735 | 0.01895 | 0.02548 |
| `pilotCost_n20` | 20 | 0.01 | 0.006133 | 0.014 | 0.8394 | -0.1151 | -0.09049 |
| `random_n32` | 32 | 0.016 | 0.01494 | 0.026 | 0.97 | -0.0005549 | 0.001397 |
| `balanced_n32` | 32 | 0.016 | 0.01335 | 0.0165 | 0.9675 | -0.003122 | 0.002316 |
| `diversity_n32` | 32 | 0.016 | 0.01769 | 0 | 1 | 0.02941 | 0.02675 |
| `SRSSampling_n32` | 32 | 0.016 | 0.01615 | 0.0205 | 0.9718 | 0.001195 | 0.000942 |
| `pairwise_n32` | 32 | 0.016 | 0.01486 | 0.0265 | 0.9735 | 0.002912 | 0.005022 |
| `pilotCost_n32` | 32 | 0.016 | 0.009699 | 0.06675 | 0.848 | -0.1226 | -0.1053 |
| `random_n40` | 40 | 0.02 | 0.02014 | 0.01275 | 0.9782 | 0.001976 | 0.001817 |
| `balanced_n40` | 40 | 0.02 | 0.01629 | 0.01125 | 0.9782 | 0.00206 | 0.007166 |
| `diversity_n40` | 40 | 0.02 | 0.02566 | 0 | 1 | 0.02381 | 0.01876 |
| `SRSSampling_n40` | 40 | 0.02 | 0.01964 | 0.02475 | 0.9723 | -0.00389 | -0.003478 |
| `pairwise_n40` | 40 | 0.02 | 0.01794 | 0.0265 | 0.9735 | -0.00269 | -9.573e-05 |
| `pilotCost_n40` | 40 | 0.02 | 0.01198 | 0.062 | 0.8319 | -0.1443 | -0.1295 |
| `random_n64` | 64 | 0.032 | 0.03167 | 0.01125 | 0.9848 | -4.848e-05 | 0.0001028 |
| `balanced_n64` | 64 | 0.032 | 0.02575 | 0.004 | 0.9917 | 0.006818 | 0.01036 |
| `diversity_n64` | 64 | 0.032 | 0.03754 | 0 | 1 | 0.01515 | 0.01297 |
| `SRSSampling_n64` | 64 | 0.032 | 0.03171 | 0.01275 | 0.9829 | -0.001998 | -0.001865 |
| `pairwise_n64` | 64 | 0.032 | 0.02896 | 0.0265 | 0.9735 | -0.01135 | -0.009809 |
| `pilotCost_n64` | 64 | 0.032 | 0.01918 | 0.008 | 0.9642 | -0.02062 | -0.01099 |
