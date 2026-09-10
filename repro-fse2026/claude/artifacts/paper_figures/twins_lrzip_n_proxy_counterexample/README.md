# Twins lrzip n-Proxy Counterexample

## Purpose

This figure is a within-Twins counterexample to the idea that nominal sample
size `n` is a sufficient proxy for real acquisition cost. It uses the
TwinsOrFalseFriends `lrzip` system, cost=`performance`, target=`energy`, and
deployable strategies only.

All points use the same nominal sample size, `n=16`. The x-axis is empirical
training cost, measured as a percentage of the full configuration universe's
`performance` cost, on a log scale. The y-axis is median MRE when predicting
`energy`.

## Main Figure

- `lrzip_fixed_n16_empirical_cost_gap_performance_cost_energy_target.png`
- `lrzip_fixed_n16_empirical_cost_gap_side_panel.png` is the paper-facing
  plot used on the right side of the integrated Figure 1 float. The LaTeX
  source builds the left-hand sampling-principle panel and selected-row
  excerpt from real `n=16` samples.
- `lrzip_fixed_n16_empirical_cost_gap_compact.png` is the earlier compact
  single-panel variant.

## Key Numbers

At fixed `n=16`:

| Strategy | Full-cost fraction | Median MRE |
|---|---:|---:|
| `pilotCost` | 0.0344% | 0.5128 |
| `diversity` | 0.5671% | 0.5235 |
| `balanced` | 0.3097% | 0.5240 |
| `random` | 0.2753% | 0.5566 |
| `pairwise` | 0.2522% | 0.3679 |

The most direct contrast is `pilotCost` versus `diversity`: both select 16
configurations and obtain nearly the same prediction error, but `diversity`
costs 16.5x more empirically. This makes the count proxy look blind: by `n`,
the two designs are indistinguishable, but by measured acquisition cost they
are not comparable. The error level is high because this is a low-budget
Twins stress case; use `../lcbench_christine_n_proxy_counterexample/` when the
paper needs the same message with a much lower MRE.

`pairwise` is included for context because it is more accurate in this scenario;
the figure's main claim is not that the cheapest strategy is always best, but
that equal `n` can hide order-of-magnitude acquisition-cost differences among
similarly accurate strategies.

## Suggested Caption

Fixed-sample-size counterexample on TwinsOrFalseFriends `lrzip`
(cost=`performance`, target=`energy`). All deployable strategies select the
same number of configurations (`n=16`), but empirical acquisition cost varies
substantially. `pilotCost` and `diversity` have almost identical MRE
(`0.513` vs `0.524`) while differing by `16.5x` in measured training cost,
showing that sample count alone can be a poor cost proxy.

## Provenance

Source table:

- `artifacts/twins_generated_representative_100s/lrzip/strategy_summary.csv`

Regenerate with:

```bash
python3 scripts/plot_twins_n_proxy_counterexample.py
```

Paper-facing right-side plot:

```bash
python3 scripts/plot_twins_n_proxy_counterexample.py \
  --side-panel \
  --hide-summary-box \
  --no-title \
  --output artifacts/paper_figures/twins_lrzip_n_proxy_counterexample/lrzip_fixed_n16_empirical_cost_gap_side_panel.png
```

Earlier compact plot:

```bash
python3 scripts/plot_twins_n_proxy_counterexample.py \
  --compact \
  --hide-summary-box \
  --no-title \
  --output artifacts/paper_figures/twins_lrzip_n_proxy_counterexample/lrzip_fixed_n16_empirical_cost_gap_compact.png
```

Equivalent explicit command:

```bash
python3 scripts/plot_twins_n_proxy_counterexample.py \
  --input-dir artifacts/twins_generated_representative_100s \
  --system-folder lrzip \
  --cost performance \
  --target energy \
  --level n16 \
  --cheap-strategy pilotCost \
  --expensive-strategy diversity \
  --output artifacts/paper_figures/twins_lrzip_n_proxy_counterexample/lrzip_fixed_n16_empirical_cost_gap_performance_cost_energy_target.png
```
