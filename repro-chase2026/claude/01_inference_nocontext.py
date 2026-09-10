#!/usr/bin/env python3
"""Specification 01 — Inference: No-Context Configuration.

For every model in Spec 00 §6, classify each of the 782 target utterances
seeing **only that utterance**, and write one prediction bundle per model:

    <out>/results_no_ctxt/<model>/all_<model>.json

Requires a running Ollama server with every Spec 00 §6 tag already pulled.
Models are never pulled implicitly (Spec 00 §3) — a missing tag fails loudly.

**If the delivered all_<model>.json bundles are used, skip this module**: a
re-run will not bit-match them (Ollama / model-weight drift, Spec 00 §3) and
modules 03-04 consume the delivered bundles.

Decoding is deterministic (`temperature = 0`); no RNG is involved, so no seed
applies (Spec 00 §3).

Run from the repository root:  python claude/01_inference_nocontext.py
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import time
from pathlib import Path
from typing import List, Optional

from tqdm import tqdm

import ollama

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repro_common import (  # noqa: E402
    MODEL_LIST,
    PROMPT_NOCONTEXT_PATH,
    REASONING_MODELS,
    TARGET_DATASET_FOLDER,
    ensure_dir,
    resolve_output_root,
)

ollama_client = ollama.Client()

# Spec 01 §5.1 — system prompt, verbatim from
# results/results_no_ctxt/emotion_labeler_no-context.py (which produced the
# delivered bundles): leading and trailing newline included.
SYSTEM_PROMPT = """
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
"""

# Spec 01 §5.1 — prompt_no-context.txt appends the user template to the same
# file; the split form (§5.2) is used, so the file's system portion is the text
# before this marker.
_PROMPT_FILE_USER_MARKER = "\n\nClassifique, portanto, o seguinte trecho:"

MAX_RETRIES = 3
RETRY_SLEEP_SECONDS = 2


def get_system_prompt() -> str:
    return SYSTEM_PROMPT


def check_prompt_file() -> None:
    """Non-fatal: confirm the embedded prompt matches the delivered .txt."""
    if not os.path.exists(PROMPT_NOCONTEXT_PATH):
        return
    with open(PROMPT_NOCONTEXT_PATH, encoding="utf-8") as f:
        on_disk = f.read()
    system_portion = on_disk.split(_PROMPT_FILE_USER_MARKER)[0]
    if system_portion != SYSTEM_PROMPT.strip():
        print(
            "WARNING: embedded system prompt differs from "
            f"{PROMPT_NOCONTEXT_PATH}; using the reference script's version "
            "(it produced the delivered bundles).",
            file=sys.stderr,
        )


def build_user_message(text: str) -> str:
    """Spec 01 §5.2 — verbatim from emotion_labeler_no-context.py.

    Leading and trailing blank line, and a single trailing space after
    'JSON de resposta:'.
    """
    return f"""
Classifique o seguinte trecho:

Trecho da mensagem: {text}
JSON de resposta: 
"""


def load_text_files(folder: str) -> List[dict]:
    """Spec 01 §2 — sorted meetings, sorted files; empty content is skipped."""
    dataset: List[dict] = []
    output_folders = sorted(glob.glob(f"{str(folder)}/output_v*"))
    for output_folder in output_folders:
        output_name = Path(output_folder).name
        txt_files = sorted(glob.glob(f"{output_folder}/*.txt"))
        for txt_file in txt_files:
            try:
                with open(txt_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                if content:
                    dataset.append({
                        "file_id": Path(txt_file).stem,
                        "output_version": output_name,
                        "content": content,
                        "file_path": txt_file,
                    })
            except Exception as e:  # noqa: BLE001 — mirrors the reference script
                print(f"Error reading {txt_file}: {e}")
    return dataset


def available_model_tags() -> set:
    """Tags already present on the server; never triggers a pull."""
    listing = ollama_client.list()
    models = listing.get("models", []) if isinstance(listing, dict) else getattr(listing, "models", [])
    tags = set()
    for entry in models:
        name = entry.get("model") or entry.get("name") if isinstance(entry, dict) else (
            getattr(entry, "model", None) or getattr(entry, "name", None)
        )
        if name:
            tags.add(name)
            if name.endswith(":latest"):
                tags.add(name[: -len(":latest")])
    return tags


def ask_ollama(model: str, text: str, max_retries: int = MAX_RETRIES) -> Optional[str]:
    """Spec 01 §5.3 — deterministic chat call, retry <= 3 with sleep(2)."""
    messages = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": build_user_message(text)},
    ]

    # Spec 00 §6 — the reference no-context script's comments: reasoning models
    # drop format="json" and set think=True.
    reasoning = model in REASONING_MODELS
    kwargs = dict(
        model=model,
        messages=messages,
        stream=False,
        think=reasoning,
        options={"temperature": 0, "num_predict": 200},
    )
    if not reasoning:
        kwargs["format"] = "json"

    for attempt in range(max_retries):
        try:
            response = ollama_client.chat(**kwargs)
            return response["message"]["content"]
        except Exception as e:  # noqa: BLE001 — mirrors the reference script
            print(f"Ollama request failed (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(RETRY_SLEEP_SECONDS)
    print(f"Ollama failed after {max_retries} attempts.")
    return None


def run_model(model: str, dataset: List[dict], out_root: str) -> str:
    """Spec 01 §3/§4/§6 — one all_<model>.json per model."""
    slug = model.replace(":", "_")
    results_folder = ensure_dir(os.path.join(out_root, "results_no_ctxt", slug))

    all_results: dict = {}
    for entry in tqdm(dataset, desc=f"[{model}] no-context"):
        classification = ask_ollama(model, entry["content"])
        if classification is None:
            # Spec 01 §3.3 — no entry written; a missing prediction downstream.
            continue
        try:
            emotion_data = json.loads(classification)
        except json.JSONDecodeError:
            # Spec 01 §3.4 — unparseable output: skip the segment.
            continue
        emotion_data["text_content"] = entry["content"]
        emotion_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        all_results.setdefault(entry["output_version"], {})[entry["file_id"]] = emotion_data

    all_file = os.path.join(results_folder, f"all_{slug}.json")
    with open(all_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    total = sum(len(v) for v in all_results.values())
    print(f"Saved: {all_file} ({total}/{len(dataset)} segments)")
    return all_file


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", default=None,
                        help="Directory mirroring results/ (default: claude/results).")
    parser.add_argument("--models", nargs="*", default=None,
                        help="Subset of Spec 00 §6 tags to run (default: all 16).")
    args = parser.parse_args()

    out_root = ensure_dir(resolve_output_root(args.output_root))
    models = args.models if args.models else list(MODEL_LIST)

    check_prompt_file()

    print("Loading text files...")
    dataset = load_text_files(TARGET_DATASET_FOLDER)
    if not dataset:
        raise FileNotFoundError(
            f"no target text files found under {TARGET_DATASET_FOLDER}"
        )
    print(f"found {len(dataset)}/782 text files")

    # Spec 00 §3 — never pull a model implicitly; fail loudly with the tag.
    try:
        present = available_model_tags()
    except Exception as e:  # noqa: BLE001
        raise SystemExit(
            f"Cannot reach the Ollama server ({e}). Start it and pull the "
            f"Spec 00 §6 tags before running this module."
        )
    missing = [m for m in models if m not in present]
    if missing:
        raise SystemExit(
            "Missing Ollama model tags (pull them explicitly, this script will "
            "not): " + ", ".join(missing)
        )

    for model in models:
        print(f"\n==============================\n"
              f"Running for model: {model}\n"
              f"==============================")
        run_model(model, dataset, out_root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
