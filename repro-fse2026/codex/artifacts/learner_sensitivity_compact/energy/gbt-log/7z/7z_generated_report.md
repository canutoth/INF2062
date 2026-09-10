# Generated sampling on TwinsOrFalseFriends `7z`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/7z/measurements.csv`

The table has 5000 rows, 13 encoded feature columns, and labels `energy, performance`.

Context columns excluded from features: `none`.

Generated budgets: `8, 16` with 2 stochastic seeds.

Current learner: `gbt-log` (dependency-free gradient boosted regression trees trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=1.277, p90/p10=13.25, and strategy cost-over-random spans 0.06863-8.593.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.4856; median `%cost/%n`=0.7856 with IQR 0.4264-1.272.

Cost heterogeneity: CV=1.277, p90/p10=13.25. Sample-size proxy: Spearman rho=0.4856, median `%cost/%n`=0.7856 (IQR 0.4264-1.272).

Strategy cost-over-random range: 0.06863-8.593. Median calibration by strategy:

- `balanced`: 0.7621
- `cheapOracle`: 0.07341
- `diversity`: 1.177
- `expensiveOracle`: 7.108
- `pairwise`: 0.9455
- `pilotCost`: 0.4064
- `random`: 0.9865

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=1.22, p90/p10=12.71, and strategy cost-over-random spans 0.0836-8.249.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.4336; median `%cost/%n`=0.8568 with IQR 0.3959-1.251.

Cost heterogeneity: CV=1.22, p90/p10=12.71. Sample-size proxy: Spearman rho=0.4336, median `%cost/%n`=0.8568 (IQR 0.3959-1.251).

Strategy cost-over-random range: 0.0836-8.249. Median calibration by strategy:

- `balanced`: 0.912
- `cheapOracle`: 0.08784
- `diversity`: 1.161
- `expensiveOracle`: 6.643
- `pairwise`: 1.054
- `pilotCost`: 0.3325
- `random`: 0.9622

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in all scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0 | 0.5849 | 0.4 | `pilotCost_n16` |
| `cost=performance, target=energy` | 0 | 0.5667 | 0.4 | `pilotCost_n16` |
| `cost=energy, target=performance` | 0.2857 | 0.529 | 0.3333 | `pilotCost_n8` |
| `cost=energy, target=energy` | 0.4286 | 0.5566 | 0.5 | `balanced_n16` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4; count cost selects 2 non-dominated pairs and empirical cost selects 5.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4; count cost selects 2 non-dominated pairs and empirical cost selects 5.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0.2857; 5 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.3333; count cost selects 1 non-dominated pairs and empirical cost selects 3.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 2 non-dominated pairs and empirical cost selects 4.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
