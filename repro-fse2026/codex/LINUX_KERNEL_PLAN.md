# LinuxData (TuxKConfig) — empirical sampling-cost replication

This document scopes the integration of the **TuxKConfig / LinuxData** corpus
(arXiv 2505.07487, EASE 2025) into the empirical-cost study described in
`PLAN.md`. The aim is to extend RQ1 and RQ2 (and partially RQ3/RQ4) from the
ICPE-style configurable-system corpus to a much larger, fundamentally different
kind of system — the Linux kernel — without violating the dataset-scope
discipline already in place for this paper.

The plan is deliberately conservative: it commits only to what is feasible
without instrumenting Kconfig itself, and it surfaces every approximation as a
threat to validity rather than burying it.

---

## 1. Why this dataset, and why now

The empirical-cost paper currently relies on the ICPE-rawdata corpus, where
every benchmark exposes a clean per-configuration wall-clock measurement
(`x264`, `BerkeleyDBC`, etc.). That corpus delivers RQ1–RQ5 cleanly but is
homogeneous in two respects: (i) configuration spaces are small (≤ a few
thousand configurations, ≤ 30 options); (ii) cost dynamic range, while
non-trivial, rarely spans more than two orders of magnitude.

**TuxKConfig changes both axes by an order of magnitude or more.**

| Dimension                       | ICPE-rawdata (e.g. x264)        | TuxKConfig v4.13 (OpenML 46759)                |
| ------------------------------- | -------------------------------- | ----------------------------------------------- |
| Configurations                  | 1,152                            | 92,562 valid v4.13 configurations (also v5.08, smaller) |
| Options                         | 16                               | 9,466 binary Kconfig options                    |
| Cost dynamic range              | ≈ 10× (encoding time)            | ≈ 10²–10³× (binary size: 1 MB → 100+ MB)        |
| Cost signal                     | Wall-clock time (canonical)      | Binary size (storage-bound `cost(c)`)           |
| Sampling distribution           | Strategy-driven (Kaltenecker)    | Single random pool (`make randconfig`)          |
| Variability model available?    | Yes, used by literature samplers | No usable feature model in the published artifact |

For a paper whose core question is **"is sample size a calibrated proxy for
empirical acquisition cost?"**, a system that pushes cost heterogeneity out by
two orders of magnitude is the single most informative addition we can make.

This addition is also defensible against the recorded scope rule
(`feedback_dataset_scope.md`): TuxKConfig is a configurable software system in
the SPL sense, and binary size is an explicitly endorsed `cost(c)` instance
("size of a video can be a computational cost") — not a surrogate, not an
HPO benchmark, not a deployment workflow.

---

## 2. What the dataset actually contains

**Sources.** Two OpenML datasets from the TuxKConfig series (Borges et al.,
EASE 2025, arXiv 2505.07487v1):

- v4.13 — OpenML id 46759, 102 MB parquet, ~92.5 K configurations.
- v5.08 — OpenML id 46744, 39 MB parquet, ~26 K configurations.

Both mirrored locally under `ICPE-rawdata/linux/tuxkconfig_<release>.parquet`.

**Schema (9,488 columns).**

- **9,466 kernel-option columns**, all binary numeric (0/1). Examples:
  `X86_LOCAL_APIC`, `OPENVSWITCH`, `MPLS`, `NETWORK_FILESYSTEMS`, …
- `active_options` — number of options enabled in this configuration.
- `vmlinux` — uncompressed kernel binary size in bytes. **Canonical cost in
  this study.**
- Six compressed-image families × {bzImage, vmlinux, raw} columns:
  `GZIP-bzImage`, `GZIP-vmlinux`, `GZIP`, `BZIP2-*`, `LZMA-*`, `XZ-*`,
  `LZO-*`, `LZ4-*`. These are alternative target/cost combinations.
- `cid` — configuration id (row identifier, ignored).

**Provenance.** Configurations were drawn with `make randconfig` over the v4.13
Kconfig tree; every row is a SAT-feasible kernel configuration that compiled
successfully. The published artifact does **not** include build time. There is
no exposed feature model or constraint solver hook usable for fresh sampling.

**Population view.** For this paper the 92,562 rows constitute a fixed,
finite, randconfig-induced *measurement pool*. We do not generate new
configurations; we subsample from this pool.

---

## 3. The methodological framing this dataset forces

The literature sampling strategies used elsewhere in this paper
(uniform-over-feasible, t-wise, distance-based, diversified-distance,
solver-based, randomized solver-based) are **synthesis** strategies — they
require a feature model + SAT solver, and they generate fresh configurations
that must then be measured.

On TuxKConfig we cannot run synthesis without re-implementing a substantial
chunk of Kconfig. Instead we adopt a **pool-based subsampling** view:

> Given a pre-existing pool of measured configurations, what is the empirical
> cost behavior of strategies that *select from the pool* at fixed sample
> size n?

This framing is methodologically clean:

1. It is what a real practitioner does when they have a benchmark dataset.
2. It removes the confound of differing feasibility constraints across
   synthesis strategies — every strategy operates on the same population.
3. It allows the same calibration metric `(%cost / %n)` to be computed
   without reference to an unmeasured "full configuration space".

The cost: synthesis-only strategies (true t-wise, true uniform-over-SAT) are
out of scope for this dataset and must be flagged in threats to validity.

---

## 4. Research-question coverage

| RQ  | Coverage on TuxKConfig                                                                                                                                                                              |
| --- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RQ1 | **Full.** Cost heterogeneity at fixed n is the headline question this dataset answers most clearly. Pool-based strategies will exhibit different cost distributions on a population with 100×+ heterogeneity. |
| RQ2 | **Full.** Calibration ratio `(%cost / %n)`, Spearman ρ(n, train_cost), per-strategy bias. The randconfig pool gives a clean denominator for `FullCost = Σ vmlinux`.                                |
| RQ3 | **Partial.** Rank stability across λ values is computable, but the strategy set is pool-based — we cannot mix in synthesis strategies, so the ranking story is internally consistent but narrower than x264. |
| RQ4 | **Partial.** Pareto frontiers in (count, MRE) and (empirical-cost, MRE) planes are computable. Same caveat as RQ3 on strategy set.                                                                  |
| RQ5 | **Out of scope for this dataset.** TuxKConfig 4.13 is a single workload/property combination. Cross-version replication (4.15, 4.20, 5.x) is future work.                                            |

The plan therefore commits to full RQ1/RQ2 and a labelled-partial RQ3/RQ4.

---

## 5. Sampling strategies (pool-based)

Seven strategies are evaluated. All operate on the fixed pool, none requires
a feature model, and only the two oracles read the cost signal directly.

1. **`random`** — uniform random subsample without replacement. Stochastic;
   100 runs. The reference baseline.

2. **`balanced`** — stratified random by `active_options` decile.
   Each decile contributes `n/10` configurations (rounded). Stochastic;
   100 runs. Tests whether matching the marginal distribution of "kernel
   bigness" is enough to remove cost bias.

3. **`diversity`** — greedy farthest-first traversal in Hamming distance
   over kernel options. Seed drawn uniformly at random; thereafter each
   addition maximises minimum Hamming distance to the current selection
   using a candidate-batch trick (`candidate_size=512`). Stochastic;
   20 runs. Capped at `n ≤ 1851` (≤ 2% of pool) because the sampler is
   `O(n² × features)` in the worst case.

4. **`uncertainty`** — residual-driven active learning. Train ridge on a
   random seed of size `max(50, ⌈n/4⌉)`, predict on the rest of the pool,
   add the top `n − seed` configurations by absolute relative residual.
   Stochastic in the seed; 20 runs. **Deployable** — a practitioner doing
   active learning sees the target's residuals, not the cost signal.

5. **`coverage`** — greedy option-frequency matching. At each step picks
   the candidate (from a random batch of 512) whose addition minimises the
   L1 distance between the running per-option enabled-frequency and the
   pool's per-option frequency. A pool-based proxy for marginal coverage
   that does not require a Kconfig feature model. Stochastic; 20 runs.

6. **`cheapOracle`** — deterministic: bottom-n configurations by `vmlinux`.
   Diagnostic only — assumes access to the cost signal we are calibrating.
   Lower-bound reference for `train_cost`.

7. **`expensiveOracle`** — deterministic: top-n configurations by `vmlinux`.
   Symmetric upper-bound reference.

**Deployable vs diagnostic.** Strategies 1–5 are deployable: they use only
information available before the cost is measured (option vectors,
`active_options`, the target via ridge residuals). Strategies 6–7 are
diagnostic — they bracket the room cost-aware sampling could in principle
exploit. Strategy bias on calibration ratio is the load-bearing finding,
not the oracle bracket.

Sample sizes are percentage-based to keep results commensurable with the
ICPE-rawdata study:

```
levels = {p01: 1%, p02: 2%, p05: 5%, p10: 10%, p20: 20%}
```

corresponding to absolute n ∈ {926, 1851, 4628, 9256, 18512}.

---

## 6. Cost and target choice

**Default scenario — `linux413_vmlinux`:**

- Target = `vmlinux` (uncompressed binary size).
- Cost   = `vmlinux`.
- Same column for both, mirroring the `x264_time_*` design where target ≡
  cost. Storage-bound interpretation of `cost(c)`: the cost of acquiring a
  measurement equals the size of what you store.

**Optional secondary — `linux413_lzma`:**

- Target = `LZMA-bzImage` (release artifact for distribution).
- Cost   = `vmlinux` (the build artifact you actually have to handle).
- Mirrors `x264_size_*` with cost from `x264_time_*`.

The default is run first; the secondary is enabled only if the default reveals
heterogeneity worth replicating across cost choices.

---

## 7. Learner and feature handling

**Learner.** Ridge / log-linear (the existing
`cost_sampling.metrics.fit_ridge`). `log_target=True` is appropriate: binary
sizes span a factor of 100, log-linear is the existing default. α=1.0.

**Feature pruning.** Three sequential filters on the option matrix:

1. Drop columns where the minority class has fewer than 50 occurrences in
   the full pool — removes near-constant options (typically retains
   ~9,200 of 9,466 on v4.13).
2. Top-K by marginal effect on the target, K=512 — for each remaining
   option, the absolute difference of mean target between
   `option=1` and `option=0`; keep the K largest. This is the dominant
   speedup; without it ridge over 9,000+ features would push end-to-end
   wall-clock per evaluation to seconds, multiplied by 1,250 evaluations.
3. Drop exact-duplicate columns (one representative kept).

The pruning is dataset-level and one-time, applied before any sampling
decision is taken. The retained columns are documented in
`linux_feature_columns.csv`. RQ1/RQ2 metrics are computed on the full pool
and **do not depend on which columns the ridge sees** — feature pruning
affects MRE-based RQs (RQ3, RQ4) only.

**Test set.** The complement of the training sample within the full pool.
Predictions are chunked (default 4096 rows) so the float64 design matrix
never exceeds a few hundred MB.

**Forbidden as features.** Twenty-one columns are excluded from the design
matrix (single source of truth: `cost_sampling.linux_data.NON_OPTION_COLUMNS`):

- the prediction target `vmlinux` (1 column),
- 18 compressed-image variants (six compression families × {bzImage,
  vmlinux, "raw"}) — all functions of the same kernel build and
  therefore tightly correlated with the target,
- `active_options` — the count of enabled options is exactly derivable
  from the option vector itself; including it would let ridge collapse
  to a size-of-config regression and trivially beat any sampling strategy,
- `cid` — row identifier with no semantic content.

The runner asserts at load time that no forbidden column survives into
`feature_names`, and prints an explicit count line:

```
forbidden columns excluded from features: 21 (target 'vmlinux',
all 19 size variants, active_options, cid)
```

---

## 8. Runs and budget

| Strategy           | Runs  | Levels   | Total samples | Notes                                                |
| ------------------ | ----- | -------- | ------------- | ---------------------------------------------------- |
| random             | 100   | 5        | 500           |                                                      |
| balanced           | 100   | 5        | 500           |                                                      |
| diversity          | 20    | 2 (n≤1851)| 40           | farthest-first; capped at ≤ 2% pool                  |
| uncertainty        | 20    | 5        | 100           | one extra ridge fit + chunked predict per call       |
| coverage           | 20    | 5        | 100           | candidate-batch greedy frequency matching            |
| cheapOracle        | 1     | 5        | 5             | deterministic                                        |
| expensiveOracle    | 1     | 5        | 5             | deterministic                                        |
|                    |       |          | **1250**      |                                                      |

After feature pruning (top-K=512 by marginal effect on the target, ~495
columns surviving deduplication), a single ridge fit takes <100 ms on CPU.
The compute bottleneck is the diversity sampler at n=1851
(≈20 s/run × 20 runs = ~7 min) and coverage at the largest level
(≈5 s/run × 20 runs = ~2 min). End-to-end wall-clock per release is
≤ 30 minutes.

---

## 9. Expected outputs

Outputs are written to `artifacts/linux413_vmlinux/` and follow the layout of
`artifacts/x264_time_all/` so the existing `run_system_report.py` and
plotting helpers can be reused with minimal adaptation:

- `records.csv`              — one row per (strategy, level, run).
- `rq1_cost_heterogeneity.csv` — pool-level cost statistics.
- `strategy_summary.csv`     — median/IQR cost, calibration, MRE,
  cost-over-random.
- `rq2_proxy_summary.csv`    — Spearman ρ, calibration ratio, bias.
- `rq3_rank_stability.csv`   — λ-sweep top-1/top-3/τ.
- `rq4_pareto.csv`           — count and empirical Pareto labels.
- `linux_feature_columns.csv` — option columns retained after pruning.
- `fig_rq1_cost_distribution.png`, `fig_rq2_size_cost_calibration.png`,
  `fig_rq3_rank_stability.png`, `fig_rq4_accuracy_cost_frontier.png`,
  `fig_rq1_strategy_cost_bias.png`.
- `linux413_vmlinux_report.md` — narrative summary.

---

## 10. Threats to validity specific to this dataset

1. **No build-time signal.** The headline cost in this study is binary size,
   not wall-clock build time. Build time is the more practically relevant
   acquisition cost for kernel configuration. Replicating with build time
   would require re-instrumenting the original measurement workflow — out of
   scope here, flagged as future work. Binary size remains a legitimate
   `cost(c)` instance (storage-bound).

2. **Single sampling distribution upstream.** The 92,562-row pool was drawn
   with `make randconfig`, which is itself a stochastic synthesis procedure.
   Pool-based subsampling therefore evaluates strategies *conditional on* the
   randconfig distribution. Strategies that would behave differently on a
   uniform-over-SAT or t-wise pool cannot be assessed here. This is a hard
   limit of using a published dataset rather than re-running the build.

3. **No synthesis strategies.** True uniform random over the formal Kconfig
   space, t-wise coverage, distance-based on the formal model — none of
   these are evaluable on TuxKConfig as published. The strategy set is
   pool-based-only and labelled as such throughout.

4. **Two kernel versions, partial cross-version coverage.** v4.13 and v5.08
   are evaluated; the remaining four releases (4.15, 4.20, 5.0, 5.4, 5.7)
   slot into the same pipeline by changing `--release` and `--parquet` and
   are flagged as future replication work.

5. **Feature pruning may interact with pool-based diversity strategies.**
   Farthest-first and cluster-random use the option vectors as their distance
   space. Pruning near-constant columns slightly changes that geometry.
   We pin a single pruned column set across strategies to keep the comparison
   fair; the pruned-vs-unpruned sensitivity is reported in an appendix figure
   on a 5%-level subset.

6. **Cheap/expensive oracles use the very signal we are calibrating.** They
   are reported as references, not as candidate strategies. The paper text
   should explicitly mark them as upper/lower bounds on `train_cost`, not as
   methods.

---

## 11. What this addition lets the paper say

If RQ1 and RQ2 hold on TuxKConfig the way the x264 results suggest, the
strengthened claim is:

> Sample size (n) is a miscalibrated proxy for empirical acquisition cost
> not just on small benchmarks with single-digit option counts, but on
> production-scale configurable systems with 10⁴ options and 10²–10³×
> per-configuration cost spread. The miscalibration is robust to the
> sampling-strategy axis, and pool-based strategies that look diversity-
> aware can drift systematically toward higher- or lower-cost regions of
> the configuration space.

If RQ1/RQ2 *fail* to replicate (i.e. n calibrates well on TuxKConfig despite
the heterogeneity), the paper learns something equally important: that on
randconfig-style pools the cost-vs-count gap closes, and the miscalibration
risk is concentrated in expert-driven sampling rather than in random
acquisition. Either outcome is a publishable contribution.

---

## 12. Implementation pointers

- Loader: `cost_sampling/linux_data.py` (new) — reads parquet via pyarrow,
  returns a `RunDataset`-compatible object after pruning.
- Samplers: `cost_sampling/pool_samplers.py` (new) — six pool-based samplers
  with seedable RNGs.
- Runner: `scripts/run_linux_kernel.py` (new) — mirrors `run_poc.py` /
  `run_x264_size_batch.py` in CLI shape and output structure.
- Palette: extend `cost_sampling.plots.PALETTE` with the four new strategy
  names so figures keep their colour discipline.
- Sort key: extend `level_sort_key` to recognise `pNN` percentage levels so
  axes order naturally `p01 < p02 < p05 < p10 < p20`.

These are the only existing files that need light edits; the rest of the
analysis pipeline (`analysis.py`, `metrics.py`, the plotting helpers) is
strategy-agnostic and works as-is.
