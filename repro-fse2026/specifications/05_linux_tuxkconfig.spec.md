# Specification 05 — Phase 5: Linux / TuxKConfig Measured Pools

Script: `scripts/run_fse_posterior_linux_batch.py`
Corpus labels: `LINUX`, `EXTERNAL-VALIDITY-LINUX-POOL`
Output directory: `artifacts/fse_posterior_linux_<suffix>/`

See Spec 00 §6 (metrics), §7 (hypotheses), §11 (terminology).

---

## 1. Goal

- Test FSE-style posterior risk on a large, structurally different
  configurable-system family.
- Report results as **pool-relative** posterior risk (never exhaustive-space).

## 2. Inputs

- `ICPE-rawdata/linux/tuxkconfig_{413,415,420,500,504,507,508}.parquet`
  (canonical data root, Spec 00 §5.2; already present in the working repo).

This is exactly the release map `scripts/run_fse_posterior_linux_batch.py`
already defaults to — no path override is needed for a working-repo run.

## 3. Commands

### 3.1 Quick pass

```bash
python3 scripts/run_fse_posterior_linux_batch.py \
  --releases ALL \
  --output-dir artifacts/fse_posterior_linux_all_quick_final \
  --target-column vmlinux \
  --levels 0.01,0.02 \
  --stochastic-runs 30 \
  --diversity-runs 5 \
  --uncertainty-runs 5 \
  --coverage-runs 5 \
  --srs-seeds 30 \
  --top-k-features 512 \
  --extreme max \
  --prior-offset 1 \
  --quick
```

### 3.2 Fuller pass (if time budget allows)

```bash
python3 scripts/run_fse_posterior_linux_batch.py \
  --releases ALL \
  --output-dir artifacts/fse_posterior_linux_all_full \
  --target-column vmlinux \
  --levels 0.01,0.02,0.05 \
  --stochastic-runs 100 \
  --diversity-runs 20 \
  --uncertainty-runs 20 \
  --coverage-runs 20 \
  --srs-seeds 100 \
  --top-k-features 512 \
  --extreme max \
  --prior-offset 1
```

## 4. Expected outputs (per output-dir)

```text
fse_posterior_linux_report.md
fse_posterior_linux_conclusion.md
posterior_linux_release_summary.csv
posterior_linux_budget_trends.csv
posterior_strategy_summary.csv
posterior_hypothesis_summary.csv
<release>/…                      # per-release reports + figures
```

## 5. Required validation checks

- All **seven** releases present: `413`, `415`, `420`, `500`, `504`, `507`, `508`.
- Result scope is described as **measured-pool relative**.
- Reproduces the prior quick-pass result within tolerance:
  - strategy posterior-risk distributions differ in **11/14**;
  - SRS best cost-normalized in ≈ **3/14**;
  - SRS on the empirical Pareto frontier in ≈ **8/14**;
  - empirical frontier changes in **14/14**.

  (14 scopes = 7 releases × 2 budget levels.)

## 6. Interpretation target

- Linux weakens the universal SRS recommendation.
- This does **not** invalidate posterior risk — it shows the recommendation is
  sensitive to system family and empirical acquisition cost.

## 7. Libraries

`numpy`, `pandas`, `pyarrow` (parquet), `scipy.stats`, `matplotlib`; repo modules
`cost_sampling.posterior`, `cost_sampling.srs`, `cost_sampling.pool_samplers`,
`scripts/significance_linux.py`, `scripts/sig_core.py`. No new dependencies
beyond what the target repo already pins for parquet reads.
