# BerkeleyDBC FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2560 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `False`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t2` (risk 0.0007813, %cost 0.1179).

Best integrated confidence after normalizing the prior baseline by empirical cost: `random_t2` (omega_cost -5.576e-05, %cost 0.03812).

Empirical cost/confidence Pareto front:

- `random_t2`: posterior area 0.9899, risk 0.007031, %cost 0.03812, omega_cost -5.576e-05
- `solverBased_t2`: posterior area 0.6046, risk 0.4008, %cost 0.00706, omega_cost -0.3456
- `divDistBased_t2`: posterior area 0.985, risk 0.007031, %cost 0.03222, omega_cost -0.003175
- `twise_t2`: posterior area 0.9477, risk 0.05234, %cost 0.01084, omega_cost -0.01873
- `SRSSampling_t2`: posterior area 0.9934, risk 0.0007813, %cost 0.1179, omega_cost -0.003341

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `BerkeleyDBC:t2` | `supports` | 409.2 | 2.90e-87 | large (0.8185) | median risks: random=0.007031, solverBased=0.4008, divDistBased=0.007031, twise=0.05234, SRSSampling=0.0007813; spread=0.4 |
| `FSE2` | `BerkeleyDBC:t2` | `supports` | 1 |  | changed (0.003286) | best size-normalized=SRSSampling_t2; best cost-normalized=random_t2 |
| `FSE3` | `BerkeleyDBC:t2` | `refutes` | 0 |  | moderate (0.003286) | best cost-normalized=random_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `BerkeleyDBC:t2` | `supports` | 0.2 |  | large frontier change (4) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,divDistBased_t2,random_t2,solverBased_t2,twise_t2 |
| `FSE5` | `BerkeleyDBC:t2` | `supports` | 1816 | 2.84e-13 | large (0.1816) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0007813, median random=0.007031 |
| `FSE6` | `BerkeleyDBC:t2` | `supports` | 271 | 2.08e-28 | large (0.9729) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1179, median random=0.03812 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t2` | 97 | 0.03789 | 0.03812 | 0.007031 | 0.9899 | 3.354e-06 | -5.576e-05 |
| `solverBased_t2` | 97 | 0.03789 | 0.00706 | 0.4008 | 0.6046 | -0.3853 | -0.3456 |
| `divDistBased_t2` | 97 | 0.03789 | 0.03222 | 0.007031 | 0.985 | -0.004911 | -0.003175 |
| `twise_t2` | 97 | 0.03789 | 0.01084 | 0.05234 | 0.9477 | -0.04224 | -0.01873 |
| `SRSSampling_t2` | 97 | 0.03789 | 0.1179 | 0.0007813 | 0.9934 | 0.003468 | -0.003341 |
