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
| `ambivert.wav.tar` | 1.544 | 0.4812 | 1.041 | 0 / 7 | 1 | `cheapOracle_n8` |
| `artificl.tar` | 0.9505 | 0.5849 | 1.008 | 0 / 7 | 1 | `cheapOracle_n8` |
| `deepfield.tar` | 1.524 | 0.4764 | 1.024 | 0 / 7 | 1 | `cheapOracle_n8` |
| `enwik8.tar` | 1.217 | 0.533 | 1.067 | 0 / 7 | 1 | `cheapOracle_n8` |
| `fannie_mae_500k.tar` | 0.188 | 0.8821 | 1.014 | 3 / 7 | 0.5 | `diversity_n8` |
| `large.tar` | 0.75 | 0.5613 | 1.061 | 0 / 7 | 1 | `cheapOracle_n8` |
| `misc.tar` | 0.8109 | 0.604 | 1.049 | 0 / 7 | 1 | `cheapOracle_n8` |
| `silesia.tar` | 1.306 | 0.4434 | 1.128 | 2 / 7 | 1 | `pilotCost_n10` |
| `uiq-32.bin` | 1.559 | 0.4434 | 1.125 | 0 / 7 | 1 | `cheapOracle_n8` |
| `uiq2-16.bin` | 1.517 | 0.5 | 1.062 | 2 / 7 | 0.6667 | `pilotCost_n10` |
| `uiq2-4.bin` | 1.239 | 0.5236 | 1.008 | 6 / 7 | 0.5 | `pilotCost_n8` |
| `uiq2-8.bin` | 1.382 | 0.5425 | 1.023 | 0 / 7 | 1 | `cheapOracle_n8` |
| `vmlinux-5.10.tar` | 0.9248 | 0.6038 | 1.052 | 0 / 7 | 1 | `cheapOracle_n8` |

## Readout

Highest heterogeneity: `uiq-32.bin` with CV=1.559.

Least count-stable workload: `uiq2-4.bin` with 6 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `silesia.tar` with Spearman rho=0.4434.

## H5a

Verdict: `refutes`. K-W on 13 inputs: p=1; eta^2=0; ratio spread=0.12

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
