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
| `corona` | 0.3215 | 0.9374 | 0.967 | 3 / 7 | 0.5 | `balanced_n64` |
| `cranium` | 0.2769 | 0.96 | 0.9798 | 0 / 7 | 0.5 | `pilotCost_n8` |
| `cubus` | 0.1732 | 0.9656 | 0.9861 | 3 / 7 | 0.6 | `balanced_n64` |
| `flame` | 0.2013 | 0.9575 | 0.9843 | 4 / 7 | 0.7143 | `balanced_n64` |
| `france` | 0.2839 | 0.9644 | 0.9782 | 0 / 7 | 0.75 | `pilotCost_n64` |
| `frisco` | 0.1889 | 0.9689 | 0.9843 | 4 / 7 | 0.5 | `random_n64` |
| `jelly` | 0.383 | 0.9225 | 0.9585 | 1 / 7 | 0.5 | `balanced_n64` |
| `karte` | 0.3404 | 0.9511 | 0.9729 | 2 / 7 | 0.5714 | `balanced_n64` |
| `mandelbrot` | 0.1195 | 0.9793 | 0.9883 | 6 / 7 | 0.4 | `balanced_n64` |
| `strawberry` | 0.1948 | 0.9689 | 0.9806 | 2 / 7 | 0.4 | `random_n64` |
| `village` | 1.027 | 0.8118 | 0.8729 | 1 / 7 | 0.75 | `pilotCost_n20` |

## Readout

Highest heterogeneity: `village` with CV=1.027.

Least count-stable workload: `mandelbrot` with 6 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `village` with Spearman rho=0.8118.

## H5a

Verdict: `supports`. K-W on 11 inputs: p=0.0255; eta^2=0.00839; ratio spread=0.115

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
