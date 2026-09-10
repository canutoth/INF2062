# Generated sampling on TwinsOrFalseFriends `PostgreSQL`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/PostgreSQL/measurements.csv`

The table has 864 rows, 8 encoded feature columns, and labels `performance, energy`.

Context columns excluded from features: `revision`.

Generated budgets: `8, 9, 16` with 2 stochastic seeds.

Current learner: `gbt-log` (dependency-free gradient boosted regression trees trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=0.06759, p90/p10=1.177, and strategy cost-over-random spans 0.9235-1.129.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.915; median `%cost/%n`=0.9934 with IQR 0.9621-1.01.

Cost heterogeneity: CV=0.06759, p90/p10=1.177. Sample-size proxy: Spearman rho=0.915, median `%cost/%n`=0.9934 (IQR 0.9621-1.01).

Strategy cost-over-random range: 0.9235-1.129. Median calibration by strategy:

- `balanced`: 0.9984
- `cheapOracle`: 0.9296
- `diversity`: 0.9928
- `expensiveOracle`: 1.119
- `pairwise`: 1.01
- `pilotCost`: 0.9438
- `random`: 1.006

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=0.05751, p90/p10=1.151, and strategy cost-over-random spans 0.9062-1.116.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.9197; median `%cost/%n`=0.996 with IQR 0.9678-1.006.

Cost heterogeneity: CV=0.05751, p90/p10=1.151. Sample-size proxy: Spearman rho=0.9197, median `%cost/%n`=0.996 (IQR 0.9678-1.006).

Strategy cost-over-random range: 0.9062-1.116. Median calibration by strategy:

- `balanced`: 1.002
- `cheapOracle`: 0.9107
- `diversity`: 0.9926
- `expensiveOracle`: 1.112
- `pairwise`: 1.006
- `pilotCost`: 0.9526
- `random`: 1.007

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in 3 of 4 scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0.4286 | 0.8748 | 0.4286 | `diversity_n9` |
| `cost=performance, target=energy` | 1 | 0.8721 | 0.3333 | `pairwise_n9` |
| `cost=energy, target=performance` | 0.4286 | 0.8639 | 0.5 | `diversity_n9` |
| `cost=energy, target=energy` | 0.8571 | 0.872 | 0.4286 | `pairwise_n9` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4286; count cost selects 3 non-dominated pairs and empirical cost selects 7.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 1; 0 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.3333; count cost selects 3 non-dominated pairs and empirical cost selects 9.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 3 non-dominated pairs and empirical cost selects 6.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0.8571; 1 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4286; count cost selects 3 non-dominated pairs and empirical cost selects 7.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
