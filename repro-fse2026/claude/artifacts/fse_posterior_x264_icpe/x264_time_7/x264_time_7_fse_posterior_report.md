# x264_time_7 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.2005).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t2` (omega_cost 0.008052, %cost 0.06876).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.923, risk 0.05686, %cost 0.01023, omega_cost -0.004503
- `henard_t1`: posterior area 0.8312, risk 0.1476, %cost 0.008543, omega_cost -0.08435
- `distBased_t1`: posterior area 0.8381, risk 0.1328, %cost 0.009535, omega_cost -0.08493
- `divDistBased_t1`: posterior area 0.9042, risk 0.08594, %cost 0.009933, omega_cost -0.02144
- `SRSSampling_t1`: posterior area 0.9332, risk 0.05165, %cost 0.01055, omega_cost 0.003831
- `random_t2`: posterior area 0.9856, risk 0.01085, %cost 0.05653, omega_cost 0.0004973
- `distBased_t2`: posterior area 0.9725, risk 0.02951, %cost 0.05616, omega_cost -0.01253
- `divDistBased_t2`: posterior area 0.9895, risk 0.001302, %cost 0.05737, omega_cost 0.004227
- `SRSSampling_t2`: posterior area 0.9957, risk 0.001736, %cost 0.06876, omega_cost 0.008052
- `divDistBased_t3`: posterior area 0.9975, risk 0.0008681, %cost 0.1831, omega_cost 0.002189
- `twise_t3`: posterior area 0.9983, risk 0.001736, %cost 0.1892, omega_cost 0.00281
- `SRSSampling_t3`: posterior area 0.9992, risk 0, %cost 0.2005, omega_cost 0.003468

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_7:t1` | `supports` | 154.1 | 1.07e-30 | large (0.2137) | median risks: random=0.05686, solverBased=0.3958, henard=0.1476, distBased=0.1328, divDistBased=0.08594, twise=0.08594, SRSSampling=0.05165; spread=0.3442 |
| `FSE1` | `x264_time_7:t2` | `supports` | 421 | 8.50e-88 | large (0.5989) | median risks: random=0.01085, solverBased=0.3681, henard=0.08594, distBased=0.02951, divDistBased=0.001302, twise=0.02604, SRSSampling=0.001736; spread=0.3668 |
| `FSE1` | `x264_time_7:t3` | `supports` | 352.9 | 3.76e-73 | large (0.5005) | median risks: random=0.00217, solverBased=0.3333, henard=0.08594, distBased=0.00434, divDistBased=0.0008681, twise=0.001736, SRSSampling=0; spread=0.3333 |
| `FSE2` | `x264_time_7:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t1; best cost-normalized=SRSSampling_t1 |
| `FSE3` | `x264_time_7:t1` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_7:t1` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t1; empirical front=SRSSampling_t1,distBased_t1,divDistBased_t1,henard_t1,random_t1 |
| `FSE5` | `x264_time_7:t1` | `refutes` | 4622 | 0.672 | negligible (0.4622) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05165, median random=0.05686 |
| `FSE6` | `x264_time_7:t1` | `inconclusive` | 4246 | 0.179 | small (0.5754) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01055, median random=0.01023 |
| `FSE2` | `x264_time_7:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_7:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_7:t2` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,distBased_t2,divDistBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_7:t2` | `supports` | 2182 | 1.43e-10 | large (0.2182) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001736, median random=0.01085 |
| `FSE6` | `x264_time_7:t2` | `supports` | 0 | 1.04e-31 | large (1) | A12>0.5 means SRS costs tend to be higher; median SRS=0.06876, median random=0.05653 |
| `FSE2` | `x264_time_7:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_7:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_7:t3` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3,twise_t3 |
| `FSE5` | `x264_time_7:t3` | `supports` | 2144 | 3.95e-12 | large (0.2144) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.00217 |
| `FSE6` | `x264_time_7:t3` | `supports` | 5 | 1.21e-31 | large (0.9995) | A12>0.5 means SRS costs tend to be higher; median SRS=0.2005, median random=0.1839 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01023 | 0.05686 | 0.923 | -0.005611 | -0.004503 |
| `solverBased_t1` | 12 | 0.01042 | 0.009826 | 0.3958 | 0.7219 | -0.2066 | -0.203 |
| `henard_t1` | 12 | 0.01042 | 0.008543 | 0.1476 | 0.8312 | -0.09737 | -0.08435 |
| `distBased_t1` | 12 | 0.01042 | 0.009535 | 0.1328 | 0.8381 | -0.09052 | -0.08493 |
| `divDistBased_t1` | 12 | 0.01042 | 0.009933 | 0.08594 | 0.9042 | -0.0244 | -0.02144 |
| `twise_t1` | 12 | 0.01042 | 0.01099 | 0.08594 | 0.9141 | -0.01451 | -0.01774 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01055 | 0.05165 | 0.9332 | 0.00458 | 0.003831 |
| `random_t2` | 65 | 0.05642 | 0.05653 | 0.01085 | 0.9856 | 0.0005243 | 0.0004973 |
| `solverBased_t2` | 65 | 0.05642 | 0.05281 | 0.3681 | 0.7492 | -0.2358 | -0.2349 |
| `henard_t2` | 65 | 0.05642 | 0.04206 | 0.08594 | 0.884 | -0.1011 | -0.09621 |
| `distBased_t2` | 65 | 0.05642 | 0.05616 | 0.02951 | 0.9725 | -0.01259 | -0.01253 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05737 | 0.001302 | 0.9895 | 0.004465 | 0.004227 |
| `twise_t2` | 65 | 0.05642 | 0.05863 | 0.02604 | 0.974 | -0.01112 | -0.01166 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.06876 | 0.001736 | 0.9957 | 0.01066 | 0.008052 |
| `random_t3` | 212 | 0.184 | 0.1839 | 0.00217 | 0.9964 | 0.001088 | 0.001091 |
| `solverBased_t3` | 212 | 0.184 | 0.1754 | 0.3333 | 0.782 | -0.2134 | -0.2131 |
| `henard_t3` | 212 | 0.184 | 0.1357 | 0.08594 | 0.8965 | -0.09887 | -0.09723 |
| `distBased_t3` | 212 | 0.184 | 0.1862 | 0.00434 | 0.9939 | -0.001447 | -0.001502 |
| `divDistBased_t3` | 212 | 0.184 | 0.1831 | 0.0008681 | 0.9975 | 0.002164 | 0.002189 |
| `twise_t3` | 212 | 0.184 | 0.1892 | 0.001736 | 0.9983 | 0.002937 | 0.00281 |
| `SRSSampling_t3` | 212 | 0.184 | 0.2005 | 0 | 0.9992 | 0.003848 | 0.003468 |
