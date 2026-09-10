# Polly FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 60000 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `False`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `divDistBased_t2` (risk 0.001392, %cost 0.00568).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t2` (omega_cost 0.0006115, %cost 0.005841).

Empirical cost/confidence Pareto front:

- `random_t2`: posterior area 0.9971, risk 0.001842, %cost 0.005743, omega_cost 3.308e-05
- `solverBased_t2`: posterior area 0.9972, risk 0.00225, %cost 0.005795, omega_cost 9.644e-05
- `divDistBased_t2`: posterior area 0.997, risk 0.001392, %cost 0.00568, omega_cost -9.795e-05
- `twise_t2`: posterior area 0.9956, risk 0.004417, %cost 0.004134, omega_cost -0.0004169
- `SRSSampling_t2`: posterior area 0.9978, risk 0.0016, %cost 0.005841, omega_cost 0.0006115

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `Polly:t2` | `supports` | 118.2 | 1.31e-24 | small (0.2307) | median risks: random=0.001842, solverBased=0.00225, divDistBased=0.001392, twise=0.004417, SRSSampling=0.0016; spread=0.003025 |
| `FSE2` | `Polly:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `Polly:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `Polly:t2` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,divDistBased_t2,random_t2,solverBased_t2,twise_t2 |
| `FSE5` | `Polly:t2` | `inconclusive` | 4146 | 0.112 | small (0.4146) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0016, median random=0.001842 |
| `FSE6` | `Polly:t2` | `supports` | 2047 | 1.88e-11 | large (0.7953) | A12>0.5 means SRS costs tend to be higher; median SRS=0.005841, median random=0.005743 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t2` | 345 | 0.00575 | 0.005743 | 0.001842 | 0.9971 | 2.934e-05 | 3.308e-05 |
| `solverBased_t2` | 345 | 0.00575 | 0.005795 | 0.00225 | 0.9972 | 0.0001188 | 9.644e-05 |
| `divDistBased_t2` | 345 | 0.00575 | 0.00568 | 0.001392 | 0.997 | -0.0001335 | -9.795e-05 |
| `twise_t2` | 345 | 0.00575 | 0.004134 | 0.004417 | 0.9956 | -0.001535 | -0.0004169 |
| `SRSSampling_t2` | 345 | 0.00575 | 0.005841 | 0.0016 | 0.9978 | 0.0006562 | 0.0006115 |
