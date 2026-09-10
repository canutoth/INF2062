# LinuxData report: linux413_vmlinux

## Pool

- Configurations: 92562
- Active option columns after pruning: 495
- Cost signal: `vmlinux`
- Learner: `gbt-log`
- Cost p90/p10 ratio: 4.609
- Cost CV: 1.425
- Min / median / max cost: 1.168e+06 / 3.144e+07 / 1.781e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2339 to 11.61.
- RQ2 — Spearman ρ(n, train_cost) = 0.907; median calibration ratio = 0.9994.
- RQ3 — top-1 strategy/size pair changes for 4 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00926, balanced_n00926, cheapOracle_n00926, balanced_n01851, cheapOracle_n01851.
  count-Pareto pairs: balanced_n00926, balanced_n01851.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9994 | -0.0005973 |
| balanced | 0.9989 | -0.001058 |
| cheapOracle | 0.2919 | -0.7081 |
| expensiveOracle | 5.64 | 4.64 |

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
