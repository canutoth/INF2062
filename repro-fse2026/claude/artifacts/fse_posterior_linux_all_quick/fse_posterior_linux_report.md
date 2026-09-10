# FSE 2026 posterior-risk revisit on Linux/TuxKConfig

## Scope

This applies the FSE posterior-risk/posterior-confidence framework to Linux/TuxKConfig releases.
Important caveat: Linux is a large measured pool, not the full Linux configuration space. Posterior risk is therefore interpreted relative to the measured TuxKConfig pool.

Releases: `413,415,420,500,504,507,508`. Levels/fractions: `0.01,0.02`.
SRS generated: `True` with `5` seeds per release/level.

## Headline

Strategy posterior-risk distributions differ in 11/14 release-level scopes.
SRS is the best empirical-cost-normalized recommendation in 3/14 scopes and appears on the empirical cost/confidence Pareto frontier in 8/14 scopes.
Cost-normalization changes the top recommendation in 9/14 scopes and changes the confidence Pareto frontier in 14/14 scopes.
SRS has lower posterior risk than random in 1/14 scopes; its empirical acquisition cost differs from random in 5/14 scopes.

Best empirical-cost-normalized pairs:

- `SRSSampling_n00926`: 1/14
- `diversity_n01851`: 1/14
- `diversity_n00394`: 1/14
- `random_n00788`: 1/14
- `diversity_n00235`: 1/14
- `diversity_n00470`: 1/14
- `uncertainty_n00200`: 1/14
- `SRSSampling_n00399`: 1/14
- `diversity_n00258`: 1/14
- `diversity_n00517`: 1/14
- `SRSSampling_n00202`: 1/14
- `diversity_n00403`: 1/14
- `diversity_n00219`: 1/14
- `diversity_n00438`: 1/14

## Release-Level Summary

| Release | Level | n | Best cost pair | SRS best? | SRS on front? | Jaccard |
|---|---|---:|---|---:|---:|---:|
| `413` | `n00926` | 926 | `SRSSampling_n00926` | 1 | 1 | 0.1429 |
| `413` | `n01851` | 1851 | `diversity_n01851` | 0 | 0 | 0.1429 |
| `415` | `n00394` | 394 | `diversity_n00394` | 0 | 1 | 0.1667 |
| `415` | `n00788` | 788 | `random_n00788` | 0 | 0 | 0.1667 |
| `420` | `n00235` | 235 | `diversity_n00235` | 0 | 1 | 0.1429 |
| `420` | `n00470` | 470 | `diversity_n00470` | 0 | 0 | 0.1429 |
| `500` | `n00200` | 200 | `uncertainty_n00200` | 0 | 0 | 0.25 |
| `500` | `n00399` | 399 | `SRSSampling_n00399` | 1 | 1 | 0.1429 |
| `504` | `n00258` | 258 | `diversity_n00258` | 0 | 0 | 0.1667 |
| `504` | `n00517` | 517 | `diversity_n00517` | 0 | 1 | 0.1429 |
| `507` | `n00202` | 202 | `SRSSampling_n00202` | 1 | 1 | 0.1429 |
| `507` | `n00403` | 403 | `diversity_n00403` | 0 | 1 | 0.1429 |
| `508` | `n00219` | 219 | `diversity_n00219` | 0 | 1 | 0.1429 |
| `508` | `n00438` | 438 | `diversity_n00438` | 0 | 0 | 0.1667 |

## Budget Scaling

| Strategy | Risk non-increasing | Posterior area non-decreasing | Omega(size) >= 0 all levels | Omega(cost) >= 0 all levels |
|---|---:|---:|---:|---:|
| `random` | 6/7 | 5/7 | 1/7 | 1/7 |
| `balanced` | 6/7 | 7/7 | 3/7 | 2/7 |
| `diversity` | 7/7 | 7/7 | 7/7 | 7/7 |
| `uncertainty` | 4/7 | 4/7 | 0/7 | 0/7 |
| `coverage` | 6/7 | 6/7 | 2/7 | 2/7 |
| `SRSSampling` | 7/7 | 6/7 | 7/7 | 7/7 |
| `cheapOracle` | 7/7 | 7/7 | 0/7 | 0/7 |
| `expensiveOracle` | 7/7 | 7/7 | 7/7 | 7/7 |

For SRS, posterior risk is non-increasing in 7/7 releases and posterior area is non-decreasing in 6/7 releases.

## Applicability

Linux is applicable as a replication-plus-extension dataset if the claim is scoped to the measured pool. It is not a direct full-space replication like the FSE systems or x264 because the full valid Linux configuration space is not exhaustively measured.

## Output Files

- `posterior_linux_release_summary.csv`: release-level posterior/cost decisions.
- `posterior_linux_budget_trends.csv`: budget-scaling trends per strategy.
- `posterior_hypothesis_tests.csv`: per-release/level FSE-style tests.
- per-release folders with CSVs, reports, and figures.
