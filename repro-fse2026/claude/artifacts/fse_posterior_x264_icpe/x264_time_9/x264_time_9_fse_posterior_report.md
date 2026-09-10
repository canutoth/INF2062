# x264_time_9 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.2027).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t2` (omega_cost 0.007687, %cost 0.07075).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9242, risk 0.0612, %cost 0.01022, omega_cost -0.003265
- `henard_t1`: posterior area 0.8117, risk 0.1519, %cost 0.008115, omega_cost -0.1002
- `distBased_t1`: posterior area 0.8631, risk 0.1055, %cost 0.00951, omega_cost -0.05968
- `divDistBased_t1`: posterior area 0.9222, risk 0.05382, %cost 0.009978, omega_cost -0.003745
- `SRSSampling_t1`: posterior area 0.937, risk 0.04731, %cost 0.0106, omega_cost 0.007426
- `random_t2`: posterior area 0.9854, risk 0.01042, %cost 0.05652, omega_cost 0.0002828
- `divDistBased_t2`: posterior area 0.9884, risk 0.001736, %cost 0.05783, omega_cost 0.003019
- `SRSSampling_t2`: posterior area 0.9957, risk 0.001736, %cost 0.07075, omega_cost 0.007687
- `random_t3`: posterior area 0.9968, risk 0.002604, %cost 0.184, omega_cost 0.001461
- `divDistBased_t3`: posterior area 0.9963, risk 0.0008681, %cost 0.183, omega_cost 0.00101
- `SRSSampling_t3`: posterior area 0.9991, risk 0, %cost 0.2027, omega_cost 0.003353

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_9:t1` | `supports` | 210.3 | 1.19e-42 | large (0.2949) | median risks: random=0.0612, solverBased=0.4158, henard=0.1519, distBased=0.1055, divDistBased=0.05382, twise=0.1042, SRSSampling=0.04731; spread=0.3685 |
| `FSE1` | `x264_time_9:t2` | `supports` | 413.7 | 3.11e-86 | large (0.5884) | median risks: random=0.01042, solverBased=0.3533, henard=0.1042, distBased=0.01823, divDistBased=0.001736, twise=0.02604, SRSSampling=0.001736; spread=0.3516 |
| `FSE1` | `x264_time_9:t3` | `supports` | 369.3 | 1.10e-76 | large (0.5243) | median risks: random=0.002604, solverBased=0.3342, henard=0.1042, distBased=0.002604, divDistBased=0.0008681, twise=0.00434, SRSSampling=0; spread=0.3342 |
| `FSE2` | `x264_time_9:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t1; best cost-normalized=SRSSampling_t1 |
| `FSE3` | `x264_time_9:t1` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_9:t1` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t1; empirical front=SRSSampling_t1,distBased_t1,divDistBased_t1,henard_t1,random_t1 |
| `FSE5` | `x264_time_9:t1` | `refutes` | 4503 | 0.475 | negligible (0.4503) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04731, median random=0.0612 |
| `FSE6` | `x264_time_9:t1` | `inconclusive` | 4174 | 0.129 | small (0.5826) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0106, median random=0.01022 |
| `FSE2` | `x264_time_9:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_9:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_9:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,divDistBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_9:t2` | `supports` | 2348 | 1.95e-09 | large (0.2348) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001736, median random=0.01042 |
| `FSE6` | `x264_time_9:t2` | `supports` | 0 | 1.04e-31 | large (1) | A12>0.5 means SRS costs tend to be higher; median SRS=0.07075, median random=0.05652 |
| `FSE2` | `x264_time_9:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_9:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_9:t3` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3,random_t3 |
| `FSE5` | `x264_time_9:t3` | `supports` | 2275 | 6.46e-11 | large (0.2275) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.002604 |
| `FSE6` | `x264_time_9:t3` | `supports` | 22 | 1.97e-31 | large (0.9978) | A12>0.5 means SRS costs tend to be higher; median SRS=0.2027, median random=0.184 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01022 | 0.0612 | 0.9242 | -0.004413 | -0.003265 |
| `solverBased_t1` | 12 | 0.01042 | 0.009702 | 0.4158 | 0.6986 | -0.2299 | -0.2255 |
| `henard_t1` | 12 | 0.01042 | 0.008115 | 0.1519 | 0.8117 | -0.1169 | -0.1002 |
| `distBased_t1` | 12 | 0.01042 | 0.00951 | 0.1055 | 0.8631 | -0.06544 | -0.05968 |
| `divDistBased_t1` | 12 | 0.01042 | 0.009978 | 0.05382 | 0.9222 | -0.006419 | -0.003745 |
| `twise_t1` | 12 | 0.01042 | 0.01059 | 0.1042 | 0.8958 | -0.03274 | -0.03372 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.0106 | 0.04731 | 0.937 | 0.00846 | 0.007426 |
| `random_t2` | 65 | 0.05642 | 0.05652 | 0.01042 | 0.9854 | 0.0003073 | 0.0002828 |
| `solverBased_t2` | 65 | 0.05642 | 0.05231 | 0.3533 | 0.7602 | -0.2249 | -0.2238 |
| `henard_t2` | 65 | 0.05642 | 0.04043 | 0.1042 | 0.8657 | -0.1194 | -0.1138 |
| `distBased_t2` | 65 | 0.05642 | 0.05671 | 0.01823 | 0.9733 | -0.01178 | -0.01185 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05783 | 0.001736 | 0.9884 | 0.003372 | 0.003019 |
| `twise_t2` | 65 | 0.05642 | 0.05709 | 0.02604 | 0.974 | -0.01112 | -0.01129 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.07075 | 0.001736 | 0.9957 | 0.01064 | 0.007687 |
| `random_t3` | 212 | 0.184 | 0.184 | 0.002604 | 0.9968 | 0.001461 | 0.001461 |
| `solverBased_t3` | 212 | 0.184 | 0.1729 | 0.3342 | 0.7803 | -0.215 | -0.2148 |
| `henard_t3` | 212 | 0.184 | 0.1302 | 0.1042 | 0.8793 | -0.116 | -0.1141 |
| `distBased_t3` | 212 | 0.184 | 0.1881 | 0.002604 | 0.9955 | 0.000133 | 3.36e-05 |
| `divDistBased_t3` | 212 | 0.184 | 0.183 | 0.0008681 | 0.9963 | 0.0009837 | 0.00101 |
| `twise_t3` | 212 | 0.184 | 0.1859 | 0.00434 | 0.9957 | 0.0003326 | 0.0002871 |
| `SRSSampling_t3` | 212 | 0.184 | 0.2027 | 0 | 0.9991 | 0.003779 | 0.003353 |
