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
| `corona` | 0.3215 | 0.9722 | 0.9694 | 2 / 7 | 0.6 | `balanced_n64` |
| `cranium` | 0.2769 | 0.9744 | 0.9805 | 0 / 7 | 0.6 | `pilotCost_n8` |
| `cubus` | 0.1732 | 0.9793 | 0.9868 | 2 / 7 | 0.4286 | `balanced_n64` |
| `flame` | 0.2013 | 0.9705 | 0.9838 | 3 / 7 | 0.5556 | `balanced_n64` |
| `france` | 0.2839 | 0.9774 | 0.9794 | 1 / 7 | 0.8 | `pilotCost_n64` |
| `frisco` | 0.1889 | 0.9797 | 0.9824 | 2 / 7 | 0.6 | `balanced_n64` |
| `jelly` | 0.383 | 0.9642 | 0.9523 | 3 / 7 | 0.4 | `pairwise_n8` |
| `karte` | 0.3404 | 0.9709 | 0.971 | 2 / 7 | 0.5714 | `balanced_n64` |
| `mandelbrot` | 0.1195 | 0.9847 | 0.9882 | 4 / 7 | 0.5714 | `balanced_n64` |
| `strawberry` | 0.1948 | 0.9796 | 0.9784 | 3 / 7 | 0.4 | `balanced_n64` |
| `village` | 1.027 | 0.8932 | 0.8599 | 1 / 7 | 0.8 | `pilotCost_n64` |

## Readout

Highest heterogeneity: `village` with CV=1.027.

Least count-stable workload: `mandelbrot` with 4 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `village` with Spearman rho=0.8932.

## H5a

Verdict: `supports`. K-W on 11 inputs: p=3.82e-26; eta^2=0.0218; ratio spread=0.128

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
