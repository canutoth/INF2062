# LinuxData report: linux420_vmlinux

## Pool

- Configurations: 23489
- Active option columns after pruning: 9645
- Cost signal: `vmlinux`
- Learner: `sk-hgbt-log`
- Cost p90/p10 ratio: 5.796
- Cost CV: 1.16
- Min / median / max cost: 1.156e+07 / 6.36e+07 / 2.134e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2545 to 9.804.
- RQ2 — Spearman ρ(n, train_cost) = nan; median calibration ratio = 0.9128.
- RQ3 — top-1 strategy/size pair changes for 7 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00254, balanced_n00254, uncertainty_n00254, cheapOracle_n00254.
  count-Pareto pairs: balanced_n00254.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.8707 | -0.1293 |
| balanced | 1.014 | 0.0143 |
| diversity | 1.362 | 0.3623 |
| uncertainty | 0.4519 | -0.5481 |
| coverage | 0.9128 | -0.08723 |
| cheapOracle | 0.2216 | -0.7784 |
| expensiveOracle | 8.536 | 7.536 |

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
