# x264_size_6 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.1868).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t2` (omega_cost 0.007349, %cost 0.0583).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9188, risk 0.04601, %cost 0.0102, omega_cost -0.008542
- `henard_t1`: posterior area 0.9099, risk 0.09028, %cost 0.008892, omega_cost -0.008425
- `SRSSampling_t1`: posterior area 0.9215, risk 0.05165, %cost 0.01057, omega_cost -0.00796
- `random_t2`: posterior area 0.9872, risk 0.01172, %cost 0.05641, omega_cost 0.0021
- `solverBased_t2`: posterior area 0.9545, risk 0.04167, %cost 0.05433, omega_cost -0.03006
- `SRSSampling_t2`: posterior area 0.9929, risk 0.002604, %cost 0.0583, omega_cost 0.007349
- `random_t3`: posterior area 0.9957, risk 0.003472, %cost 0.1839, omega_cost 0.0003458
- `SRSSampling_t3`: posterior area 0.9988, risk 0, %cost 0.1868, omega_cost 0.003372

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_6:t1` | `supports` | 247.6 | 1.34e-50 | large (0.3486) | median risks: random=0.04601, solverBased=0.09983, henard=0.09028, distBased=0.1762, divDistBased=0.07639, twise=0.0842, SRSSampling=0.05165; spread=0.1302 |
| `FSE1` | `x264_size_6:t2` | `supports` | 523.2 | 8.48e-110 | large (0.7463) | median risks: random=0.01172, solverBased=0.04167, henard=0.08594, distBased=0.07639, divDistBased=0.04601, twise=0.01562, SRSSampling=0.002604; spread=0.08333 |
| `FSE1` | `x264_size_6:t3` | `supports` | 422.6 | 3.91e-88 | moderate (0.6011) | median risks: random=0.003472, solverBased=0.01389, henard=0.03472, distBased=0.0217, divDistBased=0.003038, twise=0.002604, SRSSampling=0; spread=0.03472 |
| `FSE2` | `x264_size_6:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t1; best cost-normalized=SRSSampling_t1 |
| `FSE3` | `x264_size_6:t1` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_6:t1` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t1; empirical front=SRSSampling_t1,henard_t1,random_t1 |
| `FSE5` | `x264_size_6:t1` | `refutes` | 4808 | 0.975 | negligible (0.5192) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05165, median random=0.04601 |
| `FSE6` | `x264_size_6:t1` | `inconclusive` | 4261 | 0.192 | small (0.5739) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01057, median random=0.0102 |
| `FSE2` | `x264_size_6:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_size_6:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_6:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,henard_t2,random_t2,solverBased_t2 |
| `FSE5` | `x264_size_6:t2` | `supports` | 2690 | 2.50e-07 | large (0.269) | A12<0.5 means SRS risks tend to be lower; median SRS=0.002604, median random=0.01172 |
| `FSE6` | `x264_size_6:t2` | `supports` | 2966 | 7.83e-06 | medium (0.7034) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0583, median random=0.05641 |
| `FSE2` | `x264_size_6:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_size_6:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_6:t3` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,henard_t3,random_t3,solverBased_t3 |
| `FSE5` | `x264_size_6:t3` | `supports` | 2188 | 3.08e-11 | large (0.2188) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.003472 |
| `FSE6` | `x264_size_6:t3` | `supports` | 3254 | 1.66e-04 | medium (0.6746) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1868, median random=0.1839 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.0102 | 0.04601 | 0.9188 | -0.009813 | -0.008542 |
| `solverBased_t1` | 12 | 0.01042 | 0.01007 | 0.09983 | 0.8427 | -0.08585 | -0.08373 |
| `henard_t1` | 12 | 0.01042 | 0.008892 | 0.09028 | 0.9099 | -0.01868 | -0.008425 |
| `distBased_t1` | 12 | 0.01042 | 0.009648 | 0.1762 | 0.8286 | -0.09996 | -0.09514 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01005 | 0.07639 | 0.8914 | -0.03718 | -0.03493 |
| `twise_t1` | 12 | 0.01042 | 0.01134 | 0.0842 | 0.9158 | -0.01277 | -0.01784 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01057 | 0.05165 | 0.9215 | -0.007096 | -0.00796 |
| `random_t2` | 65 | 0.05642 | 0.05641 | 0.01172 | 0.9872 | 0.002096 | 0.0021 |
| `solverBased_t2` | 65 | 0.05642 | 0.05433 | 0.04167 | 0.9545 | -0.03062 | -0.03006 |
| `henard_t2` | 65 | 0.05642 | 0.04228 | 0.08594 | 0.9173 | -0.06781 | -0.06301 |
| `distBased_t2` | 65 | 0.05642 | 0.05721 | 0.07639 | 0.9202 | -0.06488 | -0.06508 |
| `divDistBased_t2` | 65 | 0.05642 | 0.0583 | 0.04601 | 0.9591 | -0.02593 | -0.0264 |
| `twise_t2` | 65 | 0.05642 | 0.06034 | 0.01562 | 0.9844 | -0.0006996 | -0.001641 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.0583 | 0.002604 | 0.9929 | 0.007816 | 0.007349 |
| `random_t3` | 212 | 0.184 | 0.1839 | 0.003472 | 0.9957 | 0.0003413 | 0.0003458 |
| `solverBased_t3` | 212 | 0.184 | 0.1776 | 0.01389 | 0.9804 | -0.01493 | -0.01476 |
| `henard_t3` | 212 | 0.184 | 0.1348 | 0.03472 | 0.9652 | -0.03009 | -0.02841 |
| `distBased_t3` | 212 | 0.184 | 0.1901 | 0.0217 | 0.9758 | -0.01953 | -0.01968 |
| `divDistBased_t3` | 212 | 0.184 | 0.184 | 0.003038 | 0.9927 | -0.002653 | -0.002652 |
| `twise_t3` | 212 | 0.184 | 0.1935 | 0.002604 | 0.9974 | 0.002069 | 0.001841 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1868 | 0 | 0.9988 | 0.00344 | 0.003372 |
