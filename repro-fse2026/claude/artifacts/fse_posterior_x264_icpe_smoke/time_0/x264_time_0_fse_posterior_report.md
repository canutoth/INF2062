# x264_time_0 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t2` (risk 0, %cost 0.07831).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t1` (omega_cost 0.01489, %cost 0.01036).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9255, risk 0.06207, %cost 0.01027, omega_cost -0.002189
- `henard_t1`: posterior area 0.8187, risk 0.1337, %cost 0.00782, omega_cost -0.09046
- `distBased_t1`: posterior area 0.8632, risk 0.1337, %cost 0.009285, omega_cost -0.05803
- `divDistBased_t1`: posterior area 0.9039, risk 0.06163, %cost 0.009982, omega_cost -0.02201
- `SRSSampling_t1`: posterior area 0.9431, risk 0.04427, %cost 0.01036, omega_cost 0.01489
- `random_t2`: posterior area 0.9847, risk 0.01302, %cost 0.05662, omega_cost -0.0003863
- `distBased_t2`: posterior area 0.956, risk 0.0434, %cost 0.05622, omega_cost -0.02898
- `SRSSampling_t2`: posterior area 0.9989, risk 0, %cost 0.07831, omega_cost 0.009716
- `SRSSampling_t3`: posterior area 0.9999, risk 0, %cost 0.2087, omega_cost 0.004038

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_0:t1` | `supports` | 106.1 | 1.36e-20 | large (0.1659) | median risks: random=0.06207, solverBased=0.1597, henard=0.1337, distBased=0.1337, divDistBased=0.06163, twise=0.1189, SRSSampling=0.04427; spread=0.1155 |
| `FSE1` | `x264_time_0:t2` | `supports` | 299 | 1.37e-61 | large (0.4858) | median risks: random=0.01302, solverBased=0.1562, henard=0.1189, distBased=0.0434, divDistBased=0.02257, twise=0.02691, SRSSampling=0; spread=0.1562 |
| `FSE1` | `x264_time_0:t3` | `supports` | 281.6 | 7.17e-58 | large (0.457) | median risks: random=0.003472, solverBased=0.1562, henard=0.1189, distBased=0.01823, divDistBased=0.01389, twise=0.006944, SRSSampling=0; spread=0.1562 |
| `FSE2` | `x264_time_0:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t1; best cost-normalized=SRSSampling_t1 |
| `FSE3` | `x264_time_0:t1` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_0:t1` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t1; empirical front=SRSSampling_t1,distBased_t1,divDistBased_t1,henard_t1,random_t1 |
| `FSE5` | `x264_time_0:t1` | `refutes` | 442.5 | 0.922 | negligible (0.4425) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04427, median random=0.06207 |
| `FSE6` | `x264_time_0:t1` | `refutes` | 452 | 0.999 | negligible (0.548) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01036, median random=0.01027 |
| `FSE2` | `x264_time_0:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_0:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_0:t2` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,distBased_t2,random_t2 |
| `FSE5` | `x264_time_0:t2` | `supports` | 102.5 | 2.72e-04 | large (0.1025) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.01302 |
| `FSE6` | `x264_time_0:t2` | `supports` | 0 | 2.62e-06 | large (1) | A12>0.5 means SRS costs tend to be higher; median SRS=0.07831, median random=0.05662 |
| `FSE2` | `x264_time_0:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_0:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_0:t3` | `refutes` | 1 |  | same frontier (0) | count front=SRSSampling_t3; empirical front=SRSSampling_t3 |
| `FSE5` | `x264_time_0:t3` | `supports` | 122 | 5.03e-04 | large (0.122) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.003472 |
| `FSE6` | `x264_time_0:t3` | `supports` | 0 | 2.62e-06 | large (1) | A12>0.5 means SRS costs tend to be higher; median SRS=0.2087, median random=0.1844 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01027 | 0.06207 | 0.9255 | -0.003085 | -0.002189 |
| `solverBased_t1` | 12 | 0.01042 | 0.01141 | 0.1597 | 0.8711 | -0.0575 | -0.06291 |
| `henard_t1` | 12 | 0.01042 | 0.00782 | 0.1337 | 0.8187 | -0.1099 | -0.09046 |
| `distBased_t1` | 12 | 0.01042 | 0.009285 | 0.1337 | 0.8632 | -0.06537 | -0.05803 |
| `divDistBased_t1` | 12 | 0.01042 | 0.009982 | 0.06163 | 0.9039 | -0.02467 | -0.02201 |
| `twise_t1` | 12 | 0.01042 | 0.01131 | 0.1189 | 0.8811 | -0.0475 | -0.05237 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01036 | 0.04427 | 0.9431 | 0.01457 | 0.01489 |
| `random_t2` | 65 | 0.05642 | 0.05662 | 0.01302 | 0.9847 | -0.000335 | -0.0003863 |
| `solverBased_t2` | 65 | 0.05642 | 0.05778 | 0.1562 | 0.8935 | -0.09153 | -0.09187 |
| `henard_t2` | 65 | 0.05642 | 0.04079 | 0.1189 | 0.8607 | -0.1244 | -0.1189 |
| `distBased_t2` | 65 | 0.05642 | 0.05622 | 0.0434 | 0.956 | -0.02903 | -0.02898 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05845 | 0.02257 | 0.9803 | -0.004806 | -0.005307 |
| `twise_t2` | 65 | 0.05642 | 0.06021 | 0.02691 | 0.9731 | -0.01198 | -0.0129 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.07831 | 0 | 0.9989 | 0.0138 | 0.009716 |
| `random_t3` | 212 | 0.184 | 0.1844 | 0.003472 | 0.9957 | 0.0003326 | 0.0003243 |
| `solverBased_t3` | 212 | 0.184 | 0.1873 | 0.1562 | 0.8953 | -0.1001 | -0.1002 |
| `henard_t3` | 212 | 0.184 | 0.1309 | 0.1189 | 0.8725 | -0.1228 | -0.1209 |
| `distBased_t3` | 212 | 0.184 | 0.1875 | 0.01823 | 0.9858 | -0.009528 | -0.009614 |
| `divDistBased_t3` | 212 | 0.184 | 0.1822 | 0.01389 | 0.9865 | -0.00886 | -0.008813 |
| `twise_t3` | 212 | 0.184 | 0.1932 | 0.006944 | 0.9931 | -0.002272 | -0.002492 |
| `SRSSampling_t3` | 212 | 0.184 | 0.2087 | 0 | 0.9999 | 0.004586 | 0.004038 |
