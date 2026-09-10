# Linux sklearn baseline

This artifact checks Linux kernel-size prediction with stronger off-the-shelf sklearn learners.
It is not the paper RQ sampling-cost pipeline; it is a diagnostic baseline against published Linux results.

## Best median MAPE

| Release | Feature set | Learner | Budget | Median MAPE | Runs |
|---|---|---|---:|---:|---:|
| `413` | `all` | `hgbt-log` | 10000 | 0.0645 | 3 |
| `413` | `topk512` | `hgbt-log` | 10000 | 0.1896 | 3 |
| `415` | `all` | `hgbt-log` | 10000 | 0.0586 | 3 |
| `415` | `topk512` | `hgbt-log` | 10000 | 0.3046 | 3 |
| `420` | `all` | `hgbt-log` | 10000 | 0.0581 | 3 |
| `420` | `topk512` | `hgbt-log` | 10000 | 0.3141 | 3 |
| `500` | `all` | `hgbt-log` | 10000 | 0.0572 | 3 |
| `500` | `topk512` | `hgbt-log` | 10000 | 0.2922 | 3 |
| `504` | `all` | `hgbt-log` | 10000 | 0.0585 | 3 |
| `504` | `topk512` | `hgbt-log` | 10000 | 0.3140 | 3 |
| `507` | `all` | `hgbt-log` | 10000 | 0.0592 | 3 |
| `507` | `topk512` | `hgbt-log` | 10000 | 0.3152 | 3 |
| `508` | `all` | `hgbt-log` | 10000 | 0.0561 | 3 |
| `508` | `topk512` | `hgbt-log` | 10000 | 0.2852 | 3 |

## Files

- `linux_sklearn_baseline_long.csv`: one row per release, feature set, learner, budget, and run.
- `linux_sklearn_baseline_summary.csv`: median/mean/min/max MAPE.
- `linux_sklearn_baseline_best.csv`: best median MAPE per release and feature set.
