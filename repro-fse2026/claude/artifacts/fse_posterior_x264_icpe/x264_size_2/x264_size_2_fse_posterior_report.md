# x264_size_2 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.1891).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t2` (omega_cost 0.00962, %cost 0.06119).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9178, risk 0.04948, %cost 0.01034, omega_cost -0.01035
- `henard_t1`: posterior area 0.9123, risk 0.08854, %cost 0.009952, omega_cost -0.01346
- `SRSSampling_t1`: posterior area 0.9186, risk 0.05165, %cost 0.01049, omega_cost -0.01039
- `random_t2`: posterior area 0.9844, risk 0.01042, %cost 0.05644, omega_cost -0.0006337
- `solverBased_t2`: posterior area 0.9283, risk 0.0651, %cost 0.05546, omega_cost -0.05649
- `henard_t2`: posterior area 0.9241, risk 0.08247, %cost 0.04602, omega_cost -0.05767
- `SRSSampling_t2`: posterior area 0.9958, risk 0.001736, %cost 0.06119, omega_cost 0.00962
- `random_t3`: posterior area 0.9967, risk 0.001736, %cost 0.1844, omega_cost 0.001348
- `SRSSampling_t3`: posterior area 0.9992, risk 0, %cost 0.1891, omega_cost 0.003785

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_2:t1` | `supports` | 345.3 | 1.54e-71 | large (0.4897) | median risks: random=0.04948, solverBased=0.2109, henard=0.08854, distBased=0.1319, divDistBased=0.07118, twise=0.1502, SRSSampling=0.05165; spread=0.1615 |
| `FSE1` | `x264_size_2:t2` | `supports` | 423.7 | 2.26e-88 | large (0.6027) | median risks: random=0.01042, solverBased=0.0651, henard=0.08247, distBased=0.04948, divDistBased=0.06337, twise=0.04948, SRSSampling=0.001736; spread=0.08073 |
| `FSE1` | `x264_size_2:t3` | `supports` | 386.8 | 1.94e-80 | large (0.5495) | median risks: random=0.001736, solverBased=0.0625, henard=0.006944, distBased=0.001736, divDistBased=0.006944, twise=0.006944, SRSSampling=0; spread=0.0625 |
| `FSE2` | `x264_size_2:t1` | `supports` | 1 |  | changed (4.123e-05) | best size-normalized=SRSSampling_t1; best cost-normalized=random_t1 |
| `FSE3` | `x264_size_2:t1` | `refutes` | 0 |  | negligible (4.123e-05) | best cost-normalized=random_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_2:t1` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t1; empirical front=SRSSampling_t1,henard_t1,random_t1 |
| `FSE5` | `x264_size_2:t1` | `refutes` | 4796 | 0.999 | negligible (0.5204) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05165, median random=0.04948 |
| `FSE6` | `x264_size_2:t1` | `refutes` | 4503 | 0.475 | negligible (0.5497) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01049, median random=0.01034 |
| `FSE2` | `x264_size_2:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_size_2:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_2:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,henard_t2,random_t2,solverBased_t2 |
| `FSE5` | `x264_size_2:t2` | `supports` | 2168 | 7.12e-11 | large (0.2168) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001736, median random=0.01042 |
| `FSE6` | `x264_size_2:t2` | `supports` | 392 | 5.37e-27 | large (0.9608) | A12>0.5 means SRS costs tend to be higher; median SRS=0.06119, median random=0.05644 |
| `FSE2` | `x264_size_2:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_size_2:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_2:t3` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,henard_t3,random_t3 |
| `FSE5` | `x264_size_2:t3` | `supports` | 2884 | 3.17e-08 | large (0.2884) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.001736 |
| `FSE6` | `x264_size_2:t3` | `supports` | 829 | 3.28e-22 | large (0.9171) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1891, median random=0.1844 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01034 | 0.04948 | 0.9178 | -0.01079 | -0.01035 |
| `solverBased_t1` | 12 | 0.01042 | 0.01039 | 0.2109 | 0.7634 | -0.1651 | -0.165 |
| `henard_t1` | 12 | 0.01042 | 0.009952 | 0.08854 | 0.9123 | -0.0163 | -0.01346 |
| `distBased_t1` | 12 | 0.01042 | 0.01026 | 0.1319 | 0.8584 | -0.07019 | -0.06927 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01046 | 0.07118 | 0.8997 | -0.02891 | -0.02919 |
| `twise_t1` | 12 | 0.01042 | 0.01268 | 0.1502 | 0.8498 | -0.07875 | -0.08998 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01049 | 0.05165 | 0.9186 | -0.009986 | -0.01039 |
| `random_t2` | 65 | 0.05642 | 0.05644 | 0.01042 | 0.9844 | -0.0006302 | -0.0006337 |
| `solverBased_t2` | 65 | 0.05642 | 0.05546 | 0.0651 | 0.9283 | -0.05674 | -0.05649 |
| `henard_t2` | 65 | 0.05642 | 0.04602 | 0.08247 | 0.9241 | -0.06093 | -0.05767 |
| `distBased_t2` | 65 | 0.05642 | 0.05988 | 0.04948 | 0.9363 | -0.04876 | -0.04959 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05741 | 0.06337 | 0.952 | -0.03311 | -0.03336 |
| `twise_t2` | 65 | 0.05642 | 0.06508 | 0.04948 | 0.9505 | -0.03455 | -0.03649 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.06119 | 0.001736 | 0.9958 | 0.01075 | 0.00962 |
| `random_t3` | 212 | 0.184 | 0.1844 | 0.001736 | 0.9967 | 0.001357 | 0.001348 |
| `solverBased_t3` | 212 | 0.184 | 0.187 | 0.0625 | 0.9541 | -0.04118 | -0.04125 |
| `henard_t3` | 212 | 0.184 | 0.149 | 0.006944 | 0.988 | -0.00735 | -0.006262 |
| `distBased_t3` | 212 | 0.184 | 0.1952 | 0.001736 | 0.9838 | -0.01158 | -0.01184 |
| `divDistBased_t3` | 212 | 0.184 | 0.1849 | 0.006944 | 0.985 | -0.01029 | -0.01031 |
| `twise_t3` | 212 | 0.184 | 0.2032 | 0.006944 | 0.9931 | -0.002272 | -0.002708 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1891 | 0 | 0.9992 | 0.003909 | 0.003785 |
