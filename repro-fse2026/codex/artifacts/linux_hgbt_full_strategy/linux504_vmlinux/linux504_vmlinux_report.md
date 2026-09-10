# LinuxData report: linux504_vmlinux

## Pool

- Configurations: 25847
- Active option columns after pruning: 10283
- Cost signal: `vmlinux`
- Learner: `sk-hgbt-log`
- Cost p90/p10 ratio: 5.211
- Cost CV: 1.076
- Min / median / max cost: 1.159e+07 / 8.698e+07 / 2.055e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2078 to 8.094.
- RQ2 — Spearman ρ(n, train_cost) = 0.8487; median calibration ratio = 0.9909.
- RQ3 — top-1 strategy/size pair changes for 5 / 7 λ values.
- RQ4 — empirical-Pareto pairs: uncertainty_n00279, coverage_n00279, cheapOracle_n00279, random_n01396, balanced_n01396, uncertainty_n01396, random_n02791, uncertainty_n02791.
  count-Pareto pairs: coverage_n00279, random_n01396, random_n02791.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9941 | -0.005909 |
| balanced | 0.9851 | -0.0149 |
| diversity | 1.258 | 0.2575 |
| uncertainty | 0.5577 | -0.4423 |
| coverage | 0.996 | -0.003951 |
| cheapOracle | 0.2569 | -0.7431 |
| expensiveOracle | 4.427 | 3.427 |

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
