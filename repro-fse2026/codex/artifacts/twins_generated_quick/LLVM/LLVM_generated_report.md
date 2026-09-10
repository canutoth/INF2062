# Generated sampling on TwinsOrFalseFriends `LLVM`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/LLVM/measurements.csv`

The table has 5000 rows, 16 encoded feature columns, and labels `performance, energy`.

Context columns excluded from features: `none`.

Generated budgets: `8, 16, 32` with 3 stochastic seeds.

Current learner: `ridge-log` (ridge regression trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=0.1197, p90/p10=1.379, and strategy cost-over-random spans 0.7044-1.38.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.9431; median `%cost/%n`=0.9945 with IQR 0.9065-1.007.

Cost heterogeneity: CV=0.1197, p90/p10=1.379. Sample-size proxy: Spearman rho=0.9431, median `%cost/%n`=0.9945 (IQR 0.9065-1.007).

Strategy cost-over-random range: 0.7044-1.38. Median calibration by strategy:

- `balanced`: 0.9995
- `cheapOracle`: 0.7308
- `diversity`: 1.002
- `expensiveOracle`: 1.299
- `pairwise`: 1.007
- `pilotCost`: 0.8756
- `random`: 0.9857

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=0.117, p90/p10=1.369, and strategy cost-over-random spans 0.7071-1.377.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.9431; median `%cost/%n`=0.993 with IQR 0.9056-1.005.

Cost heterogeneity: CV=0.117, p90/p10=1.369. Sample-size proxy: Spearman rho=0.9431, median `%cost/%n`=0.993 (IQR 0.9056-1.005).

Strategy cost-over-random range: 0.7071-1.377. Median calibration by strategy:

- `balanced`: 0.9975
- `cheapOracle`: 0.7335
- `diversity`: 1.002
- `expensiveOracle`: 1.297
- `pairwise`: 1.007
- `pilotCost`: 0.88
- `random`: 0.986

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in all scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0.5714 | 0.8435 | 0.4286 | `diversity_n32` |
| `cost=performance, target=energy` | 0.5714 | 0.8353 | 0.4286 | `diversity_n32` |
| `cost=energy, target=performance` | 0.5714 | 0.8353 | 0.4286 | `diversity_n32` |
| `cost=energy, target=energy` | 0.5714 | 0.8312 | 0.4286 | `diversity_n32` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0.5714; 3 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4286; count cost selects 3 non-dominated pairs and empirical cost selects 7.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0.5714; 3 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4286; count cost selects 3 non-dominated pairs and empirical cost selects 7.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0.5714; 3 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4286; count cost selects 3 non-dominated pairs and empirical cost selects 7.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0.5714; 3 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.4286; count cost selects 3 non-dominated pairs and empirical cost selects 7.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
