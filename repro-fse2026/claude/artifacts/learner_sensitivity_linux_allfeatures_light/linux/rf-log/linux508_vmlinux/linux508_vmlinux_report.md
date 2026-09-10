# LinuxData report: linux508_vmlinux

## Pool

- Configurations: 21923
- Active option columns after pruning: 10935
- Cost signal: `vmlinux`
- Learner: `rf-log`
- Cost p90/p10 ratio: 4.018
- Cost CV: 1.014
- Min / median / max cost: 1.161e+07 / 7.104e+07 / 1.998e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2799 to 8.538.
- RQ2 — Spearman ρ(n, train_cost) = 0.8221; median calibration ratio = 1.004.
- RQ3 — top-1 strategy/size pair changes for 4 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00219, cheapOracle_n00219, balanced_n00438, cheapOracle_n00438, random_n01096, balanced_n01096.
  count-Pareto pairs: random_n00219, balanced_n00438, balanced_n01096.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9979 | -0.002094 |
| balanced | 1.006 | 0.005981 |
| cheapOracle | 0.2877 | -0.7123 |
| expensiveOracle | 6.32 | 5.32 |

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
