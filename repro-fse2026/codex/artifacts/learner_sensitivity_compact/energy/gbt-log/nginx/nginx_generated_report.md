# Generated sampling on TwinsOrFalseFriends `nginx`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/nginx/measurements.csv`

The table has 4416 rows, 15 encoded feature columns, and labels `performance, energy`.

Context columns excluded from features: `none`.

Generated budgets: `8, 16` with 2 stochastic seeds.

Current learner: `gbt-log` (dependency-free gradient boosted regression trees trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=0.6419, p90/p10=67.98, and strategy cost-over-random spans 0.008287-1.996.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.5723; median `%cost/%n`=0.8116 with IQR 0.6709-1.069.

Cost heterogeneity: CV=0.6419, p90/p10=67.98. Sample-size proxy: Spearman rho=0.5723, median `%cost/%n`=0.8116 (IQR 0.6709-1.069).

Strategy cost-over-random range: 0.008287-1.996. Median calibration by strategy:

- `balanced`: 1.122
- `cheapOracle`: 0.007763
- `diversity`: 0.7657
- `expensiveOracle`: 1.604
- `pairwise`: 0.6792
- `pilotCost`: 0.3724
- `random`: 0.9057

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=0.6412, p90/p10=74.86, and strategy cost-over-random spans 0.004716-1.935.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.5723; median `%cost/%n`=0.8121 with IQR 0.6729-1.07.

Cost heterogeneity: CV=0.6412, p90/p10=74.86. Sample-size proxy: Spearman rho=0.5723, median `%cost/%n`=0.8121 (IQR 0.6729-1.07).

Strategy cost-over-random range: 0.004716-1.935. Median calibration by strategy:

- `balanced`: 1.121
- `cheapOracle`: 0.00438
- `diversity`: 0.7684
- `expensiveOracle`: 1.557
- `pairwise`: 0.6815
- `pilotCost`: 0.3805
- `random`: 0.9013

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** the top recommendation is stable under count and empirical cost for all scenarios.

**RQ4 answer:** the count-cost and empirical-cost Pareto sets are identical for all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 1 | 0.6672 | 1 | `pilotCost_n16` |
| `cost=performance, target=energy` | 1 | 0.6735 | 1 | `pilotCost_n16` |
| `cost=energy, target=performance` | 1 | 0.6703 | 1 | `cheapOracle_n8` |
| `cost=energy, target=energy` | 1 | 0.6515 | 1 | `cheapOracle_n8` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 1; 0 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 1; count cost selects 2 non-dominated pairs and empirical cost selects 2.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 1; 0 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 1; count cost selects 2 non-dominated pairs and empirical cost selects 2.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 1; 0 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 1; count cost selects 1 non-dominated pairs and empirical cost selects 1.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 1; 0 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 1; count cost selects 1 non-dominated pairs and empirical cost selects 1.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
