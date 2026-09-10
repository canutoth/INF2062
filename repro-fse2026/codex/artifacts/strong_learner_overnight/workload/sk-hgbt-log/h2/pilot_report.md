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
| `smallbank-1` | 0.1446 | 0.9838 | 0.9898 | 0 / 7 | 0.2857 | `diversity_n64` |
| `smallbank-10` | 0.154 | 0.9814 | 0.9932 | 2 / 7 | 0.375 | `diversity_n64` |
| `tpcc-2` | 0.1053 | 0.9849 | 0.9917 | 1 / 7 | 0.2857 | `diversity_n64` |
| `tpcc-8` | 0.2994 | 0.9758 | 0.9955 | 0 / 7 | 0.3333 | `pilotCost_n8` |
| `voter-16` | 0.2089 | 0.9717 | 0.9908 | 1 / 7 | 0.3333 | `diversity_n64` |
| `voter-2` | 0.2098 | 0.9715 | 0.9913 | 2 / 7 | 0.3077 | `diversity_n64` |
| `ycsb-2400` | 0.1396 | 0.9836 | 0.9869 | 2 / 7 | 0.3333 | `diversity_n8` |
| `ycsb-600` | 0.1687 | 0.9833 | 0.9784 | 3 / 7 | 0.3077 | `diversity_n64` |

## Readout

Highest heterogeneity: `tpcc-8` with CV=0.2994.

Least count-stable workload: `ycsb-600` with 3 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `voter-2` with Spearman rho=0.9715.

## H5a

Verdict: `inconclusive`. K-W on 8 inputs: p=9.26e-12; eta^2=0.0131; ratio spread=0.0171

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
