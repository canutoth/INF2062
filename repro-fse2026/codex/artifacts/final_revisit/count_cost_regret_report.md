# Count-Cost Recommendation Regret

This report quantifies how often a sampling recommendation that looks best under sample-size cost loses once measured acquisition cost is charged.

Definitions:

- `changed_rate`: fraction of `(context, lambda)` decisions whose top strategy--budget pair changes when measured cost replaces sample-size cost.
- measured-cost regret (CSV field `empirical_regret`): `J_meas(count winner) - J_meas(measured-cost winner)`, using the same min-max-normalized MRE and measured-cost objective as the RQ3 rank-stability analysis.
- `cost_ratio`: measured training cost of the count-cost winner divided by the measured-cost winner.
- `more_accurate_but_costlier`: the count-cost winner has lower MRE but higher measured cost; this is a trade-off pattern, not a strict same-budget dominance claim.
- `not_empirical_pareto`: the count-cost winner is not on the measured-cost Pareto frontier, so another strategy--budget pair is no less accurate and no more expensive under measured cost.

## Summary

| Family | Decisions | Changed | Median regret | Median cost ratio | Accurate but costlier | Not measured-cost Pareto | Count-front false positives | Hidden measured-cost pairs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `ALL_PRIMARY` | 1666 | 538 (0.323) | 0.022 | 1.043 | 0.545 | 0.106 | 0.032 | 0.515 |
| `ENERGY` | 196 | 94 (0.480) | 0.002 | 1.037 | 0.489 | 0.223 | 0.040 | 0.454 |
| `LCBENCH` | 245 | 157 (0.641) | 0.054 | 0.512 | 0.159 | 0.185 | 0.071 | 0.511 |
| `LINUX` | 49 | 36 (0.735) | 0.019 | 1.984 | 0.833 | 0.000 | 0.000 | 0.700 |
| `REPLICATION-ICPE20` | 476 | 48 (0.101) | 0.006 | 1.045 | 0.875 | 0.000 | 0.000 | 0.584 |
| `REPLICATION-ICSE19` | 49 | 7 (0.143) | 0.035 | 0.201 | 0.429 | 0.000 | 0.000 | 0.447 |
| `WORKLOAD` | 651 | 196 (0.301) | 0.021 | 1.253 | 0.750 | 0.036 | 0.033 | 0.481 |

## Headline Reading

Across primary artifacts, `538/1666` count-cost top strategy--budget pairs change under measured cost.
Among changed decisions, the median measured-cost ratio of the count winner is `1.043`.
The CSV and summary table retain normalized objective regret for auditability, but it is not a reader-facing effect size.
In `0.545` of changed decisions, the count-cost winner buys more accuracy at higher measured cost; this explains why the measured-cost objective can choose differently, but it is a trade-off.
In `0.106` of changed decisions, the stronger same-budget failure appears: the count-cost winner is not on the measured-cost Pareto frontier.
Pareto analysis also shows a count-front false-positive rate of `0.032` and a hidden measured-cost pair rate of `0.515`.

Most frequent count-cost winner strategies in changed decisions:

- `pilotCost`: 145
- `pairwise`: 127
- `diversity`: 69
- `random`: 45
- `balanced`: 40
- `cheapOracle`: 31
- `expensiveOracle`: 27
- `divDistBased`: 16
- `coverage`: 16
- `distBased`: 9
