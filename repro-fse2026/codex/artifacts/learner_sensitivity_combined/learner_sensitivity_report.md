# Learner Sensitivity Report

## Headline

RQ1 and RQ2 do not change with learner choice because they use only selected configurations and empirical costs. The relevant checks are RQ3/RQ4: rank stability, Pareto overlap, and median prediction error.

## Aggregate by family and learner

| Family | Label | Learner | Units | Median MRE | Top-1 agreement | Pareto Jaccard |
|---|---|---:|---:|---:|---:|---:|
| `ENERGY` | `twins` | `gbt-log` | 56 | 0.2573 | 0.4286 | 0.4 |
| `ENERGY` | `twins` | `rf-log` | 56 | 0.2947 | 0.3571 | 0.5 |
| `ENERGY` | `twins` | `ridge-log` | 56 | 0.1893 | 0.2857 | 0.5 |
| `LCBENCH` | `data_2k_lw` | `gbt-raw` | 35 | 0.1366 | 0.2857 | 0.4 |
| `LCBENCH` | `data_2k_lw` | `rf-raw` | 35 | 0.1344 | 0.2857 | 0.5 |
| `LCBENCH` | `data_2k_lw` | `ridge-raw` | 35 | 0.1345 | 0.2857 | 0.5 |
| `LINUX` | `413` | `gbt-log` | 1 | 0.3003 | 0 | 0.5 |
| `LINUX` | `413` | `rf-log` | 1 | 0.3067 | 0 | 0.4286 |
| `LINUX` | `413` | `ridge-log` | 1 | 0.2383 | 1 | 0.4286 |
| `LINUX` | `415` | `gbt-log` | 1 | 0.3993 | 0 | 0.4286 |
| `LINUX` | `415` | `rf-log` | 1 | 0.3866 | 0 | 0.375 |
| `LINUX` | `415` | `ridge-log` | 1 | 0.3426 | 1 | 0.2 |
| `LINUX` | `420` | `gbt-log` | 1 | 0.4191 | 0 | 0.6 |
| `LINUX` | `420` | `rf-log` | 1 | 0.3903 | 0 | 0.6 |
| `LINUX` | `420` | `ridge-log` | 1 | 0.3411 | 1 | 0.3333 |
| `LINUX` | `500` | `gbt-log` | 1 | 0.3761 | 1 | 0.6 |
| `LINUX` | `500` | `rf-log` | 1 | 0.3691 | 0 | 0.5 |
| `LINUX` | `500` | `ridge-log` | 1 | 0.3233 | 0 | 0.3333 |
| `LINUX` | `504` | `gbt-log` | 1 | 0.3739 | 1 | 0.5 |
| `LINUX` | `504` | `rf-log` | 1 | 0.38 | 1 | 0.6 |
| `LINUX` | `504` | `ridge-log` | 1 | 0.3438 | 0 | 0.5 |
| `LINUX` | `507` | `gbt-log` | 1 | 0.3664 | 0 | 0.5 |
| `LINUX` | `507` | `rf-log` | 1 | 0.3728 | 0 | 0.4286 |
| `LINUX` | `507` | `ridge-log` | 1 | 0.3673 | 0 | 0.4 |
| `LINUX` | `508` | `gbt-log` | 1 | 0.3651 | 0 | 0.5 |
| `LINUX` | `508` | `rf-log` | 1 | 0.3461 | 0 | 0.5 |
| `LINUX` | `508` | `ridge-log` | 1 | 0.3138 | 0 | 0.4286 |
| `REPLICATION` | `newruns` | `gbt-log` | 2 | 0.4451 | nan | 0.75 |
| `REPLICATION` | `newruns` | `rf-log` | 2 | 0.4472 | nan | 0.4286 |
| `REPLICATION` | `newruns` | `ridge-log` | 2 | 0.2957 | nan | 0.5208 |
| `REPLICATION` | `x264_matrix` | `gbt-log` | 4 | 0.1268 | nan | 0.4875 |
| `REPLICATION` | `x264_matrix` | `rf-log` | 4 | 0.1555 | nan | 0.3375 |
| `REPLICATION` | `x264_matrix` | `ridge-log` | 4 | 0.07525 | nan | 0.4375 |
| `WORKLOAD` | `workload-impact` | `gbt-log` | 93 | 0.3188 | 0.4286 | 0.4 |
| `WORKLOAD` | `workload-impact` | `rf-log` | 93 | 0.3568 | 0.4286 | 0.4 |
| `WORKLOAD` | `workload-impact` | `ridge-log` | 93 | 0.3361 | 0.4286 | 0.4 |

## Best learners by criterion

| Family | Label | Best MRE learner | Most rank-stable learner | Most Pareto-stable learner |
|---|---|---|---|---|
| `ENERGY` | `twins` | `ridge-log` (0.1893) | `gbt-log` (0.4286) | `rf-log` (0.5) |
| `LCBENCH` | `data_2k_lw` | `rf-raw` (0.1344) | `gbt-raw` (0.2857) | `rf-raw` (0.5) |
| `LINUX` | `413` | `ridge-log` (0.2383) | `ridge-log` (1) | `gbt-log` (0.5) |
| `LINUX` | `415` | `ridge-log` (0.3426) | `ridge-log` (1) | `gbt-log` (0.4286) |
| `LINUX` | `420` | `ridge-log` (0.3411) | `ridge-log` (1) | `gbt-log` (0.6) |
| `LINUX` | `500` | `ridge-log` (0.3233) | `gbt-log` (1) | `gbt-log` (0.6) |
| `LINUX` | `504` | `ridge-log` (0.3438) | `gbt-log` (1) | `rf-log` (0.6) |
| `LINUX` | `507` | `gbt-log` (0.3664) | `gbt-log` (0) | `gbt-log` (0.5) |
| `LINUX` | `508` | `ridge-log` (0.3138) | `gbt-log` (0) | `gbt-log` (0.5) |
| `REPLICATION` | `newruns` | `ridge-log` (0.2957) | `NA` (nan) | `gbt-log` (0.75) |
| `REPLICATION` | `x264_matrix` | `ridge-log` (0.07525) | `NA` (nan) | `gbt-log` (0.4875) |
| `WORKLOAD` | `workload-impact` | `gbt-log` (0.3188) | `gbt-log` (0.4286) | `gbt-log` (0.4) |

## Conclusions

- RQ1 and RQ2 are unchanged by construction: they inspect sampled configurations and empirical costs, before any learner is fitted.
- Stronger learners change absolute MRE, but they do not remove the decision-level instability measured by top-1 agreement and Pareto overlap.
- Ridge/log-linear remains a competitive default in the compact REPLICATION and ENERGY slices; boosted trees are useful as a robustness check and can improve median MRE in WORKLOAD and LCBENCH.
- The main interpretation should therefore be learner sensitivity, not learner replacement: report the primary learner per family, then keep random forests and boosted trees as supplementary robustness evidence.

## Family-level reading

- `ENERGY` / `twins`: best median MRE is `ridge-log` (0.1893); worst is `rf-log` (0.2947). Pareto overlap remains partial (best median Jaccard `rf-log` = 0.5).
- `LCBENCH` / `data_2k_lw`: best median MRE is `rf-raw` (0.1344); worst is `gbt-raw` (0.1366). Pareto overlap remains partial (best median Jaccard `rf-raw` = 0.5).
- `LINUX` / `413`: best median MRE is `ridge-log` (0.2383); worst is `rf-log` (0.3067). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.5).
- `LINUX` / `415`: best median MRE is `ridge-log` (0.3426); worst is `gbt-log` (0.3993). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.4286).
- `LINUX` / `420`: best median MRE is `ridge-log` (0.3411); worst is `gbt-log` (0.4191). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.6).
- `LINUX` / `500`: best median MRE is `ridge-log` (0.3233); worst is `gbt-log` (0.3761). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.6).
- `LINUX` / `504`: best median MRE is `ridge-log` (0.3438); worst is `rf-log` (0.38). Pareto overlap remains partial (best median Jaccard `rf-log` = 0.6).
- `LINUX` / `507`: best median MRE is `gbt-log` (0.3664); worst is `rf-log` (0.3728). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.5).
- `LINUX` / `508`: best median MRE is `ridge-log` (0.3138); worst is `gbt-log` (0.3651). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.5).
- `REPLICATION` / `newruns`: best median MRE is `ridge-log` (0.2957); worst is `rf-log` (0.4472). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.75).
- `REPLICATION` / `x264_matrix`: best median MRE is `ridge-log` (0.07525); worst is `rf-log` (0.1555). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.4875).
- `WORKLOAD` / `workload-impact`: best median MRE is `gbt-log` (0.3188); worst is `rf-log` (0.3568). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.4).
