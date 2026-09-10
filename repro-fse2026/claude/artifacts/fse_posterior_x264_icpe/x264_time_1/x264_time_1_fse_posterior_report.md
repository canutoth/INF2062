# x264_time_1 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t2` (risk 0, %cost 0.07048).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t2` (omega_cost 0.01087, %cost 0.07048).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9242, risk 0.05729, %cost 0.01027, omega_cost -0.003504
- `henard_t1`: posterior area 0.905, risk 0.09288, %cost 0.0092, omega_cost -0.01562
- `twise_t1`: posterior area 0.9479, risk 0.05208, %cost 0.01252, omega_cost 0.00879
- `SRSSampling_t1`: posterior area 0.9302, risk 0.05556, %cost 0.01052, omega_cost 0.001013
- `random_t2`: posterior area 0.9843, risk 0.01128, %cost 0.05664, omega_cost -0.0008681
- `distBased_t2`: posterior area 0.9937, risk 0.006076, %cost 0.05835, omega_cost 0.008102
- `divDistBased_t2`: posterior area 0.9936, risk 0.006076, %cost 0.05806, omega_cost 0.008146
- `twise_t2`: posterior area 0.9939, risk 0.006076, %cost 0.06466, omega_cost 0.006998
- `SRSSampling_t2`: posterior area 0.9989, risk 0, %cost 0.07048, omega_cost 0.01087
- `SRSSampling_t3`: posterior area 0.9997, risk 0, %cost 0.2008, omega_cost 0.004025

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_1:t1` | `supports` | 168.6 | 8.95e-34 | large (0.2346) | median risks: random=0.05729, solverBased=0.2743, henard=0.09288, distBased=0.09549, divDistBased=0.05686, twise=0.05208, SRSSampling=0.05556; spread=0.2222 |
| `FSE1` | `x264_time_1:t2` | `supports` | 502.7 | 2.22e-105 | large (0.7167) | median risks: random=0.01128, solverBased=0.2422, henard=0.05208, distBased=0.006076, divDistBased=0.006076, twise=0.006076, SRSSampling=0; spread=0.2422 |
| `FSE1` | `x264_time_1:t3` | `supports` | 387 | 1.71e-80 | large (0.5498) | median risks: random=0.003472, solverBased=0.07118, henard=0.05208, distBased=0.006076, divDistBased=0, twise=0.003472, SRSSampling=0; spread=0.07118 |
| `FSE2` | `x264_time_1:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t1; best cost-normalized=twise_t1 |
| `FSE3` | `x264_time_1:t1` | `refutes` | 0 |  | moderate (0.007777) | best cost-normalized=twise_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_1:t1` | `supports` | 0.25 |  | large frontier change (3) | count front=twise_t1; empirical front=SRSSampling_t1,henard_t1,random_t1,twise_t1 |
| `FSE5` | `x264_time_1:t1` | `refutes` | 4688 | 0.794 | negligible (0.4688) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05556, median random=0.05729 |
| `FSE6` | `x264_time_1:t1` | `inconclusive` | 4294 | 0.221 | small (0.5706) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01052, median random=0.01027 |
| `FSE2` | `x264_time_1:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_1:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_1:t2` | `supports` | 0.1667 |  | large frontier change (5) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,distBased_t2,divDistBased_t2,henard_t2,random_t2,twise_t2 |
| `FSE5` | `x264_time_1:t2` | `supports` | 542.5 | 7.68e-26 | large (0.05425) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.01128 |
| `FSE6` | `x264_time_1:t2` | `supports` | 0 | 1.04e-31 | large (1) | A12>0.5 means SRS costs tend to be higher; median SRS=0.07048, median random=0.05664 |
| `FSE2` | `x264_time_1:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_1:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_1:t3` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3 |
| `FSE5` | `x264_time_1:t3` | `supports` | 1022 | 4.39e-23 | large (0.1022) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.003472 |
| `FSE6` | `x264_time_1:t3` | `supports` | 9 | 1.35e-31 | large (0.9991) | A12>0.5 means SRS costs tend to be higher; median SRS=0.2008, median random=0.1844 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01027 | 0.05729 | 0.9242 | -0.00437 | -0.003504 |
| `solverBased_t1` | 12 | 0.01042 | 0.01034 | 0.2743 | 0.7918 | -0.1367 | -0.1363 |
| `henard_t1` | 12 | 0.01042 | 0.0092 | 0.09288 | 0.905 | -0.02357 | -0.01562 |
| `distBased_t1` | 12 | 0.01042 | 0.00983 | 0.09549 | 0.8744 | -0.05418 | -0.05056 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01035 | 0.05686 | 0.9192 | -0.009405 | -0.009034 |
| `twise_t1` | 12 | 0.01042 | 0.01252 | 0.05208 | 0.9479 | 0.01935 | 0.00879 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01052 | 0.05556 | 0.9302 | 0.001611 | 0.001013 |
| `random_t2` | 65 | 0.05642 | 0.05664 | 0.01128 | 0.9843 | -0.0008125 | -0.0008681 |
| `solverBased_t2` | 65 | 0.05642 | 0.05507 | 0.2422 | 0.8207 | -0.1644 | -0.164 |
| `henard_t2` | 65 | 0.05642 | 0.04254 | 0.05208 | 0.9358 | -0.04924 | -0.04456 |
| `distBased_t2` | 65 | 0.05642 | 0.05835 | 0.006076 | 0.9937 | 0.00858 | 0.008102 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05806 | 0.006076 | 0.9936 | 0.008554 | 0.008146 |
| `twise_t2` | 65 | 0.05642 | 0.06466 | 0.006076 | 0.9939 | 0.008849 | 0.006998 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.07048 | 0 | 0.9989 | 0.01378 | 0.01087 |
| `random_t3` | 212 | 0.184 | 0.1844 | 0.003472 | 0.9959 | 0.0005323 | 0.0005228 |
| `solverBased_t3` | 212 | 0.184 | 0.1844 | 0.07118 | 0.9355 | -0.05982 | -0.05983 |
| `henard_t3` | 212 | 0.184 | 0.1385 | 0.05208 | 0.9465 | -0.04887 | -0.04735 |
| `distBased_t3` | 212 | 0.184 | 0.194 | 0.006076 | 0.9957 | 0.0003326 | 9.528e-05 |
| `divDistBased_t3` | 212 | 0.184 | 0.1836 | 0 | 0.9982 | 0.002833 | 0.002843 |
| `twise_t3` | 212 | 0.184 | 0.2032 | 0.003472 | 0.9965 | 0.001201 | 0.0007629 |
| `SRSSampling_t3` | 212 | 0.184 | 0.2008 | 0 | 0.9997 | 0.004412 | 0.004025 |
