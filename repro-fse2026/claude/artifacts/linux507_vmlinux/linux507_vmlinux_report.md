# `linux507_vmlinux` with empirical `vmlinux` acquisition cost

## Scope and protocol

This report covers TuxKConfig **Linux 5.07** (OpenML 46743, Borges et
al., EASE 2025), a pool of **20,159 valid kernel configurations** —
the second-smallest of the seven evaluated releases (only v5.0 at
19,952 is smaller).

Same protocol; **494 kernel options** after pruning. Levels:
`n ∈ {202, 403, 1008, 2016, 4032}`.

## Headline result

v5.07 produces three notable findings:

- **`diversity` 1.999×** — seventh confirmation of the ~2× upward
  bias, but the lowest magnitude in the series (just under 2).
- **First release where CV < 1**: cost CV is **0.99**, p90/p10 is
  4.76. This makes v5.07 the *least* heterogeneous of the seven
  randconfig pools.
- **RQ3 flip rate is intermediate**: 4/7 — sitting between the two
  clusters (v4.13/v4.15/v4.20/v5.0 at 2/7; v5.04 at 7/7; v5.08 at 6/7).

## RQ1: Cost heterogeneity

- min/median/max `vmlinux`: 11.6 MB / 88 MB / 2.00 GB.
- CV: **0.99** (the only sub-1 CV in the series).
- p90/p10: **4.76**.

The CV decline across the seven releases is non-monotone but trending
downward with kernel version: 1.43 (4.13), 1.16 (4.15), 1.16 (4.20),
1.12 (5.0), 1.08 (5.04), 0.99 (5.07), 1.01 (5.08). The configuration
search space grows but the cost distribution gets less heavy-tailed
in the later kernels.

## RQ2: Calibration ratios

| strategy          | runs | median ratio | bias    | IQR              |
| ----------------- | ---- | ------------ | ------- | ---------------- |
| `random`          | 500  | **0.999**    | −0.001  | [0.983, 1.016]   |
| `balanced`        | 500  | **0.997**    | −0.003  | [0.979, 1.016]   |
| `coverage`        | 100  | **0.993**    | −0.007  | [0.980, 1.010]   |
| `uncertainty`     | 100  | **0.839**    | −0.161  | [0.755, 0.918]   |
| `diversity`       | 60   | **1.999**    | +0.999  | [1.900, 2.076]   |
| `cheapOracle`     | 5    | **0.270**    | −0.730  | [0.239, 0.306]   |
| `expensiveOracle` | 5    | **4.193**    | +3.193  | [3.116, 6.049]   |

`uncertainty` per-level (a strictly monotone seam):

| level | n     | ratio    | MRE   |
| ----- | ----- | -------- | ----- |
| 1%    | 202   | **0.678**| 0.400 |
| 2%    | 403   | 0.763    | 0.380 |
| 5%    | 1008  | 0.783    | 0.385 |
| 10%   | 2016  | 0.866    | 0.370 |
| 20%   | 4032  | **1.122**| 0.329 |

Spearman ρ over the level grid is **1.0** (strict monotone increasing,
matching v5.0 and v5.08). Cross-over from <1 to >1 happens between
n=2016 and n=4032. This is one of the cleanest seam observations.

The `uncertainty` IQR [0.755, 0.918] is the **furthest below 1** of
any release in the study — even the median (0.839) is well below 1.
On v5.07 the AL bias is dominantly cheap-leaning across levels, with
only the largest level (20%) crossing over to expensive.

## RQ3: 4/7 flips — the missing-middle case

| λ     | count top-1            | empirical top-1            | flip? |
| ----- | ---------------------- | -------------------------- | ----- |
| 0.1   | `random_n00202`        | `random_n00202`            | no    |
| 0.25  | `random_n00202`        | `random_n00202`            | no    |
| 0.5   | `random_n00202`        | `random_n00202`            | no    |
| 1.0   | `random_n00202`        | `uncertainty_n00202`       | yes   |
| 2.0   | `random_n00202`        | `uncertainty_n00202`       | yes   |
| 4.0   | `random_n00202`        | `uncertainty_n00202`       | yes   |
| 10.0  | `random_n00202`        | `cheapOracle_n00202`       | yes   |

Mean Kendall τ ranges from 0.792 (λ=0.1) to 0.598 (λ=10).

**Mechanism.** v5.07 is a *partial* version of the v5.04 mechanism:
count cost picks `random_n00202` (lowest MRE among deployable
strategies at the smallest level), and empirical cost agrees at low
λ (where MRE dominates) but diverges at higher λ once the cost term
weight is enough to expose `uncertainty`'s 33% cheap discount at
n=202. So v5.07 has the **count-disagrees-on-strategy mechanism** of
v5.04/v5.08, but with a softer transition because `random` and
`uncertainty` are closer in MRE than `balanced` and `uncertainty`
were on v5.04.

This makes the bimodal flip-rate picture across releases now look
trimodal:

| flip rate | releases                       | count-side top-1     |
| --------- | ------------------------------ | -------------------- |
| 2/7       | v4.13, v4.15, v4.20, v5.0      | `uncertainty_n=small` |
| 4/7       | v5.07                          | `random_n=small`     |
| 6–7/7     | v5.04, v5.08                   | `balanced_n=small`   |

The pattern: **count cost and empirical cost agree on the top-1
exactly when count cost happens to pick `uncertainty`** (which is
also empirical cost's natural pick once cost weight grows). When
count picks anything else (`random`, `balanced`), the disagreement
rate scales with how many λ values are dominated by the cost term.

## RQ4: Pareto frontiers

Empirical Pareto frontier: 7 strategy-size pairs.
Count Pareto frontier: 5.

Diversity dominated under both cost models (seventh confirmation).
The empirical frontier adds the cheap-tail oracle and the
`uncertainty_n00202` cheap-leaning AL point.

## Cross-version pointers

`diversity` calibration across all seven releases: 2.28, 2.23, 2.27,
2.06, 2.09, **2.00**, 2.02. The window narrows to **[2.00, 2.28]** —
the most robust replicated effect in the study.

`uncertainty` Spearman ρ in n: 0.6 (v4.13), 0.6 (v4.15), 0.4 (v4.20),
1.0 (v5.0), 0.8 (v5.04), **1.0** (v5.07), 1.0 (v5.08). Strictly
monotone seam in 3 of 7 releases (v5.0, v5.07, v5.08).

The 7-release flip-rate spread (2 / 2 / 2 / 2 / 4 / 6 / 7) is now
explained by which strategy wins count-MRE at the smallest level,
which reduces to a count-vs-empirical decision rule that doesn't
depend on cost CV or pool size in any clean way.
