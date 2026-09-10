# Hipacc sampling-cost report

## Scope and protocol

This report extends the infrastructure beyond x264 using `Hipacc` from `NewRuns.zip`. The archive exposes sampled configuration CSVs for this system. The only available measured property is `Performance`, so this is the single diagonal scenario: empirical performance is both the cost of measuring a selected configuration and the target being predicted.

The sampled CSVs reconstruct 13472 of 13485 configurations. The current learner remains the lightweight ridge/log-linear model.

Because there is no separate size property here, this report is not a 2x2 matrix. It is the non-x264 analogue of the `cost=performance, target=performance` case.

## RQ1: Empirical cost heterogeneity

![Cost distribution by strategy and level](fig_rq1_cost_distribution.png)

![Strategy cost bias](fig_rq1_strategy_cost_bias.png)

Per-configuration empirical cost is heterogeneous: CV is 0.4353, and the p90/p10 cost ratio is 2.59. At fixed sample size, strategy overhead relative to random ranges from 1 to 1.696.

Median cost-over-random by strategy:

- `distBased`: 1.03
- `divDistBased`: 1.124
- `henard`: 1.212
- `random`: 1
- `solverBased`: 1.119

Interpretation: even on this non-x264 system, `n` does not force all strategies at the same level to consume the same empirical cost. The strength of the bias depends on which regions of the configuration space the strategy selects.

## RQ2: Sample size as cost proxy

![Sample-size calibration](fig_rq2_size_cost_calibration.png)

Spearman rho between `n` and empirical `TrainCost` is 0.9429. The median calibration ratio `%cost/%n` is 1.064, with IQR 1.002-1.114.

Median calibration ratio by strategy:

- `distBased`: 1.055
- `divDistBased`: 1.115
- `henard`: 1.171
- `random`: 0.9896
- `solverBased`: 1.081

Interpretation: sample size is useful as a first-order axis only if one is satisfied with coarse ordering. Calibration and strategy-specific bias still need to be checked.

## RQ3: Ranking robustness

![Rank agreement](fig_rq3_rank_stability.png)

Across 7 lambda values, the top-1 recommendation changes 0 times, so top-1 agreement is 1. Mean Kendall tau is 0.9341; the weakest lambda is 1 with tau 0.8462.

Interpretation: this directly tests whether a count-cost conclusion survives when empirical cost replaces sample size in the same accuracy-cost objective.

## RQ4: Pareto-efficient sampling

![Empirical accuracy-cost frontier](fig_rq4_accuracy_cost_frontier.png)

![Count vs empirical Pareto fronts](fig_rq4_frontier_count_vs_empirical.png)

Count-vs-empirical frontier Jaccard is 1. The count-cost frontier contains:

- `random_t1`
- `random_t2`

The empirical-cost frontier contains:

- `random_t1`
- `random_t2`

Interpretation: the Pareto comparison is the decision-level check. If the two lists differ, then replacing count cost by empirical cost changes which sampling choices are non-dominated.

## Takeaway

`Hipacc` gives a useful non-x264 replication point. It does not support the full time/size matrix because the archive exposes one `Performance` property, but it does let us test the central cost-proxy claim on another configurable system using the same code path.
