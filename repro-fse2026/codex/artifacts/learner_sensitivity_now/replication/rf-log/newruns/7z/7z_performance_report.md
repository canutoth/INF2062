# 7z sampling-cost report

## Scope and protocol

This report extends the infrastructure beyond x264 using `7z` from `NewRuns.zip`. The archive exposes sampled configuration CSVs for this system. The only available measured property is `Performance`, so this is the single diagonal scenario: empirical performance is both the cost of measuring a selected configuration and the target being predicted.

The sampled CSVs reconstruct 47072 of 68640 configurations. The current learner remains the lightweight ridge/log-linear model.

Because there is no separate size property here, this report is not a 2x2 matrix. It is the non-x264 analogue of the `cost=performance, target=performance` case.

## RQ1: Empirical cost heterogeneity

![Cost distribution by strategy and level](fig_rq1_cost_distribution.png)

![Strategy cost bias](fig_rq1_strategy_cost_bias.png)

Per-configuration empirical cost is heterogeneous: CV is 1.201, and the p90/p10 cost ratio is 10.07. At fixed sample size, strategy overhead relative to random ranges from 0.2739 to 1.141.

Median cost-over-random by strategy:

- `distBased`: 0.7001
- `divDistBased`: 1.025
- `henard`: 0.3738
- `random`: 1
- `solverBased`: 0.8262

Interpretation: even on this non-x264 system, `n` does not force all strategies at the same level to consume the same empirical cost. The strength of the bias depends on which regions of the configuration space the strategy selects.

## RQ2: Sample size as cost proxy

![Sample-size calibration](fig_rq2_size_cost_calibration.png)

Spearman rho between `n` and empirical `TrainCost` is 0.9429. The median calibration ratio `%cost/%n` is 0.9947, with IQR 0.7178-1.082.

Median calibration ratio by strategy:

- `distBased`: 0.8694
- `divDistBased`: 1.08
- `henard`: 0.4063
- `random`: 1.042
- `solverBased`: 0.7841

Interpretation: sample size is useful as a first-order axis only if one is satisfied with coarse ordering. Calibration and strategy-specific bias still need to be checked.

## RQ3: Ranking robustness

![Rank agreement](fig_rq3_rank_stability.png)

Across 7 lambda values, the top-1 recommendation changes 1 times, so top-1 agreement is 0.8571. Mean Kendall tau is 0.831; the weakest lambda is 10 with tau 0.7333.

Interpretation: this directly tests whether a count-cost conclusion survives when empirical cost replaces sample size in the same accuracy-cost objective.

## RQ4: Pareto-efficient sampling

![Empirical accuracy-cost frontier](fig_rq4_accuracy_cost_frontier.png)

![Count vs empirical Pareto fronts](fig_rq4_frontier_count_vs_empirical.png)

Count-vs-empirical frontier Jaccard is 0.6. The count-cost frontier contains:

- `random_t2`
- `random_t3`
- `solverBased_t1`

The empirical-cost frontier contains:

- `distBased_t3`
- `henard_t2`
- `random_t2`
- `random_t3`
- `solverBased_t1`

Interpretation: the Pareto comparison is the decision-level check. If the two lists differ, then replacing count cost by empirical cost changes which sampling choices are non-dominated.

## Takeaway

`7z` gives a useful non-x264 replication point. It does not support the full time/size matrix because the archive exposes one `Performance` property, but it does let us test the central cost-proxy claim on another configurable system using the same code path.
