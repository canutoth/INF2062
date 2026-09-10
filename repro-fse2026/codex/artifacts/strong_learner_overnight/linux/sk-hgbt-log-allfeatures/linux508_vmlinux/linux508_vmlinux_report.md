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
- RQ2 — Spearman ρ(n, train_cost) = 0.7814; median calibration ratio = 0.9969.
- RQ3 — top-1 strategy/size pair changes for 6 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00237, balanced_n00237, cheapOracle_n00237, random_n01184, balanced_n01184, balanced_n02368.
  count-Pareto pairs: balanced_n00237, balanced_n01184, balanced_n02368.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9932 | -0.00681 |
| balanced | 1.011 | 0.0106 |
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
