# `linux504_vmlinux` with empirical `vmlinux` acquisition cost

## Scope and protocol

This report covers TuxKConfig **Linux 5.04** (OpenML 46742, Borges et
al., EASE 2025), a pool of **25,847 valid kernel configurations**.
Same protocol as the other releases. After feature pruning, **494
kernel options** enter the design matrix.

Sample sizes for the percentage-based level grid: `n ∈ {258, 517,
1292, 2585, 5169}`. Diversity capped at the smallest three levels.

## Headline result — and a surprise

The calibration story replicates as expected:

- `random`, `balanced`, `coverage` all calibrated to ±0.7%.
- **`diversity` 2.087×** — sixth confirmation of the ~2× upward bias.
- `uncertainty` median 0.878 with a non-monotone seam.
- Oracles: cheap 0.254×, expensive 4.58×.

**The RQ3 ranking instability finding is the surprise**: v5.04 shows
**7/7 top-1 flips** between count-cost and empirical-cost rankings —
even more than v5.08's 6/7. This kills the v1-style hypothesis
(ratified up to v5.0) that "v5.08 is the level-grid outlier". v5.04
sits between v4.20 (23K, 2/7) and v5.0 (20K, 2/7) by pool size, but
joins v5.08 on the high-flip side.

## RQ1: Cost heterogeneity

- min/median/max `vmlinux`: 11.6 MB / 87 MB / 2.05 GB.
- CV: **1.08** (lowest among the three "long-tailed" releases v4.15,
  v5.0, v5.04, v4.20).
- p90/p10: **5.21**.

## RQ2: Calibration ratios

| strategy          | runs | median ratio | bias    | IQR              |
| ----------------- | ---- | ------------ | ------- | ---------------- |
| `random`          | 500  | **1.000**    | +0.000  | [0.979, 1.021]   |
| `balanced`        | 500  | **0.999**    | −0.001  | [0.980, 1.018]   |
| `coverage`        | 100  | **0.993**    | −0.007  | [0.980, 1.006]   |
| `uncertainty`     | 100  | **0.878**    | −0.122  | [0.815, 1.010]   |
| `diversity`       | 60   | **2.087**    | +1.087  | [1.897, 2.192]   |
| `cheapOracle`     | 5    | **0.254**    | −0.746  | [0.225, 0.289]   |
| `expensiveOracle` | 5    | **4.579**    | +3.579  | [3.358, 6.626]   |

`uncertainty` per-level (the seam):

| level | n     | ratio    | MRE   |
| ----- | ----- | -------- | ----- |
| 1%    | 258   | **0.758**| 0.395 |
| 2%    | 517   | 0.839    | 0.377 |
| 5%    | 1292  | 0.921    | 0.344 |
| 10%   | 2585  | 0.850    | 0.348 |
| 20%   | 5169  | **1.171**| 0.311 |

Direction is consistent (cheap-leaning at small n, expensive-leaning
at the largest level), but the bulk has a back-dip at n=2585 (0.92 →
0.85), so Spearman ρ over the level grid is non-monotone. The
cross-over from <1 to >1 happens between n=2585 and n=5169.

## RQ3: The unexpected 7/7 flip rate

| λ     | count top-1            | empirical top-1            | flip? |
| ----- | ---------------------- | -------------------------- | ----- |
| 0.1   | `balanced_n00258`      | `uncertainty_n00517`       | yes   |
| 0.25  | `balanced_n00258`      | `uncertainty_n00258`       | yes   |
| 0.5   | `balanced_n00258`      | `uncertainty_n00258`       | yes   |
| 1.0   | `balanced_n00258`      | `uncertainty_n00258`       | yes   |
| 2.0   | `balanced_n00258`      | `uncertainty_n00258`       | yes   |
| 4.0   | `balanced_n00258`      | `cheapOracle_n00258`       | yes   |
| 10.0  | `balanced_n00258`      | `cheapOracle_n00258`       | yes   |

Mean Kendall τ falls from 0.795 (λ=0.25) to 0.610 (λ=10).

**Mechanism.** At the smallest level (n=258), `balanced` has the
lowest median MRE among deployable strategies, so count cost picks
`balanced_n00258` for every λ. Under empirical cost, `uncertainty`'s
calibration ratio is 0.76 at this level — a 24% discount on training
cost — which more than compensates for `uncertainty`'s slightly
higher MRE in the cost-aware objective. So empirical picks
`uncertainty_n00258` across most of the λ range, and `cheapOracle_n00258`
at extreme λ.

**Why this is different from v5.0 and v4.20** (which show 2/7 flips
on similar pool sizes): on those releases, count cost *also* picks
`uncertainty` at the smallest level (because `uncertainty` happens to
have the lowest MRE there), so count and empirical agree on the
top-1 for most λ. On v5.04, `balanced` happens to win the count-side
MRE comparison at n=258, so the strategies disagree everywhere.

This is a cleaner mechanism for the high-flip behaviour: it is **not
about pool size**, it is about whether count cost and empirical cost
pick the same strategy at the smallest level. When they pick the same
strategy, flips concentrate at the λ extremes (2/7); when they pick
different strategies, every λ flips (6/7 or 7/7).

## RQ4: Pareto frontiers

Empirical Pareto frontier: 8 strategy-size pairs.
Count Pareto frontier: 5.

Diversity dominated under both cost models at every level (sixth
confirmation).

## Cross-version pointers

`diversity` calibration so far across six releases: 2.28, 2.23, 2.27,
2.06, **2.09**, 2.02. The window [2.02, 2.28] is now even tighter.

Flip-rate panel so far:

| release | pool   | flips |
| ------- | ------ | ----- |
| v4.13   | 92,562 | 2/7   |
| v4.15   | 39,391 | 2/7   |
| v4.20   | 23,489 | 2/7   |
| v5.0    | 19,952 | 2/7   |
| v5.04   | 25,847 | **7/7** |
| v5.08   | 21,923 | 6/7   |

The mechanism (count vs empirical disagreeing at n=smallest) explains
the bimodal clustering: v5.04 and v5.08 have `balanced` (or `random`)
winning count-MRE at the smallest n while `uncertainty` wins empirical
cost; the other four releases have `uncertainty` winning both, so
count and empirical agree on the top-1 for most λ.
