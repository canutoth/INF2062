# Generated sampling pilot on workload-impact `dconvert`

## Scope

Source archive: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip`

Source member(s): `icse22_supplementary-main/dashboard/resources/dconvert/sample.csv + icse22_supplementary-main/dashboard/resources/dconvert/measurements.csv`

Target column: `time`. Cost column: `time`.

Workloads analyzed: `jpeg-large, jpeg-medium, jpeg-small, png-large, png-medium, png-small, psd-large, psd-medium, psd-small, svg-large, svg-medium, svg-small`

Encoded feature columns: `35`.

This pilot reuses the Twins-style generated-sampling protocol on the measured configuration universe provided by the ICSE 2023 workload dataset. Each workload is treated as a separate context.

## Workload summary

| Workload | Cost CV | Spearman rho | Median %cost/%n | Top-1 flips | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---:|---:|---|
| `jpeg-large` | 0.3828 | 0.9361 | 0.9572 | 7 / 7 | 0.5714 | `balanced_n64` |
| `jpeg-medium` | 0.3011 | 0.9399 | 0.9622 | 5 / 7 | 0.5 | `balanced_n64` |
| `jpeg-small` | 0.05973 | 0.9684 | 0.9942 | 5 / 7 | 0.2857 | `diversity_n8` |
| `png-large` | 0.2754 | 0.9474 | 0.9758 | 4 / 7 | 0.5 | `random_n64` |
| `png-medium` | 0.1274 | 0.9683 | 0.9921 | 1 / 7 | 0.4 | `random_n64` |
| `png-small` | 0.07376 | 0.9684 | 0.9945 | 2 / 7 | 0.5 | `balanced_n64` |
| `psd-large` | 0.3681 | 0.9093 | 0.9673 | 4 / 7 | 0.5 | `balanced_n64` |
| `psd-medium` | 0.1459 | 0.9667 | 0.9849 | 6 / 7 | 0.4286 | `balanced_n64` |
| `psd-small` | 0.0746 | 0.9684 | 0.9905 | 5 / 7 | 0.4286 | `diversity_n64` |
| `svg-large` | 0.02639 | 0.9684 | 0.9982 | 1 / 7 | 0.3333 | `pairwise_n8` |
| `svg-medium` | 0.02738 | 0.9684 | 0.9961 | 0 / 7 | 0.5714 | `pairwise_n8` |
| `svg-small` | 0.08757 | 0.9683 | 0.992 | 2 / 7 | 0.375 | `diversity_n64` |

## Readout

Highest heterogeneity: `jpeg-large` with CV=0.3828.

Least count-stable workload: `jpeg-large` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `psd-large` with Spearman rho=0.9093.

## H5a

Verdict: `supports`. K-W on 12 inputs: p=3.48e-12; eta^2=0.0745; ratio spread=0.041

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
