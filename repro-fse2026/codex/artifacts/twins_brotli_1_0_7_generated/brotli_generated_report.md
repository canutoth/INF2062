# Generated sampling on TwinsOrFalseFriends `brotli`

## Scope

Source archive: `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`

Source member: `AI-4-SE-TwinsOrFalseFriends-69b208d/data/brotli/measurements.csv`

The table has 180 rows, 2 encoded feature columns, and labels `performance, energy`.

Context columns excluded from features: `revision`.

Generated budgets: `8, 9, 16, 18, 32, 36, 54` with 20 stochastic seeds.

Current learner: `ridge-log` (ridge regression trained on log-transformed targets).

Interpretation note: these results test the sampling-cost protocol, not the final learner choice. The learner is now a command-line parameter, so the same generated samples can be rerun with CART or raw-target ridge. A full replication with stepwise linear regression and a literature-aligned CART implementation should be reported as a learner-robustness extension.

The protocol uses random, feature-balanced, diversity, pairwise-coverage, and pilot-cost-aware sampling. Cheap-first and expensive-first are diagnostic oracles when enabled.

## RQ1/RQ2: cost properties

### Cost = `performance`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `performance`, CV=2.092, p90/p10=149.4, and strategy cost-over-random spans 0.01541-8.891.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.8248; median `%cost/%n`=1.014 with IQR 0.7806-1.258.

Cost heterogeneity: CV=2.092, p90/p10=149.4. Sample-size proxy: Spearman rho=0.8248, median `%cost/%n`=1.014 (IQR 0.7806-1.258).

Strategy cost-over-random range: 0.01541-8.891. Median calibration by strategy:

- `balanced`: 0.9916
- `cheapOracle`: 0.01793
- `diversity`: 1.406
- `expensiveOracle`: 6.692
- `pairwise`: 6.672
- `pilotCost`: 1.094
- `random`: 0.9464

![Calibration for performance](fig_rq2_calibration_cost_performance.png)

![Strategy cost bias for performance](fig_rq1_strategy_cost_bias_performance.png)

### Cost = `energy`

**RQ1 answer:** empirical cost is heterogeneous at fixed sample size. For `energy`, CV=1.974, p90/p10=50.06, and strategy cost-over-random spans 0.0487-8.417.

**RQ2 answer:** sample size is a strong rank proxy but not a fully calibrated cost model. Spearman rho=0.8352; median `%cost/%n`=1.017 with IQR 0.7962-1.242.

Cost heterogeneity: CV=1.974, p90/p10=50.06. Sample-size proxy: Spearman rho=0.8352, median `%cost/%n`=1.017 (IQR 0.7962-1.242).

Strategy cost-over-random range: 0.0487-8.417. Median calibration by strategy:

- `balanced`: 0.994
- `cheapOracle`: 0.05084
- `diversity`: 1.377
- `expensiveOracle`: 6.366
- `pairwise`: 6.345
- `pilotCost`: 1.096
- `random`: 0.9505

![Calibration for energy](fig_rq2_calibration_cost_energy.png)

![Strategy cost bias for energy](fig_rq1_strategy_cost_bias_energy.png)

## RQ3/RQ4: cost-target scenarios

**RQ3 answer:** replacing count cost with empirical cost changes the cost-sensitive ranking in 3 of 4 scenarios.

**RQ4 answer:** replacing count cost with empirical cost changes the non-dominated sampling choices in all scenarios.

| Scenario | Top-1 agreement | Mean tau | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---|
| `cost=performance, target=performance` | 0 | 0.6474 | 0.3333 | `cheapOracle_n54` |
| `cost=performance, target=energy` | 0 | 0.6377 | 0.2857 | `pilotCost_n9` |
| `cost=energy, target=performance` | 1 | 0.6588 | 0.5556 | `pilotCost_n16` |
| `cost=energy, target=energy` | 0 | 0.6491 | 0.3333 | `pilotCost_n9` |

![Rank agreement by scenario](fig_rq3_rank_agreement_by_scenario.png)

![Pareto Jaccard by scenario](fig_rq4_pareto_jaccard_by_scenario.png)

The Pareto-front figures below show the direct count-cost vs empirical-cost decision comparison.

### cost=performance, target=performance

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.3333; count cost selects 4 non-dominated pairs and empirical cost selects 8.

![Pareto frontier cost_performance__target_performance](fig_rq4_frontier_cost_performance__target_performance.png)

### cost=performance, target=energy

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.2857; count cost selects 3 non-dominated pairs and empirical cost selects 6.

![Pareto frontier cost_performance__target_energy](fig_rq4_frontier_cost_performance__target_energy.png)

### cost=energy, target=performance

RQ3 detail: top-1 agreement is 1; 0 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.5556; count cost selects 5 non-dominated pairs and empirical cost selects 9.

![Pareto frontier cost_energy__target_performance](fig_rq4_frontier_cost_energy__target_performance.png)

### cost=energy, target=energy

RQ3 detail: top-1 agreement is 0; 7 of 7 lambda settings select a different top recommendation under empirical cost than under count cost.

RQ4 detail: Pareto Jaccard is 0.3333; count cost selects 3 non-dominated pairs and empirical cost selects 5.

![Pareto frontier cost_energy__target_energy](fig_rq4_frontier_cost_energy__target_energy.png)

## Interpretation

This is a generated-sampling replication point: the dataset supplies measured configurations and labels, but not sample traces. Therefore, conclusions should be compared to precomputed ICPE/Kaltenecker results by protocol-aware facets, not by aggregating all rows into one table.

For paper writing, use this as the first proof that the same RQ machinery works when we must generate common strategies and a common budget grid ourselves.
