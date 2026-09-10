#!/usr/bin/env python3
"""Specification 03 — Evaluation & Metrics.

Scores every (model, configuration, subset) from the delivered prediction
bundles and writes:

    <out>/llm_models_metrics.csv                                   (64 rows)
    <out>/llm_models_metrics_ranking_{context,nocontext}_{full,test}.csv (16 each)
    <out>/llm_models_metrics_rankings_all.csv                      (64 rows + 3 cols)

Pure pandas / scikit-learn.  No randomness (Spec 00 §3) — no seed is set
because no stochastic operation exists.

Run from the repository root:  python claude/03_evaluation_metrics.py
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Dict, List, Optional, Tuple

import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repro_common import (  # noqa: E402
    GROUND_TRUTH_PATH,
    PREDICTION_SPECS,
    RESULTS_ROOT,
    SPLITS_PATH,
    SUBSET_WRITE_ORDER,
    collect_pairs,
    discover_models,
    ensure_dir,
    load_ground_truth,
    load_model_predictions,
    load_splits,
    resolve_output_root,
)

# Spec 03 §5 — column order, exactly.
METRIC_COLUMNS: List[str] = [
    'model_id', 'model', 'context', 'subset',
    'precision_weighted', 'recall_weighted', 'f1_weighted',
    'precision_macro', 'recall_macro', 'f1_macro',
    'accuracy', 'samples',
    'hallucination_rate', 'coverage',
    'hallucination_rate_inclusive', 'coverage_inclusive',
    'total_expected', 'total_seen', 'missing_predictions',
]

FLOAT_COLUMNS: List[str] = [
    'precision_weighted', 'recall_weighted', 'f1_weighted',
    'precision_macro', 'recall_macro', 'f1_macro',
    'accuracy',
    'hallucination_rate', 'coverage',
    'hallucination_rate_inclusive', 'coverage_inclusive',
]

# The committed CSV carries floats rounded to 6 decimals (verified: coverage
# 10/381 = 0.026246719... is committed as 0.026247).
FLOAT_ROUND = 6

# Spec 03 §6 — ranking blocks, in this exact order, with these exact titles.
RANKING_BLOCKS: List[Tuple[str, str, str]] = [
    ('with context and full data', 'context', 'full'),
    ('with context and test data', 'context', 'test'),
    ('without context and full data', 'nocontext', 'full'),
    ('without context and test data', 'nocontext', 'test'),
]


def coverage_counts(gt: Dict[str, Dict[str, str]],
                    preds: Dict[str, Dict[str, Optional[str]]],
                    subset: Optional[str],
                    split_map: Dict[Tuple[str, str], str]) -> Tuple[int, int, int, int]:
    """Spec 03 §4.2 — (total_expected, total_seen, hallucinations, samples).

    Iterates the ground truth exactly like ``collect_pairs`` so the counters and
    the (y_true, y_pred) pairs stay consistent.
    """
    total_expected = 0
    total_seen = 0
    hallucinations = 0
    samples = 0
    for output_name, segs_gt in gt.items():
        segs_pred = preds.get(output_name)
        for seg_id in segs_gt:
            if subset == 'test' and split_map.get((output_name, seg_id), None) != 'test':
                continue
            total_expected += 1
            if segs_pred is None or seg_id not in segs_pred:
                continue
            total_seen += 1
            if segs_pred.get(seg_id) is None:
                hallucinations += 1
            else:
                samples += 1
    return total_expected, total_seen, hallucinations, samples


def score(y_true: List[str], y_pred: List[str]) -> Dict[str, float]:
    """Spec 03 §4.3 — weighted / macro P-R-F1 + accuracy, zero_division=0."""
    if not y_true:
        return {
            'precision_weighted': 0.0, 'recall_weighted': 0.0, 'f1_weighted': 0.0,
            'precision_macro': 0.0, 'recall_macro': 0.0, 'f1_macro': 0.0,
            'accuracy': 0.0,
        }
    pw, rw, fw, _ = precision_recall_fscore_support(
        y_true, y_pred, average='weighted', zero_division=0
    )
    pm, rm, fm, _ = precision_recall_fscore_support(
        y_true, y_pred, average='macro', zero_division=0
    )
    return {
        'precision_weighted': float(pw), 'recall_weighted': float(rw),
        'f1_weighted': float(fw),
        'precision_macro': float(pm), 'recall_macro': float(rm),
        'f1_macro': float(fm),
        'accuracy': float(accuracy_score(y_true, y_pred)),
    }


def build_metrics(gt, split_map) -> pd.DataFrame:
    rows: List[Dict[str, object]] = []

    # Spec 03 §5 — row order: configurations, then sorted model dirs, then subsets.
    for subdir, ctx in PREDICTION_SPECS:
        ctx_dir = os.path.join(RESULTS_ROOT, subdir)
        for model_name, all_json in discover_models(ctx_dir):
            preds = load_model_predictions(all_json)

            for subset in SUBSET_WRITE_ORDER:
                subset_arg = None if subset == 'full' else 'test'

                y_true, y_pred = collect_pairs(gt, preds, subset_arg, split_map)
                total_expected, total_seen, hallucinations, samples = coverage_counts(
                    gt, preds, subset_arg, split_map
                )
                assert samples == len(y_true), (
                    f"counter/pair mismatch for {model_name}/{ctx}/{subset}"
                )

                metrics = score(y_true, y_pred)

                # Spec 03 §4.2 — coverage / hallucination formulas.
                missing_predictions = total_expected - total_seen
                # Spec 03 §4.2 states `hallucinations / total_seen` guarded only
                # by `total_seen == 0`.  The committed reference CSV also zeroes
                # this column when no usable sample survives: the row
                # `deepseek-r1_8b-nocontext-test` (total_seen=72, samples=0) is
                # committed as 0.0, not 1.0.  The committed artefact is the
                # definition of done (Spec 00 §1), so the `samples` guard is
                # reproduced here; every other row is unaffected.
                hallucination_rate = (
                    hallucinations / total_seen if (total_seen and samples) else 0.0
                )
                coverage = samples / total_seen if total_seen else 0.0
                hallucination_rate_inclusive = (
                    (missing_predictions + hallucinations) / total_expected
                    if total_expected else 0.0
                )
                coverage_inclusive = (
                    samples / total_expected if total_expected else 0.0
                )

                row: Dict[str, object] = {
                    'model_id': f"{model_name}-{ctx}-{subset}",
                    'model': model_name,
                    'context': ctx,
                    'subset': subset,
                    'samples': samples,
                    'hallucination_rate': hallucination_rate,
                    'coverage': coverage,
                    'hallucination_rate_inclusive': hallucination_rate_inclusive,
                    'coverage_inclusive': coverage_inclusive,
                    'total_expected': total_expected,
                    'total_seen': total_seen,
                    'missing_predictions': missing_predictions,
                }
                row.update(metrics)
                rows.append(row)

    df = pd.DataFrame(rows, columns=METRIC_COLUMNS)
    for col in FLOAT_COLUMNS:
        df[col] = df[col].astype(float).round(FLOAT_ROUND)
    for col in ('samples', 'total_expected', 'total_seen', 'missing_predictions'):
        df[col] = df[col].astype(int)
    return df


def build_rankings(df: pd.DataFrame) -> Tuple[Dict[str, pd.DataFrame], pd.DataFrame]:
    """Spec 03 §6 — per-(context, subset) rankings by f1_macro descending."""
    per_file: Dict[str, pd.DataFrame] = {}
    blocks: List[pd.DataFrame] = []

    for title, ctx, subset in RANKING_BLOCKS:
        block = df[(df['context'] == ctx) & (df['subset'] == subset)]
        # kind='stable' keeps the source (sorted-model-dir) order for f1 ties,
        # which is what the committed ranking CSVs show.
        block = block.sort_values('f1_macro', ascending=False, kind='stable')
        per_file[f"llm_models_metrics_ranking_{ctx}_{subset}.csv"] = block

        annotated = block.copy()
        annotated['ranking_title'] = title
        annotated['ranking_context'] = ctx
        annotated['ranking_subset'] = subset
        blocks.append(annotated)

    rankings_all = pd.concat(blocks, ignore_index=True)
    return per_file, rankings_all


def validate(out_root: str) -> int:
    """Compare every generated CSV with the committed reference under results/."""
    names = ['llm_models_metrics.csv', 'llm_models_metrics_rankings_all.csv'] + [
        f"llm_models_metrics_ranking_{ctx}_{subset}.csv"
        for _, ctx, subset in RANKING_BLOCKS
    ]
    failures = 0
    for name in names:
        generated = os.path.join(out_root, name)
        reference = os.path.join(RESULTS_ROOT, name)
        if os.path.abspath(generated) == os.path.abspath(reference):
            print(f"[validate] {name}: SKIP (writing in place)")
            continue
        if not os.path.exists(reference):
            print(f"[validate] {name}: no committed reference — skipped")
            continue
        with open(generated, 'r', encoding='utf-8') as f:
            got = f.read()
        with open(reference, 'r', encoding='utf-8') as f:
            want = f.read()
        if got == want:
            print(f"[validate] {name}: OK (byte-identical to committed reference)")
        else:
            failures += 1
            print(f"[validate] {name}: MISMATCH vs committed reference")
            got_lines, want_lines = got.splitlines(), want.splitlines()
            print(f"           rows: generated={len(got_lines)} reference={len(want_lines)}")
            shown = 0
            for i, (a, b) in enumerate(zip(got_lines, want_lines)):
                if a != b and shown < 5:
                    print(f"           line {i + 1}:\n             got : {a}\n             want: {b}")
                    shown += 1
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--output-root', default=None,
        help="Directory mirroring results/ for generated CSVs "
             "(default: claude/results).",
    )
    parser.add_argument(
        '--no-validate', action='store_true',
        help="Skip the comparison against the committed reference CSVs.",
    )
    args = parser.parse_args()

    out_root = ensure_dir(resolve_output_root(args.output_root))

    for path in (GROUND_TRUTH_PATH, SPLITS_PATH):
        if not os.path.exists(path):
            raise FileNotFoundError(path)

    gt = load_ground_truth(GROUND_TRUTH_PATH)
    split_map = load_splits(SPLITS_PATH)

    df = build_metrics(gt, split_map)

    metrics_csv = os.path.join(out_root, 'llm_models_metrics.csv')
    df.to_csv(metrics_csv, index=False, encoding='utf-8')
    print(f"Saved: {metrics_csv} ({len(df)} rows)")

    per_file, rankings_all = build_rankings(df)
    for name, block in per_file.items():
        path = os.path.join(out_root, name)
        block.to_csv(path, index=False, encoding='utf-8')
        print(f"Saved: {path} ({len(block)} rows)")

    all_path = os.path.join(out_root, 'llm_models_metrics_rankings_all.csv')
    rankings_all.to_csv(all_path, index=False, encoding='utf-8')
    print(f"Saved: {all_path} ({len(rankings_all)} rows)")

    if args.no_validate:
        return 0
    return 1 if validate(out_root) else 0


if __name__ == '__main__':
    raise SystemExit(main())
