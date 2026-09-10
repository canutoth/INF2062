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
| `jpeg-large` | 0.3828 | 0.711 | 0.9519 | 4 / 7 | 0.4 | `pairwise_n16` |
| `jpeg-medium` | 0.3011 | 0.711 | 0.9583 | 7 / 7 | 0.2857 | `pairwise_n16` |
| `jpeg-small` | 0.05973 | 0.8671 | 0.9931 | 1 / 7 | 0.5 | `pairwise_n8` |
| `png-large` | 0.2754 | 0.7284 | 0.9729 | 3 / 7 | 0.5 | `pairwise_n16` |
| `png-medium` | 0.1274 | 0.8674 | 0.9887 | 7 / 7 | 0.4 | `pairwise_n16` |
| `png-small` | 0.07376 | 0.8681 | 0.9965 | 2 / 7 | 0.4 | `pairwise_n16` |
| `psd-large` | 0.3681 | 0.711 | 0.9359 | 2 / 7 | 0.5 | `diversity_n16` |
| `psd-medium` | 0.1459 | 0.8498 | 0.9761 | 2 / 7 | 0.4 | `pairwise_n16` |
| `psd-small` | 0.0746 | 0.8674 | 0.9838 | 3 / 7 | 0.4 | `diversity_n16` |
| `svg-large` | 0.02639 | 0.8678 | 0.9974 | 1 / 7 | 0.3333 | `diversity_n8` |
| `svg-medium` | 0.02738 | 0.8671 | 0.9939 | 0 / 7 | 0.6667 | `diversity_n8` |
| `svg-small` | 0.08757 | 0.8671 | 1 | 2 / 7 | 0.3333 | `diversity_n16` |

## Readout

Highest heterogeneity: `jpeg-large` with CV=0.3828.

Least count-stable workload: `jpeg-medium` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `jpeg-large` with Spearman rho=0.711.

## H5a

Verdict: `inconclusive`. K-W on 12 inputs: p=0.17; eta^2=0.0188; ratio spread=0.0646

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
