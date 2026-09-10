# Curated FSE Posterior Guarantee/Cost Frontiers

This folder keeps five representative frontier panels for paper assembly instead of surfacing every generated per-context plot.
Each panel uses measured acquisition cost on the x-axis and integrated posterior confidence on the y-axis; outlined points are on the measured-cost/confidence Pareto frontier.

## Selection Table

| # | Corpus | Context | Level | Best cost pair | SRS best | SRS frontier | Top changed | Best-SRS omega |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Original FSE artifact | 7z | t2 | twise_t2 | 0 | 1 | 1 | 0.00155153 |
| 2 | x264 | x264_time_1 | t2 | SRSSampling_t2 | 1 | 1 | 0 | 0 |
| 3 | WORKLOAD | kanzi__workload_vmlinux__cost_time__target_time | n8 | pilotCost_n8 | 0 | 1 | 1 | 0.341793 |
| 4 | Linux/TuxKConfig | linux500_vmlinux | n00200 | diversity_n00200 | 0 | 1 | 0 | 0.00139077 |
| 5 | LCBench | lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy | n8 | pilotCost_n8 | 0 | 0 | 1 | 0.18141 |

## Figures

### 1. Original FSE artifact - `7z:t2`

![01_fse_7z_srs_pareto_not_best](01_fse_7z_srs_pareto_not_best.png)

The restored FSE 7z system keeps SRS on the measured-cost/confidence frontier, but cost normalization moves the top recommendation to `twise_t2`.

- Role: Direct anchor: cost changes the recommendation while SRS remains Pareto-efficient.
- Best by sample-size baseline: `SRSSampling_t2`
- Best by measured-cost baseline: `twise_t2`
- SRS best cost-normalized: `0`
- SRS on measured-cost frontier: `1`
- Best minus SRS omega-cost gap: `0.00155153`

### 2. x264 - `x264_time_1:t2`

![02_x264_time_1_srs_best](02_x264_time_1_srs_best.png)

x264 remains the cleanest favorable extension for SRS: in this target/context, `SRSSampling_t2` is both the cost-normalized winner and Pareto-efficient.

- Role: Positive external replication: SRS is the empirical-cost-normalized winner.
- Best by sample-size baseline: `SRSSampling_t2`
- Best by measured-cost baseline: `SRSSampling_t2`
- SRS best cost-normalized: `1`
- SRS on measured-cost frontier: `1`
- Best minus SRS omega-cost gap: `0`

### 3. WORKLOAD - `kanzi__workload_vmlinux__cost_time__target_time:n8`

![03_workload_kanzi_vmlinux_srs_pareto_not_best](03_workload_kanzi_vmlinux_srs_pareto_not_best.png)

For kanzi/vmlinux, measured acquisition cost changes the top recommendation to `pilotCost_n8`; SRS remains on the frontier but trails the best cost-normalized option.

- Role: Workload stress case: SRS is defensible but no longer the best cost-aware choice.
- Best by sample-size baseline: `balanced_n8`
- Best by measured-cost baseline: `pilotCost_n8`
- SRS best cost-normalized: `0`
- SRS on measured-cost frontier: `1`
- Best minus SRS omega-cost gap: `0.341793`

### 4. Linux/TuxKConfig - `linux500_vmlinux:n00200`

![04_linux500_pool_srs_pareto_not_best](04_linux500_pool_srs_pareto_not_best.png)

The Linux measured-pool example illustrates the external-validity framing: SRS is Pareto-efficient, but `diversity_n00200` is the best cost-normalized recommendation.

- Role: Measured-pool external validity: SRS is Pareto-efficient but not dominant.
- Best by sample-size baseline: `diversity_n00200`
- Best by measured-cost baseline: `diversity_n00200`
- SRS best cost-normalized: `0`
- SRS on measured-cost frontier: `1`
- Best minus SRS omega-cost gap: `0.00139077`

### 5. LCBench - `lcbench__workload_mfeat_factors__cost_time_total__target_final_val_accuracy:n8`

![05_lcbench_mfeat_factors_srs_not_frontier](05_lcbench_mfeat_factors_srs_not_frontier.png)

LCBench mfeat-factors is a clear negative example: cost normalization changes the top recommendation to `pilotCost_n8`, and SRS is not on the measured-cost frontier.

- Role: Stress case: SRS is not on the measured-cost/confidence frontier.
- Best by sample-size baseline: `diversity_n8`
- Best by measured-cost baseline: `pilotCost_n8`
- SRS best cost-normalized: `0`
- SRS on measured-cost frontier: `0`
- Best minus SRS omega-cost gap: `0.18141`

## Source Tables

- `curated_frontier_examples.csv`: machine-readable manifest for the selected examples.
- Source `posterior_pareto.csv` and summary paths are recorded per row in the manifest.
