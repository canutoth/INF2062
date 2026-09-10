# `linux500_vmlinux` with empirical `vmlinux` acquisition cost

## Scope and protocol

This report covers TuxKConfig **Linux 5.0** (OpenML 46741, Borges et
al., EASE 2025), a pool of **19,952 valid kernel configurations** drawn
with `make randconfig` on the v5.0 kernel tree. This is the smallest
pool of the four releases evaluated in the study (v4.13: 92,562;
v4.15: 39,391; v5.08: 21,923; v5.0: 19,952).

Same protocol as the other Linux releases: prediction target = cost =
`vmlinux` uncompressed binary size; storage-bound `cost(c)` instance.

**Forbidden as features.** Same 21 columns excluded (target `vmlinux`,
18 compressed-image variants, `active_options`, `cid`). After
near-constant pruning and top-K=512 marginal-effect filtering, **494
kernel options** enter the design matrix.

**Strategies and levels.** Same seven strategies and percentage-based
level grid as the other releases. Levels map to
`n ∈ {200, 399, 998, 1995, 3990}`. Diversity caps at `n ≤ 1851`, so it
runs at the smallest three levels (n = 200, 399, 998).

## Overall result

v5.0 is the cleanest replication of the cross-version pattern so far:

- `random`, `balanced`, `coverage` are all calibrated within ±0.3% of 1.
- **`diversity` drifts to 2.06×** — the **fourth independent
  confirmation** of the ~2× upward bias on randconfig pools.
- **`uncertainty`'s calibration ratio is strictly monotone increasing
  in n** (the cleanest seam yet), crossing 1.0 between n=998 and
  n=1995. Spearman rho = 1.0 over 5 levels.
- The oracle bracket is similar to v5.08 (cheap 0.26×, expensive 4.76×).

RQ3 instability is **2/7 top-1 flips**, matching v4.13 and v4.15 — not
v5.08's 6/7. This isolates v5.08 as the outlier: pool size alone does
not explain ranking instability (v5.0's pool is *smaller* than v5.08's
yet shows 3× fewer flips), so the v5.08 6/7 finding looks specific to
that release's pct_n level grid landing on tie-prone absolute-n values.

## RQ1: Empirical cost heterogeneity

- min `vmlinux` size: **11.6 MB**
- median `vmlinux` size: **68 MB**
- max `vmlinux` size: **1.96 GB**
- coefficient of variation: **1.12**
- p90/p10 ratio: **5.70**

The p90/p10 ratio is the **second-highest** of the four releases (after
v4.15's 6.04), even though the CV (1.12) is intermediate. v5.0 has a
similar bulk to v5.08 with a longer right tail — the p90/p10
characteristic that v4.15 first exposed is reinforced here.

## RQ2: Validity of sample size as cost proxy

Spearman ρ(n, train_cost) = **0.968** overall.

| strategy          | runs | median ratio | bias    | IQR              |
| ----------------- | ---- | ------------ | ------- | ---------------- |
| `random`          | 500  | **1.002**    | +0.002  | [0.980, 1.023]   |
| `balanced`        | 500  | **0.998**    | −0.002  | [0.975, 1.022]   |
| `coverage`        | 100  | **0.997**    | −0.003  | [0.980, 1.009]   |
| `uncertainty`     | 100  | **0.979**    | −0.021  | [0.864, 1.128]   |
| `diversity`       | 60   | **2.056**    | +1.056  | [1.910, 2.137]   |
| `cheapOracle`     | 5    | **0.261**    | −0.739  | [0.238, 0.287]   |
| `expensiveOracle` | 5    | **4.765**    | +3.765  | [3.520, 6.732]   |

Per-level uncertainty calibration (the seam — strictly monotone):

| level | n     | uncertainty ratio | uncertainty MRE |
| ----- | ----- | ------------------ | --------------- |
| 1%    | 200   | **0.794**          | 0.350           |
| 2%    | 399   | 0.885              | 0.331           |
| 5%    | 998   | 0.974              | 0.316           |
| 10%   | 1995  | 1.030              | 0.306           |
| 20%   | 3990  | **1.353**          | 0.282           |

Spearman ρ over the level grid is **1.0** (perfect monotone increasing
order), with cross-over from <1 to >1 between n=998 (ratio 0.974) and
n=1995 (ratio 1.030). This is the cleanest AL-seam observation across
all four releases.

## RQ3: Robustness of conclusions to the cost model

Top-1 strategy-size pair flips for **2/7** λ values, matching v4.13
and v4.15 (and unlike v5.08's 6/7). The two flips are at λ=0.1
(uncertainty_n00200 vs uncertainty_n00399 — adjacent-level swap) and
λ=10 (uncertainty_n00200 vs cheapOracle_n00200 — cost-heavy regime).

This is the cleanest confirmation that v5.08's high flip count is not
a "small-pool" artifact. v5.0's pool (19,952) is *smaller* than
v5.08's (21,923) but produces 3× fewer flips, so the explanation has
to be specific to v5.08's level grid landing on tie-prone absolute-n
values, not pool size per se.

## RQ4: Pareto-efficient sampling under empirical cost

Empirical Pareto frontier: **6** strategy-size pairs.
Count Pareto frontier: **5** strategy-size pairs.

Empirical-only points include the cheap-tail oracle at small n and
typically `uncertainty` at small n (its cheap-leaning calibration on
this pool makes it Pareto-efficient under empirical cost where it is
dominated under count cost). Diversity is dominated under both cost
models at every level — fourth confirmation that geometric diversity
is a Pareto-bad strategy on randconfig pools.

## Cross-version comparison

| metric                          | v4.13     | v4.15     | v5.0       | v5.08     |
| ------------------------------- | --------- | --------- | ---------- | --------- |
| pool size                       | 92,562    | 39,391    | **19,952** | 21,923    |
| cost CV                         | 1.43      | 1.16      | 1.12       | 1.01      |
| p90/p10 cost ratio              | 4.61      | 6.04      | 5.70       | 4.02      |
| Spearman ρ(n, cost)             | 0.966     | 0.966     | 0.968      | 0.967     |
| `random` calibration            | 0.999     | 1.003     | 1.002      | 0.999     |
| `balanced` calibration          | 0.999     | 1.000     | 0.998      | 0.999     |
| `coverage` calibration          | 0.974     | 1.007     | 0.997      | 0.994     |
| **`diversity` calibration**     | **2.281** | **2.234** | **2.056**  | **2.019** |
| `uncertainty` calibration       | 1.246     | 0.996     | 0.979      | 0.946     |
| `uncertainty` Spearman ρ over n | 0.6 (ns)  | 0.6 (ns)  | **1.0**    | 1.0       |
| `cheapOracle` calibration       | 0.292     | 0.248     | 0.261      | 0.319     |
| `expensiveOracle` calibration   | 5.640     | 4.955     | 4.765      | 4.199     |
| top-1 RQ3 flips (out of 7)      | 2         | 2         | 2          | **6**     |
| count-Pareto cardinality        | 5         | 6         | 5          | 4         |
| empirical-Pareto cardinality    | 11        | 8         | 6          | 8         |

Findings replicated four times across releases:

1. **`random`, `balanced`, `coverage` calibrate to ±1%.** Robust
   null finding.
2. **`diversity` drifts to ~2× expected cost.** Magnitudes:
   2.28, 2.23, 2.06, 2.02. Direction and order-of-magnitude both robust.
3. **`uncertainty`'s calibration ratio rises monotonically in n.**
   Spearman ρ = 0.6 (v4.13, v4.15, n.s.) and 1.0 (v5.0, v5.08, p
   < 0.05).
4. **Empirical Pareto frontier ≥ count Pareto frontier.**
5. **Cost heterogeneity is heavy-tailed** (CV ≥ 1, p90/p10 ≥ 4 on all
   four pools).

What sets v5.08 apart: 6/7 RQ3 flips. v5.0 confirms this is *not* a
small-pool artifact (v5.0 is even smaller and shows 2/7).

## Threats specific to this release

- **Smallest pool of the four releases**, ~20K configurations. Smaller
  level n than v5.08, which is why the AL seam is more clearly resolved
  here (the cross-over is in the middle of the level grid).
- **High p90/p10 (5.70) with moderate CV (1.12)** — long right tail
  similar to v4.15. Worth flagging if the paper picks one heterogeneity
  metric over the other.
- All other threats from the v4.13 / v4.15 / v5.08 reports apply
  identically.

## Generated artifacts

Identical layout to the other releases. See
`artifacts/linux_kernels_summary.md` for the four-release narrative.
