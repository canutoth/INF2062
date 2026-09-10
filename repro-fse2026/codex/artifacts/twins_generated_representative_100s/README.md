# TwinsOrFalseFriends Representative 100-Seed Run

## Purpose

This folder contains a stronger generated-sampling experiment for the
TwinsOrFalseFriends tier. It is intended to provide more conclusive evidence
than the broad `twins_generated_quick/` triage batch while keeping runtime
manageable.

The run covers seven representative systems:

- High cost heterogeneity: `brotli`, `jump3r`, `lrzip`
- Moderate/familiar cases: `HSQLDB`, `x264`
- Low-heterogeneity contrasts: `MongoDB`, `PostgreSQL`

Revisioned systems are filtered to the latest revision by
`scripts/run_twins_batch.py`: `brotli=1.0.7` and `PostgreSQL=11.2`.

## Command

```bash
python3 scripts/run_twins_batch.py \
  --systems HSQLDB,brotli,jump3r,lrzip,MongoDB,PostgreSQL,x264 \
  --seeds 100 \
  --max-budget 256 \
  --max-rows 0 \
  --output-dir artifacts/twins_generated_representative_100s \
  --continue-on-error

python3 scripts/run_twins_hypotheses.py \
  --input-dir artifacts/twins_generated_representative_100s

python3 scripts/summarize_twins_generated_batch.py \
  --input-dir artifacts/twins_generated_representative_100s

python3 scripts/plot_twins_explanatory_bias.py \
  --input-dir artifacts/twins_generated_representative_100s \
  --fixed-levels n8

python3 scripts/plot_twins_explanatory_bias.py \
  --input-dir artifacts/twins_generated_representative_100s \
  --systems brotli_1.0.7 \
  --scenarios performance:energy \
  --fixed-levels n8 \
  --exclude-oracles

python3 scripts/summarize_twins_generated_batch.py \
  --input-dir artifacts/twins_generated_representative_100s
```

This is a long-running command. On the current machine it ran successfully
within one interactive session, but high-row systems dominate runtime because
feature-balanced and pilot-cost sampling are Python-level loops.

## Outputs

Main reports:

- `twins_generated_batch_report.md`
- `twins_hypothesis_report.md`

Main tables:

- `system_summary.csv`: selected systems, filters, row counts, and report paths.
- `scenario_summary.csv`: 28 rows, one per system and cost-target scenario.
- `hypothesis_tests.csv`: formal H1--H4 test rows.
- `hypothesis_summary.csv`: support/refute/inconclusive counts.
- `strategy_calibration_summary.csv`: bootstrap calibration checks by strategy.

Main figures:

- `fig_cost_cv_range_by_system.png`
- `fig_rq2_proxy_spearman_by_system_cost.png`
- `fig_rq2_median_calibration_by_system_cost.png`
- `fig_rq3_top1_agreement_heatmap.png`
- `fig_rq4_pareto_jaccard_heatmap.png`
- `fig_twins_hypothesis_verdicts.png`
- `fig_explain_strategy_calibration_heatmap.png`

Mechanism/explanation figures:

- `fig_explain_strategy_calibration_heatmap.png`: batch-level strategy calibration bias.
- Per-system `fig_explain_cost_error_*.png`: full cost distribution plus sample mean cost versus MRE for each cost-target scenario.
- Per-system `fig_explain_strategy_budget_path_*.png`: aggregated median cost/MRE trajectory, one point per strategy and budget.
- Per-system `fig_explain_fixed_n8_*.png`: fixed-`n=8` strategy comparison, one point per strategy with seed-IQR error bars where applicable.
- `brotli_1_0_7/*_deployable.png`: deployable-only versions of the brotli cost=`performance`, target=`energy` explanatory plots, excluding diagnostic oracles.

Each per-system subfolder also contains the detailed generated report, RQ CSVs,
and per-scenario Pareto-front figures.

## Key Findings

- RQ1/H1a: cost heterogeneity is supported in `11/14` system-cost contexts.
- RQ1/H1b: fixed-n strategy cost effects are supported in `14/14` contexts.
- RQ2/H2a: `n` is positively rank-correlated with empirical cost in `14/14` contexts.
- RQ2/H2b: aggregate median calibration is mixed; only `4/14` contexts clearly deviate from 1.
- RQ2/H2c: calibration depends on strategy in `14/14` contexts.
- RQ3/H3a: count-cost and empirical-cost rankings differ in `24/28` scenarios.
- RQ3/H3b: cost CV correlates with rank-flip count across scenarios, Spearman rho `0.719`.
- RQ4/H4a/H4b: empirical-cost Pareto frontiers differ from count-cost frontiers in `28/28` scenarios.

## How To Cite This Folder

Use this folder for representative, higher-confidence Twins evidence. State the
scope explicitly: seven systems, 100 stochastic seeds, no row caps, max budget
256, four performance/energy cost-target scenarios per system.

Do not describe it as a full 14-system Twins replication. For full coverage,
use `twins_generated_quick/` as triage evidence or rerun all 14 systems with
the same 100-seed protocol.
