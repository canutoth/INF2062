# x264_time_11 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `twise_t3` (risk 0, %cost 0.1984).

Best integrated confidence after normalizing the prior baseline by empirical cost: `twise_t1` (omega_cost 0.02009, %cost 0.01194).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9232, risk 0.05946, %cost 0.01024, omega_cost -0.004321
- `henard_t1`: posterior area 0.8999, risk 0.08854, %cost 0.008892, omega_cost -0.0184
- `twise_t1`: posterior area 0.9566, risk 0.0434, %cost 0.01194, omega_cost 0.02009
- `random_t2`: posterior area 0.9856, risk 0.01128, %cost 0.05634, omega_cost 0.0005365
- `distBased_t2`: posterior area 0.9906, risk 0.008681, %cost 0.05844, omega_cost 0.005068
- `divDistBased_t2`: posterior area 0.9919, risk 0.008681, %cost 0.05903, omega_cost 0.006142
- `SRSSampling_t2`: posterior area 0.9954, risk 0.0008681, %cost 0.07181, omega_cost 0.007158
- `random_t3`: posterior area 0.9963, risk 0.001736, %cost 0.1844, omega_cost 0.001001
- `distBased_t3`: posterior area 0.9977, risk 0.001736, %cost 0.1927, omega_cost 0.002138
- `divDistBased_t3`: posterior area 0.9966, risk 0.003472, %cost 0.1846, omega_cost 0.00123
- `twise_t3`: posterior area 1, risk 0, %cost 0.1984, omega_cost 0.004337

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_11:t1` | `supports` | 149.3 | 1.08e-29 | large (0.2068) | median risks: random=0.05946, solverBased=0.1936, henard=0.08854, distBased=0.1042, divDistBased=0.07118, twise=0.0434, SRSSampling=0.05425; spread=0.1502 |
| `FSE1` | `x264_time_11:t2` | `supports` | 370.2 | 7.18e-77 | large (0.5255) | median risks: random=0.01128, solverBased=0.1727, henard=0.0434, distBased=0.008681, divDistBased=0.008681, twise=0.008681, SRSSampling=0.0008681; spread=0.1719 |
| `FSE1` | `x264_time_11:t3` | `supports` | 394.1 | 5.13e-82 | large (0.5601) | median risks: random=0.001736, solverBased=0.1667, henard=0.0434, distBased=0.001736, divDistBased=0.003472, twise=0, SRSSampling=0; spread=0.1667 |
| `FSE2` | `x264_time_11:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t1; best cost-normalized=twise_t1 |
| `FSE3` | `x264_time_11:t1` | `refutes` | 0 |  | large (0.02667) | best cost-normalized=twise_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_time_11:t1` | `supports` | 0.3333 |  | large frontier change (2) | count front=twise_t1; empirical front=henard_t1,random_t1,twise_t1 |
| `FSE5` | `x264_time_11:t1` | `refutes` | 4928 | 0.745 | negligible (0.4929) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05425, median random=0.05946 |
| `FSE6` | `x264_time_11:t1` | `inconclusive` | 4274 | 0.203 | small (0.5726) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01051, median random=0.01024 |
| `FSE2` | `x264_time_11:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_11:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_11:t2` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,distBased_t2,divDistBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_11:t2` | `supports` | 1526 | 7.55e-16 | large (0.1525) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0008681, median random=0.01128 |
| `FSE6` | `x264_time_11:t2` | `supports` | 50 | 4.38e-31 | large (0.995) | A12>0.5 means SRS costs tend to be higher; median SRS=0.07181, median random=0.05634 |
| `FSE2` | `x264_time_11:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t3; best cost-normalized=twise_t3 |
| `FSE3` | `x264_time_11:t3` | `refutes` | 0 |  | small (0.000633) | best cost-normalized=twise_t3; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_time_11:t3` | `supports` | 0.2 |  | large frontier change (4) | count front=twise_t3; empirical front=distBased_t3,divDistBased_t3,henard_t3,random_t3,twise_t3 |
| `FSE5` | `x264_time_11:t3` | `supports` | 1807 | 6.89e-15 | large (0.1807) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.001736 |
| `FSE6` | `x264_time_11:t3` | `supports` | 87 | 1.25e-30 | large (0.9913) | A12>0.5 means SRS costs tend to be higher; median SRS=0.2025, median random=0.1844 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01024 | 0.05946 | 0.9232 | -0.005368 | -0.004321 |
| `solverBased_t1` | 12 | 0.01042 | 0.01121 | 0.1936 | 0.8461 | -0.08247 | -0.08684 |
| `henard_t1` | 12 | 0.01042 | 0.008892 | 0.08854 | 0.8999 | -0.02865 | -0.0184 |
| `distBased_t1` | 12 | 0.01042 | 0.009808 | 0.1042 | 0.8643 | -0.06426 | -0.06049 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01031 | 0.07118 | 0.916 | -0.01261 | -0.01199 |
| `twise_t1` | 12 | 0.01042 | 0.01194 | 0.0434 | 0.9566 | 0.02803 | 0.02009 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01051 | 0.05425 | 0.9225 | -0.006037 | -0.006586 |
| `random_t2` | 65 | 0.05642 | 0.05634 | 0.01128 | 0.9856 | 0.0005157 | 0.0005365 |
| `solverBased_t2` | 65 | 0.05642 | 0.05776 | 0.1727 | 0.8744 | -0.1107 | -0.111 |
| `henard_t2` | 65 | 0.05642 | 0.04234 | 0.0434 | 0.9358 | -0.04927 | -0.0445 |
| `distBased_t2` | 65 | 0.05642 | 0.05844 | 0.008681 | 0.9906 | 0.005568 | 0.005068 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05903 | 0.008681 | 0.9919 | 0.006783 | 0.006142 |
| `twise_t2` | 65 | 0.05642 | 0.06267 | 0.008681 | 0.9913 | 0.006245 | 0.004798 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.07181 | 0.0008681 | 0.9954 | 0.01028 | 0.007158 |
| `random_t3` | 212 | 0.184 | 0.1844 | 0.001736 | 0.9963 | 0.00101 | 0.001001 |
| `solverBased_t3` | 212 | 0.184 | 0.1887 | 0.1667 | 0.8872 | -0.1081 | -0.1082 |
| `henard_t3` | 212 | 0.184 | 0.1352 | 0.0434 | 0.9466 | -0.04872 | -0.04706 |
| `distBased_t3` | 212 | 0.184 | 0.1927 | 0.001736 | 0.9977 | 0.002347 | 0.002138 |
| `divDistBased_t3` | 212 | 0.184 | 0.1846 | 0.003472 | 0.9966 | 0.001244 | 0.00123 |
| `twise_t3` | 212 | 0.184 | 0.1984 | 0 | 1 | 0.004673 | 0.004337 |
| `SRSSampling_t3` | 212 | 0.184 | 0.2025 | 0 | 0.9995 | 0.004126 | 0.003704 |
