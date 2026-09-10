# Twins jump3r Run-Level n-Proxy Counterexample

## Purpose

This is a non-LCBench, non-Linux counterexample showing that nominal sample size
can hide a large real-cost difference. It uses the TwinsOrFalseFriends
`jump3r` representative run, cost=`performance`, target=`energy`, and fixed
sample size `n=128`.

Unlike the `lrzip` and `LCBench/christine` figures, this is a run-level figure:
each faint point is one generated sample run at the same `n`, and the two large
markers are two actual repeated samples selected from the cloud. This makes the
figure useful for explaining variability that is hidden by strategy medians.

## Main Figure

- `jump3r_fixed_n128_runlevel_cost_gap_performance_cost_energy_target.png`

## Key Numbers

Highlighted runs at fixed `n=128`:

| Strategy/run | Full-cost fraction | MRE |
|---|---:|---:|
| `pilotCost` run `62` | 0.2255% | 0.1738 |
| `random` run `32` | 2.8265% | 0.1757 |

The highlighted runs have nearly identical prediction error, but the `random`
sample costs 12.5x more empirically. This is a clearer non-LCBench example
than the `lrzip` fixed-`n=16` stress case because the error is below 20% MRE.

## Interpretation

The figure should be described as a run-level witness, not a median strategy
comparison. The broader cloud shows why the witness exists: with heavy-tailed
configuration costs, repeated samples at the same nominal `n` can land in very
different empirical-cost regions while producing similar prediction quality.

## Suggested Caption

Run-level fixed-sample-size counterexample on TwinsOrFalseFriends `jump3r`
(cost=`performance`, target=`energy`). All points use `n=128`; faint markers
show repeated generated samples, and the two large markers highlight one
`pilotCost` run and one `random` run with nearly identical MRE (`0.1738` vs
`0.1757`). Despite the same sample size and similar prediction error, the
measured training cost differs by 12.5x.

## Provenance

Source table:

- `artifacts/twins_generated_representative_100s/jump3r/records.csv`

Regenerate with:

```bash
python3 scripts/plot_records_n_proxy_counterexample.py \
  --records artifacts/twins_generated_representative_100s/jump3r/records.csv \
  --cost performance \
  --target energy \
  --level n128 \
  --cheap-strategy pilotCost \
  --cheap-run 62 \
  --expensive-strategy random \
  --expensive-run 32 \
  --label Twins/jump3r \
  --title "Twins/jump3r: fixed n=128, same MRE, 12.5x cost gap" \
  --cost-label performance \
  --target-label energy \
  --output artifacts/paper_figures/twins_jump3r_runlevel_n_proxy_counterexample/jump3r_fixed_n128_runlevel_cost_gap_performance_cost_energy_target.png
```

