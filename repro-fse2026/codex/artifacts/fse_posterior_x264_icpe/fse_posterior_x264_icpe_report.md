# FSE 2026 posterior-risk revisit on ICPE x264

## Scope

This experiment reuses the FSE 2026 posterior risk, posterior confidence, and integrated confidence discrepancy outcomes on the REPLICATION-ICPE x264 corpus.

Target properties: `time,size`. Empirical acquisition cost property: `time`.
Levels: `t1,t2,t3`. Fixed-budget summary level: `t2`.
SRS generated: `True` with `100` seeds per context/level.

The fixed-budget part corresponds to the FSE paper's first experiment: do posterior risk and confidence reveal meaningful differences between strategies at the same sample size?

The budget-scaling part corresponds to the FSE paper's second experiment: do posterior risk and confidence improve as the sample size increases?

## Headline

At `t2`, strategy posterior-risk distributions differ in 34/34 x264 target contexts.

SRS is the best empirical-cost-normalized recommendation in 26/34 contexts and appears on the empirical cost/confidence Pareto frontier in 29/34 contexts.

Cost-normalization changes the top integrated-confidence recommendation in 2/34 contexts and changes the confidence Pareto frontier in 30/34 contexts.

SRS has lower posterior risk than random sampling in 34/34 contexts at `t2`; its empirical acquisition cost differs from random in 33/34 contexts.

## FSE Experiment 1 Revisited: Fixed Sample Size

| Target | Best empirical-cost-normalized pair counts |
|---|---|
| `size` | `SRSSampling_t2`=11; `henard_t2`=5; `divDistBased_t2`=1 |
| `time` | `SRSSampling_t2`=15; `divDistBased_t2`=2 |

| Target | Contexts | SRS best | SRS on Pareto front | Cost changed top | Pareto changed |
|---|---:|---:|---:|---:|---:|
| `size` | 17 | 11 | 13 | 1 | 13 |
| `time` | 17 | 15 | 16 | 1 | 17 |

Interpretation: the FSE posterior outcomes transfer to x264: they do separate strategies at the same nominal budget. The cost-aware qualification also transfers: equal sample size does not necessarily mean equal acquisition effort.

## FSE Experiment 2 Revisited: Increasing Sample Size

| Strategy | Risk non-increasing | Posterior area non-decreasing | Omega(size) >= 0 for all levels | Omega(cost) >= 0 for all levels |
|---|---:|---:|---:|---:|
| `random` | 34/34 | 34/34 | 3/34 | 7/34 |
| `solverBased` | 34/34 | 34/34 | 0/34 | 0/34 |
| `henard` | 34/34 | 34/34 | 1/34 | 1/34 |
| `distBased` | 34/34 | 34/34 | 1/34 | 1/34 |
| `divDistBased` | 34/34 | 34/34 | 8/34 | 9/34 |
| `twise` | 34/34 | 34/34 | 9/34 | 9/34 |
| `SRSSampling` | 34/34 | 34/34 | 10/34 | 10/34 |

For SRS specifically, posterior risk is non-increasing in 34/34 contexts and integrated posterior confidence is non-decreasing in 34/34 contexts.

## Practical Take-Away

Yes, the FSE 2026 paper can be revisited on REPLICATION-ICPE/x264. The required ingredients are present: a known configuration universe, measured target values, repeated sampling traces for existing strategies, and enough configuration features to generate SRS.

The scientific question should be phrased as a replication-plus-extension:

1. Replication of FSE: do posterior risk/confidence distinguish strategies and improve with budget?
2. Extension from our paper: do those posterior guarantees still support the same recommendation after empirical acquisition cost replaces sample size?

## Output Files

- `posterior_x264_context_summary.csv`: one row per input/target/level.
- `posterior_x264_budget_trends.csv`: budget-scaling trends per strategy and context.
- `posterior_hypothesis_tests.csv`: FSE-style fixed-level and per-level tests.
- `posterior_strategy_summary.csv`: all per-strategy posterior summaries.
- per-context folders with reports, CSVs, and figures.
