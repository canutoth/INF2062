# x264_time_12 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t2` (risk 0, %cost 0.06907).

Best integrated confidence after normalizing the prior baseline by empirical cost: `twise_t1` (omega_cost 0.0373, %cost 0.01255).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9227, risk 0.06076, %cost 0.0103, omega_cost -0.005234
- `henard_t1`: posterior area 0.9225, risk 0.05556, %cost 0.009665, omega_cost -0.001391
- `divDistBased_t1`: posterior area 0.9271, risk 0.05208, %cost 0.01049, omega_cost -0.001906
- `twise_t1`: posterior area 0.9766, risk 0.02344, %cost 0.01255, omega_cost 0.0373
- `random_t2`: posterior area 0.9834, risk 0.009549, %cost 0.05653, omega_cost -0.001656
- `divDistBased_t2`: posterior area 0.9907, risk 0.007812, %cost 0.05836, omega_cost 0.005104
- `SRSSampling_t2`: posterior area 0.9987, risk 0, %cost 0.06907, omega_cost 0.01091
- `SRSSampling_t3`: posterior area 0.9997, risk 0, %cost 0.1982, omega_cost 0.00402

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_12:t1` | `supports` | 187.4 | 9.26e-38 | large (0.2617) | median risks: random=0.06076, solverBased=0.2274, henard=0.05556, distBased=0.06944, divDistBased=0.05208, twise=0.02344, SRSSampling=0.0599; spread=0.204 |
| `FSE1` | `x264_time_12:t2` | `supports` | 460.3 | 2.94e-96 | large (0.6556) | median risks: random=0.009549, solverBased=0.1832, henard=0.02344, distBased=0.01389, divDistBased=0.007812, twise=0.01215, SRSSampling=0; spread=0.1832 |
| `FSE1` | `x264_time_12:t3` | `supports` | 381.2 | 3.02e-79 | large (0.5415) | median risks: random=0.002604, solverBased=0.07899, henard=0.02344, distBased=0.001736, divDistBased=0.0008681, twise=0.002604, SRSSampling=0; spread=0.07899 |
| `FSE2` | `x264_time_12:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t1; best cost-normalized=twise_t1 |
| `FSE3` | `x264_time_12:t1` | `refutes` | 0 |  | large (0.0413) | best cost-normalized=twise_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_time_12:t1` | `supports` | 0.25 |  | large frontier change (3) | count front=twise_t1; empirical front=divDistBased_t1,henard_t1,random_t1,twise_t1 |
| `FSE5` | `x264_time_12:t1` | `refutes` | 4771 | 0.952 | negligible (0.4771) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0599, median random=0.06076 |
| `FSE6` | `x264_time_12:t1` | `inconclusive` | 4360 | 0.288 | small (0.5639) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01049, median random=0.0103 |
| `FSE2` | `x264_time_12:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_12:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_12:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,divDistBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_12:t2` | `supports` | 741.5 | 5.73e-24 | large (0.07415) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.009549 |
| `FSE6` | `x264_time_12:t2` | `supports` | 0 | 1.04e-31 | large (1) | A12>0.5 means SRS costs tend to be higher; median SRS=0.06907, median random=0.05653 |
| `FSE2` | `x264_time_12:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_12:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_12:t3` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3,random_t3 |
| `FSE5` | `x264_time_12:t3` | `supports` | 1478 | 2.49e-19 | large (0.1477) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.002604 |
| `FSE6` | `x264_time_12:t3` | `supports` | 4 | 1.17e-31 | large (0.9996) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1982, median random=0.1844 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.0103 | 0.06076 | 0.9227 | -0.005898 | -0.005234 |
| `solverBased_t1` | 12 | 0.01042 | 0.0109 | 0.2274 | 0.8295 | -0.09911 | -0.1019 |
| `henard_t1` | 12 | 0.01042 | 0.009665 | 0.05556 | 0.9225 | -0.006097 | -0.001391 |
| `distBased_t1` | 12 | 0.01042 | 0.01006 | 0.06944 | 0.899 | -0.02957 | -0.0274 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01049 | 0.05208 | 0.9271 | -0.001505 | -0.001906 |
| `twise_t1` | 12 | 0.01042 | 0.01255 | 0.02344 | 0.9766 | 0.04799 | 0.0373 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01049 | 0.0599 | 0.925 | -0.003597 | -0.004 |
| `random_t2` | 65 | 0.05642 | 0.05653 | 0.009549 | 0.9834 | -0.001628 | -0.001656 |
| `solverBased_t2` | 65 | 0.05642 | 0.05731 | 0.1832 | 0.867 | -0.1181 | -0.1183 |
| `henard_t2` | 65 | 0.05642 | 0.04492 | 0.02344 | 0.9542 | -0.03092 | -0.02723 |
| `distBased_t2` | 65 | 0.05642 | 0.0591 | 0.01389 | 0.9879 | 0.002868 | 0.002212 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05836 | 0.007812 | 0.9907 | 0.005585 | 0.005104 |
| `twise_t2` | 65 | 0.05642 | 0.0647 | 0.01215 | 0.9878 | 0.002773 | 0.0009127 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.06907 | 0 | 0.9987 | 0.01358 | 0.01091 |
| `random_t3` | 212 | 0.184 | 0.1844 | 0.002604 | 0.9964 | 0.001114 | 0.001103 |
| `solverBased_t3` | 212 | 0.184 | 0.1883 | 0.07899 | 0.9342 | -0.06113 | -0.06123 |
| `henard_t3` | 212 | 0.184 | 0.144 | 0.02344 | 0.9644 | -0.03091 | -0.02962 |
| `distBased_t3` | 212 | 0.184 | 0.1948 | 0.001736 | 0.997 | 0.001695 | 0.001438 |
| `divDistBased_t3` | 212 | 0.184 | 0.1845 | 0.0008681 | 0.9971 | 0.0018 | 0.001788 |
| `twise_t3` | 212 | 0.184 | 0.2029 | 0.002604 | 0.9974 | 0.002069 | 0.001639 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1982 | 0 | 0.9997 | 0.004352 | 0.00402 |
