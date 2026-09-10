# LinuxData report: linux415_vmlinux

## Pool

- Configurations: 39391
- Active option columns after pruning: 8960
- Cost signal: `vmlinux`
- Learner: `sk-hgbt-log`
- Cost p90/p10 ratio: 6.044
- Cost CV: 1.157
- Min / median / max cost: 1.154e+07 / 6.44e+07 / 1.87e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2063 to 8.413.
- RQ2 — Spearman ρ(n, train_cost) = 0.7814; median calibration ratio = 0.9997.
- RQ3 — top-1 strategy/size pair changes for 4 / 7 λ values.
- RQ4 — empirical-Pareto pairs: random_n00425, balanced_n00425, cheapOracle_n00425, balanced_n02127, balanced_n04254.
  count-Pareto pairs: balanced_n00425, balanced_n02127, balanced_n04254.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9961 | -0.003944 |
| balanced | 1.003 | 0.003315 |
| cheapOracle | 0.2502 | -0.7498 |
| expensiveOracle | 4.798 | 3.798 |

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
