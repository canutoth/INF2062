# LinuxData report: linux413_vmlinux

## Pool

- Configurations: 92562
- Active option columns after pruning: 8760
- Cost signal: `vmlinux`
- Learner: `sk-hgbt-log`
- Cost p90/p10 ratio: 4.609
- Cost CV: 1.425
- Min / median / max cost: 1.168e+06 / 3.144e+07 / 1.781e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.234 to 11.16.
- RQ2 — Spearman ρ(n, train_cost) = nan; median calibration ratio = 1.002.
- RQ3 — top-1 strategy/size pair changes for 7 / 7 λ values.
- RQ4 — empirical-Pareto pairs: balanced_n01000, uncertainty_n01000, coverage_n01000, cheapOracle_n01000.
  count-Pareto pairs: coverage_n01000.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 1.002 | 0.001724 |
| balanced | 0.9825 | -0.01751 |
| diversity | 1.627 | 0.6269 |
| uncertainty | 0.6453 | -0.3547 |
| coverage | 1.002 | 0.001964 |
| cheapOracle | 0.2344 | -0.7656 |
| expensiveOracle | 11.18 | 10.18 |

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
