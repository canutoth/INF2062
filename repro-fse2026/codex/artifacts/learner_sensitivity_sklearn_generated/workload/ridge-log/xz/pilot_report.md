# Generated sampling pilot on workload-impact `xz`

## Scope

Source archive: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip`

Source member(s): `icse22_supplementary-main/dashboard/resources/xz/sample.csv + icse22_supplementary-main/dashboard/resources/xz/measurements.csv`

Target column: `time`. Cost column: `time`.

Workloads analyzed: `ambivert.wav.tar, artificl.tar, deepfield.tar, enwik8.tar, fannie_mae_500k.tar, large.tar, misc.tar, silesia.tar, uiq-32.bin, uiq2-16.bin, uiq2-4.bin, uiq2-8.bin, vmlinux-5.10.tar`

Encoded feature columns: `33`.

This pilot reuses the Twins-style generated-sampling protocol on the measured configuration universe provided by the ICSE 2023 workload dataset. Each workload is treated as a separate context.

## Workload summary

| Workload | Cost CV | Spearman rho | Median %cost/%n | Top-1 flips | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---:|---:|---|
| `ambivert.wav.tar` | 1.293 | 0.6651 | 0.8525 | 7 / 7 | 0.4 | `pilotCost_n64` |
| `artificl.tar` | 0.3067 | 0.9296 | 0.9722 | 2 / 7 | 0.4 | `diversity_n16` |
| `deepfield.tar` | 0.8822 | 0.7466 | 0.9154 | 7 / 7 | 0.3333 | `diversity_n64` |
| `enwik8.tar` | 1.534 | 0.6058 | 0.7791 | 4 / 7 | 0.5714 | `pilotCost_n64` |
| `fannie_mae_500k.tar` | 1.063 | 0.7032 | 0.837 | 3 / 7 | 0.2857 | `pilotCost_n40` |
| `large.tar` | 0.7016 | 0.8228 | 0.9018 | 6 / 7 | 0.4167 | `pilotCost_n64` |
| `misc.tar` | 0.6005 | 0.8777 | 0.9421 | 6 / 7 | 0.4 | `pairwise_n40` |
| `silesia.tar` | 1.119 | 0.706 | 0.8445 | 7 / 7 | 0.4 | `pilotCost_n64` |
| `uiq-32.bin` | 1.14 | 0.6753 | 0.8539 | 2 / 7 | 0.7143 | `pilotCost_n64` |
| `uiq2-16.bin` | 1.112 | 0.6904 | 0.8763 | 3 / 7 | 0.6667 | `pilotCost_n64` |
| `uiq2-4.bin` | 0.8886 | 0.761 | 0.9258 | 7 / 7 | 0.2727 | `balanced_n64` |
| `uiq2-8.bin` | 1.008 | 0.727 | 0.8848 | 7 / 7 | 0.4444 | `pilotCost_n40` |
| `vmlinux-5.10.tar` | 0.5619 | 0.8565 | 0.9403 | 3 / 7 | 0.2727 | `pairwise_n32` |

## Readout

Highest heterogeneity: `enwik8.tar` with CV=1.534.

Least count-stable workload: `ambivert.wav.tar` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `enwik8.tar` with Spearman rho=0.6058.

## H5a

Verdict: `supports`. K-W on 13 inputs: p=4.54e-06; eta^2=0.0239; ratio spread=0.193

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
