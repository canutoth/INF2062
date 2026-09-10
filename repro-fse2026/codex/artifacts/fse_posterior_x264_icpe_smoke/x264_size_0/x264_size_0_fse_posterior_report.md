# x264_size_0 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `henard_t2` (risk 0, %cost 0.04079).

Best integrated confidence after normalizing the prior baseline by empirical cost: `henard_t2` (omega_cost 0.02041, %cost 0.04079).

Empirical cost/confidence Pareto front:

- `henard_t1`: posterior area 0.4729, risk 0.526, %cost 0.00782, omega_cost -0.4362
- `distBased_t1`: posterior area 0.932, risk 0.02083, %cost 0.009285, omega_cost 0.0108
- `divDistBased_t1`: posterior area 0.9417, risk 0.02083, %cost 0.009982, omega_cost 0.01578
- `henard_t2`: posterior area 1, risk 0, %cost 0.04079, omega_cost 0.02041

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_0:t1` | `supports` | 429.2 | 1.50e-89 | large (0.7018) | median risks: random=0.04688, solverBased=0.09635, henard=0.526, distBased=0.02083, divDistBased=0.02083, twise=0.3932, SRSSampling=0.1042; spread=0.5052 |
| `FSE1` | `x264_size_0:t2` | `supports` | 521.3 | 2.21e-109 | large (0.8545) | median risks: random=0.01042, solverBased=0.09115, henard=0, distBased=0.02083, divDistBased=0.005208, twise=0.1797, SRSSampling=0; spread=0.1797 |
| `FSE1` | `x264_size_0:t3` | `supports` | 496 | 6.00e-104 | large (0.8127) | median risks: random=0, solverBased=0.08333, henard=0, distBased=0.005208, divDistBased=0, twise=0.05729, SRSSampling=0; spread=0.08333 |
| `FSE2` | `x264_size_0:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=divDistBased_t1; best cost-normalized=divDistBased_t1 |
| `FSE3` | `x264_size_0:t1` | `refutes` | 0 |  | large (0.05601) | best cost-normalized=divDistBased_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_0:t1` | `supports` | 0.3333 |  | large frontier change (2) | count front=divDistBased_t1; empirical front=distBased_t1,divDistBased_t1,henard_t1 |
| `FSE5` | `x264_size_0:t1` | `inconclusive` | 317.5 | 0.162 | medium (0.6825) | A12<0.5 means SRS risks tend to be lower; median SRS=0.1042, median random=0.04688 |
| `FSE6` | `x264_size_0:t1` | `refutes` | 452 | 0.999 | negligible (0.548) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01036, median random=0.01027 |
| `FSE2` | `x264_size_0:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t2; best cost-normalized=henard_t2 |
| `FSE3` | `x264_size_0:t2` | `refutes` | 0 |  | moderate (0.00665) | best cost-normalized=henard_t2; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_0:t2` | `refutes` | 1 |  | same frontier (0) | count front=henard_t2; empirical front=henard_t2 |
| `FSE5` | `x264_size_0:t2` | `supports` | 212 | 0.0103 | large (0.212) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.01042 |
| `FSE6` | `x264_size_0:t2` | `inconclusive` | 287 | 0.0864 | large (0.287) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05491, median random=0.05662 |
| `FSE2` | `x264_size_0:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t3; best cost-normalized=henard_t3 |
| `FSE3` | `x264_size_0:t3` | `refutes` | 0 |  | moderate (0.00228) | best cost-normalized=henard_t3; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_0:t3` | `refutes` | 1 |  | same frontier (0) | count front=henard_t3; empirical front=henard_t3 |
| `FSE5` | `x264_size_0:t3` | `inconclusive` | 382 | 0.308 | small (0.382) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `x264_size_0:t3` | `supports` | 168 | 0.00316 | large (0.168) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1797, median random=0.1844 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01027 | 0.04688 | 0.9251 | -0.003502 | -0.002605 |
| `solverBased_t1` | 12 | 0.01042 | 0.01141 | 0.09635 | 0.7863 | -0.1423 | -0.1477 |
| `henard_t1` | 12 | 0.01042 | 0.00782 | 0.526 | 0.4729 | -0.4556 | -0.4362 |
| `distBased_t1` | 12 | 0.01042 | 0.009285 | 0.02083 | 0.932 | 0.00346 | 0.0108 |
| `divDistBased_t1` | 12 | 0.01042 | 0.009982 | 0.02083 | 0.9417 | 0.01313 | 0.01578 |
| `twise_t1` | 12 | 0.01042 | 0.01131 | 0.3932 | 0.6068 | -0.3218 | -0.3267 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01036 | 0.1042 | 0.888 | -0.04055 | -0.04023 |
| `random_t2` | 65 | 0.05642 | 0.05662 | 0.01042 | 0.9875 | 0.002425 | 0.002374 |
| `solverBased_t2` | 65 | 0.05642 | 0.05778 | 0.09115 | 0.9056 | -0.07948 | -0.07982 |
| `henard_t2` | 65 | 0.05642 | 0.04079 | 0 | 1 | 0.01493 | 0.02041 |
| `distBased_t2` | 65 | 0.05642 | 0.05622 | 0.02083 | 0.9803 | -0.004788 | -0.004737 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05845 | 0.005208 | 0.9939 | 0.008832 | 0.00833 |
| `twise_t2` | 65 | 0.05642 | 0.06021 | 0.1797 | 0.8203 | -0.1648 | -0.1657 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.05491 | 0 | 0.9984 | 0.01336 | 0.01376 |
| `random_t3` | 212 | 0.184 | 0.1844 | 0 | 0.9969 | 0.0016 | 0.001592 |
| `solverBased_t3` | 212 | 0.184 | 0.1873 | 0.08333 | 0.9111 | -0.08418 | -0.08426 |
| `henard_t3` | 212 | 0.184 | 0.1309 | 0 | 1 | 0.004673 | 0.006544 |
| `distBased_t3` | 212 | 0.184 | 0.1875 | 0.005208 | 0.9965 | 0.001183 | 0.001098 |
| `divDistBased_t3` | 212 | 0.184 | 0.1822 | 0 | 0.9989 | 0.003527 | 0.003574 |
| `twise_t3` | 212 | 0.184 | 0.1932 | 0.05729 | 0.9427 | -0.05262 | -0.05284 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1797 | 0 | 0.9995 | 0.004152 | 0.004264 |
