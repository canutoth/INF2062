# Generated sampling on TwinsOrFalseFriends `x264`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/x264/measurements.csv`

The table has 4608 rows, 21 encoded feature columns, and labels `energy, performance`.

Context columns excluded from features: `none`.

Generated budgets: `8, 16` with 2 stochastic seeds.

Current learner: `ridge-log` (ridge regression trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=0.5945, p90/p10=4.41, and strategy cost-over-random spans 0.3666-3.766.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.5029; median `%cost/%n`=0.9213 with IQR 0.6956-0.9985.

Cost heterogeneity: CV=0.5945, p90/p10=4.41. Sample-size proxy: Spearman rho=0.5029, median `%cost/%n`=0.9213 (IQR 0.6956-0.9985).

Strategy cost-over-random range: 0.3666-3.766. Median calibration by strategy:

- `balanced`: 0.9598
- `cheapOracle`: 0.3217
- `diversity`: 0.9979
- `expensiveOracle`: 2.884
- `pairwise`: 1.025
- `pilotCost`: 0.69
- `random`: 0.8566

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=0.4133, p90/p10=3.006, and strategy cost-over-random spans 0.4662-2.871.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.6243; median `%cost/%n`=0.947 with IQR 0.7839-1.011.

Cost heterogeneity: CV=0.4133, p90/p10=3.006. Sample-size proxy: Spearman rho=0.6243, median `%cost/%n`=0.947 (IQR 0.7839-1.011).

Strategy cost-over-random range: 0.4662-2.871. Median calibration by strategy:

- `balanced`: 0.9766
- `cheapOracle`: 0.4291
- `diversity`: 1.001
- `expensiveOracle`: 2.366
- `pairwise`: 1.047
- `pilotCost`: 0.6754
- `random`: 0.8835

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in all scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0.4286 | 0.4749 | 0.25 | `pairwise_n16` |
| `cost=performance, target=energy` | 0 | 0.46 | 0.25 | `pairwise_n16` |
| `cost=energy, target=performance` | 0.1429 | 0.4403 | 0.25 | `pairwise_n16` |
| `cost=energy, target=energy` | 0 | 0.4812 | 0.25 | `pairwise_n16` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.25; count cost selects 2 non-dominated pairs and empirical cost selects 8.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.25; count cost selects 2 non-dominated pairs and empirical cost selects 8.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0.1429; 6 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.25; count cost selects 2 non-dominated pairs and empirical cost selects 8.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.25; count cost selects 2 non-dominated pairs and empirical cost selects 8.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
