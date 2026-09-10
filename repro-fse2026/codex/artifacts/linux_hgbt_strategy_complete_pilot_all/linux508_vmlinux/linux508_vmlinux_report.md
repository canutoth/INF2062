# LinuxData report: linux508_vmlinux

## Pool

- Configurations: 21923
- Active option columns after pruning: 10935
- Cost signal: `vmlinux`
- Learner: `sk-hgbt-log`
- Cost p90/p10 ratio: 4.018
- Cost CV: 1.014
- Min / median / max cost: 1.161e+07 / 7.104e+07 / 1.998e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2738 to 8.056.
- RQ2 — Spearman ρ(n, train_cost) = nan; median calibration ratio = 1.019.
- RQ3 — top-1 strategy/size pair changes for 6 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00237, uncertainty_n00237, coverage_n00237, cheapOracle_n00237.
  count-Pareto pairs: coverage_n00237.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.995 | -0.004971 |
| balanced | 1.034 | 0.03441 |
| diversity | 1.317 | 0.3169 |
| uncertainty | 0.5524 | -0.4476 |
| coverage | 1.019 | 0.01889 |
| cheapOracle | 0.2724 | -0.7276 |
| expensiveOracle | 8.016 | 7.016 |

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
