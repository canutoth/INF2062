# Generated sampling on TwinsOrFalseFriends `nginx`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/nginx/measurements.csv`

The table has 4416 rows, 15 encoded feature columns, and labels `performance, energy`.

Context columns excluded from features: `none`.

Generated budgets: `8, 16, 32` with 3 stochastic seeds.

Current learner: `ridge-log` (ridge regression trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=0.6419, p90/p10=67.98, and strategy cost-over-random spans 0.007924-1.788.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.519; median `%cost/%n`=0.8975 with IQR 0.6316-1.081.

Cost heterogeneity: CV=0.6419, p90/p10=67.98. Sample-size proxy: Spearman rho=0.519, median `%cost/%n`=0.8975 (IQR 0.6316-1.081).

Strategy cost-over-random range: 0.007924-1.788. Median calibration by strategy:

- `balanced`: 1.088
- `cheapOracle`: 0.007777
- `diversity`: 0.8133
- `expensiveOracle`: 1.602
- `pairwise`: 0.7647
- `pilotCost`: 0.03379
- `random`: 0.914

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=0.6412, p90/p10=74.86, and strategy cost-over-random spans 0.004521-1.736.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.519; median `%cost/%n`=0.8978 with IQR 0.6326-1.076.

Cost heterogeneity: CV=0.6412, p90/p10=74.86. Sample-size proxy: Spearman rho=0.519, median `%cost/%n`=0.8978 (IQR 0.6326-1.076).

Strategy cost-over-random range: 0.004521-1.736. Median calibration by strategy:

- `balanced`: 1.077
- `cheapOracle`: 0.004414
- `diversity`: 0.813
- `expensiveOracle`: 1.556
- `pairwise`: 0.7644
- `pilotCost`: 0.03422
- `random`: 0.9049

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in all scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0.1429 | 0.6204 | 0.5 | `pilotCost_n32` |
| `cost=performance, target=energy` | 0.1429 | 0.5823 | 0.5 | `diversity_n32` |
| `cost=energy, target=performance` | 0 | 0.619 | 0.6667 | `pilotCost_n32` |
| `cost=energy, target=energy` | 0 | 0.5782 | 0.4 | `diversity_n32` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0.1429; 6 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 3 non-dominated pairs and empirical cost selects 3.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0.1429; 6 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 3 non-dominated pairs and empirical cost selects 6.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.6667; count cost selects 2 non-dominated pairs and empirical cost selects 3.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4; count cost selects 2 non-dominated pairs and empirical cost selects 5.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
