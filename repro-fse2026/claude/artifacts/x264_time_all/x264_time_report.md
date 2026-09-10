# x264_time_* with empirical x264_time_* acquisition cost

## Scope and protocol

This batch analyzes the 17 `x264_time_i` contexts. For each input `i`, the prediction target is encoding time and the empirical training acquisition cost is the same encoding time measurement. Each context uses 7 lambda values and the available 100 runs for six strategies at `t1`, `t2`, and `t3` sample sizes.

This is the strongest Tier 1 setting for the paper because the target property and measurement cost are the same phenomenon. If count-based effort is misleading here, it is not because we used an unrelated cost proxy.

The learner is the current lightweight ridge/log-linear model. These results validate the infrastructure and expose cost-model behavior; final paper numbers should still be replicated with the chosen literature-aligned learner.

## Overall result

The time-property case strengthens the core argument. Sample size remains highly correlated with empirical measurement cost, but strategy identity creates repeatable fixed-size bias. Because time is both target and cost here, cost-aware conclusions are especially sensitive to whether we use `n` or measured time.

## RQ1: Empirical cost heterogeneity

Across the 17 inputs, per-configuration time-cost CV ranges from 0.212 to 0.3898 with median 0.2529. The p90/p10 cost ratio ranges from 1.777 to 2.976 with median 2.007. Thus, even within the same system and target property, configurations are not equal-cost units.

At fixed sample size, median strategy overhead relative to random ranges from 0.6143 to 1.241 across all contexts, strategies, and levels. The count-cost model assigns these samples identical effort, but the empirical data does not.

Median cost-over-random by strategy across all inputs and levels:

- `distBased`: 1.014
- `divDistBased`: 1.003
- `henard`: 0.7618
- `random`: 1
- `solverBased`: 0.9998
- `twise`: 1.101

Interpretation: `henard` repeatedly selects cheaper configurations, while `twise` repeatedly selects costlier ones. The other strategies are closer to random on median but still vary by input and sample level.

## RQ2: Validity of sample size as cost proxy

Spearman rho between `n` and empirical `TrainCost` is high in every context (range 0.9431-0.9431, median 0.9431). So sample size is a useful coarse ranking signal.

Calibration is the problem. The context-level median `%cost/%n` ratio ranges from 0.9927 to 1.02; the lower quartile can drop to 0.9131, and the upper quartile can reach 1.115. A strategy can therefore look equivalent under `n` while consuming materially less or more measurement time.

Median calibration ratio by strategy:

- `distBased`: 1.014
- `divDistBased`: 1.004
- `henard`: 0.7529
- `random`: 0.9998
- `solverBased`: 0.9988
- `twise`: 1.102

Interpretation: sample size is not wrong as a first-order abstraction, but it is incomplete. The correct paper phrasing is that `n` is usually correlated with cost, yet it is not a calibrated or strategy-neutral cost model.

## RQ3: Robustness of conclusions to the cost model

Across 119 `(context, lambda)` ranking cases, the top-1 strategy-size pair changes 6 times, so top-1 agreement is 0.9496. The lowest mean Kendall tau occurs at lambda=4 with tau=0.8401.

This is stronger evidence than in a pure target/cost-separation scenario: when predicting time, the empirical cost term is also the property being modeled. A count-cost ranking can therefore recommend a sample that is not actually efficient once measurement time is accounted for.

## RQ4: Pareto-efficient sampling under empirical cost

Count-frontier overlap with the empirical frontier has median Jaccard 0.4286 across inputs. The count frontier is concentrated on:

- `random_t3`: 16 / 17 contexts
- `distBased_t1`: 14 / 17 contexts
- `divDistBased_t2`: 13 / 17 contexts
- `divDistBased_t1`: 2 / 17 contexts
- `random_t2`: 2 / 17 contexts
- `distBased_t2`: 2 / 17 contexts
- `divDistBased_t3`: 1 / 17 contexts
- `random_t1`: 1 / 17 contexts

The empirical frontier highlights a different decision set:
- `distBased_t1`: 17 / 17 contexts
- `henard_t1`: 17 / 17 contexts
- `random_t3`: 16 / 17 contexts
- `random_t2`: 15 / 17 contexts
- `divDistBased_t2`: 14 / 17 contexts
- `henard_t2`: 13 / 17 contexts
- `divDistBased_t3`: 12 / 17 contexts
- `distBased_t2`: 11 / 17 contexts
- `divDistBased_t1`: 2 / 17 contexts
- `random_t1`: 1 / 17 contexts

Interpretation: empirical Pareto analysis surfaces cheap, accuracy-competitive fixed-size choices that count-based Pareto analysis can hide. This is exactly why RQ4 is useful: it avoids arguing about one lambda and asks which choices are simply dominated under the measured cost.

## RQ5: Context sensitivity

The effect appears across all 17 inputs, but magnitude varies. Cost CV ranges over 0.1778 absolute points, and context-level median calibration ratio spans 0.0274. Rank sensitivity is also context-dependent: some inputs have no top-1 flips, while the maximum is 1 / 7 lambda values.

This supports a context-sensitive conclusion rather than a universal one: size-based effort is safer in some inputs than others, even for the same configurable system and same target property.

## Paper-level takeaway

For `x264_time_*`, sample size is a strong coarse proxy but not a calibrated empirical-cost model. The central paper claim is well supported: replacing count-based effort with measured training time can expose strategy-specific acquisition bias, change cost-sensitive rankings, and produce different Pareto frontiers.

Most frequent simple best pairs by context-level `MRE + empirical-cost` are:

- `distBased_t1`: 8 / 17 contexts
- `random_t2`: 6 / 17 contexts
- `distBased_t2`: 2 / 17 contexts
- `divDistBased_t2`: 1 / 17 contexts
