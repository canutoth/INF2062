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
| `APSFailure` | 1.301 | 0.8675 | 0.8427 | 7/7 | 0.4 |
| `Amazon_employee_access` | 0.9237 | 0.912 | 0.8157 | 6/7 | 0.4545 |
| `Australian` | 0.9998 | 0.9072 | 0.6694 | 4/7 | 0.6 |
| `Fashion-MNIST` | 0.5947 | 0.7073 | 1.012 | 3/7 | 0.4444 |
| `KDDCup09_appetency` | 1.128 | 0.8822 | 0.853 | 4/7 | 0.4545 |
| `MiniBooNE` | 2.247 | 0.8618 | 0.7822 | 7/7 | 0.5 |
| `adult` | 1.239 | 0.8976 | 0.8263 | 6/7 | 0.4 |
| `airlines` | 1.581 | 0.846 | 0.8196 | 2/7 | 0.4 |
| `albert` | 1.593 | 0.8103 | 0.8116 | 6/7 | 0.5556 |
| `bank-marketing` | 1.199 | 0.9006 | 0.8274 | 0/7 | 0.3333 |
| `blood-transfusion-service-center` | 1.013 | 0.9107 | 0.6776 | 5/7 | 1 |
| `car` | 0.9829 | 0.9131 | 0.6863 | 4/7 | 1 |
| `christine` | 0.71 | 0.5433 | 0.9955 | 3/7 | 0.375 |
| `cnae-9` | 0.655 | 0.5873 | 0.987 | 6/7 | 0.3 |
| `connect-4` | 1.1 | 0.8948 | 0.8329 | 6/7 | 0.75 |
| `covertype` | 1.703 | 0.8433 | 0.8419 | 6/7 | 0.75 |
| `credit-g` | 0.9841 | 0.9071 | 0.6754 | 5/7 | 0.8 |
| `dionis` | 1.25 | 0.8691 | 0.8322 | 3/7 | 0.2308 |
| `fabert` | 0.6428 | 0.5963 | 1.002 | 4/7 | 0.8333 |
| `helena` | 0.8877 | 0.9118 | 0.8489 | 6/7 | 0.1818 |
| `higgs` | 1.314 | 0.8896 | 0.8447 | 6/7 | 0.4 |
| `jannis` | 1.366 | 0.8995 | 0.848 | 5/7 | 0.5 |
| `jasmine` | 0.932 | 0.8831 | 0.6733 | 6/7 | 0.25 |
| `jungle_chess_2pcs_raw_endgame_complete` | 0.9472 | 0.9177 | 0.8447 | 2/7 | 0.5714 |
| `kc1` | 0.9861 | 0.9076 | 0.6832 | 0/7 | 0.3333 |
| `kr-vs-kp` | 0.9602 | 0.9072 | 0.6865 | 4/7 | 0.3333 |
| `mfeat-factors` | 0.8691 | 0.8628 | 0.7071 | 5/7 | 0.3 |
| `nomao` | 0.8467 | 0.9078 | 0.8061 | 4/7 | 0.5714 |
| `numerai28.6` | 1.237 | 0.8885 | 0.8505 | 6/7 | 0.5 |
| `phoneme` | 0.9659 | 0.9175 | 0.7115 | 2/7 | 0.3333 |
| `segment` | 0.9816 | 0.9079 | 0.6879 | 4/7 | 0.5556 |
| `shuttle` | 1.064 | 0.9104 | 0.8485 | 5/7 | 1 |
| `sylvine` | 0.9568 | 0.912 | 0.7072 | 5/7 | 0.5 |
| `vehicle` | 1.002 | 0.9042 | 0.6696 | 6/7 | 0.5556 |
| `volkert` | 1.018 | 0.8959 | 0.8614 | 4/7 | 0.6667 |

## H5a-style context sensitivity

p-value: `4.489e-71`; ratio spread: `0.3423`; verdict: `supports`.
