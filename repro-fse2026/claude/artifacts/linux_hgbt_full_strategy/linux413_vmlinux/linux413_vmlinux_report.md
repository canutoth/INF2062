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

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2371 to 11.31.
- RQ2 — Spearman ρ(n, train_cost) = 0.8186; median calibration ratio = 1.002.
- RQ3 — top-1 strategy/size pair changes for 4 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n01000, uncertainty_n01000, cheapOracle_n01000, random_n04998, balanced_n04998, uncertainty_n04998, balanced_n09997, coverage_n09997.
  count-Pareto pairs: random_n01000, balanced_n04998, coverage_n09997.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9887 | -0.01131 |
| balanced | 1.009 | 0.008774 |
| diversity | 1.524 | 0.5244 |
| uncertainty | 0.749 | -0.251 |
| coverage | 0.9964 | -0.003571 |
| cheapOracle | 0.2953 | -0.7047 |
| expensiveOracle | 5.424 | 4.424 |

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
