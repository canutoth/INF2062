# x264_size_7 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.1865).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t2` (omega_cost 0.011, %cost 0.05805).

Empirical cost/confidence Pareto front:

- `random_t1`: posterior area 0.9197, risk 0.05642, %cost 0.01023, omega_cost -0.007715
- `henard_t1`: posterior area 0.8604, risk 0.1406, %cost 0.008543, omega_cost -0.05518
- `distBased_t1`: posterior area 0.8694, risk 0.1016, %cost 0.009535, omega_cost -0.05361
- `divDistBased_t1`: posterior area 0.9086, risk 0.07639, %cost 0.009933, omega_cost -0.01701
- `twise_t1`: posterior area 0.934, risk 0.06597, %cost 0.01099, omega_cost 0.002229
- `random_t2`: posterior area 0.9857, risk 0.008681, %cost 0.05653, omega_cost 0.0006189
- `distBased_t2`: posterior area 0.9429, risk 0.07118, %cost 0.05616, omega_cost -0.04213
- `SRSSampling_t2`: posterior area 0.9965, risk 0.0008681, %cost 0.05805, omega_cost 0.011
- `SRSSampling_t3`: posterior area 0.9993, risk 0, %cost 0.1865, omega_cost 0.003881

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_7:t1` | `supports` | 329.8 | 3.37e-68 | large (0.4672) | median risks: random=0.05642, solverBased=0.1797, henard=0.1406, distBased=0.1016, divDistBased=0.07639, twise=0.06597, SRSSampling=0.06163; spread=0.1233 |
| `FSE1` | `x264_size_7:t2` | `supports` | 524.9 | 3.62e-110 | large (0.7488) | median risks: random=0.008681, solverBased=0.1276, henard=0.1311, distBased=0.07118, divDistBased=0.01476, twise=0.02865, SRSSampling=0.0008681; spread=0.1302 |
| `FSE1` | `x264_size_7:t3` | `supports` | 450.2 | 4.40e-94 | moderate (0.641) | median risks: random=0.001736, solverBased=0.01649, henard=0.01997, distBased=0.005208, divDistBased=0.003472, twise=0.01215, SRSSampling=0; spread=0.01997 |
| `FSE2` | `x264_size_7:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=twise_t1; best cost-normalized=twise_t1 |
| `FSE3` | `x264_size_7:t1` | `refutes` | 0 |  | large (0.01205) | best cost-normalized=twise_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_7:t1` | `supports` | 0.2 |  | large frontier change (4) | count front=twise_t1; empirical front=distBased_t1,divDistBased_t1,henard_t1,random_t1,twise_t1 |
| `FSE5` | `x264_size_7:t1` | `refutes` | 4826 | 0.939 | negligible (0.5173) | A12<0.5 means SRS risks tend to be lower; median SRS=0.06163, median random=0.05642 |
| `FSE6` | `x264_size_7:t1` | `inconclusive` | 4246 | 0.179 | small (0.5754) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01055, median random=0.01023 |
| `FSE2` | `x264_size_7:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_size_7:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_7:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,distBased_t2,henard_t2,random_t2 |
| `FSE5` | `x264_size_7:t2` | `supports` | 1668 | 1.10e-14 | large (0.1668) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0008681, median random=0.008681 |
| `FSE6` | `x264_size_7:t2` | `supports` | 2987 | 9.94e-06 | medium (0.7013) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05805, median random=0.05653 |
| `FSE2` | `x264_size_7:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_size_7:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_7:t3` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3,random_t3 |
| `FSE5` | `x264_size_7:t3` | `supports` | 1884 | 7.44e-14 | large (0.1885) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.001736 |
| `FSE6` | `x264_size_7:t3` | `supports` | 3670 | 0.00596 | small (0.633) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1865, median random=0.1839 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01023 | 0.05642 | 0.9197 | -0.008823 | -0.007715 |
| `solverBased_t1` | 12 | 0.01042 | 0.009826 | 0.1797 | 0.7563 | -0.1723 | -0.1686 |
| `henard_t1` | 12 | 0.01042 | 0.008543 | 0.1406 | 0.8604 | -0.0682 | -0.05518 |
| `distBased_t1` | 12 | 0.01042 | 0.009535 | 0.1016 | 0.8694 | -0.0592 | -0.05361 |
| `divDistBased_t1` | 12 | 0.01042 | 0.009933 | 0.07639 | 0.9086 | -0.01997 | -0.01701 |
| `twise_t1` | 12 | 0.01042 | 0.01099 | 0.06597 | 0.934 | 0.005456 | 0.002229 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01055 | 0.06163 | 0.9195 | -0.009075 | -0.009823 |
| `random_t2` | 65 | 0.05642 | 0.05653 | 0.008681 | 0.9857 | 0.0006459 | 0.0006189 |
| `solverBased_t2` | 65 | 0.05642 | 0.05281 | 0.1276 | 0.8726 | -0.1125 | -0.1115 |
| `henard_t2` | 65 | 0.05642 | 0.04206 | 0.1311 | 0.882 | -0.1031 | -0.09819 |
| `distBased_t2` | 65 | 0.05642 | 0.05616 | 0.07118 | 0.9429 | -0.04219 | -0.04213 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05737 | 0.01476 | 0.9774 | -0.007714 | -0.007952 |
| `twise_t2` | 65 | 0.05642 | 0.05863 | 0.02865 | 0.9714 | -0.01372 | -0.01427 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.05805 | 0.0008681 | 0.9965 | 0.0114 | 0.011 |
| `random_t3` | 212 | 0.184 | 0.1839 | 0.001736 | 0.9964 | 0.001027 | 0.00103 |
| `solverBased_t3` | 212 | 0.184 | 0.1754 | 0.01649 | 0.9609 | -0.03442 | -0.0342 |
| `henard_t3` | 212 | 0.184 | 0.1357 | 0.01997 | 0.9799 | -0.01538 | -0.01374 |
| `distBased_t3` | 212 | 0.184 | 0.1862 | 0.005208 | 0.991 | -0.004355 | -0.00441 |
| `divDistBased_t3` | 212 | 0.184 | 0.1831 | 0.003472 | 0.9937 | -0.001664 | -0.001639 |
| `twise_t3` | 212 | 0.184 | 0.1892 | 0.01215 | 0.9878 | -0.00748 | -0.007607 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1865 | 0 | 0.9993 | 0.003944 | 0.003881 |
