# x264_size_12 FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1152 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `henard_t3` (risk 0, %cost 0.144).

Best integrated confidence after normalizing the prior baseline by empirical cost: `henard_t1` (omega_cost 0.0487, %cost 0.009665).

Empirical cost/confidence Pareto front:

- `henard_t1`: posterior area 0.9726, risk 0.02778, %cost 0.009665, omega_cost 0.0487
- `random_t2`: posterior area 0.9857, risk 0.008681, %cost 0.05653, omega_cost 0.0006183
- `henard_t2`: posterior area 0.9753, risk 0.02778, %cost 0.04492, omega_cost -0.00608
- `SRSSampling_t2`: posterior area 0.9945, risk 0.001736, %cost 0.05851, omega_cost 0.008861
- `henard_t3`: posterior area 0.9997, risk 0, %cost 0.144, omega_cost 0.005611

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `x264_size_12:t1` | `supports` | 335 | 2.62e-69 | large (0.4747) | median risks: random=0.05078, solverBased=0.1372, henard=0.02778, distBased=0.08681, divDistBased=0.09375, twise=0.1293, SRSSampling=0.05816; spread=0.1094 |
| `FSE1` | `x264_size_12:t2` | `supports` | 375.8 | 4.40e-78 | large (0.5337) | median risks: random=0.008681, solverBased=0.05208, henard=0.02778, distBased=0.02604, divDistBased=0.0816, twise=0.006944, SRSSampling=0.001736; spread=0.07986 |
| `FSE1` | `x264_size_12:t3` | `supports` | 489.2 | 1.74e-102 | large (0.6973) | median risks: random=0.001736, solverBased=0.05208, henard=0, distBased=0.001736, divDistBased=0.006944, twise=0.006944, SRSSampling=0; spread=0.05208 |
| `FSE2` | `x264_size_12:t1` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t1; best cost-normalized=henard_t1 |
| `FSE3` | `x264_size_12:t1` | `refutes` | 0 |  | large (0.05795) | best cost-normalized=henard_t1; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_12:t1` | `refutes` | 1 |  | same frontier (0) | count front=henard_t1; empirical front=henard_t1 |
| `FSE5` | `x264_size_12:t1` | `refutes` | 4626 | 0.679 | negligible (0.5374) | A12<0.5 means SRS risks tend to be lower; median SRS=0.05816, median random=0.05078 |
| `FSE6` | `x264_size_12:t1` | `inconclusive` | 4360 | 0.288 | small (0.5639) | A12>0.5 means SRS costs tend to be higher; median SRS=0.01049, median random=0.0103 |
| `FSE2` | `x264_size_12:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `x264_size_12:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `x264_size_12:t2` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,henard_t2,random_t2 |
| `FSE5` | `x264_size_12:t2` | `supports` | 2333 | 1.23e-09 | large (0.2333) | A12<0.5 means SRS risks tend to be lower; median SRS=0.001736, median random=0.008681 |
| `FSE6` | `x264_size_12:t2` | `supports` | 2358 | 2.59e-09 | large (0.7642) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05851, median random=0.05653 |
| `FSE2` | `x264_size_12:t3` | `refutes` | 0 |  | unchanged (0) | best size-normalized=henard_t3; best cost-normalized=henard_t3 |
| `FSE3` | `x264_size_12:t3` | `refutes` | 0 |  | moderate (0.001592) | best cost-normalized=henard_t3; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `x264_size_12:t3` | `refutes` | 1 |  | same frontier (0) | count front=henard_t3; empirical front=henard_t3 |
| `FSE5` | `x264_size_12:t3` | `supports` | 2427 | 4.30e-11 | large (0.2427) | A12<0.5 means SRS risks tend to be lower; median SRS=0, median random=0.001736 |
| `FSE6` | `x264_size_12:t3` | `supports` | 3607 | 0.00369 | small (0.6393) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1859, median random=0.1844 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t1` | 12 | 0.01042 | 0.0103 | 0.05078 | 0.924 | -0.004587 | -0.003923 |
| `solverBased_t1` | 12 | 0.01042 | 0.0109 | 0.1372 | 0.8334 | -0.09518 | -0.09793 |
| `henard_t1` | 12 | 0.01042 | 0.009665 | 0.02778 | 0.9726 | 0.044 | 0.0487 |
| `distBased_t1` | 12 | 0.01042 | 0.01006 | 0.08681 | 0.9033 | -0.02532 | -0.02315 |
| `divDistBased_t1` | 12 | 0.01042 | 0.01049 | 0.09375 | 0.8962 | -0.03235 | -0.03275 |
| `twise_t1` | 12 | 0.01042 | 0.01255 | 0.1293 | 0.8707 | -0.05791 | -0.0686 |
| `SRSSampling_t1` | 12 | 0.01042 | 0.01049 | 0.05816 | 0.9197 | -0.008841 | -0.009243 |
| `random_t2` | 65 | 0.05642 | 0.05653 | 0.008681 | 0.9857 | 0.0006459 | 0.0006183 |
| `solverBased_t2` | 65 | 0.05642 | 0.05731 | 0.05208 | 0.932 | -0.05312 | -0.05335 |
| `henard_t2` | 65 | 0.05642 | 0.04492 | 0.02778 | 0.9753 | -0.009762 | -0.00608 |
| `distBased_t2` | 65 | 0.05642 | 0.0591 | 0.02604 | 0.9617 | -0.02342 | -0.02407 |
| `divDistBased_t2` | 65 | 0.05642 | 0.05836 | 0.0816 | 0.9373 | -0.04775 | -0.04823 |
| `twise_t2` | 65 | 0.05642 | 0.0647 | 0.006944 | 0.9931 | 0.007981 | 0.006121 |
| `SRSSampling_t2` | 65 | 0.05642 | 0.05851 | 0.001736 | 0.9945 | 0.009378 | 0.008861 |
| `random_t3` | 212 | 0.184 | 0.1844 | 0.001736 | 0.9958 | 0.0004889 | 0.0004785 |
| `solverBased_t3` | 212 | 0.184 | 0.1883 | 0.05208 | 0.9454 | -0.04993 | -0.05003 |
| `henard_t3` | 212 | 0.184 | 0.144 | 0 | 0.9997 | 0.004326 | 0.005611 |
| `distBased_t3` | 212 | 0.184 | 0.1948 | 0.001736 | 0.996 | 0.0007059 | 0.0004487 |
| `divDistBased_t3` | 212 | 0.184 | 0.1845 | 0.006944 | 0.9952 | -8.405e-05 | -9.527e-05 |
| `twise_t3` | 212 | 0.184 | 0.2029 | 0.006944 | 0.9931 | -0.002272 | -0.002702 |
| `SRSSampling_t3` | 212 | 0.184 | 0.1859 | 0 | 0.9994 | 0.004065 | 0.004019 |
