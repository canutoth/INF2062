# NewRuns cross-system sampling-cost report

## Scope

This report systematizes the non-x264 `NewRuns.zip` systems that expose sampled configuration CSVs with a `Performance` column. Each system has one measured property, so every analysis is the diagonal scenario `cost=performance, target=performance`.

The cost model is the same as in the x264 infrastructure: empirical training cost is the sum of `Performance` over the configurations selected by a sampling run. The prediction target is also `Performance`, because these systems do not expose a separate size property in the sampled CSVs.

Included systems: 7z, BerkeleyDBC, Dune, Hipacc, LLVM, Polly, lrzip.

## Overall conclusion

The conclusion is stronger than for x264. On these NewRuns systems, empirical cost is often highly heterogeneous and strategy-dependent. Sample size remains a useful coarse axis, but it is not a calibrated cost model and it can change decision-level conclusions.

Across 7 systems, cost CV ranges from 0.07241 to 1.981 (median 0.4352), and p90/p10 cost ratio ranges from 1.213 to 47.04 (median 2.59). Median `%cost/%n` ranges from 0.7356 to 1.078. Pareto Jaccard ranges from 0.4286 to 1.

## RQ1: Empirical cost heterogeneity

![Cost heterogeneity by system](fig_rq1_cost_heterogeneity_by_system.png)

![Strategy cost bias heatmap](fig_rq1_strategy_bias_heatmap.png)

| System | Reconstructed / expected configs | Cost CV | p90/p10 | Cost-over-random range | Strongest strategy-level bias |
|---|---:|---:|---:|---:|---|
| `7z` | 60148 / 68640 | 1.188 | 10.15 | 0.2678-1.04 | `solverBased_t1` = 0.2678 |
| `BerkeleyDBC` | 2485 / 2560 | 1.414 | 44.52 | 0.1178-1.891 | `henard_t1` = 0.1178 |
| `Dune` | 2304 / 2304 | 0.3438 | 1.827 | 0.9678-1.507 | `henard_t1` = 1.507 |
| `Hipacc` | 13485 / 13485 | 0.4352 | 2.59 | 1-1.635 | `solverBased_t1` = 1.635 |
| `LLVM` | 1017 / 1024 | 0.07241 | 1.213 | 0.9162-1.027 | `solverBased_t1` = 0.9162 |
| `Polly` | 37894 / 60000 | 0.2448 | 2.171 | 0.8786-1 | `divDistBased_t1` = 0.8786 |
| `lrzip` | 432 / 432 | 1.981 | 47.04 | 0.2353-1.104 | `solverBased_t1` = 0.2353 |

Interpretation: the equal-cost assumption is weak for this batch. The issue is not only that configurations vary in cost; sampling strategies repeatedly select systematically cheaper or costlier regions at the same sample size.

## RQ2: Sample size as cost proxy

![Calibration by system](fig_rq2_calibration_by_system.png)

| System | Spearman rho | Median %cost/%n | IQR %cost/%n |
|---|---:|---:|---:|
| `7z` | 0.9428 | 0.9699 | 0.7505-1.065 |
| `BerkeleyDBC` | 0.8697 | 0.7356 | 0.1933-1.083 |
| `Dune` | 0.9428 | 1.01 | 0.9818-1.067 |
| `Hipacc` | 0.9428 | 1.078 | 1.009-1.123 |
| `LLVM` | 0.9431 | 0.9968 | 0.97-1.007 |
| `Polly` | 0.9429 | 0.9995 | 0.9578-1.015 |
| `lrzip` | 0.9404 | 0.8653 | 0.5702-1.027 |

Interpretation: high correlation does not imply calibration. Several systems have median ratios far from one or wide IQRs, so a count budget can overstate or understate empirical measurement cost depending on the strategy.

## RQ3: Ranking robustness

![Decision agreement by system](fig_rq3_rq4_decision_change_by_system.png)

| System | Top-1 flips / 7 lambdas | Mean Kendall tau | Mean top-3 overlap |
|---|---:|---:|---:|
| `7z` | 2 / 7 | 0.8365 | 0.8571 |
| `BerkeleyDBC` | 0 / 7 | 0.5966 | 0.6667 |
| `Dune` | 0 / 7 | 0.9728 | 0.9524 |
| `Hipacc` | 0 / 7 | 0.937 | 1 |
| `LLVM` | 0 / 7 | 0.9455 | 1 |
| `Polly` | 0 / 7 | 0.9921 | 1 |
| `lrzip` | 2 / 7 | 0.7741 | 0.619 |

Interpretation: replacing count by empirical cost can change the cost-sensitive ranking. The effect varies by system, which is exactly why systematizing beyond x264 matters.

## RQ4: Pareto-efficient sampling

| System | Jaccard | Count frontier size | Empirical frontier size | Best empirical simple pair |
|---|---:|---:|---:|---|
| `7z` | 0.5 | 3 | 6 | `random_t2` |
| `BerkeleyDBC` | 0.6 | 3 | 5 | `random_t2` |
| `Dune` | 1 | 3 | 3 | `random_t1` |
| `Hipacc` | 1 | 3 | 3 | `random_t1` |
| `LLVM` | 0.4286 | 3 | 7 | `random_t1` |
| `Polly` | 0.5 | 3 | 6 | `random_t2` |
| `lrzip` | 0.6667 | 2 | 3 | `solverBased_t2` |

Interpretation: the Pareto front is a compact decision-level witness. When Jaccard is below one, the empirical-cost view is not just a rescaled count-cost view; it changes which sampling choices are non-dominated.

## Per-system reports

- [`7z` report](7z/7z_performance_report.md)
- [`BerkeleyDBC` report](BerkeleyDBC/BerkeleyDBC_performance_report.md)
- [`Dune` report](Dune/Dune_performance_report.md)
- [`Hipacc` report](Hipacc/Hipacc_performance_report.md)
- [`LLVM` report](LLVM/LLVM_performance_report.md)
- [`Polly` report](Polly/Polly_performance_report.md)
- [`lrzip` report](lrzip/lrzip_performance_report.md)

## Paper-level takeaway

The NewRuns systems provide stronger evidence for the paper's main claim than x264 alone. x264 showed that sample size can be a strong but incomplete proxy. NewRuns shows that the incompleteness can be large enough to affect calibration, rankings, and Pareto-efficient recommendations across multiple configurable systems.
