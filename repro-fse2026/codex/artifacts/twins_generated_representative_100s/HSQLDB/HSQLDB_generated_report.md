# Generated sampling on TwinsOrFalseFriends `HSQLDB`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/HSQLDB/measurements.csv`

The table has 864 rows, 17 encoded feature columns, and labels `energy, performance`.

Context columns excluded from features: `none`.

Generated budgets: `8, 9, 16, 18, 32, 44, 64, 87, 128, 173, 256` with 100 stochastic seeds.

Current learner: `ridge-log` (ridge regression trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=0.319, p90/p10=2.045, and strategy cost-over-random spans 0.759-1.621.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.9912; median `%cost/%n`=0.995 with IQR 0.9323-1.014.

Cost heterogeneity: CV=0.319, p90/p10=2.045. Sample-size proxy: Spearman rho=0.9912, median `%cost/%n`=0.995 (IQR 0.9323-1.014).

Strategy cost-over-random range: 0.759-1.621. Median calibration by strategy:

- `balanced`: 1.01
- `cheapOracle`: 0.7657
- `diversity`: 0.9884
- `expensiveOracle`: 1.595
- `pairwise`: 0.9827
- `pilotCost`: 0.8444
- `random`: 0.9999

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=0.3584, p90/p10=2.26, and strategy cost-over-random spans 0.7072-1.828.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.9907; median `%cost/%n`=0.9928 with IQR 0.9281-1.013.

Cost heterogeneity: CV=0.3584, p90/p10=2.26. Sample-size proxy: Spearman rho=0.9907, median `%cost/%n`=0.9928 (IQR 0.9281-1.013).

Strategy cost-over-random range: 0.7072-1.828. Median calibration by strategy:

- `balanced`: 1.007
- `cheapOracle`: 0.7149
- `diversity`: 0.9888
- `expensiveOracle`: 1.715
- `pairwise`: 0.9852
- `pilotCost`: 0.8294
- `random`: 0.9997

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in all scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0.4286 | 0.8894 | 0.6111 | `diversity_n18` |
| `cost=performance, target=energy` | 0.8571 | 0.8963 | 0.6875 | `diversity_n18` |
| `cost=energy, target=performance` | 0.4286 | 0.8814 | 0.6111 | `diversity_n18` |
| `cost=energy, target=energy` | 0.7143 | 0.894 | 0.6875 | `diversity_n18` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.6111; count cost selects 11 non-dominated pairs and empirical cost selects 18.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0.8571; 1 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.6875; count cost selects 11 non-dominated pairs and empirical cost selects 16.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.6111; count cost selects 11 non-dominated pairs and empirical cost selects 18.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0.7143; 2 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.6875; count cost selects 11 non-dominated pairs and empirical cost selects 16.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
