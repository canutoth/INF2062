# Generated sampling pilot on workload-impact `h2`

## Scope

Source archive: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip`

Source member(s): `icse22_supplementary-main/dashboard/resources/h2/sample.csv + icse22_supplementary-main/dashboard/resources/h2/measurements.csv`

Target column: `throughput`. Cost column: `throughput`.

Workloads analyzed: `smallbank-1, smallbank-10, tpcc-2, tpcc-8, voter-16, voter-2, ycsb-2400, ycsb-600`

Encoded feature columns: `32`.

This pilot reuses the Twins-style generated-sampling protocol on the measured configuration universe provided by the ICSE 2023 workload dataset. Each workload is treated as a separate context.

## Workload summary

| Workload | Cost CV | Spearman rho | Median %cost/%n | Top-1 flips | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---:|---:|---|
| `smallbank-1` | 0.1446 | 0.9773 | 0.9877 | 1 / 7 | 0.2857 | `diversity_n64` |
| `smallbank-10` | 0.154 | 0.9754 | 0.9932 | 2 / 7 | 0.3529 | `diversity_n64` |
| `tpcc-2` | 0.1053 | 0.9807 | 0.993 | 3 / 7 | 0.3077 | `diversity_n64` |
| `tpcc-8` | 0.2994 | 0.942 | 0.9886 | 7 / 7 | 0.4286 | `pilotCost_n16` |
| `voter-16` | 0.2089 | 0.9698 | 0.9916 | 1 / 7 | 0.3077 | `diversity_n64` |
| `voter-2` | 0.2098 | 0.9697 | 0.9936 | 2 / 7 | 0.3333 | `diversity_n64` |
| `ycsb-2400` | 0.1396 | 0.974 | 0.9892 | 2 / 7 | 0.4286 | `diversity_n8` |
| `ycsb-600` | 0.1687 | 0.9729 | 0.989 | 3 / 7 | 0.3077 | `diversity_n64` |

## Readout

Highest heterogeneity: `tpcc-8` with CV=0.2994.

Least count-stable workload: `tpcc-8` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `tpcc-8` with Spearman rho=0.942.

## H5a

Verdict: `refutes`. K-W on 8 inputs: p=0.62; eta^2=0; ratio spread=0.00586

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
