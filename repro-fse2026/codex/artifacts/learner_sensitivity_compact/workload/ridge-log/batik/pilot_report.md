# Generated sampling pilot on workload-impact `batik`

## Scope

Source archive: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip`

Source member(s): `icse22_supplementary-main/dashboard/resources/batik/sample.csv + icse22_supplementary-main/dashboard/resources/batik/measurements.csv`

Target column: `time`. Cost column: `time`.

Workloads analyzed: `corona, cranium, cubus, flame, france, frisco, jelly, karte, mandelbrot, strawberry, village`

Encoded feature columns: `18`.

This pilot reuses the Twins-style generated-sampling protocol on the measured configuration universe provided by the ICSE 2023 workload dataset. Each workload is treated as a separate context.

## Workload summary

| Workload | Cost CV | Spearman rho | Median %cost/%n | Top-1 flips | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---:|---:|---|
| `corona` | 0.3215 | 0.711 | 0.9797 | 4 / 7 | 0.3333 | `pairwise_n16` |
| `cranium` | 0.2769 | 0.8327 | 1.006 | 5 / 7 | 0.3333 | `diversity_n16` |
| `cubus` | 0.1732 | 0.8498 | 0.9918 | 3 / 7 | 0.3333 | `diversity_n16` |
| `flame` | 0.2013 | 0.8498 | 0.9841 | 3 / 7 | 0.3333 | `diversity_n16` |
| `france` | 0.2839 | 0.8324 | 1.002 | 5 / 7 | 0.4 | `pairwise_n16` |
| `frisco` | 0.1889 | 0.8498 | 0.9974 | 4 / 7 | 0.3333 | `diversity_n16` |
| `jelly` | 0.383 | 0.711 | 0.9674 | 3 / 7 | 0.4 | `diversity_n16` |
| `karte` | 0.3404 | 0.8498 | 0.9926 | 6 / 7 | 0.4 | `pairwise_n16` |
| `mandelbrot` | 0.1195 | 0.8671 | 0.9925 | 2 / 7 | 0.3333 | `pairwise_n16` |
| `strawberry` | 0.1948 | 0.8324 | 0.9935 | 4 / 7 | 0.3333 | `pairwise_n16` |
| `village` | 1.027 | 0.5896 | 0.7883 | 3 / 7 | 0.5 | `pilotCost_n8` |

## Readout

Highest heterogeneity: `village` with CV=1.027.

Least count-stable workload: `karte` with 6 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `village` with Spearman rho=0.5896.

## H5a

Verdict: `refutes`. K-W on 11 inputs: p=0.996; eta^2=0; ratio spread=0.218

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
