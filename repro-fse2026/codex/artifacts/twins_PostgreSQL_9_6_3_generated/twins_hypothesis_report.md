# TwinsOrFalseFriends Generated-Sampling Hypothesis Checks

## Scope

Input batch: `artifacts/twins_PostgreSQL_9_6_3_generated`.

The tests reuse the H1a--H4b operationalization in `cost_sampling/hypotheses.py`.
For this 2x2 performance/energy setting, scopes are deliberately not aggregated:

- H1/H2 are tested per system and cost property.
- H3/H4 are tested per system, cost property, and prediction target.
- H3b is a single cross-scenario correlation between cost CV and top-1 rank flips.

The main H1/H2 tests exclude the diagnostic cheap/expensive oracles; oracle calibration is reported separately.

This run has 20 stochastic seeds and no row cap recorded in the scenario summary.
H3b is descriptive only for this single-system report; use the broad batch for the cross-system H3b claim.

## Verdict Summary

![Hypothesis verdicts](fig_twins_hypothesis_verdicts.png)

| Hypothesis | RQ | Scope | Verdict summary | Interpretation |
|---|---|---|---|---|
| H1a | RQ1 | system-cost | refuted (2/2) (0 support, 2 refute, 0 inconclusive) | Per-configuration acquisition cost is usually heterogeneous. Strong-CV contexts: 0/2. |
| H1b | RQ1 | system-cost | supported (2/2) (2 support, 0 refute, 0 inconclusive) | Formal strategy-cost effects are supported in 2/2 scopes; 2/2 scopes have large eta^2. |
| H2a | RQ2 | system-cost | supported (2/2) (2 support, 0 refute, 0 inconclusive) | n is often rank-correlated with TrainCost; strong rho contexts: 2/2. |
| H2b | RQ2 | system-cost | mixed (sup=0, ref=0, inc=2 of 2) (0 support, 0 refute, 2 inconclusive) | Aggregate median calibration is conditional, with context medians spanning 0.999-0.999. |
| H2c | RQ2 | system-cost | supported (2/2) (2 support, 0 refute, 0 inconclusive) | Calibration depends on strategy, so a single global ratio is not enough. |
| H3a | RQ3 | system-cost-target | supported (3/4) (3 support, 1 refute, 0 inconclusive) | Count-cost and empirical-cost rankings disagree in 3/4 scenarios. |
| H3b | RQ3 | global scenarios | mixed (sup=0, ref=0, inc=1 of 1) (0 support, 0 refute, 1 inconclusive) | Cross-scenario CV-to-flip relation: rho=0.577, p=0.423. |
| H4a | RQ4 | system-cost-target | supported (4/4) (4 support, 0 refute, 0 inconclusive) | At least one pair flips Pareto status in most or all scenarios. |
| H4b | RQ4 | system-cost-target | supported (4/4) (4 support, 0 refute, 0 inconclusive) | Count and empirical Pareto frontiers differ in 4/4 scenarios. |

## RQ-Level Synthesis

**RQ1.** The equal-cost-per-configuration assumption is not credible for Twins overall.
H1a gives the formal support. H1b also supports strategy-induced cost differences at fixed n.
The strongest cost heterogeneity appears in:

- `twins_PostgreSQL_9_6_3_generated` cost=`performance`: CV=0.0679, p90/p10=1.18.
- `twins_PostgreSQL_9_6_3_generated` cost=`energy`: CV=0.0572, p90/p10=1.15.

The lowest-heterogeneity contrasts are:

- `twins_PostgreSQL_9_6_3_generated` cost=`energy`: CV=0.0572, p90/p10=1.15.
- `twins_PostgreSQL_9_6_3_generated` cost=`performance`: CV=0.0679, p90/p10=1.18.

**RQ2.** Sample size is a useful ordering proxy in many contexts, but not a complete cost model.
The median calibration ratios across system-cost contexts span 0.999-0.999, and H2c shows that strategy-specific calibration must be reported.

**RQ3.** The cost model changes cost-sensitive strategy rankings.
Top-1 recommendations change in 3/4 cost-target scenarios under the lambda sweep.
This is why performance/energy cost and performance/energy targets should be kept faceted.

**RQ4.** The Pareto-front conclusion is stronger than the scalar-ranking conclusion.
Empirical-cost and count-cost frontiers differ in 4/4 scenarios.
For paper figures, prefer the per-system frontier plots because the x-axis is an actual cost fraction and the y-axis is MRE.

## Per-Strategy Calibration Appendix

This table aggregates per-system bootstrap checks of the median calibration ratio by strategy and cost property.
The verdict is `miscalibrated` when the 95% bootstrap CI excludes 1 and the median deviation is at least 5%.
With limited stochastic repetition, deterministic strategies and oracles often have fewer than ten records per system-cost context, so `inconclusive` here usually means insufficient bootstrap sample size rather than evidence of calibration.

| Cost | Strategy | Scopes | Calibrated | Miscalibrated | Inconclusive | Median ratio | Median abs deviation |
|---|---|---:|---:|---:|---:|---:|---:|
| `energy` | `balanced` | 1 | 1 | 0 | 0 | 1 | 5.18e-05 |
| `energy` | `cheapOracle` | 1 | 0 | 1 | 0 | 0.922 | 0.0781 |
| `energy` | `diversity` | 1 | 1 | 0 | 0 | 0.999 | 0.000816 |
| `energy` | `expensiveOracle` | 1 | 0 | 1 | 0 | 1.1 | 0.0955 |
| `energy` | `pairwise` | 1 | 0 | 0 | 1 | 1.02 | 0.0208 |
| `energy` | `pilotCost` | 1 | 0 | 0 | 1 | 0.975 | 0.0249 |
| `energy` | `random` | 1 | 0 | 0 | 1 | 1 | 0.00184 |
| `performance` | `balanced` | 1 | 1 | 0 | 0 | 1 | 0.000123 |
| `performance` | `cheapOracle` | 1 | 0 | 1 | 0 | 0.93 | 0.0699 |
| `performance` | `diversity` | 1 | 1 | 0 | 0 | 0.998 | 0.00195 |
| `performance` | `expensiveOracle` | 1 | 0 | 1 | 0 | 1.11 | 0.111 |
| `performance` | `pairwise` | 1 | 0 | 0 | 1 | 1.03 | 0.0255 |
| `performance` | `pilotCost` | 1 | 0 | 0 | 1 | 0.969 | 0.0315 |
| `performance` | `random` | 1 | 0 | 0 | 1 | 1 | 0.00234 |

## Output Files

- `hypothesis_tests.csv`: one row per formal H1--H4 test scope.
- `hypothesis_summary.csv`: support/refute/inconclusive counts per hypothesis.
- `strategy_calibration_tests.csv`: per-system, per-cost, per-strategy bootstrap calibration checks.
- `strategy_calibration_summary.csv`: aggregate strategy-calibration table.
- `fig_twins_hypothesis_verdicts.png`: stacked verdict-count figure.
