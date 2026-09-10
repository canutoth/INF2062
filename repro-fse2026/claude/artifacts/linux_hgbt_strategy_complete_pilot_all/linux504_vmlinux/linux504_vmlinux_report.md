# LinuxData report: linux504_vmlinux

## Pool

- Configurations: 25847
- Active option columns after pruning: 10283
- Cost signal: `vmlinux`
- Learner: `sk-hgbt-log`
- Cost p90/p10 ratio: 5.211
- Cost CV: 1.076
- Min / median / max cost: 1.159e+07 / 8.698e+07 / 2.055e+09

## RQ snapshots

- RQ1 — fixed-n strategy cost overhead vs random ranges from 0.2123 to 8.271.
- RQ2 — Spearman ρ(n, train_cost) = nan; median calibration ratio = 0.9941.
- RQ3 — top-1 strategy/size pair changes for 6 / 7 λ values.
- RQ4 — empirical-Pareto pairs: uncertainty_n00279, coverage_n00279, cheapOracle_n00279.
  count-Pareto pairs: coverage_n00279.

## Calibration by strategy

| strategy | median ratio | bias |
|---|---|---|
| random | 0.9941 | -0.005909 |
| balanced | 1.083 | 0.08345 |
| diversity | 1.209 | 0.2088 |
| uncertainty | 0.4971 | -0.5029 |
| coverage | 0.9871 | -0.01289 |
| cheapOracle | 0.2111 | -0.7889 |
| expensiveOracle | 8.222 | 7.222 |

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
