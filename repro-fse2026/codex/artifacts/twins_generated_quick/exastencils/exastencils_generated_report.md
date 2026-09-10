# Generated sampling on TwinsOrFalseFriends `exastencils`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/exastencils/measurements.csv`

The table has 5000 rows, 11 encoded feature columns, and labels `energy, performance`.

Context columns excluded from features: `none`.

Generated budgets: `8, 16, 32` with 3 stochastic seeds.

Current learner: `ridge-log` (ridge regression trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=0.2812, p90/p10=1.867, and strategy cost-over-random spans 0.6253-2.346.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.8762; median `%cost/%n`=0.9816 with IQR 0.8623-1.007.

Cost heterogeneity: CV=0.2812, p90/p10=1.867. Sample-size proxy: Spearman rho=0.8762, median `%cost/%n`=0.9816 (IQR 0.8623-1.007).

Strategy cost-over-random range: 0.6253-2.346. Median calibration by strategy:

- `balanced`: 0.9971
- `cheapOracle`: 0.6181
- `diversity`: 0.9861
- `expensiveOracle`: 2.206
- `pairwise`: 1.007
- `pilotCost`: 0.8433
- `random`: 0.976

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=0.3845, p90/p10=2.459, and strategy cost-over-random spans 0.4143-2.853.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.8315; median `%cost/%n`=0.964 with IQR 0.8186-1.016.

Cost heterogeneity: CV=0.3845, p90/p10=2.459. Sample-size proxy: Spearman rho=0.8315, median `%cost/%n`=0.964 (IQR 0.8186-1.016).

Strategy cost-over-random range: 0.4143-2.853. Median calibration by strategy:

- `balanced`: 0.9956
- `cheapOracle`: 0.4228
- `diversity`: 0.9987
- `expensiveOracle`: 2.616
- `pairwise`: 1.013
- `pilotCost`: 0.8119
- `random`: 0.9603

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in all scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0.8571 | 0.7659 | 0.75 | `pilotCost_n32` |
| `cost=performance, target=energy` | 0.8571 | 0.7686 | 0.6667 | `pilotCost_n32` |
| `cost=energy, target=performance` | 0.5714 | 0.7101 | 0.6 | `pairwise_n32` |
| `cost=energy, target=energy` | 0.5714 | 0.7128 | 0.75 | `pairwise_n32` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0.8571; 1 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.75; count cost selects 3 non-dominated pairs and empirical cost selects 4.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0.8571; 1 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.6667; count cost selects 2 non-dominated pairs and empirical cost selects 3.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0.5714; 3 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.6; count cost selects 3 non-dominated pairs and empirical cost selects 5.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0.5714; 3 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.75; count cost selects 3 non-dominated pairs and empirical cost selects 4.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
