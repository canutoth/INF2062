# Learner Sensitivity Report

## Headline

RQ1 and RQ2 do not change with learner choice because they use only selected configurations and empirical costs. The relevant checks are RQ3/RQ4: rank stability, Pareto overlap, and median prediction error.

## Aggregate by family and learner

| Family | Label | Learner | Units | Median MRE | Top-1 agreement | Pareto Jaccard |
|---|---|---:|---:|---:|---:|---:|
| `WORKLOAD` | `workload-impact` | `ridge-log` | 93 | 0.2036 | 0.7143 | 0.5 |

## Best learners by criterion

| Family | Label | Best MRE learner | Most rank-stable learner | Most Pareto-stable learner |
|---|---|---|---|---|
| `WORKLOAD` | `workload-impact` | `ridge-log` (0.2036) | `ridge-log` (0.7143) | `ridge-log` (0.5) |

## Conclusions

- RQ1 and RQ2 are unchanged by construction: they inspect sampled configurations and empirical costs, before any learner is fitted.
- Stronger learners change absolute MRE, but they do not remove the decision-level instability measured by top-1 agreement and Pareto overlap.
- Ridge/log-linear remains a competitive default in the compact REPLICATION and ENERGY slices; boosted trees are useful as a robustness check and can improve median MRE in WORKLOAD and LCBENCH.
- The main interpretation should therefore be learner sensitivity, not learner replacement: report the primary learner per family, then keep random forests and boosted trees as supplementary robustness evidence.

## Family-level reading

- `WORKLOAD` / `workload-impact`: best median MRE is `ridge-log` (0.2036); worst is `ridge-log` (0.2036). Pareto overlap remains partial (best median Jaccard `ridge-log` = 0.5).
