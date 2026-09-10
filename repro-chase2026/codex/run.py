#!/usr/bin/env python3
import argparse
import glob
import json
import os
import platform
import sys
import time
import warnings
from bisect import bisect_left
from pathlib import Path

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR / "outputs"

AMOUNT_CONTEXT = 15

EMOTION_MAPPING_PT_TO_EN = {
    "felicidade": "Happiness",
    "tristeza": "Sadness",
    "medo": "Fear",
    "raiva": "Anger",
    "surpresa": "Surprise",
    "desgosto": "Disgust",
    "neutro": "Neutral",
}
CANONICAL_LABELS = set(EMOTION_MAPPING_PT_TO_EN.values())
LABELS_ORDER = sorted(CANONICAL_LABELS)
PER_EMOTION_COLUMN_ORDER = ["Neutral", "Happiness", "Anger", "Surprise", "Sadness", "Fear", "Disgust"]

MODEL_LIST = [
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

REASONING_MODELS = ("gpt-oss", "deepseek-r1")

DISPLAY_NAMES = {
    "deepseek-r1_8b": "DeepSeek-R1 (8B)",
    "deepseek-r1_14b": "DeepSeek-R1 (14B)",
    "deepseek-r1_32b": "DeepSeek-R1 (32B)",
    "gemma3_12b": "Gemma-3 (12B)",
    "gemma3_27b": "Gemma-3 (27B)",
    "gpt-oss_20b": "Gpt-Oss (20B)",
    "llama3.1_latest": "Llama 3.1 (8B)",
    "llama4_latest": "Llama 4 (17B)",
    "mistral_7b": "Mistral (7B)",
    "mistral-nemo_latest": "Mistral-Nemo (12B)",
    "mistral-small3.2_latest": "Mistral-Small 3.2 (24B)",
    "phi4-mini_latest": "Phi-4-Mini (3.8B)",
    "phi4_14b": "Phi-4 (14B)",
    "qwen3_14b": "Qwen-3 (14B)",
    "qwen3_30b": "Qwen-3 (30B)",
}

METRICS_COLUMNS = [
    "model_id", "model", "context", "subset",
    "precision_weighted", "recall_weighted", "f1_weighted",
    "precision_macro", "recall_macro", "f1_macro",
    "accuracy", "samples",
    "hallucination_rate", "coverage",
    "hallucination_rate_inclusive", "coverage_inclusive",
    "total_expected", "total_seen", "missing_predictions",
]

PRINT_MODEL = None


def load_ground_truth(gt_path):
    with open(gt_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    gt = {}
    for output_name, segments in data.items():
        gt[output_name] = {}
        for seg_id, seg_data in segments.items():
            label = seg_data.get("principal_emocao_detectada")
            gt[output_name][seg_id] = label
    return gt


def normalize_label(value):
    if not value:
        return None
    raw = str(value).strip().lower()
    if raw in EMOTION_MAPPING_PT_TO_EN:
        return EMOTION_MAPPING_PT_TO_EN[raw]
    alias = {
        "happy": "Happiness", "happiness": "Happiness",
        "sad": "Sadness", "sadness": "Sadness",
        "fear": "Fear", "afraid": "Fear",
        "angry": "Anger", "anger": "Anger",
        "surprise": "Surprise", "surprised": "Surprise",
        "disgust": "Disgust", "disgusted": "Disgust",
        "neutral": "Neutral",
    }
    if raw in alias:
        return alias[raw]
    cap = raw.capitalize()
    if cap in CANONICAL_LABELS:
        return cap
    return None


def load_splits(csv_path):
    import pandas as pd
    df = pd.read_csv(csv_path)
    mapping = {}
    for _, row in df.iterrows():
        file_path = str(row["File Path"])
        split = str(row["Split"]).strip().lower()
        file_path = file_path.replace("/", "\\").replace("\\", os.sep)
        parts = file_path.split(os.sep)
        if len(parts) >= 2:
            output_name = parts[0]
            seg = os.path.splitext(parts[1])[0]
            mapping[(output_name, seg)] = split
    return mapping


def extract_pred_label(seg_obj):
    for key in (
        "principal_emocao_detectada", "emoção", "emocao", "emotion", "label", "pred"
    ):
        if key in seg_obj and seg_obj[key]:
            return str(seg_obj[key])
    return None


def load_model_predictions(all_json_path):
    with open(all_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    preds = {}
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


def collect_pairs(gt, preds, subset, split_map):
    y_true = []
    y_pred = []
    for output_name, segs_gt in gt.items():
        if output_name not in preds:
            continue
        segs_pred = preds[output_name]
        for seg_id, true_label in segs_gt.items():
            if subset == "test" and split_map.get((output_name, seg_id), None) != "test":
                continue
            if seg_id not in segs_pred:
                continue
            pred_label = segs_pred.get(seg_id)
            if pred_label is None:
                continue
            y_true.append(true_label)
            y_pred.append(pred_label)
    return y_true, y_pred


def predictions_root(subdir):
    own = OUTPUT_DIR / subdir
    if own.is_dir():
        return own
    committed = RESULTS_DIR / subdir
    if committed.is_dir():
        return committed
    return own


def discover_models(subdir):
    cdir = predictions_root(subdir)
    if not cdir.is_dir():
        raise FileNotFoundError(f"Predictions directory not found: {cdir}")
    models = []
    for name in sorted(os.listdir(str(cdir))):
        model_dir = cdir / name
        if not model_dir.is_dir():
            continue
        if not glob.glob(str(model_dir / "all_*.json")):
            continue
        models.append(name)
    return models


def check_ollama_models(models):
    import ollama
    client = ollama.Client()
    available = set()
    try:
        for m in client.list()["models"]:
            available.add(m["name"])
    except KeyError:
        for m in client.list():
            item = m if isinstance(m, dict) else m.get("model", "")
            available.add(item.get("name", item.get("model", "")))
    missing = [m for m in models if m not in available]
    if missing:
        raise RuntimeError("Ollama is missing the following tags: " + ", ".join(missing))
    return client


def load_text_files(folder):
    dataset = []
    output_folders = sorted(glob.glob(str(Path(folder) / "output_v*")))
    for output_folder in output_folders:
        output_name = Path(output_folder).name
        txt_files = sorted(glob.glob(str(Path(output_folder) / "*.txt")))
        for txt_file in txt_files:
            with open(txt_file, "r", encoding="utf-8") as f:
                content = f.read().strip()
            if content:
                dataset.append({
                    "file_id": Path(txt_file).stem,
                    "output_version": output_name,
                    "content": content,
                    "file_path": txt_file,
                })
    return dataset


def _extract_num(file_id):
    try:
        return int(file_id.split("_")[-1])
    except Exception:
        return -1


def module01_inference_nocontext():
    from tqdm import tqdm
    client = check_ollama_models(MODEL_LIST)
    system_prompt = read_nocontext_prompt()
    for model in MODEL_LIST:
        model_dir = OUTPUT_DIR / "results_no_ctxt" / model.replace(":", "_")
        os.makedirs(str(model_dir), exist_ok=True)
        dataset = load_text_files(ROOT / "data" / "transcriptions" / "target")
        use_format = not any(model.startswith(r) for r in REASONING_MODELS)
        think = any(model.startswith(r) for r in REASONING_MODELS)
        all_results = {}
        for entry in tqdm(dataset, desc=f"Analyzing {model}"):
            classification = ask_ollama_nocontext(client, model, entry["content"], system_prompt, use_format, think)
            if classification is None:
                continue
            try:
                emotion_data = json.loads(classification)
            except json.JSONDecodeError:
                continue
            emotion_data["text_content"] = entry["content"]
            emotion_data["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
            all_results.setdefault(entry["output_version"], {})[entry["file_id"]] = emotion_data
        out_file = model_dir / f"all_{model.replace(':', '_')}.json"
        with open(str(out_file), "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
    print("module 01 complete")


def read_nocontext_prompt():
    prompt_path = RESULTS_DIR / "results_no_ctxt" / "prompt_no-context.txt"
    full = Path(prompt_path).read_text(encoding="utf-8")
    marker = "Classifique, portanto"
    idx = full.find(marker)
    if idx != -1:
        return full[:idx].strip()
    return full.strip()


def ask_ollama_nocontext(client, model, text, system_prompt, use_format, think, max_retries=3):
    user_message = (
        "\n"
        "Classifique o seguinte trecho:\n"
        "\n"
        f"Trecho da mensagem: {text}\n"
        "JSON de resposta: \n"
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message},
    ]
    kwargs = {
        "model": model,
        "messages": messages,
        "stream": False,
        "think": think,
        "options": {"temperature": 0, "num_predict": 200},
    }
    if use_format:
        kwargs["format"] = "json"
    for attempt in range(max_retries):
        try:
            response = client.chat(**kwargs)
            return response["message"]["content"]
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(2)
    return None


def module02_inference_context():
    from tqdm import tqdm
    client = check_ollama_models(MODEL_LIST)
    system_prompt = read_context_prompt()
    for model in MODEL_LIST:
        model_dir = OUTPUT_DIR / "results_ctxt" / model.replace(":", "_")
        os.makedirs(str(model_dir), exist_ok=True)
        dataset_target = load_text_files(ROOT / "data" / "transcriptions" / "target")
        dataset_context = load_text_files(ROOT / "data" / "transcriptions" / "context")
        grouped_target = {}
        grouped_context = {}
        for entry in dataset_target:
            grouped_target.setdefault(entry["output_version"], []).append(entry)
        for entry in dataset_context:
            grouped_context.setdefault(entry["output_version"], []).append(entry)
        for entries in grouped_target.values():
            entries.sort(key=lambda x: _extract_num(x["file_id"]))
        for entries in grouped_context.values():
            entries.sort(key=lambda x: _extract_num(x["file_id"]))
        context_nums_by_version = {}
        for version, entries in grouped_context.items():
            context_nums_by_version[version] = [_extract_num(e["file_id"]) for e in entries]
        results_by_version = {}
        for version, target_entries in grouped_target.items():
            results_by_version[version] = {}
            context_entries = grouped_context.get(version, [])
            context_nums = context_nums_by_version.get(version, [])
            for entry in tqdm(target_entries, desc=f"Analyzing {version}"):
                target_id = entry["file_id"]
                target_num = _extract_num(target_id)
                if context_nums:
                    pos = bisect_left(context_nums, target_num)
                else:
                    pos = 0
                if AMOUNT_CONTEXT > 0 and pos > 0:
                    start = max(0, pos - AMOUNT_CONTEXT)
                    context_segments = context_entries[start:pos]
                else:
                    context_segments = []
                user_content = build_user_message(target_id, entry["content"], context_segments)
                classification = ask_ollama_context(client, model, user_content, system_prompt)
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
            version_file = model_dir / f"{version}.json"
            with open(str(version_file), "w", encoding="utf-8") as f:
                json.dump(results_by_version[version], f, ensure_ascii=False, indent=2)
        all_file = model_dir / f"all_{model.replace(':', '_')}.json"
        with open(str(all_file), "w", encoding="utf-8") as f:
            json.dump(results_by_version, f, ensure_ascii=False, indent=2)
    print("module 02 complete")


def read_context_prompt():
    prompt_path = RESULTS_DIR / "results_ctxt" / "prompt_context.txt"
    return Path(prompt_path).read_text(encoding="utf-8")


def build_user_message(target_id, target_text, context_segments):
    parts = []
    if context_segments:
        parts.append("Contexto anterior:")
        for seg in context_segments:
            parts.append(f"[{seg['file_id']}] {seg['content']}")
    else:
        parts.append("Contexto anterior:")
        parts.append("    (Sem contexto anterior disponível)")
    parts.append("")
    parts.append(
        "```\n"
        + target_text
        + "\n```"
        + "                 "
    )
    parts.append("")
    parts.append("JSON de resposta:")
    return "\n".join(parts)


def ask_ollama_context(client, model, user_content, system_prompt, max_retries=3):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content},
    ]
    for attempt in range(max_retries):
        try:
            response = client.chat(
                model=model,
                messages=messages,
                format="json",
                stream=False,
                think=False,
                options={"temperature": 0, "num_predict": 200},
            )
            return response["message"]["content"]
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(2)
    return None


def module03_evaluation_metrics():
    from sklearn.metrics import precision_recall_fscore_support, accuracy_score
    gt = load_ground_truth(str(RESULTS_DIR / "manual_labelling.json"))
    split_map = load_splits(str(RESULTS_DIR / "data_splits.csv"))
    rows = []
    for subdir, ctx in [("results_ctxt", "context"), ("results_no_ctxt", "nocontext")]:
        pdir = predictions_root(subdir)
        models = discover_models(subdir)
        for name in models:
            all_json = glob.glob(str(pdir / name / "all_*.json"))[0]
            preds = load_model_predictions(all_json)
            for subset in ("test", "full"):
                subset_arg = None if subset == "full" else "test"
                y_true = []
                y_pred = []
                total_expected = 0
                total_seen = 0
                hallucinations = 0
                samples = 0
                for output_name, segs_gt in gt.items():
                    for seg_id, true_label in segs_gt.items():
                        if subset == "test" and split_map.get((output_name, seg_id), None) != "test":
                            continue
                        total_expected += 1
                        if output_name in preds and seg_id in preds[output_name]:
                            total_seen += 1
                            pred_label = preds[output_name][seg_id]
                            if pred_label is None:
                                hallucinations += 1
                            else:
                                samples += 1
                                y_true.append(true_label)
                                y_pred.append(pred_label)
                if y_true:
                    p_w, r_w, f_w, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)
                    p_m, r_m, f_m, _ = precision_recall_fscore_support(y_true, y_pred, average="macro", zero_division=0)
                    acc = accuracy_score(y_true, y_pred)
                else:
                    p_w = r_w = f_w = p_m = r_m = f_m = acc = 0.0
                if samples:
                    hallucination_rate = hallucinations / total_seen
                    coverage = samples / total_seen
                else:
                    hallucination_rate = 0.0
                    coverage = 0.0
                hallucination_rate_inclusive = (total_expected - total_seen + hallucinations) / total_expected
                coverage_inclusive = samples / total_expected
                rows.append({
                    "model_id": f"{name}-{ctx}-{subset}",
                    "model": name,
                    "context": ctx,
                    "subset": subset,
                    "precision_weighted": float(p_w),
                    "recall_weighted": float(r_w),
                    "f1_weighted": float(f_w),
                    "precision_macro": float(p_m),
                    "recall_macro": float(r_m),
                    "f1_macro": float(f_m),
                    "accuracy": float(acc),
                    "samples": int(samples),
                    "hallucination_rate": float(hallucination_rate),
                    "coverage": float(coverage),
                    "hallucination_rate_inclusive": float(hallucination_rate_inclusive),
                    "coverage_inclusive": float(coverage_inclusive),
                    "total_expected": int(total_expected),
                    "total_seen": int(total_seen),
                    "missing_predictions": int(total_expected - total_seen),
                })
    import pandas as pd
    df = pd.DataFrame(rows, columns=METRICS_COLUMNS)
    os.makedirs(str(OUTPUT_DIR), exist_ok=True)
    round_cols = [
        "precision_weighted", "recall_weighted", "f1_weighted",
        "precision_macro", "recall_macro", "f1_macro",
        "accuracy", "hallucination_rate", "coverage",
        "hallucination_rate_inclusive", "coverage_inclusive",
    ]
    for col in round_cols:
        df[col] = df[col].round(6)
    df.to_csv(str(OUTPUT_DIR / "llm_models_metrics.csv"), index=False, encoding="utf-8")
    for ctx in ("context", "nocontext"):
        for subset in ("full", "test"):
            sub = df[(df["context"] == ctx) & (df["subset"] == subset)].sort_values("f1_macro", ascending=False)
            sub.to_csv(str(OUTPUT_DIR / f"llm_models_metrics_ranking_{ctx}_{subset}.csv"), index=False, encoding="utf-8")
    blocks = [
        (df[(df["context"] == "context") & (df["subset"] == "full")], "with context and full data", "context", "full"),
        (df[(df["context"] == "context") & (df["subset"] == "test")], "with context and test data", "context", "test"),
        (df[(df["context"] == "nocontext") & (df["subset"] == "full")], "without context and full data", "nocontext", "full"),
        (df[(df["context"] == "nocontext") & (df["subset"] == "test")], "without context and test data", "nocontext", "test"),
    ]
    parts = []
    for block, title, ctx_label, subset_label in blocks:
        b = block.copy().sort_values("f1_macro", ascending=False)
        b["ranking_title"] = title
        b["ranking_context"] = ctx_label
        b["ranking_subset"] = subset_label
        parts.append(b)
    rankings_all = pd.concat(parts, ignore_index=True, sort=False)
    rankings_all.to_csv(str(OUTPUT_DIR / "llm_models_metrics_rankings_all.csv"), index=False, encoding="utf-8")
    print("module 03 complete")


def per_emotion_metrics(y_true, y_pred):
    from sklearn.metrics import precision_recall_fscore_support
    import pandas as pd
    if not y_true:
        return pd.DataFrame({
            "emotion": LABELS_ORDER,
            "precision": [0.0] * len(LABELS_ORDER),
            "recall": [0.0] * len(LABELS_ORDER),
            "f1": [0.0] * len(LABELS_ORDER),
            "support": [0] * len(LABELS_ORDER),
        })
    p, r, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=LABELS_ORDER, average=None, zero_division=0
    )
    return pd.DataFrame({
        "emotion": LABELS_ORDER,
        "precision": p,
        "recall": r,
        "f1": f1,
        "support": support,
    })


def module04_per_emotion():
    import pandas as pd
    gt = load_ground_truth(str(RESULTS_DIR / "manual_labelling.json"))
    split_map = load_splits(str(RESULTS_DIR / "data_splits.csv"))
    specs = [
        ("results_ctxt", "context"),
        ("results_no_ctxt", "nocontext"),
    ]
    rows = []
    for subdir, ctx in specs:
        cdir = predictions_root(subdir)
        if not cdir.is_dir():
            continue
        for name in sorted(os.listdir(str(cdir))):
            model_dir = cdir / name
            if not model_dir.is_dir():
                continue
            json_candidates = glob.glob(str(model_dir / "all_*.json"))
            if not json_candidates:
                continue
            all_json = json_candidates[0]
            preds = load_model_predictions(all_json)
            for subset in ("full", "test"):
                subset_arg = None if subset == "full" else "test"
                y_true, y_pred = collect_pairs(gt, preds, subset_arg, split_map)
                df_em = per_emotion_metrics(y_true, y_pred)
                for _, r in df_em.iterrows():
                    rows.append({
                        "model": name,
                        "context": ctx,
                        "subset": subset,
                        "emotion": r["emotion"],
                        "precision": float(r["precision"]),
                        "recall": float(r["recall"]),
                        "f1": float(r["f1"]),
                        "support": int(r["support"]),
                    })
    if not rows:
        print("No per-emotion results found.")
        return
    df_base = pd.DataFrame(rows)
    out_dir = OUTPUT_DIR
    os.makedirs(str(out_dir), exist_ok=True)
    base_csv = out_dir / "per_emotion_metrics.csv"
    df_base.to_csv(str(base_csv), index=False, encoding="utf-8")
    print(f"Saved: {base_csv}")

    piv_cols = ["model", "subset", "emotion"]
    ctx_df = df_base[df_base["context"] == "context"][piv_cols + ["precision", "recall", "f1"]].copy()
    nctx_df = df_base[df_base["context"] == "nocontext"][piv_cols + ["precision", "recall", "f1"]].copy()
    ctx_df = ctx_df.rename(columns={
        "precision": "precision_context",
        "recall": "recall_context",
        "f1": "f1_context",
    })
    nctx_df = nctx_df.rename(columns={
        "precision": "precision_nocontext",
        "recall": "recall_nocontext",
        "f1": "f1_nocontext",
    })
    cmp_df = pd.merge(ctx_df, nctx_df, on=piv_cols, how="inner")
    if not cmp_df.empty:
        cmp_df["precision_delta"] = cmp_df["precision_context"] - cmp_df["precision_nocontext"]
        cmp_df["recall_delta"] = cmp_df["recall_context"] - cmp_df["recall_nocontext"]
        cmp_df["f1_delta"] = cmp_df["f1_context"] - cmp_df["f1_nocontext"]

        def pct(a, b):
            if b and b != 0:
                return (a - b) / b * 100.0
            return float("nan")
        cmp_df["f1_pct_change"] = cmp_df.apply(lambda r: pct(r["f1_context"], r["f1_nocontext"]), axis=1)
        cmp_df["precision_pct_change"] = cmp_df.apply(lambda r: pct(r["precision_context"], r["precision_nocontext"]), axis=1)
        cmp_df["recall_pct_change"] = cmp_df.apply(lambda r: pct(r["recall_context"], r["recall_nocontext"]), axis=1)

    cmp_csv = out_dir / "per_emotion_metrics_comparison.csv"
    cmp_df.to_csv(str(cmp_csv), index=False, encoding="utf-8")
    print(f"Saved: {cmp_csv}")

    if not cmp_df.empty:
        wide = cmp_df.copy()
        wide = wide.set_index(["model", "emotion", "subset"])
        keep_cols = [
            "precision_context", "precision_nocontext",
            "recall_context", "recall_nocontext",
            "f1_context", "f1_nocontext",
        ]
        wide = wide[keep_cols]
        wide = wide.unstack("subset")
        wide.columns = [f"{metric}_{subset}_{'context' if 'context' in metric else 'nocontext'}" for metric, subset in wide.columns]
        desired = []
        for m in ("precision", "recall", "f1"):
            for subset in ("full", "test"):
                for ctx in ("context", "nocontext"):
                    desired.append(f"{m}_{subset}_{ctx}")
        cols = [c for c in desired if c in wide.columns]
        other_cols = [c for c in wide.columns if c not in cols]
        wide = wide[cols + other_cols]
        wide = wide.reset_index()

        wide_csv = out_dir / "per_emotion_metrics_wide.csv"
        wide.to_csv(str(wide_csv), index=False, encoding="utf-8")
        print(f"Saved: {wide_csv}")

    for subset in ("full", "test"):
        print(f"\n=== Top F1 improvements per emotion (subset={subset}) ===")
        sub = cmp_df[cmp_df["subset"] == subset]
        if sub.empty:
            print("No data")
            continue
        for emo in LABELS_ORDER:
            emo_df = sub[sub["emotion"] == emo]
            if emo_df.empty:
                continue
            top = emo_df.sort_values(by="f1_delta", ascending=False).head(5)
            if top.empty:
                continue
            print(f"\nEmotion: {emo}")
            for _, row in top.iterrows():
                print(
                    f"- {row['model']}: f1_ctx={row['f1_context']:.2f} | f1_nctx={row['f1_nocontext']:.2f} | "
                    f"delta={row['f1_delta']:+.2f} ({row['f1_pct_change']:.2f}%)"
                )

    if PRINT_MODEL:
        print(f"\n=== Per-emotion metrics for model: {PRINT_MODEL} ===")
        mdf = cmp_df[cmp_df["model"] == PRINT_MODEL]
        if mdf.empty:
            print("No data for this model (ensure it exists in both context and nocontext).")
        else:
            for subset in ("full", "test"):
                ms = mdf[mdf["subset"] == subset]
                if ms.empty:
                    continue
                print(f"\nSubset: {subset}")
                ms = ms.copy()
                ms["emotion"] = pd.Categorical(ms["emotion"], categories=LABELS_ORDER, ordered=True)
                ms = ms.sort_values("emotion")
                for _, row in ms.iterrows():
                    print(
                        f"{row['emotion']}: "
                        f"P/R/F1 ctx={row['precision_context']:.2f}/{row['recall_context']:.2f}/{row['f1_context']:.2f} | "
                        f"nctx={row['precision_nocontext']:.2f}/{row['recall_nocontext']:.2f}/{row['f1_nocontext']:.2f} | "
                        f"ΔF1={row['f1_delta']:+.2f} ({row['f1_pct_change']:.2f}%)"
                    )

    print("module 04 complete")


def module04_context_effect():
    import pandas as pd
    csv_path = OUTPUT_DIR / "llm_models_metrics.csv"
    if not csv_path.exists():
        raise FileNotFoundError(f"Metrics CSV not found: {csv_path}. Run module 03 first.")
    df = pd.read_csv(str(csv_path))
    required = {"model", "context", "subset", "f1_macro"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in CSV: {missing}")
    df["subset"] = df["subset"].astype(str).str.lower()
    df["context"] = df["context"].astype(str).str.lower()
    df["model"] = df["model"].astype(str)
    df["f1_macro"] = pd.to_numeric(df["f1_macro"], errors="coerce")

    subsets = []
    if "full" in df["subset"].unique():
        subsets.append("full")
    if "test" in df["subset"].unique():
        subsets.append("test")
    if not subsets:
        print("No supported subsets found in CSV (expected 'full' and/or 'test').")
        return

    for sub in subsets:
        print_report(df, sub)
    print("module 04 (context effect) complete")


def compute_context_delta(df, subset):
    import pandas as pd
    sub = subset.strip().lower()
    sub_df = df[df["subset"] == sub].copy()
    pivot = sub_df.pivot_table(index="model", columns="context", values="f1_macro", aggfunc="max")
    for col in ["context", "nocontext"]:
        if col not in pivot.columns:
            pivot[col] = float("nan")
    both = pivot.dropna(subset=["context", "nocontext"]).reset_index()
    both = both.rename(columns={"context": "f1_context", "nocontext": "f1_nocontext"})
    if both.empty:
        return both.assign(delta=pd.NA, pct_change=pd.NA), 0.0, 0.0, 0
    both["delta"] = both["f1_context"] - both["f1_nocontext"]

    def pct(row):
        base = row["f1_nocontext"]
        if base and base != 0:
            return (row["delta"] / base) * 100.0
        return float("nan")
    both["pct_change"] = both.apply(pct, axis=1)
    avg_delta = float(both["delta"].mean())
    avg_pct = float(both["pct_change"].dropna().mean()) if both["pct_change"].notna().any() else 0.0
    n_models = int(len(both))
    both = both.sort_values(by="delta", ascending=False)
    return both[["model", "f1_context", "f1_nocontext", "delta", "pct_change"]], avg_delta, avg_pct, n_models


def print_report(df, subset):
    import pandas as pd
    table, avg_delta, avg_pct, n = compute_context_delta(df, subset)
    print(f"\n=== Context effect for subset='{subset}' ===")
    if n == 0:
        print("No models with both context and nocontext found.")
        return
    print(f"Models matched: {n}")
    print(f"Average delta (context - nocontext) in F1_macro: {avg_delta:.6f}")
    if pd.notna(avg_pct):
        print(f"Average percent change relative to no-context: {avg_pct:.2f}%")
    print("\nPer-model F1_macro (sorted by delta desc):")
    for _, row in table.iterrows():
        model = row["model"]
        f1c = row["f1_context"]
        f1n = row["f1_nocontext"]
        delta = row["delta"]
        pct = row["pct_change"]
        pct_s = f"{pct:.2f}%" if pd.notna(pct) else "NA"
        print(f"- {model}: context={f1c:.6f} | nocontext={f1n:.6f} | delta={delta:+.6f} ({pct_s})")


def module05_latex_tables():
    import pandas as pd
    metrics_csv = OUTPUT_DIR / "llm_models_metrics.csv"
    per_emotion_csv = OUTPUT_DIR / "per_emotion_metrics.csv"
    if not metrics_csv.exists():
        raise FileNotFoundError(f"Metrics CSV not found: {metrics_csv}. Run module 03 first.")
    if not per_emotion_csv.exists():
        raise FileNotFoundError(f"Per-emotion CSV not found: {per_emotion_csv}. Run module 04 first.")
    metrics = pd.read_csv(str(metrics_csv))
    pem = pd.read_csv(str(per_emotion_csv))
    out_dir = OUTPUT_DIR / "LLMs"
    os.makedirs(str(out_dir), exist_ok=True)

    row_lookup = {}
    for _, r in metrics.iterrows():
        row_lookup[(r["model"], r["context"], r["subset"])] = r

    display_names = dict(DISPLAY_NAMES)
    display_names["mixtral_8x7b"] = "Mixtral-8x (7B)"
    models = discover_models("results_no_ctxt")
    rows = []
    for name in models:
        fields = [display_names[name]]
        for subset in ("full", "test"):
            crow = row_lookup[(name, "context", subset)]
            nrow = row_lookup[(name, "nocontext", subset)]
            fields.append(f"{crow['coverage_inclusive'] * 100:.2f}")
            for block in (
                [crow["precision_macro"], crow["recall_macro"], crow["f1_macro"]],
                [crow["precision_weighted"], crow["recall_weighted"], crow["f1_weighted"]],
                [nrow["precision_macro"], nrow["recall_macro"], nrow["f1_macro"]],
                [nrow["precision_weighted"], nrow["recall_weighted"], nrow["f1_weighted"]],
            ):
                for value in block:
                    fields.append(f"{float(value):.2f}")
        rows.append(" & ".join(fields))
    write_tex_rows(str(out_dir / "llm_results_rows.tex"), rows, last_trailing_space=True)

    per_emotion_order = [
        ("nocontext", "full", "per_emotion_llm_noctx_full_rows.tex", "Mixtral 8x (7B)"),
        ("nocontext", "test", "per_emotion_llm_noctx_test_rows.tex", "Mixtral 8X (7B)"),
        ("context", "full", "per_emotion_llm_ctx_full_rows.tex", "Mixtral 8x (7B)"),
        ("context", "test", "per_emotion_llm_ctx_test_rows.tex", "Mixtral 8X (7B)"),
    ]
    for ctx, subset, fname, mixtral_display in per_emotion_order:
        name_to_display = {}
        for name in models:
            if name == "mixtral_8x7b":
                name_to_display[name] = mixtral_display
            else:
                name_to_display[name] = DISPLAY_NAMES[name]
        rows = []
        for display in sorted(name_to_display.values()):
            name = [k for k, v in name_to_display.items() if v == display][0]
            sub_df = pem[(pem["model"] == name) & (pem["context"] == ctx) & (pem["subset"] == subset)]
            emo_map = {}
            for _, r in sub_df.iterrows():
                emo_map[r["emotion"]] = r
            fields = [display]
            for emo in PER_EMOTION_COLUMN_ORDER:
                r = emo_map[emo]
                fields.append(f"{float(r['precision']):.2f}")
                fields.append(f"{float(r['recall']):.2f}")
                fields.append(f"{float(r['f1']):.2f}")
            rows.append(" & ".join(fields))
        write_tex_rows(str(out_dir / fname), rows)
    print("module 05 complete")


def write_tex_rows(path, rows, last_trailing_space=False):
    if not rows:
        raise ValueError("no rows to write")
    suffix = " " if last_trailing_space else ""
    content = "\n".join(r + " \\\\" for r in rows[:-1]) + "\n" + rows[-1] + suffix
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def write_manifest():
    import importlib
    manifest = {"python": platform.python_version(), "platform": platform.platform()}
    try:
        import pandas
        manifest["pandas"] = pandas.__version__
    except Exception:
        manifest["pandas"] = "not installed"
    try:
        from sklearn import __version__ as sklearn_version
        manifest["scikit-learn"] = sklearn_version
    except Exception:
        manifest["scikit-learn"] = "not installed"
    try:
        import numpy
        manifest["numpy"] = numpy.__version__
    except Exception:
        manifest["numpy"] = "not installed"
    for mod in ("ollama", "tqdm"):
        try:
            m = importlib.import_module(mod)
            manifest[mod] = getattr(m, "__version__", "installed")
        except Exception:
            manifest[mod] = "not installed"
    manifest["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(str(SCRIPT_DIR / "run_manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)


def main():
    global PRINT_MODEL
    parser = argparse.ArgumentParser(description="CHASE 2026 text-based LLM track reproduction (modules 01-05)")
    parser.add_argument("--module", nargs="+", type=str, choices=["01", "02", "03", "04", "05"],
                        help="modules to run (default: all)")
    parser.add_argument("--offline", action="store_true",
                        help="run only the offline, reproducible modules 03-05 (no Ollama)")
    parser.add_argument("--print-model", type=str, default=None,
                        help="module 04: print full per-emotion comparison for a model")
    args = parser.parse_args()

    PRINT_MODEL = args.print_model

    if args.offline:
        modules = ["03", "04", "05"]
    elif args.module:
        modules = args.module
    else:
        modules = ["01", "02", "03", "04", "05"]

    if "01" in modules:
        module01_inference_nocontext()
    if "02" in modules:
        module02_inference_context()
    if "03" in modules:
        module03_evaluation_metrics()
    if "04" in modules:
        module04_per_emotion()
        module04_context_effect()
    if "05" in modules:
        module05_latex_tables()

    write_manifest()
    print(f"run complete (modules: {', '.join(modules)})")


if __name__ == "__main__":
    main()