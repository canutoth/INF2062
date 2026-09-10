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
| `ambivert.wav.tar` | 1.293 | 0.443 | 0.6993 | 7 / 7 | 0.5 | `diversity_n16` |
| `artificl.tar` | 0.3067 | 0.6556 | 1.049 | 6 / 7 | 0.4 | `pilotCost_n16` |
| `deepfield.tar` | 0.8822 | 0.5139 | 0.9339 | 7 / 7 | 0.4 | `balanced_n16` |
| `enwik8.tar` | 1.534 | 0.4075 | 0.6418 | 3 / 7 | 0.4 | `pilotCost_n16` |
| `fannie_mae_500k.tar` | 1.063 | 0.4075 | 0.6433 | 6 / 7 | 0.3333 | `pilotCost_n16` |
| `large.tar` | 0.7016 | 0.443 | 0.7969 | 6 / 7 | 0.3333 | `pilotCost_n16` |
| `misc.tar` | 0.6005 | 0.5847 | 0.8689 | 7 / 7 | 0.4 | `pairwise_n16` |
| `silesia.tar` | 1.119 | 0.443 | 0.6786 | 7 / 7 | 0.4 | `pilotCost_n16` |
| `uiq-32.bin` | 1.14 | 0.4075 | 0.7486 | 3 / 7 | 0.5 | `pilotCost_n16` |
| `uiq2-16.bin` | 1.112 | 0.4075 | 0.7616 | 3 / 7 | 0.5 | `pilotCost_n16` |
| `uiq2-4.bin` | 0.8886 | 0.4784 | 0.8909 | 6 / 7 | 0.3333 | `balanced_n16` |
| `uiq2-8.bin` | 1.008 | 0.4784 | 0.8459 | 7 / 7 | 0.3333 | `pilotCost_n16` |
| `vmlinux-5.10.tar` | 0.5619 | 0.5139 | 0.8946 | 5 / 7 | 0.3333 | `pilotCost_n16` |

## Readout

Highest heterogeneity: `enwik8.tar` with CV=1.534.

Least count-stable workload: `ambivert.wav.tar` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `enwik8.tar` with Spearman rho=0.4075.

## H5a

Verdict: `refutes`. K-W on 13 inputs: p=0.994; eta^2=0; ratio spread=0.407

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
