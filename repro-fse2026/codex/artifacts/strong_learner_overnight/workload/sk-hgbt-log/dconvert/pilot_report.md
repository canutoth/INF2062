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
| `jpeg-large` | 0.3828 | 0.9617 | 0.9525 | 7 / 7 | 0.5 | `balanced_n64` |
| `jpeg-medium` | 0.3011 | 0.9623 | 0.9617 | 6 / 7 | 0.5714 | `balanced_n64` |
| `jpeg-small` | 0.05973 | 0.9683 | 0.9931 | 5 / 7 | 0.2857 | `diversity_n8` |
| `png-large` | 0.2754 | 0.9638 | 0.9834 | 4 / 7 | 0.5714 | `random_n64` |
| `png-medium` | 0.1274 | 0.9683 | 0.9929 | 1 / 7 | 0.3333 | `random_n64` |
| `png-small` | 0.07376 | 0.9683 | 0.99 | 2 / 7 | 0.4444 | `diversity_n64` |
| `psd-large` | 0.3681 | 0.9217 | 0.9814 | 2 / 7 | 0.5 | `balanced_n64` |
| `psd-medium` | 0.1459 | 0.9682 | 0.9863 | 6 / 7 | 0.5 | `balanced_n64` |
| `psd-small` | 0.0746 | 0.9683 | 0.9905 | 1 / 7 | 0.5 | `diversity_n64` |
| `svg-large` | 0.02639 | 0.9683 | 0.9989 | 0 / 7 | 0.5 | `pairwise_n8` |
| `svg-medium` | 0.02738 | 0.9683 | 0.9973 | 0 / 7 | 0.5 | `pairwise_n8` |
| `svg-small` | 0.08757 | 0.9683 | 0.9941 | 3 / 7 | 0.2857 | `diversity_n64` |

## Readout

Highest heterogeneity: `jpeg-large` with CV=0.3828.

Least count-stable workload: `jpeg-large` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `psd-large` with Spearman rho=0.9217.

## H5a

Verdict: `supports`. K-W on 12 inputs: p=2.95e-60; eta^2=0.0668; ratio spread=0.0465

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
