# Generated sampling on TwinsOrFalseFriends `PostgreSQL`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/PostgreSQL/measurements.csv`

The table has 864 rows, 8 encoded feature columns, and labels `performance, energy`.

Context columns excluded from features: `revision`.

Generated budgets: `8, 9, 16, 18, 32` with 3 stochastic seeds.

Current learner: `ridge-log` (ridge regression trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=0.06759, p90/p10=1.177, and strategy cost-over-random spans 0.9288-1.15.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.9724; median `%cost/%n`=0.9959 with IQR 0.9493-1.009.

Cost heterogeneity: CV=0.06759, p90/p10=1.177. Sample-size proxy: Spearman rho=0.9724, median `%cost/%n`=0.9959 (IQR 0.9493-1.009).

Strategy cost-over-random range: 0.9288-1.15. Median calibration by strategy:

- `balanced`: 1.002
- `cheapOracle`: 0.9303
- `diversity`: 0.9939
- `expensiveOracle`: 1.116
- `pairwise`: 1.02
- `pilotCost`: 0.9407
- `random`: 0.9994

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=0.05751, p90/p10=1.151, and strategy cost-over-random spans 0.9152-1.14.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.9735; median `%cost/%n`=0.9963 with IQR 0.9569-1.006.

Cost heterogeneity: CV=0.05751, p90/p10=1.151. Sample-size proxy: Spearman rho=0.9735, median `%cost/%n`=0.9963 (IQR 0.9569-1.006).

Strategy cost-over-random range: 0.9152-1.14. Median calibration by strategy:

- `balanced`: 1.002
- `cheapOracle`: 0.9134
- `diversity`: 0.9964
- `expensiveOracle`: 1.106
- `pairwise`: 1.01
- `pilotCost`: 0.9496
- `random`: 0.9963

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in 2 of 4 scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0.8571 | 0.938 | 0.5556 | `diversity_n9` |
| `cost=performance, target=energy` | 1 | 0.9414 | 0.5 | `pairwise_n9` |
| `cost=energy, target=performance` | 0.8571 | 0.9395 | 0.4545 | `diversity_n9` |
| `cost=energy, target=energy` | 1 | 0.9481 | 0.4167 | `pairwise_n9` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0.8571; 1 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5556; count cost selects 5 non-dominated pairs and empirical cost selects 9.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 1; 0 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 5 non-dominated pairs and empirical cost selects 10.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0.8571; 1 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4545; count cost selects 5 non-dominated pairs and empirical cost selects 11.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 1; 0 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4167; count cost selects 5 non-dominated pairs and empirical cost selects 12.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
