# x264_size_15 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.1865).

Best integrated confidence after normalizing the prior baseline by empirical cost: `twise_t1` (omega_cost 0.01796, %cost 0.01202).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9281, risk 0.04818, %cost 0.0102, omega_cost 0.0008793
- `henard_t1`: posterior area 0.8959, risk 0.09896, %cost 0.00911, omega_cost -0.02411
- `twise_t1`: posterior area 0.9549, risk 0.04514, %cost 0.01202, omega_cost 0.01796
- `random_t2`: posterior area 0.9853, risk 0.008681, %cost 0.05635, omega_cost 0.0002653
- `SRSSampling_t2`: posterior area 0.9943, risk 0.001736, %cost 0.05951, omega_cost 0.008496
- `random_t3`: posterior area 0.9963, risk 0.003472, %cost 0.1839, omega_cost 0.0009432
- `SRSSampling_t3`: posterior area 0.9989, risk 0, %cost 0.1865, omega_cost 0.003501

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_15:t1` | `supports` | 348.6 | 3.13e-72 | large (0.4943) | median risks: random=0.04818, solverBased=0.204, henard=0.09896, distBased=0.1476, divDistBased=0.0625, twise=0.04514, SRSSampling=0.05903; spread=0.1589 |
| `FSE1` | `x264_size_15:t2` | `supports` | 475.1 | 1.96e-99 | large (0.6769) | median risks: random=0.008681, solverBased=0.1597, henard=0.09896, distBased=0.03993, divDistBased=0.03385, twise=0.02604, SRSSampling=0.001736; spread=0.158 |
| `FSE1` | `x264_size_15:t3` | `supports` | 513.1 | 1.26e-107 | moderate (0.7317) | median risks: random=0.003472, solverBased=0.03819, henard=0.01736, distBased=0.001736, divDistBased=0.009549, twise=0.01389, SRSSampling=0; spread=0.03819 |
| `FSE2` | `x264_size_15:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t1; best cost-normalized=twise_t1 |
| `FSE3` | `x264_size_15:t1` | `refutes` | 0 |  | large (0.02603) | best cost-normalized=twise_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_15:t1` | `supports` | 0.3333 |  | large frontier change (2) | count front=twise_t1; empirical front=henard_t1,random_t1,twise_t1 |
| `FSE5` | `x264_size_15:t1` | `refutes` | 4580 | 0.598 | negligible (0.5421) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05903, median random=0.04818 |
| `FSE6` | `x264_size_15:t1` | `inconclusive` | 4214 | 0.155 | small (0.5786) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01055, median random=0.0102 |
| `FSE2` | `x264_size_15:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_size_15:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_15:t2` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,henard_t2,random_t2 |
| `FSE5` | `x264_size_15:t2` | `supports` | 2622 | 8.08e-08 | large (0.2621) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001736, median random=0.008681 |
| `FSE6` | `x264_size_15:t2` | `supports` | 1824 | 3.87e-13 | large (0.8176) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05951, median random=0.05635 |
| `FSE2` | `x264_size_15:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_size_15:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_15:t3` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,henard_t3,random_t3 |
| `FSE5` | `x264_size_15:t3` | `supports` | 2401 | 1.20e-10 | large (0.2401) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.003472 |
| `FSE6` | `x264_size_15:t3` | `supports` | 2967 | 7.92e-06 | medium (0.7033) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1865, median random=0.1839 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.0102 | 0.04818 | 0.9281 | -0.0004291 | 0.0008793 |
| `solverBased_t1` | 12 | 0.01042 | 0.01043 | 0.204 | 0.7764 | -0.1521 | -0.1522 |
| `henard_t1` | 12 | 0.01042 | 0.00911 | 0.09896 | 0.8959 | -0.03272 | -0.02411 |
| `distBased_t1` | 12 | 0.01042 | 0.009828 | 0.1476 | 0.8463 | -0.08229 | -0.07865 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01026 | 0.0625 | 0.9146 | -0.01394 | -0.01304 |
| `twise_t1` | 12 | 0.01042 | 0.01202 | 0.04514 | 0.9549 | 0.02629 | 0.01796 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01055 | 0.05903 | 0.9213 | -0.007278 | -0.008072 |
| `random_t2` | 65 | 0.05642 | 0.05635 | 0.008681 | 0.9853 | 0.0002466 | 0.0002653 |
| `solverBased_t2` | 65 | 0.05642 | 0.05606 | 0.1597 | 0.834 | -0.1511 | -0.151 |
| `henard_t2` | 65 | 0.05642 | 0.04232 | 0.09896 | 0.9132 | -0.07183 | -0.06705 |
| `distBased_t2` | 65 | 0.05642 | 0.05824 | 0.03993 | 0.9474 | -0.03771 | -0.03817 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05853 | 0.03385 | 0.9694 | -0.01567 | -0.0162 |
| `twise_t2` | 65 | 0.05642 | 0.06286 | 0.02604 | 0.974 | -0.01112 | -0.0126 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.05951 | 0.001736 | 0.9943 | 0.009248 | 0.008496 |
| `random_t3` | 212 | 0.184 | 0.1839 | 0.003472 | 0.9963 | 0.0009403 | 0.0009432 |
| `solverBased_t3` | 212 | 0.184 | 0.1841 | 0.03819 | 0.9426 | -0.05274 | -0.05274 |
| `henard_t3` | 212 | 0.184 | 0.1353 | 0.01736 | 0.9829 | -0.01246 | -0.0108 |
| `distBased_t3` | 212 | 0.184 | 0.1929 | 0.001736 | 0.994 | -0.001291 | -0.001503 |
| `divDistBased_t3` | 212 | 0.184 | 0.1849 | 0.009549 | 0.9911 | -0.004181 | -0.004203 |
| `twise_t3` | 212 | 0.184 | 0.1988 | 0.01389 | 0.9861 | -0.009216 | -0.00956 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1865 | 0 | 0.9989 | 0.003562 | 0.003501 |
