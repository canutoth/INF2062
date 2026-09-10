# Generated sampling pilot on workload-impact `xz`

## Scope

Source archive: `workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip`

Source member(s): `icse22_supplementary-main/dashboard/resources/xz/sample.csv + icse22_supplementary-main/dashboard/resources/xz/measurements.csv`

Target column: `time`. Cost column: `time`.

Workloads analyzed: `ambivert.wav.tar, artificl.tar, deepfield.tar, enwik8.tar, fannie_mae_500k.tar, large.tar, misc.tar, silesia.tar, uiq-32.bin, uiq2-16.bin, uiq2-4.bin, uiq2-8.bin, vmlinux-5.10.tar`

Encoded feature columns: `33`.

This pilot reuses the Twins-style generated-sampling protocol on the measured configuration universe provided by the ICSE 2023 workload dataset. Each workload is treated as a separate context.

## Workload summary

| Workload | Cost CV | Spearman rho | Median %cost/%n | Top-1 flips | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---:|---:|---|
| `ambivert.wav.tar` | 1.293 | 0.7296 | 0.8495 | 2 / 7 | 0.75 | `diversity_n64` |
| `artificl.tar` | 0.3067 | 0.9726 | 0.9847 | 1 / 7 | 0.6 | `pairwise_n64` |
| `deepfield.tar` | 0.8822 | 0.8178 | 0.9115 | 2 / 7 | 0.7143 | `diversity_n64` |
| `enwik8.tar` | 1.534 | 0.6615 | 0.8191 | 2 / 7 | 0.5 | `diversity_n64` |
| `fannie_mae_500k.tar` | 1.063 | 0.7636 | 0.8634 | 2 / 7 | 0.5 | `diversity_n64` |
| `large.tar` | 0.7016 | 0.8879 | 0.9156 | 2 / 7 | 0.5 | `diversity_n64` |
| `misc.tar` | 0.6005 | 0.9419 | 0.9398 | 2 / 7 | 0.75 | `pilotCost_n64` |
| `silesia.tar` | 1.119 | 0.7732 | 0.8592 | 2 / 7 | 0.6667 | `diversity_n64` |
| `uiq-32.bin` | 1.14 | 0.7298 | 0.8763 | 2 / 7 | 0.5714 | `diversity_n64` |
| `uiq2-16.bin` | 1.112 | 0.752 | 0.877 | 2 / 7 | 0.5 | `diversity_n64` |
| `uiq2-4.bin` | 0.8886 | 0.8387 | 0.915 | 2 / 7 | 0.375 | `diversity_n64` |
| `uiq2-8.bin` | 1.008 | 0.7921 | 0.8933 | 2 / 7 | 0.5556 | `diversity_n64` |
| `vmlinux-5.10.tar` | 0.5619 | 0.9191 | 0.9434 | 7 / 7 | 0.625 | `diversity_n64` |

## Readout

Highest heterogeneity: `enwik8.tar` with CV=1.534.

Least count-stable workload: `vmlinux-5.10.tar` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `enwik8.tar` with Spearman rho=0.6615.

## H5a

Verdict: `supports`. K-W on 13 inputs: p=2.59e-41; eta^2=0.0291; ratio spread=0.166

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
