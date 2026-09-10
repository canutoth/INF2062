# x264_time_16 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.2009).

Best integrated confidence after normalizing the prior baseline by empirical cost: `twise_t1` (omega_cost 0.02337, %cost 0.01161).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9249, risk 0.05382, %cost 0.01019, omega_cost -0.002331
- `henard_t1`: posterior area 0.8898, risk 0.07031, %cost 0.008876, omega_cost -0.02844
- `divDistBased_t1`: posterior area 0.9194, risk 0.05208, %cost 0.01016, omega_cost -0.007665
- `twise_t1`: posterior area 0.9583, risk 0.04167, %cost 0.01161, omega_cost 0.02337
- `SRSSampling_t1`: posterior area 0.932, risk 0.05035, %cost 0.01054, omega_cost 0.002685
- `random_t2`: posterior area 0.9843, risk 0.01302, %cost 0.05647, omega_cost -0.0007637
- `distBased_t2`: posterior area 0.9857, risk 0.01302, %cost 0.05772, omega_cost 0.0002868
- `divDistBased_t2`: posterior area 0.9913, risk 0.00217, %cost 0.05828, omega_cost 0.005731
- `SRSSampling_t2`: posterior area 0.9967, risk 0.0008681, %cost 0.0693, omega_cost 0.008948
- `divDistBased_t3`: posterior area 0.9973, risk 0.0008681, %cost 0.1838, omega_cost 0.001952
- `SRSSampling_t3`: posterior area 0.9989, risk 0, %cost 0.2009, omega_cost 0.003208

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_16:t1` | `supports` | 166.1 | 3.02e-33 | large (0.231) | median risks: random=0.05382, solverBased=0.3212, henard=0.07031, distBased=0.09635, divDistBased=0.05208, twise=0.04167, SRSSampling=0.05035; spread=0.2795 |
| `FSE1` | `x264_time_16:t2` | `supports` | 417.1 | 5.80e-87 | large (0.5933) | median risks: random=0.01302, solverBased=0.2951, henard=0.04167, distBased=0.01302, divDistBased=0.00217, twise=0.01042, SRSSampling=0.0008681; spread=0.2943 |
| `FSE1` | `x264_time_16:t3` | `supports` | 364.9 | 9.90e-76 | large (0.5178) | median risks: random=0.002604, solverBased=0.191, henard=0.04167, distBased=0.002604, divDistBased=0.0008681, twise=0.00434, SRSSampling=0; spread=0.191 |
| `FSE2` | `x264_time_16:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t1; best cost-normalized=twise_t1 |
| `FSE3` | `x264_time_16:t1` | `refutes` | 0 |  | large (0.02069) | best cost-normalized=twise_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_16:t1` | `supports` | 0.2 |  | large frontier change (4) | count front=twise_t1; empirical front=SRSSampling_t1,divDistBased_t1,henard_t1,random_t1,twise_t1 |
| `FSE5` | `x264_time_16:t1` | `refutes` | 4788 | 0.985 | negligible (0.4788) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05035, median random=0.05382 |
| `FSE6` | `x264_time_16:t1` | `inconclusive` | 4165 | 0.124 | small (0.5835) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01054, median random=0.01019 |
| `FSE2` | `x264_time_16:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_16:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_16:t2` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,distBased_t2,divDistBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_16:t2` | `supports` | 1722 | 3.25e-14 | large (0.1721) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0008681, median random=0.01302 |
| `FSE6` | `x264_time_16:t2` | `supports` | 0 | 1.04e-31 | large (1) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0693, median random=0.05647 |
| `FSE2` | `x264_time_16:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_16:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_16:t3` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3 |
| `FSE5` | `x264_time_16:t3` | `supports` | 2350 | 1.99e-10 | large (0.235) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.002604 |
| `FSE6` | `x264_time_16:t3` | `supports` | 33 | 2.69e-31 | large (0.9967) | A12>0.5 means SRS costs tend to be higher; median SRS=0.2009, median random=0.184 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01019 | 0.05382 | 0.9249 | -0.003693 | -0.002331 |
| `solverBased_t1` | 12 | 0.01042 | 0.01042 | 0.3212 | 0.7691 | -0.1595 | -0.1595 |
| `henard_t1` | 12 | 0.01042 | 0.008876 | 0.07031 | 0.8898 | -0.03881 | -0.02844 |
| `distBased_t1` | 12 | 0.01042 | 0.009717 | 0.09635 | 0.8699 | -0.0587 | -0.05434 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01016 | 0.05208 | 0.9194 | -0.009214 | -0.007665 |
| `twise_t1` | 12 | 0.01042 | 0.01161 | 0.04167 | 0.9583 | 0.02976 | 0.02337 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01054 | 0.05035 | 0.932 | 0.003399 | 0.002685 |
| `random_t2` | 65 | 0.05642 | 0.05647 | 0.01302 | 0.9843 | -0.0007517 | -0.0007637 |
| `solverBased_t2` | 65 | 0.05642 | 0.0554 | 0.2951 | 0.7978 | -0.1873 | -0.187 |
| `henard_t2` | 65 | 0.05642 | 0.04282 | 0.04167 | 0.9355 | -0.04959 | -0.04503 |
| `distBased_t2` | 65 | 0.05642 | 0.05772 | 0.01302 | 0.9857 | 0.0006111 | 0.0002868 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05828 | 0.00217 | 0.9913 | 0.006193 | 0.005731 |
| `twise_t2` | 65 | 0.05642 | 0.06127 | 0.01042 | 0.9896 | 0.004509 | 0.00336 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.0693 | 0.0008681 | 0.9967 | 0.01165 | 0.008948 |
| `random_t3` | 212 | 0.184 | 0.184 | 0.002604 | 0.9966 | 0.00127 | 0.001271 |
| `solverBased_t3` | 212 | 0.184 | 0.1824 | 0.191 | 0.869 | -0.1264 | -0.1263 |
| `henard_t3` | 212 | 0.184 | 0.1371 | 0.04167 | 0.9476 | -0.04775 | -0.04617 |
| `distBased_t3` | 212 | 0.184 | 0.1911 | 0.002604 | 0.9968 | 0.001426 | 0.001256 |
| `divDistBased_t3` | 212 | 0.184 | 0.1838 | 0.0008681 | 0.9973 | 0.001947 | 0.001952 |
| `twise_t3` | 212 | 0.184 | 0.1953 | 0.00434 | 0.9957 | 0.0003326 | 6.597e-05 |
| `SRSSampling_t3` | 212 | 0.184 | 0.2009 | 0 | 0.9989 | 0.003597 | 0.003208 |
