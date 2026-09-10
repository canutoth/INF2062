# `linux413_vmlinux` with empirical `vmlinux` acquisition cost

## Scope and protocol

This report covers TuxKConfig **Linux 4.13** (OpenML 46759, Borges et al.,
EASE 2025), a pool of **92,562 valid kernel configurations** drawn with
`make randconfig`. The prediction target and empirical acquisition cost
are both the uncompressed kernel binary size (`vmlinux`); the cost
construct is the storage-bound case of `cost(c)` (the published artifact
does not ship build time).

**Forbidden as features.** Twenty-one columns are excluded from the
design matrix (`cost_sampling.linux_data.NON_OPTION_COLUMNS`):

- `vmlinux` — the prediction target.
- 18 compressed-image variants
  ({GZIP, BZIP2, LZMA, XZ, LZO, LZ4} × {bzImage, vmlinux, raw}) — all
  functions of the same kernel build and tightly correlated with the
  target; including any of them would let the learner short-circuit the
  option vector.
- `active_options` — count of enabled options, exactly derivable from
  the option vector itself; would collapse ridge to a size-of-config
  regression.
- `cid` — row identifier.

The runner asserts on load that no forbidden column survives into
`feature_names`. After near-constant pruning (minor-class ≥ 50) and a
top-K=512 marginal-effect filter, **495 kernel options** enter the
design matrix.

**Strategies (seven, all pool-based).** Five are deployable, two are
diagnostic oracles:

| strategy           | runs | levels      | reads cost? | role                          |
| ------------------ | ---- | ----------- | ----------- | ----------------------------- |
| `random`           | 100  | 5           | no          | reference baseline            |
| `balanced`         | 100  | 5           | no          | active-options decile strata  |
| `diversity`        | 20   | 2 (n≤1851)  | no          | farthest-first in Hamming     |
| `uncertainty`      | 20   | 5           | no          | residual-driven active learning |
| `coverage`         | 20   | 5           | no          | greedy option-frequency match |
| `cheapOracle`      | 1    | 5           | yes         | lower-bound diagnostic        |
| `expensiveOracle`  | 1    | 5           | yes         | upper-bound diagnostic        |

Levels: 1%, 2%, 5%, 10%, 20% of the pool ⇒ `n ∈ {926, 1851, 4628, 9256,
18512}`. Diversity is capped at `n ≤ 1851` because its `O(n²)` cost
becomes prohibitive at larger sizes. The learner is the existing
`fit_ridge` log-linear model with `α=1.0`. MRE is computed on the
complement of the training sample within the 92,562-row pool, with
chunked predictions (4096 rows/chunk).

## Overall result

The richer strategy panel turns the v1 finding (random/balanced perfectly
calibrated, oracles wildly off) into a clearer mid-band story: **two of
the three new deployable strategies bias the calibration ratio in
specific, non-trivial ways, while the third is well-behaved.** Concretely:

- `diversity` (farthest-first) drifts to a calibration ratio of
  **2.28×** (median, IQR [2.22, 2.40]). Geometric diversity in option
  space correlates strongly with cost — high-Hamming-distance configs
  are systematically the larger kernels.
- `uncertainty` (active learning) drifts to **1.25×** (IQR [1.13, 1.33]),
  with the bias *increasing* in n: 1.20 at n=926, 1.35 at n=18512.
  Residual-driven selection pulls toward cost-extreme configs.
- `coverage` (option-frequency matching) is essentially calibrated at
  **0.97×**.
- `random` and `balanced` are calibrated to **1.000** (IQR [0.987, 1.013]).
- The oracle bracket spans **0.29× to 5.64×** (median; up to **11.5×**
  at the smallest level).

This is the qualitative shift the v1 panel was missing: the
miscalibration story is no longer "only oracles bend the proxy" — it is
"diversity-aware and active-learning samplers, which a real practitioner
might run to look smart, drift the calibration ratio by 25–125%."

## RQ1: Empirical cost heterogeneity

The pool exhibits the largest per-configuration cost spread we have:

- min `vmlinux` size: **1.17 MB**
- median `vmlinux` size: **31 MB**
- max `vmlinux` size: **1.78 GB**
- coefficient of variation: **1.43**
- p90/p10 ratio: **4.6**

Strategy overhead vs random (median across all levels):

- `random`: 1.000 (reference)
- `balanced`: 0.999–1.012 across levels
- `coverage`: 0.974–0.992 across levels
- `uncertainty`: 1.111–1.348 across levels (increasing in n)
- `diversity`: 2.230–2.247 across the two evaluated levels
- `cheapOracle`: 0.232–0.405 (decreasing in n)
- `expensiveOracle`: 2.221–11.49 (decreasing in n)

The fixed-n cost spread between deployable strategies alone is
**0.97× to 2.40×** — a factor of ~2.5 between two strategies a
practitioner might plausibly choose. The count cost model assigns these
samples identical effort.

## RQ2: Validity of sample size as cost proxy

Spearman ρ(n, train_cost) = **0.966** overall. Per-strategy calibration
ratios:

| strategy          | runs | median ratio | bias    | IQR              |
| ----------------- | ---- | ------------ | ------- | ---------------- |
| `random`          | 500  | **0.999**    | −0.001  | [0.988, 1.013]   |
| `balanced`        | 500  | **0.999**    | −0.001  | [0.986, 1.012]   |
| `coverage`        | 100  | **0.974**    | −0.026  | [0.967, 0.983]   |
| `uncertainty`     | 100  | **1.246**    | +0.246  | [1.130, 1.328]   |
| `diversity`       | 40   | **2.281**    | +1.281  | [2.222, 2.399]   |
| `cheapOracle`     | 5    | **0.292**    | −0.708  | [0.254, 0.325]   |
| `expensiveOracle` | 5    | **5.640**    | +4.640  | [3.907, 8.691]   |

`uncertainty` and `diversity` are the headline result. Both are
deployable, neither reads the cost signal, both drift the calibration
ratio substantially upward — diversity by ~125%, active learning by
~25%.

**Why it happens, mechanically.** Both strategies are biased toward
*atypical* configurations: farthest-first picks rows that are far from
the bulk of the pool in Hamming distance, residual-driven AL picks rows
where a small ridge model errs most. On TuxKConfig 4.13 those atypical
rows are dominated by **large kernels with many subsystems enabled** —
which are also the cost-heaviest rows. The cost bias is not a property
of the strategy abstractly; it is a property of the pool's
joint distribution between option-vector geometry and binary size.

The uncertainty bias also has a clear **n-dependence**: ratio rises from
1.20 at n=926 to 1.35 at n=18512. As the seed grows the ridge model
gets better at the bulk, leaving residual mass concentrated on the
extremes — a direct consequence of pool-AL operating on a heavy-tailed
target.

## RQ3: Robustness of conclusions to the cost model

Across 7 λ values, the top-1 strategy-size pair changes for **2 / 7** λ.
Mean Kendall τ between count-based and empirical-cost rankings ranges
from **0.835** (λ=0.1) down to **0.601** (λ=10).

The two top-1 disagreements:

- λ=0.1: count picks `balanced_n00926`, empirical picks
  `balanced_n01851`. At very low cost weight the cost term barely
  matters; the disagreement reflects rounding in MRE differences.
- λ=10: count picks `balanced_n00926`, empirical picks
  `cheapOracle_n00926`. At extreme cost weight, the empirical model
  surfaces the (otherwise oracle-only) cheap-first as the cost-cheapest
  option, while count cost cannot distinguish strategies that have the
  same n.

A more striking observation comes from the n=18512 row of the strategy
summary: **uncertainty has the lowest median MRE (0.178) of any
strategy**, beating random (0.208) and balanced (0.208) by ~15%. Under
count cost, uncertainty therefore wins the n=18512 level outright —
both by accuracy and by ties on n. Under empirical cost, uncertainty
costs **35% more** than balanced at the same n (calibration ratio
1.35), and the ranking flips toward balanced/random for cost-heavy λ.
This is exactly the kind of decision-flip RQ3 was designed to surface.

## RQ4: Pareto-efficient sampling under empirical cost

The empirical-cost Pareto frontier contains **11** strategy-size pairs;
the count-cost frontier contains **5**.

Count-cost Pareto frontier (5 points):
- `balanced_n00926`, `balanced_n01851`, `random_n04628`,
  `balanced_n09256`, `uncertainty_n18512`.

Empirical-cost Pareto frontier (11 points):
- All five count-frontier points, plus
  `coverage_n00926`, `cheapOracle_n00926`, `random_n01851`,
  `cheapOracle_n01851`, `random_n09256`, `balanced_n18512`.

The empirical frontier surfaces three categories of points the count
frontier hides:

1. **Coverage at small n** (`coverage_n00926`) — slightly worse MRE
   than `balanced_n00926` but lower empirical cost (0.97×). Under
   count cost, dominated by balanced; under empirical, undominated.
2. **Cheap-oracle at small n** — same ranking flip as v1, robust.
3. **Random / balanced co-dominance at multiple levels** — the count
   frontier locks in one deployable choice per level; empirical
   cost shows that random and balanced trade off MRE for cost in
   ways the count model erases.

Notably, **diversity is dominated under both cost models** — it pays
2.3× the cost of random while delivering ~2.3× the MRE. Geometric
diversity is a Pareto-bad strategy on this pool, full stop.

## Where this dataset disagrees with the x264 story

| dimension                                       | x264_time_*       | linux413_vmlinux             |
| ----------------------------------------------- | ----------------- | ---------------------------- |
| cost CV                                         | ≈ 0.25            | **1.43**                     |
| p90/p10                                         | ≈ 2.0             | **4.6**                      |
| Spearman ρ(n, cost)                             | 0.943             | **0.966**                    |
| deployable-strategy calibration spread          | henard 0.75, twise 1.10 | diversity 2.28, uncertainty 1.25 |
| count-vs-empirical Pareto cardinality (count vs emp) | 5 vs 8 (median)  | 5 vs 11                      |
| top-1 ranking flips                             | 6 / 119 (5%)      | 2 / 7 (29%)                  |

Both datasets support the central claim — count-based effort is an
incomplete cost model — but for different reasons. On x264 the
mechanism is mild fixed-direction bias from synthesis-style samplers
(henard cheaper, twise costlier). On Linux the mechanism is **stronger
direction-of-bias for diversity-aware and AL-style strategies, plus a
heavy-tailed cost distribution that makes the cheap tail a Pareto-
relevant region under empirical cost**.

## Threats specific to this dataset

- **No build-time signal.** Cost here is uncompressed binary size; build
  time is the practically interesting acquisition cost but is absent
  from the published artifact.
- **Single sampling distribution upstream.** The pool is randconfig-
  induced; pool-based subsampling evaluates strategies *conditional on*
  randconfig.
- **No synthesis strategies.** True t-wise, distance-based on the
  formal model, solver-based — none are evaluable here.
- **Top-K feature pruning.** The learner sees the 495 most informative
  kernel options. RQ1 / RQ2 metrics are computed on the full pool and
  do not depend on what columns the ridge sees; RQ3 / RQ4 metrics
  involve MRE and inherit the pruning sensitivity.
- **Diversity capped at n ≤ 1851.** Compute scales as `O(n² × features)`;
  the largest two levels are missing for that strategy. The drift is
  observed at both evaluated levels and decreases mildly with n
  (2.40 → 2.22), so the trend is unlikely to flip at larger n, but the
  point is flagged.
- **Oracles are diagnostic, not deployable.** They use the cost signal
  we are calibrating against.

## Paper-level takeaway

For `linux413_vmlinux`, sample size is a strong rank-predictor of
empirical cost (ρ = 0.97), but on **deployable, cost-blind strategies**
the calibration ratio splits into three regimes:

- **Calibrated** (ratio ≈ 1): `random`, `balanced`, `coverage`.
- **Modestly biased upward** (ratio ≈ 1.25): `uncertainty` /
  active learning.
- **Strongly biased upward** (ratio ≈ 2.3): `diversity` /
  farthest-first.

This is the v1 finding sharpened: count-based effort is not just an
incomplete *aggregate* cost model — it is **strategy-specific**, with a
gap that rises to >2× for one of the most popular diversity heuristics
in the configurable-systems literature. The combined paper claim with
the x264 results is now:

> Count-based effort hides cost-relevant decisions in three concrete
> ways observable on configurable-system data: (i) on systems where
> sampling strategies select cost-biased regions of the configuration
> space (x264, henard/twise; Linux, diversity/uncertainty), the bias
> is invisible to count cost and accumulates with sample size;
> (ii) on systems with heavy-tailed per-configuration cost (Linux),
> the cheap tail is Pareto-relevant under empirical cost and ignored
> under count cost; (iii) under cost-heavy λ, count-based and
> empirical-cost rankings disagree on the best strategy-size choice.
> All three pathologies are testable per-system before committing to a
> sampling protocol; we provide the metrics for doing so.

## Generated artifacts

- `records.csv` — one row per (strategy, level, run).
- `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`,
  `rq3_rank_stability.csv`, `rq4_pareto.csv`, `strategy_summary.csv` —
  standard analysis outputs.
- `linux_feature_columns.csv` — 495 retained kernel options.
- `fig_rq1_cost_distribution.png`, `fig_rq1_strategy_cost_bias.png`,
  `fig_rq2_size_cost_calibration.png`, `fig_rq3_rank_stability.png`,
  `fig_rq4_accuracy_cost_frontier.png`.
