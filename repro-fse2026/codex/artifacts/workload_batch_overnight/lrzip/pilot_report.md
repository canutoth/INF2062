# Generated sampling pilot on workload-impact `lrzip`

## Scope

Source archive: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip`

Source member(s): `icse22_supplementary-main/dashboard/resources/lrzip/sample.csv + icse22_supplementary-main/dashboard/resources/lrzip/measurements.csv`

Target column: `time`. Cost column: `time`.

Workloads analyzed: `ambivert.wav.tar, artificl.tar, deepfield.tar, enwik8.tar, fannie_mae_500k.tar, large.tar, misc.tar, silesia.tar, uiq-32.bin, uiq2-16.bin, uiq2-4.bin, uiq2-8.bin, vmlinux-5.10.tar`

Encoded feature columns: `11`.

This pilot reuses the Twins-style generated-sampling protocol on the measured configuration universe provided by the ICSE 2023 workload dataset. Each workload is treated as a separate context.

## Workload summary

| Workload | Cost CV | Spearman rho | Median %cost/%n | Top-1 flips | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---:|---:|---|
| `ambivert.wav.tar` | 1.544 | 0.8958 | 1.059 | 0 / 7 | 1 | `cheapOracle_n8` |
| `artificl.tar` | 0.9505 | 0.9455 | 1.017 | 0 / 7 | 1 | `cheapOracle_n8` |
| `deepfield.tar` | 1.524 | 0.8973 | 1.044 | 0 / 7 | 1 | `cheapOracle_n8` |
| `enwik8.tar` | 1.217 | 0.9244 | 1.014 | 0 / 7 | 1 | `cheapOracle_n8` |
| `fannie_mae_500k.tar` | 0.188 | 0.9884 | 1.005 | 2 / 7 | 0.75 | `diversity_n8` |
| `large.tar` | 0.75 | 0.9517 | 1.01 | 0 / 7 | 1 | `cheapOracle_n8` |
| `misc.tar` | 0.8109 | 0.9475 | 1.022 | 0 / 7 | 1 | `cheapOracle_n8` |
| `silesia.tar` | 1.306 | 0.9172 | 1.014 | 0 / 7 | 1 | `cheapOracle_n8` |
| `uiq-32.bin` | 1.559 | 0.8968 | 0.9885 | 0 / 7 | 1 | `cheapOracle_n8` |
| `uiq2-16.bin` | 1.517 | 0.8974 | 1.027 | 1 / 7 | 1 | `cheapOracle_n10` |
| `uiq2-4.bin` | 1.239 | 0.9175 | 1.022 | 0 / 7 | 1 | `cheapOracle_n8` |
| `uiq2-8.bin` | 1.382 | 0.9096 | 1.026 | 0 / 7 | 1 | `cheapOracle_n8` |
| `vmlinux-5.10.tar` | 0.9248 | 0.9423 | 1.03 | 0 / 7 | 1 | `cheapOracle_n8` |

## Readout

Highest heterogeneity: `uiq-32.bin` with CV=1.559.

Least count-stable workload: `fannie_mae_500k.tar` with 2 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `ambivert.wav.tar` with Spearman rho=0.8958.

## H5a

Verdict: `inconclusive`. K-W on 13 inputs: p=0.000322; eta^2=0.00281; ratio spread=0.0705

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
