# x264_time_8 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0.0008681, %cost 0.1978).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t1` (omega_cost 0.009439, %cost 0.01051).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9232, risk 0.05946, %cost 0.01031, omega_cost -0.004757
- `henard_t1`: posterior area 0.7756, risk 0.2352, %cost 0.00859, omega_cost -0.1404
- `distBased_t1`: posterior area 0.8531, risk 0.115, %cost 0.009758, omega_cost -0.0714
- `divDistBased_t1`: posterior area 0.9184, risk 0.03733, %cost 0.01006, omega_cost -0.008039
- `SRSSampling_t1`: posterior area 0.9386, risk 0.0421, %cost 0.01051, omega_cost 0.009439
- `random_t2`: posterior area 0.9856, risk 0.009549, %cost 0.05657, omega_cost 0.0005036
- `distBased_t2`: posterior area 0.9682, risk 0.03212, %cost 0.05655, omega_cost -0.01696
- `divDistBased_t2`: posterior area 0.9861, risk 0.006944, %cost 0.05685, omega_cost 0.0009287
- `SRSSampling_t2`: posterior area 0.9964, risk 0.001736, %cost 0.06749, omega_cost 0.008963
- `SRSSampling_t3`: posterior area 0.9987, risk 0.0008681, %cost 0.1978, omega_cost 0.003091

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_8:t1` | `supports` | 257.2 | 1.21e-52 | large (0.3624) | median risks: random=0.05946, solverBased=0.4757, henard=0.2352, distBased=0.115, divDistBased=0.03733, twise=0.1441, SRSSampling=0.0421; spread=0.4384 |
| `FSE1` | `x264_time_8:t2` | `supports` | 438.2 | 1.70e-91 | large (0.6237) | median risks: random=0.009549, solverBased=0.3446, henard=0.1441, distBased=0.03212, divDistBased=0.006944, twise=0.04514, SRSSampling=0.001736; spread=0.3429 |
| `FSE1` | `x264_time_8:t3` | `supports` | 390 | 3.95e-81 | large (0.5541) | median risks: random=0.003472, solverBased=0.3012, henard=0.1441, distBased=0.007812, divDistBased=0.006076, twise=0.01215, SRSSampling=0.0008681; spread=0.3003 |
| `FSE2` | `x264_time_8:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t1; best cost-normalized=SRSSampling_t1 |
| `FSE3` | `x264_time_8:t1` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_8:t1` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t1; empirical front=SRSSampling_t1,distBased_t1,divDistBased_t1,henard_t1,random_t1 |
| `FSE5` | `x264_time_8:t1` | `inconclusive` | 4389 | 0.321 | small (0.4389) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0421, median random=0.05946 |
| `FSE6` | `x264_time_8:t1` | `inconclusive` | 4237 | 0.172 | small (0.5763) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01051, median random=0.01031 |
| `FSE2` | `x264_time_8:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_8:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_8:t2` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,distBased_t2,divDistBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_8:t2` | `supports` | 2105 | 4.01e-11 | large (0.2105) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001736, median random=0.009549 |
| `FSE6` | `x264_time_8:t2` | `supports` | 0 | 1.04e-31 | large (1) | A12>0.5 means SRS costs tend to be higher; median SRS=0.06749, median random=0.05657 |
| `FSE2` | `x264_time_8:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_8:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_8:t3` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3,random_t3 |
| `FSE5` | `x264_time_8:t3` | `supports` | 2435 | 2.54e-09 | large (0.2435) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0008681, median random=0.003472 |
| `FSE6` | `x264_time_8:t3` | `supports` | 16 | 1.65e-31 | large (0.9984) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1978, median random=0.1841 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01031 | 0.05946 | 0.9232 | -0.005412 | -0.004757 |
| `solverBased_t1` | 12 | 0.01042 | 0.009471 | 0.4757 | 0.662 | -0.2665 | -0.2605 |
| `henard_t1` | 12 | 0.01042 | 0.00859 | 0.2352 | 0.7756 | -0.153 | -0.1404 |
| `distBased_t1` | 12 | 0.01042 | 0.009758 | 0.115 | 0.8531 | -0.07549 | -0.0714 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01006 | 0.03733 | 0.9184 | -0.0102 | -0.008039 |
| `twise_t1` | 12 | 0.01042 | 0.01074 | 0.1441 | 0.8559 | -0.07267 | -0.07451 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01051 | 0.0421 | 0.9386 | 0.01 | 0.009439 |
| `random_t2` | 65 | 0.05642 | 0.05657 | 0.009549 | 0.9856 | 0.0005417 | 0.0005036 |
| `solverBased_t2` | 65 | 0.05642 | 0.05223 | 0.3446 | 0.765 | -0.2201 | -0.2189 |
| `henard_t2` | 65 | 0.05642 | 0.04241 | 0.1441 | 0.8209 | -0.1642 | -0.1594 |
| `distBased_t2` | 65 | 0.05642 | 0.05655 | 0.03212 | 0.9682 | -0.01692 | -0.01696 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05685 | 0.006944 | 0.9861 | 0.001036 | 0.0009287 |
| `twise_t2` | 65 | 0.05642 | 0.05745 | 0.04514 | 0.9549 | -0.03021 | -0.03047 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.06749 | 0.001736 | 0.9964 | 0.01135 | 0.008963 |
| `random_t3` | 212 | 0.184 | 0.1841 | 0.003472 | 0.996 | 0.0006712 | 0.0006691 |
| `solverBased_t3` | 212 | 0.184 | 0.1757 | 0.3012 | 0.7974 | -0.1979 | -0.1977 |
| `henard_t3` | 212 | 0.184 | 0.139 | 0.1441 | 0.8306 | -0.1647 | -0.1632 |
| `distBased_t3` | 212 | 0.184 | 0.1858 | 0.007812 | 0.9906 | -0.004763 | -0.004808 |
| `divDistBased_t3` | 212 | 0.184 | 0.1822 | 0.006076 | 0.9928 | -0.002549 | -0.002503 |
| `twise_t3` | 212 | 0.184 | 0.1862 | 0.01215 | 0.9878 | -0.00748 | -0.007534 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1978 | 0.0008681 | 0.9987 | 0.003414 | 0.003091 |
