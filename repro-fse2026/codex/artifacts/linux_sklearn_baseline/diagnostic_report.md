# Linux sklearn baseline diagnostic

## Question

The earlier Linux learner-sensitivity runs reported MRE values around 20-35%,
which looked inconsistent with the Linux kernel-size prediction literature.
This diagnostic checks whether the discrepancy comes from the dataset itself or
from our simplified sampling/learner pipeline.

## Protocol

- Releases: Linux 4.13, 4.15, 4.20, 5.0, 5.4, 5.7, and 5.8.
- Target: `vmlinux`.
- Metric: MAPE/MRE on the held-out complement of the sampled training set.
- Training budgets: 1,000, 5,000, and 10,000 configurations.
- Runs: 3 random training samples per release, feature set, and budget.
- Strong learner: `sklearn.ensemble.HistGradientBoostingRegressor` on
  log-transformed targets.
- Feature sets:
  - `all`: all post-pruning, non-duplicate option columns.
  - `topk512`: the aggressive marginal-effect top-k feature set used by the
    earlier tractable Linux sampling pipeline.

## Main finding

The Linux dataset is not intrinsically producing 30% prediction errors. With a
strong sklearn HGBT learner and all post-pruned features, the results match the
published Linux-size prediction regime: roughly 7-8% MAPE with 5,000 training
configurations and roughly 5.6-6.5% MAPE with 10,000 training configurations.

| Release | All features, 5k | All features, 10k | Top-k 512, 10k |
|---|---:|---:|---:|
| 4.13 | 0.0760 | 0.0645 | 0.1896 |
| 4.15 | 0.0747 | 0.0586 | 0.3046 |
| 4.20 | 0.0731 | 0.0581 | 0.3141 |
| 5.0 | 0.0722 | 0.0572 | 0.2922 |
| 5.4 | 0.0751 | 0.0585 | 0.3140 |
| 5.7 | 0.0767 | 0.0592 | 0.3152 |
| 5.8 | 0.0721 | 0.0561 | 0.2852 |

## Interpretation

The discrepancy is mainly methodological:

1. The earlier Linux pipeline used dependency-free lightweight learners for
   tractability. Those are not equivalent to tuned production-grade tree
   ensembles.
2. The `topk512` feature cap is too aggressive for Linux boosted-tree
   prediction. It keeps only about 490-497 columns after duplicate removal,
   whereas the all-feature representation keeps roughly 8,760-10,935 columns.
3. A strong HGBT learner benefits substantially from the full option space.
   Under the same learner and budgets, top-k 512 remains around 19-31% MAPE at
   10,000 configurations, while all features reaches about 6%.

## Consequence for the paper

Linux should not be reported as a naturally low-accuracy dataset. The correct
story is narrower: our sampling-cost RQ pipeline used a deliberately tractable
Linux learner/feature setting, and that setting can distort the absolute MRE
scale. For Linux RQ3-RQ5 claims, the stronger baseline should either replace
the current Linux learner or be reported as a robustness correction.

RQ1 and RQ2 remain unaffected because they depend only on sampled
configurations and empirical acquisition costs.
