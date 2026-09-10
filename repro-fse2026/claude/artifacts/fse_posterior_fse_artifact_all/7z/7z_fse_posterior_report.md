# 7z FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 68640 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `False`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t2` (risk 0.0001311, %cost 0.015).

Best integrated confidence after normalizing the prior baseline by empirical cost: `twise_t2` (omega_cost 0.001997, %cost 0.005493).

Empirical cost/confidence Pareto front:

- `twise_t2`: posterior area 0.9994, risk 0.000641, %cost 0.005493, omega_cost 0.001997
- `SRSSampling_t2`: posterior area 0.9995, risk 0.0001311, %cost 0.015, omega_cost 0.0004518

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `7z:t2` | `supports` | 196.7 | 1.95e-41 | moderate (0.3892) | median risks: random=0.001042, solverBased=0.02314, divDistBased=0.00236, twise=0.000641, SRSSampling=0.0001311; spread=0.023 |
| `FSE2` | `7z:t2` | `supports` | 1 |  | changed (0.001545) | best size-normalized=SRSSampling_t2; best cost-normalized=twise_t2 |
| `FSE3` | `7z:t2` | `refutes` | 0 |  | moderate (0.001545) | best cost-normalized=twise_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `7z:t2` | `supports` | 0.5 |  | frontier change (1) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,twise_t2 |
| `FSE5` | `7z:t2` | `supports` | 1948 | 3.29e-12 | large (0.1948) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0001311, median random=0.001042 |
| `FSE6` | `7z:t2` | `supports` | 107 | 2.21e-30 | large (0.9893) | A12>0.5 means SRS costs tend to be higher; median SRS=0.015, median random=0.00867 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t2` | 600 | 0.008741 | 0.00867 | 0.001042 | 0.9984 | 3.7e-05 | 5.066e-05 |
| `solverBased_t2` | 600 | 0.008741 | 0.0066 | 0.02314 | 0.9591 | -0.03923 | -0.03869 |
| `divDistBased_t2` | 600 | 0.008741 | 0.008643 | 0.00236 | 0.9971 | -0.001233 | -0.001214 |
| `twise_t2` | 600 | 0.008741 | 0.005493 | 0.000641 | 0.9994 | 0.00102 | 0.001997 |
| `SRSSampling_t2` | 600 | 0.008741 | 0.015 | 0.0001311 | 0.9995 | 0.001144 | 0.0004518 |
