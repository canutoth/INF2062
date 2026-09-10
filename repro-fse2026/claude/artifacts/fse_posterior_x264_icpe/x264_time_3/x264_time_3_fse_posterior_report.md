# x264_time_3 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.204).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t2` (omega_cost 0.009137, %cost 0.07049).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9269, risk 0.05816, %cost 0.01037, omega_cost -0.001423
- `henard_t1`: posterior area 0.7497, risk 0.2292, %cost 0.00795, omega_cost -0.1607
- `distBased_t1`: posterior area 0.8606, risk 0.08247, %cost 0.009613, omega_cost -0.06292
- `divDistBased_t1`: posterior area 0.9044, risk 0.05903, %cost 0.01004, omega_cost -0.02186
- `SRSSampling_t1`: posterior area 0.9372, risk 0.03819, %cost 0.01049, omega_cost 0.008206
- `random_t2`: posterior area 0.987, risk 0.01042, %cost 0.05645, omega_cost 0.001898
- `distBased_t2`: posterior area 0.9624, risk 0.03125, %cost 0.05609, omega_cost -0.02257
- `SRSSampling_t2`: posterior area 0.9971, risk 0.001736, %cost 0.07049, omega_cost 0.009137
- `twise_t3`: posterior area 0.9974, risk 0.002604, %cost 0.1879, omega_cost 0.001974
- `SRSSampling_t3`: posterior area 0.9995, risk 0, %cost 0.204, omega_cost 0.003725

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_time_3:t1` | `supports` | 247.2 | 1.64e-50 | large (0.348) | median risks: random=0.05816, solverBased=0.3273, henard=0.2292, distBased=0.08247, divDistBased=0.05903, twise=0.1571, SRSSampling=0.03819; spread=0.2891 |
| `FSE1` | `x264_time_3:t2` | `supports` | 494.2 | 1.48e-103 | large (0.7045) | median risks: random=0.01042, solverBased=0.1345, henard=0.1571, distBased=0.03125, divDistBased=0.03559, twise=0.05208, SRSSampling=0.001736; spread=0.1554 |
| `FSE1` | `x264_time_3:t3` | `supports` | 472.4 | 7.29e-99 | large (0.6731) | median risks: random=0.002604, solverBased=0.1259, henard=0.1571, distBased=0.0191, divDistBased=0.008681, twise=0.002604, SRSSampling=0; spread=0.1571 |
| `FSE2` | `x264_time_3:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t1; best cost-normalized=SRSSampling_t1 |
| `FSE3` | `x264_time_3:t1` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t1; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_3:t1` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t1; empirical front=SRSSampling_t1,distBased_t1,divDistBased_t1,henard_t1,random_t1 |
| `FSE5` | `x264_time_3:t1` | `refutes` | 4406 | 0.342 | negligible (0.4406) | A12<0.5 means SRS risks tend to be lower; median SRS=0.03819, median random=0.05816 |
| `FSE6` | `x264_time_3:t1` | `inconclusive` | 4392 | 0.324 | small (0.5608) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01049, median random=0.01037 |
| `FSE2` | `x264_time_3:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_time_3:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_3:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,distBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_time_3:t2` | `supports` | 1662 | 1.44e-14 | large (0.1662) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001736, median random=0.01042 |
| `FSE6` | `x264_time_3:t2` | `supports` | 9 | 1.35e-31 | large (0.9991) | A12>0.5 means SRS costs tend to be higher; median SRS=0.07049, median random=0.05645 |
| `FSE2` | `x264_time_3:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_time_3:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_time_3:t3` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3,random_t3,twise_t3 |
| `FSE5` | `x264_time_3:t3` | `supports` | 1402 | 3.31e-18 | large (0.1401) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.002604 |
| `FSE6` | `x264_time_3:t3` | `supports` | 24 | 2.08e-31 | large (0.9976) | A12>0.5 means SRS costs tend to be higher; median SRS=0.204, median random=0.1842 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01037 | 0.05816 | 0.9269 | -0.001714 | -0.001423 |
| `solverBased_t1` | 12 | 0.01042 | 0.01034 | 0.3273 | 0.7645 | -0.1641 | -0.1637 |
| `henard_t1` | 12 | 0.01042 | 0.00795 | 0.2292 | 0.7497 | -0.1789 | -0.1607 |
| `distBased_t1` | 12 | 0.01042 | 0.009613 | 0.08247 | 0.8606 | -0.06797 | -0.06292 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01004 | 0.05903 | 0.9044 | -0.02416 | -0.02186 |
| `twise_t1` | 12 | 0.01042 | 0.01056 | 0.1571 | 0.8429 | -0.08569 | -0.08653 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01049 | 0.03819 | 0.9372 | 0.008607 | 0.008206 |
| `random_t2` | 65 | 0.05642 | 0.05645 | 0.01042 | 0.987 | 0.001905 | 0.001898 |
| `solverBased_t2` | 65 | 0.05642 | 0.0563 | 0.1345 | 0.9006 | -0.08448 | -0.08445 |
| `henard_t2` | 65 | 0.05642 | 0.0415 | 0.1571 | 0.8006 | -0.1845 | -0.1793 |
| `distBased_t2` | 65 | 0.05642 | 0.05609 | 0.03125 | 0.9624 | -0.02265 | -0.02257 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05705 | 0.03559 | 0.9727 | -0.01235 | -0.01251 |
| `twise_t2` | 65 | 0.05642 | 0.05783 | 0.05208 | 0.9479 | -0.03716 | -0.03751 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.07049 | 0.001736 | 0.9971 | 0.01204 | 0.009137 |
| `random_t3` | 212 | 0.184 | 0.1842 | 0.002604 | 0.9961 | 0.00081 | 0.0008069 |
| `solverBased_t3` | 212 | 0.184 | 0.1858 | 0.1259 | 0.9128 | -0.08253 | -0.08258 |
| `henard_t3` | 212 | 0.184 | 0.1333 | 0.1571 | 0.82 | -0.1753 | -0.1735 |
| `distBased_t3` | 212 | 0.184 | 0.1851 | 0.0191 | 0.982 | -0.01329 | -0.01331 |
| `divDistBased_t3` | 212 | 0.184 | 0.1812 | 0.008681 | 0.992 | -0.003374 | -0.003302 |
| `twise_t3` | 212 | 0.184 | 0.1879 | 0.002604 | 0.9974 | 0.002069 | 0.001974 |
| `SRSSampling_t3` | 212 | 0.184 | 0.204 | 0 | 0.9995 | 0.004178 | 0.003725 |
