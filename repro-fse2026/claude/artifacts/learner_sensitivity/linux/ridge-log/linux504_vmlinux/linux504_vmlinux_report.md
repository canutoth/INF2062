# LinuxData report: linux504_vmlinux

## Pool

- Configurations: 25847
- Active option columns after pruning: 490
- Cost signal: `vmlinux`
- Learner: `ridge-log`
- Cost p90/p10 ratio: 5.211
- Cost CV: 1.076
- Min / median / max cost: 1.159e+07 / 8.698e+07 / 2.055e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2163 to 8.713.
- RQ2 — Spearman ρ(n, train_cost) = 0.8178; median calibration ratio = 0.9954.
- RQ3 — top-1 strategy/size pair changes for 7 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00258, uncertainty_n00258, cheapOracle_n00258, uncertainty_n00517, cheapOracle_n00517, uncertainty_n01292.
  count-Pareto pairs: random_n00258, uncertainty_n00517, uncertainty_n01292.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9954 | -0.004593 |
| balanced | 1.002 | 0.002132 |
| diversity | 2.193 | 1.193 |
| uncertainty | 0.8402 | -0.1598 |
| coverage | 0.9877 | -0.01226 |
| cheapOracle | 0.225 | -0.775 |
| expensiveOracle | 6.626 | 5.626 |

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
