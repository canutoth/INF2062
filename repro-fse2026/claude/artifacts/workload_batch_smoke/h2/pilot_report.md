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
| `smallbank-1` | 0.1446 | 0.8682 | 0.9828 | 3 / 7 | 0.2857 | `balanced_n16` |
| `smallbank-10` | 0.154 | 0.8682 | 1.006 | 2 / 7 | 0.3333 | `balanced_n16` |
| `tpcc-2` | 0.1053 | 0.8682 | 0.9951 | 2 / 7 | 0.4 | `balanced_n16` |
| `tpcc-8` | 0.2994 | 0.5847 | 1.01 | 4 / 7 | 0.4 | `pilotCost_n16` |
| `voter-16` | 0.2089 | 0.8682 | 0.9795 | 2 / 7 | 0.25 | `random_n16` |
| `voter-2` | 0.2098 | 0.8328 | 0.976 | 2 / 7 | 0.3333 | `balanced_n16` |
| `ycsb-2400` | 0.1396 | 0.8328 | 0.9952 | 2 / 7 | 0.3333 | `random_n16` |
| `ycsb-600` | 0.1687 | 0.8328 | 0.9875 | 4 / 7 | 0.3333 | `random_n16` |

## Readout

Highest heterogeneity: `tpcc-8` with CV=0.2994.

Least count-stable workload: `tpcc-8` with 4 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `tpcc-8` with Spearman rho=0.5847.

## H5a

Verdict: `refutes`. K-W on 8 inputs: p=0.945; eta^2=0; ratio spread=0.0336

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
