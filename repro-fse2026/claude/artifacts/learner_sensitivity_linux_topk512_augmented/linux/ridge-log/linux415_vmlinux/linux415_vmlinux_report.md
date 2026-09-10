# LinuxData report: linux415_vmlinux

## Pool

- Configurations: 39391
- Active option columns after pruning: 497
- Cost signal: `vmlinux`
- Learner: `ridge-log`
- Cost p90/p10 ratio: 6.044
- Cost CV: 1.157
- Min / median / max cost: 1.154e+07 / 6.44e+07 / 1.87e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.1998 to 8.406.
- RQ2 — Spearman ρ(n, train_cost) = 0.9191; median calibration ratio = 0.9996.
- RQ3 — top-1 strategy/size pair changes for 2 / 7 λ values.
- RQ4 — empirical-Pareto pairs: balanced_n00394, cheapOracle_n00394, cheapOracle_n00788, random_n01970, balanced_n01970, balanced_n03939, random_n07878.
  count-Pareto pairs: balanced_n00394, random_n01970, balanced_n03939, random_n07878.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9992 | -0.0008208 |
| balanced | 1.002 | 0.001921 |
| cheapOracle | 0.2477 | -0.7523 |
| expensiveOracle | 4.955 | 3.955 |

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
