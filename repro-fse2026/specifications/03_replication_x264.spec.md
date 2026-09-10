# Specification 03 — Phase 3: REPLICATION / x264

Script: `scripts/run_fse_posterior_x264_batch.py`
Corpus label: `REPLICATION-ICPE20-x264` (x264 corpus, ICPE 2020 artifact)
Output directory: `artifacts/fse_posterior_x264_icpe_<suffix>/`

See Spec 00 §6 (metrics), §7 (hypotheses), §11 (terminology).

---

## 1. Goal

- Run FSE posterior-risk metrics on the x264 corpus.
- Test whether SRS and posterior guarantees transfer.
- Test whether cost-normalized decisions differ from sample-size decisions.

## 2. Input

- `ICPE-rawdata/AllRuns.zip` (canonical data root, Spec 00 §5.2; already present
  in the working repo).

## 3. Commands

### 3.1 Primary

```bash
python3 scripts/run_fse_posterior_x264_batch.py \
  --runs-zip ICPE-rawdata/AllRuns.zip \
  --output-dir artifacts/fse_posterior_x264_icpe_final \
  --contexts 0-16 \
  --target-props time,size \
  --cost-prop time \
  --strategies random,solverBased,divDistBased,twise,distBased,henard \
  --levels t1,t2,t3 \
  --fixed-level t2 \
  --max-runs 100 \
  --srs-seeds 100 \
  --extreme max \
  --prior-offset 1
```

### 3.2 Sensitivity — each target uses its own acquisition cost

```bash
python3 scripts/run_fse_posterior_x264_batch.py \
  --runs-zip ICPE-rawdata/AllRuns.zip \
  --output-dir artifacts/fse_posterior_x264_icpe_final_cost_same \
  --contexts 0-16 \
  --target-props time,size \
  --cost-prop same \
  --strategies random,solverBased,divDistBased,twise,distBased,henard \
  --levels t1,t2,t3 \
  --fixed-level t2 \
  --max-runs 100 \
  --srs-seeds 100 \
  --extreme max \
  --prior-offset 1
```

`--cost-prop time` = one acquisition cost (runtime) for all targets;
`--cost-prop same` = each target property is normalized by its own cost.

## 4. Expected outputs (per output-dir)

```text
fse_posterior_x264_icpe_report.md
posterior_x264_context_summary.csv
posterior_x264_budget_trends.csv
posterior_strategy_summary.csv
posterior_hypothesis_summary.csv
<context>/…                      # per-context reports + figures
```

## 5. Required validation checks

- **34** fixed-level target contexts = 17 inputs × 2 target properties.
- Reproduces the prior "current" result within tolerance:
  - strategy posterior-risk distributions differ in **34/34**;
  - SRS best cost-normalized in ≈ **26/34**;
  - SRS on the empirical Pareto frontier in ≈ **29/34**;
  - empirical frontier changes in ≈ **30/34**.

## 6. Interpretation target

- x264 is likely the strongest positive SRS replication.
- The cost-aware result still matters: Pareto frontiers change even when the top
  scalar recommendation is stable.

## 7. Libraries

`numpy`, `pandas`, `scipy.stats`, `matplotlib`; repo modules
`cost_sampling.posterior`, `cost_sampling.srs`, `cost_sampling.pool_samplers`.
No new dependencies.
