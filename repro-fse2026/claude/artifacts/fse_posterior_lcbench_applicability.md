# Applicability: FSE-Style Posterior Guarantees on LCBench

## Status

LCBench is applicable as an external-validation family for reference-relative posterior risk. The raw lightweight JSON is external to this repository; for the current run, it was downloaded to `/private/tmp/lcbench/data_2k_lw.json`.

Existing LCBench artifacts under `artifacts/lcbench_data_2k_lw/` contain MRE/cost summaries but not the sampled configuration indices or the full target vector needed to recompute posterior risk. The new runner therefore expects the raw `data_2k_lw.json` file.

## Interpretation

Each OpenML dataset should be treated as one measured reference universe. Each hyperparameter configuration is a sampled object. For the default target `final_val_accuracy`, posterior risk is the fraction of measured LCBench configurations whose validation accuracy is higher than the best sampled validation accuracy.

This is not a configurable-software result in the SPL sense. It is an out-of-domain external-validity check for the same methodological question: do posterior-risk and posterior-confidence recommendations change when normalized by empirical acquisition cost rather than by sample size?

## Command

```bash
.venv/bin/python scripts/run_fse_posterior_lcbench_batch.py \
  --json /private/tmp/lcbench/data_2k_lw.json \
  --quick
```

For a full pass over the 35 datasets:

```bash
.venv/bin/python scripts/run_fse_posterior_lcbench_batch.py \
  --json /private/tmp/lcbench/data_2k_lw.json \
  --output-dir artifacts/fse_posterior_lcbench
```

## Expected Inputs

- `data_2k_lw.json` from the LCBench lightweight archive.
- Default target: `final_val_accuracy`.
- Default empirical acquisition cost: `time_total`, derived from the runtime learning curve.

## Recommended Framing

Use LCBench as `EXTERNAL-VALIDITY-LCBENCH`, not as another configurable-software replication dataset. It is conceptually close to the Linux measured-pool case because the posterior guarantees are reference-relative, but the scientific object differs: ML hyperparameter configurations over OpenML datasets rather than software-product-line configurations.
