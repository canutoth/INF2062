# TwinsOrFalseFriends Generated-Sampling Hypothesis Checks

## Scope

Input batch: `artifacts/twins_generated_quick`.

The tests reuse the H1a--H4b operationalization in `cost_sampling/hypotheses.py`.
For this 2x2 performance/energy setting, scopes are deliberately not aggregated:

- H1/H2 are tested per system and cost property.
- H3/H4 are tested per system, cost property, and prediction target.
- H3b is a single cross-scenario correlation between cost CV and top-1 rank flips.

The main H1/H2 tests exclude the diagnostic cheap/expensive oracles; oracle calibration is reported separately.

This run has 3 stochastic seeds and row caps 5000.
H3b is evaluated across the cost-target scenarios in this batch.

## Verdict Summary

![Hypothesis verdicts](fig_twins_hypothesis_verdicts.png)

| Hypothesis | RQ | Scope | Verdict summary | Interpretation |
|---|---|---|---|---|
| H1a | RQ1 | system-cost | supported (23/28) (23 support, 2 refute, 3 inconclusive) | Per-configuration acquisition cost is usually heterogeneous. Strong-CV contexts: 16/28. |
| H1b | RQ1 | system-cost | mixed (sup=0, ref=0, inc=28 of 28) (0 support, 0 refute, 28 inconclusive) | Underpowered in this run: 28/28 scopes have large eta^2, but only 20/28 reach p<0.10. |
| H2a | RQ2 | system-cost | supported (28/28) (28 support, 0 refute, 0 inconclusive) | n is often rank-correlated with TrainCost; strong rho contexts: 14/28. |
| H2b | RQ2 | system-cost | refuted (15/28) (5 support, 15 refute, 8 inconclusive) | Aggregate median calibration is conditional, with context medians spanning 0.161-1.06. |
| H2c | RQ2 | system-cost | supported (27/28) (27 support, 0 refute, 1 inconclusive) | Calibration depends on strategy, so a single global ratio is not enough. |
| H3a | RQ3 | system-cost-target | supported (54/56) (54 support, 2 refute, 0 inconclusive) | Count-cost and empirical-cost rankings disagree in 54/56 scenarios. |
| H3b | RQ3 | global scenarios | supported (1/1) (1 support, 0 refute, 0 inconclusive) | Cross-scenario CV-to-flip relation: rho=0.657, p=3.83e-08. |
| H4a | RQ4 | system-cost-target | supported (56/56) (56 support, 0 refute, 0 inconclusive) | At least one pair flips Pareto status in most or all scenarios. |
| H4b | RQ4 | system-cost-target | supported (56/56) (56 support, 0 refute, 0 inconclusive) | Count and empirical Pareto frontiers differ in 56/56 scenarios. |

## RQ-Level Synthesis

**RQ1.** The equal-cost-per-configuration assumption is not credible for Twins overall.
H1a gives the formal support. H1b should be treated as inconclusive in this run because the fixed-n group test lacks enough statistical support, despite large observed effect sizes.
The strongest cost heterogeneity appears in:

- `jump3r` cost=`performance`: CV=7.1, p90/p10=4.5.
- `jump3r` cost=`energy`: CV=5.54, p90/p10=2.2.
- `lrzip` cost=`performance`: CV=2.18, p90/p10=26.2.
- `kanzi` cost=`energy`: CV=2.13, p90/p10=80.5.
- `brotli_1.0.7` cost=`performance`: CV=2.09, p90/p10=149.

The lowest-heterogeneity contrasts are:

- `PostgreSQL_11.2` cost=`energy`: CV=0.0575, p90/p10=1.15.
- `PostgreSQL_11.2` cost=`performance`: CV=0.0676, p90/p10=1.18.
- `LLVM` cost=`energy`: CV=0.117, p90/p10=1.37.
- `LLVM` cost=`performance`: CV=0.12, p90/p10=1.38.
- `MongoDB` cost=`performance`: CV=0.142, p90/p10=1.47.

**RQ2.** Sample size is a useful ordering proxy in many contexts, but not a complete cost model.
The median calibration ratios across system-cost contexts span 0.161-1.06, and H2c shows that strategy-specific calibration must be reported.

**RQ3.** The cost model changes cost-sensitive strategy rankings.
Top-1 recommendations change in 54/56 cost-target scenarios under the lambda sweep.
This is why performance/energy cost and performance/energy targets should be kept faceted.

**RQ4.** The Pareto-front conclusion is stronger than the scalar-ranking conclusion.
Empirical-cost and count-cost frontiers differ in 56/56 scenarios.
For paper figures, prefer the per-system frontier plots because the x-axis is an actual cost fraction and the y-axis is MRE.

## Per-Strategy Calibration Appendix

This table aggregates per-system bootstrap checks of the median calibration ratio by strategy and cost property.
The verdict is `miscalibrated` when the 95% bootstrap CI excludes 1 and the median deviation is at least 5%.
With limited stochastic repetition, deterministic strategies and oracles often have fewer than ten records per system-cost context, so `inconclusive` here usually means insufficient bootstrap sample size rather than evidence of calibration.

| Cost | Strategy | Scopes | Calibrated | Miscalibrated | Inconclusive | Median ratio | Median abs deviation |
|---|---|---:|---:|---:|---:|---:|---:|
| `energy` | `balanced` | 14 | 4 | 0 | 10 | 1 | 0.00675 |
| `energy` | `cheapOracle` | 14 | 0 | 0 | 14 | -- | -- |
| `energy` | `diversity` | 14 | 0 | 0 | 14 | -- | -- |
| `energy` | `expensiveOracle` | 14 | 0 | 0 | 14 | -- | -- |
| `energy` | `pairwise` | 14 | 0 | 0 | 14 | -- | -- |
| `energy` | `pilotCost` | 14 | 0 | 4 | 10 | 0.854 | 0.146 |
| `energy` | `random` | 14 | 3 | 0 | 11 | 0.996 | 0.0185 |
| `performance` | `balanced` | 14 | 4 | 0 | 10 | 1.01 | 0.0137 |
| `performance` | `cheapOracle` | 14 | 0 | 0 | 14 | -- | -- |
| `performance` | `diversity` | 14 | 0 | 0 | 14 | -- | -- |
| `performance` | `expensiveOracle` | 14 | 0 | 0 | 14 | -- | -- |
| `performance` | `pairwise` | 14 | 0 | 0 | 14 | -- | -- |
| `performance` | `pilotCost` | 14 | 0 | 4 | 10 | 0.83 | 0.17 |
| `performance` | `random` | 14 | 4 | 0 | 10 | 0.997 | 0.0164 |

## Output Files

- `hypothesis_tests.csv`: one row per formal H1--H4 test scope.
- `hypothesis_summary.csv`: support/refute/inconclusive counts per hypothesis.
- `strategy_calibration_tests.csv`: per-system, per-cost, per-strategy bootstrap calibration checks.
- `strategy_calibration_summary.csv`: aggregate strategy-calibration table.
- `fig_twins_hypothesis_verdicts.png`: stacked verdict-count figure.
