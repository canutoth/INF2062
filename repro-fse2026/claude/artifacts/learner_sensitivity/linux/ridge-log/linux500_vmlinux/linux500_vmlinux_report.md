# LinuxData report: linux500_vmlinux

## Pool

- Configurations: 19952
- Active option columns after pruning: 497
- Cost signal: `vmlinux`
- Learner: `ridge-log`
- Cost p90/p10 ratio: 5.701
- Cost CV: 1.123
- Min / median / max cost: 1.156e+07 / 6.783e+07 / 1.96e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2272 to 8.621.
- RQ2 — Spearman ρ(n, train_cost) = 0.8226; median calibration ratio = 0.99.
- RQ3 — top-1 strategy/size pair changes for 6 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00200, balanced_n00200, uncertainty_n00200, cheapOracle_n00200, cheapOracle_n00399, uncertainty_n00998.
  count-Pareto pairs: random_n00200, uncertainty_n00998.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9989 | -0.001117 |
| balanced | 0.9745 | -0.02549 |
| diversity | 2.076 | 1.076 |
| uncertainty | 0.8619 | -0.1381 |
| coverage | 0.9725 | -0.02749 |
| cheapOracle | 0.2376 | -0.7624 |
| expensiveOracle | 6.732 | 5.732 |

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
