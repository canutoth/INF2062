# Specification 02 — Inference: With-Context Configuration

Reference script: `results/results_ctxt/emotion_labeler_context.py` (**authoritative**
for this module — it has the `MODEL_LIST` loop, the context-window logic and the
`build_user_message` helper).
Configuration label: `context`.
Output directory: `results/results_ctxt/<model>/`.

Requires a running Ollama server. **If the delivered `all_<model>.json` bundles
are used, skip this module.** Shares Spec 00 §3, §4, §6.

---

## 1. Purpose

For every model, classify each of the 782 target utterances while also showing
the model up to `AMOUNT_CONTEXT = 15` strictly-earlier utterances from the same
meeting; write one prediction bundle per model.

## 2. Input

- `data/transcriptions/target/output_v{1,3,4,5}/segment_NNN.txt` — 782 files.
- `data/transcriptions/context/output_v{1,3,4,5}/segment_NNN.txt` — 783 files
  (= target ids + `output_v1/segment_182`).
- `results/results_ctxt/prompt_context.txt` — system prompt (§5.1).
- Model tags: Spec 00 §6 (the script's `MODEL_LIST` also lists `llama3.3:70b` /
  a duplicate `gemma3:27b` — skip those).

Both folders are loaded by `load_text_files()` into records
`{file_id, output_version, content, file_path}`, grouped by `output_version`,
each group sorted by `_extract_num(file_id) = int(file_id.split("_")[-1])`.

## 3. Processing

For each `model`, for each meeting, for each target entry (in numeric order):

1. `target_num = _extract_num(target_id)`.
2. `context_nums` = sorted numeric ids of the meeting's **context** entries.
   `pos = bisect_left(context_nums, target_num)` (0 if no context entries).
3. If `AMOUNT_CONTEXT > 0 and pos > 0`:
   `context_segments = context_entries[max(0, pos - 15) : pos]`; else `[]`.
   (So a target at or before the first context id gets an empty window.)
4. `messages = [{system, prompt_context}, {user, build_user_message(...)}]` (§5).
5. Call Ollama (§5.3), retry ≤ 3, `sleep(2)`.
6. `None` → skip. `json.loads` → on `JSONDecodeError` skip. On success add
   `text_content`, `timestamp`, `context_size = len(context_segments)`,
   `context_ids = [c["file_id"] for c in context_segments]`.
7. After each meeting, write `results/results_ctxt/<model>/<meeting>.json`; at the
   end write `all_<model>.json`.

## 4. Model iteration

`if __name__ == "__main__"` loops `MODEL_LIST`, setting `OLLAMA_MODEL` and
`RESULTS_FOLDER = results/results_ctxt/<model>/` per model.

## 5. Prompt & call

### 5.1 System prompt — `results/results_ctxt/prompt_context.txt` (verbatim)

Identical to Spec 01 §5.1 except the second paragraph gains one sentence:

```
Esses trechos estão escritos em português brasileiro.
Você também receberá um contexto anterior da reunião para ajudar na classificação.
```

Response JSON keys: `emoção`, `justificativa`.

### 5.2 User message — `build_user_message()` (verbatim structure)

Lines joined by `"\n"`:

```
Contexto anterior:
[{file_id}] {content}          ← one line per selected context segment, in order
                               ← (if the window is empty, instead: the single
                                  line "    (Sem contexto anterior disponível)")

```
{target_text}
```                 
                               ← blank line
JSON de resposta:
```

The target block is literally ```` ```\n{target_text}\n``` ```` followed by 17
trailing spaces (an artefact of the reference f-string). Reproduce
`build_user_message` exactly rather than re-deriving the whitespace.

### 5.3 Ollama call

```python
ollama_client.chat(
    model=OLLAMA_MODEL, messages=messages,
    format="json", stream=False, think=False,
    options={"temperature": 0, "num_predict": 200},
)
```

(The committed context script keeps `format="json"` / `think=False` for **all**
models, including the reasoning ones.)

### 5.4 Output entry (`results/results_ctxt/<model>/all_<model>.json`)

```json
{
  "output_v1": {
    "segment_003": {
      "emoção": "…",
      "justificativa": "…",
      "text_content": "…",
      "timestamp": "%Y-%m-%d %H:%M:%S",
      "context_size": 3,
      "context_ids": ["segment_000", "segment_001", "segment_002"]
    }
  }
}
```

`json.dump(..., ensure_ascii=False, indent=2)`. Per-meeting `output_v*.json` are
also written (one object per meeting, same per-segment schema).

## 6. Outputs

`results/results_ctxt/<model>/all_<model>.json` (+ `output_v*.json`) for each of
the 16 models.

## 7. Libraries

`ollama`, `json`, `os`, `time`, `glob`, `pathlib`, `bisect`, `tqdm`.
