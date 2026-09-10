# Specification 06 — Phase 6: LCBench Measured Pools

Script: `scripts/run_fse_posterior_lcbench_batch.py`
Corpus labels: `LCBENCH`, `EXTERNAL-VALIDITY-LCBENCH`
Output directory: `artifacts/fse_posterior_lcbench_<suffix>/`

See Spec 00 §6 (metrics), §7 (hypotheses), §11 (terminology).

---

## 1. Goal

- Use LCBench as a cross-domain stress test for the FSE posterior framework.
- Determine whether posterior-risk strategy recommendations survive empirical
  runtime normalization.

## 2. Input

- `ICPE-rawdata/lcbench/data_2k_lw.json` (canonical data root, Spec 00 §5.2).
  This file is external — stage it under `ICPE-rawdata/lcbench/` before the run.
- Document JSON provenance (source, checksum, local path) in the run manifest;
  it is not version-stable.

## 3. Commands

### 3.1 Primary — no oracles

```bash
python3 scripts/run_fse_posterior_lcbench_batch.py \
  --json ICPE-rawdata/lcbench/data_2k_lw.json \
  --datasets ALL \
  --output-dir artifacts/fse_posterior_lcbench_no_oracles_final \
  --target-column final_val_accuracy \
  --cost-column time_total \
  --runtime-mode last \
  --max-budget 64 \
  --seeds 30 \
  --srs-seeds 30 \
  --no-oracles \
  --extreme max \
  --prior-offset 1
```

### 3.2 Diagnostic — with oracle strategies

```bash
python3 scripts/run_fse_posterior_lcbench_batch.py \
  --json ICPE-rawdata/lcbench/data_2k_lw.json \
  --datasets ALL \
  --output-dir artifacts/fse_posterior_lcbench_with_oracles_diagnostic \
  --target-column final_val_accuracy \
  --cost-column time_total \
  --runtime-mode last \
  --max-budget 64 \
  --seeds 30 \
  --srs-seeds 30 \
  --extreme max \
  --prior-offset 1
```

Oracle strategies are diagnostic only — the headline result uses `--no-oracles`
(Spec 00 §8 item 7).

## 4. Expected outputs (per output-dir)

```text
fse_posterior_lcbench_report.md
fse_posterior_lcbench_conclusion.md
posterior_lcbench_dataset_summary.csv
posterior_lcbench_budget_trends.csv
posterior_strategy_summary.csv
posterior_hypothesis_summary.csv
<dataset>/…                      # per-dataset reports + figures
```

## 5. Required validation checks

- **35** datasets and **210** dataset-budget scopes = 35 datasets × 6 budgets.
- Reproduces the prior no-oracle result within tolerance:
  - strategy posterior-risk distributions differ in **155/210**;
  - SRS best cost-normalized in **0/210**;
  - SRS on the empirical Pareto frontier in ≈ **20/210**;
  - empirical **top recommendation** changes in ≈ **119/210**;
  - empirical **frontier** changes in ≈ **207/210**.

## 6. Interpretation target

- LCBench does **not** refute the FSE framework.
- LCBench strongly challenges a broad, domain-independent SRS recommendation.
- Phrase every claim as reference-relative measured-pool posterior risk.

## 7. Libraries

`numpy`, `pandas`, `scipy.stats`, `matplotlib`; repo modules
`cost_sampling.posterior`, `cost_sampling.srs`,
`cost_sampling.generated_sampling`, `cost_sampling.pool_samplers`.
No new dependencies.
