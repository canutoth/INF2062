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
| `ambivert.wav.tar` | 1.293 | 0.7296 | 0.8443 | 7 / 7 | 0.4 | `pilotCost_n64` |
| `artificl.tar` | 0.3067 | 0.9734 | 0.9847 | 2 / 7 | 0.5 | `diversity_n16` |
| `deepfield.tar` | 0.8822 | 0.8184 | 0.9091 | 7 / 7 | 0.4545 | `diversity_n64` |
| `enwik8.tar` | 1.534 | 0.6622 | 0.8191 | 3 / 7 | 0.5 | `pilotCost_n64` |
| `fannie_mae_500k.tar` | 1.063 | 0.7638 | 0.8634 | 3 / 7 | 0.2857 | `pilotCost_n64` |
| `large.tar` | 0.7016 | 0.8881 | 0.9156 | 6 / 7 | 0.4545 | `pairwise_n32` |
| `misc.tar` | 0.6005 | 0.9415 | 0.9394 | 4 / 7 | 0.4444 | `pairwise_n40` |
| `silesia.tar` | 1.119 | 0.773 | 0.8582 | 7 / 7 | 0.4 | `pairwise_n32` |
| `uiq-32.bin` | 1.14 | 0.7309 | 0.8734 | 3 / 7 | 0.1429 | `pilotCost_n64` |
| `uiq2-16.bin` | 1.112 | 0.7529 | 0.8763 | 3 / 7 | 0.4545 | `pilotCost_n64` |
| `uiq2-4.bin` | 0.8886 | 0.8388 | 0.9156 | 3 / 7 | 0.25 | `pilotCost_n64` |
| `uiq2-8.bin` | 1.008 | 0.7934 | 0.8916 | 3 / 7 | 0.2727 | `pilotCost_n64` |
| `vmlinux-5.10.tar` | 0.5619 | 0.9191 | 0.943 | 4 / 7 | 0.3333 | `pairwise_n32` |

## Readout

Highest heterogeneity: `enwik8.tar` with CV=1.534.

Least count-stable workload: `ambivert.wav.tar` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `enwik8.tar` with Spearman rho=0.6622.

## H5a

Verdict: `supports`. K-W on 13 inputs: p=1.13e-41; eta^2=0.0293; ratio spread=0.166

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
