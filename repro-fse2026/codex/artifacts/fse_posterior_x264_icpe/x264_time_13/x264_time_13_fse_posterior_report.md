# x264_time_13 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t2` (risk 0, %cost 0.06759).

Best integrated confidence after normalizing the prior baseline by empirical cost: `twise_t1` (omega_cost 0.01743, %cost 0.01253).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9168, risk 0.06684, %cost 0.01037, omega_cost -0.01146
- `henard_t1`: posterior area 0.9036, risk 0.09028, %cost 0.009633, omega_cost -0.02008
- `divDistBased_t1`: posterior area 0.914, risk 0.06163, %cost 0.01035, omega_cost -0.01415
- `twise_t1`: posterior area 0.9566, risk 0.0434, %cost 0.01253, omega_cost 0.01743
- `SRSSampling_t1`: posterior area 0.9244, risk 0.05469, %cost 0.01048, omega_cost -0.004568
- `random_t2`: posterior area 0.9861, risk 0.008681, %cost 0.05634, omega_cost 0.001006
- `divDistBased_t2`: posterior area 0.9932, risk 0.005208, %cost 0.05736, omega_cost 0.007874
- `SRSSampling_t2`: posterior area 0.998, risk 0, %cost 0.06759, omega_cost 0.01055
- `twise_t3`: posterior area 1, risk 0, %cost 0.2017, omega_cost 0.004267
- `SRSSampling_t3`: posterior area 0.9998, risk 0, %cost 0.1972, omega_cost 0.004129

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_13:t1` | `supports` | 164.8 | 5.79e-33 | large (0.2291) | median risks: random=0.06684, solverBased=0.2595, henard=0.09028, distBased=0.07726, divDistBased=0.06163, twise=0.0434, SRSSampling=0.05469; spread=0.2161 |
| `FSE1` | `x264_time_13:t2` | `supports` | 485.4 | 1.18e-101 | large (0.6917) | median risks: random=0.008681, solverBased=0.2352, henard=0.0434, distBased=0.01042, divDistBased=0.005208, twise=0.01042, SRSSampling=0; spread=0.2352 |
| `FSE1` | `x264_time_13:t3` | `supports` | 432.1 | 3.58e-90 | moderate (0.6148) | median risks: random=0.002604, solverBased=0.04167, henard=0.0434, distBased=0.0008681, divDistBased=0.002604, twise=0, SRSSampling=0; spread=0.0434 |
| `FSE2` | `x264_time_13:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t1; best cost-normalized=twise_t1 |
| `FSE3` | `x264_time_13:t1` | `refutes` | 0 |  | large (0.022) | best cost-normalized=twise_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_13:t1` | `supports` | 0.2 |  | large frontier change (4) | count front=twise_t1; empirical front=SRSSampling_t1,divDistBased_t1,henard_t1,random_t1,twise_t1 |
| `FSE5` | `x264_time_13:t1` | `refutes` | 4595 | 0.624 | negligible (0.4595) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05469, median random=0.06684 |
| `FSE6` | `x264_time_13:t1` | `refutes` | 4522 | 0.505 | negligible (0.5477) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01048, median random=0.01037 |
| `FSE2` | `x264_time_13:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_13:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_13:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,divDistBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_13:t2` | `supports` | 874 | 1.34e-22 | large (0.0874) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.008681 |
| `FSE6` | `x264_time_13:t2` | `supports` | 29 | 2.40e-31 | large (0.9971) | A12>0.5 means SRS costs tend to be higher; median SRS=0.06759, median random=0.05634 |
| `FSE2` | `x264_time_13:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t3; best cost-normalized=twise_t3 |
| `FSE3` | `x264_time_13:t3` | `refutes` | 0 |  | small (0.0001373) | best cost-normalized=twise_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_13:t3` | `supports` | 0.2 |  | large frontier change (4) | count front=twise_t3; empirical front=SRSSampling_t3,distBased_t3,divDistBased_t3,henard_t3,twise_t3 |
| `FSE5` | `x264_time_13:t3` | `supports` | 1262 | 4.61e-21 | large (0.1263) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.002604 |
| `FSE6` | `x264_time_13:t3` | `supports` | 24 | 2.08e-31 | large (0.9976) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1972, median random=0.1844 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01037 | 0.06684 | 0.9168 | -0.01176 | -0.01146 |
| `solverBased_t1` | 12 | 0.01042 | 0.01024 | 0.2595 | 0.7943 | -0.1343 | -0.1333 |
| `henard_t1` | 12 | 0.01042 | 0.009633 | 0.09028 | 0.9036 | -0.025 | -0.02008 |
| `distBased_t1` | 12 | 0.01042 | 0.01009 | 0.07726 | 0.8848 | -0.04378 | -0.04178 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01035 | 0.06163 | 0.914 | -0.01454 | -0.01415 |
| `twise_t1` | 12 | 0.01042 | 0.01253 | 0.0434 | 0.9566 | 0.02803 | 0.01743 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01048 | 0.05469 | 0.9244 | -0.004188 | -0.004568 |
| `random_t2` | 65 | 0.05642 | 0.05634 | 0.008681 | 0.9861 | 0.0009844 | 0.001006 |
| `solverBased_t2` | 65 | 0.05642 | 0.05447 | 0.2352 | 0.8151 | -0.1699 | -0.1694 |
| `henard_t2` | 65 | 0.05642 | 0.04569 | 0.0434 | 0.9352 | -0.04992 | -0.04654 |
| `distBased_t2` | 65 | 0.05642 | 0.05911 | 0.01042 | 0.9907 | 0.00562 | 0.004961 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05736 | 0.005208 | 0.9932 | 0.008111 | 0.007874 |
| `twise_t2` | 65 | 0.05642 | 0.06441 | 0.01042 | 0.9896 | 0.004509 | 0.002708 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.06759 | 0 | 0.998 | 0.01295 | 0.01055 |
| `random_t3` | 212 | 0.184 | 0.1844 | 0.002604 | 0.9964 | 0.001062 | 0.001052 |
| `solverBased_t3` | 212 | 0.184 | 0.1848 | 0.04167 | 0.9633 | -0.03199 | -0.03201 |
| `henard_t3` | 212 | 0.184 | 0.1477 | 0.0434 | 0.9448 | -0.0505 | -0.04937 |
| `distBased_t3` | 212 | 0.184 | 0.1936 | 0.0008681 | 0.9977 | 0.002355 | 0.002126 |
| `divDistBased_t3` | 212 | 0.184 | 0.1844 | 0.002604 | 0.9969 | 0.001548 | 0.001539 |
| `twise_t3` | 212 | 0.184 | 0.2017 | 0 | 1 | 0.004673 | 0.004267 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1972 | 0 | 0.9998 | 0.004439 | 0.004129 |
