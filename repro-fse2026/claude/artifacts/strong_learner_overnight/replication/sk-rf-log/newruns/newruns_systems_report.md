# NewRuns cross-system sampling-cost report

## Scope

This report systematizes the non-x264 `NewRuns.zip` systems that expose sampled configuration CSVs with a `Performance` column. Each system has one measured property, so every analysis is the diagonal scenario `cost=performance, target=performance`.

The cost model is the same as in the x264 infrastructure: empirical training cost is the sum of `Performance` over the configurations selected by a sampling run. The prediction target is also `Performance`, because these systems do not expose a separate size property in the sampled CSVs.

Included systems: 7z, BerkeleyDBC, Dune, Hipacc, LLVM, Polly, lrzip.

## Overall conclusion

The conclusion is stronger than for x264. On these NewRuns systems, empirical cost is often highly heterogeneous and strategy-dependent. Sample size remains a useful coarse axis, but it is not a calibrated cost model and it can change decision-level conclusions.

Across 7 systems, cost CV ranges from 0.07236 to 1.981 (median 0.4352), and p90/p10 cost ratio ranges from 1.212 to 47.9 (median 2.59). Median `%cost/%n` ranges from 0.7881 to 1.076. Pareto Jaccard ranges from 0.3 to 1.

## RQ1: Empirical cost heterogeneity

![Cost heterogeneity by system](fig_rq1_cost_heterogeneity_by_system.png)

![Strategy cost bias heatmap](fig_rq1_strategy_bias_heatmap.png)

| System | Reconstructed / expected configs | Cost CV | p90/p10 | Cost-over-random range | Strongest strategy-level bias |
|---|---:|---:|---:|---:|---|
| `7z` | 68599 / 68640 | 1.188 | 10.13 | 0.2849-1.205 | `solverBased_t1` = 0.2849 |
| `BerkeleyDBC` | 2560 / 2560 | 1.42 | 47.9 | 0.1543-1.46 | `solverBased_t1` = 0.1543 |
| `Dune` | 2304 / 2304 | 0.3438 | 1.827 | 0.9798-1.445 | `henard_t1` = 1.445 |
| `Hipacc` | 13485 / 13485 | 0.4352 | 2.59 | 1-1.589 | `solverBased_t1` = 1.589 |
| `LLVM` | 1024 / 1024 | 0.07236 | 1.212 | 0.9111-1.024 | `solverBased_t1` = 0.9111 |
| `Polly` | 58565 / 60000 | 0.2389 | 2.106 | 0.9021-1.011 | `divDistBased_t1` = 0.9021 |
| `lrzip` | 432 / 432 | 1.981 | 47.04 | 0.2785-1.091 | `solverBased_t1` = 0.2785 |

Interpretation: the equal-cost assumption is weak for this batch. The issue is not only that configurations vary in cost; sampling strategies repeatedly select systematically cheaper or costlier regions at the same sample size.

## RQ2: Sample size as cost proxy

![Calibration by system](fig_rq2_calibration_by_system.png)

| System | Spearman rho | Median %cost/%n | IQR %cost/%n |
|---|---:|---:|---:|
| `7z` | 0.9428 | 0.9561 | 0.7278-1.033 |
| `BerkeleyDBC` | 0.8761 | 0.7881 | 0.1931-1.097 |
| `Dune` | 0.9428 | 1.011 | 0.9843-1.07 |
| `Hipacc` | 0.9428 | 1.076 | 1.01-1.134 |
| `LLVM` | 0.943 | 0.9964 | 0.9686-1.008 |
| `Polly` | 0.9428 | 0.9962 | 0.9669-1.01 |
| `lrzip` | 0.9386 | 0.8597 | 0.5632-0.9981 |

Interpretation: high correlation does not imply calibration. Several systems have median ratios far from one or wide IQRs, so a count budget can overstate or understate empirical measurement cost depending on the strategy.

## RQ3: Ranking robustness

![Decision agreement by system](fig_rq3_rq4_decision_change_by_system.png)

| System | Top-1 flips / 7 lambdas | Mean Kendall tau | Mean top-3 overlap |
|---|---:|---:|---:|
| `7z` | 1 / 7 | 0.7874 | 0.8571 |
| `BerkeleyDBC` | 1 / 7 | 0.6402 | 0.5714 |
| `Dune` | 0 / 7 | 0.9564 | 1 |
| `Hipacc` | 0 / 7 | 0.9339 | 0.9524 |
| `LLVM` | 0 / 7 | 0.9673 | 0.9524 |
| `Polly` | 0 / 7 | 0.9683 | 0.9524 |
| `lrzip` | 4 / 7 | 0.7682 | 0.619 |

Interpretation: replacing count by empirical cost can change the cost-sensitive ranking. The effect varies by system, which is exactly why systematizing beyond x264 matters.

## RQ4: Pareto-efficient sampling

| System | Jaccard | Count frontier size | Empirical frontier size | Best empirical simple pair |
|---|---:|---:|---:|---|
| `7z` | 0.4286 | 3 | 7 | `random_t3` |
| `BerkeleyDBC` | 0.5 | 3 | 6 | `random_t3` |
| `Dune` | 0.6 | 3 | 5 | `random_t1` |
| `Hipacc` | 1 | 3 | 3 | `random_t2` |
| `LLVM` | 0.3 | 3 | 10 | `random_t1` |
| `Polly` | 0.4286 | 3 | 7 | `random_t3` |
| `lrzip` | 0.375 | 3 | 8 | `solverBased_t2` |

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
