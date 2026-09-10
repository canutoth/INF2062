# Generated sampling pilot on LCBench

## Scope

Source JSON: `/private/tmp/lcbench/data_2k_lw.json`

Target column: `final_val_accuracy`. Cost column: `time_total`.

OpenML datasets analyzed: `APSFailure, Amazon_employee_access, Australian, Fashion-MNIST, KDDCup09_appetency, MiniBooNE, adult, airlines, albert, bank-marketing, blood-transfusion-service-center, car, christine, cnae-9, connect-4, covertype, credit-g, dionis, fabert, helena, higgs, jannis, jasmine, jungle_chess_2pcs_raw_endgame_complete, kc1, kr-vs-kp, mfeat-factors, nomao, numerai28.6, phoneme, segment, shuttle, sylvine, vehicle, volkert`

Encoded hyperparameter columns: `17`.

LCBench is treated as a workload-style benchmark: each OpenML dataset is a distinct context,
the sampled objects are hyperparameter configurations, and acquisition cost is the cumulative
training runtime of a configuration on that dataset.

## Per-dataset summary

| Dataset | Cost CV | Spearman(n,cost) | Median %cost/%n | Top-1 flips / 7 | Pareto Jaccard |
|---|---:|---:|---:|---:|---:|
| `APSFailure` | 1.301 | 0.4682 | 0.8988 | 5/7 | 0.2 |
| `Amazon_employee_access` | 0.9237 | 0.5376 | 0.9837 | 5/7 | 0.4 |
| `Australian` | 0.9998 | 0.5029 | 0.8415 | 4/7 | 1 |
| `Fashion-MNIST` | 0.5947 | 0.4682 | 1.034 | 6/7 | 0.2857 |
| `KDDCup09_appetency` | 1.128 | 0.4856 | 0.9279 | 4/7 | 0.4 |
| `MiniBooNE` | 2.247 | 0.3989 | 0.8572 | 0/7 | 1 |
| `adult` | 1.239 | 0.6243 | 0.8671 | 7/7 | 0.5 |
| `airlines` | 1.581 | 0.5029 | 0.8396 | 6/7 | 0.6667 |
| `albert` | 1.593 | 0.3295 | 0.9423 | 6/7 | 0.4 |
| `bank-marketing` | 1.199 | 0.6243 | 0.8815 | 4/7 | 0.4 |
| `blood-transfusion-service-center` | 1.013 | 0.5376 | 0.8502 | 4/7 | 1 |
| `car` | 0.9829 | 0.5376 | 0.8504 | 4/7 | 1 |
| `christine` | 0.71 | 0.4682 | 1.017 | 5/7 | 0.5 |
| `cnae-9` | 0.655 | 0.4682 | 1.013 | 5/7 | 0.3333 |
| `connect-4` | 1.1 | 0.555 | 0.9471 | 4/7 | 0.5 |
| `covertype` | 1.703 | 0.2948 | 1.01 | 6/7 | 0.2 |
| `credit-g` | 0.9841 | 0.4509 | 0.8475 | 6/7 | 0.4 |
| `dionis` | 1.25 | 0.4856 | 0.9998 | 5/7 | 0.3333 |
| `fabert` | 0.6428 | 0.4682 | 1.027 | 6/7 | 0.25 |
| `helena` | 0.8877 | 0.5896 | 0.9686 | 5/7 | 0.1667 |
| `higgs` | 1.314 | 0.555 | 0.9191 | 3/7 | 0.6667 |
| `jannis` | 1.366 | 0.5723 | 0.9325 | 4/7 | 0.4 |
| `jasmine` | 0.932 | 0.5376 | 0.8384 | 5/7 | 0.2857 |
| `jungle_chess_2pcs_raw_endgame_complete` | 0.9472 | 0.6243 | 0.8999 | 0/7 | 0.25 |
| `kc1` | 0.9861 | 0.4682 | 0.8432 | 4/7 | 0.5 |
| `kr-vs-kp` | 0.9602 | 0.4682 | 0.8598 | 4/7 | 0.5 |
| `mfeat-factors` | 0.8691 | 0.5029 | 0.8579 | 5/7 | 0.2 |
| `nomao` | 0.8467 | 0.607 | 0.9172 | 7/7 | 0.2857 |
| `numerai28.6` | 1.237 | 0.555 | 0.9279 | 6/7 | 0.6667 |
| `phoneme` | 0.9659 | 0.6417 | 0.8622 | 6/7 | 0.4 |
| `segment` | 0.9816 | 0.4682 | 0.8482 | 5/7 | 0.25 |
| `shuttle` | 1.064 | 0.6243 | 0.9379 | 6/7 | 0.6667 |
| `sylvine` | 0.9568 | 0.4856 | 0.8538 | 4/7 | 0.4 |
| `vehicle` | 1.002 | 0.4682 | 0.8426 | 7/7 | 0.5 |
| `volkert` | 1.018 | 0.607 | 0.8902 | 4/7 | 0.4 |

## H5a-style context sensitivity

p-value: `1`; ratio spread: `0.1954`; verdict: `refutes`.
