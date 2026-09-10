# x264_size_11 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `henard_t2` (risk 0, %cost 0.04234).

Best integrated confidence after normalizing the prior baseline by empirical cost: `henard_t2` (omega_cost 0.01969, %cost 0.04234).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9372, risk 0.04688, %cost 0.01024, omega_cost 0.00969
- `henard_t1`: posterior area 0.7794, risk 0.2222, %cost 0.008892, omega_cost -0.1389
- `distBased_t1`: posterior area 0.9228, risk 0.05208, %cost 0.009808, omega_cost -0.002026
- `divDistBased_t1`: posterior area 0.9446, risk 0.05208, %cost 0.01031, omega_cost 0.01664
- `henard_t2`: posterior area 1, risk 0, %cost 0.04234, omega_cost 0.01969

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_11:t1` | `supports` | 469.6 | 2.94e-98 | large (0.669) | median risks: random=0.04688, solverBased=0.1502, henard=0.2222, distBased=0.05208, divDistBased=0.05208, twise=0.3472, SRSSampling=0.07639; spread=0.3003 |
| `FSE1` | `x264_size_11:t2` | `supports` | 614.7 | 1.55e-129 | large (0.8784) | median risks: random=0.01042, solverBased=0.1398, henard=0, distBased=0.05208, divDistBased=0, twise=0.1146, SRSSampling=0; spread=0.1398 |
| `FSE1` | `x264_size_11:t3` | `supports` | 641.7 | 2.40e-135 | large (0.9173) | median risks: random=0, solverBased=0.1319, henard=0, distBased=0, divDistBased=0, twise=0.03125, SRSSampling=0; spread=0.1319 |
| `FSE2` | `x264_size_11:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=divDistBased_t1; best cost-normalized=divDistBased_t1 |
| `FSE3` | `x264_size_11:t1` | `refutes` | 0 |  | large (0.03329) | best cost-normalized=divDistBased_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_11:t1` | `supports` | 0.25 |  | large frontier change (3) | count front=divDistBased_t1; empirical front=distBased_t1,divDistBased_t1,henard_t1,random_t1 |
| `FSE5` | `x264_size_11:t1` | `refutes` | 3888 | 0.0261 | small (0.6112) | A12<0.5 means SRS risks tend to be lower; median SRS=0.07639, median random=0.04688 |
| `FSE6` | `x264_size_11:t1` | `inconclusive` | 4274 | 0.203 | small (0.5726) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01051, median random=0.01024 |
| `FSE2` | `x264_size_11:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t2; best cost-normalized=henard_t2 |
| `FSE3` | `x264_size_11:t2` | `refutes` | 0 |  | moderate (0.003718) | best cost-normalized=henard_t2; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_11:t2` | `refutes` | 1 |  | same frontier (0) | count front=henard_t2; empirical front=henard_t2 |
| `FSE5` | `x264_size_11:t2` | `supports` | 2628 | 7.88e-12 | large (0.2628) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.01042 |
| `FSE6` | `x264_size_11:t2` | `supports` | 379 | 3.80e-27 | large (0.0379) | A12>0.5 means SRS costs tend to be higher; median SRS=0.04886, median random=0.05634 |
| `FSE2` | `x264_size_11:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t3; best cost-normalized=henard_t3 |
| `FSE3` | `x264_size_11:t3` | `refutes` | 0 |  | moderate (0.001493) | best cost-normalized=henard_t3; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_11:t3` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t3,divDistBased_t3,henard_t3; empirical front=henard_t3 |
| `FSE5` | `x264_size_11:t3` | `supports` | 4200 | 2.54e-04 | small (0.42) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `x264_size_11:t3` | `supports` | 540 | 2.54e-25 | large (0.054) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1775, median random=0.1844 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01024 | 0.04688 | 0.9372 | 0.008642 | 0.00969 |
| `solverBased_t1` | 12 | 0.01042 | 0.01121 | 0.1502 | 0.7075 | -0.221 | -0.2254 |
| `henard_t1` | 12 | 0.01042 | 0.008892 | 0.2222 | 0.7794 | -0.1491 | -0.1389 |
| `distBased_t1` | 12 | 0.01042 | 0.009808 | 0.05208 | 0.9228 | -0.005794 | -0.002026 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01031 | 0.05208 | 0.9446 | 0.01602 | 0.01664 |
| `twise_t1` | 12 | 0.01042 | 0.01194 | 0.3472 | 0.6528 | -0.2758 | -0.2837 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01051 | 0.07639 | 0.9125 | -0.0161 | -0.01665 |
| `random_t2` | 65 | 0.05642 | 0.05634 | 0.01042 | 0.9883 | 0.003259 | 0.00328 |
| `solverBased_t2` | 65 | 0.05642 | 0.05776 | 0.1398 | 0.8527 | -0.1323 | -0.1327 |
| `henard_t2` | 65 | 0.05642 | 0.04234 | 0 | 1 | 0.01493 | 0.01969 |
| `distBased_t2` | 65 | 0.05642 | 0.05844 | 0.05208 | 0.9552 | -0.02988 | -0.03038 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05903 | 0 | 0.9968 | 0.0117 | 0.01106 |
| `twise_t2` | 65 | 0.05642 | 0.06267 | 0.1146 | 0.8854 | -0.09966 | -0.1011 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.04886 | 0 | 0.9988 | 0.01374 | 0.01598 |
| `random_t3` | 212 | 0.184 | 0.1844 | 0 | 0.9981 | 0.002798 | 0.002789 |
| `solverBased_t3` | 212 | 0.184 | 0.1887 | 0.1319 | 0.8594 | -0.136 | -0.1361 |
| `henard_t3` | 212 | 0.184 | 0.1352 | 0 | 1 | 0.004673 | 0.006337 |
| `distBased_t3` | 212 | 0.184 | 0.1927 | 0 | 0.9979 | 0.00259 | 0.002381 |
| `divDistBased_t3` | 212 | 0.184 | 0.1846 | 0 | 1 | 0.004673 | 0.004659 |
| `twise_t3` | 212 | 0.184 | 0.1984 | 0.03125 | 0.9688 | -0.02658 | -0.02691 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1775 | 0 | 1 | 0.004673 | 0.004844 |
