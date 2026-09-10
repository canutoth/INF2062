# x264_time_10 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.2007).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t2` (omega_cost 0.009507, %cost 0.06922).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9255, risk 0.05339, %cost 0.01028, omega_cost -0.002294
- `henard_t1`: posterior area 0.8404, risk 0.1484, %cost 0.00886, omega_cost -0.0777
- `distBased_t1`: posterior area 0.8536, risk 0.1128, %cost 0.009743, omega_cost -0.07077
- `divDistBased_t1`: posterior area 0.9073, risk 0.0651, %cost 0.01018, omega_cost -0.01985
- `SRSSampling_t1`: posterior area 0.9329, risk 0.04644, %cost 0.01058, omega_cost 0.00343
- `random_t2`: posterior area 0.9849, risk 0.01172, %cost 0.05652, omega_cost -0.0001608
- `divDistBased_t2`: posterior area 0.9877, risk 0.003472, %cost 0.05789, omega_cost 0.002274
- `SRSSampling_t2`: posterior area 0.9973, risk 0.0008681, %cost 0.06922, omega_cost 0.009507
- `SRSSampling_t3`: posterior area 0.9992, risk 0, %cost 0.2007, omega_cost 0.003507

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_10:t1` | `supports` | 217.3 | 3.85e-44 | large (0.305) | median risks: random=0.05339, solverBased=0.3299, henard=0.1484, distBased=0.1128, divDistBased=0.0651, twise=0.1042, SRSSampling=0.04644; spread=0.2834 |
| `FSE1` | `x264_time_10:t2` | `supports` | 472.2 | 7.99e-99 | large (0.6728) | median risks: random=0.01172, solverBased=0.2439, henard=0.1042, distBased=0.01302, divDistBased=0.003472, twise=0.02431, SRSSampling=0.0008681; spread=0.2431 |
| `FSE1` | `x264_time_10:t3` | `supports` | 387.3 | 1.48e-80 | large (0.5503) | median risks: random=0.003038, solverBased=0.1693, henard=0.1042, distBased=0.0008681, divDistBased=0.001736, twise=0.006076, SRSSampling=0; spread=0.1693 |
| `FSE2` | `x264_time_10:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t1; best cost-normalized=SRSSampling_t1 |
| `FSE3` | `x264_time_10:t1` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_10:t1` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t1; empirical front=SRSSampling_t1,distBased_t1,divDistBased_t1,henard_t1,random_t1 |
| `FSE5` | `x264_time_10:t1` | `refutes` | 4600 | 0.632 | negligible (0.46) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04644, median random=0.05339 |
| `FSE6` | `x264_time_10:t1` | `inconclusive` | 4228 | 0.166 | small (0.5772) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01058, median random=0.01028 |
| `FSE2` | `x264_time_10:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_10:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_10:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,divDistBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_10:t2` | `supports` | 1369 | 2.99e-17 | large (0.1369) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0008681, median random=0.01172 |
| `FSE6` | `x264_time_10:t2` | `supports` | 0 | 1.04e-31 | large (1) | A12>0.5 means SRS costs tend to be higher; median SRS=0.06922, median random=0.05652 |
| `FSE2` | `x264_time_10:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_10:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_10:t3` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3 |
| `FSE5` | `x264_time_10:t3` | `supports` | 2032 | 4.22e-13 | large (0.2032) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.003038 |
| `FSE6` | `x264_time_10:t3` | `supports` | 2 | 1.11e-31 | large (0.9998) | A12>0.5 means SRS costs tend to be higher; median SRS=0.2007, median random=0.1842 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01028 | 0.05339 | 0.9255 | -0.00312 | -0.002294 |
| `solverBased_t1` | 12 | 0.01042 | 0.01031 | 0.3299 | 0.7466 | -0.182 | -0.1813 |
| `henard_t1` | 12 | 0.01042 | 0.00886 | 0.1484 | 0.8404 | -0.08819 | -0.0777 |
| `distBased_t1` | 12 | 0.01042 | 0.009743 | 0.1128 | 0.8536 | -0.07496 | -0.07077 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01018 | 0.0651 | 0.9073 | -0.02127 | -0.01985 |
| `twise_t1` | 12 | 0.01042 | 0.01154 | 0.1042 | 0.8958 | -0.03274 | -0.0388 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01058 | 0.04644 | 0.9329 | 0.004363 | 0.00343 |
| `random_t2` | 65 | 0.05642 | 0.05652 | 0.01172 | 0.9849 | -0.0001354 | -0.0001608 |
| `solverBased_t2` | 65 | 0.05642 | 0.05501 | 0.2439 | 0.8284 | -0.1567 | -0.1563 |
| `henard_t2` | 65 | 0.05642 | 0.04241 | 0.1042 | 0.881 | -0.1041 | -0.09937 |
| `distBased_t2` | 65 | 0.05642 | 0.05755 | 0.01302 | 0.9746 | -0.0105 | -0.01078 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05789 | 0.003472 | 0.9877 | 0.002642 | 0.002274 |
| `twise_t2` | 65 | 0.05642 | 0.06094 | 0.02431 | 0.9757 | -0.00938 | -0.01046 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.06922 | 0.0008681 | 0.9973 | 0.0122 | 0.009507 |
| `random_t3` | 212 | 0.184 | 0.1842 | 0.003038 | 0.9962 | 0.0008969 | 0.0008917 |
| `solverBased_t3` | 212 | 0.184 | 0.1826 | 0.1693 | 0.8818 | -0.1135 | -0.1135 |
| `henard_t3` | 212 | 0.184 | 0.137 | 0.1042 | 0.8923 | -0.1031 | -0.1015 |
| `distBased_t3` | 212 | 0.184 | 0.191 | 0.0008681 | 0.9963 | 0.001001 | 0.0008329 |
| `divDistBased_t3` | 212 | 0.184 | 0.1829 | 0.001736 | 0.9966 | 0.001279 | 0.001307 |
| `twise_t3` | 212 | 0.184 | 0.1948 | 0.006076 | 0.9939 | -0.001403 | -0.00166 |
| `SRSSampling_t3` | 212 | 0.184 | 0.2007 | 0 | 0.9992 | 0.003892 | 0.003507 |
