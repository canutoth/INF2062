# x264_time_15 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.2014).

Best integrated confidence after normalizing the prior baseline by empirical cost: `twise_t1` (omega_cost 0.03792, %cost 0.01202).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9226, risk 0.06163, %cost 0.0102, omega_cost -0.004615
- `henard_t1`: posterior area 0.9038, risk 0.05816, %cost 0.00911, omega_cost -0.01621
- `divDistBased_t1`: posterior area 0.9255, risk 0.04253, %cost 0.01026, omega_cost -0.002176
- `twise_t1`: posterior area 0.9748, risk 0.02517, %cost 0.01202, omega_cost 0.03792
- `SRSSampling_t1`: posterior area 0.9271, risk 0.05903, %cost 0.01055, omega_cost -0.002248
- `random_t2`: posterior area 0.9831, risk 0.01215, %cost 0.05635, omega_cost -0.002
- `distBased_t2`: posterior area 0.9906, risk 0.009549, %cost 0.05824, omega_cost 0.005038
- `divDistBased_t2`: posterior area 0.9913, risk 0.008681, %cost 0.05853, omega_cost 0.005741
- `SRSSampling_t2`: posterior area 0.9966, risk 0.0008681, %cost 0.07013, omega_cost 0.008675
- `distBased_t3`: posterior area 0.9981, risk 0.0008681, %cost 0.1929, omega_cost 0.002586
- `divDistBased_t3`: posterior area 0.9976, risk 0.0008681, %cost 0.1849, omega_cost 0.00223
- `SRSSampling_t3`: posterior area 0.9995, risk 0, %cost 0.2014, omega_cost 0.003787

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_15:t1` | `supports` | 192.1 | 8.99e-39 | large (0.2686) | median risks: random=0.06163, solverBased=0.2899, henard=0.05816, distBased=0.07118, divDistBased=0.04253, twise=0.02517, SRSSampling=0.05903; spread=0.2648 |
| `FSE1` | `x264_time_15:t2` | `supports` | 433.5 | 1.72e-90 | large (0.6169) | median risks: random=0.01215, solverBased=0.2804, henard=0.02517, distBased=0.009549, divDistBased=0.008681, twise=0.009549, SRSSampling=0.0008681; spread=0.2795 |
| `FSE1` | `x264_time_15:t3` | `supports` | 420.8 | 9.34e-88 | large (0.5986) | median risks: random=0.003472, solverBased=0.1944, henard=0.02517, distBased=0.0008681, divDistBased=0.0008681, twise=0.006944, SRSSampling=0; spread=0.1944 |
| `FSE2` | `x264_time_15:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t1; best cost-normalized=twise_t1 |
| `FSE3` | `x264_time_15:t1` | `refutes` | 0 |  | large (0.04017) | best cost-normalized=twise_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_15:t1` | `supports` | 0.2 |  | large frontier change (4) | count front=twise_t1; empirical front=SRSSampling_t1,divDistBased_t1,henard_t1,random_t1,twise_t1 |
| `FSE5` | `x264_time_15:t1` | `refutes` | 4706 | 0.826 | negligible (0.4706) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05903, median random=0.06163 |
| `FSE6` | `x264_time_15:t1` | `inconclusive` | 4214 | 0.155 | small (0.5786) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01055, median random=0.0102 |
| `FSE2` | `x264_time_15:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_15:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_15:t2` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,distBased_t2,divDistBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_15:t2` | `supports` | 1517 | 6.94e-16 | large (0.1517) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0008681, median random=0.01215 |
| `FSE6` | `x264_time_15:t2` | `supports` | 13 | 1.52e-31 | large (0.9987) | A12>0.5 means SRS costs tend to be higher; median SRS=0.07013, median random=0.05635 |
| `FSE2` | `x264_time_15:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_15:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_15:t3` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,distBased_t3,divDistBased_t3,henard_t3,random_t3 |
| `FSE5` | `x264_time_15:t3` | `supports` | 1333 | 2.31e-19 | large (0.1333) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.003472 |
| `FSE6` | `x264_time_15:t3` | `supports` | 41 | 3.39e-31 | large (0.9959) | A12>0.5 means SRS costs tend to be higher; median SRS=0.2014, median random=0.1839 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.0102 | 0.06163 | 0.9226 | -0.005924 | -0.004615 |
| `solverBased_t1` | 12 | 0.01042 | 0.01043 | 0.2899 | 0.7896 | -0.139 | -0.1391 |
| `henard_t1` | 12 | 0.01042 | 0.00911 | 0.05816 | 0.9038 | -0.02482 | -0.01621 |
| `distBased_t1` | 12 | 0.01042 | 0.009828 | 0.07118 | 0.882 | -0.04658 | -0.04295 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01026 | 0.04253 | 0.9255 | -0.003085 | -0.002176 |
| `twise_t1` | 12 | 0.01042 | 0.01202 | 0.02517 | 0.9748 | 0.04625 | 0.03792 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01055 | 0.05903 | 0.9271 | -0.001453 | -0.002248 |
| `random_t2` | 65 | 0.05642 | 0.05635 | 0.01215 | 0.9831 | -0.002019 | -0.002 |
| `solverBased_t2` | 65 | 0.05642 | 0.05606 | 0.2804 | 0.8033 | -0.1818 | -0.1817 |
| `henard_t2` | 65 | 0.05642 | 0.04232 | 0.02517 | 0.9479 | -0.03716 | -0.03238 |
| `distBased_t2` | 65 | 0.05642 | 0.05824 | 0.009549 | 0.9906 | 0.00549 | 0.005038 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05853 | 0.008681 | 0.9913 | 0.006262 | 0.005741 |
| `twise_t2` | 65 | 0.05642 | 0.06286 | 0.009549 | 0.9905 | 0.005377 | 0.003889 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.07013 | 0.0008681 | 0.9966 | 0.01152 | 0.008675 |
| `random_t3` | 212 | 0.184 | 0.1839 | 0.003472 | 0.996 | 0.0006625 | 0.0006654 |
| `solverBased_t3` | 212 | 0.184 | 0.1841 | 0.1944 | 0.8658 | -0.1295 | -0.1295 |
| `henard_t3` | 212 | 0.184 | 0.1353 | 0.02517 | 0.9626 | -0.03277 | -0.0311 |
| `distBased_t3` | 212 | 0.184 | 0.1929 | 0.0008681 | 0.9981 | 0.002798 | 0.002586 |
| `divDistBased_t3` | 212 | 0.184 | 0.1849 | 0.0008681 | 0.9976 | 0.002251 | 0.00223 |
| `twise_t3` | 212 | 0.184 | 0.1988 | 0.006944 | 0.9931 | -0.002272 | -0.002616 |
| `SRSSampling_t3` | 212 | 0.184 | 0.2014 | 0 | 0.9995 | 0.004187 | 0.003787 |
