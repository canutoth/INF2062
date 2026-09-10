# x264_size_10 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `divDistBased_t2` (risk 0, %cost 0.05789).

Best integrated confidence after normalizing the prior baseline by empirical cost: `divDistBased_t1` (omega_cost 0.01587, %cost 0.01018).

Empirical cost/confidence Pareto front:

- `henard_t1`: posterior area 0.5475, risk 0.4557, %cost 0.00886, omega_cost -0.3706
- `distBased_t1`: posterior area 0.8966, risk 0.09375, %cost 0.009743, omega_cost -0.02777
- `divDistBased_t1`: posterior area 0.943, risk 0.0612, %cost 0.01018, omega_cost 0.01587
- `henard_t2`: posterior area 0.9896, risk 0.01042, %cost 0.04241, omega_cost 0.009245
- `SRSSampling_t2`: posterior area 0.9981, risk 0, %cost 0.05233, omega_cost 0.01418
- `henard_t3`: posterior area 1, risk 0, %cost 0.137, omega_cost 0.006259

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_10:t1` | `supports` | 411.8 | 8.08e-86 | large (0.5856) | median risks: random=0.04688, solverBased=0.08333, henard=0.4557, distBased=0.09375, divDistBased=0.0612, twise=0.3524, SRSSampling=0.07161; spread=0.4089 |
| `FSE1` | `x264_size_10:t2` | `supports` | 569.8 | 7.76e-120 | large (0.8135) | median risks: random=0.005208, solverBased=0.02865, henard=0.01042, distBased=0.08854, divDistBased=0, twise=0.1476, SRSSampling=0; spread=0.1476 |
| `FSE1` | `x264_size_10:t3` | `supports` | 608.5 | 3.42e-128 | moderate (0.8694) | median risks: random=0, solverBased=0.02083, henard=0, distBased=0, divDistBased=0, twise=0.04167, SRSSampling=0; spread=0.04167 |
| `FSE2` | `x264_size_10:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=divDistBased_t1; best cost-normalized=divDistBased_t1 |
| `FSE3` | `x264_size_10:t1` | `refutes` | 0 |  | large (0.03166) | best cost-normalized=divDistBased_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_10:t1` | `supports` | 0.3333 |  | large frontier change (2) | count front=divDistBased_t1; empirical front=distBased_t1,divDistBased_t1,henard_t1 |
| `FSE5` | `x264_size_10:t1` | `inconclusive` | 4360 | 0.288 | small (0.5639) | A12<0.5 means SRS risks tend to be lower; median SRS=0.07161, median random=0.04688 |
| `FSE6` | `x264_size_10:t1` | `inconclusive` | 4228 | 0.166 | small (0.5772) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01058, median random=0.01028 |
| `FSE2` | `x264_size_10:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_size_10:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_10:t2` | `supports` | 0.5 |  | frontier change (1) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,henard_t2 |
| `FSE5` | `x264_size_10:t2` | `supports` | 2090 | 2.95e-14 | large (0.209) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.005208 |
| `FSE6` | `x264_size_10:t2` | `supports` | 1073 | 9.44e-20 | large (0.1073) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05233, median random=0.05652 |
| `FSE2` | `x264_size_10:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t3; best cost-normalized=henard_t3 |
| `FSE3` | `x264_size_10:t3` | `refutes` | 0 |  | moderate (0.001711) | best cost-normalized=henard_t3; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_10:t3` | `supports` | 0.5 |  | frontier change (1) | count front=divDistBased_t3,henard_t3; empirical front=henard_t3 |
| `FSE5` | `x264_size_10:t3` | `supports` | 3374 | 7.60e-08 | medium (0.3373) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `x264_size_10:t3` | `supports` | 1099 | 1.69e-19 | large (0.1099) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1788, median random=0.1842 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01028 | 0.04688 | 0.9313 | 0.002713 | 0.003539 |
| `solverBased_t1` | 12 | 0.01042 | 0.01031 | 0.08333 | 0.7482 | -0.1804 | -0.1798 |
| `henard_t1` | 12 | 0.01042 | 0.00886 | 0.4557 | 0.5475 | -0.3811 | -0.3706 |
| `distBased_t1` | 12 | 0.01042 | 0.009743 | 0.09375 | 0.8966 | -0.03196 | -0.02777 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01018 | 0.0612 | 0.943 | 0.01445 | 0.01587 |
| `twise_t1` | 12 | 0.01042 | 0.01154 | 0.3524 | 0.6476 | -0.281 | -0.2871 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01058 | 0.07161 | 0.9137 | -0.01486 | -0.01579 |
| `random_t2` | 65 | 0.05642 | 0.05652 | 0.005208 | 0.9884 | 0.003363 | 0.003337 |
| `solverBased_t2` | 65 | 0.05642 | 0.05501 | 0.02865 | 0.9596 | -0.02545 | -0.02507 |
| `henard_t2` | 65 | 0.05642 | 0.04241 | 0.01042 | 0.9896 | 0.004509 | 0.009245 |
| `distBased_t2` | 65 | 0.05642 | 0.05755 | 0.08854 | 0.9352 | -0.04984 | -0.05012 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05789 | 0 | 0.9953 | 0.01026 | 0.009896 |
| `twise_t2` | 65 | 0.05642 | 0.06094 | 0.1476 | 0.8524 | -0.1326 | -0.1337 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.05233 | 0 | 0.9981 | 0.01305 | 0.01418 |
| `random_t3` | 212 | 0.184 | 0.1842 | 0 | 0.9971 | 0.001756 | 0.001751 |
| `solverBased_t3` | 212 | 0.184 | 0.1826 | 0.02083 | 0.9689 | -0.02642 | -0.02638 |
| `henard_t3` | 212 | 0.184 | 0.137 | 0 | 1 | 0.004673 | 0.006259 |
| `distBased_t3` | 212 | 0.184 | 0.191 | 0 | 0.9991 | 0.003735 | 0.003567 |
| `divDistBased_t3` | 212 | 0.184 | 0.1829 | 0 | 1 | 0.004673 | 0.004701 |
| `twise_t3` | 212 | 0.184 | 0.1948 | 0.04167 | 0.9583 | -0.03699 | -0.03725 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1788 | 0 | 0.9997 | 0.004412 | 0.004548 |
