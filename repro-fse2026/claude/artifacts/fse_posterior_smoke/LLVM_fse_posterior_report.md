# LLVM FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1017 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `True`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `solverBased_t2` (risk 0, %cost 0.05384).

Best integrated confidence after normalizing the prior baseline by empirical cost: `distBased_t2` (omega_cost 0.01392, %cost 0.05565).

Empirical cost/confidence Pareto front:

- `distBased_t2`: posterior area 0.9969, risk 0.0009833, %cost 0.05565, omega_cost 0.01392
- `divDistBased_t2`: posterior area 0.9967, risk 0.0009833, %cost 0.05515, omega_cost 0.01387
- `henard_t2`: posterior area 0.8869, risk 0.1131, %cost 0.05341, omega_cost -0.09532
- `solverBased_t2`: posterior area 0.9904, risk 0, %cost 0.05384, omega_cost 0.007984

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `SRSSampling_t2` | 56 | 0.05506 | 0.05736 | 0.00295 | 0.9939 | 0.01115 | 0.01048 |
| `distBased_t2` | 56 | 0.05506 | 0.05565 | 0.0009833 | 0.9969 | 0.01409 | 0.01392 |
| `divDistBased_t2` | 56 | 0.05506 | 0.05515 | 0.0009833 | 0.9967 | 0.0139 | 0.01387 |
| `henard_t2` | 56 | 0.05506 | 0.05341 | 0.1131 | 0.8869 | -0.09584 | -0.09532 |
| `random_t2` | 56 | 0.05506 | 0.05489 | 0.01622 | 0.9804 | -0.002326 | -0.002273 |
| `solverBased_t2` | 56 | 0.05506 | 0.05384 | 0 | 0.9904 | 0.007605 | 0.007984 |
