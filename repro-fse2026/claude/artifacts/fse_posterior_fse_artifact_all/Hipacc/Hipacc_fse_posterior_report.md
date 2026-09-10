# Hipacc FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 13485 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `False`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `solverBased_t2` (risk 0, %cost 0.07026).

Best integrated confidence after normalizing the prior baseline by empirical cost: `divDistBased_t2` (omega_cost 0.0008044, %cost 0.07094).

Empirical cost/confidence Pareto front:

- `random_t2`: posterior area 0.9988, risk 0.0008157, %cost 0.0626, omega_cost 6.371e-06
- `divDistBased_t2`: posterior area 0.9998, risk 0.0001483, %cost 0.07094, omega_cost 0.0008044
- `twise_t2`: posterior area 0.9986, risk 0.001409, %cost 0.04951, omega_cost 8.438e-05
- `SRSSampling_t2`: posterior area 0.9996, risk 0.0002595, %cost 0.06855, omega_cost 0.0007072

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `Hipacc:t2` | `supports` | 234.4 | 1.48e-49 | small (0.4655) | median risks: random=0.0008157, solverBased=0, divDistBased=0.0001483, twise=0.001409, SRSSampling=0.0002595; spread=0.001409 |
| `FSE2` | `Hipacc:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=divDistBased_t2; best cost-normalized=divDistBased_t2 |
| `FSE3` | `Hipacc:t2` | `refutes` | 0 |  | negligible (9.717e-05) | best cost-normalized=divDistBased_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `Hipacc:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=divDistBased_t2; empirical front=SRSSampling_t2,divDistBased_t2,random_t2,twise_t2 |
| `FSE5` | `Hipacc:t2` | `supports` | 2445 | 8.32e-09 | large (0.2445) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0002595, median random=0.0008157 |
| `FSE6` | `Hipacc:t2` | `supports` | 54 | 4.91e-31 | large (0.9946) | A12>0.5 means SRS costs tend to be higher; median SRS=0.06855, median random=0.0626 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t2` | 843 | 0.06251 | 0.0626 | 0.0008157 | 0.9988 | 8.052e-06 | 6.371e-06 |
| `solverBased_t2` | 843 | 0.06251 | 0.07026 | 0 | 0.9994 | 0.0005531 | 0.000423 |
| `divDistBased_t2` | 843 | 0.06251 | 0.07094 | 0.0001483 | 0.9998 | 0.0009446 | 0.0008044 |
| `twise_t2` | 843 | 0.06251 | 0.04951 | 0.001409 | 0.9986 | -0.0002255 | 8.438e-05 |
| `SRSSampling_t2` | 843 | 0.06251 | 0.06855 | 0.0002595 | 0.9996 | 0.0008112 | 0.0007072 |
