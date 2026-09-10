# FSE 2026 posterior-risk revisit on Linux/TuxKConfig

## Scope

This applies the FSE posterior-risk/posterior-confidence framework to Linux/TuxKConfig releases.
Important caveat: Linux is a large measured pool, not the full Linux configuration space. Posterior risk is therefore interpreted relative to the measured TuxKConfig pool.

Releases: `508`. Levels/fractions: `0.01,0.02`.
SRS generated: `True` with `5` seeds per release/level.

## Headline

Strategy posterior-risk distributions differ in 2/2 release-level scopes.
SRS is the best empirical-cost-normalized recommendation in 0/2 scopes and appears on the empirical cost/confidence Pareto frontier in 1/2 scopes.
Cost-normalization changes the top recommendation in 2/2 scopes and changes the confidence Pareto frontier in 2/2 scopes.
SRS has lower posterior risk than random in 0/2 scopes; its empirical acquisition cost differs from random in 1/2 scopes.

Best empirical-cost-normalized pairs:

- `diversity_n00219`: 1/2
- `diversity_n00438`: 1/2

## Release-Level Summary

| Release | Level | n | Best cost pair | SRS best? | SRS on front? | Jaccard |
|---|---|---:|---|---:|---:|---:|
| `508` | `n00219` | 219 | `diversity_n00219` | 0 | 1 | 0.1429 |
| `508` | `n00438` | 438 | `diversity_n00438` | 0 | 0 | 0.1667 |

## Budget Scaling

| Strategy | Risk non-increasing | Posterior area non-decreasing | Omega(size) >= 0 all levels | Omega(cost) >= 0 all levels |
|---|---:|---:|---:|---:|
| `random` | 0/1 | 0/1 | 0/1 | 0/1 |
| `balanced` | 1/1 | 1/1 | 0/1 | 0/1 |
| `diversity` | 1/1 | 1/1 | 1/1 | 1/1 |
| `uncertainty` | 0/1 | 0/1 | 0/1 | 0/1 |
| `coverage` | 1/1 | 1/1 | 0/1 | 0/1 |
| `SRSSampling` | 1/1 | 1/1 | 1/1 | 1/1 |
| `cheapOracle` | 1/1 | 1/1 | 0/1 | 0/1 |
| `expensiveOracle` | 1/1 | 1/1 | 1/1 | 1/1 |

For SRS, posterior risk is non-increasing in 1/1 releases and posterior area is non-decreasing in 1/1 releases.

## Applicability

Linux is applicable as a replication-plus-extension dataset if the claim is scoped to the measured pool. It is not a direct full-space replication like the FSE systems or x264 because the full valid Linux configuration space is not exhaustively measured.

## Output Files

- `posterior_linux_release_summary.csv`: release-level posterior/cost decisions.
- `posterior_linux_budget_trends.csv`: budget-scaling trends per strategy.
- `posterior_hypothesis_tests.csv`: per-release/level FSE-style tests.
- per-release folders with CSVs, reports, and figures.
