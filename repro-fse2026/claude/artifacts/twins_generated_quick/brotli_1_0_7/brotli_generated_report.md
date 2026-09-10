# Generated sampling on TwinsOrFalseFriends `brotli`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/brotli/measurements.csv`

The table has 180 rows, 2 encoded feature columns, and labels `performance, energy`.

Context columns excluded from features: `revision`.

Generated budgets: `8, 9, 16, 18, 32` with 3 stochastic seeds.

Current learner: `ridge-log` (ridge regression trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=2.092, p90/p10=149.4, and strategy cost-over-random spans 0.01631-10.43.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.4842; median `%cost/%n`=0.9865 with IQR 0.6314-1.512.

Cost heterogeneity: CV=2.092, p90/p10=149.4. Sample-size proxy: Spearman rho=0.4842, median `%cost/%n`=0.9865 (IQR 0.6314-1.512).

Strategy cost-over-random range: 0.01631-10.43. Median calibration by strategy:

- `balanced`: 0.9863
- `cheapOracle`: 0.01742
- `diversity`: 1.48
- `expensiveOracle`: 7.091
- `pairwise`: 6.997
- `pilotCost`: 0.8817
- `random`: 0.7894

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=1.974, p90/p10=50.06, and strategy cost-over-random spans 0.05179-9.581.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.5126; median `%cost/%n`=0.9959 with IQR 0.6528-1.487.

Cost heterogeneity: CV=1.974, p90/p10=50.06. Sample-size proxy: Spearman rho=0.5126, median `%cost/%n`=0.9959 (IQR 0.6528-1.487).

Strategy cost-over-random range: 0.05179-9.581. Median calibration by strategy:

- `balanced`: 0.9884
- `cheapOracle`: 0.04979
- `diversity`: 1.441
- `expensiveOracle`: 6.745
- `pairwise`: 6.656
- `pilotCost`: 0.8836
- `random`: 0.8075

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in all scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0 | 0.6176 | 0.5 | `pilotCost_n16` |
| `cost=performance, target=energy` | 0.1429 | 0.6157 | 0.5 | `pilotCost_n8` |
| `cost=energy, target=performance` | 0 | 0.6253 | 0.4 | `pilotCost_n8` |
| `cost=energy, target=energy` | 0.1429 | 0.6234 | 0.5 | `pilotCost_n8` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 2 non-dominated pairs and empirical cost selects 4.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0.1429; 6 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 2 non-dominated pairs and empirical cost selects 4.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4; count cost selects 2 non-dominated pairs and empirical cost selects 5.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0.1429; 6 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 2 non-dominated pairs and empirical cost selects 4.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
