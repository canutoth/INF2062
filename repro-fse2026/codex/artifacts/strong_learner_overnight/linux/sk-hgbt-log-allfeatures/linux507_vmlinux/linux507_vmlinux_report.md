# LinuxData report: linux507_vmlinux

## Pool

- Configurations: 20159
- Active option columns after pruning: 10740
- Cost signal: `vmlinux`
- Learner: `sk-hgbt-log`
- Cost p90/p10 ratio: 4.757
- Cost CV: 0.9887
- Min / median / max cost: 1.16e+07 / 8.79e+07 / 1.999e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2111 to 7.025.
- RQ2 — Spearman ρ(n, train_cost) = 0.7814; median calibration ratio = 1.03.
- RQ3 — top-1 strategy/size pair changes for 4 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00218, balanced_n00218, cheapOracle_n00218, random_n01089, balanced_n01089, random_n02177, balanced_n02177.
  count-Pareto pairs: random_n00218, balanced_n01089, balanced_n02177.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 1.034 | 0.03351 |
| balanced | 1.026 | 0.02648 |
| cheapOracle | 0.273 | -0.727 |
| expensiveOracle | 4.058 | 3.058 |

## Notes

- Pool-based subsampling only.  Synthesis strategies (true uniform-
  over-feasible, t-wise) are not evaluable on the published TuxKConfig
  artifact and are flagged in `LINUX_KERNEL_PLAN.md` as out of scope.
- `cheapOracle` and `expensiveOracle` are diagnostic references, not
  deployable strategies — they assume access to the cost they help
  bound.
- All MRE values are computed against the complement of the training
  sample within the same 92,562-row pool; cost = sum of `vmlinux`
  binary size over selected configurations.
