# Generated sampling on TwinsOrFalseFriends `HSQLDB`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/HSQLDB/measurements.csv`

The table has 864 rows, 17 encoded feature columns, and labels `energy, performance`.

Context columns excluded from features: `none`.

Generated budgets: `8, 9, 16, 18, 32, 44, 64, 87, 128, 173, 256` with 20 stochastic seeds.

Current learner: `ridge-log` (ridge regression trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=0.319, p90/p10=2.045, and strategy cost-over-random spans 0.7504-1.609.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.9904; median `%cost/%n`=0.9954 with IQR 0.9422-1.015.

Cost heterogeneity: CV=0.319, p90/p10=2.045. Sample-size proxy: Spearman rho=0.9904, median `%cost/%n`=0.9954 (IQR 0.9422-1.015).

Strategy cost-over-random range: 0.7504-1.609. Median calibration by strategy:

- `balanced`: 1.01
- `cheapOracle`: 0.7657
- `diversity`: 0.9884
- `expensiveOracle`: 1.595
- `pairwise`: 0.9827
- `pilotCost`: 0.8543
- `random`: 1

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=0.3584, p90/p10=2.26, and strategy cost-over-random spans 0.6958-1.796.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.9894; median `%cost/%n`=0.9936 with IQR 0.9369-1.014.

Cost heterogeneity: CV=0.3584, p90/p10=2.26. Sample-size proxy: Spearman rho=0.9894, median `%cost/%n`=0.9936 (IQR 0.9369-1.014).

Strategy cost-over-random range: 0.6958-1.796. Median calibration by strategy:

- `balanced`: 1.007
- `cheapOracle`: 0.7149
- `diversity`: 0.9888
- `expensiveOracle`: 1.715
- `pairwise`: 0.9852
- `pilotCost`: 0.843
- `random`: 1.003

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in all scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0.4286 | 0.89 | 0.55 | `diversity_n18` |
| `cost=performance, target=energy` | 0.5714 | 0.895 | 0.5 | `diversity_n18` |
| `cost=energy, target=performance` | 0.4286 | 0.8802 | 0.5789 | `diversity_n18` |
| `cost=energy, target=energy` | 0.4286 | 0.8928 | 0.5556 | `diversity_n18` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.55; count cost selects 11 non-dominated pairs and empirical cost selects 20.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0.5714; 3 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 10 non-dominated pairs and empirical cost selects 20.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5789; count cost selects 11 non-dominated pairs and empirical cost selects 19.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5556; count cost selects 10 non-dominated pairs and empirical cost selects 18.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
