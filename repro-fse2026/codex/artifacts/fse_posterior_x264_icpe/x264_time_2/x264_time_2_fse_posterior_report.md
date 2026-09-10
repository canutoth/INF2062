# x264_time_2 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t2` (risk 0, %cost 0.06755).

Best integrated confidence after normalizing the prior baseline by empirical cost: `twise_t1` (omega_cost 0.02027, %cost 0.01268).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9161, risk 0.06814, %cost 0.01034, omega_cost -0.01199
- `henard_t1`: posterior area 0.908, risk 0.09722, %cost 0.009952, omega_cost -0.01776
- `divDistBased_t1`: posterior area 0.9206, risk 0.05903, %cost 0.01046, omega_cost -0.008245
- `twise_t1`: posterior area 0.9601, risk 0.03993, %cost 0.01268, omega_cost 0.02027
- `SRSSampling_t1`: posterior area 0.9241, risk 0.0612, %cost 0.01049, omega_cost -0.004866
- `random_t2`: posterior area 0.9835, risk 0.01259, %cost 0.05644, omega_cost -0.001606
- `distBased_t2`: posterior area 0.9897, risk 0.006944, %cost 0.05988, omega_cost 0.003819
- `divDistBased_t2`: posterior area 0.9896, risk 0.01042, %cost 0.05741, omega_cost 0.004311
- `SRSSampling_t2`: posterior area 0.9978, risk 0, %cost 0.06755, omega_cost 0.01038
- `SRSSampling_t3`: posterior area 0.9996, risk 0, %cost 0.1967, omega_cost 0.003975

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_2:t1` | `supports` | 148.9 | 1.30e-29 | large (0.2063) | median risks: random=0.06814, solverBased=0.2083, henard=0.09722, distBased=0.07899, divDistBased=0.05903, twise=0.03993, SRSSampling=0.0612; spread=0.1684 |
| `FSE1` | `x264_time_2:t2` | `supports` | 499 | 1.38e-104 | large (0.7114) | median risks: random=0.01259, solverBased=0.2005, henard=0.03993, distBased=0.006944, divDistBased=0.01042, twise=0.01823, SRSSampling=0; spread=0.2005 |
| `FSE1` | `x264_time_2:t3` | `supports` | 405.6 | 1.73e-84 | moderate (0.5766) | median risks: random=0.002604, solverBased=0.0408, henard=0.03993, distBased=0.001736, divDistBased=0, twise=0.001736, SRSSampling=0; spread=0.0408 |
| `FSE2` | `x264_time_2:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t1; best cost-normalized=twise_t1 |
| `FSE3` | `x264_time_2:t1` | `refutes` | 0 |  | large (0.02513) | best cost-normalized=twise_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_2:t1` | `supports` | 0.2 |  | large frontier change (4) | count front=twise_t1; empirical front=SRSSampling_t1,divDistBased_t1,henard_t1,random_t1,twise_t1 |
| `FSE5` | `x264_time_2:t1` | `refutes` | 4552 | 0.553 | negligible (0.4552) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0612, median random=0.06814 |
| `FSE6` | `x264_time_2:t1` | `refutes` | 4503 | 0.475 | negligible (0.5497) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01049, median random=0.01034 |
| `FSE2` | `x264_time_2:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_2:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_2:t2` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,distBased_t2,divDistBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_2:t2` | `supports` | 912.5 | 7.27e-22 | large (0.09125) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.01259 |
| `FSE6` | `x264_time_2:t2` | `supports` | 0 | 1.04e-31 | large (1) | A12>0.5 means SRS costs tend to be higher; median SRS=0.06755, median random=0.05644 |
| `FSE2` | `x264_time_2:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_2:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_2:t3` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3,random_t3 |
| `FSE5` | `x264_time_2:t3` | `supports` | 1196 | 6.77e-21 | large (0.1196) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.002604 |
| `FSE6` | `x264_time_2:t3` | `supports` | 12 | 1.47e-31 | large (0.9988) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1967, median random=0.1844 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01034 | 0.06814 | 0.9161 | -0.01244 | -0.01199 |
| `solverBased_t1` | 12 | 0.01042 | 0.01039 | 0.2083 | 0.8291 | -0.0995 | -0.09934 |
| `henard_t1` | 12 | 0.01042 | 0.009952 | 0.09722 | 0.908 | -0.0206 | -0.01776 |
| `distBased_t1` | 12 | 0.01042 | 0.01026 | 0.07899 | 0.904 | -0.02457 | -0.02365 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01046 | 0.05903 | 0.9206 | -0.007964 | -0.008245 |
| `twise_t1` | 12 | 0.01042 | 0.01268 | 0.03993 | 0.9601 | 0.0315 | 0.02027 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01049 | 0.0612 | 0.9241 | -0.004466 | -0.004866 |
| `random_t2` | 65 | 0.05642 | 0.05644 | 0.01259 | 0.9835 | -0.001602 | -0.001606 |
| `solverBased_t2` | 65 | 0.05642 | 0.05546 | 0.2005 | 0.8524 | -0.1327 | -0.1324 |
| `henard_t2` | 65 | 0.05642 | 0.04602 | 0.03993 | 0.9361 | -0.049 | -0.04575 |
| `distBased_t2` | 65 | 0.05642 | 0.05988 | 0.006944 | 0.9897 | 0.004656 | 0.003819 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05741 | 0.01042 | 0.9896 | 0.004561 | 0.004311 |
| `twise_t2` | 65 | 0.05642 | 0.06508 | 0.01823 | 0.9818 | -0.003304 | -0.005238 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.06755 | 0 | 0.9978 | 0.01277 | 0.01038 |
| `random_t3` | 212 | 0.184 | 0.1844 | 0.002604 | 0.996 | 0.0006972 | 0.000688 |
| `solverBased_t3` | 212 | 0.184 | 0.187 | 0.0408 | 0.9622 | -0.03308 | -0.03315 |
| `henard_t3` | 212 | 0.184 | 0.149 | 0.03993 | 0.9461 | -0.04921 | -0.04812 |
| `distBased_t3` | 212 | 0.184 | 0.1952 | 0.001736 | 0.9972 | 0.001843 | 0.001578 |
| `divDistBased_t3` | 212 | 0.184 | 0.1849 | 0 | 0.9976 | 0.00232 | 0.002299 |
| `twise_t3` | 212 | 0.184 | 0.2032 | 0.001736 | 0.9983 | 0.002937 | 0.0025 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1967 | 0 | 0.9996 | 0.004274 | 0.003975 |
