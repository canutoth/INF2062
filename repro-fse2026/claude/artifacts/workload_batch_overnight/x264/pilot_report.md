# Generated sampling pilot on workload-impact `x264`

## Scope

Source archive: `/Users/mathieuacher/SANDBOX/cost-sampling-matters/workload-impact-ICSE2023/artifact_excluding_raw_coverage.zip`

Source member(s): `icse22_supplementary-main/dashboard/resources/x264/sample.csv + icse22_supplementary-main/dashboard/resources/x264/measurements.csv`

Target column: `time`. Cost column: `time`.

Workloads analyzed: `Johnny_1280x720_60_short.y4m, Netflix_Crosswalk_4096x2160_60fps_10bit_420_short.y4m, blue_sky_1080p25_short.y4m, pedestrian_area_1080p25_short.y4m, riverbed_1080p25_short.y4m, sd_bridge_close_cif_short.y4m, sd_city_4cif_short.y4m, sd_crew_cif_short.y4m, sintel_trailer_2k_720p24_short.y4m`

Encoded feature columns: `25`.

This pilot reuses the Twins-style generated-sampling protocol on the measured configuration universe provided by the ICSE 2023 workload dataset. Each workload is treated as a separate context.

## Workload summary

| Workload | Cost CV | Spearman rho | Median %cost/%n | Top-1 flips | Pareto Jaccard | Best simple pair |
|---|---:|---:|---:|---:|---:|---|
| `Johnny_1280x720_60_short.y4m` | 0.9509 | 0.7315 | 0.9308 | 6 / 7 | 0.3636 | `diversity_n63` |
| `Netflix_Crosswalk_4096x2160_60fps_10bit_420_short.y4m` | 0.9214 | 0.7358 | 0.9373 | 6 / 7 | 0.1765 | `pairwise_n64` |
| `blue_sky_1080p25_short.y4m` | 0.9217 | 0.7585 | 0.9329 | 4 / 7 | 0.3333 | `diversity_n64` |
| `pedestrian_area_1080p25_short.y4m` | 0.9022 | 0.742 | 0.9376 | 6 / 7 | 0.5 | `pairwise_n64` |
| `riverbed_1080p25_short.y4m` | 0.8899 | 0.7725 | 0.9344 | 5 / 7 | 0.4167 | `diversity_n63` |
| `sd_bridge_close_cif_short.y4m` | 0.8459 | 0.7659 | 0.9395 | 4 / 7 | 0.3571 | `diversity_n64` |
| `sd_city_4cif_short.y4m` | 0.9384 | 0.7515 | 0.9457 | 6 / 7 | 0.2941 | `diversity_n63` |
| `sd_crew_cif_short.y4m` | 0.8825 | 0.7613 | 0.9354 | 4 / 7 | 0.4444 | `pairwise_n63` |
| `sintel_trailer_2k_720p24_short.y4m` | 0.8469 | 0.7395 | 0.9529 | 4 / 7 | 0.5 | `diversity_n63` |

## Readout

Highest heterogeneity: `Johnny_1280x720_60_short.y4m` with CV=0.9509.

Least count-stable workload: `Johnny_1280x720_60_short.y4m` with 6 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `Johnny_1280x720_60_short.y4m` with Spearman rho=0.7315.

## H5a

Verdict: `refutes`. K-W on 9 inputs: p=0.962; eta^2=0; ratio spread=0.0221

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
