# x264_size_14 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `distBased_t2` (risk 0, %cost 0.05905).

Best integrated confidence after normalizing the prior baseline by empirical cost: `henard_t1` (omega_cost 0.06922, %cost 0.008041).

Empirical cost/confidence Pareto front:

- `henard_t1`: posterior area 0.9804, risk 0.008681, %cost 0.008041, omega_cost 0.06922
- `henard_t2`: posterior area 0.9965, risk 0.003472, %cost 0.03618, omega_cost 0.01942
- `henard_t3`: posterior area 0.9982, risk 0.001736, %cost 0.1132, omega_cost 0.005711
- `distBased_t3`: posterior area 0.999, risk 0, %cost 0.1966, omega_cost 0.003387
- `SRSSampling_t3`: posterior area 0.999, risk 0, %cost 0.1783, omega_cost 0.003814

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_14:t1` | `supports` | 318.9 | 7.18e-66 | large (0.4516) | median risks: random=0.05122, solverBased=0.0434, henard=0.008681, distBased=0.008681, divDistBased=0.008681, twise=0.1875, SRSSampling=0.05946; spread=0.1788 |
| `FSE1` | `x264_size_14:t2` | `supports` | 457.1 | 1.48e-95 | large (0.6509) | median risks: random=0.01042, solverBased=0.03038, henard=0.003472, distBased=0, divDistBased=0.008681, twise=0.09201, SRSSampling=0.001736; spread=0.09201 |
| `FSE1` | `x264_size_14:t3` | `supports` | 517.6 | 1.36e-108 | moderate (0.7382) | median risks: random=0.001736, solverBased=0.02431, henard=0.001736, distBased=0, divDistBased=0.003472, twise=0.03472, SRSSampling=0; spread=0.03472 |
| `FSE2` | `x264_size_14:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t1; best cost-normalized=henard_t1 |
| `FSE3` | `x264_size_14:t1` | `refutes` | 0 |  | large (0.07943) | best cost-normalized=henard_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_14:t1` | `refutes` | 1 |  | same frontier (0) | count front=henard_t1; empirical front=henard_t1 |
| `FSE5` | `x264_size_14:t1` | `refutes` | 4800 | 0.99 | negligible (0.52) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05946, median random=0.05122 |
| `FSE6` | `x264_size_14:t1` | `inconclusive` | 4195 | 0.142 | small (0.5805) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01062, median random=0.01014 |
| `FSE2` | `x264_size_14:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t2; best cost-normalized=henard_t2 |
| `FSE3` | `x264_size_14:t2` | `refutes` | 0 |  | moderate (0.009011) | best cost-normalized=henard_t2; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_14:t2` | `refutes` | 1 |  | same frontier (0) | count front=henard_t2; empirical front=henard_t2 |
| `FSE5` | `x264_size_14:t2` | `supports` | 2534 | 2.02e-08 | large (0.2534) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001736, median random=0.01042 |
| `FSE6` | `x264_size_14:t2` | `supports` | 2981 | 9.28e-06 | medium (0.2981) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05435, median random=0.05655 |
| `FSE2` | `x264_size_14:t3` | `supports` | 1 |  | changed (0.002324) | best size-normalized=distBased_t3; best cost-normalized=henard_t3 |
| `FSE3` | `x264_size_14:t3` | `refutes` | 0 |  | moderate (0.001897) | best cost-normalized=henard_t3; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_14:t3` | `supports` | 0.3333 |  | large frontier change (2) | count front=distBased_t3; empirical front=SRSSampling_t3,distBased_t3,henard_t3 |
| `FSE5` | `x264_size_14:t3` | `supports` | 2745 | 2.68e-08 | large (0.2745) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.001736 |
| `FSE6` | `x264_size_14:t3` | `supports` | 2190 | 1.94e-10 | large (0.219) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1783, median random=0.1843 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01014 | 0.05122 | 0.9182 | -0.01034 | -0.008677 |
| `solverBased_t1` | 12 | 0.01042 | 0.01158 | 0.0434 | 0.8012 | -0.1274 | -0.1336 |
| `henard_t1` | 12 | 0.01042 | 0.008041 | 0.008681 | 0.9804 | 0.05186 | 0.06922 |
| `distBased_t1` | 12 | 0.01042 | 0.009452 | 0.008681 | 0.9646 | 0.03607 | 0.04223 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01018 | 0.008681 | 0.9551 | 0.02651 | 0.02791 |
| `twise_t1` | 12 | 0.01042 | 0.01259 | 0.1875 | 0.8125 | -0.1161 | -0.1269 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01062 | 0.05946 | 0.9195 | -0.009066 | -0.01022 |
| `random_t2` | 65 | 0.05642 | 0.05655 | 0.01042 | 0.9847 | -0.0003871 | -0.0004207 |
| `solverBased_t2` | 65 | 0.05642 | 0.05751 | 0.03038 | 0.9451 | -0.03994 | -0.04022 |
| `henard_t2` | 65 | 0.05642 | 0.03618 | 0.003472 | 0.9965 | 0.01145 | 0.01942 |
| `distBased_t2` | 65 | 0.05642 | 0.05905 | 0 | 0.9905 | 0.005464 | 0.00482 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05973 | 0.008681 | 0.9873 | 0.002208 | 0.001405 |
| `twise_t2` | 65 | 0.05642 | 0.06536 | 0.09201 | 0.908 | -0.07709 | -0.07908 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.05435 | 0.001736 | 0.9949 | 0.009856 | 0.01041 |
| `random_t3` | 212 | 0.184 | 0.1843 | 0.001736 | 0.997 | 0.001695 | 0.001689 |
| `solverBased_t3` | 212 | 0.184 | 0.1879 | 0.02431 | 0.9556 | -0.03971 | -0.03981 |
| `henard_t3` | 212 | 0.184 | 0.1132 | 0.001736 | 0.9982 | 0.002833 | 0.005711 |
| `distBased_t3` | 212 | 0.184 | 0.1966 | 0 | 0.999 | 0.003683 | 0.003387 |
| `divDistBased_t3` | 212 | 0.184 | 0.1837 | 0.003472 | 0.9964 | 0.001062 | 0.00107 |
| `twise_t3` | 212 | 0.184 | 0.2051 | 0.03472 | 0.9653 | -0.03005 | -0.03053 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1783 | 0 | 0.999 | 0.003666 | 0.003814 |
