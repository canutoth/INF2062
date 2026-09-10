# LinuxData report: linux508_vmlinux

## Pool

- Configurations: 21923
- Active option columns after pruning: 494
- Cost signal: `vmlinux`
- Learner: `ridge-log`
- Cost p90/p10 ratio: 4.018
- Cost CV: 1.014
- Min / median / max cost: 1.161e+07 / 7.104e+07 / 1.998e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2802 to 8.538.
- RQ2 — Spearman ρ(n, train_cost) = 0.8178; median calibration ratio = 1.002.
- RQ3 — top-1 strategy/size pair changes for 6 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00219, balanced_n00219, uncertainty_n00219, cheapOracle_n00219, uncertainty_n00438, cheapOracle_n00438, uncertainty_n01096.
  count-Pareto pairs: balanced_n00219, uncertainty_n00438, uncertainty_n01096.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9926 | -0.007424 |
| balanced | 1.011 | 0.01147 |
| diversity | 2.094 | 1.094 |
| uncertainty | 1.008 | 0.008198 |
| coverage | 0.9983 | -0.001686 |
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
