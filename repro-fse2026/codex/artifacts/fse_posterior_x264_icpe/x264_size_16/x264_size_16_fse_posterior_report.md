# x264_size_16 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t2` (risk 0, %cost 0.0564).

Best integrated confidence after normalizing the prior baseline by empirical cost: `henard_t1` (omega_cost 0.05495, %cost 0.008876).

Empirical cost/confidence Pareto front:

- `henard_t1`: posterior area 0.9732, risk 0.02604, %cost 0.008876, omega_cost 0.05495
- `henard_t2`: posterior area 0.9792, risk 0.02083, %cost 0.04282, omega_cost -0.001352
- `SRSSampling_t2`: posterior area 0.9981, risk 0, %cost 0.0564, omega_cost 0.01303
- `SRSSampling_t3`: posterior area 0.9994, risk 0, %cost 0.1838, omega_cost 0.004036

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_16:t1` | `supports` | 261 | 1.81e-53 | large (0.368) | median risks: random=0.05339, solverBased=0.08681, henard=0.02604, distBased=0.1398, divDistBased=0.1016, twise=0.09201, SRSSampling=0.05035; spread=0.1137 |
| `FSE1` | `x264_size_16:t2` | `supports` | 386.8 | 1.93e-80 | moderate (0.5495) | median risks: random=0.01042, solverBased=0.04427, henard=0.02083, distBased=0.0408, divDistBased=0.04253, twise=0.0408, SRSSampling=0; spread=0.04427 |
| `FSE1` | `x264_size_16:t3` | `supports` | 378.4 | 1.22e-78 | moderate (0.5374) | median risks: random=0.001736, solverBased=0.02778, henard=0.001736, distBased=0.008681, divDistBased=0.006944, twise=0.005208, SRSSampling=0; spread=0.02778 |
| `FSE2` | `x264_size_16:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t1; best cost-normalized=henard_t1 |
| `FSE3` | `x264_size_16:t1` | `refutes` | 0 |  | large (0.06146) | best cost-normalized=henard_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_16:t1` | `refutes` | 1 |  | same frontier (0) | count front=henard_t1; empirical front=henard_t1 |
| `FSE5` | `x264_size_16:t1` | `refutes` | 4961 | 0.686 | negligible (0.4961) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05035, median random=0.05339 |
| `FSE6` | `x264_size_16:t1` | `inconclusive` | 4165 | 0.124 | small (0.5835) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01054, median random=0.01019 |
| `FSE2` | `x264_size_16:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_size_16:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_16:t2` | `supports` | 0.5 |  | frontier change (1) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,henard_t2 |
| `FSE5` | `x264_size_16:t2` | `supports` | 1864 | 1.39e-13 | large (0.1865) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.01042 |
| `FSE6` | `x264_size_16:t2` | `refutes` | 4591 | 0.618 | negligible (0.4591) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0564, median random=0.05647 |
| `FSE2` | `x264_size_16:t3` | `supports` | 1 |  | changed (0.0003072) | best size-normalized=SRSSampling_t3; best cost-normalized=henard_t3 |
| `FSE3` | `x264_size_16:t3` | `refutes` | 0 |  | small (0.0003072) | best cost-normalized=henard_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_16:t3` | `supports` | 0.5 |  | frontier change (1) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,henard_t3 |
| `FSE5` | `x264_size_16:t3` | `supports` | 2809 | 2.29e-08 | large (0.2809) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.001736 |
| `FSE6` | `x264_size_16:t3` | `inconclusive` | 4384 | 0.315 | small (0.4384) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1838, median random=0.184 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01019 | 0.05339 | 0.9203 | -0.008276 | -0.006915 |
| `solverBased_t1` | 12 | 0.01042 | 0.01042 | 0.08681 | 0.8551 | -0.07348 | -0.07349 |
| `henard_t1` | 12 | 0.01042 | 0.008876 | 0.02604 | 0.9732 | 0.04458 | 0.05495 |
| `distBased_t1` | 12 | 0.01042 | 0.009717 | 0.1398 | 0.8603 | -0.06827 | -0.0639 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01016 | 0.1016 | 0.8962 | -0.03233 | -0.03078 |
| `twise_t1` | 12 | 0.01042 | 0.01161 | 0.09201 | 0.908 | -0.02059 | -0.02698 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01054 | 0.05035 | 0.9228 | -0.005794 | -0.006508 |
| `random_t2` | 65 | 0.05642 | 0.05647 | 0.01042 | 0.9857 | 0.0006719 | 0.0006599 |
| `solverBased_t2` | 65 | 0.05642 | 0.0554 | 0.04427 | 0.955 | -0.03006 | -0.02979 |
| `henard_t2` | 65 | 0.05642 | 0.04282 | 0.02083 | 0.9792 | -0.005908 | -0.001352 |
| `distBased_t2` | 65 | 0.05642 | 0.05772 | 0.0408 | 0.9401 | -0.04501 | -0.04534 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05828 | 0.04253 | 0.9598 | -0.02523 | -0.02569 |
| `twise_t2` | 65 | 0.05642 | 0.06127 | 0.0408 | 0.9592 | -0.02587 | -0.02702 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.0564 | 0 | 0.9981 | 0.01302 | 0.01303 |
| `random_t3` | 212 | 0.184 | 0.184 | 0.001736 | 0.9961 | 0.0008187 | 0.0008198 |
| `solverBased_t3` | 212 | 0.184 | 0.1824 | 0.02778 | 0.9733 | -0.02203 | -0.02199 |
| `henard_t3` | 212 | 0.184 | 0.1371 | 0.001736 | 0.9981 | 0.002763 | 0.004343 |
| `distBased_t3` | 212 | 0.184 | 0.1911 | 0.008681 | 0.9921 | -0.003192 | -0.003362 |
| `divDistBased_t3` | 212 | 0.184 | 0.1838 | 0.006944 | 0.9914 | -0.003895 | -0.00389 |
| `twise_t3` | 212 | 0.184 | 0.1953 | 0.005208 | 0.9948 | -0.0005354 | -0.0008021 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1838 | 0 | 0.9994 | 0.004031 | 0.004036 |
