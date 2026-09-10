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

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2743 to 8.071.
- RQ2 — Spearman ρ(n, train_cost) = 0.8619; median calibration ratio = 1.001.
- RQ3 — top-1 strategy/size pair changes for 5 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00237, uncertainty_n00237, coverage_n00237, cheapOracle_n00237, random_n01184, balanced_n01184, uncertainty_n01184, coverage_n01184, random_n02368, coverage_n02368.
  count-Pareto pairs: coverage_n00237, coverage_n01184, random_n02368.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9954 | -0.004568 |
| balanced | 0.997 | -0.003005 |
| diversity | 1.3 | 0.3004 |
| uncertainty | 0.6103 | -0.3897 |
| coverage | 0.9989 | -0.001069 |
| cheapOracle | 0.3218 | -0.6782 |
| expensiveOracle | 4.053 | 3.053 |

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
