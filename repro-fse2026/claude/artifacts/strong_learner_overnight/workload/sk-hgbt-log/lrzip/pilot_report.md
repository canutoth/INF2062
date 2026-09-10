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
| `ambivert.wav.tar` | 1.544 | 0.8971 | 1.055 | 7 / 7 | 0.3333 | `pilotCost_n8` |
| `artificl.tar` | 0.9505 | 0.9455 | 1.017 | 0 / 7 | 1 | `cheapOracle_n8` |
| `deepfield.tar` | 1.524 | 0.9003 | 1.043 | 0 / 7 | 1 | `cheapOracle_n8` |
| `enwik8.tar` | 1.217 | 0.9249 | 1.013 | 0 / 7 | 1 | `cheapOracle_n8` |
| `fannie_mae_500k.tar` | 0.188 | 0.9884 | 1.004 | 2 / 7 | 0.5 | `random_n8` |
| `large.tar` | 0.75 | 0.9518 | 1.012 | 0 / 7 | 1 | `cheapOracle_n8` |
| `misc.tar` | 0.8109 | 0.9474 | 1.026 | 0 / 7 | 1 | `cheapOracle_n8` |
| `silesia.tar` | 1.306 | 0.9188 | 1.006 | 0 / 7 | 1 | `cheapOracle_n8` |
| `uiq-32.bin` | 1.559 | 0.8972 | 0.9824 | 0 / 7 | 1 | `cheapOracle_n10` |
| `uiq2-16.bin` | 1.517 | 0.8972 | 1.022 | 0 / 7 | 1 | `cheapOracle_n10` |
| `uiq2-4.bin` | 1.239 | 0.9198 | 1.02 | 0 / 7 | 1 | `cheapOracle_n8` |
| `uiq2-8.bin` | 1.382 | 0.9089 | 1.027 | 0 / 7 | 1 | `cheapOracle_n8` |
| `vmlinux-5.10.tar` | 0.9248 | 0.9419 | 1.03 | 0 / 7 | 1 | `cheapOracle_n8` |

## Readout

Highest heterogeneity: `uiq-32.bin` with CV=1.559.

Least count-stable workload: `ambivert.wav.tar` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `ambivert.wav.tar` with Spearman rho=0.8971.

## H5a

Verdict: `inconclusive`. K-W on 13 inputs: p=0.000729; eta^2=0.00255; ratio spread=0.0722

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
