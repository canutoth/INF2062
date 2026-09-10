# x264_time_6 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.2023).

Best integrated confidence after normalizing the prior baseline by empirical cost: `twise_t1` (omega_cost 0.02904, %cost 0.01134).

Empirical cost/confidence Pareto front:

- `henard_t1`: posterior area 0.879, risk 0.05295, %cost 0.008892, omega_cost -0.0393
- `divDistBased_t1`: posterior area 0.924, risk 0.03906, %cost 0.01005, omega_cost -0.002334
- `twise_t1`: posterior area 0.9627, risk 0.03733, %cost 0.01134, omega_cost 0.02904
- `SRSSampling_t1`: posterior area 0.9316, risk 0.05339, %cost 0.01057, omega_cost 0.002205
- `random_t2`: posterior area 0.9842, risk 0.01259, %cost 0.05641, omega_cost -0.000895
- `divDistBased_t2`: posterior area 0.9901, risk 0.00217, %cost 0.0583, omega_cost 0.004511
- `SRSSampling_t2`: posterior area 0.9966, risk 0.0008681, %cost 0.07088, omega_cost 0.008533
- `divDistBased_t3`: posterior area 0.997, risk 0.0008681, %cost 0.184, omega_cost 0.001714
- `SRSSampling_t3`: posterior area 0.9994, risk 0, %cost 0.2023, omega_cost 0.003613

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_6:t1` | `supports` | 145.7 | 6.38e-29 | large (0.2015) | median risks: random=0.05903, solverBased=0.362, henard=0.05295, distBased=0.07726, divDistBased=0.03906, twise=0.03733, SRSSampling=0.05339; spread=0.3247 |
| `FSE1` | `x264_time_6:t2` | `supports` | 400 | 2.81e-83 | large (0.5685) | median risks: random=0.01259, solverBased=0.3602, henard=0.03733, distBased=0.02517, divDistBased=0.00217, twise=0.01389, SRSSampling=0.0008681; spread=0.3594 |
| `FSE1` | `x264_time_6:t3` | `supports` | 368.1 | 1.99e-76 | large (0.5225) | median risks: random=0.002604, solverBased=0.2969, henard=0.03733, distBased=0.002604, divDistBased=0.0008681, twise=0.003472, SRSSampling=0; spread=0.2969 |
| `FSE2` | `x264_time_6:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t1; best cost-normalized=twise_t1 |
| `FSE3` | `x264_time_6:t1` | `refutes` | 0 |  | large (0.02683) | best cost-normalized=twise_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_6:t1` | `supports` | 0.25 |  | large frontier change (3) | count front=twise_t1; empirical front=SRSSampling_t1,divDistBased_t1,henard_t1,twise_t1 |
| `FSE5` | `x264_time_6:t1` | `refutes` | 4854 | 0.887 | negligible (0.4854) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05339, median random=0.05903 |
| `FSE6` | `x264_time_6:t1` | `inconclusive` | 4261 | 0.192 | small (0.5739) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01057, median random=0.0102 |
| `FSE2` | `x264_time_6:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_6:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_6:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,divDistBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_6:t2` | `supports` | 1809 | 2.03e-13 | large (0.1809) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0008681, median random=0.01259 |
| `FSE6` | `x264_time_6:t2` | `supports` | 0 | 1.04e-31 | large (1) | A12>0.5 means SRS costs tend to be higher; median SRS=0.07088, median random=0.05641 |
| `FSE2` | `x264_time_6:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_6:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_6:t3` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3,random_t3 |
| `FSE5` | `x264_time_6:t3` | `supports` | 1894 | 2.19e-14 | large (0.1894) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.002604 |
| `FSE6` | `x264_time_6:t3` | `supports` | 84 | 1.15e-30 | large (0.9916) | A12>0.5 means SRS costs tend to be higher; median SRS=0.2023, median random=0.1839 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.0102 | 0.05903 | 0.924 | -0.004596 | -0.003325 |
| `solverBased_t1` | 12 | 0.01042 | 0.01007 | 0.362 | 0.7474 | -0.1811 | -0.179 |
| `henard_t1` | 12 | 0.01042 | 0.008892 | 0.05295 | 0.879 | -0.04955 | -0.0393 |
| `distBased_t1` | 12 | 0.01042 | 0.009648 | 0.07726 | 0.8725 | -0.05611 | -0.05128 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01005 | 0.03906 | 0.924 | -0.004587 | -0.002334 |
| `twise_t1` | 12 | 0.01042 | 0.01134 | 0.03733 | 0.9627 | 0.0341 | 0.02904 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01057 | 0.05339 | 0.9316 | 0.003069 | 0.002205 |
| `random_t2` | 65 | 0.05642 | 0.05641 | 0.01259 | 0.9842 | -0.0008993 | -0.000895 |
| `solverBased_t2` | 65 | 0.05642 | 0.05433 | 0.3602 | 0.7593 | -0.2258 | -0.2253 |
| `henard_t2` | 65 | 0.05642 | 0.04228 | 0.03733 | 0.9359 | -0.04917 | -0.04437 |
| `distBased_t2` | 65 | 0.05642 | 0.05721 | 0.02517 | 0.9806 | -0.004493 | -0.004693 |
| `divDistBased_t2` | 65 | 0.05642 | 0.0583 | 0.00217 | 0.9901 | 0.004977 | 0.004511 |
| `twise_t2` | 65 | 0.05642 | 0.06034 | 0.01389 | 0.9861 | 0.001036 | 9.512e-05 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.07088 | 0.0008681 | 0.9966 | 0.01151 | 0.008533 |
| `random_t3` | 212 | 0.184 | 0.1839 | 0.002604 | 0.9965 | 0.001149 | 0.001153 |
| `solverBased_t3` | 212 | 0.184 | 0.1776 | 0.2969 | 0.8004 | -0.195 | -0.1948 |
| `henard_t3` | 212 | 0.184 | 0.1348 | 0.03733 | 0.9513 | -0.04405 | -0.04237 |
| `distBased_t3` | 212 | 0.184 | 0.1901 | 0.002604 | 0.9965 | 0.001166 | 0.001018 |
| `divDistBased_t3` | 212 | 0.184 | 0.184 | 0.0008681 | 0.997 | 0.001713 | 0.001714 |
| `twise_t3` | 212 | 0.184 | 0.1935 | 0.003472 | 0.9965 | 0.001201 | 0.0009733 |
| `SRSSampling_t3` | 212 | 0.184 | 0.2023 | 0 | 0.9994 | 0.004031 | 0.003613 |
