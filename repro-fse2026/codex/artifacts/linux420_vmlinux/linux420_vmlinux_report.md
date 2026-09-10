# `linux420_vmlinux` with empirical `vmlinux` acquisition cost

## Scope and protocol

This report covers TuxKConfig **Linux 4.20** (OpenML 46740, Borges et
al., EASE 2025), a pool of **23,489 valid kernel configurations**.
Same protocol as the other Linux releases: target = cost = `vmlinux`
uncompressed binary size; storage-bound `cost(c)`. After near-constant
pruning and top-K=512 marginal-effect filtering, **494 kernel options**
enter the design matrix.

Sample sizes for the percentage-based level grid: `n ∈ {235, 470,
1174, 2349, 4698}`. Diversity caps at `n ≤ 1851`, so it runs at the
smallest three levels.

## Headline result

v4.20 is another clean replication of the four earlier panels:

- `random`, `balanced`, `coverage` calibrated to ±0.2%.
- **`diversity` drifts to 2.27×** — fifth confirmation of the ~2×
  upward bias.
- `uncertainty` median 0.94, with a near-monotone seam (one mid-grid
  dip).
- RQ3: **2/7 top-1 flips** — joins the v4.13/v4.15/v5.0 cluster, not
  v5.08.

## RQ1: Cost heterogeneity

- min/median/max `vmlinux`: 11.6 MB / 64 MB / **2.13 GB** (the largest
  max of the five releases so far).
- CV: **1.16**.
- p90/p10: **5.80**.

The p90/p10 ratio is in the high group with v4.15 (6.04) and v5.0
(5.70). Like those releases, v4.20 has a moderate CV but a long
right tail.

## RQ2: Calibration ratios

| strategy          | runs | median ratio | bias    | IQR              |
| ----------------- | ---- | ------------ | ------- | ---------------- |
| `random`          | 500  | **1.002**    | +0.002  | [0.981, 1.022]   |
| `balanced`        | 500  | **0.998**    | −0.002  | [0.979, 1.021]   |
| `coverage`        | 100  | **1.001**    | +0.001  | [0.988, 1.012]   |
| `uncertainty`     | 100  | **0.943**    | −0.057  | [0.834, 1.096]   |
| `diversity`       | 60   | **2.269**    | +1.269  | [1.969, 2.439]   |
| `cheapOracle`     | 5    | **0.260**    | −0.740  | [0.235, 0.285]   |
| `expensiveOracle` | 5    | **4.877**    | +3.877  | [3.582, 6.931]   |

`uncertainty` per-level (the seam):

| level | n     | ratio    | MRE   |
| ----- | ----- | -------- | ----- |
| 1%    | 235   | **0.772**| 0.368 |
| 2%    | 470   | 0.918    | 0.347 |
| 5%    | 1174  | 0.899    | 0.346 |
| 10%   | 2349  | 0.957    | 0.332 |
| 20%   | 4698  | **1.255**| 0.291 |

Direction is consistent (cheap-leaning at small n, expensive-leaning
at n=4698) but with one mid-grid dip at the 5% level (0.92 → 0.90),
similar to v4.15. Spearman ρ over n is positive but not strictly
monotone; the seam crosses 1.0 between n=2349 and n=4698.

## RQ3: Robustness of conclusions

**2/7** top-1 flips (matches v4.13, v4.15, v5.0). Top-1 is
`uncertainty_n00235` for every λ except 0.1 (adjacent-level swap to
n=470) and 10 (cost-heavy swap to `cheapOracle_n00235`).

## RQ4: Pareto frontiers

Empirical Pareto frontier: 7 strategy-size pairs.
Count Pareto frontier: 5.

The empirical frontier adds the cheap-tail oracle and the
cheap-leaning AL points at small n. `diversity` is dominated under
both cost models at every level.

## Cross-version pointers

`diversity` calibration so far: 2.28 (v4.13), 2.23 (v4.15), 2.27
(v4.20), 2.06 (v5.0), 2.02 (v5.08). The five-release window
[2.02, 2.28] is even tighter than the three-release window the plan
budgeted for.

`uncertainty` cross-over n on this release sits between n=2349 and
n=4698, similar to v4.15's cross-over in roughly the same absolute-n
neighbourhood. The four-release seam picture in
`linux_kernels_summary.md` (and the regenerated 5/6/7-release
versions) covers v4.20 as another point in the bulk.
