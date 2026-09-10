# Generated sampling on TwinsOrFalseFriends `kanzi`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/kanzi/measurements.csv`

The table has 3202 rows, 30 encoded feature columns, and labels `energy, performance`.

Context columns excluded from features: `workload`.

Generated budgets: `8, 16, 32` with 3 stochastic seeds.

Current learner: `ridge-log` (ridge regression trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=1.978, p90/p10=87.99, and strategy cost-over-random spans 0.00844-47.63.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.4269; median `%cost/%n`=1.032 with IQR 0.3064-1.647.

Cost heterogeneity: CV=1.978, p90/p10=87.99. Sample-size proxy: Spearman rho=0.4269, median `%cost/%n`=1.032 (IQR 0.3064-1.647).

Strategy cost-over-random range: 0.00844-47.63. Median calibration by strategy:

- `balanced`: 1.136
- `cheapOracle`: 0.008422
- `diversity`: 1.792
- `expensiveOracle`: 10.09
- `pairwise`: 1.434
- `pilotCost`: 0.2059
- `random`: 0.7408

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=2.132, p90/p10=80.46, and strategy cost-over-random spans 0.0148-80.54.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.4241; median `%cost/%n`=0.8958 with IQR 0.3186-1.412.

Cost heterogeneity: CV=2.132, p90/p10=80.46. Sample-size proxy: Spearman rho=0.4241, median `%cost/%n`=0.8958 (IQR 0.3186-1.412).

Strategy cost-over-random range: 0.0148-80.54. Median calibration by strategy:

- `balanced`: 1.095
- `cheapOracle`: 0.01331
- `diversity`: 1.788
- `expensiveOracle`: 11.74
- `pairwise`: 1.412
- `pilotCost`: 0.3173
- `random`: 0.5798

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in all scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0 | 0.4527 | 0.3333 | `pilotCost_n32` |
| `cost=performance, target=energy` | 0 | 0.4653 | 0.3333 | `pilotCost_n32` |
| `cost=energy, target=performance` | 0.8571 | 0.4272 | 0.5 | `pilotCost_n32` |
| `cost=energy, target=energy` | 0.1429 | 0.4432 | 0.3333 | `pilotCost_n32` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.3333; count cost selects 3 non-dominated pairs and empirical cost selects 5.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.3333; count cost selects 3 non-dominated pairs and empirical cost selects 5.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0.8571; 1 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 3 non-dominated pairs and empirical cost selects 3.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0.1429; 6 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.3333; count cost selects 3 non-dominated pairs and empirical cost selects 5.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
