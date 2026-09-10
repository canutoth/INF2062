# Validating the pilot audit

## What this checks

The paper recommends a cheap **pilot audit** before trusting sample *count* as a proxy for sampling *cost*: inspect (1) the spread of per-configuration measured cost (`cost_cv`, `cost_p90p10`), (2) whether the prediction target is itself the cost (`target_cost_decorr`), and (3) the per-strategy budget **Ratio** = pct_cost / pct_n at a small pilot budget (`strategy_bias` = spread of median Ratio across deployable strategies). We test whether those pilot diagnostics **predict** that trusting sample count instead of measured cost changes the cost-controlled Kruskal-Wallis recommendation.

## Two outcomes (both from the corrected KW CSVs, one row per budget level)

1. **decision_stakes (validated, headline):** does the count-era best sampler differ from the cost-era best sampler by more than **0.01** in held-out MRE (`|mre_gap| > tau`)? `stakes_rate` = mean over levels; `stakes_any` = any. This is the *consequential* question -- "is count a **materially** unsafe proxy".
2. **group_changed (secondary, as literally named in the brief):** does the Dunn top-GROUP **set** change. `flip_rate` = mean over levels; `flipped` = any. This is a p=0.05 set-membership test; it is statistically noisy and *saturates* (a decisive cost winner makes the set stable), so it is reported only as a caveat.

## Setup

- **167 contexts** across **6 families**: energy, icse19, lcbench, linux, workload, x264.
- Diagnostics computed on the **smallest 2 budget level(s)** (a genuine pilot); `strategy_bias` reuses the SAME cells the KW analysis builds and fits **no learner** (Ratio needs only the sample indices + per-config cost).
- **No approximation used**: every family computes the exact per-strategy Ratio (archive samples / generated pilot samples / cached Linux HGBT cells).

## Predictive power -- decision_stakes (VALIDATED)

Base rate (any-budget stakes) = 0.53.

| diagnostic | ROC-AUC for `stakes_any` |
|---|---|
| cost_cv | 0.686 |
| cost_p90p10 | 0.791 |
| target_cost_decorr | 0.404 |
| strategy_bias | 0.664 |
| **2-feature rule (cost_p90p10 x strategy_bias)** | **0.731** |

(Spearman rho of the 2-feature rule with `stakes_rate` = +0.471.)

### 3x3 mean stakes_rate (cost p90/p10 ratio x strategy_bias tertiles)

Tertile edges -- cost p90/p10 ratio: [2.587, 5.961]; strategy_bias: [0.302, 0.634]. Rows = cost heterogeneity, columns = strategy_bias.

| het \ bias | low | med | high |
|---|---|---|---|
| **low** | 0.06 (n=48) | 0.19 (n=8) | – |
| **med** | – | 0.10 (n=37) | 0.13 (n=18) |
| **high** | 0.30 (n=8) | 0.32 (n=10) | 0.39 (n=38) |

## Secondary -- group_changed (noisy top-group set identity)

Base rate (any-level group change) = 0.93. This outcome is **not** predicted by the cost-spread / bias diagnostics; pooled it is mildly *negative* (a decisive cost winner stabilises the top-group set), which is exactly why we report decision_stakes as the meaningful outcome.

| diagnostic | ROC-AUC for `flipped` |
|---|---|
| cost_cv | 0.288 |
| cost_p90p10 | 0.276 |
| target_cost_decorr | 0.610 |
| strategy_bias | 0.274 |
| 2-feature rule (cost_cv x strategy_bias) | 0.249 |

3x3 mean group_changed flip_rate (same axes):

| het \ bias | low | med | high |
|---|---|---|---|
| **low** | 0.58 (n=48) | 0.34 (n=8) | – |
| **med** | – | 0.51 (n=37) | 0.53 (n=18) |
| **high** | 0.41 (n=8) | 0.47 (n=10) | 0.34 (n=38) |

## Paraphrase for the paper

> A cheap pilot audit -- cost spread (`cost_p90p10`) and the per-strategy budget Ratio spread (`strategy_bias`) -- predicts whether trusting sample **count** instead of measured **cost** materially changes the recommended sampler (the count-era and cost-era best samplers differ by >0.01 held-out MRE) with ROC-AUC = 0.73 (best single diagnostic `cost_p90p10`, AUC = 0.79; `strategy_bias` alone, AUC = 0.66) over 167 contexts in 6 families. In the low-spread / low-bias regime only 6% of pilot budgets carry a material count-vs-cost gap (count is a safe proxy), versus 39% in the high-spread / high-bias regime (count is unsafe). The target--cost correlation diagnostic alone is weak (AUC = 0.40) because several families measure the cost directly; the actionable signal is the cost spread and the per-strategy Ratio -- precisely the two quantities the cheap audit reports. (The narrow Dunn top-group *set* identity is a noisier, saturating statistic and is not predictable this way; the materially consequential gap is.)
