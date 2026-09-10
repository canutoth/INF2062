# Specification 01 — Inference: No-Context Configuration

Reference script: `results/results_no_ctxt/emotion_labeler_no-context.py` (rough —
hardcodes one model and reads a `dataset/` folder; treat as a behaviour sketch,
not a template).
Configuration label: `nocontext`.
Output directory: `results/results_no_ctxt/<model>/`.

Requires a running Ollama server with every Spec 00 §6 tag pulled. **If the
delivered `all_<model>.json` bundles are used, skip this module** — a re-run will
not bit-match them and modules 03–04 consume the delivered bundles.

Shares Spec 00 §3 (environment), §4 (labels), §6 (models).

---

## 1. Purpose

For every model, classify each of the 782 target utterances seeing **only that
utterance**, and write one prediction bundle per model.

## 2. Input

- `data/transcriptions/target/output_v{1,3,4,5}/segment_NNN.txt` — 782 files.
  `content = open(path, encoding="utf-8").read().strip()`; skip a file whose
  content is empty.
- `results/results_no_ctxt/prompt_no-context.txt` — the system + user prompt
  text. Read verbatim; §5 quotes it.
- Model tags: Spec 00 §6.

Meeting = the `output_vN` directory name; `segment_id` = file stem
(`segment_NNN`). Iterate meetings sorted (`output_v1, output_v3, output_v4,
output_v5`) and, within a meeting, files sorted lexicographically (== numeric,
ids are zero-padded).

## 3. Processing

For each `model`, for each `(meeting, segment_id)`:

1. Build `messages` = `[{role: system, content: SYSTEM_PROMPT}, {role: user,
   content: USER_MESSAGE}]` (§5).
2. Call Ollama (§5.3). Retry ≤ 3 times, `time.sleep(2)` between attempts; on
   total failure the classification is `None`.
3. If `None` → skip the segment (no entry written; it becomes a *missing
   prediction* downstream).
4. Else `emotion_data = json.loads(classification)` — on `JSONDecodeError`, skip
   the segment. On success, add `text_content` and `timestamp` (§5.4) and store
   under `all_results[meeting][segment_id]`.

All 782 targets are attempted; no ground-truth filtering here.

## 4. Model iteration

`OLLAMA_MODEL` is set per model; `RESULTS_FOLDER =
results/results_no_ctxt/<model>/` (`:`→`_`). One `all_<model>.json` per model.
(The delivered reference script processes a single hardcoded model; the delivered
*results* cover all 16, so wrap it in a loop over Spec 00 §6.)

## 5. Prompt & call

### 5.1 System prompt — `results/results_no_ctxt/prompt_no-context.txt` (verbatim, LF, tabs before the list items)

```
Você é um robô construído para identificar emoções em trechos transcritos de reuniões. 

Esses trechos estão escritos em português brasileiro.

Cada trecho pode ser classificado como apenas uma dessas opções:
	- felicidade
	- tristeza
	- medo
	- raiva
	- surpresa
	- desgosto
	- neutro

Classifique a mensagem como "neutro" quando houver ausência de emoção.

Para cada trecho, dê também uma curta justificativa para sua classificação. Sua justificativa também deverá ser escrita em português brasileiro.

A resposta deve ser feita no seguinte formato, e deve conter apenas o JSON da resposta:

{
    "emoção": "<principal emoção>",
    "justificativa": "explicação curta em português brasileiro"
}
```

The `prompt_no-context.txt` file appends the user-message template to the same
file; the reference script instead passes it as a separate `user` message. Use
the split form (§5.2). The response JSON keys are **`emoção`** and
**`justificativa`**.

### 5.2 User message (`emotion_labeler_no-context.py`, verbatim)

```

Classifique o seguinte trecho:

Trecho da mensagem: {content}
JSON de resposta: 

```

(leading and trailing blank line, single trailing space after `JSON de
resposta:`, `{content}` = the target text.)

### 5.3 Ollama call (`emotion_labeler_no-context.py`, verbatim)

```python
ollama_client.chat(
    model=OLLAMA_MODEL,
    messages=messages,
    format="json",      # commented out for gpt-oss / reasoning models
    stream=False,
    think=False,        # True for gpt-oss / reasoning models
    options={"temperature": 0, "num_predict": 200},
)
# uses response['message']['content']
```

### 5.4 Output entry (`results/results_no_ctxt/<model>/all_<model>.json`)

```json
{
  "output_v1": {
    "segment_000": {
      "emoção": "…",                    // from the parsed model JSON, verbatim (not normalised)
      "justificativa": "…",             // from the parsed model JSON
      "text_content": "…",              // the target text sent
      "timestamp": "%Y-%m-%d %H:%M:%S"  // time.strftime at record time
    }
  }
}
```

- Whatever keys the model returned are kept verbatim; only `text_content` and
  `timestamp` are added. No `context_size` / `context_ids` in this config.
- `json.dump(..., ensure_ascii=False, indent=2)`.
- Per-meeting `output_v*.json` files are **not** produced in the no-context
  config.

## 6. Outputs

`results/results_no_ctxt/<model>/all_<model>.json` for each of the 16 models.
`os.makedirs(..., exist_ok=True)`.

## 7. Libraries

`ollama`, `json`, `os`, `time`, `glob`, `pathlib`, `tqdm`. No scikit-learn, no
pandas.
