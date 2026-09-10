# Generated sampling on TwinsOrFalseFriends `jump3r`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/jump3r/measurements.csv`

The table has 4296 rows, 36 encoded feature columns, and labels `energy, performance`.

Context columns excluded from features: `workload`.

Generated budgets: `8, 16, 32, 43, 64, 86, 128, 215, 256` with 100 stochastic seeds.

Current learner: `ridge-log` (ridge regression trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=7.104, p90/p10=4.504, and strategy cost-over-random spans 0.03722-489.3.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.7488; median `%cost/%n`=0.1682 with IQR 0.1152-0.8443.

Cost heterogeneity: CV=7.104, p90/p10=4.504. Sample-size proxy: Spearman rho=0.7488, median `%cost/%n`=0.1682 (IQR 0.1152-0.8443).

Strategy cost-over-random range: 0.03722-489.3. Median calibration by strategy:

- `balanced`: 0.2974
- `cheapOracle`: 0.03864
- `diversity`: 1.629
- `expensiveOracle`: 55.06
- `pairwise`: 0.9861
- `pilotCost`: 0.1004
- `random`: 0.7042

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=5.538, p90/p10=2.2, and strategy cost-over-random spans 0.1799-189.2.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.8353; median `%cost/%n`=0.3578 with IQR 0.2978-0.8759.

Cost heterogeneity: CV=5.538, p90/p10=2.2. Sample-size proxy: Spearman rho=0.8353, median `%cost/%n`=0.3578 (IQR 0.2978-0.8759).

Strategy cost-over-random range: 0.1799-189.2. Median calibration by strategy:

- `balanced`: 0.4566
- `cheapOracle`: 0.1781
- `diversity`: 1.639
- `expensiveOracle`: 43.22
- `pairwise`: 0.9727
- `pilotCost`: 0.2785
- `random`: 0.7742

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in all scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0 | 0.5914 | 0.5 | `pilotCost_n256` |
| `cost=performance, target=energy` | 0.1429 | 0.5804 | 0.75 | `pairwise_n64` |
| `cost=energy, target=performance` | 0.1429 | 0.6625 | 0.7 | `pilotCost_n256` |
| `cost=energy, target=energy` | 0.4286 | 0.6416 | 0.75 | `pairwise_n64` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5; count cost selects 7 non-dominated pairs and empirical cost selects 14.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0.1429; 6 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.75; count cost selects 6 non-dominated pairs and empirical cost selects 8.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 0.1429; 6 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.7; count cost selects 7 non-dominated pairs and empirical cost selects 10.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0.4286; 4 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.75; count cost selects 6 non-dominated pairs and empirical cost selects 8.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
