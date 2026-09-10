"""Shared constants, paths and loader/normaliser helpers.

Spec 00 (Study Overview) + Spec 03 §2/§4 + Spec 04 §1.

The loader / normaliser helpers below are reproduced **verbatim** from the
authoritative ``tools/compare_per_emotion.py`` (Spec 03: "Reuse the
loader/normaliser helpers from tools/compare_per_emotion.py verbatim
(load_ground_truth, normalize_label, load_splits, extract_pred_label,
collect_pairs)").

No randomness anywhere in the evaluation path (Spec 00 §3) — no seed is set
because no stochastic operation exists.
"""

from __future__ import annotations

import glob
import json
import os
import warnings
from typing import Dict, List, Optional, Tuple

import pandas as pd

# Spec 00 §3 — autonomous execution: suppress non-critical warnings
# (e.g. sklearn UndefinedMetricWarning).
warnings.filterwarnings("ignore")
os.environ.setdefault("PYTHONWARNINGS", "ignore")


# --------------------------------------------------------------------------
# Paths (Spec 00 §3 — repo-root-relative, scripts executed from the repo root)
# --------------------------------------------------------------------------
# Resolved from this file's location so the scripts also work when invoked with
# an absolute path; the layout is identical to running from the repo root.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Delivered, read-only material (Spec 00 §2).
DATA_ROOT = os.path.join(REPO_ROOT, "data")
RESULTS_ROOT = os.path.join(REPO_ROOT, "results")

GROUND_TRUTH_PATH = os.path.join(RESULTS_ROOT, "manual_labelling.json")
SPLITS_PATH = os.path.join(RESULTS_ROOT, "data_splits.csv")

TARGET_DATASET_FOLDER = os.path.join(DATA_ROOT, "transcriptions", "target")
CONTEXT_DATASET_FOLDER = os.path.join(DATA_ROOT, "transcriptions", "context")

PROMPT_NOCONTEXT_PATH = os.path.join(
    RESULTS_ROOT, "results_no_ctxt", "prompt_no-context.txt"
)
PROMPT_CONTEXT_PATH = os.path.join(RESULTS_ROOT, "results_ctxt", "prompt_context.txt")

# Generated artefacts.  The specs name paths under ``results/``; this
# reproduction is sandboxed to ``claude/`` and therefore mirrors the exact
# ``results/`` sub-tree under ``claude/results/`` by default.  Pass
# ``--output-root results`` (or set REPRO_OUTPUT_ROOT) to write to the literal
# spec paths.
DEFAULT_OUTPUT_ROOT = os.path.join(REPO_ROOT, "claude", "results")


def resolve_output_root(cli_value: Optional[str] = None) -> str:
    """Output root for generated artefacts, mirroring the ``results/`` layout."""
    value = cli_value or os.environ.get("REPRO_OUTPUT_ROOT") or DEFAULT_OUTPUT_ROOT
    if not os.path.isabs(value):
        value = os.path.join(REPO_ROOT, value)
    return os.path.normpath(value)


# Prediction bundles (delivered): (sub-directory, configuration label).
# Spec 03 §5 row order / Spec 04 §1.2 iteration order.
PREDICTION_SPECS: List[Tuple[str, str]] = [
    ("results_ctxt", "context"),
    ("results_no_ctxt", "nocontext"),
]

# Spec 03 §3 — subset grid.  The committed ``llm_models_metrics.csv`` emits
# ('test', 'full') per model (verified against the delivered 64-row file);
# the ranking CSVs re-sort anyway.
SUBSET_WRITE_ORDER: Tuple[str, ...] = ("test", "full")


# --------------------------------------------------------------------------
# Spec 00 §4 — emotion label set (verbatim from tools/compare_per_emotion.py)
# --------------------------------------------------------------------------
EMOTION_MAPPING_PT_TO_EN = {
    'felicidade': 'Happiness',
    'tristeza': 'Sadness',
    'medo': 'Fear',
    'raiva': 'Anger',
    'surpresa': 'Surprise',
    'desgosto': 'Disgust',
    'neutro': 'Neutral',
}
CANONICAL_LABELS = set(EMOTION_MAPPING_PT_TO_EN.values())

# Spec 00 §4.2 — metrics / per-emotion CSV order.
LABELS_ORDER = sorted(CANONICAL_LABELS)

# Spec 00 §4.2 — LaTeX per-emotion column order (results/LLMs/llm-per-emotion.tex).
LATEX_EMOTION_ORDER = [
    'Neutral', 'Happiness', 'Anger', 'Surprise', 'Sadness', 'Fear', 'Disgust',
]

# Spec 00 §6 — the 16 model tags (llama3.3:70b excluded: no results exist;
# the duplicated gemma3:27b is de-duplicated).
MODEL_LIST: List[str] = [
    "deepseek-r1:8b",
    "deepseek-r1:14b",
    "deepseek-r1:32b",
    "gemma3:12b",
    "gemma3:27b",
    "gpt-oss:20b",
    "llama3.1:latest",
    "llama4:latest",
    "mistral:7b",
    "mistral-nemo:latest",
    "mistral-small3.2:latest",
    "mixtral:8x7b",
    "phi4-mini:latest",
    "phi4:14b",
    "qwen3:14b",
    "qwen3:30b",
]

# Spec 00 §6 — reasoning models: the no-context reference script's comments say
# to drop format="json" and set think=True for these.
REASONING_MODELS = {"gpt-oss:20b", "deepseek-r1:8b", "deepseek-r1:14b", "deepseek-r1:32b"}

# Spec 00 §7 — directory name -> LaTeX display name.
DISPLAY_NAMES: Dict[str, str] = {
    'deepseek-r1_8b': 'DeepSeek-R1 (8B)',
    'deepseek-r1_14b': 'DeepSeek-R1 (14B)',
    'deepseek-r1_32b': 'DeepSeek-R1 (32B)',
    'gemma3_12b': 'Gemma-3 (12B)',
    'gemma3_27b': 'Gemma-3 (27B)',
    'gpt-oss_20b': 'Gpt-Oss (20B)',
    'llama3.1_latest': 'Llama 3.1 (8B)',
    'llama4_latest': 'Llama 4 (17B)',
    'mistral_7b': 'Mistral (7B)',
    'mistral-nemo_latest': 'Mistral-Nemo (12B)',
    'mistral-small3.2_latest': 'Mistral-Small 3.2 (24B)',
    'mixtral_8x7b': 'Mixtral-8x (7B)',   # llm_results_rows.tex spelling
    'phi4-mini_latest': 'Phi-4-Mini (3.8B)',
    'phi4_14b': 'Phi-4 (14B)',
    'qwen3_14b': 'Qwen-3 (14B)',
    'qwen3_30b': 'Qwen-3 (30B)',
}

# Spec 00 §7 / Spec 05 §1 — the committed per-emotion row files spell Mixtral
# differently per subset; match each file as committed.
PER_EMOTION_DISPLAY_OVERRIDES: Dict[str, Dict[str, str]] = {
    'full': {'mixtral_8x7b': 'Mixtral 8x (7B)'},
    'test': {'mixtral_8x7b': 'Mixtral 8X (7B)'},
}


def display_name(model_dir: str, subset: Optional[str] = None) -> str:
    """Spec 00 §7 display name; ``subset`` selects the per-emotion spelling."""
    if subset is not None:
        override = PER_EMOTION_DISPLAY_OVERRIDES.get(subset, {})
        if model_dir in override:
            return override[model_dir]
    return DISPLAY_NAMES[model_dir]


# --------------------------------------------------------------------------
# Loader / normaliser helpers — verbatim from tools/compare_per_emotion.py
# --------------------------------------------------------------------------
def load_ground_truth(gt_path: str) -> Dict[str, Dict[str, str]]:
    with open(gt_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    gt: Dict[str, Dict[str, str]] = {}
    for output_name, segments in data.items():
        gt[output_name] = {}
        for seg_id, seg_data in segments.items():
            label = seg_data.get('principal_emocao_detectada')
            gt[output_name][seg_id] = label
    return gt


def normalize_label(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    raw = str(value).strip().lower()

    if raw in EMOTION_MAPPING_PT_TO_EN:
        return EMOTION_MAPPING_PT_TO_EN[raw]

    alias = {
        'happy': 'Happiness', 'happiness': 'Happiness',
        'sad': 'Sadness', 'sadness': 'Sadness',
        'fear': 'Fear', 'afraid': 'Fear',
        'angry': 'Anger', 'anger': 'Anger',
        'surprise': 'Surprise', 'surprised': 'Surprise',
        'disgust': 'Disgust', 'disgusted': 'Disgust',
        'neutral': 'Neutral',
    }
    if raw in alias:
        return alias[raw]

    cap = raw.capitalize()
    if cap in CANONICAL_LABELS:
        return cap
    return None


def load_splits(csv_path: str) -> Dict[Tuple[str, str], str]:
    df = pd.read_csv(csv_path)
    mapping: Dict[Tuple[str, str], str] = {}
    for _, row in df.iterrows():
        file_path = str(row['File Path'])
        split = str(row['Split']).strip().lower()
        file_path = file_path.replace('/', '\\').replace('\\', os.sep)
        parts = file_path.split(os.sep)
        if len(parts) >= 2:
            output_name = parts[0]
            seg_with_ext = parts[1]
            seg = os.path.splitext(seg_with_ext)[0]
            mapping[(output_name, seg)] = split
    return mapping


def extract_pred_label(seg_obj: dict) -> Optional[str]:
    for key in (
        'principal_emocao_detectada', 'emoção', 'emocao', 'emotion', 'label', 'pred'
    ):
        if key in seg_obj and seg_obj[key]:
            return str(seg_obj[key])
    return None


def load_model_predictions(all_json_path: str) -> Dict[str, Dict[str, Optional[str]]]:
    with open(all_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    preds: Dict[str, Dict[str, Optional[str]]] = {}
    for output_name, segments in data.items():
        if not isinstance(segments, dict):
            continue
        preds[output_name] = {}
        for seg_id, seg_obj in segments.items():
            if not isinstance(seg_obj, dict):
                continue
            raw_label = extract_pred_label(seg_obj)
            preds[output_name][seg_id] = normalize_label(raw_label)
    return preds


def collect_pairs(gt: Dict[str, Dict[str, str]],
                  preds: Dict[str, Dict[str, Optional[str]]],
                  subset: Optional[str],
                  split_map: Dict[Tuple[str, str], str]) -> Tuple[List[str], List[str]]:
    y_true: List[str] = []
    y_pred: List[str] = []
    for output_name, segs_gt in gt.items():
        if output_name not in preds:
            continue
        segs_pred = preds[output_name]
        for seg_id, true_label in segs_gt.items():
            if subset == 'test' and split_map.get((output_name, seg_id), None) != 'test':
                continue
            if seg_id not in segs_pred:
                continue
            pred_label = segs_pred.get(seg_id)
            if pred_label is None:
                continue
            y_true.append(true_label)
            y_pred.append(pred_label)
    return y_true, y_pred


# --------------------------------------------------------------------------
# Model discovery (Spec 03 §2 / Spec 04 §1.2)
# --------------------------------------------------------------------------
def discover_models(ctx_dir: str) -> List[Tuple[str, str]]:
    """``sorted(os.listdir)`` sub-directories that hold an ``all_*.json``."""
    found: List[Tuple[str, str]] = []
    if not os.path.isdir(ctx_dir):
        return found
    for name in sorted(os.listdir(ctx_dir)):
        model_dir = os.path.join(ctx_dir, name)
        if not os.path.isdir(model_dir):
            continue
        json_candidates = glob.glob(os.path.join(model_dir, 'all_*.json'))
        if not json_candidates:
            continue
        found.append((name, json_candidates[0]))
    return found


def ensure_dir(path: str) -> str:
    os.makedirs(path, exist_ok=True)
    return path
