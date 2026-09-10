# Generated sampling on TwinsOrFalseFriends `x264`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/x264/measurements.csv`

The table has 4608 rows, 21 encoded feature columns, and labels `energy, performance`.

Context columns excluded from features: `none`.

Generated budgets: `8, 16, 32, 47, 64, 93, 128, 231, 256` with 100 stochastic seeds.

Current learner: `ridge-log` (ridge regression trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=0.5945, p90/p10=4.41, and strategy cost-over-random spans 0.3196-2.979.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.9516; median `%cost/%n`=0.9756 with IQR 0.5847-1.01.

Cost heterogeneity: CV=0.5945, p90/p10=4.41. Sample-size proxy: Spearman rho=0.9516, median `%cost/%n`=0.9756 (IQR 0.5847-1.01).

Strategy cost-over-random range: 0.3196-2.979. Median calibration by strategy:

- `balanced`: 0.9986
- `cheapOracle`: 0.3323
- `diversity`: 1.001
- `expensiveOracle`: 2.777
- `pairwise`: 1.001
- `pilotCost`: 0.5292
- `random`: 0.9984

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=0.4133, p90/p10=3.006, and strategy cost-over-random spans 0.4286-2.406.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.9739; median `%cost/%n`=0.9836 with IQR 0.7105-1.006.

Cost heterogeneity: CV=0.4133, p90/p10=3.006. Sample-size proxy: Spearman rho=0.9739, median `%cost/%n`=0.9836 (IQR 0.7105-1.006).

Strategy cost-over-random range: 0.4286-2.406. Median calibration by strategy:

- `balanced`: 0.9994
- `cheapOracle`: 0.4449
- `diversity`: 1.002
- `expensiveOracle`: 2.254
- `pairwise`: 1.002
- `pilotCost`: 0.6307
- `random`: 1

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in all scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0.4286 | 0.7523 | 0.5625 | `pairwise_n64` |
| `cost=performance, target=energy` | 0.2857 | 0.7545 | 0.5294 | `pairwise_n64` |
| `cost=energy, target=performance` | 0.4286 | 0.7975 | 0.5 | `pairwise_n64` |
| `cost=energy, target=energy` | 0.2857 | 0.8001 | 0.5 | `pairwise_n64` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5625; count cost selects 9 non-dominated pairs and empirical cost selects 16.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0.2857; 5 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5294; count cost selects 9 non-dominated pairs and empirical cost selects 17.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 9 non-dominated pairs and empirical cost selects 18.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0.2857; 5 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 9 non-dominated pairs and empirical cost selects 18.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
