# x264_size_3 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t2` (risk 0, %cost 0.05766).

Best integrated confidence after normalizing the prior baseline by empirical cost: `divDistBased_t1` (omega_cost 0.01532, %cost 0.01004).

Empirical cost/confidence Pareto front:

- `henard_t1`: posterior area 0.2545, risk 0.7361, %cost 0.00795, omega_cost -0.6559
- `distBased_t1`: posterior area 0.9012, risk 0.08594, %cost 0.009613, omega_cost -0.0223
- `divDistBased_t1`: posterior area 0.9416, risk 0.02865, %cost 0.01004, omega_cost 0.01532
- `random_t2`: posterior area 0.9896, risk 0.007812, %cost 0.05645, omega_cost 0.004554
- `solverBased_t2`: posterior area 0.9887, risk 0.002604, %cost 0.0563, omega_cost 0.003628
- `henard_t2`: posterior area 0.9792, risk 0.02083, %cost 0.0415, omega_cost -0.0007548
- `divDistBased_t2`: posterior area 0.9906, risk 0.005208, %cost 0.05705, omega_cost 0.005392
- `SRSSampling_t2`: posterior area 0.9979, risk 0, %cost 0.05766, omega_cost 0.01248
- `distBased_t3`: posterior area 0.9997, risk 0, %cost 0.1851, omega_cost 0.00436
- `divDistBased_t3`: posterior area 0.9994, risk 0, %cost 0.1812, omega_cost 0.004172
- `SRSSampling_t3`: posterior area 0.9998, risk 0, %cost 0.1857, omega_cost 0.004422

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_3:t1` | `supports` | 523.2 | 8.42e-110 | large (0.7463) | median risks: random=0.04297, solverBased=0.1458, henard=0.7361, distBased=0.08594, divDistBased=0.02865, twise=0.3776, SRSSampling=0.05729; spread=0.7075 |
| `FSE1` | `x264_size_3:t2` | `supports` | 422.8 | 3.43e-88 | large (0.6015) | median risks: random=0.007812, solverBased=0.002604, henard=0.02083, distBased=0.08073, divDistBased=0.005208, twise=0.2005, SRSSampling=0; spread=0.2005 |
| `FSE1` | `x264_size_3:t3` | `supports` | 559.3 | 1.40e-117 | large (0.7984) | median risks: random=0, solverBased=0, henard=0.01562, distBased=0, divDistBased=0, twise=0.07031, SRSSampling=0; spread=0.07031 |
| `FSE2` | `x264_size_3:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=divDistBased_t1; best cost-normalized=divDistBased_t1 |
| `FSE3` | `x264_size_3:t1` | `refutes` | 0 |  | large (0.02614) | best cost-normalized=divDistBased_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_3:t1` | `supports` | 0.3333 |  | large frontier change (2) | count front=divDistBased_t1; empirical front=distBased_t1,divDistBased_t1,henard_t1 |
| `FSE5` | `x264_size_3:t1` | `inconclusive` | 4296 | 0.222 | small (0.5705) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05729, median random=0.04297 |
| `FSE6` | `x264_size_3:t1` | `inconclusive` | 4392 | 0.324 | small (0.5608) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01049, median random=0.01037 |
| `FSE2` | `x264_size_3:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_size_3:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_3:t2` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,divDistBased_t2,henard_t2,random_t2,solverBased_t2 |
| `FSE5` | `x264_size_3:t2` | `supports` | 2350 | 3.10e-10 | large (0.2349) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.007812 |
| `FSE6` | `x264_size_3:t2` | `supports` | 3249 | 1.58e-04 | medium (0.6751) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05766, median random=0.05645 |
| `FSE2` | `x264_size_3:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_size_3:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_3:t3` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,distBased_t3,divDistBased_t3,henard_t3 |
| `FSE5` | `x264_size_3:t3` | `supports` | 2901 | 9.37e-10 | medium (0.2901) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `x264_size_3:t3` | `supports` | 3864 | 0.0228 | small (0.6137) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1857, median random=0.1842 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01037 | 0.04297 | 0.9329 | 0.004311 | 0.004601 |
| `solverBased_t1` | 12 | 0.01042 | 0.01034 | 0.1458 | 0.7621 | -0.1664 | -0.166 |
| `henard_t1` | 12 | 0.01042 | 0.00795 | 0.7361 | 0.2545 | -0.6741 | -0.6559 |
| `distBased_t1` | 12 | 0.01042 | 0.009613 | 0.08594 | 0.9012 | -0.02736 | -0.0223 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01004 | 0.02865 | 0.9416 | 0.01302 | 0.01532 |
| `twise_t1` | 12 | 0.01042 | 0.01056 | 0.3776 | 0.6224 | -0.3062 | -0.307 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01049 | 0.05729 | 0.9182 | -0.01042 | -0.01082 |
| `random_t2` | 65 | 0.05642 | 0.05645 | 0.007812 | 0.9896 | 0.004561 | 0.004554 |
| `solverBased_t2` | 65 | 0.05642 | 0.0563 | 0.002604 | 0.9887 | 0.003597 | 0.003628 |
| `henard_t2` | 65 | 0.05642 | 0.0415 | 0.02083 | 0.9792 | -0.005908 | -0.0007548 |
| `distBased_t2` | 65 | 0.05642 | 0.05609 | 0.08073 | 0.9511 | -0.03401 | -0.03392 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05705 | 0.005208 | 0.9906 | 0.00555 | 0.005392 |
| `twise_t2` | 65 | 0.05642 | 0.05783 | 0.2005 | 0.7995 | -0.1856 | -0.1859 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.05766 | 0 | 0.9979 | 0.01279 | 0.01248 |
| `random_t3` | 212 | 0.184 | 0.1842 | 0 | 0.9975 | 0.002173 | 0.00217 |
| `solverBased_t3` | 212 | 0.184 | 0.1858 | 0 | 0.9989 | 0.003605 | 0.00356 |
| `henard_t3` | 212 | 0.184 | 0.1333 | 0.01562 | 0.9844 | -0.01095 | -0.009197 |
| `distBased_t3` | 212 | 0.184 | 0.1851 | 0 | 0.9997 | 0.004386 | 0.00436 |
| `divDistBased_t3` | 212 | 0.184 | 0.1812 | 0 | 0.9994 | 0.0041 | 0.004172 |
| `twise_t3` | 212 | 0.184 | 0.1879 | 0.07031 | 0.9297 | -0.06564 | -0.06573 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1857 | 0 | 0.9998 | 0.004465 | 0.004422 |
