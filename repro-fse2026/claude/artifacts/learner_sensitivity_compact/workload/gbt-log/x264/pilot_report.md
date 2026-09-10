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
| `Johnny_1280x720_60_short.y4m` | 0.9509 | 0.4509 | 0.8619 | 5 / 7 | 0.5 | `pilotCost_n16` |
| `Netflix_Crosswalk_4096x2160_60fps_10bit_420_short.y4m` | 0.9214 | 0.4856 | 0.9608 | 7 / 7 | 0.4 | `diversity_n16` |
| `blue_sky_1080p25_short.y4m` | 0.9217 | 0.4162 | 0.9359 | 7 / 7 | 0.2 | `pilotCost_n16` |
| `pedestrian_area_1080p25_short.y4m` | 0.9022 | 0.5723 | 0.9577 | 5 / 7 | 0.5 | `pilotCost_n16` |
| `riverbed_1080p25_short.y4m` | 0.8899 | 0.4336 | 0.9306 | 7 / 7 | 0.4 | `random_n16` |
| `sd_bridge_close_cif_short.y4m` | 0.8459 | 0.3468 | 0.8986 | 7 / 7 | 0.4 | `diversity_n8` |
| `sd_city_4cif_short.y4m` | 0.9384 | 0.4511 | 0.9885 | 7 / 7 | 0.4 | `pairwise_n16` |
| `sd_crew_cif_short.y4m` | 0.8825 | 0.5029 | 0.9295 | 5 / 7 | 0.5 | `pilotCost_n16` |
| `sintel_trailer_2k_720p24_short.y4m` | 0.8469 | 0.4162 | 0.8077 | 6 / 7 | 0.5 | `pilotCost_n16` |

## Readout

Highest heterogeneity: `Johnny_1280x720_60_short.y4m` with CV=0.9509.

Least count-stable workload: `Netflix_Crosswalk_4096x2160_60fps_10bit_420_short.y4m` with 7 top-1 flips out of 7 lambda settings.

Weakest rank-proxy workload: `sd_bridge_close_cif_short.y4m` with Spearman rho=0.3468.

## H5a

Verdict: `refutes`. K-W on 9 inputs: p=0.975; eta^2=0; ratio spread=0.181

## Files

- `records.csv`: one row per sampled run.
- `workload_summary.csv`: one row per workload context.
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, `rq4_pareto.csv`: workload-faceted analysis tables.
- `h5_workload_sensitivity.csv`: workload-sensitivity verdict when at least three workloads are available.
