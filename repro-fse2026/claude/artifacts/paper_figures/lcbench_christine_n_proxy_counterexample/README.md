# LCBench Christine n-Proxy Counterexample

## Purpose

This figure is the cleaner, low-error version of the fixed-`n` counterexample.
It uses the LCBench pilot output for workload `christine`, cost=`time_total`,
and target=`final_val_accuracy`.

All strategies use the same nominal sample size, `n=8`. The x-axis is empirical
training cost, measured as a percentage of the full training-time cost, on a
log scale. The y-axis is median MRE when predicting validation accuracy.

## Main Figure

- `lcbench_christine_fixed_n8_empirical_cost_gap_time_cost_accuracy_target.png`

## Key Numbers

At fixed `n=8`:

| Strategy | Full-cost fraction | Median MRE |
|---|---:|---:|
| `pilotCost` | 0.0155% | 0.04107 |
| `pairwise` | 0.4857% | 0.04134 |
| `random` | 0.4180% | 0.04004 |
| `balanced` | 0.4488% | 0.03947 |
| `diversity` | 0.3509% | 0.03753 |

The headline contrast is `pilotCost` versus `pairwise`: both select 8
configurations and have essentially the same MRE (`0.04107` vs `0.04134`), but
`pairwise` costs 31.3x more empirically. This is the clearest current figure
for showing that `n` can fail as a cost proxy even when prediction error is in
a reasonable range.

## Suggested Caption

Fixed-sample-size counterexample on LCBench workload `christine`
(cost=`time_total`, target=`final_val_accuracy`). All deployable strategies
select the same number of configurations (`n=8`). `pilotCost` and `pairwise`
obtain nearly identical median MRE (`0.04107` vs `0.04134`), yet their measured
training cost differs by 31.3x. The nominal sample count is identical, but the
real acquisition cost is not.

## Provenance

Source table:

- `artifacts/lcbench_data_2k_lw/strategy_summary.csv`

Regenerate with:

```bash
python3 scripts/plot_twins_n_proxy_counterexample.py \
  --input-dir artifacts/lcbench_data_2k_lw \
  --system-folder . \
  --workload christine \
  --label LCBench/christine \
  --title "LCBench/christine: fixed n=8, 31x cost gap at 4% MRE" \
  --cost time_total \
  --cost-label "training time" \
  --target final_val_accuracy \
  --target-label "validation accuracy" \
  --level n8 \
  --cheap-strategy pilotCost \
  --expensive-strategy pairwise \
  --output artifacts/paper_figures/lcbench_christine_n_proxy_counterexample/lcbench_christine_fixed_n8_empirical_cost_gap_time_cost_accuracy_target.png
```

