# Twins Brotli Pairwise n8 Figure Set

## Purpose

This folder saves a paper-facing copy of the clearest current explanatory
example for the generated-sampling protocol. The case is deliberately narrow:
TwinsOrFalseFriends `brotli`, revision `1.0.7`, cost=`performance`,
target=`energy`, deployable strategies only, with diagnostic oracles excluded.

The main point is that the sampling strategy can be badly calibrated with
respect to empirical acquisition cost even when the nominal sample size is
fixed. At `n=8`, `pairwise` operates in a much costlier region and still gives
much worse prediction error.

## Files

| File | Recommended use |
|---|---|
| `brotli_trajectory_with_performance_distribution_deployable.png` | Main paper figure. Top panel shows the full performance-cost distribution; bottom panel connects each deployable strategy across increasing `n`. |
| `brotli_fixed_n8_with_performance_distribution_deployable.png` | Fixed-`n` variant. Top panel shows the full performance-cost distribution; bottom panel shows where each deployable strategy operates at fixed `n=8`. |
| `brotli_fixed_n8_performance_cost_energy_target_deployable.png` | Compact variant. One point per deployable strategy at fixed `n=8`; x-axis is median fraction of full performance cost; y-axis is median MRE predicting energy. |
| `brotli_strategy_budget_trajectories_performance_cost_energy_target_deployable.png` | Supporting figure. One median point per strategy and budget, connected to show how each strategy moves as `n` increases. |
| `brotli_run_level_cost_error_performance_cost_energy_target_deployable.png` | Appendix/debug figure. Full run-level diagnostic with cost distribution and sample mean cost versus MRE. |

## Key Numbers

At fixed `n=8`:

| Strategy | Full-cost fraction | Median MRE |
|---|---:|---:|
| `pairwise` | 31.19% | 47.98 |
| `random` | 4.228% | 0.7828 |
| `balanced` | 4.655% | 0.7418 |
| `pilotCost` | 2.352% | 0.5333 |
| `diversity` | 7.389% | 1.203 |

Interpretation: `pairwise` is dominated for the fixed `n=8` comparison. It
costs about 7.4x more than `random` while having roughly 61x higher median MRE.
This is a concrete mechanism figure for the broader claim that sample count is
not enough to characterize acquisition cost.

## Suggested Caption

Strategy-trajectory comparison on TwinsOrFalseFriends `brotli` revision
`1.0.7`, using measured `performance` as acquisition cost and measured
`energy` as prediction target. The top panel shows the full distribution of
per-configuration performance cost; the bottom panel connects increasing
sample sizes for deployable strategies and excludes diagnostic oracles. The
`pairwise` strategy operates in the costly tail at low `n` and only reaches low
error after consuming almost the full empirical budget, illustrating that
nominal sample size can hide strategy-specific cost bias.

## Provenance

Canonical generated outputs:

- `artifacts/twins_generated_representative_100s/brotli_1_0_7/fig_explain_fixed_n8_cost_performance__target_energy_deployable.png`
- `artifacts/twins_generated_representative_100s/brotli_1_0_7/fig_explain_strategy_budget_path_cost_performance__target_energy_deployable.png`
- `artifacts/twins_generated_representative_100s/brotli_1_0_7/fig_explain_cost_error_cost_performance__target_energy_deployable.png`
- `artifacts/twins_generated_representative_100s/brotli_1_0_7/strategy_summary.csv`
- `artifacts/twins_generated_representative_100s/brotli_1_0_7/records.csv`

Regenerate the source figures with:

```bash
python3 scripts/plot_twins_explanatory_bias.py \
  --input-dir artifacts/twins_generated_representative_100s \
  --systems brotli_1.0.7 \
  --scenarios performance:energy \
  --fixed-levels n8 \
  --exclude-oracles
```

Then copy the regenerated source figures into this folder if the paper-facing
copies need to be refreshed.

Regenerate the paper-facing distribution figure with:

```bash
python3 scripts/plot_twins_fixed_n_with_distribution.py \
  --output artifacts/paper_figures/twins_brotli_pairwise_n8/brotli_fixed_n8_with_performance_distribution_deployable.png
```

Regenerate the paper-facing trajectory + distribution figure with:

```bash
python3 scripts/plot_twins_trajectory_with_distribution.py \
  --output artifacts/paper_figures/twins_brotli_pairwise_n8/brotli_trajectory_with_performance_distribution_deployable.png
```
