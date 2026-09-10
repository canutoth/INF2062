# Specification 03 — Evaluation & Metrics

Output directory: `results/`
Outputs: `llm_models_metrics.csv` + `llm_models_metrics_ranking_{context,nocontext}_{full,test}.csv`
+ `llm_models_metrics_rankings_all.csv`.

The generator script was **not** delivered — write it from this spec and validate
against the committed `results/llm_models_metrics.csv` (64 rows) and the five
ranking CSVs. Pure pandas / scikit-learn; **no randomness** (Spec 00 §3). Reuse
the loader/normaliser helpers from `tools/compare_per_emotion.py` verbatim
(`load_ground_truth`, `normalize_label`, `load_splits`, `extract_pred_label`,
`collect_pairs`).

---

## 1. Purpose

Score every `(model, configuration, subset)` and emit one metrics table plus
per-configuration/subset rankings.

## 2. Input

- Predictions: `results/results_{ctxt,no_ctxt}/<model>/all_<model>.json` — 16
  models. `context` from `results_ctxt/`, `nocontext` from `results_no_ctxt/`.
  Discover models with `sorted(os.listdir(<dir>))` filtered to sub-directories
  containing an `all_*.json` (`glob('all_*.json')[0]`).
- Ground truth: `results/manual_labelling.json` (Spec 00 §5.2).
- Split: `results/data_splits.csv` (Spec 00 §5.3).

## 3. Grid

`configuration ∈ {context, nocontext}` × `subset ∈ {full, test}` × 16 models →
**64 rows** in `llm_models_metrics.csv`.

- `full`: all 769 labelled segments.
- `test`: labelled segments whose split is `test` (154).

## 4. Per-(model, configuration, subset) procedure

1. `preds = load_model_predictions(all_json)` → `{output: {seg: normalize_label(extract_pred_label(seg_obj))}}`.
   `extract_pred_label` key order: `principal_emocao_detectada, emoção, emocao,
   emotion, label, pred` (first present & truthy).
2. Iterate the ground truth. For each `(output_name, seg_id, true_label)`:
   - `test` subset: skip unless `split_map[(output_name, seg_id)] == "test"`.
   - `total_expected += 1`.
   - if `output_name` in `preds` **and** `seg_id` in `preds[output_name]`:
     `total_seen += 1`; then if the normalised pred is `None` → `hallucinations
     += 1`, else `samples += 1` and append `(true_label, pred)` to
     `(y_true, y_pred)`.
3. Metrics on `(y_true, y_pred)` (scikit-learn 1.3.2, `zero_division=0`):
   - `precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)`
     → `precision_weighted, recall_weighted, f1_weighted`;
   - same with `average="macro"` → `*_macro`;
   - `accuracy_score(y_true, y_pred)` → `accuracy`;
   - on empty `y_true`: all six + accuracy = `0.0`.
4. `samples = len(y_true)`.

### 4.1 Coverage / hallucination (verified against the committed CSV)

| Column | Formula |
|---|---|
| `total_expected` | GT segments in the subset |
| `total_seen` | of those, the ones with a prediction entry |
| `missing_predictions` | `total_expected - total_seen` |
| `hallucination_rate` | `hallucinations / total_seen` (0.0 if `total_seen == 0`) |
| `coverage` | `samples / total_seen` (0.0 if `total_seen == 0`) |
| `hallucination_rate_inclusive` | `(missing_predictions + hallucinations) / total_expected` |
| `coverage_inclusive` | `samples / total_expected` |

## 5. `llm_models_metrics.csv` — columns in this exact order

```
model_id, model, context, subset,
precision_weighted, recall_weighted, f1_weighted,
precision_macro, recall_macro, f1_macro,
accuracy, samples,
hallucination_rate, coverage,
hallucination_rate_inclusive, coverage_inclusive,
total_expected, total_seen, missing_predictions
```

- `model` = the model **directory name** verbatim (`deepseek-r1_14b`,
  `mixtral_8x7b`, …) — **not** a display name.
- `model_id` = `f"{model}-{context}-{subset}"` (e.g. `deepseek-r1_8b-context-test`).
- `context` ∈ {`context`, `nocontext`}; `subset` ∈ {`full`, `test`}.
- Float columns written at full pandas precision (the committed file shows ~6
  significant digits, i.e. default `DataFrame.to_csv`).
- Row order: iterate `[('results_ctxt','context'), ('results_no_ctxt','nocontext')]`
  → models `sorted(os.listdir)` → `('full', 'test')`.

### 5.1 Validation anchors (from the committed file)

| model_id | f1_macro | samples | coverage | total_seen |
|---|---|---|---|---|
| `deepseek-r1_8b-nocontext-full` | 0.0 | 10 | 0.026247 | 381 |
| `deepseek-r1_8b-context-full` | 0.04 | 69 | 0.278226 | 248 |
| `deepseek-r1_14b-context-full` | 0.180558 | 769 | 1.0 | 769 |
| `gpt-oss_20b-context-full` | 0.222593 | 769 | 1.0 | 769 |

## 6. Ranking CSVs (`results/`)

Each sorted by **`f1_macro` descending** (`DataFrame.sort_values('f1_macro',
ascending=False)`), same columns as `llm_models_metrics.csv`:

| File | Rows |
|---|---|
| `llm_models_metrics_ranking_context_full.csv` | the 16 `(context, full)` rows |
| `llm_models_metrics_ranking_context_test.csv` | 16 `(context, test)` |
| `llm_models_metrics_ranking_nocontext_full.csv` | 16 `(nocontext, full)` |
| `llm_models_metrics_ranking_nocontext_test.csv` | 16 `(nocontext, test)` |
| `llm_models_metrics_rankings_all.csv` | all four blocks concatenated (64 rows) + columns `ranking_title, ranking_context, ranking_subset` |

`rankings_all` block order and the exact `ranking_title` strings (verified):

| order | ranking_title | ranking_context | ranking_subset |
|---|---|---|---|
| 1 | `with context and full data` | `context` | `full` |
| 2 | `with context and test data` | `context` | `test` |
| 3 | `without context and full data` | `nocontext` | `full` |
| 4 | `without context and test data` | `nocontext` | `test` |

Each block is the 16 rows for that `(context, subset)` sorted by `f1_macro`
descending.

## 7. Libraries

`pandas`, `scikit-learn` (`sklearn.metrics.precision_recall_fscore_support`,
`accuracy_score`), `json`, `os`, `glob`. No `ollama`, no `numpy` beyond what
sklearn pulls.
