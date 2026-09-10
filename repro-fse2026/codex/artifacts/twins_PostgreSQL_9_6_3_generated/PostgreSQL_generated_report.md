# Generated sampling on TwinsOrFalseFriends `PostgreSQL`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/PostgreSQL/measurements.csv`

The table has 864 rows, 8 encoded feature columns, and labels `performance, energy`.

Context columns excluded from features: `revision`.

Generated budgets: `8, 9, 16, 18, 32, 44, 64, 87, 128, 173, 256` with 20 stochastic seeds.

Current learner: `ridge-log` (ridge regression trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=0.06788, p90/p10=1.18, and strategy cost-over-random spans 0.9227-1.12.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.9957; median `%cost/%n`=0.9992 with IQR 0.9895-1.003.

Cost heterogeneity: CV=0.06788, p90/p10=1.18. Sample-size proxy: Spearman rho=0.9957, median `%cost/%n`=0.9992 (IQR 0.9895-1.003).

Strategy cost-over-random range: 0.9227-1.12. Median calibration by strategy:

- `balanced`: 1
- `cheapOracle`: 0.9301
- `diversity`: 0.9981
- `expensiveOracle`: 1.111
- `pairwise`: 1.026
- `pilotCost`: 0.9685
- `random`: 1.002

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=0.05719, p90/p10=1.154, and strategy cost-over-random spans 0.9077-1.111.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.9958; median `%cost/%n`=0.9994 with IQR 0.9914-1.002.

Cost heterogeneity: CV=0.05719, p90/p10=1.154. Sample-size proxy: Spearman rho=0.9958, median `%cost/%n`=0.9994 (IQR 0.9914-1.002).

Strategy cost-over-random range: 0.9077-1.111. Median calibration by strategy:

- `balanced`: 1
- `cheapOracle`: 0.9219
- `diversity`: 0.9992
- `expensiveOracle`: 1.095
- `pairwise`: 1.021
- `pilotCost`: 0.9751
- `random`: 1.002

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in 3 of 4 scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0.8571 | 0.9743 | 0.7333 | `diversity_n9` |
| `cost=performance, target=energy` | 0.8571 | 0.9749 | 0.5882 | `pairwise_n8` |
| `cost=energy, target=performance` | 0.8571 | 0.9797 | 0.6667 | `diversity_n9` |
| `cost=energy, target=energy` | 1 | 0.979 | 0.5882 | `pairwise_n8` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0.8571; 1 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.7333; count cost selects 11 non-dominated pairs and empirical cost selects 15.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0.8571; 1 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5882; count cost selects 10 non-dominated pairs and empirical cost selects 17.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0.8571; 1 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.6667; count cost selects 10 non-dominated pairs and empirical cost selects 15.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 1; 0 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5882; count cost selects 10 non-dominated pairs and empirical cost selects 17.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
