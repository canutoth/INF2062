# Generated sampling on TwinsOrFalseFriends `jump3r`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/jump3r/measurements.csv`

The table has 4296 rows, 36 encoded feature columns, and labels `energy, performance`.

Context columns excluded from features: `workload`.

Generated budgets: `8, 16` with 2 stochastic seeds.

Current learner: `gbt-log` (dependency-free gradient boosted regression trees trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=7.104, p90/p10=4.504, and strategy cost-over-random spans 0.207-511.8.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.3295; median `%cost/%n`=0.1558 with IQR 0.1182-0.1807.

Cost heterogeneity: CV=7.104, p90/p10=4.504. Sample-size proxy: Spearman rho=0.3295, median `%cost/%n`=0.1558 (IQR 0.1182-0.1807).

Strategy cost-over-random range: 0.207-511.8. Median calibration by strategy:

- `balanced`: 0.1678
- `cheapOracle`: 0.03355
- `diversity`: 2.046
- `expensiveOracle`: 76.98
- `pairwise`: 0.1349
- `pilotCost`: 0.08075
- `random`: 0.1486

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=5.538, p90/p10=2.2, and strategy cost-over-random spans 0.4635-190.5.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.659; median `%cost/%n`=0.3231 with IQR 0.2929-0.3582.

Cost heterogeneity: CV=5.538, p90/p10=2.2. Sample-size proxy: Spearman rho=0.659, median `%cost/%n`=0.3231 (IQR 0.2929-0.3582).

Strategy cost-over-random range: 0.4635-190.5. Median calibration by strategy:

- `balanced`: 0.3525
- `cheapOracle`: 0.1611
- `diversity`: 1.954
- `expensiveOracle`: 62.8
- `pairwise`: 0.3143
- `pilotCost`: 0.2542
- `random`: 0.3322

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in all scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0.4286 | 0.4244 | 0.4 | `random_n16` |
| `cost=performance, target=energy` | 0.5714 | 0.4528 | 0.5 | `random_n16` |
| `cost=energy, target=performance` | 0.1429 | 0.5942 | 0.3333 | `random_n16` |
| `cost=energy, target=energy` | 0.4286 | 0.5754 | 0.4 | `random_n16` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4; count cost selects 2 non-dominated pairs and empirical cost selects 5.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0.5714; 3 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 2 non-dominated pairs and empirical cost selects 4.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0.1429; 6 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.3333; count cost selects 2 non-dominated pairs and empirical cost selects 6.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4; count cost selects 2 non-dominated pairs and empirical cost selects 5.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
