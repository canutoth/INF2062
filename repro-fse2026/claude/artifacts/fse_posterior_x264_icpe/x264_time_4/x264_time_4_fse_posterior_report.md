# x264_time_4 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.1989).

Best integrated confidence after normalizing the prior baseline by empirical cost: `twise_t1` (omega_cost 0.01176, %cost 0.01186).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9285, risk 0.05122, %cost 0.01027, omega_cost 0.0007903
- `henard_t1`: posterior area 0.8903, risk 0.1076, %cost 0.009266, omega_cost -0.03076
- `divDistBased_t1`: posterior area 0.9035, risk 0.07986, %cost 0.01023, omega_cost -0.02391
- `twise_t1`: posterior area 0.9479, risk 0.05208, %cost 0.01186, omega_cost 0.01176
- `SRSSampling_t1`: posterior area 0.9307, risk 0.04948, %cost 0.01055, omega_cost 0.001299
- `random_t2`: posterior area 0.9852, risk 0.01128, %cost 0.0565, omega_cost 0.0001497
- `divDistBased_t2`: posterior area 0.9905, risk 0.001736, %cost 0.05795, omega_cost 0.004996
- `twise_t2`: posterior area 0.9922, risk 0.007812, %cost 0.06219, omega_cost 0.005766
- `SRSSampling_t2`: posterior area 0.9973, risk 0.0008681, %cost 0.06865, omega_cost 0.009607
- `divDistBased_t3`: posterior area 0.9978, risk 0.0008681, %cost 0.1835, omega_cost 0.002455
- `twise_t3`: posterior area 0.9991, risk 0.0008681, %cost 0.1972, omega_cost 0.003495
- `SRSSampling_t3`: posterior area 0.9994, risk 0, %cost 0.1989, omega_cost 0.003763

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_4:t1` | `supports` | 185.2 | 2.72e-37 | large (0.2585) | median risks: random=0.05122, solverBased=0.3151, henard=0.1076, distBased=0.1076, divDistBased=0.07986, twise=0.05208, SRSSampling=0.04948; spread=0.2656 |
| `FSE1` | `x264_time_4:t2` | `supports` | 426 | 7.10e-89 | large (0.6061) | median risks: random=0.01128, solverBased=0.2665, henard=0.05208, distBased=0.0217, divDistBased=0.001736, twise=0.007812, SRSSampling=0.0008681; spread=0.2656 |
| `FSE1` | `x264_time_4:t3` | `supports` | 370.3 | 6.80e-77 | large (0.5257) | median risks: random=0.00217, solverBased=0.171, henard=0.05208, distBased=0.006076, divDistBased=0.0008681, twise=0.0008681, SRSSampling=0; spread=0.171 |
| `FSE2` | `x264_time_4:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t1; best cost-normalized=twise_t1 |
| `FSE3` | `x264_time_4:t1` | `refutes` | 0 |  | large (0.01046) | best cost-normalized=twise_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_4:t1` | `supports` | 0.2 |  | large frontier change (4) | count front=twise_t1; empirical front=SRSSampling_t1,divDistBased_t1,henard_t1,random_t1,twise_t1 |
| `FSE5` | `x264_time_4:t1` | `refutes` | 4822 | 0.949 | negligible (0.4822) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04948, median random=0.05122 |
| `FSE6` | `x264_time_4:t1` | `inconclusive` | 4258 | 0.189 | small (0.5742) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01055, median random=0.01027 |
| `FSE2` | `x264_time_4:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_4:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_4:t2` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,divDistBased_t2,henard_t2,random_t2,twise_t2 |
| `FSE5` | `x264_time_4:t2` | `supports` | 1435 | 9.25e-17 | large (0.1435) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0008681, median random=0.01128 |
| `FSE6` | `x264_time_4:t2` | `supports` | 0 | 1.04e-31 | large (1) | A12>0.5 means SRS costs tend to be higher; median SRS=0.06865, median random=0.0565 |
| `FSE2` | `x264_time_4:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_4:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_4:t3` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3,twise_t3 |
| `FSE5` | `x264_time_4:t3` | `supports` | 1858 | 7.57e-15 | large (0.1857) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.00217 |
| `FSE6` | `x264_time_4:t3` | `supports` | 2 | 1.11e-31 | large (0.9998) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1989, median random=0.1842 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01027 | 0.05122 | 0.9285 | -0.0001079 | 0.0007903 |
| `solverBased_t1` | 12 | 0.01042 | 0.01047 | 0.3151 | 0.7712 | -0.1574 | -0.1577 |
| `henard_t1` | 12 | 0.01042 | 0.009266 | 0.1076 | 0.8903 | -0.03823 | -0.03076 |
| `distBased_t1` | 12 | 0.01042 | 0.009858 | 0.1076 | 0.8547 | -0.07388 | -0.07044 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01023 | 0.07986 | 0.9035 | -0.02505 | -0.02391 |
| `twise_t1` | 12 | 0.01042 | 0.01186 | 0.05208 | 0.9479 | 0.01935 | 0.01176 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01055 | 0.04948 | 0.9307 | 0.00208 | 0.001299 |
| `random_t2` | 65 | 0.05642 | 0.0565 | 0.01128 | 0.9852 | 0.0001684 | 0.0001497 |
| `solverBased_t2` | 65 | 0.05642 | 0.0548 | 0.2665 | 0.819 | -0.1661 | -0.1657 |
| `henard_t2` | 65 | 0.05642 | 0.04383 | 0.05208 | 0.9234 | -0.06172 | -0.05759 |
| `distBased_t2` | 65 | 0.05642 | 0.05756 | 0.0217 | 0.9794 | -0.005708 | -0.005995 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05795 | 0.001736 | 0.9905 | 0.005377 | 0.004996 |
| `twise_t2` | 65 | 0.05642 | 0.06219 | 0.007812 | 0.9922 | 0.007113 | 0.005766 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.06865 | 0.0008681 | 0.9973 | 0.0122 | 0.009607 |
| `random_t3` | 212 | 0.184 | 0.1842 | 0.00217 | 0.9963 | 0.0009576 | 0.0009544 |
| `solverBased_t3` | 212 | 0.184 | 0.1823 | 0.171 | 0.8847 | -0.1107 | -0.1106 |
| `henard_t3` | 212 | 0.184 | 0.1421 | 0.05208 | 0.9317 | -0.06361 | -0.06225 |
| `distBased_t3` | 212 | 0.184 | 0.1903 | 0.006076 | 0.9948 | -0.0004834 | -0.0006357 |
| `divDistBased_t3` | 212 | 0.184 | 0.1835 | 0.0008681 | 0.9978 | 0.002442 | 0.002455 |
| `twise_t3` | 212 | 0.184 | 0.1972 | 0.0008681 | 0.9991 | 0.003805 | 0.003495 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1989 | 0 | 0.9994 | 0.004109 | 0.003763 |
