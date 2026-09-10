# LLVM FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 1024 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `False`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `solverBased_t2` (risk 0, %cost 0.05346).

Best integrated confidence after normalizing the prior baseline by empirical cost: `divDistBased_t2` (omega_cost 0.01217, %cost 0.05466).

Empirical cost/confidence Pareto front:

- `divDistBased_t2`: posterior area 0.9949, risk 0.005371, %cost 0.05466, omega_cost 0.01217
- `solverBased_t2`: posterior area 0.9903, risk 0, %cost 0.05346, omega_cost 0.007957

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `SRSSampling_t2` | 56 | 0.05469 | 0.05677 | 0.004883 | 0.9926 | 0.00982 | 0.009209 |
| `divDistBased_t2` | 56 | 0.05469 | 0.05466 | 0.005371 | 0.9949 | 0.01216 | 0.01217 |
| `random_t2` | 56 | 0.05469 | 0.0545 | 0.01611 | 0.9805 | -0.00229 | -0.002232 |
| `solverBased_t2` | 56 | 0.05469 | 0.05346 | 0 | 0.9903 | 0.007573 | 0.007957 |
