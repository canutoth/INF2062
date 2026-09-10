# Generated sampling pilot on workload-impact `xz`

## Scope

Source archive: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip`

Source member(s): `icse22_supplementary-main/dashboard/resources/xz/sample.csv + icse22_supplementary-main/dashboard/resources/xz/measurements.csv`

Target column: `time`. Cost column: `time`.

Workloads analyzed: `artificl.tar, deepfield.tar, uiq-32.bin`

Encoded feature columns: `33`.

This pilot reuses the Twins-style generated-sampling protocol on the measured configuration universe provided by the ICSE 2023 workload dataset. Each workload is treated as a separate context.

## Workload summary

| Workload | Cost CV | Spearman rho | Median %cost/%n | Top-1 flips | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---:|---:|---|
| `artificl.tar` | 0.3067 | 0.9542 | 0.9847 | 4 / 7 | 0.5 | `diversity_n16` |
| `deepfield.tar` | 0.8822 | 0.7853 | 0.9145 | 7 / 7 | 0.3077 | `diversity_n64` |
| `uiq-32.bin` | 1.14 | 0.7027 | 0.8742 | 2 / 7 | 0.3636 | `pilotCost_n64` |

## Readout

Highest heterogeneity: `uiq-32.bin` with CV=1.14.

Least count-stable workload: `deepfield.tar` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `uiq-32.bin` with Spearman rho=0.7027.

## H5a

Verdict: `supports`. K-W on 3 inputs: p=8.19e-08; eta^2=0.0503; ratio spread=0.111

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
