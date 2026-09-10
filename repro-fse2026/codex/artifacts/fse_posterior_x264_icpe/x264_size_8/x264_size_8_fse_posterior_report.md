# x264_size_8 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `henard_t2` (risk 0, %cost 0.04241).

Best integrated confidence after normalizing the prior baseline by empirical cost: `divDistBased_t1` (omega_cost 0.03246, %cost 0.01006).

Empirical cost/confidence Pareto front:

- `solverBased_t1`: posterior area 0.8421, risk 0.04688, %cost 0.009471, omega_cost -0.08049
- `henard_t1`: posterior area 0.3657, risk 0.6337, %cost 0.00859, omega_cost -0.5503
- `distBased_t1`: posterior area 0.9286, risk 0.05729, %cost 0.009758, omega_cost 0.004141
- `divDistBased_t1`: posterior area 0.9589, risk 0.03646, %cost 0.01006, omega_cost 0.03246
- `henard_t2`: posterior area 1, risk 0, %cost 0.04241, omega_cost 0.01966

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_8:t1` | `supports` | 436.7 | 3.53e-91 | large (0.6215) | median risks: random=0.05339, solverBased=0.04688, henard=0.6337, distBased=0.05729, divDistBased=0.03646, twise=0.5104, SRSSampling=0.06771; spread=0.5972 |
| `FSE1` | `x264_size_8:t2` | `supports` | 567 | 3.08e-119 | large (0.8095) | median risks: random=0.01042, solverBased=0.02474, henard=0, distBased=0.05729, divDistBased=0, twise=0.2161, SRSSampling=0; spread=0.2161 |
| `FSE1` | `x264_size_8:t3` | `supports` | 647.2 | 1.56e-136 | moderate (0.9252) | median risks: random=0, solverBased=0.02083, henard=0, distBased=0, divDistBased=0, twise=0.04688, SRSSampling=0; spread=0.04688 |
| `FSE2` | `x264_size_8:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=divDistBased_t1; best cost-normalized=divDistBased_t1 |
| `FSE3` | `x264_size_8:t1` | `refutes` | 0 |  | large (0.04418) | best cost-normalized=divDistBased_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_8:t1` | `supports` | 0.25 |  | large frontier change (3) | count front=divDistBased_t1; empirical front=distBased_t1,divDistBased_t1,henard_t1,solverBased_t1 |
| `FSE5` | `x264_size_8:t1` | `refutes` | 4488 | 0.452 | negligible (0.5512) | A12<0.5 means SRS risks tend to be lower; median SRS=0.06771, median random=0.05339 |
| `FSE6` | `x264_size_8:t1` | `inconclusive` | 4237 | 0.172 | small (0.5763) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01051, median random=0.01031 |
| `FSE2` | `x264_size_8:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t2; best cost-normalized=henard_t2 |
| `FSE3` | `x264_size_8:t2` | `refutes` | 0 |  | moderate (0.005342) | best cost-normalized=henard_t2; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_8:t2` | `refutes` | 1 |  | same frontier (0) | count front=henard_t2; empirical front=henard_t2 |
| `FSE5` | `x264_size_8:t2` | `supports` | 2631 | 8.59e-12 | large (0.2631) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.01042 |
| `FSE6` | `x264_size_8:t2` | `supports` | 2954 | 6.82e-06 | medium (0.2954) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05526, median random=0.05657 |
| `FSE2` | `x264_size_8:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t3; best cost-normalized=henard_t3 |
| `FSE3` | `x264_size_8:t3` | `refutes` | 0 |  | moderate (0.001559) | best cost-normalized=henard_t3; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_8:t3` | `supports` | 0.5 |  | frontier change (1) | count front=divDistBased_t3,henard_t3; empirical front=henard_t3 |
| `FSE5` | `x264_size_8:t3` | `supports` | 4249 | 9.76e-04 | small (0.4249) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `x264_size_8:t3` | `supports` | 2871 | 2.58e-06 | large (0.2871) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1824, median random=0.1841 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01031 | 0.05339 | 0.9282 | -0.0003683 | 0.0002867 |
| `solverBased_t1` | 12 | 0.01042 | 0.009471 | 0.04688 | 0.8421 | -0.08651 | -0.08049 |
| `henard_t1` | 12 | 0.01042 | 0.00859 | 0.6337 | 0.3657 | -0.5629 | -0.5503 |
| `distBased_t1` | 12 | 0.01042 | 0.009758 | 0.05729 | 0.9286 | 4.836e-05 | 0.004141 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01006 | 0.03646 | 0.9589 | 0.03029 | 0.03246 |
| `twise_t1` | 12 | 0.01042 | 0.01074 | 0.5104 | 0.4896 | -0.439 | -0.4408 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01051 | 0.06771 | 0.9174 | -0.01116 | -0.01172 |
| `random_t2` | 65 | 0.05642 | 0.05657 | 0.01042 | 0.9891 | 0.00404 | 0.004002 |
| `solverBased_t2` | 65 | 0.05642 | 0.05223 | 0.02474 | 0.9721 | -0.01299 | -0.01183 |
| `henard_t2` | 65 | 0.05642 | 0.04241 | 0 | 1 | 0.01493 | 0.01966 |
| `distBased_t2` | 65 | 0.05642 | 0.05655 | 0.05729 | 0.9599 | -0.0252 | -0.02524 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05685 | 0 | 0.9972 | 0.01214 | 0.01203 |
| `twise_t2` | 65 | 0.05642 | 0.05745 | 0.2161 | 0.7839 | -0.2012 | -0.2015 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.05526 | 0 | 0.9991 | 0.01401 | 0.01432 |
| `random_t3` | 212 | 0.184 | 0.1841 | 0 | 0.9981 | 0.002772 | 0.00277 |
| `solverBased_t3` | 212 | 0.184 | 0.1757 | 0.02083 | 0.9768 | -0.0185 | -0.01828 |
| `henard_t3` | 212 | 0.184 | 0.139 | 0 | 1 | 0.004673 | 0.006169 |
| `distBased_t3` | 212 | 0.184 | 0.1858 | 0 | 0.9992 | 0.00384 | 0.003795 |
| `divDistBased_t3` | 212 | 0.184 | 0.1822 | 0 | 1 | 0.004673 | 0.004719 |
| `twise_t3` | 212 | 0.184 | 0.1862 | 0.04688 | 0.9531 | -0.0422 | -0.04226 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1824 | 0 | 0.9999 | 0.004569 | 0.004611 |
