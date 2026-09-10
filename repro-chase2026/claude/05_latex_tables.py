#!/usr/bin/env python3
"""Specification 05 — LaTeX Table Rows.

Writes the five ``*_rows.tex`` files that the delivered wrappers
``results/LLMs/llms.tex`` and ``results/LLMs/llm-per-emotion.tex`` ``\\input{}``:

    <out>/LLMs/llm_results_rows.tex
    <out>/LLMs/per_emotion_llm_{noctx,ctx}_{full,test}_rows.tex

Inputs: ``llm_models_metrics.csv`` (module 03) and ``per_emotion_metrics.csv``
(module 04) from the same output root, plus the Spec 00 §7 display-name map.

Deterministic string formatting; no randomness (Spec 00 §3).  The wrappers are
delivered and are **not** modified — they own \\begin{tabular}, the header, the
Average row, and the final ``\\\\`` after each \\input, so every row here except
the last ends with " \\\\" and the file carries no trailing newline.

Run from the repository root:  python claude/05_latex_tables.py
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Dict, List

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repro_common import (  # noqa: E402
    LATEX_EMOTION_ORDER,
    RESULTS_ROOT,
    display_name,
    ensure_dir,
    resolve_output_root,
)

# Spec 05 §1 — every numeric field is formatted with two decimals.
FMT = "{:.2f}"

# Spec 05 §1 — rows joined with " \\" + newline; the wrapper supplies the last one.
ROW_SEP = " \\\\\n"

# Spec 05 §3 — file -> (context, subset).
PER_EMOTION_FILES: List[tuple] = [
    ("per_emotion_llm_noctx_full_rows.tex", "nocontext", "full"),
    ("per_emotion_llm_noctx_test_rows.tex", "nocontext", "test"),
    ("per_emotion_llm_ctx_full_rows.tex", "context", "full"),
    ("per_emotion_llm_ctx_test_rows.tex", "context", "test"),
]

# Spec 05 §2 — block layout: coverage %, then macro P/R/F1 and weighted P/R/F1
# for the context configuration, then the same pair for no-context.
MACRO_COLS = ["precision_macro", "recall_macro", "f1_macro"]
WEIGHTED_COLS = ["precision_weighted", "recall_weighted", "f1_weighted"]


def num(value) -> str:
    return FMT.format(float(value))


def _metric_row(metrics: pd.DataFrame, model: str, ctx: str, subset: str) -> pd.Series:
    sel = metrics[
        (metrics["model"] == model)
        & (metrics["context"] == ctx)
        & (metrics["subset"] == subset)
    ]
    if len(sel) != 1:
        raise ValueError(
            f"expected exactly 1 metrics row for ({model}, {ctx}, {subset}), got {len(sel)}"
        )
    return sel.iloc[0]


def build_results_rows(metrics: pd.DataFrame) -> str:
    """Spec 05 §2 — llm_results_rows.tex, ordered by model directory name."""
    models = sorted(metrics["model"].unique())
    rows: List[str] = []
    for model in models:
        fields: List[str] = [display_name(model)]
        for subset in ("full", "test"):
            ctx_row = _metric_row(metrics, model, "context", subset)
            noctx_row = _metric_row(metrics, model, "nocontext", subset)
            # 1 — coverage %, taken from the *context* row (Spec 05 §2).
            fields.append(num(ctx_row["coverage_inclusive"] * 100))
            # 2-4 / 5-7 — context macro then weighted.
            fields.extend(num(ctx_row[c]) for c in MACRO_COLS)
            fields.extend(num(ctx_row[c]) for c in WEIGHTED_COLS)
            # 8-10 / 11-13 — no-context macro then weighted.
            fields.extend(num(noctx_row[c]) for c in MACRO_COLS)
            fields.extend(num(noctx_row[c]) for c in WEIGHTED_COLS)
        rows.append(" & ".join(fields))
    # The committed results/LLMs/llm_results_rows.tex ends its final row with a
    # single trailing space (an artefact of the original generator, which
    # suffixed every row with " " and joined on "\\\\\n").  The per-emotion row
    # files do not carry it.  Reproduced so the diff in §4 is byte-exact.
    return ROW_SEP.join(rows) + " "


def build_per_emotion_rows(per_emotion: pd.DataFrame, ctx: str, subset: str) -> str:
    """Spec 05 §3 — 16 rows ordered by display name, 21 numeric fields each."""
    sub = per_emotion[
        (per_emotion["context"] == ctx) & (per_emotion["subset"] == subset)
    ]
    models = sorted(sub["model"].unique())
    # Ordered by the *display name* string (differs from the directory order).
    models = sorted(models, key=lambda m: display_name(m, subset))

    rows: List[str] = []
    for model in models:
        model_rows = sub[sub["model"] == model]
        by_emotion: Dict[str, pd.Series] = {
            r["emotion"]: r for _, r in model_rows.iterrows()
        }
        fields: List[str] = [display_name(model, subset)]
        # Wrapper column order (Spec 00 §4.2), not LABELS_ORDER.
        for emotion in LATEX_EMOTION_ORDER:
            r = by_emotion[emotion]
            fields.extend((num(r["precision"]), num(r["recall"]), num(r["f1"])))
        rows.append(" & ".join(fields))
    return ROW_SEP.join(rows)


def validate(out_dir: str, names: List[str]) -> int:
    """Spec 05 §4 — diff against the committed results/LLMs/*_rows.tex."""
    ref_dir = os.path.join(RESULTS_ROOT, "LLMs")
    failures = 0
    for name in names:
        generated = os.path.join(out_dir, name)
        reference = os.path.join(ref_dir, name)
        if os.path.abspath(generated) == os.path.abspath(reference):
            print(f"[validate] {name}: SKIP (writing in place)")
            continue
        if not os.path.exists(reference):
            print(f"[validate] {name}: no committed reference — skipped")
            continue
        with open(generated, "r", encoding="utf-8") as f:
            got = f.read()
        with open(reference, "r", encoding="utf-8") as f:
            want = f.read()
        # Spec 05 §4 — "byte-for-byte (modulo a possible trailing newline)".
        if got.rstrip("\n") == want.rstrip("\n"):
            exact = " (byte-identical)" if got == want else " (modulo trailing newline)"
            print(f"[validate] {name}: OK{exact}")
        else:
            failures += 1
            print(f"[validate] {name}: MISMATCH vs committed reference")
            got_lines, want_lines = got.splitlines(), want.splitlines()
            print(f"           rows: generated={len(got_lines)} reference={len(want_lines)}")
            shown = 0
            for i, (a, b) in enumerate(zip(got_lines, want_lines)):
                if a != b and shown < 3:
                    print(f"           line {i + 1}:\n             got : {a}\n             want: {b}")
                    shown += 1
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-root", default=None,
                        help="Directory mirroring results/ (default: claude/results).")
    parser.add_argument("--no-validate", action="store_true")
    args = parser.parse_args()

    root = resolve_output_root(args.output_root)
    out_dir = ensure_dir(os.path.join(root, "LLMs"))

    metrics_csv = os.path.join(root, "llm_models_metrics.csv")
    per_emotion_csv = os.path.join(root, "per_emotion_metrics.csv")
    for path, module in ((metrics_csv, "03"), (per_emotion_csv, "04")):
        if not os.path.exists(path):
            raise FileNotFoundError(f"{path} not found — run module {module} first.")

    metrics = pd.read_csv(metrics_csv)
    per_emotion = pd.read_csv(per_emotion_csv)

    written: List[str] = []

    path = os.path.join(out_dir, "llm_results_rows.tex")
    with open(path, "w", encoding="utf-8") as f:
        f.write(build_results_rows(metrics))
    written.append("llm_results_rows.tex")
    print(f"Saved: {path}")

    for name, ctx, subset in PER_EMOTION_FILES:
        path = os.path.join(out_dir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(build_per_emotion_rows(per_emotion, ctx, subset))
        written.append(name)
        print(f"Saved: {path}")

    if args.no_validate:
        return 0
    return 1 if validate(out_dir, written) else 0


if __name__ == "__main__":
    raise SystemExit(main())
