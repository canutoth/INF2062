# x264_time_14 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t2` (risk 0, %cost 0.08038).

Best integrated confidence after normalizing the prior baseline by empirical cost: `twise_t1` (omega_cost 0.0363, %cost 0.01259).

Empirical cost/confidence Pareto front:

- `henard_t1`: posterior area 0.9268, risk 0.04253, %cost 0.008041, omega_cost 0.01557
- `divDistBased_t1`: posterior area 0.9274, risk 0.04167, %cost 0.01018, omega_cost 0.0001841
- `twise_t1`: posterior area 0.9757, risk 0.02431, %cost 0.01259, omega_cost 0.0363
- `SRSSampling_t1`: posterior area 0.9282, risk 0.04861, %cost 0.01062, omega_cost -0.001562
- `random_t2`: posterior area 0.9837, risk 0.01042, %cost 0.05655, omega_cost -0.001436
- `distBased_t2`: posterior area 0.9928, risk 0.006076, %cost 0.05905, omega_cost 0.007111
- `divDistBased_t2`: posterior area 0.9962, risk 0.0008681, %cost 0.05973, omega_cost 0.01031
- `divDistBased_t3`: posterior area 0.9992, risk 0, %cost 0.1837, omega_cost 0.003926
- `twise_t3`: posterior area 1, risk 0, %cost 0.2051, omega_cost 0.004196

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_14:t1` | `supports` | 202 | 7.24e-41 | large (0.2828) | median risks: random=0.06033, solverBased=0.2144, henard=0.04253, distBased=0.1233, divDistBased=0.04167, twise=0.02431, SRSSampling=0.04861; spread=0.1901 |
| `FSE1` | `x264_time_14:t2` | `supports` | 416.5 | 7.97e-87 | large (0.5923) | median risks: random=0.01042, solverBased=0.2049, henard=0.02431, distBased=0.006076, divDistBased=0.0008681, twise=0.006076, SRSSampling=0; spread=0.2049 |
| `FSE1` | `x264_time_14:t3` | `supports` | 428.7 | 1.88e-89 | large (0.61) | median risks: random=0.001736, solverBased=0.1667, henard=0.02431, distBased=0.006076, divDistBased=0, twise=0, SRSSampling=0; spread=0.1667 |
| `FSE2` | `x264_time_14:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t1; best cost-normalized=twise_t1 |
| `FSE3` | `x264_time_14:t1` | `refutes` | 0 |  | large (0.03786) | best cost-normalized=twise_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_14:t1` | `supports` | 0.25 |  | large frontier change (3) | count front=twise_t1; empirical front=SRSSampling_t1,divDistBased_t1,henard_t1,twise_t1 |
| `FSE5` | `x264_time_14:t1` | `refutes` | 4588 | 0.612 | negligible (0.4588) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04861, median random=0.06033 |
| `FSE6` | `x264_time_14:t1` | `inconclusive` | 4195 | 0.142 | small (0.5805) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01062, median random=0.01014 |
| `FSE2` | `x264_time_14:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=divDistBased_t2; best cost-normalized=divDistBased_t2 |
| `FSE3` | `x264_time_14:t2` | `refutes` | 0 |  | moderate (0.00481) | best cost-normalized=divDistBased_t2; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_time_14:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=divDistBased_t2; empirical front=distBased_t2,divDistBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_14:t2` | `supports` | 1698 | 1.67e-14 | large (0.1698) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.01042 |
| `FSE6` | `x264_time_14:t2` | `supports` | 49 | 4.26e-31 | large (0.9951) | A12>0.5 means SRS costs tend to be higher; median SRS=0.08038, median random=0.05655 |
| `FSE2` | `x264_time_14:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t3; best cost-normalized=twise_t3 |
| `FSE3` | `x264_time_14:t3` | `refutes` | 0 |  | small (0.0006309) | best cost-normalized=twise_t3; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_time_14:t3` | `supports` | 0.3333 |  | large frontier change (2) | count front=twise_t3; empirical front=divDistBased_t3,henard_t3,twise_t3 |
| `FSE5` | `x264_time_14:t3` | `supports` | 1638 | 1.04e-16 | large (0.1638) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.001736 |
| `FSE6` | `x264_time_14:t3` | `supports` | 66 | 6.91e-31 | large (0.9934) | A12>0.5 means SRS costs tend to be higher; median SRS=0.2089, median random=0.1843 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01014 | 0.06033 | 0.9204 | -0.008163 | -0.006498 |
| `solverBased_t1` | 12 | 0.01042 | 0.01158 | 0.2144 | 0.8412 | -0.08736 | -0.09359 |
| `henard_t1` | 12 | 0.01042 | 0.008041 | 0.04253 | 0.9268 | -0.001783 | 0.01557 |
| `distBased_t1` | 12 | 0.01042 | 0.009452 | 0.1233 | 0.8766 | -0.05193 | -0.04577 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01018 | 0.04167 | 0.9274 | -0.001219 | 0.0001841 |
| `twise_t1` | 12 | 0.01042 | 0.01259 | 0.02431 | 0.9757 | 0.04712 | 0.0363 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01062 | 0.04861 | 0.9282 | -0.0004117 | -0.001562 |
| `random_t2` | 65 | 0.05642 | 0.05655 | 0.01042 | 0.9837 | -0.001403 | -0.001436 |
| `solverBased_t2` | 65 | 0.05642 | 0.05751 | 0.2049 | 0.8519 | -0.1332 | -0.1335 |
| `henard_t2` | 65 | 0.05642 | 0.03618 | 0.02431 | 0.9596 | -0.02547 | -0.0175 |
| `distBased_t2` | 65 | 0.05642 | 0.05905 | 0.006076 | 0.9928 | 0.007755 | 0.007111 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05973 | 0.0008681 | 0.9962 | 0.01111 | 0.01031 |
| `twise_t2` | 65 | 0.05642 | 0.06536 | 0.006076 | 0.9939 | 0.008849 | 0.006862 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.08038 | 0 | 0.9949 | 0.009856 | 0.005501 |
| `random_t3` | 212 | 0.184 | 0.1843 | 0.001736 | 0.9966 | 0.001261 | 0.001255 |
| `solverBased_t3` | 212 | 0.184 | 0.1879 | 0.1667 | 0.8873 | -0.1081 | -0.1082 |
| `henard_t3` | 212 | 0.184 | 0.1132 | 0.02431 | 0.9704 | -0.02494 | -0.02206 |
| `distBased_t3` | 212 | 0.184 | 0.1966 | 0.006076 | 0.9953 | -1.46e-05 | -0.0003111 |
| `divDistBased_t3` | 212 | 0.184 | 0.1837 | 0 | 0.9992 | 0.003918 | 0.003926 |
| `twise_t3` | 212 | 0.184 | 0.2051 | 0 | 1 | 0.004673 | 0.004196 |
| `SRSSampling_t3` | 212 | 0.184 | 0.2089 | 0 | 0.9994 | 0.004117 | 0.003565 |
