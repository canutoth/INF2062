# LLVM FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1024 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `False`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `solverBased_t2` (risk 0, %cost 0.05341).

Best integrated confidence after normalizing the prior baseline by empirical cost: `divDistBased_t2` (omega_cost 0.01208, %cost 0.05481).

Empirical cost/confidence Pareto front:

- `divDistBased_t2`: posterior area 0.9949, risk 0.003906, %cost 0.05481, omega_cost 0.01208
- `twise_t2`: posterior area 0.9873, risk 0.0127, %cost 0.0492, omega_cost 0.006395

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `LLVM:t2` | `supports` | 170.2 | 9.55e-36 | moderate (0.3357) | median risks: random=0.01221, solverBased=0, divDistBased=0.003906, twise=0.0127, SRSSampling=0.003906; spread=0.0127 |
| `FSE2` | `LLVM:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=divDistBased_t2; best cost-normalized=divDistBased_t2 |
| `FSE3` | `LLVM:t2` | `refutes` | 0 |  | moderate (0.0017) | best cost-normalized=divDistBased_t2; SRS on empirical cost/confidence Pareto=False |
| `FSE4` | `LLVM:t2` | `refutes` | 1 |  | same frontier (0) | count front=divDistBased_t2,twise_t2; empirical front=divDistBased_t2,twise_t2 |
| `FSE5` | `LLVM:t2` | `supports` | 2747 | 4.91e-07 | large (0.2747) | A12<0.5 means SRS risks tend to be lower; median SRS=0.003906, median random=0.01221 |
| `FSE6` | `LLVM:t2` | `supports` | 477 | 5.00e-26 | large (0.9523) | A12>0.5 means SRS costs tend to be higher; median SRS=0.05685, median random=0.05474 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t2` | 56 | 0.05469 | 0.05474 | 0.01221 | 0.9838 | 0.001021 | 0.001006 |
| `solverBased_t2` | 56 | 0.05469 | 0.05341 | 0 | 0.9826 | -0.0001317 | 0.000265 |
| `divDistBased_t2` | 56 | 0.05469 | 0.05481 | 0.003906 | 0.9949 | 0.01211 | 0.01208 |
| `twise_t2` | 55 | 0.05371 | 0.0492 | 0.0127 | 0.9873 | 0.004849 | 0.006395 |
| `SRSSampling_t2` | 56 | 0.05469 | 0.05685 | 0.003906 | 0.9938 | 0.01101 | 0.01038 |
