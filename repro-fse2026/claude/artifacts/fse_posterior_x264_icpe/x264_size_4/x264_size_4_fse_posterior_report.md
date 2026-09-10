# x264_size_4 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `divDistBased_t2` (risk 0, %cost 0.05795).

Best integrated confidence after normalizing the prior baseline by empirical cost: `divDistBased_t1` (omega_cost 0.03503, %cost 0.01023).

Empirical cost/confidence Pareto front:

- `henard_t1`: posterior area 0.4055, risk 0.5929, %cost 0.009266, omega_cost -0.5156
- `distBased_t1`: posterior area 0.9237, risk 0.05208, %cost 0.009858, omega_cost -0.001432
- `divDistBased_t1`: posterior area 0.9625, risk 0.02214, %cost 0.01023, omega_cost 0.03503
- `divDistBased_t2`: posterior area 0.9981, risk 0, %cost 0.05795, omega_cost 0.01267
- `SRSSampling_t2`: posterior area 0.9965, risk 0, %cost 0.05453, omega_cost 0.01189
- `henard_t3`: posterior area 1, risk 0, %cost 0.1421, omega_cost 0.006034

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_4:t1` | `supports` | 524.3 | 4.91e-110 | large (0.7479) | median risks: random=0.04427, solverBased=0.1432, henard=0.5929, distBased=0.05208, divDistBased=0.02214, twise=0.474, SRSSampling=0.0625; spread=0.5707 |
| `FSE1` | `x264_size_4:t2` | `supports` | 565.6 | 6.10e-119 | large (0.8075) | median risks: random=0.005208, solverBased=0.007812, henard=0.0625, distBased=0.03125, divDistBased=0, twise=0.2005, SRSSampling=0; spread=0.2005 |
| `FSE1` | `x264_size_4:t3` | `supports` | 584.5 | 5.09e-123 | large (0.8348) | median risks: random=0, solverBased=0.005208, henard=0, distBased=0, divDistBased=0, twise=0.1016, SRSSampling=0; spread=0.1016 |
| `FSE2` | `x264_size_4:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=divDistBased_t1; best cost-normalized=divDistBased_t1 |
| `FSE3` | `x264_size_4:t1` | `refutes` | 0 |  | large (0.05126) | best cost-normalized=divDistBased_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_4:t1` | `supports` | 0.3333 |  | large frontier change (2) | count front=divDistBased_t1; empirical front=distBased_t1,divDistBased_t1,henard_t1 |
| `FSE5` | `x264_size_4:t1` | `refutes` | 4567 | 0.576 | negligible (0.5433) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0625, median random=0.04427 |
| `FSE6` | `x264_size_4:t1` | `inconclusive` | 4258 | 0.189 | small (0.5742) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01055, median random=0.01027 |
| `FSE2` | `x264_size_4:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=divDistBased_t2; best cost-normalized=divDistBased_t2 |
| `FSE3` | `x264_size_4:t2` | `refutes` | 0 |  | small (0.0007826) | best cost-normalized=divDistBased_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_4:t2` | `supports` | 0.3333 |  | large frontier change (2) | count front=divDistBased_t2; empirical front=SRSSampling_t2,divDistBased_t2,henard_t2 |
| `FSE5` | `x264_size_4:t2` | `supports` | 2738 | 2.88e-08 | large (0.2737) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.005208 |
| `FSE6` | `x264_size_4:t2` | `supports` | 2011 | 1.02e-11 | large (0.2011) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05453, median random=0.0565 |
| `FSE2` | `x264_size_4:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t3; best cost-normalized=henard_t3 |
| `FSE3` | `x264_size_4:t3` | `refutes` | 0 |  | moderate (0.001763) | best cost-normalized=henard_t3; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_4:t3` | `supports` | 0.5 |  | frontier change (1) | count front=divDistBased_t3,henard_t3; empirical front=henard_t3 |
| `FSE5` | `x264_size_4:t3` | `supports` | 3584 | 1.02e-05 | medium (0.3584) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `x264_size_4:t3` | `supports` | 2416 | 6.11e-09 | large (0.2416) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1814, median random=0.1842 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01027 | 0.04427 | 0.9177 | -0.01092 | -0.01002 |
| `solverBased_t1` | 12 | 0.01042 | 0.01047 | 0.1432 | 0.7667 | -0.1618 | -0.1622 |
| `henard_t1` | 12 | 0.01042 | 0.009266 | 0.5929 | 0.4055 | -0.523 | -0.5156 |
| `distBased_t1` | 12 | 0.01042 | 0.009858 | 0.05208 | 0.9237 | -0.004874 | -0.001432 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01023 | 0.02214 | 0.9625 | 0.03389 | 0.03503 |
| `twise_t1` | 12 | 0.01042 | 0.01186 | 0.474 | 0.526 | -0.4025 | -0.4101 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01055 | 0.0625 | 0.9131 | -0.01545 | -0.01623 |
| `random_t2` | 65 | 0.05642 | 0.0565 | 0.005208 | 0.9884 | 0.003363 | 0.003344 |
| `solverBased_t2` | 65 | 0.05642 | 0.0548 | 0.007812 | 0.9842 | -0.000908 | -0.0004785 |
| `henard_t2` | 65 | 0.05642 | 0.04383 | 0.0625 | 0.9375 | -0.04757 | -0.04345 |
| `distBased_t2` | 65 | 0.05642 | 0.05756 | 0.03125 | 0.9746 | -0.01044 | -0.01073 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05795 | 0 | 0.9981 | 0.01305 | 0.01267 |
| `twise_t2` | 65 | 0.05642 | 0.06219 | 0.2005 | 0.7995 | -0.1856 | -0.1869 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.05453 | 0 | 0.9965 | 0.01138 | 0.01189 |
| `random_t3` | 212 | 0.184 | 0.1842 | 0 | 0.9975 | 0.002147 | 0.002144 |
| `solverBased_t3` | 212 | 0.184 | 0.1823 | 0.005208 | 0.9939 | -0.001395 | -0.001351 |
| `henard_t3` | 212 | 0.184 | 0.1421 | 0 | 1 | 0.004673 | 0.006034 |
| `distBased_t3` | 212 | 0.184 | 0.1903 | 0 | 0.9997 | 0.004412 | 0.00426 |
| `divDistBased_t3` | 212 | 0.184 | 0.1835 | 0 | 1 | 0.004673 | 0.004686 |
| `twise_t3` | 212 | 0.184 | 0.1972 | 0.1016 | 0.8984 | -0.09689 | -0.0972 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1814 | 0 | 0.9995 | 0.004204 | 0.004271 |
