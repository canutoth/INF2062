# Learner Sensitivity Report

## Headline

RQ1 and RQ2 do not change with learner choice because they use only selected configurations and empirical costs. The relevant checks are RQ3/RQ4: rank stability, Pareto overlap, and median prediction error.

## Aggregate by family and learner

| Family | Label | Learner | Units | Median MRE | Top-1 agreement | Pareto Jaccard |
|---|---|---:|---:|---:|---:|---:|
| `LINUX` | `413` | `gbt-log` | 1 | 0.3685 | 0 | 0.6 |
| `LINUX` | `413` | `rf-log` | 1 | 0.3631 | 0 | 0.5 |
| `LINUX` | `413` | `ridge-log` | 1 | 0.3131 | 0 | 0.5 |
| `LINUX` | `415` | `gbt-log` | 1 | 0.4684 | 0 | 0.4286 |
| `LINUX` | `415` | `rf-log` | 1 | 0.4497 | 0 | 0.4286 |
| `LINUX` | `415` | `ridge-log` | 1 | 0.3625 | 0 | 0.4286 |
| `LINUX` | `420` | `gbt-log` | 1 | 0.4508 | 0 | 0.5 |
| `LINUX` | `420` | `rf-log` | 1 | 0.4585 | 0 | 0.5 |
| `LINUX` | `420` | `ridge-log` | 1 | 0.3682 | 0 | 0.6 |
| `LINUX` | `500` | `gbt-log` | 1 | 0.4618 | 0 | 0.4 |
| `LINUX` | `500` | `rf-log` | 1 | 0.4615 | 0 | 0.5 |
| `LINUX` | `500` | `ridge-log` | 1 | 0.382 | 0 | 0.6 |
| `LINUX` | `504` | `gbt-log` | 1 | 0.4354 | 0 | 0.5 |
| `LINUX` | `504` | `rf-log` | 1 | 0.4468 | 0 | 0.5 |
| `LINUX` | `504` | `ridge-log` | 1 | 0.3612 | 0 | 0.5 |
| `LINUX` | `507` | `gbt-log` | 1 | 0.411 | 0 | 0.5 |
| `LINUX` | `507` | `rf-log` | 1 | 0.4243 | 0 | 0.4286 |
| `LINUX` | `507` | `ridge-log` | 1 | 0.3535 | 0 | 0.5 |
| `LINUX` | `508` | `gbt-log` | 1 | 0.3836 | 0 | 0.5 |
| `LINUX` | `508` | `rf-log` | 1 | 0.3801 | 0 | 0.5 |
| `LINUX` | `508` | `ridge-log` | 1 | 0.3512 | 0 | 0.6 |

## Best learners by criterion

| Family | Label | Best MRE learner | Most rank-stable learner | Most Pareto-stable learner |
|---|---|---|---|---|
| `LINUX` | `413` | `ridge-log` (0.3131) | `gbt-log` (0) | `gbt-log` (0.6) |
| `LINUX` | `415` | `ridge-log` (0.3625) | `gbt-log` (0) | `gbt-log` (0.4286) |
| `LINUX` | `420` | `ridge-log` (0.3682) | `gbt-log` (0) | `ridge-log` (0.6) |
| `LINUX` | `500` | `ridge-log` (0.382) | `gbt-log` (0) | `ridge-log` (0.6) |
| `LINUX` | `504` | `ridge-log` (0.3612) | `gbt-log` (0) | `gbt-log` (0.5) |
| `LINUX` | `507` | `ridge-log` (0.3535) | `gbt-log` (0) | `gbt-log` (0.5) |
| `LINUX` | `508` | `ridge-log` (0.3512) | `gbt-log` (0) | `ridge-log` (0.6) |

## Conclusions

- RQ1 and RQ2 are unchanged by construction: they inspect sampled configurations and empirical costs, before any learner is fitted.
- Stronger learners change absolute MRE, but they do not remove the decision-level instability measured by top-1 agreement and Pareto overlap.
- Ridge/log-linear remains a competitive default in the compact REPLICATION and ENERGY slices; boosted trees are useful as a robustness check and can improve median MRE in WORKLOAD and LCBENCH.
- The main interpretation should therefore be learner sensitivity, not learner replacement: report the primary learner per family, then keep random forests and boosted trees as supplementary robustness evidence.

## Family-level reading

- `LINUX` / `413`: best median MRE is `ridge-log` (0.3131); worst is `gbt-log` (0.3685). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.6).
- `LINUX` / `415`: best median MRE is `ridge-log` (0.3625); worst is `gbt-log` (0.4684). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.4286).
- `LINUX` / `420`: best median MRE is `ridge-log` (0.3682); worst is `rf-log` (0.4585). Pareto overlap remains partial (best median Jaccard `ridge-log` = 0.6).
- `LINUX` / `500`: best median MRE is `ridge-log` (0.382); worst is `gbt-log` (0.4618). Pareto overlap remains partial (best median Jaccard `ridge-log` = 0.6).
- `LINUX` / `504`: best median MRE is `ridge-log` (0.3612); worst is `rf-log` (0.4468). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.5).
- `LINUX` / `507`: best median MRE is `ridge-log` (0.3535); worst is `rf-log` (0.4243). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.5).
- `LINUX` / `508`: best median MRE is `ridge-log` (0.3512); worst is `gbt-log` (0.3836). Pareto overlap remains partial (best median Jaccard `ridge-log` = 0.6).
