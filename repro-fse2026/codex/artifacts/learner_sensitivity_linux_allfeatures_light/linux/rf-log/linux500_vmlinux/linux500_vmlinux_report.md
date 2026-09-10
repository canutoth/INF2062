# LinuxData report: linux500_vmlinux

## Pool

- Configurations: 19952
- Active option columns after pruning: 9733
- Cost signal: `vmlinux`
- Learner: `rf-log`
- Cost p90/p10 ratio: 5.701
- Cost CV: 1.123
- Min / median / max cost: 1.156e+07 / 6.783e+07 / 1.96e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2272 to 8.621.
- RQ2 — Spearman ρ(n, train_cost) = 0.8221; median calibration ratio = 0.9925.
- RQ3 — top-1 strategy/size pair changes for 5 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00200, balanced_n00200, cheapOracle_n00200, balanced_n00399, cheapOracle_n00399, balanced_n00998.
  count-Pareto pairs: random_n00200, balanced_n00399, balanced_n00998.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9897 | -0.01027 |
| balanced | 0.993 | -0.006973 |
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
