# x264_size_9 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `divDistBased_t2` (risk 0, %cost 0.05783).

Best integrated confidence after normalizing the prior baseline by empirical cost: `divDistBased_t1` (omega_cost 0.03469, %cost 0.009978).

Empirical cost/confidence Pareto front:

- `henard_t1`: posterior area 0.7034, risk 0.2951, %cost 0.008115, omega_cost -0.2085
- `distBased_t1`: posterior area 0.9436, risk 0.02604, %cost 0.00951, omega_cost 0.02077
- `divDistBased_t1`: posterior area 0.9606, risk 0.02083, %cost 0.009978, omega_cost 0.03469
- `henard_t2`: posterior area 0.9948, risk 0.005208, %cost 0.04043, omega_cost 0.01538
- `SRSSampling_t2`: posterior area 0.9989, risk 0, %cost 0.05251, omega_cost 0.01491
- `henard_t3`: posterior area 1, risk 0, %cost 0.1302, omega_cost 0.006581

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_9:t1` | `supports` | 435.3 | 7.25e-91 | large (0.6194) | median risks: random=0.04948, solverBased=0.08854, henard=0.2951, distBased=0.02604, divDistBased=0.02083, twise=0.4271, SRSSampling=0.0638; spread=0.4062 |
| `FSE1` | `x264_size_9:t2` | `supports` | 587.9 | 9.53e-124 | large (0.8397) | median risks: random=0.01042, solverBased=0.05339, henard=0.005208, distBased=0.02083, divDistBased=0, twise=0.2101, SRSSampling=0; spread=0.2101 |
| `FSE1` | `x264_size_9:t3` | `supports` | 613.6 | 2.66e-129 | large (0.8768) | median risks: random=0, solverBased=0.04167, henard=0, distBased=0, divDistBased=0, twise=0.07031, SRSSampling=0; spread=0.07031 |
| `FSE2` | `x264_size_9:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=divDistBased_t1; best cost-normalized=divDistBased_t1 |
| `FSE3` | `x264_size_9:t1` | `refutes` | 0 |  | large (0.05567) | best cost-normalized=divDistBased_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_9:t1` | `supports` | 0.3333 |  | large frontier change (2) | count front=divDistBased_t1; empirical front=distBased_t1,divDistBased_t1,henard_t1 |
| `FSE5` | `x264_size_9:t1` | `inconclusive` | 4233 | 0.169 | small (0.5767) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0638, median random=0.04948 |
| `FSE6` | `x264_size_9:t1` | `inconclusive` | 4174 | 0.129 | small (0.5826) | A12>0.5 means SRS costs tend to be higher; median SRS=0.0106, median random=0.01022 |
| `FSE2` | `x264_size_9:t2` | `supports` | 1 |  | changed (0.0004679) | best size-normalized=SRSSampling_t2; best cost-normalized=henard_t2 |
| `FSE3` | `x264_size_9:t2` | `refutes` | 0 |  | small (0.0004679) | best cost-normalized=henard_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_9:t2` | `supports` | 0.5 |  | frontier change (1) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,henard_t2 |
| `FSE5` | `x264_size_9:t2` | `supports` | 1968 | 2.54e-15 | large (0.1968) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.01042 |
| `FSE6` | `x264_size_9:t2` | `supports` | 966 | 8.23e-21 | large (0.0966) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05251, median random=0.05652 |
| `FSE2` | `x264_size_9:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t3; best cost-normalized=henard_t3 |
| `FSE3` | `x264_size_9:t3` | `refutes` | 0 |  | moderate (0.00189) | best cost-normalized=henard_t3; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_9:t3` | `supports` | 0.5 |  | frontier change (1) | count front=divDistBased_t3,henard_t3; empirical front=henard_t3 |
| `FSE5` | `x264_size_9:t3` | `supports` | 3334 | 3.41e-08 | medium (0.3334) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0 |
| `FSE6` | `x264_size_9:t3` | `supports` | 1533 | 1.57e-15 | large (0.1533) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1793, median random=0.184 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.01022 | 0.04948 | 0.9278 | -0.000785 | 0.0003637 |
| `solverBased_t1` | 12 | 0.01042 | 0.009702 | 0.08854 | 0.7624 | -0.1662 | -0.1617 |
| `henard_t1` | 12 | 0.01042 | 0.008115 | 0.2951 | 0.7034 | -0.2252 | -0.2085 |
| `distBased_t1` | 12 | 0.01042 | 0.00951 | 0.02604 | 0.9436 | 0.01501 | 0.02077 |
| `divDistBased_t1` | 12 | 0.01042 | 0.009978 | 0.02083 | 0.9606 | 0.03202 | 0.03469 |
| `twise_t1` | 12 | 0.01042 | 0.01059 | 0.4271 | 0.5729 | -0.3557 | -0.3566 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.0106 | 0.0638 | 0.9086 | -0.01994 | -0.02098 |
| `random_t2` | 65 | 0.05642 | 0.05652 | 0.01042 | 0.9875 | 0.002451 | 0.002427 |
| `solverBased_t2` | 65 | 0.05642 | 0.05231 | 0.05339 | 0.94 | -0.04507 | -0.04394 |
| `henard_t2` | 65 | 0.05642 | 0.04043 | 0.005208 | 0.9948 | 0.009717 | 0.01538 |
| `distBased_t2` | 65 | 0.05642 | 0.05671 | 0.02083 | 0.981 | -0.004085 | -0.004159 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05783 | 0 | 0.9981 | 0.01305 | 0.0127 |
| `twise_t2` | 65 | 0.05642 | 0.05709 | 0.2101 | 0.7899 | -0.1951 | -0.1953 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.05251 | 0 | 0.9989 | 0.01383 | 0.01491 |
| `random_t3` | 212 | 0.184 | 0.184 | 0 | 0.9967 | 0.001392 | 0.001392 |
| `solverBased_t3` | 212 | 0.184 | 0.1729 | 0.04167 | 0.9467 | -0.04866 | -0.04836 |
| `henard_t3` | 212 | 0.184 | 0.1302 | 0 | 1 | 0.004673 | 0.006581 |
| `distBased_t3` | 212 | 0.184 | 0.1881 | 0 | 0.9991 | 0.003787 | 0.003688 |
| `divDistBased_t3` | 212 | 0.184 | 0.183 | 0 | 1 | 0.004673 | 0.0047 |
| `twise_t3` | 212 | 0.184 | 0.1859 | 0.07031 | 0.9297 | -0.06564 | -0.06569 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1793 | 0 | 0.9999 | 0.004569 | 0.004691 |
