#!/usr/bin/env python3
"""Specification 02 — Inference: With-Context Configuration.

For every model in Spec 00 §6, classify each of the 782 target utterances while
also showing up to AMOUNT_CONTEXT = 15 strictly-earlier utterances from the same
meeting, and write:

    <out>/results_ctxt/<model>/<meeting>.json     (one per meeting)
    <out>/results_ctxt/<model>/all_<model>.json

Reference script (authoritative for this module):
``results/results_ctxt/emotion_labeler_context.py`` — its MODEL_LIST loop,
context-window logic and ``build_user_message`` helper are reproduced verbatim.

Requires a running Ollama server with every Spec 00 §6 tag already pulled;
models are never pulled implicitly (Spec 00 §3).  **If the delivered
all_<model>.json bundles are used, skip this module** — a re-run will not
bit-match them.

Decoding is deterministic (`temperature = 0`); no RNG applies (Spec 00 §3).

Run from the repository root:  python claude/02_inference_context.py
"""

from __future__ import annotations

import argparse
import glob
import json
import os
import sys
import time
from bisect import bisect_left
from pathlib import Path
from typing import Dict, List, Optional

from tqdm import tqdm

import ollama

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repro_common import (  # noqa: E402
    CONTEXT_DATASET_FOLDER,
    MODEL_LIST,
    PROMPT_CONTEXT_PATH,
    TARGET_DATASET_FOLDER,
    ensure_dir,
    resolve_output_root,
)

ollama_client = ollama.Client()

# Spec 02 §1 — context window size.
AMOUNT_CONTEXT = 15

MAX_RETRIES = 3
RETRY_SLEEP_SECONDS = 2

# Spec 02 §5.1 — system prompt, verbatim from
# results/results_ctxt/emotion_labeler_context.py (which produced the delivered
# bundles).  Note: the delivered prompt_context.txt wraps the second paragraph
# over two lines; the script keeps it on one.  The script wins.
SYSTEM_PROMPT = """
Você é um robô construído para identificar emoções em trechos transcritos de reuniões. 

Esses trechos estão escritos em português brasileiro. Você também receberá um contexto anterior da reunião para ajudar na classificação.

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


def get_system_prompt() -> str:
    return SYSTEM_PROMPT


def check_prompt_file() -> None:
    """Non-fatal: report the known line-wrap divergence from the .txt."""
    if not os.path.exists(PROMPT_CONTEXT_PATH):
        return
    with open(PROMPT_CONTEXT_PATH, encoding="utf-8") as f:
        on_disk = f.read()
    if on_disk.strip() != SYSTEM_PROMPT.strip():
        print(
            "NOTE: prompt_context.txt differs from the reference script's "
            "prompt by a line wrap in the second paragraph; the script's "
            "version is used (Spec 02 header: the script is authoritative).",
            file=sys.stderr,
        )


def load_text_files(folder: str) -> List[dict]:
    """Spec 02 §2 — verbatim from emotion_labeler_context.py."""
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


def build_user_message(target_id: str, target_text: str,
                       context_segments: List[dict]) -> str:
    """Spec 02 §5.2 — verbatim from emotion_labeler_context.py.

    The target block is ```\\n{target_text}\\n``` followed by 17 trailing spaces,
    an artefact of the reference f-string.  Do not re-derive the whitespace.
    """
    parts = []
    if context_segments:
        parts.append(f"Contexto anterior:")
        for seg in context_segments:
            parts.append(f"[{seg['file_id']}] {seg['content']}")
    else:
        parts.append(f"Contexto anterior:")
        parts.append("    (Sem contexto anterior disponível)")
    parts.append("")
    parts.append(f"""\
```
{target_text}
```\
                 """)
    parts.append("")
    parts.append("JSON de resposta:")
    return "\n".join(parts)


def _extract_num(file_id: str) -> int:
    """Spec 02 §3.1 — verbatim from emotion_labeler_context.py."""
    try:
        return int(file_id.split('_')[-1])
    except Exception:  # noqa: BLE001
        return -1


def available_model_tags() -> set:
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


def ask_ollama(model: str, target_id: str, target_text: str,
               context_segments: List[dict],
               max_retries: int = MAX_RETRIES) -> Optional[str]:
    """Spec 02 §5.3 — format="json" / think=False for **all** models."""
    messages = [
        {"role": "system", "content": get_system_prompt()},
        {"role": "user", "content": build_user_message(
            target_id, target_text, context_segments)},
    ]
    for attempt in range(max_retries):
        try:
            response = ollama_client.chat(
                model=model,
                messages=messages,
                format="json",
                stream=False,
                think=False,
                options={"temperature": 0, "num_predict": 200},
            )
            return response["message"]["content"]
        except Exception as e:  # noqa: BLE001 — mirrors the reference script
            print(f"Ollama request failed (attempt {attempt+1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                time.sleep(RETRY_SLEEP_SECONDS)
    print(f"Ollama failed after {max_retries} attempts.")
    return None


def group_and_sort(dataset: List[dict]) -> Dict[str, List[dict]]:
    grouped: Dict[str, List[dict]] = {}
    for entry in dataset:
        grouped.setdefault(entry["output_version"], []).append(entry)
    for entries in grouped.values():
        entries.sort(key=lambda x: _extract_num(x["file_id"]))
    return grouped


def run_model(model: str, dataset_target: List[dict], dataset_context: List[dict],
              out_root: str) -> str:
    """Spec 02 §3/§4/§6 — per-meeting files plus one all_<model>.json."""
    slug = model.replace(":", "_")
    results_folder = ensure_dir(os.path.join(out_root, "results_ctxt", slug))

    grouped_target = group_and_sort(dataset_target)
    grouped_context = group_and_sort(dataset_context)
    context_nums_by_version = {
        version: [_extract_num(e["file_id"]) for e in entries]
        for version, entries in grouped_context.items()
    }

    results_by_version: Dict[str, dict] = {}

    for version, target_entries in grouped_target.items():
        results_by_version[version] = {}
        context_entries = grouped_context.get(version, [])
        context_nums = context_nums_by_version.get(version, [])

        for entry in tqdm(target_entries, desc=f"[{model}] {version}"):
            target_id = entry["file_id"]
            target_num = _extract_num(target_id)

            # Spec 02 §3.2/§3.3 — strictly-earlier window of at most 15.
            pos = bisect_left(context_nums, target_num) if context_nums else 0
            if AMOUNT_CONTEXT > 0 and pos > 0:
                start = max(0, pos - AMOUNT_CONTEXT)
                context_segments = context_entries[start:pos]
            else:
                context_segments = []

            classification = ask_ollama(
                model, target_id, entry["content"], context_segments
            )
            if classification is None:
                continue
            try:
                emotion_data = json.loads(classification)
            except json.JSONDecodeError:
                continue
            emotion_data["text_content"] = entry["content"]
            emotion_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            emotion_data["context_size"] = len(context_segments)
            emotion_data["context_ids"] = [c["file_id"] for c in context_segments]
            results_by_version[version][target_id] = emotion_data

        # Spec 02 §3.7 — write the meeting file after each meeting.
        version_file = os.path.join(results_folder, f"{version}.json")
        with open(version_file, "w", encoding="utf-8") as f:
            json.dump(results_by_version[version], f, ensure_ascii=False, indent=2)
        print(f"Saved {version}: {len(results_by_version[version])} segments")

    all_file = os.path.join(results_folder, f"all_{slug}.json")
    with open(all_file, "w", encoding="utf-8") as f:
        json.dump(results_by_version, f, ensure_ascii=False, indent=2)

    total = sum(len(v) for v in results_by_version.values())
    print(f"Saved: {all_file} ({total}/{len(dataset_target)} segments)")
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
    dataset_target = load_text_files(TARGET_DATASET_FOLDER)
    dataset_context = load_text_files(CONTEXT_DATASET_FOLDER)
    if not dataset_target:
        raise FileNotFoundError(
            f"no target text files found under {TARGET_DATASET_FOLDER}"
        )
    print(f"found target={len(dataset_target)} | context={len(dataset_context)} text files")

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
        run_model(model, dataset_target, dataset_context, out_root)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
