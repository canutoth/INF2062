# Specification 04 — Per-Emotion Analysis & Context-Effect Report

Provided, authoritative scripts:
`tools/compare_per_emotion.py`, `tools/compare_context_effect.py`.
Output directory: `results/`.
Outputs: `per_emotion_metrics.csv`, `per_emotion_metrics_comparison.csv`,
`per_emotion_metrics_wide.csv` + a printed context-effect report.

Both scripts are delivered and working. This module = **run them and confirm
their outputs**, or regenerate an equivalent that produces byte-identical CSVs.
The `per_emotion_metrics*.csv` files are **not** committed, so the validation
target is behavioural (re-run the script twice → identical output) plus internal
consistency with `llm_models_metrics.csv` (module 03).

Shares the loader/normaliser helpers with module 03 (they live in
`compare_per_emotion.py`). No randomness.

---

## 1. `tools/compare_per_emotion.py`

### 1.1 Inputs (paths resolved relative to the script: `../results/`)

`results/manual_labelling.json`, `results/data_splits.csv`, and every
`results/results_{ctxt,no_ctxt}/<model>/all_*.json`.

### 1.2 Procedure

For each `(subdir, ctx)` in `[('results_ctxt','context'), ('results_no_ctxt','nocontext')]`,
each model `sorted(os.listdir(subdir))`, each `subset ∈ ('full','test')`:

- `y_true, y_pred = collect_pairs(gt, preds, subset_arg, split_map)` — same
  filtering as module 03 §4 (test-split filter, prediction must exist, normalised
  label must be non-`None`).
- `p, r, f1, support = precision_recall_fscore_support(y_true, y_pred,
  labels=LABELS_ORDER, average=None, zero_division=0)` — per class, in
  `LABELS_ORDER` = `[Anger, Disgust, Fear, Happiness, Neutral, Sadness, Surprise]`.
- On empty `y_true`: precision/recall/f1 = `0.0`, support = `0` for every label.

### 1.3 `per_emotion_metrics.csv`

One row per `(model, context, subset, emotion)`. Columns:

```
model, context, subset, emotion, precision, recall, f1, support
```

`model` = directory name; `context` ∈ {`context`,`nocontext`}; `precision/recall/f1`
= `float`; `support` = `int`.

### 1.4 `per_emotion_metrics_comparison.csv`

`pd.merge` of the `context` rows and the `nocontext` rows on
`['model','subset','emotion']` (`how='inner'`), with `precision/recall/f1`
renamed `*_context` / `*_nocontext`. Then:

```
model, subset, emotion,
precision_context, recall_context, f1_context,
precision_nocontext, recall_nocontext, f1_nocontext,
precision_delta, recall_delta, f1_delta,
f1_pct_change, precision_pct_change, recall_pct_change
```

- `*_delta = *_context - *_nocontext`.
- `*_pct_change = (context - nocontext) / nocontext * 100`, or `NaN` when the
  no-context value is `0`.
- No `support` column here.

### 1.5 `per_emotion_metrics_wide.csv`

`compare_per_emotion.py` builds this by `set_index(['model','emotion','subset'])`,
keeping the six renamed metric columns, then `unstack('subset')` and flattening
column names. **The reference flatten logic is buggy** (it re-appends
`context`/`nocontext` to names that already contain it, so its "friendly reorder"
list never matches and the columns land in raw unstacked order). Reproduce
`compare_per_emotion.py` as written — do not "fix" the naming, or the output
stops matching.

### 1.6 Console output

Per subset (`full`, `test`), per emotion in `LABELS_ORDER`: top-5 models by
`f1_delta`, printed as `- <model>: f1_ctx=.. | f1_nctx=.. | delta=+.. (..%)`.
Optional `--print-model <name>` dumps that model's full per-emotion comparison.

## 2. `tools/compare_context_effect.py`

Reads `results/llm_models_metrics.csv` (module 03 output). Requires columns
`model, context, subset, f1_macro`. Per subset present (`full`, then `test`):

1. `pivot_table(index='model', columns='context', values='f1_macro', aggfunc='max')`.
2. Keep models with both `context` and `nocontext` (`dropna`).
3. `delta = f1_context - f1_nocontext`;
   `pct_change = delta / f1_nocontext * 100` (`NaN` if baseline `0`).
4. Print: number of matched models, mean `delta` (`%.6f`), mean `pct_change`
   over non-`NaN` (`%.2f%%`), then a per-model line sorted by `delta` desc:
   `- <model>: context=.. | nocontext=.. | delta=+.. (..%)`.

No file is written.

## 3. Outputs

`results/per_emotion_metrics.csv`, `results/per_emotion_metrics_comparison.csv`,
`results/per_emotion_metrics_wide.csv`, plus stdout from §1.6 and §2.

## 4. Validation

- Re-running `compare_per_emotion.py` twice produces identical CSVs (determinism).
- For every `(model, context, subset)`, `sum(support over the 7 emotions in
  per_emotion_metrics.csv)` equals `samples` in `llm_models_metrics.csv`.
- `compare_context_effect.py`'s per-model `f1_context` / `f1_nocontext` equal the
  `f1_macro` values in `llm_models_metrics.csv`.

## 5. Libraries

`pandas`, `scikit-learn` (`precision_recall_fscore_support`), `json`, `os`,
`glob`, `sys`.
