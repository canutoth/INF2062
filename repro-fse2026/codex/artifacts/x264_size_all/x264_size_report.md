# x264_size_* with empirical x264_time_* acquisition cost

## Scope and protocol

This batch analyzes the 17 `x264_size_i` contexts. For each input `i`, the target is output size from `x264_size_i`, while empirical training cost is the encoding time of the same configurations from `x264_time_i`. Each context uses 7 lambda values and the available 100 runs for six strategies at `t1`, `t2`, and `t3` sample sizes.

The learner is the current lightweight ridge/log-linear model. The results are good for validating the infrastructure and studying cost-model behavior, but they should later be replicated with the paper's final learner.

## Overall result

Sample size is a strong but incomplete proxy. It ranks broad cost levels well because `t1`, `t2`, and `t3` differ substantially in size, but it misses systematic strategy bias at fixed size. The most important empirical signal is therefore not that `%n` is useless; it is that `%n` is too coarse to explain which strategies are cheap or expensive once `n` is held constant.

## RQ1: Empirical cost heterogeneity

Across the 17 inputs, per-configuration time-cost CV ranges from 0.212 to 0.3898 with median 0.2529. The p90/p10 cost ratio ranges from 1.777 to 2.976 with median 2.007. So individual configurations are not equal-cost measurements.

At fixed sample size, median strategy overhead relative to random ranges from 0.6143 to 1.241 across all contexts, strategies, and levels. This directly violates the count-cost abstraction: two samples with the same `n` can have substantially different acquisition time.

Median cost-over-random by strategy across all inputs and levels:

- `distBased`: 1.014
- `divDistBased`: 1.003
- `henard`: 0.7618
- `random`: 1
- `solverBased`: 0.9998
- `twise`: 1.101

## RQ2: Validity of sample size as cost proxy

Spearman rho between `n` and empirical `TrainCost` is high in every context (range 0.9431-0.9431, median 0.9431). This means sample size is useful for ranking large jumps in effort.

Calibration is much less clean. The context-level median `%cost/%n` ratio ranges from 0.9927 to 1.02; the lower quartile of ratios can drop to 0.9131, and the upper quartile can reach 1.115. A high correlation therefore coexists with biased budgets.

Median calibration ratio by strategy:

- `distBased`: 1.014
- `divDistBased`: 1.004
- `henard`: 0.7529
- `random`: 0.9998
- `solverBased`: 0.9988
- `twise`: 1.102

Interpretation: `random` and `divDistBased` are close to calibrated on median, `distBased` is slightly above size cost, `solverBased` is median-neutral but can have high upper-tail cost in some inputs, `twise` is systematically costlier, and `henard` is systematically cheaper than its sample size suggests. This is exactly the distinction the paper should emphasize: sample size can be correlated with cost without being an unbiased cost model.

## RQ3: Robustness of conclusions to the cost model

Across 119 `(context, lambda)` ranking cases, the top-1 strategy-size pair changes 21 times, so top-1 agreement is 0.8235. The lowest mean Kendall tau occurs at lambda=1 with tau=0.8197.

This suggests that conclusions are often stable when accuracy dominates, but agreement degrades once cost has substantial weight. Put differently: if a paper makes claims under a cost-sensitive objective, replacing `n` by measured time can change the recommended strategy.

## RQ4: Pareto-efficient sampling under empirical cost

Count-frontier overlap with the empirical frontier has median Jaccard 0.375 across inputs. The count frontier is concentrated on:

- `random_t2`: 14 / 17 contexts
- `random_t3`: 13 / 17 contexts
- `solverBased_t1`: 12 / 17 contexts
- `divDistBased_t3`: 4 / 17 contexts
- `random_t1`: 2 / 17 contexts
- `divDistBased_t1`: 2 / 17 contexts
- `henard_t1`: 1 / 17 contexts
- `divDistBased_t2`: 1 / 17 contexts
- `henard_t2`: 1 / 17 contexts
- `twise_t2`: 1 / 17 contexts

The empirical frontier additionally favors cheaper fixed-size points:
- `henard_t1`: 17 / 17 contexts
- `henard_t2`: 17 / 17 contexts
- `random_t2`: 16 / 17 contexts
- `distBased_t1`: 14 / 17 contexts
- `random_t3`: 14 / 17 contexts
- `solverBased_t1`: 13 / 17 contexts
- `divDistBased_t3`: 12 / 17 contexts
- `random_t1`: 10 / 17 contexts
- `divDistBased_t1`: 8 / 17 contexts
- `solverBased_t2`: 7 / 17 contexts
- `henard_t3`: 6 / 17 contexts
- `distBased_t2`: 3 / 17 contexts
- `solverBased_t3`: 2 / 17 contexts
- `divDistBased_t2`: 1 / 17 contexts
- `twise_t2`: 1 / 17 contexts

Interpretation: the empirical frontier is more decision-relevant because it exposes low-time training sets that count-cost Pareto analysis hides. This is particularly visible for cheaper `t1` and `t2` points.

## RQ5: Context sensitivity

The effect is present across all 17 inputs, but its magnitude varies. Cost CV ranges over 0.1778 absolute points, and context-level median calibration ratio spans 0.0274. Rank sensitivity is also context-dependent: some inputs have no top-1 flips, while the maximum is 4 / 7 lambda values.

This supports the paper's intended positioning: cost-model validity is not a universal property of configurable-system sampling. It depends on input/workload, strategy, and the chosen accuracy-cost decision rule.

## Paper-level takeaway

For `x264_size_*`, using `n` alone is empirically defensible as a rough first-order effort axis, but not as a fully calibrated cost model. The strongest claim supported by this PoC is nuanced: count-based effort often preserves broad trends, yet it can hide fixed-size cost bias and alter cost-sensitive recommendations. That is a solid empirical gap for the paper.
