# Specification 00 — Study Overview & Reproduction Environment

## 1. Study

**Title:** *Emotion Recognition in Agile Software Meetings: A Comparative Study
of ML, DL, and Text-based LLM Approaches* (CHASE 2026).

**Scope of this reproduction:** the **text-based LLM track only**. The classical
ML and the deep-learning (RNN / embedding) tracks are **out of scope** and must
not be implemented or imported.

**Task:** classify the predominant emotion of Portuguese-language utterances
transcribed from real agile software-development meetings, using **open-weight
LLMs served locally through [Ollama](https://ollama.com)**, in two
configurations:

- **No context** — the model sees only the target utterance.
- **With context** — the model also sees up to 15 preceding utterances from the
  same meeting.

Decoding is deterministic (`temperature = 0`); the model answers with a JSON
object.

**Definition of done:** the generated `llm_models_metrics.csv`, its ranking CSVs
and the per-emotion CSVs match the delivered reference artifacts under
`results/` within rounding.

### 1.1 Module map

| Module | Type | Scope | Spec |
|---|---|---|---|
| 01 | code-gen | run every model, no-context prompt → `results_no_ctxt/<model>/all_<model>.json` | `01_inference_nocontext.spec.md` |
| 02 | code-gen | run every model, context prompt (15-utterance window) → `results_ctxt/<model>/all_<model>.json` | `02_inference_context.spec.md` |
| 03 | code-gen | score predictions vs. ground truth → `llm_models_metrics.csv` + 5 ranking CSVs | `03_evaluation_metrics.spec.md` |
| 04 | run + reproduce | per-emotion metrics + context-effect report (reference scripts provided) | `04_per_emotion_analysis.spec.md` |
| 05 | code-gen | LaTeX table rows for `results/LLMs/` | `05_latex_tables.spec.md` |

Modules 01–02 need a running Ollama server. Modules 03–04 consume the delivered
prediction bundles and run offline — they are the reproducible core.

## 2. Delivered material (audited 2026-09-10)

```text
data/transcriptions/
├── target/output_v{1,3,4,5}/segment_NNN.txt      # 782 files  (v1 182, v3 118, v4 286, v5 196)
└── context/output_v{1,3,4,5}/segment_NNN.txt      # 783 files  = target set + output_v1/segment_182
results/
├── manual_labelling.json                          # ground truth, 769 labels
├── data_splits.csv                                # File Path,Emotion,Split  (616 train / 155 test)
├── llm_models_metrics.csv                         # reference output of module 03 (64 rows)
├── llm_models_metrics_ranking_{context,nocontext}_{full,test}.csv   # 16 rows each
├── llm_models_metrics_rankings_all.csv            # 64 rows + 3 ranking_* columns
├── results_no_ctxt/
│   ├── prompt_no-context.txt                      # system prompt (module 01 §5.1)
│   ├── emotion_labeler_no-context.py              # reference script (rough, single-model)
│   └── <model>/all_<model>.json                   # 16 models — predictions
└── results_ctxt/
    ├── prompt_context.txt                         # system prompt (module 02 §5.1)
    ├── emotion_labeler_context.py                 # reference script (MODEL_LIST loop)
    └── <model>/all_<model>.json (+ output_v*.json for most models)
├── LLMs/
│   ├── llms.tex                                   # wrapper — \input{...llm_results_rows}, adds Average
│   ├── llm-per-emotion.tex                        # wrapper — 4 tables, \input{...per_emotion_llm_*_rows}
│   ├── llm_results_rows.tex                       # reference output of module 05 (16 rows)
│   └── per_emotion_llm_{ctx,noctx}_{full,test}_rows.tex   # reference outputs of module 05 (16 rows each)
tools/
├── compare_per_emotion.py                         # AUTHORITATIVE — module 04 per-emotion CSVs
└── compare_context_effect.py                      # AUTHORITATIVE — module 04 context-effect report
```

**Not delivered** (affects only the modules noted): `src/LLMs/requirements.txt`
(pins) · the `llm_models_metrics.csv` **generator** (module 03 writes it, validates
against the committed CSV) · `per_emotion_metrics*.csv` (module 04 regenerates
them) · the `*_rows.tex` **generator** (module 05 writes it, validates against the
committed `results/LLMs/*_rows.tex`).

**Removed as out of scope** (do not look for them): the audio recordings, the
video sources, and the transcript-/ground-truth-production tooling
(`convert.py`, `cut_videos_*.py`, `gemini_*.py`, `convert_manual_csv_to_json.py`).
The transcripts and `manual_labelling.json` are the given inputs.

## 3. Environment & constraints

- **Language:** Python 3.10+.
- **Dependencies (pinned):**
  ```
  scikit-learn==1.3.2      # classification metrics change across minor versions — exact pin
  pandas==2.1.4            # contemporaneous with sklearn 1.3.2
  numpy==1.26.4
  ollama                   # modules 01–02 only
  tqdm                     # modules 01–02 only
  ```
  No other third-party library may be imported. Record resolved versions in the
  run manifest.
- **Path convention:** every script is executed **from the repository root**.
  Input/output paths in each module spec are repo-root-relative and must be used
  exactly.
- **Determinism / seeds:**
  - Inference (01–02): `options={"temperature": 0}`; no RNG seed applies. Even so,
    a re-run will **not** bit-match the delivered bundles (Ollama / model-weight
    drift) — that is expected; modules 03–04 consume the *delivered* bundles.
  - Evaluation (03–04): pure pandas / scikit-learn scoring, **no stochastic
    operation** — do not introduce `np.random.seed` or any randomness. All
    iteration orders are fixed and explicit.
- **Autonomous execution:** run silently, suppress non-critical warnings (e.g.
  `sklearn` `UndefinedMetricWarning`). Never pull an Ollama model implicitly —
  fail loudly with the missing tag.
- Output directories created with `os.makedirs(..., exist_ok=True)`.

## 4. Emotion label set (verified against `compare_per_emotion.py`)

Seven classes. Prompts and raw model output are Portuguese; all metrics use the
**canonical English** labels.

| Portuguese (`EMOTION_MAPPING_PT_TO_EN`) | Canonical (English) |
|---|---|
| felicidade | Happiness |
| tristeza | Sadness |
| medo | Fear |
| raiva | Anger |
| surpresa | Surprise |
| desgosto | Disgust |
| neutro | Neutral |

### 4.1 Label normalisation — `normalize_label()` in `compare_per_emotion.py` (verbatim)

Given a raw predicted value `v`:

1. If falsy → `None`.
2. `raw = str(v).strip().lower()`.
3. If `raw` in the PT→EN table → the English label.
4. Else if `raw` in the alias table → its label:
   `happy|happiness→Happiness`, `sad|sadness→Sadness`, `fear|afraid→Fear`,
   `angry|anger→Anger`, `surprise|surprised→Surprise`,
   `disgust|disgusted→Disgust`, `neutral→Neutral`.
5. Else `cap = raw.capitalize()`; if `cap` in the 7 canonical labels → `cap`.
6. Else → `None` (**hallucination**).

### 4.2 Fixed label orders

- **Metrics / per-emotion CSV order** — `LABELS_ORDER = sorted(CANONICAL_LABELS)`
  = `[Anger, Disgust, Fear, Happiness, Neutral, Sadness, Surprise]`.
- **LaTeX per-emotion column order** (`results/LLMs/llm-per-emotion.tex` header) —
  `[Neutral, Happiness, Anger, Surprise, Sadness, Fear, Disgust]`.

## 5. Input data reference

### 5.1 Transcripts (`data/transcriptions/`)

- `target/output_v{1,3,4,5}/segment_NNN.txt` — 782 files. Ids **contiguous**
  `segment_000 … segment_{N-1}` per meeting; zero-padded 3 digits; no `output_v2`.
  File text (`.strip()`-ed) is the target utterance.
- `context/…` — 783 files = every target id **plus `output_v1/segment_182`**.
- The reference scripts load with `sorted(glob.glob(...))` — lexicographic order,
  which equals numeric order because ids are zero-padded.

### 5.2 Ground truth (`results/manual_labelling.json`)

```json
{ "output_v1": { "segment_000": { "principal_emocao_detectada": "Happiness" }, … }, … }
```

- 4 meetings; **769** labelled segments: `output_v1` 182, `output_v3` 118,
  `output_v4` 284, `output_v5` 185. (13 target `.txt` files are unlabelled and
  excluded from evaluation.)
- Label distribution: `Neutral 666, Happiness 53, Anger 24, Surprise 14,
  Sadness 5, Disgust 4, Fear 3`.
- Key is `principal_emocao_detectada`; value is already a canonical English label.

### 5.3 Split (`results/data_splits.csv`)

- Columns `File Path, Emotion, Split`. 771 rows: **616 train, 155 test**.
- `File Path` e.g. `output_v4\segment_187.m4a`. Join-key derivation
  (`load_splits()` in `compare_per_emotion.py`): replace `/`→`\`, then `\`→`os.sep`,
  split, `parts[0]` = `output_name`, `os.path.splitext(parts[1])[0]` = `segment_id`.
  `Split` is `str(...).strip().lower()` (tolerates trailing `\r`).
- `read_csv` default reader handles the file's line endings.
- **154** of the 155 `test` rows also carry a label (→ `test` subset size).

### 5.4 Predictions (`results/results_{ctxt,no_ctxt}/<model>/all_<model>.json`)

```json
{
  "output_v1": {
    "segment_000": {
      "emoção": "neutro",
      "justificativa": "…",
      "text_content": "…",
      "timestamp": "YYYY-MM-DD HH:MM:SS",
      "context_size": 0,               // context config only
      "context_ids": []                // context config only
    }, …
  }, …
}
```

- One directory per model (tag with `:` → `_`). `all_<model>.json` is canonical;
  the per-meeting `output_v*.json` files (present for most context models, absent
  for `gpt-oss_20b` / `llama4_latest` context and for all no-context models) are
  ignored by every downstream script.
- Bundles are **often incomplete** — a model that failed the JSON format has
  fewer than 782 entries (e.g. `deepseek-r1_8b` no-context has 381). Module 03's
  coverage / hallucination columns quantify this.
- The label key is `emoção` (the prompt asks for it); `extract_pred_label()`
  tries, in order, `principal_emocao_detectada, emoção, emocao, emotion, label,
  pred` for models that disobeyed.

## 6. Models (verified against `results/results_*/` and `emotion_labeler_context.py MODEL_LIST`)

16 model directories exist per configuration (`:` → `_`):

```
deepseek-r1_8b   deepseek-r1_14b   deepseek-r1_32b
gemma3_12b       gemma3_27b
gpt-oss_20b
llama3.1_latest  llama4_latest
mistral_7b       mistral-nemo_latest   mistral-small3.2_latest
mixtral_8x7b
phi4-mini_latest phi4_14b
qwen3_14b        qwen3_30b
```

- `MODEL_LIST` in `emotion_labeler_context.py` also lists `llama3.3:70b` (and
  double-lists `gemma3:27b`); **no `llama3.3_70b` results exist** — exclude it.
- `deepseek-r1_8b` scores near zero — it fails the JSON format for most segments.
  Reproduce as-is; the low score falls out of the coverage math, do not special-case.
- **Reasoning models** (`gpt-oss:20b`, `deepseek-r1:*`): the reference no-context
  script's comments say to drop `format="json"` and set `think=True`; the
  committed context script leaves `format="json"` / `think=False` for all. Match
  whichever the delivered bundle for that model looks like — but since modules
  03–04 use the delivered bundles, this only matters for a full re-run.

## 7. Model display names

`llm_models_metrics.csv` and the per-emotion CSVs use the **directory name**
verbatim in their `model` column. Only the LaTeX row files (module 05) use
display names. Map (derived from `results/LLMs/*_rows.tex`):

| Directory | Display name |
|---|---|
| `deepseek-r1_8b` | `DeepSeek-R1 (8B)` |
| `deepseek-r1_14b` | `DeepSeek-R1 (14B)` |
| `deepseek-r1_32b` | `DeepSeek-R1 (32B)` |
| `gemma3_12b` | `Gemma-3 (12B)` |
| `gemma3_27b` | `Gemma-3 (27B)` |
| `gpt-oss_20b` | `Gpt-Oss (20B)` |
| `llama3.1_latest` | `Llama 3.1 (8B)` |
| `llama4_latest` | `Llama 4 (17B)` |
| `mistral_7b` | `Mistral (7B)` |
| `mistral-nemo_latest` | `Mistral-Nemo (12B)` |
| `mistral-small3.2_latest` | `Mistral-Small 3.2 (24B)` |
| `mixtral_8x7b` | `Mixtral-8x (7B)` in `llm_results_rows.tex`; `Mixtral 8x (7B)` / `Mixtral 8X (7B)` in the per-emotion files — the reference files are **inconsistent**; match each file as committed |
| `phi4-mini_latest` | `Phi-4-Mini (3.8B)` |
| `phi4_14b` | `Phi-4 (14B)` |
| `qwen3_14b` | `Qwen-3 (14B)` |
| `qwen3_30b` | `Qwen-3 (30B)` |
