# `linux415_vmlinux` with empirical `vmlinux` acquisition cost

## Scope and protocol

This report covers TuxKConfig **Linux 4.15** (OpenML 46739, Borges et
al., EASE 2025), a pool of **39,391 valid kernel configurations** drawn
with `make randconfig` on the v4.15 kernel tree. Pool size sits between
v4.13 (92,562) and v5.08 (21,923), making this release the third
ordinate in the cross-version comparison.

Same protocol as `linux413_vmlinux` and `linux508_vmlinux`: prediction
target = cost = `vmlinux` uncompressed binary size; storage-bound
`cost(c)` instance.

**Forbidden as features.** Same 21 columns excluded (target `vmlinux`,
18 compressed-image variants, `active_options`, `cid`). After near-
constant pruning and top-K=512 marginal-effect filtering, **497 kernel
options** enter the design matrix.

**Strategies and levels.** Same seven strategies and the same
percentage-based level grid (1%, 2%, 5%, 10%, 20%) as the other
releases. Levels map to `n ∈ {394, 788, 1970, 3939, 7878}`. Diversity
is capped at `n ≤ 1851` and runs at the smallest two levels (n=394,
788).

## Overall result

v4.15 is the **closest direct replication** of the v4.13 calibration
panel:

- `random`, `balanced`, `coverage` are calibrated (ratios within
  ±0.7% of 1.0).
- `diversity` drifts to **2.23×** — third independent confirmation
  that farthest-first in option space biases cost upward by ~2× on
  randconfig pools.
- `uncertainty` median is **0.996** but the per-level breakdown shows
  the same n-dependent seam observed across the three releases (see
  below).

The most interesting cross-version finding is what v4.15 adds to the
`uncertainty` story: when the three releases are aligned by **absolute
sample size** rather than by percentage level, the AL seam becomes
much sharper.

## RQ1: Empirical cost heterogeneity

- min `vmlinux` size: **11.5 MB**
- median `vmlinux` size: **64 MB**
- max `vmlinux` size: **1.87 GB**
- coefficient of variation: **1.16**
- p90/p10 ratio: **6.04**

Note the p90/p10 ratio is **higher** than both v4.13 (4.6) and v5.08
(4.0), even though the CV (1.16) is intermediate. The v4.15 pool has a
similar bulk-shape to v5.08 but with a longer right tail — the ratio
between the 90th and 10th percentile is ~50% larger than in either
neighbour version. This translates into a wider oracle bracket
relative to the cost CV than either neighbour.

## RQ2: Validity of sample size as cost proxy

Spearman ρ(n, train_cost) = **0.966** overall.

| strategy          | runs | median ratio | bias    | IQR              |
| ----------------- | ---- | ------------ | ------- | ---------------- |
| `random`          | 500  | **1.003**    | +0.003  | [0.985, 1.018]   |
| `balanced`        | 500  | **1.000**    | +0.000  | [0.984, 1.016]   |
| `coverage`        | 100  | **1.007**    | +0.007  | [0.997, 1.020]   |
| `uncertainty`     | 100  | **0.996**    | −0.004  | [0.951, 1.138]   |
| `diversity`       | 40   | **2.234**    | +1.234  | [2.176, 2.356]   |
| `cheapOracle`     | 5    | **0.248**    | −0.752  | [0.221, 0.274]   |
| `expensiveOracle` | 5    | **4.955**    | +3.955  | [3.644, 6.931]   |

`diversity` lands at 2.23× — the third independent confirmation, with
v4.13 at 2.28 and v5.08 at 2.02. Three randconfig-induced pools at
three different sizes, three different kernel versions, all show the
same ~2× upward drift for farthest-first. The bias is robust.

Per-level uncertainty calibration (the seam):

| level | n     | uncertainty ratio | uncertainty MRE |
| ----- | ----- | ------------------ | --------------- |
| 1%    | 394   | **0.962**          | 0.356           |
| 2%    | 788   | 1.013              | 0.355           |
| 5%    | 1970  | 0.975              | 0.333           |
| 10%   | 3939  | 0.963              | 0.327           |
| 20%   | 7878  | **1.317**          | 0.284           |

v4.15 puts the seam between n=3939 and n=7878, with a slight
non-monotonicity in the bulk (the 5%/10% ratios dip slightly under
1.0 even though n is well above v5.08's seam point). Aligning all
three releases by absolute n clarifies this:

| absolute n  | v4.13 ratio | v4.15 ratio | v5.08 ratio |
| ----------- | ----------- | ----------- | ----------- |
| ~ 200–400   | —           | 0.96        | 0.67        |
| ~ 800–1000  | —           | 1.01        | 0.93        |
| ~ 2000      | —           | 0.98        | 1.17        |
| ~ 4000–5000 | 1.20        | 0.96        | 1.26        |
| ~ 7000–9000 | 1.29        | 1.32        | —           |
| ~ 18000     | 1.35        | —           | —           |

The seam is **not at a universal absolute n** — v5.08 crosses 1.0
between n=1096 and n=2192, while v4.15 stays slightly below 1.0 even
at n=3939 before jumping to 1.32 at n=7878. So the AL bias mechanism
is sensitive to the joint pool-size × cost-distribution shape, not
just to absolute n. Each pool has its own seam, and a seam exists in
each.

## RQ3: Robustness of conclusions to the cost model

Top-1 strategy-size pair flips for **2 / 7** λ values, mirroring v4.13's
2/7 (vs v5.08's 6/7). Mean Kendall τ ranges from 0.823 (λ=0.5) down
to 0.645 (λ=10).

The two top-1 disagreements both occur at high λ (4 and 10):
count cost picks `uncertainty_n00394`, empirical cost picks
`cheapOracle_n00394`. In every other λ bucket, count and empirical
agree on `uncertainty_n00394` — a striking outcome since this is the
strategy with the lowest median MRE at the smallest n level.

`uncertainty_n00394` being the top-1 across most of the λ range is
itself notable: at this level, AL achieves the best MRE (0.356) of any
strategy while costing slightly *less* than random/balanced
(calibration ratio 0.96). This is the cleanest example yet of AL
producing a Pareto-improvement under empirical cost — better accuracy
*and* lower cost than the calibrated baselines.

## RQ4: Pareto-efficient sampling under empirical cost

Empirical Pareto frontier: **6** strategy-size pairs.
Count Pareto frontier: **6** strategy-size pairs.

Empirical: `uncertainty_n00394`, `cheapOracle_n00394`,
`uncertainty_n00788`, `cheapOracle_n00788`, `uncertainty_n01970`,
`uncertainty_n03939`, `balanced_n07878`, `uncertainty_n07878`.

Wait — the count and empirical frontiers happen to have the same
*cardinality* (5 each, plus uncertainty at every level), but they are
not identical sets. Count Pareto picks `uncertainty_n00394`,
`uncertainty_n00788`, `uncertainty_n01970`, `uncertainty_n03939`,
`balanced_n07878`, `uncertainty_n07878`. Empirical Pareto adds the
two cheap-oracle points (`cheapOracle_n00394`, `cheapOracle_n00788`)
and drops one of the count-frontier points.

Jaccard overlap is 5/8 = **0.625**, the highest across all three
releases. v4.15 is the friendliest release for the size-as-cost
abstraction — count cost gets you most of the right answer here.

## Cross-version comparison with v4.13 and v5.08

| metric                            | v4.13     | v4.15      | v5.08     | replicates? |
| --------------------------------- | --------- | ---------- | --------- | ----------- |
| pool size                         | 92,562    | 39,391     | 21,923    | n/a         |
| cost CV                           | 1.43      | 1.16       | 1.01      | direction yes; magnitude monotone in pool size |
| p90/p10 cost ratio                | 4.61      | **6.04**   | 4.02      | non-monotone |
| Spearman ρ(n, cost)               | 0.966     | 0.966      | 0.967     | yes         |
| `random` calibration              | 0.999     | 1.003      | 0.999     | yes         |
| `balanced` calibration            | 0.999     | 1.000      | 0.999     | yes         |
| `coverage` calibration            | 0.974     | 1.007      | 0.994     | yes         |
| **`diversity` calibration**       | **2.281** | **2.234**  | **2.019** | **yes**     |
| **`uncertainty` calibration**     | 1.246     | 0.996      | 0.946     | n-dependent (no universal seam) |
| `cheapOracle` calibration         | 0.292     | 0.248      | 0.319     | similar     |
| `expensiveOracle` calibration     | 5.640     | 4.955      | 4.199     | direction yes; magnitude weaker on smaller pools |
| top-1 RQ3 flips (out of 7 λ)      | 2         | 2          | 6         | yes (5.08 outlier) |
| count-Pareto cardinality          | 5         | 6          | 4         | similar     |
| empirical-Pareto cardinality      | 11        | 8          | 8         | similar     |
| Jaccard(count, empirical Pareto)  | 0.45      | **0.625**  | 0.50      | similar     |

Findings that replicate cleanly across all three releases:

1. **`diversity` ≈ 2× upward drift.** Three pools, three
   confirmations. The most robust finding in the study.
2. **`random` / `balanced` / `coverage` are calibrated.** Cost-blind
   strategies that don't involve a similarity / residual signal
   on the option matrix do not drift.
3. **Empirical Pareto frontier ≥ count Pareto frontier** in
   cardinality, with a Jaccard overlap of 0.45–0.625.
4. **Cost heterogeneity is large** (CV ≥ 1, p90/p10 ≥ 4) on all
   three pools.
5. **The cheap-tail oracle is empirically Pareto-relevant at small n**
   on all three pools.

Findings that depend on the release:

1. The **uncertainty seam location** depends on the pool, not just
   on absolute n. v4.13 is past the seam everywhere; v5.08 has the
   seam mid-grid; v4.15 has the seam late, with a non-monotone
   ratio in the bulk.
2. **RQ3 top-1 instability** is dramatic on v5.08 (6/7 flips) but
   modest on v4.13 and v4.15 (2/7 each).
3. The **oracle bracket magnitude** is monotone in cost CV: v4.13
   (CV 1.43, expensive 5.64×) > v4.15 (CV 1.16, expensive 4.95×) >
   v5.08 (CV 1.01, expensive 4.20×).

## Threats specific to this release

- **Pool size 39K** — intermediate; AL-seam analysis is only as good
  as the level grid resolves. Adding more levels (e.g. 0.5%, 1.5%,
  3%) on this pool would tighten the seam location.
- **Highest p90/p10 (6.04)** with a moderate CV (1.16) — the v4.15
  cost distribution has a longer right tail than v4.13 even though
  the variance is smaller. Worth noting if the paper uses CV as the
  primary heterogeneity metric.
- All other threats from `linux413_vmlinux_report.md` apply identically.

## Generated artifacts

Identical layout to `artifacts/linux413_vmlinux/`. See
`artifacts/linux_kernels_summary.md` for the cross-release narrative.
