# Learner Sensitivity Report

## Headline

RQ1 and RQ2 do not change with learner choice because they use only selected configurations and empirical costs. The relevant checks are RQ3/RQ4: rank stability, Pareto overlap, and median prediction error.

## Aggregate by family and learner

| Family | Label | Learner | Units | Median MRE | Top-1 agreement | Pareto Jaccard |
|---|---|---:|---:|---:|---:|---:|
| `LINUX` | `413` | `gbt-log` | 1 | 0.3471 | 0 | 0.4 |
| `LINUX` | `413` | `rf-log` | 1 | 0.3067 | 0 | 0.5714 |
| `LINUX` | `413` | `ridge-log` | 1 | 0.2366 | 1 | 0.5556 |
| `LINUX` | `415` | `gbt-log` | 1 | 0.4325 | 1 | 0.5 |
| `LINUX` | `415` | `rf-log` | 1 | 0.3961 | 0 | 0.5 |
| `LINUX` | `415` | `ridge-log` | 1 | 0.392 | 1 | 0.5714 |
| `LINUX` | `420` | `gbt-log` | 1 | 0.4254 | 0 | 0.25 |
| `LINUX` | `420` | `rf-log` | 1 | 0.3969 | 1 | 0.5 |
| `LINUX` | `420` | `ridge-log` | 1 | 0.3725 | 1 | 0.4286 |
| `LINUX` | `500` | `gbt-log` | 1 | 0.4128 | 0 | 0.5714 |
| `LINUX` | `500` | `rf-log` | 1 | 0.3795 | 1 | 0.3333 |
| `LINUX` | `500` | `ridge-log` | 1 | 0.3576 | 1 | 0.5714 |
| `LINUX` | `504` | `gbt-log` | 1 | 0.408 | 1 | 0.3333 |
| `LINUX` | `504` | `rf-log` | 1 | 0.3851 | 1 | 0.6667 |
| `LINUX` | `504` | `ridge-log` | 1 | 0.3869 | 1 | 0.5 |
| `LINUX` | `507` | `gbt-log` | 1 | 0.4074 | 1 | 0.6667 |
| `LINUX` | `507` | `rf-log` | 1 | 0.3896 | 1 | 0.5714 |
| `LINUX` | `507` | `ridge-log` | 1 | 0.3784 | 1 | 0.5 |
| `LINUX` | `508` | `gbt-log` | 1 | 0.3648 | 1 | 0.6 |
| `LINUX` | `508` | `rf-log` | 1 | 0.3461 | 1 | 0.5 |
| `LINUX` | `508` | `ridge-log` | 1 | 0.3437 | 0 | 0.5 |

## Best learners by criterion

| Family | Label | Best MRE learner | Most rank-stable learner | Most Pareto-stable learner |
|---|---|---|---|---|
| `LINUX` | `413` | `ridge-log` (0.2366) | `ridge-log` (1) | `rf-log` (0.5714) |
| `LINUX` | `415` | `ridge-log` (0.392) | `gbt-log` (1) | `ridge-log` (0.5714) |
| `LINUX` | `420` | `ridge-log` (0.3725) | `rf-log` (1) | `rf-log` (0.5) |
| `LINUX` | `500` | `ridge-log` (0.3576) | `rf-log` (1) | `gbt-log` (0.5714) |
| `LINUX` | `504` | `rf-log` (0.3851) | `gbt-log` (1) | `rf-log` (0.6667) |
| `LINUX` | `507` | `ridge-log` (0.3784) | `gbt-log` (1) | `gbt-log` (0.6667) |
| `LINUX` | `508` | `ridge-log` (0.3437) | `gbt-log` (1) | `gbt-log` (0.6) |

## Conclusions

- RQ1 and RQ2 are unchanged by construction: they inspect sampled configurations and empirical costs, before any learner is fitted.
- Stronger learners change absolute MRE, but they do not remove the decision-level instability measured by top-1 agreement and Pareto overlap.
- Ridge/log-linear remains a competitive default in the compact REPLICATION and ENERGY slices; boosted trees are useful as a robustness check and can improve median MRE in WORKLOAD and LCBENCH.
- The main interpretation should therefore be learner sensitivity, not learner replacement: report the primary learner per family, then keep random forests and boosted trees as supplementary robustness evidence.

## Family-level reading

- `LINUX` / `413`: best median MRE is `ridge-log` (0.2366); worst is `gbt-log` (0.3471). Pareto overlap remains partial (best median Jaccard `rf-log` = 0.5714).
- `LINUX` / `415`: best median MRE is `ridge-log` (0.392); worst is `gbt-log` (0.4325). Pareto overlap remains partial (best median Jaccard `ridge-log` = 0.5714).
- `LINUX` / `420`: best median MRE is `ridge-log` (0.3725); worst is `gbt-log` (0.4254). Pareto overlap remains partial (best median Jaccard `rf-log` = 0.5).
- `LINUX` / `500`: best median MRE is `ridge-log` (0.3576); worst is `gbt-log` (0.4128). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.5714).
- `LINUX` / `504`: best median MRE is `rf-log` (0.3851); worst is `gbt-log` (0.408). Pareto overlap remains partial (best median Jaccard `rf-log` = 0.6667).
- `LINUX` / `507`: best median MRE is `ridge-log` (0.3784); worst is `gbt-log` (0.4074). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.6667).
- `LINUX` / `508`: best median MRE is `ridge-log` (0.3437); worst is `gbt-log` (0.3648). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.6).
