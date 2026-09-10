# LinuxData report: linux507_vmlinux

## Pool

- Configurations: 20159
- Active option columns after pruning: 10740
- Cost signal: `vmlinux`
- Learner: `sk-hgbt-log`
- Cost p90/p10 ratio: 4.757
- Cost CV: 0.9887
- Min / median / max cost: 1.16e+07 / 8.79e+07 / 1.999e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2065 to 6.87.
- RQ2 — Spearman ρ(n, train_cost) = nan; median calibration ratio = 1.088.
- RQ3 — top-1 strategy/size pair changes for 6 / 7 λ values.
- RQ4 — empirical-Pareto pairs: balanced_n00218, uncertainty_n00218, cheapOracle_n00218.
  count-Pareto pairs: balanced_n00218.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 1.092 | 0.09154 |
| balanced | 1.078 | 0.07825 |
| diversity | 1.252 | 0.2525 |
| uncertainty | 0.4735 | -0.5265 |
| coverage | 1.088 | 0.08756 |
| cheapOracle | 0.2254 | -0.7746 |
| expensiveOracle | 7.499 | 6.499 |

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
