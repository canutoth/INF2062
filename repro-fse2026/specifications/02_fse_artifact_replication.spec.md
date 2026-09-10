# Specification 02 — Phase 2: Direct FSE Artifact Replication

Script: `scripts/run_fse_posterior_batch.py`
Corpus label: `REPLICATION-FSE26` (original FSE artifact systems)
Output directory: `artifacts/fse_posterior_fse_artifact_<suffix>/`

See Spec 00 §6 (metrics), §7 (hypotheses), §11 (terminology).

---

## 1. Goal

- Reproduce FSE posterior-risk analysis on the original FSE systems.
- Add **empirical acquisition cost** as the second decision axis.

## 2. Input

- External FSE artifact root: `$FSE_ROOT` (see Spec 00 §5.3). On failure, report
  the missing path and expected format.

## 3. Commands

### 3.1 Fixed-budget (primary)

```bash
python3 scripts/run_fse_posterior_batch.py \
  --fse-root "$FSE_ROOT" \
  --output-dir artifacts/fse_posterior_fse_artifact_final_t2 \
  --contexts ALL \
  --strategies random,solverBased,divDistBased,twise,SRSSampling \
  --levels t2 \
  --max-runs 100 \
  --extreme max \
  --prior-offset 1
```

### 3.2 Prior-equation sensitivity (`N` instead of `N + 1`)

```bash
python3 scripts/run_fse_posterior_batch.py \
  --fse-root "$FSE_ROOT" \
  --output-dir artifacts/fse_posterior_fse_artifact_final_t2_priorN \
  --contexts ALL \
  --strategies random,solverBased,divDistBased,twise,SRSSampling \
  --levels t2 \
  --max-runs 100 \
  --extreme max \
  --prior-offset 0
```

### 3.3 Budget scaling across all available levels

```bash
python3 scripts/run_fse_posterior_batch.py \
  --fse-root "$FSE_ROOT" \
  --output-dir artifacts/fse_posterior_fse_artifact_final_all_levels \
  --contexts ALL \
  --strategies random,solverBased,divDistBased,twise,SRSSampling \
  --levels ALL \
  --max-runs 100 \
  --extreme max \
  --prior-offset 1
```

## 4. Expected outputs (per output-dir)

```text
fse_posterior_systems_report.md
posterior_system_summary.csv
posterior_strategy_summary.csv
posterior_hypothesis_summary.csv
posterior_hypothesis_tests.csv
<system>/…                       # per-system folders with figures + CSVs
```

## 5. Required validation checks

- All **seven** FSE systems present.
- All requested strategies present.
- SRS returns exactly the fixed requested sample size in every context.
- Reproduces the prior "current" finding within tolerance:
  - SRS best empirical-cost-normalized in ≈ **3/7**;
  - SRS on the empirical Pareto frontier in ≈ **6/7**;
  - empirical frontier changes in ≈ **6/7**.

## 6. Interpretation target

The FSE artifact is the closest direct replication. Report posterior risk
relative to the complete configuration universe **only if** the artifact contains
the full measured universe for that system (Spec 00 §11).

## 7. Libraries

`numpy`, `pandas`, `scipy.stats`, `matplotlib`; repo modules
`cost_sampling.posterior`, `cost_sampling.srs`. No new dependencies.
