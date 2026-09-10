# Linux sklearn baseline

This artifact checks Linux kernel-size prediction with stronger off-the-shelf sklearn learners.
It is not the paper RQ sampling-cost pipeline; it is a diagnostic baseline against published Linux results.

## Best median MAPE

| Release | Feature set | Learner | Budget | Median MAPE | Runs |
|---|---|---|---:|---:|---:|
| `413` | `all` | `hgbt-log` | 10000 | 0.0630 | 3 |
| `413` | `topk512` | `hgbt-log` | 10000 | 0.1902 | 3 |

## Files

- `linux_sklearn_baseline_long.csv`: one row per release, feature set, learner, budget, and run.
- `linux_sklearn_baseline_summary.csv`: median/mean/min/max MAPE.
- `linux_sklearn_baseline_best.csv`: best median MAPE per release and feature set.
