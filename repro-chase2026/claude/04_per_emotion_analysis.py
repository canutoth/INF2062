#!/usr/bin/env python3
"""Specification 04 — Per-Emotion Analysis & Context-Effect Report.

Reproduces the two authoritative delivered scripts:

  * ``tools/compare_per_emotion.py``   -> per_emotion_metrics.csv,
                                          per_emotion_metrics_comparison.csv,
                                          per_emotion_metrics_wide.csv (+ §1.6 stdout)
  * ``tools/compare_context_effect.py`` -> printed context-effect report (§2)

The delivered scripts write into ``results/``; this reproduction is sandboxed to
``claude/`` and therefore mirrors the same file names under ``--output-root``
(default ``claude/results``).  The computation is reproduced **as written**,
including the buggy column-flatten in ``per_emotion_metrics_wide.csv``
(Spec 04 §1.5 — do not "fix" it or the output stops matching).

No randomness (Spec 00 §3).

Run from the repository root:  python claude/04_per_emotion_analysis.py
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import List

import pandas as pd
from sklearn.metrics import precision_recall_fscore_support

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from repro_common import (  # noqa: E402
    GROUND_TRUTH_PATH,
    LABELS_ORDER,
    PREDICTION_SPECS,
    RESULTS_ROOT,
    SPLITS_PATH,
    collect_pairs,
    discover_models,
    ensure_dir,
    load_ground_truth,
    load_model_predictions,
    load_splits,
    resolve_output_root,
)


def per_emotion_metrics(y_true: List[str], y_pred: List[str]) -> pd.DataFrame:
    """Verbatim from tools/compare_per_emotion.py (Spec 04 §1.2)."""
    if not y_true:
        # empty frame with standard columns
        return pd.DataFrame({
            'emotion': LABELS_ORDER,
            'precision': [0.0] * len(LABELS_ORDER),
            'recall': [0.0] * len(LABELS_ORDER),
            'f1': [0.0] * len(LABELS_ORDER),
            'support': [0] * len(LABELS_ORDER),
        })
    labels = LABELS_ORDER
    p, r, f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, average=None, zero_division=0
    )
    return pd.DataFrame({
        'emotion': labels,
        'precision': p,
        'recall': r,
        'f1': f1,
        'support': support,
    })


def build_base(gt, split_map) -> pd.DataFrame:
    """Spec 04 §1.2/§1.3 — one row per (model, context, subset, emotion)."""
    rows = []
    for subdir, ctx in PREDICTION_SPECS:
        ctx_dir = os.path.join(RESULTS_ROOT, subdir)
        for name, all_json in discover_models(ctx_dir):
            preds = load_model_predictions(all_json)
            for subset in ('full', 'test'):
                subset_arg = None if subset == 'full' else 'test'
                y_true, y_pred = collect_pairs(gt, preds, subset_arg, split_map)
                df_em = per_emotion_metrics(y_true, y_pred)
                for _, r in df_em.iterrows():
                    rows.append({
                        'model': name,
                        'context': ctx,
                        'subset': subset,
                        'emotion': r['emotion'],
                        'precision': float(r['precision']),
                        'recall': float(r['recall']),
                        'f1': float(r['f1']),
                        'support': int(r['support']),
                    })
    return pd.DataFrame(rows)


def build_comparison(df_base: pd.DataFrame) -> pd.DataFrame:
    """Spec 04 §1.4 — inner-join context vs nocontext, deltas and % changes."""
    piv_cols = ['model', 'subset', 'emotion']
    ctx_df = df_base[df_base['context'] == 'context'][
        piv_cols + ['precision', 'recall', 'f1']
    ].copy()
    nctx_df = df_base[df_base['context'] == 'nocontext'][
        piv_cols + ['precision', 'recall', 'f1']
    ].copy()

    ctx_df = ctx_df.rename(columns={
        'precision': 'precision_context',
        'recall': 'recall_context',
        'f1': 'f1_context',
    })
    nctx_df = nctx_df.rename(columns={
        'precision': 'precision_nocontext',
        'recall': 'recall_nocontext',
        'f1': 'f1_nocontext',
    })

    cmp_df = pd.merge(ctx_df, nctx_df, on=piv_cols, how='inner')
    if not cmp_df.empty:
        cmp_df['precision_delta'] = cmp_df['precision_context'] - cmp_df['precision_nocontext']
        cmp_df['recall_delta'] = cmp_df['recall_context'] - cmp_df['recall_nocontext']
        cmp_df['f1_delta'] = cmp_df['f1_context'] - cmp_df['f1_nocontext']

        # Optional percent changes (relative to no-context)
        def pct(a, b):
            if b and b != 0:
                return (a - b) / b * 100.0
            return float('nan')

        cmp_df['f1_pct_change'] = cmp_df.apply(
            lambda r: pct(r['f1_context'], r['f1_nocontext']), axis=1)
        cmp_df['precision_pct_change'] = cmp_df.apply(
            lambda r: pct(r['precision_context'], r['precision_nocontext']), axis=1)
        cmp_df['recall_pct_change'] = cmp_df.apply(
            lambda r: pct(r['recall_context'], r['recall_nocontext']), axis=1)
    return cmp_df


def build_wide(cmp_df: pd.DataFrame) -> pd.DataFrame:
    """Spec 04 §1.5 — reproduced verbatim, buggy flatten included.

    The flatten re-appends 'context'/'nocontext' based on whether the *metric*
    name contains the substring 'context' — which is always true — so every
    column is suffixed '_context' and the "friendly reorder" list below never
    matches.  The columns therefore land in raw unstacked order.  Do not fix.
    """
    wide = cmp_df.copy()
    # Build a MultiIndex for columns: metric_context/nocontext by subset
    wide = wide.set_index(['model', 'emotion', 'subset'])
    keep_cols = [
        'precision_context', 'precision_nocontext',
        'recall_context', 'recall_nocontext',
        'f1_context', 'f1_nocontext',
    ]
    wide = wide[keep_cols]
    # Move subset to columns
    wide = wide.unstack('subset')
    # Flatten columns like ('precision_context','full') -> precision_full_context
    wide.columns = [
        f"{metric}_{subset}_{'context' if 'context' in metric else 'nocontext'}"
        for metric, subset in wide.columns
    ]
    # Reorder columns in a friendly order
    desired = []
    for m in ('precision', 'recall', 'f1'):
        for subset in ('full', 'test'):
            for ctx in ('context', 'nocontext'):
                desired.append(f"{m}_{subset}_{ctx}")
    # Some combinations may be missing if data absent; keep those that exist
    cols = [c for c in desired if c in wide.columns]
    other_cols = [c for c in wide.columns if c not in cols]
    wide = wide[cols + other_cols]
    return wide.reset_index()


def print_top_improvements(cmp_df: pd.DataFrame) -> None:
    """Spec 04 §1.6 — top-5 models by f1_delta, per subset and emotion."""
    for subset in ('full', 'test'):
        print(f"\n=== Top F1 improvements per emotion (subset={subset}) ===")
        sub = cmp_df[cmp_df['subset'] == subset]
        if sub.empty:
            print("No data")
            continue
        for emo in LABELS_ORDER:
            emo_df = sub[sub['emotion'] == emo]
            if emo_df.empty:
                continue
            top = emo_df.sort_values(by='f1_delta', ascending=False).head(5)
            if top.empty:
                continue
            print(f"\nEmotion: {emo}")
            for _, row in top.iterrows():
                print(
                    f"- {row['model']}: f1_ctx={row['f1_context']:.2f} | "
                    f"f1_nctx={row['f1_nocontext']:.2f} | "
                    f"delta={row['f1_delta']:+.2f} ({row['f1_pct_change']:.2f}%)"
                )


def print_model_detail(cmp_df: pd.DataFrame, model_name: str) -> None:
    """Spec 04 §1.6 — optional --print-model dump."""
    print(f"\n=== Per-emotion metrics for model: {model_name} ===")
    mdf = cmp_df[cmp_df['model'] == model_name]
    if mdf.empty:
        print("No data for this model (ensure it exists in both context and nocontext).")
        return
    for subset in ('full', 'test'):
        ms = mdf[mdf['subset'] == subset]
        if ms.empty:
            continue
        print(f"\nSubset: {subset}")
        ms = ms.copy()
        ms['emotion'] = pd.Categorical(ms['emotion'], categories=LABELS_ORDER, ordered=True)
        ms = ms.sort_values('emotion')
        for _, row in ms.iterrows():
            print(
                f"{row['emotion']}: "
                f"P/R/F1 ctx={row['precision_context']:.2f}/{row['recall_context']:.2f}/{row['f1_context']:.2f} | "
                f"nctx={row['precision_nocontext']:.2f}/{row['recall_nocontext']:.2f}/{row['f1_nocontext']:.2f} | "
                f"ΔF1={row['f1_delta']:+.2f} ({row['f1_pct_change']:.2f}%)"
            )


# --------------------------------------------------------------------------
# Spec 04 §2 — tools/compare_context_effect.py
# --------------------------------------------------------------------------
def compute_context_delta(df: pd.DataFrame, subset: str):
    sub = subset.strip().lower()
    sub_df = df[df['subset'] == sub].copy()

    pivot = sub_df.pivot_table(
        index='model', columns='context', values='f1_macro', aggfunc='max'
    )
    for col in ['context', 'nocontext']:
        if col not in pivot.columns:
            pivot[col] = float('nan')
    both = pivot.dropna(subset=['context', 'nocontext']).reset_index()
    both = both.rename(columns={'context': 'f1_context', 'nocontext': 'f1_nocontext'})

    if both.empty:
        return both.assign(delta=pd.NA, pct_change=pd.NA), 0.0, 0.0, 0

    both['delta'] = both['f1_context'] - both['f1_nocontext']

    def pct(row):
        base = row['f1_nocontext']
        if base and base != 0:
            return (row['delta'] / base) * 100.0
        return float('nan')

    both['pct_change'] = both.apply(pct, axis=1)

    avg_delta = float(both['delta'].mean())
    avg_pct = float(both['pct_change'].dropna().mean()) if both['pct_change'].notna().any() else 0.0
    n_models = int(len(both))

    both = both.sort_values(by='delta', ascending=False)
    return both[['model', 'f1_context', 'f1_nocontext', 'delta', 'pct_change']], avg_delta, avg_pct, n_models


def print_context_effect(metrics_csv: str) -> pd.DataFrame:
    if not os.path.exists(metrics_csv):
        raise FileNotFoundError(
            f"Metrics CSV not found: {metrics_csv}. Run module 03 first."
        )
    df = pd.read_csv(metrics_csv)
    required = {'model', 'context', 'subset', 'f1_macro'}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns in CSV: {missing}")
    df['subset'] = df['subset'].astype(str).str.lower()
    df['context'] = df['context'].astype(str).str.lower()
    df['model'] = df['model'].astype(str)
    df['f1_macro'] = pd.to_numeric(df['f1_macro'], errors='coerce')

    for subset in ('full', 'test'):
        if subset not in df['subset'].unique():
            continue
        table, avg_delta, avg_pct, n = compute_context_delta(df, subset)
        print(f"\n=== Context effect for subset='{subset}' ===")
        if n == 0:
            print("No models with both context and nocontext found.")
            continue
        print(f"Models matched: {n}")
        print(f"Average delta (context - nocontext) in F1_macro: {avg_delta:.6f}")
        if pd.notna(avg_pct):
            print(f"Average percent change relative to no-context: {avg_pct:.2f}%")
        print("\nPer-model F1_macro (sorted by delta desc):")
        for _, row in table.iterrows():
            pct_s = f"{row['pct_change']:.2f}%" if pd.notna(row['pct_change']) else "NA"
            print(
                f"- {row['model']}: context={row['f1_context']:.6f} | "
                f"nocontext={row['f1_nocontext']:.6f} | "
                f"delta={row['delta']:+.6f} ({pct_s})"
            )
    return df


# --------------------------------------------------------------------------
# Spec 04 §4 — validation
# --------------------------------------------------------------------------
def validate(df_base: pd.DataFrame, metrics_csv: str) -> int:
    """Support sums must equal `samples` in llm_models_metrics.csv (Spec 04 §4)."""
    failures = 0
    if not os.path.exists(metrics_csv):
        print("[validate] llm_models_metrics.csv absent — support cross-check skipped")
        return 0
    metrics = pd.read_csv(metrics_csv)
    support = (
        df_base.groupby(['model', 'context', 'subset'], sort=False)['support']
        .sum()
        .rename('support_sum')
        .reset_index()
    )
    merged = metrics.merge(support, on=['model', 'context', 'subset'], how='left')
    bad = merged[merged['samples'] != merged['support_sum']]
    if len(bad):
        failures += 1
        print(f"[validate] support-sum vs samples: MISMATCH on {len(bad)} rows")
        for _, row in bad.head(5).iterrows():
            print(f"           {row['model_id']}: samples={row['samples']} "
                  f"support_sum={row['support_sum']}")
    else:
        print(f"[validate] support-sum == samples for all {len(merged)} "
              f"(model, context, subset) rows: OK")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-root', default=None,
                        help="Directory mirroring results/ (default: claude/results).")
    parser.add_argument('--print-model', default=None,
                        help="Dump one model's full per-emotion comparison.")
    parser.add_argument('--no-validate', action='store_true')
    args = parser.parse_args()

    out_dir = ensure_dir(resolve_output_root(args.output_root))

    if not os.path.exists(GROUND_TRUTH_PATH):
        raise FileNotFoundError(f"Ground truth not found at {GROUND_TRUTH_PATH}")
    if not os.path.exists(SPLITS_PATH):
        raise FileNotFoundError(f"Splits CSV not found at {SPLITS_PATH}")

    gt = load_ground_truth(GROUND_TRUTH_PATH)
    split_map = load_splits(SPLITS_PATH)

    df_base = build_base(gt, split_map)
    if df_base.empty:
        print('No per-emotion results found.')
        return 1

    base_csv = os.path.join(out_dir, 'per_emotion_metrics.csv')
    df_base.to_csv(base_csv, index=False, encoding='utf-8')
    print(f"Saved: {base_csv}")

    cmp_df = build_comparison(df_base)
    cmp_csv = os.path.join(out_dir, 'per_emotion_metrics_comparison.csv')
    cmp_df.to_csv(cmp_csv, index=False, encoding='utf-8')
    print(f"Saved: {cmp_csv}")

    if not cmp_df.empty:
        wide = build_wide(cmp_df)
        wide_csv = os.path.join(out_dir, 'per_emotion_metrics_wide.csv')
        wide.to_csv(wide_csv, index=False, encoding='utf-8')
        print(f"Saved: {wide_csv}")

    print_top_improvements(cmp_df)

    if args.print_model:
        print_model_detail(cmp_df, args.print_model)

    # Spec 04 §2 — context-effect report over module 03's metrics table.
    metrics_csv = os.path.join(out_dir, 'llm_models_metrics.csv')
    print_context_effect(metrics_csv)

    if args.no_validate:
        return 0
    print()
    return 1 if validate(df_base, metrics_csv) else 0


if __name__ == '__main__':
    raise SystemExit(main())
