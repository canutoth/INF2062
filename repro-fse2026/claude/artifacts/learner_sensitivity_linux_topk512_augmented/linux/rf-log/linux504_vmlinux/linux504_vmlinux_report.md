# LinuxData report: linux504_vmlinux

## Pool

- Configurations: 25847
- Active option columns after pruning: 490
- Cost signal: `vmlinux`
- Learner: `rf-log`
- Cost p90/p10 ratio: 5.211
- Cost CV: 1.076
- Min / median / max cost: 1.159e+07 / 8.698e+07 / 2.055e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2163 to 8.713.
- RQ2 — Spearman ρ(n, train_cost) = 0.9191; median calibration ratio = 0.9955.
- RQ3 — top-1 strategy/size pair changes for 3 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00258, cheapOracle_n00258, balanced_n00517, cheapOracle_n00517, random_n01292, random_n05169.
  count-Pareto pairs: random_n00258, balanced_n00517, random_n01292, random_n05169.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9967 | -0.00329 |
| balanced | 0.9942 | -0.005796 |
| cheapOracle | 0.2538 | -0.7462 |
| expensiveOracle | 4.579 | 3.579 |

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
