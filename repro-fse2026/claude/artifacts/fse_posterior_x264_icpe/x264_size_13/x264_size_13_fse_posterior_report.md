# x264_size_13 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t2` (risk 0, %cost 0.05958).

Best integrated confidence after normalizing the prior baseline by empirical cost: `henard_t1` (omega_cost 0.05039, %cost 0.009633).

Empirical cost/confidence Pareto front:

- `henard_t1`: posterior area 0.974, risk 0.02604, %cost 0.009633, omega_cost 0.05039
- `random_t2`: posterior area 0.9865, risk 0.008681, %cost 0.05634, omega_cost 0.001475
- `henard_t2`: posterior area 0.9774, risk 0.02431, %cost 0.04569, omega_cost -0.004336
- `SRSSampling_t2`: posterior area 0.9959, risk 0, %cost 0.05958, omega_cost 0.0101
- `henard_t3`: posterior area 0.9983, risk 0.001736, %cost 0.1477, omega_cost 0.004071
- `SRSSampling_t3`: posterior area 0.9996, risk 0, %cost 0.1868, omega_cost 0.004169

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_13:t1` | `supports` | 301.8 | 3.39e-62 | large (0.4268) | median risks: random=0.05252, solverBased=0.1146, henard=0.02604, distBased=0.1059, divDistBased=0.09158, twise=0.07726, SRSSampling=0.06337; spread=0.08854 |
| `FSE1` | `x264_size_13:t2` | `supports` | 392.7 | 1.04e-81 | large (0.558) | median risks: random=0.008681, solverBased=0.06337, henard=0.02431, distBased=0.02778, divDistBased=0.07943, twise=0.01736, SRSSampling=0; spread=0.07943 |
| `FSE1` | `x264_size_13:t3` | `supports` | 404.1 | 3.60e-84 | large (0.5745) | median risks: random=0.001736, solverBased=0.05642, henard=0.001736, distBased=0.006944, divDistBased=0.008681, twise=0.001736, SRSSampling=0; spread=0.05642 |
| `FSE2` | `x264_size_13:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t1; best cost-normalized=henard_t1 |
| `FSE3` | `x264_size_13:t1` | `refutes` | 0 |  | large (0.06175) | best cost-normalized=henard_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_13:t1` | `refutes` | 1 |  | same frontier (0) | count front=henard_t1; empirical front=henard_t1 |
| `FSE5` | `x264_size_13:t1` | `refutes` | 4626 | 0.678 | negligible (0.5374) | A12<0.5 means SRS risks tend to be lower; median SRS=0.06337, median random=0.05252 |
| `FSE6` | `x264_size_13:t1` | `refutes` | 4522 | 0.505 | negligible (0.5477) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01048, median random=0.01037 |
| `FSE2` | `x264_size_13:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_size_13:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_13:t2` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,henard_t2,random_t2 |
| `FSE5` | `x264_size_13:t2` | `supports` | 1822 | 2.20e-14 | large (0.1822) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.008681 |
| `FSE6` | `x264_size_13:t2` | `supports` | 1305 | 1.48e-17 | large (0.8695) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05958, median random=0.05634 |
| `FSE2` | `x264_size_13:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_size_13:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_13:t3` | `supports` | 0.5 |  | frontier change (1) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,henard_t3 |
| `FSE5` | `x264_size_13:t3` | `supports` | 2679 | 2.33e-09 | large (0.2679) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.001736 |
| `FSE6` | `x264_size_13:t3` | `supports` | 2276 | 7.47e-10 | large (0.7724) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1868, median random=0.1844 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01037 | 0.05252 | 0.9253 | -0.003294 | -0.002992 |
| `solverBased_t1` | 12 | 0.01042 | 0.01024 | 0.1146 | 0.8363 | -0.09223 | -0.0912 |
| `henard_t1` | 12 | 0.01042 | 0.009633 | 0.02604 | 0.974 | 0.04547 | 0.05039 |
| `distBased_t1` | 12 | 0.01042 | 0.01009 | 0.1059 | 0.8817 | -0.04683 | -0.04483 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01035 | 0.09158 | 0.8877 | -0.0409 | -0.04051 |
| `twise_t1` | 12 | 0.01042 | 0.01253 | 0.07726 | 0.9227 | -0.005828 | -0.01642 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01048 | 0.06337 | 0.9176 | -0.01098 | -0.01136 |
| `random_t2` | 65 | 0.05642 | 0.05634 | 0.008681 | 0.9865 | 0.001453 | 0.001475 |
| `solverBased_t2` | 65 | 0.05642 | 0.05447 | 0.06337 | 0.9272 | -0.05786 | -0.05734 |
| `henard_t2` | 65 | 0.05642 | 0.04569 | 0.02431 | 0.9774 | -0.007714 | -0.004336 |
| `distBased_t2` | 65 | 0.05642 | 0.05911 | 0.02778 | 0.9536 | -0.03152 | -0.03218 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05736 | 0.07943 | 0.9423 | -0.04277 | -0.04301 |
| `twise_t2` | 65 | 0.05642 | 0.06441 | 0.01736 | 0.9826 | -0.002436 | -0.004237 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.05958 | 0 | 0.9959 | 0.01087 | 0.0101 |
| `random_t3` | 212 | 0.184 | 0.1844 | 0.001736 | 0.9961 | 0.0008014 | 0.0007917 |
| `solverBased_t3` | 212 | 0.184 | 0.1848 | 0.05642 | 0.9473 | -0.04798 | -0.048 |
| `henard_t3` | 212 | 0.184 | 0.1477 | 0.001736 | 0.9983 | 0.002937 | 0.004071 |
| `distBased_t3` | 212 | 0.184 | 0.1936 | 0.006944 | 0.9942 | -0.001134 | -0.001364 |
| `divDistBased_t3` | 212 | 0.184 | 0.1844 | 0.008681 | 0.991 | -0.004355 | -0.004364 |
| `twise_t3` | 212 | 0.184 | 0.2017 | 0.001736 | 0.9983 | 0.002937 | 0.00253 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1868 | 0 | 0.9996 | 0.004239 | 0.004169 |
