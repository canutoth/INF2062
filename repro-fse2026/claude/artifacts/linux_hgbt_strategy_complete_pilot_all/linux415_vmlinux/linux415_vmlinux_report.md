# LinuxData report: linux415_vmlinux

## Pool

- Configurations: 39391
- Active option columns after pruning: 8960
- Cost signal: `vmlinux`
- Learner: `sk-hgbt-log`
- Cost p90/p10 ratio: 6.044
- Cost CV: 1.157
- Min / median / max cost: 1.154e+07 / 6.44e+07 / 1.87e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2093 to 8.534.
- RQ2 — Spearman ρ(n, train_cost) = nan; median calibration ratio = 0.9804.
- RQ3 — top-1 strategy/size pair changes for 7 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00425, balanced_n00425, uncertainty_n00425, coverage_n00425, cheapOracle_n00425.
  count-Pareto pairs: coverage_n00425.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9804 | -0.01963 |
| balanced | 0.9746 | -0.02545 |
| diversity | 1.461 | 0.4614 |
| uncertainty | 0.5496 | -0.4504 |
| coverage | 1.03 | 0.03042 |
| cheapOracle | 0.2052 | -0.7948 |
| expensiveOracle | 8.367 | 7.367 |

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
