# Generated sampling pilot on workload-impact `jump3r`

## Scope

Source archive: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip`

Source member(s): `icse22_supplementary-main/dashboard/resources/jump3r/sample.csv + icse22_supplementary-main/dashboard/resources/jump3r/measurements.csv`

Target column: `time`. Cost column: `time`.

Workloads analyzed: `beethoven.wav, dual-channel.wav, helix.wav, single-channel.wav, speech.wav, sweep.wav`

Encoded feature columns: `29`.

This pilot reuses the Twins-style generated-sampling protocol on the measured configuration universe provided by the ICSE 2023 workload dataset. Each workload is treated as a separate context.

## Workload summary

| Workload | Cost CV | Spearman rho | Median %cost/%n | Top-1 flips | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---:|---:|---|
| `beethoven.wav` | 0.556 | 0.9084 | 0.9659 | 3 / 7 | 0.4444 | `pairwise_n32` |
| `dual-channel.wav` | 0.5472 | 0.9141 | 0.9675 | 3 / 7 | 0.5 | `pairwise_n64` |
| `helix.wav` | 0.5851 | 0.902 | 0.9638 | 3 / 7 | 0.4444 | `pairwise_n32` |
| `single-channel.wav` | 0.4632 | 0.9379 | 0.9665 | 3 / 7 | 0.625 | `pairwise_n64` |
| `speech.wav` | 0.5453 | 0.8995 | 0.9685 | 4 / 7 | 0.5 | `diversity_n64` |
| `sweep.wav` | 0.3606 | 0.9552 | 0.9768 | 3 / 7 | 0.625 | `pairwise_n32` |

## Readout

Highest heterogeneity: `helix.wav` with CV=0.5851.

Least count-stable workload: `speech.wav` with 4 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `speech.wav` with Spearman rho=0.8995.

## H5a

Verdict: `refutes`. K-W on 6 inputs: p=0.579; eta^2=0; ratio spread=0.013

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
