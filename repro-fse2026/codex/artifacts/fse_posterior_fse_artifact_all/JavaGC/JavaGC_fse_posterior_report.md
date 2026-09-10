# JavaGC FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 193536 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `False`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t2` (risk 0.0001576, %cost 0.004121).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t2` (omega_cost 0.0005056, %cost 0.004121).

Empirical cost/confidence Pareto front:

- `divDistBased_t2`: posterior area 0.998, risk 0.001152, %cost 0.002402, omega_cost 0.0001269
- `twise_t2`: posterior area 0.9931, risk 0.006913, %cost 0.001512, omega_cost -0.003519
- `SRSSampling_t2`: posterior area 0.9993, risk 0.0001576, %cost 0.004121, omega_cost 0.0005056

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `JavaGC:t2` | `supports` | 373.5 | 1.48e-79 | large (0.7464) | median risks: random=0.001684, solverBased=0.2381, divDistBased=0.001152, twise=0.006913, SRSSampling=0.0001576; spread=0.238 |
| `FSE2` | `JavaGC:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `JavaGC:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `JavaGC:t2` | `supports` | 0.3333 |  | large frontier change (2) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,divDistBased_t2,twise_t2 |
| `FSE5` | `JavaGC:t2` | `supports` | 1755 | 1.09e-13 | large (0.1755) | A12<0.5 means SRS risks tend to be lower; median SRS=0.0001576, median random=0.001684 |
| `FSE6` | `JavaGC:t2` | `supports` | 22 | 1.97e-31 | large (0.9978) | A12>0.5 means SRS costs tend to be higher; median SRS=0.004121, median random=0.002431 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t2` | 468 | 0.002418 | 0.002431 | 0.001684 | 0.9977 | -0.0001447 | -0.0001559 |
| `solverBased_t2` | 468 | 0.002418 | 0.001816 | 0.2381 | 0.8237 | -0.1742 | -0.1735 |
| `divDistBased_t2` | 468 | 0.002418 | 0.002402 | 0.001152 | 0.998 | 0.0001122 | 0.0001269 |
| `twise_t2` | 468 | 0.002418 | 0.001512 | 0.006913 | 0.9931 | -0.004786 | -0.003519 |
| `SRSSampling_t2` | 468 | 0.002418 | 0.004121 | 0.0001576 | 0.9993 | 0.001383 | 0.0005056 |
