# LinuxData report: linux500_vmlinux

## Pool

- Configurations: 19952
- Active option columns after pruning: 497
- Cost signal: `vmlinux`
- Learner: `rf-log`
- Cost p90/p10 ratio: 5.701
- Cost CV: 1.123
- Min / median / max cost: 1.156e+07 / 6.783e+07 / 1.96e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2272 to 8.621.
- RQ2 — Spearman ρ(n, train_cost) = 0.9191; median calibration ratio = 0.9944.
- RQ3 — top-1 strategy/size pair changes for 3 / 7 λ values.
- RQ4 — empirical-Pareto pairs: balanced_n00200, cheapOracle_n00200, cheapOracle_n00399.
  count-Pareto pairs: balanced_n00200.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9927 | -0.007279 |
| balanced | 0.997 | -0.003048 |
| cheapOracle | 0.2609 | -0.7391 |
| expensiveOracle | 4.765 | 3.765 |

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
