# `linux508_vmlinux` with empirical `vmlinux` acquisition cost

## Scope and protocol

This report covers TuxKConfig **Linux 5.08** (OpenML 46744, Borges et
al., EASE 2025), a pool of **21,923 valid kernel configurations** drawn
with `make randconfig` on the v5.8 kernel tree. The smaller pool size
(vs 92,562 on v4.13) is a property of the published artifact, not of
the kernel itself. Same protocol as `linux413_vmlinux`: prediction
target = cost = `vmlinux` uncompressed binary size; storage-bound
`cost(c)` instance.

**Forbidden as features.** Same 21 columns as in `linux413_vmlinux`
(target `vmlinux`, 18 compressed-image variants, `active_options`,
`cid`). After near-constant pruning and top-K=512 marginal-effect
filtering, **494 kernel options** enter the design matrix.

**Strategies and levels.** Same seven strategies and the same percentage-
based level grid (1%, 2%, 5%, 10%, 20%) as v4.13. With pool size 21,923,
levels map to `n ∈ {219, 438, 1096, 2192, 4385}`. Diversity is capped
at `n ≤ 1851` (so it runs at the smallest three levels: n=219, 438,
1096; diversity at n=2192/4385 is skipped).

## Overall result

The cross-version replication is the headline. Two of the three
new strategies behave the same way as on v4.13; one diverges in a
diagnostic way:

- **`diversity`** drifts to **2.02×** (median; range 1.84–2.26 across
  levels). Same direction, similar magnitude as v4.13's 2.28. **Robust
  cross-version replication.**
- **`coverage`** drifts to **0.99×**. Calibrated, matches v4.13.
- **`random`** and **`balanced`** stay at **1.000**. Calibrated, matches.
- **`uncertainty`** has a **bimodal-in-n calibration ratio**: 0.67 at
  n=219, 0.81 at n=438, 0.93 at n=1096, 1.17 at n=2192, 1.26 at n=4385.
  Median across levels is 0.95, but that median hides a clear sign-flip
  with sample size. **Does not replicate the v4.13 monotone-up
  pattern.**

The other striking divergence is RQ3: **6 / 7 λ values flip the top-1
strategy-size pair** on v5.08, vs only 2 / 7 on v4.13. The two pools
share the calibration story but disagree sharply on which
strategy-size choice is decision-optimal under different cost models.

## RQ1: Empirical cost heterogeneity

- min `vmlinux` size: **11.6 MB**
- median `vmlinux` size: **71 MB**
- max `vmlinux` size: **2.00 GB**
- coefficient of variation: **1.01**
- p90/p10 ratio: **4.0**

Cost CV (1.01) is lower than v4.13 (1.43); the cost distribution is
slightly less heavy-tailed. Min and median are both ~10× larger than
v4.13's, reflecting the v5.x kernel's larger baseline footprint —
the smallest valid v5.08 randconfig is bigger than the median v4.13
randconfig. The max is similar (~2 GB on both versions).

Strategy overhead vs random (median across levels) ranges from
**0.275×** (cheapOracle at n=219) to **8.385×** (expensiveOracle at
n=219).

## RQ2: Validity of sample size as cost proxy

Spearman ρ(n, train_cost) = **0.967** overall.

| strategy          | runs | median ratio | bias    | IQR              |
| ----------------- | ---- | ------------ | ------- | ---------------- |
| `random`          | 500  | **0.999**    | −0.001  | [0.979, 1.017]   |
| `balanced`        | 500  | **0.999**    | −0.001  | [0.980, 1.019]   |
| `coverage`        | 100  | **0.994**    | −0.006  | [0.983, 1.008]   |
| `uncertainty`     | 100  | **0.946**    | −0.054  | [0.821, 1.208]   |
| `diversity`       | 60   | **2.019**    | +1.019  | [1.857, 2.127]   |
| `cheapOracle`     | 5    | **0.319**    | −0.681  | [0.288, 0.352]   |
| `expensiveOracle` | 5    | **4.199**    | +3.199  | [3.049, 6.320]   |

**Diversity bias replicates almost exactly**: 2.02× on v5.08 vs 2.28×
on v4.13. The mechanism is robust — farthest-first in option space
selects high-Hamming-distance configs, which on randconfig pools means
configs with many subsystems enabled, which means large kernels.

**Uncertainty does not replicate** in median, and the per-level
breakdown explains why:

| level | n     | uncertainty ratio | uncertainty MRE |
| ----- | ----- | ------------------ | --------------- |
| 1%    | 219   | **0.669**          | 0.358           |
| 2%    | 438   | 0.805              | 0.340           |
| 5%    | 1096  | 0.931              | 0.317           |
| 10%   | 2192  | 1.173              | 0.318           |
| 20%   | 4385  | **1.262**          | 0.285           |

The ratio crosses 1.0 between 5% and 10%, monotone in n. At small n
the seed (~⌈n/4⌉ ≈ 55 configs) is too small to model the heavy tail;
absolute residuals concentrate on small/cheap configs, pulling the
sampler toward the **cheap** end of the distribution. As n grows the
seed becomes representative and AL pulls toward the **expensive** end
(matching the v4.13 pattern). The wide IQR [0.82, 1.21] in the
aggregate row reflects this seam, not within-level noise.

This is a finding the v4.13 result alone could not have produced: AL's
cost bias is **n-dependent and pool-size-dependent**, and a paper
that reported only v4.13 would have claimed a one-directional drift.
The cross-version replication is the only reason we see the seam.

## RQ3: Robustness of conclusions to the cost model

**Top-1 strategy-size pair flips for 6 / 7 λ values** — a much stronger
RQ3 signal than v4.13's 2 / 7. Mean Kendall τ ranges from 0.807
(λ=0.1) down to 0.629 (λ=10).

The rank-stability table shows count-cost essentially always picking
`random_n00219` (the 1% level, smallest n), while empirical cost picks
`uncertainty_n00438` or `uncertainty_n00219` for most λ — uncertainty's
cheap-leaning bias at small n makes it the empirical-cost winner once
the cost term has any weight. Under count cost, all 1% strategies tie
on n and the lowest-MRE wins (random); under empirical cost,
uncertainty's smaller training cost dominates.

This is the cleanest example so far in the project of count-based
effort hiding the actual cost-optimal choice. The reason it is so
visible on v5.08 is that the smaller pool produces both a finer
calibration seam (uncertainty crosses 1.0 within the level grid) and
a cost distribution where the cheap tail is closer to the centre of
mass.

## RQ4: Pareto-efficient sampling under empirical cost

Empirical Pareto frontier: **8** strategy-size pairs.
Count Pareto frontier: **4** strategy-size pairs.

Empirical-only points (4):
- `uncertainty_n00219` — the cheap-side AL point that count cannot see.
- `cheapOracle_n00219`, `cheapOracle_n00438` — the cheap-tail oracle.
- `random_n04385` — co-dominates with uncertainty at the 20% level.

The pattern matches v4.13's qualitatively: count cost concentrates the
frontier on a small per-level winner; empirical cost adds the cheap-tail
points and surfaces co-dominant deployable strategies. The Jaccard
agreement is 4/8 = 0.50, similar to v4.13's 5/11 = 0.45.

## Cross-version comparison with v4.13

| metric                          | linux413_vmlinux | linux508_vmlinux | replicates? |
| ------------------------------- | ---------------- | ---------------- | ----------- |
| pool size                       | 92,562           | 21,923           | n/a         |
| cost CV                         | 1.43             | 1.01             | weaker on 5.08 |
| p90/p10 cost ratio              | 4.6              | 4.0              | similar     |
| Spearman ρ(n, cost)             | 0.966            | 0.967            | yes         |
| `random` calibration            | 0.999            | 0.999            | yes         |
| `balanced` calibration          | 0.999            | 0.999            | yes         |
| `coverage` calibration          | 0.974            | 0.994            | yes         |
| **`diversity` calibration**     | **2.281**        | **2.019**        | **yes**     |
| **`uncertainty` calibration**   | **1.246**        | **0.946**        | **divergent** |
| `cheapOracle` calibration       | 0.292            | 0.319            | similar     |
| `expensiveOracle` calibration   | 5.640            | 4.199            | weaker on 5.08 |
| top-1 RQ3 flips (out of 7 λ)    | 2                | **6**            | divergent   |
| empirical-Pareto cardinality    | 11               | 8                | similar     |
| count-Pareto cardinality        | 5                | 4                | similar     |

Two findings replicate strongly: deployable cost-blind strategies
(`random`, `balanced`, `coverage`) are calibrated on both versions, and
`diversity` drifts to ~2× on both. Three findings diverge in
informative ways: `uncertainty`'s bias is n-dependent and changes sign
across pool sizes, RQ3 is dramatically more unstable on v5.08, and the
oracle bracket is narrower (the v5.08 cost distribution is less heavy-
tailed). Each divergence has a mechanistic explanation rooted in the
pool's joint geometry-cost distribution.

## Threats specific to this release

- **Smaller pool than v4.13.** 21,923 vs 92,562 configurations. The
  AL-seam finding (uncertainty's sign-flip with n) might be partly a
  pool-size effect: with 4× fewer rows the seed becomes representative
  more slowly. A direct test would be to subsample v4.13 to 21K rows
  and rerun — flagged as future work.
- **Cost CV 1.01 < v4.13's 1.43.** The v5.08 randconfig pool is less
  heavy-tailed; some of the v4.13 oracle-driven effects therefore
  appear weaker here.
- **Diversity capped at n ≤ 1851.** On the smaller pool this still
  covers the smallest three levels (1%, 2%, 5% = n=219, 438, 1096) —
  better proportional coverage than v4.13.
- All other threats from `linux413_vmlinux_report.md` apply identically.

## Generated artifacts

Identical layout to `artifacts/linux413_vmlinux/`. See
`artifacts/linux_kernels_summary.md` for the cross-release narrative.
