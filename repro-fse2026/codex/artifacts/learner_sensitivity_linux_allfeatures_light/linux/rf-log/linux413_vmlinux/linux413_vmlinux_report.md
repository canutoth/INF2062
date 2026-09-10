# LinuxData report: linux413_vmlinux

## Pool

- Configurations: 92562
- Active option columns after pruning: 8760
- Cost signal: `vmlinux`
- Learner: `rf-log`
- Cost p90/p10 ratio: 4.609
- Cost CV: 1.425
- Min / median / max cost: 1.168e+06 / 3.144e+07 / 1.781e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2339 to 11.61.
- RQ2 — Spearman ρ(n, train_cost) = 0.8221; median calibration ratio = 0.9966.
- RQ3 — top-1 strategy/size pair changes for 4 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00926, cheapOracle_n00926, balanced_n01851, cheapOracle_n01851, random_n04628, balanced_n04628.
  count-Pareto pairs: random_n00926, balanced_n01851, balanced_n04628.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9957 | -0.004262 |
| balanced | 0.999 | -0.001008 |
| cheapOracle | 0.254 | -0.746 |
| expensiveOracle | 8.691 | 7.691 |

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
