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

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2271 to 8.747.
- RQ2 — Spearman ρ(n, train_cost) = 0.8432; median calibration ratio = 0.9833.
- RQ3 — top-1 strategy/size pair changes for 6 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00254, balanced_n00254, uncertainty_n00254, cheapOracle_n00254, random_n01268, balanced_n01268, uncertainty_n01268, coverage_n01268, random_n02537, balanced_n02537, uncertainty_n02537, coverage_n02537.
  count-Pareto pairs: balanced_n00254, coverage_n01268, balanced_n02537.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9825 | -0.01753 |
| balanced | 0.9931 | -0.006854 |
| diversity | 1.406 | 0.406 |
| uncertainty | 0.6023 | -0.3977 |
| coverage | 0.994 | -0.006013 |
| cheapOracle | 0.2624 | -0.7376 |
| expensiveOracle | 4.721 | 3.721 |

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
