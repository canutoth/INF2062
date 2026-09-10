# Artifact Guide for Paper Writing

This directory contains generated analysis outputs. The important distinction is:

- **Paper-ready primary outputs:** `x264_matrix/` and `newruns_systems/`.
- **Generated-protocol outputs:** `twins_generated_representative_100s/`, `twins_generated_quick/`, `twins_HSQLDB_generated/`, `twins_brotli_1_0_7_generated/`, and `twins_PostgreSQL_9_6_3_generated/`.
- **Focused supporting outputs:** `x264_time_all/`, `x264_size_all/`, and per-system folders under `newruns_systems/`.
- **Exploratory or smoke outputs:** `poc_*`, `*_smoke/`, and the standalone `BerkeleyDBC_performance/`.

The paper should mainly cite the reports and figures in the paper-ready folders, then use CSV files when exact table values are needed.

## Folder Inventory

| Folder | Status | Main use |
|---|---|---|
| `artifacts/` | index | This guide plus generated analysis folders. |
| `paper_figures/` | curated copies | Stable paper-facing copies of selected figures with reuse notes and captions. |
| `x264_matrix/` | paper-ready | Main x264 2x2 cost-target matrix. |
| `newruns_systems/` | paper-ready | Cross-system NewRuns replication. |
| `twins_HSQLDB_generated/` | generated-protocol output | Generated-sampling run on TwinsOrFalseFriends HSQLDB. |
| `twins_brotli_1_0_7_generated/` | generated-protocol output | Revision-scoped generated-sampling run on TwinsOrFalseFriends brotli. |
| `twins_PostgreSQL_9_6_3_generated/` | generated-protocol output | Revision-scoped generated-sampling run on TwinsOrFalseFriends PostgreSQL. |
| `twins_generated_representative_100s/` | generated-protocol stronger evidence | Seven representative Twins systems, 100 seeds, max budget 256, no row caps. |
| `twins_generated_quick/` | generated-protocol exploratory batch | Broad 14-system TwinsOrFalseFriends pass with small seeds/budgets and row caps for large systems. |
| `generated_sampling_protocol.md` | protocol note | Shared strategy/budget plan for datasets without sample traces. |
| `twins_paper_writing_guide.md` | writing guide | Self-contained experiment description, key Twins figures/tables, and paper wording guidance. |
| `newruns_systems/7z/` | paper-ready detail | Per-system 7z report and figures. |
| `newruns_systems/BerkeleyDBC/` | paper-ready detail | Per-system BerkeleyDBC report and figures. |
| `newruns_systems/Dune/` | paper-ready detail | Per-system Dune report and figures. |
| `newruns_systems/Hipacc/` | paper-ready detail | Per-system Hipacc report and figures. |
| `newruns_systems/LLVM/` | paper-ready detail | Per-system LLVM report and figures. |
| `newruns_systems/Polly/` | paper-ready detail | Per-system Polly report and figures. |
| `newruns_systems/lrzip/` | paper-ready detail | Per-system lrzip report and figures. |
| `x264_time_all/` | supporting | Focused x264 time-target/time-cost report. |
| `x264_size_all/` | supporting | Focused x264 size-target/time-cost report. |
| `BerkeleyDBC_performance/` | superseded | Standalone BerkeleyDBC proof-of-concept; replaced by `newruns_systems/BerkeleyDBC/`. |
| `poc_x264_time_0/` | exploratory | First single-input x264 time proof-of-concept. |
| `poc_x264_size_0/` | exploratory | First single-input x264 size proof-of-concept. |
| `x264_matrix_smoke/` | smoke test | Fast x264 matrix script check; not for paper evidence. |
| `newruns_smoke/` | smoke test | Fast NewRuns batch script check; not for paper evidence. |
| `newruns_smoke/BerkeleyDBC/` | smoke detail | Smoke-test BerkeleyDBC per-system output. |
| `newruns_smoke/LLVM/` | smoke detail | Smoke-test LLVM per-system output. |

## Recommended Paper Narrative

Use the artifacts in this order:

1. **x264 2x2 matrix:** Use `x264_matrix/` to show the clean conceptual design: cost property and prediction target are separate axes. This is the best evidence for the four scenarios: time/time, time/size, size/time, and size/size.
2. **NewRuns cross-system replication:** Use `newruns_systems/` to show that the main conclusion is not an x264-only artifact. Here each system has one `Performance` property, so the analysis is `cost=performance, target=performance`.
3. **Generated-sampling outputs:** Use `twins_generated_representative_100s/` for stronger representative Twins evidence, `twins_generated_quick/` for broad triage, and `twins_HSQLDB_generated/`, `twins_brotli_1_0_7_generated/`, and `twins_PostgreSQL_9_6_3_generated/` for focused examples showing how the RQs work when sample traces are absent and we generate a common strategy/budget grid ourselves.
4. **Focused x264 appendices:** Use `x264_time_all/` and `x264_size_all/` if you want simpler single-target explanations or supplementary context-sensitivity details.
5. **Proof-of-concept and smoke outputs:** Use only for provenance/debugging, not as paper evidence.

## Common File Types

Most analysis folders follow this schema:

- `records.csv`: one row per sampled run, strategy, and sample level. Use it for custom checks or new plots.
- `rq1_cost_heterogeneity.csv`: per-configuration cost distribution summaries.
- `strategy_summary.csv`: per-strategy/per-level medians for empirical cost, MRE, calibration, and cost-over-random.
- `rq2_proxy_summary.csv`: Spearman correlation and calibration ratio summaries for `n` as a cost proxy.
- `rq3_rank_stability.csv`: count-cost versus empirical-cost ranking agreement across lambda values.
- `rq4_pareto.csv`: Pareto labels under count cost and empirical cost.
- `context_summary.csv`, `system_summary.csv`, or `scenario_summary.csv`: compact rows for paper tables.
- `*.md`: human-readable report with embedded figures.
- `fig_*.png`: figures ready to include or adapt.

## Primary: `x264_matrix/`

**Use for:** main x264 result and the 2x2 cost-target design.

Main report:

- `x264_matrix/x264_matrix_report.md`

Best paper figures:

- `fig_rq1_cost_time_strategy_bias.png`: strategy bias when cost is time.
- `fig_rq1_cost_size_strategy_bias.png`: strategy bias when cost is size.
- `fig_rq2_cost_time_calibration_by_strategy.png`: sample-size calibration for time cost.
- `fig_rq2_cost_size_calibration_by_strategy.png`: sample-size calibration for size cost.
- `fig_rq3_rank_agreement_by_scenario.png`: ranking robustness without aggregating the four scenarios.
- `fig_rq4_pareto_jaccard_by_scenario.png`: Pareto-front overlap by scenario.
- `fig_rq4_frontier_cost_time__target_time.png`
- `fig_rq4_frontier_cost_time__target_size.png`
- `fig_rq4_frontier_cost_size__target_time.png`
- `fig_rq4_frontier_cost_size__target_size.png`

Best tables/values:

- `cost_property_summary.csv`: concise RQ1/RQ2 values grouped by cost property.
- `scenario_summary.csv`: concise RQ3/RQ4 values for the four scenarios.
- `context_summary.csv`: all x264 input-level scenario rows.

Key result to cite:

- For x264, sample size is highly correlated with empirical cost, but it is not enough to preserve all decisions.
- RQ3 top-1 agreement varies by scenario, from `0.8235` to `0.9496`.
- RQ4 median Pareto Jaccard varies by scenario, from `0.375` to `0.5`.

## Primary: `newruns_systems/`

**Use for:** cross-system evidence beyond x264. This is currently the strongest evidence that empirical cost matters.

Main report:

- `newruns_systems/newruns_systems_report.md`

Best paper figures:

- `fig_rq1_cost_heterogeneity_by_system.png`: cost CV and p90/p10 by system.
- `fig_rq1_strategy_bias_heatmap.png`: strategy-specific empirical cost bias relative to random.
- `fig_rq2_calibration_by_system.png`: `%cost/%n` calibration by system.
- `fig_rq3_rq4_decision_change_by_system.png`: rank and Pareto agreement under count versus empirical cost.

Best tables/values:

- `system_summary.csv`: one row per system, ideal for paper tables.
- `strategy_summary.csv`: strategy-level cost and MRE summaries across systems.
- `rq3_rank_stability.csv`: lambda-level rank agreement.
- `rq4_pareto.csv`: exact count-frontier and empirical-frontier labels.

Key result to cite:

- Across seven systems, cost CV ranges from `0.07236` to `1.981`.
- p90/p10 cost ratio reaches `47.9`.
- Pareto Jaccard ranges from `0.3333` to `1`.
- `lrzip` changes the top-1 recommendation in `5 / 7` lambda settings.

Important caveat:

- These systems expose one `Performance` property in sampled CSVs. The scenario is therefore `cost=performance, target=performance`, not a time/size matrix.

## Generated Protocol: TwinsOrFalseFriends

**Use for:** first implementation of the generated-sampling protocol on a dataset without precomputed sample traces.

Main reports:

- `twins_generated_representative_100s/twins_generated_batch_report.md`
- `twins_generated_representative_100s/twins_hypothesis_report.md`
- `twins_generated_representative_100s/README.md`
- `twins_generated_quick/twins_generated_batch_report.md`
- `twins_generated_quick/twins_hypothesis_report.md`
- `twins_paper_writing_guide.md`
- `twins_HSQLDB_generated/HSQLDB_generated_report.md`
- `twins_brotli_1_0_7_generated/brotli_generated_report.md`
- `twins_PostgreSQL_9_6_3_generated/PostgreSQL_generated_report.md`

Broad-batch figures:

- `twins_generated_quick/fig_cost_cv_range_by_system.png`
- `twins_generated_quick/fig_decision_agreement_by_system.png`
- `twins_generated_quick/fig_rq2_proxy_spearman_by_system_cost.png`
- `twins_generated_quick/fig_rq2_median_calibration_by_system_cost.png`
- `twins_generated_quick/fig_rq3_top1_agreement_heatmap.png`
- `twins_generated_quick/fig_rq4_pareto_jaccard_heatmap.png`
- `twins_generated_quick/fig_twins_hypothesis_verdicts.png`
- `twins_generated_representative_100s/fig_explain_strategy_calibration_heatmap.png`

Best paper figures:

- `paper_figures/twins_brotli_pairwise_n8/`: curated copy of the brotli fixed-`n=8` explanatory figure set, with caption/provenance notes.
- `paper_figures/twins_lrzip_n_proxy_counterexample/`: curated fixed-`n=16` counterexample where two strategies have nearly identical MRE but a 16.5x empirical-cost gap.
- `paper_figures/twins_jump3r_runlevel_n_proxy_counterexample/`: non-LCBench/non-Linux run-level fixed-`n=128` counterexample with about 17.5% MRE and a 12.5x empirical-cost gap.
- `paper_figures/lcbench_christine_n_proxy_counterexample/`: cleaner low-MRE fixed-`n=8` counterexample where two strategies have about 4.1% MRE but a 31.3x empirical-cost gap.
- `fig_explain_strategy_calibration_heatmap.png`: strategy calibration bias by system-cost context.
- `fig_explain_cost_error_*.png`: per-system run-level cost-distribution plus MRE plots; each point is one generated sample run at one budget.
- `fig_explain_strategy_budget_path_*.png`: aggregated strategy/budget trajectories; one point per strategy and budget using median cost fraction and median MRE.
- `fig_explain_fixed_n8_*.png`: fixed-budget strategy comparison; one point per strategy at `n=8`, with seed-IQR error bars for stochastic strategies.
- `brotli_1_0_7/fig_explain_fixed_n8_cost_performance__target_energy_deployable.png`: clean deployable-only caricature of `pairwise` being costly and inaccurate under the same `n=8` budget.
- `fig_rq2_calibration_cost_performance.png`: count-vs-performance-cost calibration.
- `fig_rq2_calibration_cost_energy.png`: count-vs-energy-cost calibration.
- `fig_rq3_rank_agreement_by_scenario.png`: ranking robustness for the four `performance/energy` scenarios.
- `fig_rq4_pareto_jaccard_by_scenario.png`: Pareto-front overlap by scenario.
- `fig_rq4_frontier_cost_performance__target_performance.png`
- `fig_rq4_frontier_cost_performance__target_energy.png`
- `fig_rq4_frontier_cost_energy__target_performance.png`
- `fig_rq4_frontier_cost_energy__target_energy.png`

Best tables/values:

- `scenario_summary.csv`: one row per cost-target scenario.
- `hypothesis_tests.csv` and `hypothesis_summary.csv`: formal H1--H4 verdicts.
- `strategy_calibration_summary.csv`: per-strategy bootstrap calibration checks.
- `strategy_summary.csv`: strategy/budget rows for generated strategies.
- `records.csv`: one row per generated sample run.

Focused Twins folders now also contain `twins_hypothesis_report.md`,
`hypothesis_tests.csv`, `hypothesis_summary.csv`, and
`strategy_calibration_summary.csv`.

Key result to cite:

- The representative 100-seed Twins run covers seven selected systems and 28 cost-target scenarios with no row caps. H1a is supported in `11 / 14` system-cost contexts, H1b in `14 / 14`, H2a in `14 / 14`, H2c in `14 / 14`, H3a in `24 / 28`, H4a/H4b in `28 / 28`, and H3b has Spearman rho `0.719`.
- The 14-system quick batch covers 56 cost-target scenarios. H1a is supported in `23 / 28` system-cost contexts, H2a in `28 / 28`, H2c in `27 / 28`, H3a in `54 / 56`, and H4a/H4b in `56 / 56`.
- H1b is underpowered in the quick batch: with three seeds, fixed-n Kruskal-Wallis tests are inconclusive even though observed eta-squared values are often large.
- HSQLDB has moderate cost heterogeneity: CV `0.319` for performance cost and `0.3584` for energy cost. Top-1 agreement is `0.4286` to `0.5714`; Pareto Jaccard is `0.5` to `0.5789`.
- brotli `1.0.7` is a strong generated-protocol stress case: performance-cost CV `2.092`, energy-cost CV `1.974`, and p90/p10 up to `149.4`.
- PostgreSQL `9.6.3` is the contrast case: cost CV is low (`0.06788` performance, `0.05719` energy), sample-size calibration is almost perfect, but Pareto sets still differ.

Important caveat:

- These first runs used `20` stochastic seeds for speed. Use `--seeds 100` for paper-scale replication.
- The broad batch used `3` seeds, max budget `32`, and a `5000`-row cap for large systems; treat it as exploratory triage.
- Keep generated-protocol folders separate from `x264_matrix/` and `newruns_systems/` in aggregate figures.

### `newruns_systems/7z/`

**Use for:** a strong non-x264 case where cost is heterogeneous and decisions change.

Main report:

- `newruns_systems/7z/7z_performance_report.md`

Key values:

- Cost CV: `1.188`.
- p90/p10: `10.13`.
- Top-1 flips: `1 / 7`.
- Pareto Jaccard: `0.4286`.

### `newruns_systems/BerkeleyDBC/`

**Use for:** a very strong case study showing severe calibration bias.

Main report:

- `newruns_systems/BerkeleyDBC/BerkeleyDBC_performance_report.md`

Key values:

- Cost CV: `1.42`.
- p90/p10: `47.9`.
- Median `%cost/%n`: `0.7967`.
- Pareto Jaccard: `0.6`.

### `newruns_systems/Dune/`

**Use for:** contrast case where empirical cost differs but decisions are more stable.

Main report:

- `newruns_systems/Dune/Dune_performance_report.md`

Key values:

- Cost CV: `0.3438`.
- p90/p10: `1.827`.
- Top-1 flips: `0 / 7`.
- Pareto Jaccard: `1`.

### `newruns_systems/Hipacc/`

**Use for:** contrast case with moderate heterogeneity and stable rankings/frontiers.

Main report:

- `newruns_systems/Hipacc/Hipacc_performance_report.md`

Key values:

- Cost CV: `0.4352`.
- p90/p10: `2.59`.
- Median `%cost/%n`: `1.056`.
- Pareto Jaccard: `1`.

### `newruns_systems/LLVM/`

**Use for:** low-heterogeneity system where rank conclusions are stable, but Pareto analysis still changes.

Main report:

- `newruns_systems/LLVM/LLVM_performance_report.md`

Key values:

- Cost CV: `0.07236`.
- p90/p10: `1.212`.
- Top-1 flips: `0 / 7`.
- Pareto Jaccard: `0.3333`.

### `newruns_systems/Polly/`

**Use for:** mostly calibrated system with incomplete reconstructed coverage.

Main report:

- `newruns_systems/Polly/Polly_performance_report.md`

Key values:

- Reconstructed configurations: `59897 / 60000`.
- Cost CV: `0.2389`.
- Median `%cost/%n`: `0.9966`.
- Pareto Jaccard: `0.5`.

Caveat:

- The sampled CSVs reconstruct nearly all, but not all, configurations. Use this as a valid case with a stated coverage caveat.

### `newruns_systems/lrzip/`

**Use for:** strongest decision-change case.

Main report:

- `newruns_systems/lrzip/lrzip_performance_report.md`

Key values:

- Cost CV: `1.981`.
- p90/p10: `47.04`.
- Top-1 flips: `5 / 7`.
- Pareto Jaccard: `0.6`.

## Focused: `x264_time_all/`

**Use for:** simpler x264 explanation where cost and prediction target are both time.

Main report:

- `x264_time_all/x264_time_report.md`

Best figures:

- `fig_rq1_strategy_cost_bias.png`
- `fig_rq3_aggregate_rank_agreement.png`
- `fig_rq5_context_sensitivity.png`

Key result:

- Across 17 inputs, time-cost CV ranges from `0.212` to `0.3898`, with median `0.2529`.
- Top-1 ranking changes in `6 / 119` `(context, lambda)` cases.
- Median Pareto Jaccard is `0.4286`.

Use when you want a readable single-scenario story without the full 2x2 matrix.

## Focused: `x264_size_all/`

**Use for:** x264 size prediction with time as empirical acquisition cost.

Main report:

- `x264_size_all/x264_size_report.md`

Best figures:

- `fig_rq1_strategy_cost_bias.png`
- `fig_rq3_aggregate_rank_agreement.png`
- `fig_rq5_context_sensitivity.png`

Key result:

- Time-cost CV again ranges from `0.212` to `0.3898`, with median `0.2529`.
- Top-1 ranking changes in `21 / 119` `(context, lambda)` cases.
- Median Pareto Jaccard is `0.375`.

Use to support the claim that the prediction target matters: size prediction is more sensitive than time prediction under time cost.

## Standalone: `BerkeleyDBC_performance/`

**Use for:** historical standalone BerkeleyDBC run.

Main report:

- `BerkeleyDBC_performance/BerkeleyDBC_performance_report.md`

Status:

- Superseded by `newruns_systems/BerkeleyDBC/`.
- Keep only as provenance for the first non-x264 proof-of-concept.
- For paper writing, cite `newruns_systems/BerkeleyDBC/` instead.

## Proofs of Concept: `poc_x264_time_0/` and `poc_x264_size_0/`

**Use for:** debugging and explaining the first prototype on a single x264 input.

Reports:

- `poc_x264_time_0/summary.md`
- `poc_x264_size_0/summary.md`

Status:

- Not paper-ready as main evidence.
- Useful if you need a minimal example for methods debugging or a quick sanity check.
- Superseded by `x264_time_all/`, `x264_size_all/`, and especially `x264_matrix/`.

## Smoke Tests: `x264_matrix_smoke/` and `newruns_smoke/`

**Use for:** testing scripts on smaller subsets.

Status:

- Do not cite in the paper.
- These folders are useful to verify that scripts run quickly after edits.
- Superseded by `x264_matrix/` and `newruns_systems/`.

## Suggested Main-Paper Figure Set

For a compact paper, use:

1. `x264_matrix/fig_rq3_rank_agreement_by_scenario.png`
   - Shows why the four cost-target scenarios should not be aggregated.
2. `x264_matrix/fig_rq4_pareto_jaccard_by_scenario.png`
   - Quantifies Pareto-front disagreement for the x264 2x2 matrix.
3. One x264 Pareto-front plane, for example:
   - `x264_matrix/fig_rq4_frontier_cost_time__target_size.png`
   - This is intuitive: x-axis is cost, y-axis is MRE.
4. `newruns_systems/fig_rq1_cost_heterogeneity_by_system.png`
   - Shows cross-system empirical cost heterogeneity.
5. `newruns_systems/fig_rq1_strategy_bias_heatmap.png`
   - Shows that strategy choice changes empirical cost at fixed sample size.
6. `newruns_systems/fig_rq3_rq4_decision_change_by_system.png`
   - Shows decision-level consequences beyond calibration.

## Suggested Tables

Main paper:

- `x264_matrix/scenario_summary.csv`: four scenario rows for RQ3/RQ4.
- `newruns_systems/system_summary.csv`: one row per non-x264 system.

Appendix:

- `x264_matrix/cost_property_summary.csv`: RQ1/RQ2 grouped by cost property.
- `x264_matrix/context_summary.csv`: x264 input-level details.
- `newruns_systems/strategy_summary.csv`: strategy-level cross-system cost bias.
- Per-system `strategy_summary.csv` files under `newruns_systems/<system>/`.

## Wording Guidance

Safe wording:

> Sample size remains a useful coarse effort axis, but it is not a calibrated empirical-cost model. The discrepancy matters because it can change strategy rankings and Pareto-efficient choices.

For x264:

> The x264 matrix shows that cost validity should be separated from prediction target: RQ1/RQ2 are properties of the cost axis, while RQ3/RQ4 depend on the cost-target scenario.

For NewRuns:

> The NewRuns systems strengthen the claim beyond x264: in several systems, empirical cost heterogeneity and strategy-specific cost bias are large enough to affect cost-sensitive decisions.

Avoid claiming:

> Sample size is useless.

The evidence is subtler: sample size is often strongly correlated with empirical cost, but correlation does not guarantee calibration or decision stability.
