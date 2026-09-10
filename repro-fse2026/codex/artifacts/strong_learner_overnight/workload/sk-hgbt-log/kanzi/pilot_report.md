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
| `ambivert` | 1.439 | 0.8481 | 0.9504 | 1 / 7 | 0.8333 | `pilotCost_n64` |
| `artificl` | 0.8084 | 0.9385 | 1.002 | 3 / 7 | 0.5 | `pairwise_n64` |
| `deepfield` | 1.805 | 0.8432 | 0.9458 | 0 / 7 | 1 | `cheapOracle_n8` |
| `enwik8` | 1.761 | 0.8294 | 0.935 | 2 / 7 | 1 | `cheapOracle_n64` |
| `fannie_mae_500k` | 2.055 | 0.8234 | 0.9834 | 2 / 7 | 1 | `cheapOracle_n64` |
| `large` | 1.581 | 0.8362 | 0.9352 | 7 / 7 | 0.25 | `pilotCost_n64` |
| `misc` | 0.9088 | 0.8906 | 0.9441 | 3 / 7 | 0.5 | `pairwise_n64` |
| `silesia` | 1.808 | 0.8266 | 0.9552 | 1 / 7 | 1 | `cheapOracle_n64` |
| `vmlinux` | 2.367 | 0.5724 | 0.8229 | 2 / 7 | 1 | `cheapOracle_n64` |

## Readout

Highest heterogeneity: `vmlinux` with CV=2.367.

Least count-stable workload: `large` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `vmlinux` with Spearman rho=0.5724.

## H5a

Verdict: `supports`. K-W on 9 inputs: p=1.1e-10; eta^2=0.0131; ratio spread=0.179

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
