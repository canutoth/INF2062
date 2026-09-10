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
- `REPLICATION` / `newruns`: best median MRE is `ridge-log` (0.2957); worst is `rf-log` (0.4472). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.75).
- `REPLICATION` / `x264_matrix`: best median MRE is `ridge-log` (0.07525); worst is `rf-log` (0.1555). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.4875).
- `WORKLOAD` / `workload-impact`: best median MRE is `gbt-log` (0.3188); worst is `rf-log` (0.3568). Pareto overlap remains partial (best median Jaccard `gbt-log` = 0.4).

## Execution caveat

- `LINUX` learner sensitivity did not complete in this environment (21 failed commands). The run logs show the local Python environment is missing `pyarrow`, which is required to read the TuxKConfig parquet files.
