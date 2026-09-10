# Specification 05 — LaTeX Table Rows

Output directory: `results/LLMs/`
Outputs (overwrite; each is `\input{}`-ed by a delivered wrapper):

```
llm_results_rows.tex
per_emotion_llm_noctx_full_rows.tex
per_emotion_llm_noctx_test_rows.tex
per_emotion_llm_ctx_full_rows.tex
per_emotion_llm_ctx_test_rows.tex
```

The generator is not delivered — write it from this spec and validate against the
committed `results/LLMs/*_rows.tex` (16 rows each). The wrappers
`results/LLMs/llms.tex` and `results/LLMs/llm-per-emotion.tex` are delivered and
**must not be modified** — they own `\begin{tabular}`, the header, and the
`Average` row, and they append the final ` \\` after each `\input`.

Inputs: `results/llm_models_metrics.csv` (module 03), `results/per_emotion_metrics.csv`
(module 04), the display-name map in Spec 00 §7. Deterministic string formatting;
no randomness.

---

## 1. Shared rules

- Every numeric field: `f"{x:.2f}"` (two decimals). This applies to metrics
  **and** to the coverage percentage.
- A row = fields joined by ` & `. The file = rows joined by `" \\\\\n"` — i.e.
  every row **except the last** ends with ` \\`; the wrapper's `\input{...} \\`
  supplies the last one.
- No `\hline`, no `\midrule`, no header — data rows only.
- First field of every row = the model **display name** (Spec 00 §7), verbatim
  (including the `Mixtral` casing quirk — match the committed file being
  regenerated).

## 2. `llm_results_rows.tex` — wrapper `llms.tex`

- **16 rows, ordered by model directory name** (`sorted(os.listdir)`), i.e. the
  same order as `llm_models_metrics.csv`:
  `deepseek-r1_14b, deepseek-r1_32b, deepseek-r1_8b, gemma3_12b, gemma3_27b,
  gpt-oss_20b, llama3.1_latest, llama4_latest, mistral-nemo_latest,
  mistral-small3.2_latest, mistral_7b, mixtral_8x7b, phi4-mini_latest, phi4_14b,
  qwen3_14b, qwen3_30b`.
- Each row: `display & <Full block (13)> & <Test block (13)>`.
- A **block** for subset `S` is, in order (all from the
  `llm_models_metrics.csv` rows for that model):

  | # | value | source column |
  |---|---|---|
  | 1 | Coverage % | `coverage_inclusive` (of `context`,`S`) × 100 |
  | 2–4 | Context macro Pr, Re, F1 | `precision_macro, recall_macro, f1_macro` (`context`, `S`) |
  | 5–7 | Context weighted Pr, Re, F1 | `precision_weighted, recall_weighted, f1_weighted` (`context`, `S`) |
  | 8–10 | No-context macro Pr, Re, F1 | `*_macro` (`nocontext`, `S`) |
  | 11–13 | No-context weighted Pr, Re, F1 | `*_weighted` (`nocontext`, `S`) |

  The Coverage % shown is the **context** row's `coverage_inclusive`.
- Anchor (verify): `DeepSeek-R1 (8B)` → Full block starts
  `8.97 & 0.03 & 0.10 & 0.04 & 0.00 & 0.01 & 0.01 & …`, Test block starts
  `9.09 & …`.

## 3. `per_emotion_llm_{noctx,ctx}_{full,test}_rows.tex` — wrapper `llm-per-emotion.tex`

| File | context | subset |
|---|---|---|
| `per_emotion_llm_noctx_full_rows.tex` | nocontext | full |
| `per_emotion_llm_noctx_test_rows.tex` | nocontext | test |
| `per_emotion_llm_ctx_full_rows.tex` | context | full |
| `per_emotion_llm_ctx_test_rows.tex` | context | test |

- **16 rows, ordered by display-name string** (`sorted` on the display name) —
  note this differs from §2: here `Mistral (7B)` precedes `Mistral-Nemo (12B)`
  precedes `Mistral-Small 3.2 (24B)`, and `Phi-4 (14B)` precedes
  `Phi-4-Mini (3.8B)`.
- Each row: `display` + `Pr & Re & F1` for the seven emotions in **wrapper column
  order** `[Neutral, Happiness, Anger, Surprise, Sadness, Fear, Disgust]` = 21
  numeric fields.
- Values: `per_emotion_metrics.csv` filtered to
  `(model == <dir>, context == <this file's context>, subset == <this file's subset>)`,
  one `(precision, recall, f1)` triple per emotion.
- Anchor (verify): `per_emotion_llm_noctx_full_rows.tex`, `DeepSeek-R1 (14B)` →
  `0.88 & 0.97 & 0.92 & 0.31 & 0.09 & 0.14 & 0.10 & 0.04 & 0.06 & 0.00 & 0.00 & 0.00 & 0.17 & 0.25 & 0.20 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00 & 0.00`.

## 4. Validation

Regenerate all five files and `diff` against the committed copies — they must
match byte-for-byte (modulo a possible trailing newline). If a per-emotion file
does not match, the fault is upstream in module 04's `per_emotion_metrics.csv`.

## 5. Libraries

`pandas`, `os`. No scikit-learn, no `ollama`.
