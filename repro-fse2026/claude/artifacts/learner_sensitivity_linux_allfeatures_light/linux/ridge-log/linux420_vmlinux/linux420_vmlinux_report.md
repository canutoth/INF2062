# LinuxData report: linux420_vmlinux

## Pool

- Configurations: 23489
- Active option columns after pruning: 9645
- Cost signal: `vmlinux`
- Learner: `ridge-log`
- Cost p90/p10 ratio: 5.796
- Cost CV: 1.16
- Min / median / max cost: 1.156e+07 / 6.36e+07 / 2.134e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2357 to 9.384.
- RQ2 — Spearman ρ(n, train_cost) = 0.8221; median calibration ratio = 0.9968.
- RQ3 — top-1 strategy/size pair changes for 5 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00235, cheapOracle_n00235, random_n00470, cheapOracle_n00470, random_n01174.
  count-Pareto pairs: random_n00235, random_n00470, random_n01174.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9818 | -0.01823 |
| balanced | 1.014 | 0.01438 |
| cheapOracle | 0.2354 | -0.7646 |
| expensiveOracle | 6.931 | 5.931 |

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
