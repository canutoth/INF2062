# LinuxData report: linux500_vmlinux

## Pool

- Configurations: 19952
- Active option columns after pruning: 9733
- Cost signal: `vmlinux`
- Learner: `sk-hgbt-log`
- Cost p90/p10 ratio: 5.701
- Cost CV: 1.123
- Min / median / max cost: 1.156e+07 / 6.783e+07 / 1.96e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2293 to 8.444.
- RQ2 — Spearman ρ(n, train_cost) = 0.7814; median calibration ratio = 0.9868.
- RQ3 — top-1 strategy/size pair changes for 4 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00215, cheapOracle_n00215, random_n01077, balanced_n01077, random_n02155, balanced_n02155.
  count-Pareto pairs: random_n00215, random_n01077, random_n02155.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9916 | -0.008449 |
| balanced | 0.9821 | -0.01791 |
| cheapOracle | 0.2632 | -0.7368 |
| expensiveOracle | 4.617 | 3.617 |

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
