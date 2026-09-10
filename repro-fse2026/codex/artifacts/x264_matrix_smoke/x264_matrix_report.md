# x264 2x2 cost-target matrix

## Scope and protocol

This report separates the property used as the cost axis from the property being predicted. For every x264 input `i`, it evaluates four scenarios:

- cost=time, target=time
- cost=time, target=size
- cost=size, target=time
- cost=size, target=size

Here `cost=size` means that the cost objective is the sum of selected configurations' measured output-size values. This is not elapsed acquisition time; it is a second empirical cost metric that can matter if the budget of interest is output footprint rather than measurement duration.

RQ1 and RQ2 are grouped by cost property because they only ask whether the selected configurations have heterogeneous empirical cost and whether `n` is calibrated against that cost. RQ3 and RQ4 are scenario-specific because rankings and Pareto frontiers combine the cost metric with target-specific prediction error.

The learner remains the current lightweight ridge/log-linear model, so this is an infrastructure and positioning result rather than the final modeling claim.

## Overall result

The correction matters. Cost-model validity is primarily a property of the cost axis, while strategy recommendation is a property of the cost-target pair. The same sampling run can be near-calibrated under time cost and differently calibrated under size cost, and the same cost model can produce different rankings depending on whether the target is time or size.

## RQ1: Empirical cost heterogeneity by cost property

### Cost = time

Across 1 inputs, per-configuration cost CV ranges from 0.301 to 0.301 with median 0.301. The p90/p10 cost ratio ranges from 2.212 to 2.212 with median 2.212.

At fixed sample size, median strategy overhead relative to random ranges from 0.7101 to 1.112.

Median cost-over-random by strategy: distBased=0.9929; divDistBased=0.9881; henard=0.7204; random=1; solverBased=1.02; twise=1.063.

### Cost = size

Across 1 inputs, per-configuration cost CV ranges from 0.3097 to 0.3097 with median 0.3097. The p90/p10 cost ratio ranges from 2.21 to 2.21 with median 2.21.

At fixed sample size, median strategy overhead relative to random ranges from 0.7029 to 1.038.

Median cost-over-random by strategy: distBased=0.9604; divDistBased=0.9892; henard=1.024; random=1; solverBased=0.9092; twise=0.7589.

Interpretation: RQ1 should not be tied to the prediction target. It asks whether the chosen cost metric itself is heterogeneous across configurations and sampling strategies. Both time and size show heterogeneity, but the magnitude and strategy bias should be reported separately.

## RQ2: Validity of sample size as cost proxy by cost property

### Cost = time

Spearman rho between `n` and empirical cost ranges from 0.9431 to 0.9431, with median 0.9431. The context-level median calibration ratio `%cost/%n` ranges from 1.005 to 1.005, with median 1.005. The lower quartile can drop to 0.933, and the upper quartile can reach 1.052.

Median calibration ratio by strategy: distBased=0.9926; divDistBased=1.002; henard=0.7189; random=1.001; solverBased=1.096; twise=1.067.

### Cost = size

Spearman rho between `n` and empirical cost ranges from 0.9431 to 0.9431, with median 0.9431. The context-level median calibration ratio `%cost/%n` ranges from 0.9552 to 0.9552, with median 0.9552. The lower quartile can drop to 0.8368, and the upper quartile can reach 1.012.

Median calibration ratio by strategy: distBased=0.9664; divDistBased=0.9928; henard=1.026; random=1.002; solverBased=0.9107; twise=0.7602.

Interpretation: `n` can remain highly correlated with a cost metric while still being miscalibrated for particular strategies. That statement should be made separately for time cost and size cost.

## RQ3: Robustness of conclusions by cost-target scenario

### cost=size, target=size

Across 7 `(input, lambda)` cases, top-1 rankings change 0 times, so top-1 agreement is 1. Mean Kendall tau is 0.8635; the weakest lambda is 10 with tau 0.7386.

Most frequent simple best pairs: random_t2:1.

### cost=size, target=time

Across 7 `(input, lambda)` cases, top-1 rankings change 3 times, so top-1 agreement is 0.5714. Mean Kendall tau is 0.8599; the weakest lambda is 0.5 with tau 0.7516.

Most frequent simple best pairs: twise_t2:1.

### cost=time, target=size

Across 7 `(input, lambda)` cases, top-1 rankings change 0 times, so top-1 agreement is 1. Mean Kendall tau is 0.8971; the weakest lambda is 1 with tau 0.8158.

Most frequent simple best pairs: random_t2:1.

### cost=time, target=time

Across 7 `(input, lambda)` cases, top-1 rankings change 1 times, so top-1 agreement is 0.8571. Mean Kendall tau is 0.9216; the weakest lambda is 10 with tau 0.817.

Most frequent simple best pairs: divDistBased_t2:1.

Interpretation: RQ3 cannot be answered by cost alone. The ranking objective combines prediction error with the selected cost metric, so time-prediction and size-prediction can react differently to the same cost abstraction.

## RQ4: Pareto-efficient sampling by cost-target scenario

### cost=size, target=size

Median count-vs-empirical frontier Jaccard is 0.375 (range 0.375-0.375).

Count frontier concentration:

- `divDistBased_t3`: 1 / 1 contexts
- `random_t2`: 1 / 1 contexts
- `solverBased_t1`: 1 / 1 contexts

Empirical frontier concentration:

- `distBased_t2`: 1 / 1 contexts
- `distBased_t3`: 1 / 1 contexts
- `divDistBased_t2`: 1 / 1 contexts
- `divDistBased_t3`: 1 / 1 contexts
- `random_t2`: 1 / 1 contexts
- `solverBased_t1`: 1 / 1 contexts
- `solverBased_t2`: 1 / 1 contexts
- `twise_t1`: 1 / 1 contexts

### cost=size, target=time

Median count-vs-empirical frontier Jaccard is 0.375 (range 0.375-0.375).

Count frontier concentration:

- `divDistBased_t1`: 1 / 1 contexts
- `divDistBased_t2`: 1 / 1 contexts
- `divDistBased_t3`: 1 / 1 contexts

Empirical frontier concentration:

- `distBased_t1`: 1 / 1 contexts
- `distBased_t3`: 1 / 1 contexts
- `divDistBased_t1`: 1 / 1 contexts
- `divDistBased_t2`: 1 / 1 contexts
- `divDistBased_t3`: 1 / 1 contexts
- `henard_t1`: 1 / 1 contexts
- `twise_t1`: 1 / 1 contexts
- `twise_t2`: 1 / 1 contexts

### cost=time, target=size

Median count-vs-empirical frontier Jaccard is 0.375 (range 0.375-0.375).

Count frontier concentration:

- `divDistBased_t3`: 1 / 1 contexts
- `random_t2`: 1 / 1 contexts
- `solverBased_t1`: 1 / 1 contexts

Empirical frontier concentration:

- `distBased_t1`: 1 / 1 contexts
- `divDistBased_t1`: 1 / 1 contexts
- `divDistBased_t3`: 1 / 1 contexts
- `henard_t1`: 1 / 1 contexts
- `henard_t2`: 1 / 1 contexts
- `random_t1`: 1 / 1 contexts
- `random_t2`: 1 / 1 contexts
- `solverBased_t1`: 1 / 1 contexts

### cost=time, target=time

Median count-vs-empirical frontier Jaccard is 0.4286 (range 0.4286-0.4286).

Count frontier concentration:

- `divDistBased_t1`: 1 / 1 contexts
- `divDistBased_t2`: 1 / 1 contexts
- `divDistBased_t3`: 1 / 1 contexts

Empirical frontier concentration:

- `distBased_t1`: 1 / 1 contexts
- `distBased_t2`: 1 / 1 contexts
- `divDistBased_t1`: 1 / 1 contexts
- `divDistBased_t2`: 1 / 1 contexts
- `divDistBased_t3`: 1 / 1 contexts
- `henard_t1`: 1 / 1 contexts
- `random_t2`: 1 / 1 contexts

## Paper-level takeaway

The clean design is a 2x2 matrix: cost metric on one axis, prediction target on the other. RQ1 and RQ2 characterize the cost axis itself. RQ3 and RQ4 then ask how much the scientific conclusions change when that cost axis is combined with either time or size prediction error. This framing avoids conflating measurement-cost validity with target-prediction performance.
