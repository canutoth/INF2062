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

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.217 to 7.992.
- RQ2 — Spearman ρ(n, train_cost) = nan; median calibration ratio = 1.038.
- RQ3 — top-1 strategy/size pair changes for 6 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00215, uncertainty_n00215, cheapOracle_n00215.
  count-Pareto pairs: random_n00215.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 1.034 | 0.03398 |
| balanced | 1.043 | 0.04313 |
| diversity | 1.215 | 0.2152 |
| uncertainty | 0.451 | -0.549 |
| coverage | 1.038 | 0.03848 |
| cheapOracle | 0.2244 | -0.7756 |
| expensiveOracle | 8.263 | 7.263 |

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
