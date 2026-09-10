# x264_size_1 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.1831).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t2` (omega_cost 0.01173, %cost 0.05571).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9336, risk 0.04861, %cost 0.01027, omega_cost 0.00588
- `henard_t1`: posterior area 0.9287, risk 0.07031, %cost 0.0092, omega_cost 0.008047
- `solverBased_t2`: posterior area 0.9719, risk 0.01649, %cost 0.05507, omega_cost -0.01283
- `henard_t2`: posterior area 0.9661, risk 0.03385, %cost 0.04254, omega_cost -0.01425
- `SRSSampling_t2`: posterior area 0.9966, risk 0.001736, %cost 0.05571, omega_cost 0.01173
- `SRSSampling_t3`: posterior area 0.9989, risk 0, %cost 0.1831, omega_cost 0.003637

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_1:t1` | `supports` | 445.8 | 3.89e-93 | large (0.6347) | median risks: random=0.04861, solverBased=0.2135, henard=0.07031, distBased=0.2014, divDistBased=0.06163, twise=0.2517, SRSSampling=0.04601; spread=0.2057 |
| `FSE1` | `x264_size_1:t2` | `supports` | 371.1 | 4.55e-77 | large (0.5268) | median risks: random=0.01128, solverBased=0.01649, henard=0.03385, distBased=0.07031, divDistBased=0.03689, twise=0.05035, SRSSampling=0.001736; spread=0.06858 |
| `FSE1` | `x264_size_1:t3` | `supports` | 336.1 | 1.45e-69 | moderate (0.4764) | median risks: random=0.003472, solverBased=0.005208, henard=0.009549, distBased=0.007812, divDistBased=0.003472, twise=0.01476, SRSSampling=0; spread=0.01476 |
| `FSE2` | `x264_size_1:t1` | `supports` | 1 |  | changed (0.002167) | best size-normalized=random_t1; best cost-normalized=henard_t1 |
| `FSE3` | `x264_size_1:t1` | `refutes` | 0 |  | moderate (0.009561) | best cost-normalized=henard_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_1:t1` | `supports` | 0.5 |  | frontier change (1) | count front=random_t1; empirical front=henard_t1,random_t1 |
| `FSE5` | `x264_size_1:t1` | `refutes` | 4904 | 0.791 | negligible (0.4904) | A12<0.5 means SRS risks tend to be lower; median SRS=0.04601, median random=0.04861 |
| `FSE6` | `x264_size_1:t1` | `inconclusive` | 4294 | 0.221 | small (0.5706) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01052, median random=0.01027 |
| `FSE2` | `x264_size_1:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_size_1:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_1:t2` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,henard_t2,solverBased_t2 |
| `FSE5` | `x264_size_1:t2` | `supports` | 1430 | 1.42e-16 | large (0.143) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001736, median random=0.01128 |
| `FSE6` | `x264_size_1:t2` | `supports` | 3795 | 0.0145 | small (0.3795) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05571, median random=0.05664 |
| `FSE2` | `x264_size_1:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_size_1:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_1:t3` | `supports` | 0.5 |  | frontier change (1) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,henard_t3 |
| `FSE5` | `x264_size_1:t3` | `supports` | 2078 | 6.19e-12 | large (0.2078) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.003472 |
| `FSE6` | `x264_size_1:t3` | `supports` | 3964 | 0.0422 | small (0.3964) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1831, median random=0.1844 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01027 | 0.04861 | 0.9336 | 0.005014 | 0.00588 |
| `solverBased_t1` | 12 | 0.01042 | 0.01034 | 0.2135 | 0.6816 | -0.247 | -0.2466 |
| `henard_t1` | 12 | 0.01042 | 0.0092 | 0.07031 | 0.9287 | 0.0001004 | 0.008047 |
| `distBased_t1` | 12 | 0.01042 | 0.00983 | 0.2014 | 0.814 | -0.1146 | -0.111 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01035 | 0.06163 | 0.9008 | -0.02778 | -0.02741 |
| `twise_t1` | 12 | 0.01042 | 0.01252 | 0.2517 | 0.7483 | -0.1803 | -0.1909 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01052 | 0.04601 | 0.9277 | -0.0009152 | -0.001513 |
| `random_t2` | 65 | 0.05642 | 0.05664 | 0.01128 | 0.9849 | -0.0001441 | -0.0001997 |
| `solverBased_t2` | 65 | 0.05642 | 0.05507 | 0.01649 | 0.9719 | -0.01319 | -0.01283 |
| `henard_t2` | 65 | 0.05642 | 0.04254 | 0.03385 | 0.9661 | -0.01893 | -0.01425 |
| `distBased_t2` | 65 | 0.05642 | 0.05835 | 0.07031 | 0.9303 | -0.05474 | -0.05521 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05806 | 0.03689 | 0.9615 | -0.02357 | -0.02398 |
| `twise_t2` | 65 | 0.05642 | 0.06466 | 0.05035 | 0.9497 | -0.03542 | -0.03727 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.05571 | 0.001736 | 0.9966 | 0.01155 | 0.01173 |
| `random_t3` | 212 | 0.184 | 0.1844 | 0.003472 | 0.9949 | -0.0003879 | -0.0003973 |
| `solverBased_t3` | 212 | 0.184 | 0.1844 | 0.005208 | 0.9872 | -0.008096 | -0.008107 |
| `henard_t3` | 212 | 0.184 | 0.1385 | 0.009549 | 0.9899 | -0.00544 | -0.003923 |
| `distBased_t3` | 212 | 0.184 | 0.194 | 0.007812 | 0.9898 | -0.005544 | -0.005781 |
| `divDistBased_t3` | 212 | 0.184 | 0.1836 | 0.003472 | 0.9922 | -0.003148 | -0.003138 |
| `twise_t3` | 212 | 0.184 | 0.2032 | 0.01476 | 0.9852 | -0.01008 | -0.01052 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1831 | 0 | 0.9989 | 0.003614 | 0.003637 |
