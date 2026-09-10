# Generated sampling pilot on LCBench

## Scope

Source JSON: `/private/tmp/lcbench/six_datasets_lw.json`

Target column: `final_val_accuracy`. Cost column: `time_total`.

OpenML datasets analyzed: `Fashion-MNIST, adult, higgs, jasmine, vehicle, volkert`

Encoded hyperparameter columns: `17`.

LCBench is treated as a workload-style benchmark: each OpenML dataset is a distinct context,
the sampled objects are hyperparameter configurations, and acquisition cost is the cumulative
training runtime of a configuration on that dataset.

## Per-dataset summary

| Dataset | Cost CV | Spearman(n,cost) | Median %cost/%n | Top-1 flips / 7 | Pareto Jaccard |
|---|---:|---:|---:|---:|---:|
| `Fashion-MNIST` | 0.5947 | 0.6997 | 0.9848 | 3/7 | 0.4444 |
| `adult` | 1.239 | 0.8828 | 0.8249 | 6/7 | 0.5714 |
| `higgs` | 1.314 | 0.8549 | 0.8466 | 5/7 | 0.4444 |
| `jasmine` | 0.932 | 0.858 | 0.6801 | 4/7 | 0.2 |
| `vehicle` | 1.002 | 0.8778 | 0.675 | 6/7 | 0.4 |
| `volkert` | 1.018 | 0.8762 | 0.8574 | 3/7 | 0.6667 |

## H5a-style context sensitivity

p-value: `1.184e-05`; ratio spread: `0.3098`; verdict: `supports`.
