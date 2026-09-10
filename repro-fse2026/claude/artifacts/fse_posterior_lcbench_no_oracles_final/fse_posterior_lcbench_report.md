# FSE 2026 posterior-risk revisit on LCBench

## Scope

This applies the FSE posterior-risk/posterior-confidence framework to LCBench measured pools.
Each OpenML dataset is a distinct reference universe, and each hyperparameter configuration is a sampled object.
The result is reference-relative posterior risk over the measured LCBench pool, not a configurable-software claim.

Source JSON: `/private/tmp/lcbench/data_2k_lw.json`.
Target column: `final_val_accuracy`. Cost column: `time_total`.
Datasets analyzed: `APSFailure, Amazon_employee_access, Australian, Fashion-MNIST, KDDCup09_appetency, MiniBooNE, adult, airlines, albert, bank-marketing, blood-transfusion-service-center, car, christine, cnae-9, connect-4, covertype, credit-g, dionis, fabert, helena, higgs, jannis, jasmine, jungle_chess_2pcs_raw_endgame_complete, kc1, kr-vs-kp, mfeat-factors, nomao, numerai28.6, phoneme, segment, shuttle, sylvine, vehicle, volkert`.
SRS generated: `True` with `30` seeds per dataset/level.
Diagnostic oracles included: `False`.

## Headline

Strategy posterior-risk distributions differ in 154/210 dataset-level scopes.
SRS is the best empirical-cost-normalized recommendation in 0/210 scopes and appears on the empirical cost/confidence Pareto frontier in 21/210 scopes.
Cost-normalization changes the top recommendation in 120/210 scopes and changes the confidence Pareto frontier in 207/210 scopes.
SRS has lower posterior risk than random in 0/210 scopes; its empirical acquisition cost differs from random in 10/210 scopes.

Best empirical-cost-normalized pairs:

- `diversity_n16`: 19/210
- `balanced_n64`: 17/210
- `diversity_n32`: 14/210
- `balanced_n40`: 14/210
- `pilotCost_n20`: 11/210
- `pairwise_n8`: 11/210
- `diversity_n20`: 11/210
- `pilotCost_n40`: 9/210
- `balanced_n20`: 9/210
- `balanced_n32`: 9/210
- `diversity_n40`: 9/210
- `diversity_n8`: 9/210
- `pilotCost_n32`: 9/210
- `pilotCost_n64`: 9/210
- `pilotCost_n16`: 8/210
- `pilotCost_n8`: 8/210
- `balanced_n8`: 7/210
- `diversity_n64`: 7/210
- `balanced_n16`: 6/210
- `pairwise_n20`: 4/210
- `pairwise_n32`: 3/210
- `pairwise_n40`: 3/210
- `pairwise_n64`: 2/210
- `pairwise_n16`: 2/210

## Dataset-Level Summary

| Dataset | Level | n | Best cost pair | SRS best? | SRS on front? | Jaccard |
|---|---|---:|---|---:|---:|---:|
| `APSFailure` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.3333 |
| `APSFailure` | `n16` | 16 | `pilotCost_n16` | 0 | 0 | 0.25 |
| `APSFailure` | `n20` | 20 | `pilotCost_n20` | 0 | 0 | 0.3333 |
| `APSFailure` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `APSFailure` | `n40` | 40 | `pilotCost_n40` | 0 | 0 | 0.3333 |
| `APSFailure` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.5 |
| `Amazon_employee_access` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.2 |
| `Amazon_employee_access` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.1667 |
| `Amazon_employee_access` | `n20` | 20 | `balanced_n20` | 0 | 0 | 0.1667 |
| `Amazon_employee_access` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.1667 |
| `Amazon_employee_access` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.1667 |
| `Amazon_employee_access` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.3333 |
| `Australian` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.25 |
| `Australian` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.3333 |
| `Australian` | `n20` | 20 | `pairwise_n20` | 0 | 0 | 0.25 |
| `Australian` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.25 |
| `Australian` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.25 |
| `Australian` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.25 |
| `Fashion-MNIST` | `n8` | 8 | `pilotCost_n8` | 0 | 0 | 0.5 |
| `Fashion-MNIST` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `Fashion-MNIST` | `n20` | 20 | `pilotCost_n20` | 0 | 0 | 0.3333 |
| `Fashion-MNIST` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.5 |
| `Fashion-MNIST` | `n40` | 40 | `diversity_n40` | 0 | 0 | 0.25 |
| `Fashion-MNIST` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.25 |
| `KDDCup09_appetency` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.25 |
| `KDDCup09_appetency` | `n16` | 16 | `pairwise_n16` | 0 | 0 | 0.2 |
| `KDDCup09_appetency` | `n20` | 20 | `balanced_n20` | 0 | 0 | 0.25 |
| `KDDCup09_appetency` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.2 |
| `KDDCup09_appetency` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.1667 |
| `KDDCup09_appetency` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.1667 |
| `MiniBooNE` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.25 |
| `MiniBooNE` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.2 |
| `MiniBooNE` | `n20` | 20 | `diversity_n20` | 0 | 1 | 0.25 |
| `MiniBooNE` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.3333 |
| `MiniBooNE` | `n40` | 40 | `diversity_n40` | 0 | 0 | 0.3333 |
| `MiniBooNE` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.3333 |
| `adult` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `adult` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `adult` | `n20` | 20 | `pilotCost_n20` | 0 | 0 | 0.3333 |
| `adult` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.3333 |
| `adult` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.3333 |
| `adult` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `airlines` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `airlines` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `airlines` | `n20` | 20 | `diversity_n20` | 0 | 0 | 0.25 |
| `airlines` | `n32` | 32 | `diversity_n32` | 0 | 1 | 0.2 |
| `airlines` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.3333 |
| `airlines` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.3333 |
| `albert` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.3333 |
| `albert` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `albert` | `n20` | 20 | `diversity_n20` | 0 | 0 | 0.3333 |
| `albert` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `albert` | `n40` | 40 | `diversity_n40` | 0 | 0 | 0.3333 |
| `albert` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.3333 |
| `bank-marketing` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `bank-marketing` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.3333 |
| `bank-marketing` | `n20` | 20 | `balanced_n20` | 0 | 0 | 0.25 |
| `bank-marketing` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.3333 |
| `bank-marketing` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.3333 |
| `bank-marketing` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.25 |
| `blood-transfusion-service-center` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.25 |
| `blood-transfusion-service-center` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.3333 |
| `blood-transfusion-service-center` | `n20` | 20 | `balanced_n20` | 0 | 0 | 0.5 |
| `blood-transfusion-service-center` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.3333 |
| `blood-transfusion-service-center` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.3333 |
| `blood-transfusion-service-center` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.3333 |
| `car` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `car` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.25 |
| `car` | `n20` | 20 | `diversity_n20` | 0 | 0 | 0.25 |
| `car` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `car` | `n40` | 40 | `diversity_n40` | 0 | 0 | 0.25 |
| `car` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `christine` | `n8` | 8 | `pilotCost_n8` | 0 | 0 | 0.5 |
| `christine` | `n16` | 16 | `pilotCost_n16` | 0 | 0 | 0.3333 |
| `christine` | `n20` | 20 | `pilotCost_n20` | 0 | 0 | 0.3333 |
| `christine` | `n32` | 32 | `pilotCost_n32` | 0 | 0 | 0.5 |
| `christine` | `n40` | 40 | `pilotCost_n40` | 0 | 0 | 0.5 |
| `christine` | `n64` | 64 | `pilotCost_n64` | 0 | 0 | 0.3333 |
| `cnae-9` | `n8` | 8 | `pilotCost_n8` | 0 | 0 | 0.5 |
| `cnae-9` | `n16` | 16 | `pilotCost_n16` | 0 | 0 | 0.3333 |
| `cnae-9` | `n20` | 20 | `pilotCost_n20` | 0 | 0 | 0.5 |
| `cnae-9` | `n32` | 32 | `pilotCost_n32` | 0 | 0 | 0.5 |
| `cnae-9` | `n40` | 40 | `pilotCost_n40` | 0 | 1 | 0.25 |
| `cnae-9` | `n64` | 64 | `pilotCost_n64` | 0 | 0 | 0.3333 |
| `connect-4` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.1667 |
| `connect-4` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `connect-4` | `n20` | 20 | `balanced_n20` | 0 | 1 | 0.25 |
| `connect-4` | `n32` | 32 | `diversity_n32` | 0 | 1 | 0.2 |
| `connect-4` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.25 |
| `connect-4` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.3333 |
| `covertype` | `n8` | 8 | `balanced_n8` | 0 | 1 | 0.25 |
| `covertype` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `covertype` | `n20` | 20 | `balanced_n20` | 0 | 0 | 0.25 |
| `covertype` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.3333 |
| `covertype` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.25 |
| `covertype` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.3333 |
| `credit-g` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.3333 |
| `credit-g` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.3333 |
| `credit-g` | `n20` | 20 | `diversity_n20` | 0 | 1 | 0.2 |
| `credit-g` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.25 |
| `credit-g` | `n40` | 40 | `pairwise_n40` | 0 | 0 | 0.3333 |
| `credit-g` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.25 |
| `dionis` | `n8` | 8 | `pilotCost_n8` | 0 | 0 | 0.5 |
| `dionis` | `n16` | 16 | `pilotCost_n16` | 0 | 0 | 0.5 |
| `dionis` | `n20` | 20 | `pilotCost_n20` | 0 | 0 | 0.5 |
| `dionis` | `n32` | 32 | `pilotCost_n32` | 0 | 0 | 0.5 |
| `dionis` | `n40` | 40 | `pilotCost_n40` | 0 | 0 | 0.5 |
| `dionis` | `n64` | 64 | `pilotCost_n64` | 0 | 0 | 0.3333 |
| `fabert` | `n8` | 8 | `pilotCost_n8` | 0 | 0 | 0.3333 |
| `fabert` | `n16` | 16 | `pilotCost_n16` | 0 | 0 | 0.3333 |
| `fabert` | `n20` | 20 | `pilotCost_n20` | 0 | 0 | 0.25 |
| `fabert` | `n32` | 32 | `pilotCost_n32` | 0 | 0 | 0.25 |
| `fabert` | `n40` | 40 | `pilotCost_n40` | 0 | 1 | 0.2 |
| `fabert` | `n64` | 64 | `pilotCost_n64` | 0 | 1 | 0.2 |
| `helena` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.5 |
| `helena` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `helena` | `n20` | 20 | `pilotCost_n20` | 0 | 0 | 0.5 |
| `helena` | `n32` | 32 | `pilotCost_n32` | 0 | 0 | 0.5 |
| `helena` | `n40` | 40 | `pilotCost_n40` | 0 | 0 | 0.5 |
| `helena` | `n64` | 64 | `pilotCost_n64` | 0 | 0 | 0.5 |
| `higgs` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.25 |
| `higgs` | `n16` | 16 | `diversity_n16` | 0 | 1 | 0.25 |
| `higgs` | `n20` | 20 | `pairwise_n20` | 0 | 0 | 0.3333 |
| `higgs` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `higgs` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.3333 |
| `higgs` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.3333 |
| `jannis` | `n8` | 8 | `diversity_n8` | 0 | 1 | 0.2 |
| `jannis` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `jannis` | `n20` | 20 | `diversity_n20` | 0 | 0 | 0.3333 |
| `jannis` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `jannis` | `n40` | 40 | `diversity_n40` | 0 | 0 | 0.25 |
| `jannis` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `jasmine` | `n8` | 8 | `pilotCost_n8` | 0 | 0 | 0.5 |
| `jasmine` | `n16` | 16 | `pilotCost_n16` | 0 | 0 | 0.5 |
| `jasmine` | `n20` | 20 | `pilotCost_n20` | 0 | 0 | 0.5 |
| `jasmine` | `n32` | 32 | `pilotCost_n32` | 0 | 0 | 0.5 |
| `jasmine` | `n40` | 40 | `pilotCost_n40` | 0 | 0 | 1 |
| `jasmine` | `n64` | 64 | `pilotCost_n64` | 0 | 0 | 0.5 |
| `jungle_chess_2pcs_raw_endgame_complete` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `jungle_chess_2pcs_raw_endgame_complete` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.3333 |
| `jungle_chess_2pcs_raw_endgame_complete` | `n20` | 20 | `diversity_n20` | 0 | 0 | 0.3333 |
| `jungle_chess_2pcs_raw_endgame_complete` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `jungle_chess_2pcs_raw_endgame_complete` | `n40` | 40 | `diversity_n40` | 0 | 0 | 0.3333 |
| `jungle_chess_2pcs_raw_endgame_complete` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `kc1` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `kc1` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.3333 |
| `kc1` | `n20` | 20 | `balanced_n20` | 0 | 0 | 0.5 |
| `kc1` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.5 |
| `kc1` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.5 |
| `kc1` | `n64` | 64 | `balanced_n64` | 0 | 1 | 0.3333 |
| `kr-vs-kp` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.25 |
| `kr-vs-kp` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.3333 |
| `kr-vs-kp` | `n20` | 20 | `diversity_n20` | 0 | 0 | 0.25 |
| `kr-vs-kp` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `kr-vs-kp` | `n40` | 40 | `pairwise_n40` | 0 | 0 | 0.25 |
| `kr-vs-kp` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.25 |
| `mfeat-factors` | `n8` | 8 | `pilotCost_n8` | 0 | 0 | 0.25 |
| `mfeat-factors` | `n16` | 16 | `pilotCost_n16` | 0 | 0 | 0.3333 |
| `mfeat-factors` | `n20` | 20 | `pilotCost_n20` | 0 | 0 | 0.25 |
| `mfeat-factors` | `n32` | 32 | `pilotCost_n32` | 0 | 0 | 0.25 |
| `mfeat-factors` | `n40` | 40 | `pilotCost_n40` | 0 | 0 | 0.25 |
| `mfeat-factors` | `n64` | 64 | `pilotCost_n64` | 0 | 0 | 0.3333 |
| `nomao` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `nomao` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `nomao` | `n20` | 20 | `diversity_n20` | 0 | 0 | 0.25 |
| `nomao` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `nomao` | `n40` | 40 | `diversity_n40` | 0 | 0 | 0.3333 |
| `nomao` | `n64` | 64 | `diversity_n64` | 0 | 0 | 0.3333 |
| `numerai28.6` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.5 |
| `numerai28.6` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.5 |
| `numerai28.6` | `n20` | 20 | `pairwise_n20` | 0 | 0 | 0.3333 |
| `numerai28.6` | `n32` | 32 | `pilotCost_n32` | 0 | 0 | 0.3333 |
| `numerai28.6` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.5 |
| `numerai28.6` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.5 |
| `phoneme` | `n8` | 8 | `balanced_n8` | 0 | 0 | 0.25 |
| `phoneme` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `phoneme` | `n20` | 20 | `balanced_n20` | 0 | 0 | 0.25 |
| `phoneme` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `phoneme` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.3333 |
| `phoneme` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.3333 |
| `segment` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.25 |
| `segment` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.25 |
| `segment` | `n20` | 20 | `diversity_n20` | 0 | 0 | 0.3333 |
| `segment` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `segment` | `n40` | 40 | `diversity_n40` | 0 | 0 | 0.25 |
| `segment` | `n64` | 64 | `pilotCost_n64` | 0 | 0 | 0.5 |
| `shuttle` | `n8` | 8 | `pairwise_n8` | 0 | 1 | 0.2 |
| `shuttle` | `n16` | 16 | `pairwise_n16` | 0 | 1 | 0.25 |
| `shuttle` | `n20` | 20 | `pairwise_n20` | 0 | 0 | 0.25 |
| `shuttle` | `n32` | 32 | `pairwise_n32` | 0 | 0 | 0.25 |
| `shuttle` | `n40` | 40 | `pairwise_n40` | 0 | 0 | 0.25 |
| `shuttle` | `n64` | 64 | `pairwise_n64` | 0 | 0 | 0.25 |
| `sylvine` | `n8` | 8 | `pairwise_n8` | 0 | 0 | 0.3333 |
| `sylvine` | `n16` | 16 | `balanced_n16` | 0 | 0 | 0.25 |
| `sylvine` | `n20` | 20 | `balanced_n20` | 0 | 0 | 0.25 |
| `sylvine` | `n32` | 32 | `balanced_n32` | 0 | 0 | 0.3333 |
| `sylvine` | `n40` | 40 | `balanced_n40` | 0 | 0 | 0.3333 |
| `sylvine` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.3333 |
| `vehicle` | `n8` | 8 | `pilotCost_n8` | 0 | 0 | 0.3333 |
| `vehicle` | `n16` | 16 | `pilotCost_n16` | 0 | 0 | 0.25 |
| `vehicle` | `n20` | 20 | `pilotCost_n20` | 0 | 0 | 0.25 |
| `vehicle` | `n32` | 32 | `pilotCost_n32` | 0 | 0 | 0.5 |
| `vehicle` | `n40` | 40 | `pilotCost_n40` | 0 | 0 | 1 |
| `vehicle` | `n64` | 64 | `pilotCost_n64` | 0 | 0 | 1 |
| `volkert` | `n8` | 8 | `diversity_n8` | 0 | 0 | 0.3333 |
| `volkert` | `n16` | 16 | `diversity_n16` | 0 | 0 | 0.3333 |
| `volkert` | `n20` | 20 | `diversity_n20` | 0 | 0 | 0.25 |
| `volkert` | `n32` | 32 | `diversity_n32` | 0 | 0 | 0.25 |
| `volkert` | `n40` | 40 | `diversity_n40` | 0 | 0 | 0.3333 |
| `volkert` | `n64` | 64 | `balanced_n64` | 0 | 0 | 0.3333 |

## Budget Scaling

| Strategy | Risk non-increasing | Posterior area non-decreasing | Omega(size) >= 0 all datasets | Omega(cost) >= 0 all datasets |
|---|---:|---:|---:|---:|
| `random` | 19/35 | 19/35 | 6/35 | 8/35 |
| `balanced` | 21/35 | 18/35 | 24/35 | 29/35 |
| `diversity` | 35/35 | 35/35 | 32/35 | 29/35 |
| `SRSSampling` | 17/35 | 19/35 | 6/35 | 7/35 |
| `pairwise` | 35/35 | 35/35 | 11/35 | 13/35 |
| `pilotCost` | 9/35 | 11/35 | 5/35 | 14/35 |

For SRS, posterior risk is non-increasing in 17/35 datasets and posterior area is non-decreasing in 19/35 datasets.

## Applicability

LCBench is applicable as an external-validation dataset for reference-relative posterior risk. It should not be merged directly with configurable-software systems: the sampled objects are ML hyperparameter configurations, and the contexts are OpenML datasets.

## Output Files

- `posterior_lcbench_dataset_summary.csv`: dataset-level posterior/cost decisions.
- `posterior_lcbench_budget_trends.csv`: budget-scaling trends per strategy.
- `posterior_hypothesis_tests.csv`: per-dataset/level FSE-style tests.
- per-dataset folders with CSVs, reports, and figures.
