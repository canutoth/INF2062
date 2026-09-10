# x264_size_5 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t3` (risk 0, %cost 0.1877).

Best integrated confidence after normalizing the prior baseline by empirical cost: `henard_t1` (omega_cost 0.02541, %cost 0.009255).

Empirical cost/confidence Pareto front:

- `henard_t1`: posterior area 0.9464, risk 0.05295, %cost 0.009255, omega_cost 0.02541
- `random_t2`: posterior area 0.9852, risk 0.01215, %cost 0.05651, omega_cost 0.0001212
- `solverBased_t2`: posterior area 0.9833, risk 0.009115, %cost 0.0565, omega_cost -0.001795
- `henard_t2`: posterior area 0.9531, risk 0.04688, %cost 0.04311, omega_cost -0.02752
- `SRSSampling_t2`: posterior area 0.9934, risk 0.002604, %cost 0.05889, omega_cost 0.007721
- `random_t3`: posterior area 0.9953, risk 0.003472, %cost 0.1842, omega_cost -7.962e-05
- `SRSSampling_t3`: posterior area 0.9986, risk 0, %cost 0.1877, omega_cost 0.00315

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_5:t1` | `supports` | 270.3 | 1.89e-55 | large (0.3814) | median risks: random=0.05165, solverBased=0.09201, henard=0.05295, distBased=0.1762, divDistBased=0.105, twise=0.1102, SRSSampling=0.05252; spread=0.1246 |
| `FSE1` | `x264_size_5:t2` | `supports` | 457.7 | 1.06e-95 | large (0.6519) | median risks: random=0.01215, solverBased=0.009115, henard=0.04688, distBased=0.07205, divDistBased=0.08681, twise=0.03125, SRSSampling=0.002604; spread=0.0842 |
| `FSE1` | `x264_size_5:t3` | `supports` | 430.8 | 6.65e-90 | moderate (0.613) | median risks: random=0.003472, solverBased=0.003472, henard=0.02083, distBased=0.02344, divDistBased=0.003472, twise=0.002604, SRSSampling=0; spread=0.02344 |
| `FSE2` | `x264_size_5:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t1; best cost-normalized=henard_t1 |
| `FSE3` | `x264_size_5:t1` | `refutes` | 0 |  | large (0.03172) | best cost-normalized=henard_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_5:t1` | `refutes` | 1 |  | same frontier (0) | count front=henard_t1; empirical front=henard_t1 |
| `FSE5` | `x264_size_5:t1` | `refutes` | 4882 | 0.831 | negligible (0.4883) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05252, median random=0.05165 |
| `FSE6` | `x264_size_5:t1` | `inconclusive` | 4332 | 0.258 | small (0.5668) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01056, median random=0.01022 |
| `FSE2` | `x264_size_5:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_size_5:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_5:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,henard_t2,random_t2,solverBased_t2 |
| `FSE5` | `x264_size_5:t2` | `supports` | 2455 | 1.02e-08 | large (0.2455) | A12<0.5 means SRS risks tend to be lower; median SRS=0.002604, median random=0.01215 |
| `FSE6` | `x264_size_5:t2` | `supports` | 2117 | 5.98e-11 | large (0.7883) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05889, median random=0.05651 |
| `FSE2` | `x264_size_5:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t3; best cost-normalized=SRSSampling_t3 |
| `FSE3` | `x264_size_5:t3` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_5:t3` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t3; empirical front=SRSSampling_t3,divDistBased_t3,henard_t3,random_t3 |
| `FSE5` | `x264_size_5:t3` | `supports` | 2036 | 3.33e-12 | large (0.2036) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.003472 |
| `FSE6` | `x264_size_5:t3` | `supports` | 2742 | 5.24e-07 | large (0.7258) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1877, median random=0.1842 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01022 | 0.05165 | 0.9181 | -0.01045 | -0.009269 |
| `solverBased_t1` | 12 | 0.01042 | 0.01097 | 0.09201 | 0.8522 | -0.07642 | -0.07955 |
| `henard_t1` | 12 | 0.01042 | 0.009255 | 0.05295 | 0.9464 | 0.01786 | 0.02541 |
| `distBased_t1` | 12 | 0.01042 | 0.009851 | 0.1762 | 0.8286 | -0.1 | -0.09652 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01033 | 0.105 | 0.877 | -0.05162 | -0.05108 |
| `twise_t1` | 12 | 0.01042 | 0.01261 | 0.1102 | 0.8898 | -0.03881 | -0.04975 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01056 | 0.05252 | 0.9231 | -0.005464 | -0.006304 |
| `random_t2` | 65 | 0.05642 | 0.05651 | 0.01215 | 0.9852 | 0.0001424 | 0.0001212 |
| `solverBased_t2` | 65 | 0.05642 | 0.0565 | 0.009115 | 0.9833 | -0.001776 | -0.001795 |
| `henard_t2` | 65 | 0.05642 | 0.04311 | 0.04688 | 0.9531 | -0.03195 | -0.02752 |
| `distBased_t2` | 65 | 0.05642 | 0.05852 | 0.07205 | 0.9192 | -0.06592 | -0.06644 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05849 | 0.08681 | 0.9385 | -0.04653 | -0.04704 |
| `twise_t2` | 65 | 0.05642 | 0.06528 | 0.03125 | 0.9688 | -0.01632 | -0.0183 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.05889 | 0.002604 | 0.9934 | 0.008328 | 0.007721 |
| `random_t3` | 212 | 0.184 | 0.1842 | 0.003472 | 0.9953 | -7.537e-05 | -7.962e-05 |
| `solverBased_t3` | 212 | 0.184 | 0.1878 | 0.003472 | 0.9943 | -0.0009868 | -0.00108 |
| `henard_t3` | 212 | 0.184 | 0.1385 | 0.02083 | 0.9786 | -0.01672 | -0.01521 |
| `distBased_t3` | 212 | 0.184 | 0.1944 | 0.02344 | 0.9737 | -0.0216 | -0.02185 |
| `divDistBased_t3` | 212 | 0.184 | 0.1835 | 0.003472 | 0.991 | -0.004346 | -0.004334 |
| `twise_t3` | 212 | 0.184 | 0.2045 | 0.002604 | 0.9974 | 0.002069 | 0.001605 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1877 | 0 | 0.9986 | 0.003241 | 0.00315 |
