# Linux HGBT all-feature cross-release report

## Scope

This report summarizes the strong-learner Linux batch: `sk-hgbt-log`, all post-pruning feature columns, and approximately 1k/5k/10k generated training budgets across seven Linux releases.

The older Linux report remains the reproducibility-oriented baseline. This report is the strong-default learner view for the learner-sensitivity question.

## Main Findings

- Best observed deployable MRE is `0.06361` on `v4.13` with `coverage_n09997` at `0.1073` empirical cost fraction.
- Cost heterogeneity remains high in every release: CV ranges `0.9887`-`1.425`.
- Count-cost calibration is close at the aggregate level: median `%cost/%n` ranges `0.9833`-`1.005`.
- Decision-level Pareto disagreement remains visible: worst release is `v4.20` with Jaccard `0.25`.

![Cross-release metrics](fig_linux_hgbt_release_metrics.png)

![Strategy MRE by release](fig_linux_hgbt_strategy_mre.png)

## Release Summary

| Release | Features | Configs | Cost CV | Proxy ratio | Top-1 agreement | Pareto Jaccard | Best MRE pair | Best MRE |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| `v4.13` | 8760 | 92562 | 1.425 | 1.002 | 0.4286 | 0.375 | `coverage_n09997` | 0.06361 |
| `v4.15` | 8960 | 39391 | 1.157 | 0.9939 | 0.2857 | 0.2727 | `balanced_n04254` | 0.07892 |
| `v4.20` | 9645 | 23489 | 1.16 | 0.9833 | 0.1429 | 0.25 | `balanced_n02537` | 0.09636 |
| `v5.0` | 9733 | 19952 | 1.123 | 1.004 | 0.2857 | 0.2727 | `coverage_n02155` | 0.1028 |
| `v5.04` | 10283 | 25847 | 1.076 | 0.9909 | 0.2857 | 0.375 | `random_n02791` | 0.09335 |
| `v5.07` | 10740 | 20159 | 0.9887 | 1.005 | 0.1429 | 0.3 | `balanced_n02177` | 0.1069 |
| `v5.08` | 10935 | 21923 | 1.014 | 1.001 | 0.2857 | 0.3 | `random_n02368` | 0.09595 |

## Hypothesis Summary

| Hypothesis | Verdict | Supports | Refutes | Inconclusive |
|---|---|---:|---:|---:|
| `H1a` | supported (7/7) | 7 | 0 | 0 |
| `H1b` | supported (7/7) | 7 | 0 | 0 |
| `H2a` | supported (7/7) | 7 | 0 | 0 |
| `H2b` | refuted (7/7) | 0 | 7 | 0 |
| `H2c` | supported (6/7) | 6 | 0 | 1 |
| `H3a` | supported (7/7) | 7 | 0 | 0 |
| `H4a` | supported (7/7) | 7 | 0 | 0 |
| `H4b` | supported (7/7) | 7 | 0 | 0 |

## Output Files

- `release_summary.csv`: one row per Linux release.
- `all_strategy_summary.csv`, `all_records.csv`, `all_rq*_*.csv`: concatenated per-release artifacts.
- `hypothesis_tests.csv` and `hypothesis_summary.csv`: H1a-H4b tests over release scopes.
- `fig_linux_hgbt_release_metrics.png` and `fig_linux_hgbt_strategy_mre.png`: cross-release figures.
