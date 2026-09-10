# LinuxData report: linux507_vmlinux

## Pool

- Configurations: 20159
- Active option columns after pruning: 489
- Cost signal: `vmlinux`
- Learner: `gbt-log`
- Cost p90/p10 ratio: 4.757
- Cost CV: 0.9887
- Min / median / max cost: 1.16e+07 / 8.79e+07 / 1.999e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2115 to 7.272.
- RQ2 — Spearman ρ(n, train_cost) = 0.819; median calibration ratio = 1.009.
- RQ3 — top-1 strategy/size pair changes for 7 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00202, uncertainty_n00202, cheapOracle_n00202, uncertainty_n00403, cheapOracle_n00403, uncertainty_n01008.
  count-Pareto pairs: random_n00202, uncertainty_n00403, uncertainty_n01008.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 1.008 | 0.007923 |
| balanced | 1.009 | 0.008742 |
| diversity | 1.993 | 0.9935 |
| uncertainty | 0.8107 | -0.1893 |
| coverage | 1.01 | 0.01006 |
| cheapOracle | 0.2395 | -0.7605 |
| expensiveOracle | 6.049 | 5.049 |

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
