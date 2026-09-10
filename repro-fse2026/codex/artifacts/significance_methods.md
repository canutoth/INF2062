# Significance of RQ2 decision flips — method & parameters

Purpose: test whether the RQ2 "the top strategy–budget combination changes when
measured cost replaces count cost" flips are *statistically robust* or within
noise. Driven by the observation that many flips are tight near-ties.

## Parameters (decided 2026-06-23)

- **Stochastic seeds: 30** per (strategy, budget level). Rationale: significance
  here comes primarily from the **test-set bootstrap**, not from seed count, so
  30 is sufficient and ~3× cheaper than the 100-seed exploratory batch. Stored
  in `scripts/significance_flips.py` (`--seeds 30`).
- **Bootstrap replicates: 1000** per flip.
- **Learner: ridge-log, alpha=1.0** (matches the figure/primary batches).
- **Candidates: ordinary strategies only** (random, balanced, diversity,
  pairwise, pilotCost) — oracles excluded, matching the paper.
- **Weights (λ): [0.1, 0.25, 0.5, 1, 2, 4, 10].**

## Why a test-set bootstrap (not seed-only)

`pairwise` and `diversity` are **deterministic by construction**
(`generated_sampling.py:705`, fixed seed-0 RNG, one sample regardless of
`--seeds`). Seed-resampling therefore tells us nothing about them. MRE is a mean
of per-configuration relative errors over the held-out population
(`analysis.py:86`), so we resample the **evaluation configurations** (and, for
stochastic strategies, also draw a seed). This is a uniform uncertainty axis
that applies to deterministic and stochastic strategies alike.

## Robustness criterion

For a flip (count-winner `cw` vs measured-winner `mw`) at weight λ, each
bootstrap replicate resamples the common evaluation set (population minus the
two samples' training indices) and, for stochastic strategies, a seed. Using
fixed min–max ranges (Rmre, Rcost, Rn) from the median candidate set, the
pairwise objective sign is exact:

    count prefers cw  ⇔  (mre_cw−mre_mw)/Rmre + λ(n_cw−n_mw)/Rn  < 0
    measured prefers mw ⇔ (mre_mw−mre_cw)/Rmre + λ(cost_mw−cost_cw)/Rcost < 0

`p_reproduce` = fraction of replicates where *both* hold (the flip reproduces).
A flip is **robust** if `p_reproduce ≥ 0.95`, else **within noise**.

## Reproduce

```bash
.venv/bin/python scripts/significance_flips.py \
  --systems 7z Apache brotli exastencils HSQLDB jump3r kanzi LLVM lrzip \
            MongoDB nginx PostgreSQL VP8 x264 \
  --seeds 30 --bootstrap 1000 --zip /tmp/twins_main.zip \
  --out artifacts/significance_flips.csv
```

Energy data: TwinsOrFalseFriends GitHub/Zenodo archive (see
`memory/reference_data_sources_repro.md`). Other families (workload,
replications, Linux, LCBench) use their own loaders and are run separately.
