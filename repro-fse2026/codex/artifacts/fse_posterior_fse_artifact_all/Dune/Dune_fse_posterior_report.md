# Dune FSE-style posterior guarantee report

## Scope

This report treats posterior risk/confidence as the outcome, replacing prediction MRE for this family. The bound direction is `max` over 2304 reconstructed configurations.

The prior-confidence baseline uses `1 - (1 - epsilon)^(N + offset)` with `offset=1`. The default offset of 1 matches the FSE 2026 artifact notebook.

SRS generated in this run: `False`. When enabled, the implementation uses the FSE artifact defaults: `step_sample_size=25`, Welch's t-test, and random fill to the requested sample size.

## Headline

Lowest median posterior risk: `SRSSampling_t2` (risk 0.000434, %cost 0.1242).

Best integrated confidence after normalizing the prior baseline by empirical cost: `SRSSampling_t2` (omega_cost 0.002077, %cost 0.1242).

Empirical cost/confidence Pareto front:

- `random_t2`: posterior area 0.9964, risk 0.00217, %cost 0.115, omega_cost 0.0001485
- `divDistBased_t2`: posterior area 0.9969, risk 0.002604, %cost 0.1173, omega_cost 0.0005795
- `twise_t2`: posterior area 0.9961, risk 0.003906, %cost 0.1148, omega_cost -0.0001537
- `SRSSampling_t2`: posterior area 0.9986, risk 0.000434, %cost 0.1242, omega_cost 0.002077

## Figures

- `fig_posterior_risk_by_strategy.png`
- `fig_confidence_discrepancy.png`
- `fig_guarantee_cost_frontier.png`
- `fig_integrated_confidence_discrepancy.png`

## Hypothesis Tests

| Hypothesis | Scope | Verdict | Statistic | p-value | Effect | Notes |
|---|---|---|---:|---:|---|---|
| `FSE1` | `Dune:t2` | `supports` | 129.8 | 4.34e-27 | small (0.2541) | median risks: random=0.00217, solverBased=0.006944, divDistBased=0.002604, twise=0.003906, SRSSampling=0.000434; spread=0.00651 |
| `FSE2` | `Dune:t2` | `refutes` | 0 |  | unchanged (0) | best size-normalized=SRSSampling_t2; best cost-normalized=SRSSampling_t2 |
| `FSE3` | `Dune:t2` | `supports` | 1 |  | best (0) | best cost-normalized=SRSSampling_t2; SRS on empirical cost/confidence Pareto=True |
| `FSE4` | `Dune:t2` | `supports` | 0.25 |  | large frontier change (3) | count front=SRSSampling_t2; empirical front=SRSSampling_t2,divDistBased_t2,random_t2,twise_t2 |
| `FSE5` | `Dune:t2` | `supports` | 3002 | 8.63e-06 | medium (0.3002) | A12<0.5 means SRS risks tend to be lower; median SRS=0.000434, median random=0.00217 |
| `FSE6` | `Dune:t2` | `supports` | 1307 | 1.55e-17 | large (0.8693) | A12>0.5 means SRS costs tend to be higher; median SRS=0.1242, median random=0.115 |

## Strategy Summary

| Strategy | n | %n | %cost | risk | posterior area | omega(size) | omega(cost) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `random_t2` | 265 | 0.115 | 0.115 | 0.00217 | 0.9964 | 0.0001472 | 0.0001485 |
| `solverBased_t2` | 265 | 0.115 | 0.1149 | 0.006944 | 0.9938 | -0.002474 | -0.00247 |
| `divDistBased_t2` | 265 | 0.115 | 0.1173 | 0.002604 | 0.9969 | 0.0006507 | 0.0005795 |
| `twise_t2` | 265 | 0.115 | 0.1148 | 0.003906 | 0.9961 | -0.0001609 | -0.0001537 |
| `SRSSampling_t2` | 265 | 0.115 | 0.1242 | 0.000434 | 0.9986 | 0.002352 | 0.002077 |
