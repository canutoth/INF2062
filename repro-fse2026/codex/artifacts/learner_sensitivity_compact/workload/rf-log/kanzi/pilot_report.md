# Generated sampling pilot on workload-impact `kanzi`

## Scope

Source archive: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip`

Source member(s): `icse22_supplementary-main/dashboard/resources/kanzi/sample.csv + icse22_supplementary-main/dashboard/resources/kanzi/measurements.csv`

Target column: `time`. Cost column: `time`.

Workloads analyzed: `ambivert, artificl, deepfield, enwik8, fannie_mae_500k, large, misc, silesia, vmlinux`

Encoded feature columns: `48`.

This pilot reuses the Twins-style generated-sampling protocol on the measured configuration universe provided by the ICSE 2023 workload dataset. Each workload is treated as a separate context.

## Workload summary

| Workload | Cost CV | Spearman rho | Median %cost/%n | Top-1 flips | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---:|---:|---|
| `ambivert` | 1.439 | 0.4509 | 0.9251 | 7 / 7 | 0.5 | `random_n16` |
| `artificl` | 0.8084 | 0.4856 | 0.9952 | 4 / 7 | 0.3333 | `pilotCost_n8` |
| `deepfield` | 1.805 | 0.3989 | 0.9604 | 0 / 7 | 1 | `cheapOracle_n8` |
| `enwik8` | 1.761 | 0.3989 | 0.9397 | 7 / 7 | 0.3333 | `random_n8` |
| `fannie_mae_500k` | 2.055 | 0.2601 | 0.924 | 7 / 7 | 0.3333 | `cheapOracle_n16` |
| `large` | 1.581 | 0.3989 | 0.9372 | 5 / 7 | 0.3333 | `random_n8` |
| `misc` | 0.9088 | 0.4682 | 1.009 | 4 / 7 | 0.5 | `random_n16` |
| `silesia` | 1.808 | 0.3122 | 0.9232 | 7 / 7 | 0.3333 | `random_n8` |
| `vmlinux` | 2.367 | 0.4682 | 0.6399 | 7 / 7 | 0.3333 | `pilotCost_n8` |

## Readout

Highest heterogeneity: `vmlinux` with CV=2.367.

Least count-stable workload: `ambivert` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `fannie_mae_500k` with Spearman rho=0.2601.

## H5a

Verdict: `refutes`. K-W on 9 inputs: p=0.915; eta^2=0; ratio spread=0.369

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
