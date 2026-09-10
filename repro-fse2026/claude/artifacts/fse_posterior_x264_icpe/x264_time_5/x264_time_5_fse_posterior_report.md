# x264_time_5 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.202).

Best integrated confidence after normalizing the prior baseline by empirical cost: `twise_t1` (omega_cost 0.02144, %cost 0.01261).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9227, risk 0.0612, %cost 0.01022, omega_cost -0.004651
- `henard_t1`: posterior area 0.9219, risk 0.0434, %cost 0.009255, omega_cost 0.000924
- `twise_t1`: posterior area 0.9609, risk 0.03906, %cost 0.01261, omega_cost 0.02144
- `SRSSampling_t1`: posterior area 0.927, risk 0.05339, %cost 0.01056, omega_cost -0.00245
- `random_t2`: posterior area 0.9853, risk 0.01128, %cost 0.05651, omega_cost 0.0001733
- `divDistBased_t2`: posterior area 0.9944, risk 0.002604, %cost 0.05849, omega_cost 0.008841
- `SRSSampling_t2`: posterior area 0.9967, risk 0.0008681, %cost 0.07218, omega_cost 0.008428
- `divDistBased_t3`: posterior area 0.9978, risk 0.0008681, %cost 0.1835, omega_cost 0.002533
- `SRSSampling_t3`: posterior area 0.9996, risk 0, %cost 0.202, omega_cost 0.003818

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_5:t1` | `supports` | 173.8 | 7.03e-35 | large (0.2421) | median risks: random=0.0612, solverBased=0.23, henard=0.0434, distBased=0.1102, divDistBased=0.04948, twise=0.03906, SRSSampling=0.05339; spread=0.191 |
| `FSE1` | `x264_time_5:t2` | `supports` | 464.2 | 4.33e-97 | large (0.6612) | median risks: random=0.01128, solverBased=0.2231, henard=0.03906, distBased=0.008681, divDistBased=0.002604, twise=0.008681, SRSSampling=0.0008681; spread=0.2222 |
| `FSE1` | `x264_time_5:t3` | `supports` | 356.4 | 6.46e-74 | large (0.5057) | median risks: random=0.002604, solverBased=0.1667, henard=0.03906, distBased=0.005208, divDistBased=0.0008681, twise=0.0008681, SRSSampling=0; spread=0.1667 |
| `FSE2` | `x264_time_5:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t1; best cost-normalized=twise_t1 |
| `FSE3` | `x264_time_5:t1` | `refutes` | 0 |  | large (0.02388) | best cost-normalized=twise_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_5:t1` | `supports` | 0.25 |  | large frontier change (3) | count front=twise_t1; empirical front=SRSSampling_t1,henard_t1,random_t1,twise_t1 |
| `FSE5` | `x264_time_5:t1` | `refutes` | 4770 | 0.95 | negligible (0.4769) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05339, median random=0.0612 |
| `FSE6` | `x264_time_5:t1` | `inconclusive` | 4332 | 0.258 | small (0.5668) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01056, median random=0.01022 |
| `FSE2` | `x264_time_5:t2` | `supports` | 1 |  | changed (0.0004128) | best size-normalized=SRSSampling_t2; best cost-normalized=divDistBased_t2 |
| `FSE3` | `x264_time_5:t2` | `refutes` | 0 |  | small (0.0004128) | best cost-normalized=divDistBased_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_5:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,divDistBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_5:t2` | `supports` | 1148 | 1.91e-19 | large (0.1148) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0008681, median random=0.01128 |
| `FSE6` | `x264_time_5:t2` | `supports` | 10 | 1.39e-31 | large (0.999) | A12>0.5 means SRS costs tend to be higher; median SRS=0.07218, median random=0.05651 |
| `FSE2` | `x264_time_5:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_5:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_5:t3` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3 |
| `FSE5` | `x264_time_5:t3` | `supports` | 1330 | 1.59e-19 | large (0.133) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.002604 |
| `FSE6` | `x264_time_5:t3` | `supports` | 16 | 1.65e-31 | large (0.9984) | A12>0.5 means SRS costs tend to be higher; median SRS=0.202, median random=0.1842 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01022 | 0.0612 | 0.9227 | -0.005828 | -0.004651 |
| `solverBased_t1` | 12 | 0.01042 | 0.01097 | 0.23 | 0.8276 | -0.101 | -0.1041 |
| `henard_t1` | 12 | 0.01042 | 0.009255 | 0.0434 | 0.9219 | -0.006627 | 0.000924 |
| `distBased_t1` | 12 | 0.01042 | 0.009851 | 0.1102 | 0.8841 | -0.04447 | -0.04098 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01033 | 0.04948 | 0.9214 | -0.007156 | -0.006616 |
| `twise_t1` | 12 | 0.01042 | 0.01261 | 0.03906 | 0.9609 | 0.03237 | 0.02144 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01056 | 0.05339 | 0.927 | -0.00161 | -0.00245 |
| `random_t2` | 65 | 0.05642 | 0.05651 | 0.01128 | 0.9853 | 0.0001945 | 0.0001733 |
| `solverBased_t2` | 65 | 0.05642 | 0.0565 | 0.2231 | 0.8391 | -0.146 | -0.146 |
| `henard_t2` | 65 | 0.05642 | 0.04311 | 0.03906 | 0.9566 | -0.0285 | -0.02407 |
| `distBased_t2` | 65 | 0.05642 | 0.05852 | 0.008681 | 0.9918 | 0.006714 | 0.006194 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05849 | 0.002604 | 0.9944 | 0.009352 | 0.008841 |
| `twise_t2` | 65 | 0.05642 | 0.06528 | 0.008681 | 0.9913 | 0.006245 | 0.004272 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.07218 | 0.0008681 | 0.9967 | 0.01161 | 0.008428 |
| `random_t3` | 212 | 0.184 | 0.1842 | 0.002604 | 0.9962 | 0.0009055 | 0.0009013 |
| `solverBased_t3` | 212 | 0.184 | 0.1878 | 0.1667 | 0.8885 | -0.1069 | -0.107 |
| `henard_t3` | 212 | 0.184 | 0.1385 | 0.03906 | 0.9661 | -0.02922 | -0.02771 |
| `distBased_t3` | 212 | 0.184 | 0.1944 | 0.005208 | 0.9961 | 0.0007927 | 0.0005461 |
| `divDistBased_t3` | 212 | 0.184 | 0.1835 | 0.0008681 | 0.9978 | 0.00252 | 0.002533 |
| `twise_t3` | 212 | 0.184 | 0.2045 | 0.0008681 | 0.9991 | 0.003805 | 0.003341 |
| `SRSSampling_t3` | 212 | 0.184 | 0.202 | 0 | 0.9996 | 0.00423 | 0.003818 |
