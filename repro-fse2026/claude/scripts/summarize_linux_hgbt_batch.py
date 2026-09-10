#!/usr/bin/env python3
"""Summarize the Linux all-feature HGBT batch across releases."""

from __future__ import annotations

import argparse
import csv
import math
import os
from pathlib import Path
import sys
import tempfile
from typing import Any

import numpy as np


_cache_root = Path(tempfile.gettempdir()) / "cost_sampling_cache"
(_cache_root / "matplotlib").mkdir(parents=True, exist_ok=True)
(_cache_root / "fontconfig").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_cache_root / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(_cache_root / "fontconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cost_sampling.analysis import write_csv
from cost_sampling.hypotheses import aggregate_verdicts, evaluate_per_context_hypotheses


RELEASES = ("413", "415", "420", "500", "504", "507", "508")
RELEASE_LABELS = {
    "413": "v4.13",
    "415": "v4.15",
    "420": "v4.20",
    "500": "v5.0",
    "504": "v5.04",
    "507": "v5.07",
    "508": "v5.08",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        default="artifacts/strong_learner_overnight/linux/sk-hgbt-log-allfeatures",
        help="Directory containing linux<release>_vmlinux subdirectories.",
    )
    parser.add_argument("--output-dir", default=None, help="Defaults to --input-dir.")
    return parser.parse_args()


def _read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _float(row: dict[str, Any], key: str, default: float = float("nan")) -> float:
    try:
        return float(row.get(key, default))
    except (TypeError, ValueError):
        return default


def _int(row: dict[str, Any], key: str, default: int = 0) -> int:
    try:
        return int(float(row.get(key, default)))
    except (TypeError, ValueError):
        return default


def _fmt(value: Any, digits: int = 4) -> str:
    try:
        x = float(value)
    except (TypeError, ValueError):
        return str(value)
    if not math.isfinite(x):
        return "--"
    return f"{x:.{digits}g}"


def _coerce_records(rows: list[dict[str, Any]], release: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["release"] = release
        item["run"] = _int(item, "run")
        item["n"] = _int(item, "n")
        for key in ("pct_n", "train_cost", "pct_cost", "calibration_ratio", "mre"):
            item[key] = _float(item, key)
        out.append(item)
    return out


def _coerce_heterogeneity(rows: list[dict[str, Any]], release: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["release"] = release
        item["n_configurations"] = _int(item, "n_configurations")
        for key in ("full_cost", "min_cost", "median_cost", "mean_cost", "max_cost", "std_cost", "cv_cost", "p90_over_p10"):
            item[key] = _float(item, key)
        out.append(item)
    return out


def _coerce_numeric_rows(rows: list[dict[str, Any]], release: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["release"] = release
        for key, value in list(item.items()):
            if key in {"target_context", "cost_context", "context", "strategy", "level", "learner", "zip_member", "release"}:
                continue
            try:
                if value == "":
                    continue
                item[key] = float(value)
                if float(item[key]).is_integer() and key in {"run", "runs", "n", "pareto_count", "pareto_empirical", "top1_agreement"}:
                    item[key] = int(item[key])
            except (TypeError, ValueError):
                pass
        out.append(item)
    return out


def _pairs(rows: list[dict[str, Any]], column: str) -> set[str]:
    return {f"{row['strategy']}_{row['level']}" for row in rows if int(row.get(column, 0))}


def _release_summary(
    *,
    release: str,
    folder: Path,
    heterogeneity: list[dict[str, Any]],
    strategy_rows: list[dict[str, Any]],
    proxy_rows: list[dict[str, Any]],
    rank_rows: list[dict[str, Any]],
    pareto_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    h = heterogeneity[0]
    proxy_all = next((row for row in proxy_rows if row.get("strategy") == "ALL"), {})
    deployable = [row for row in strategy_rows if row.get("strategy") not in {"cheapOracle", "expensiveOracle"}]
    best_mre = min(deployable, key=lambda row: _float(row, "median_mre"))
    best_joint = min(deployable, key=lambda row: _float(row, "median_mre") + _float(row, "median_pct_cost"))
    count_pairs = _pairs(pareto_rows, "pareto_count")
    empirical_pairs = _pairs(pareto_rows, "pareto_empirical")
    union = count_pairs | empirical_pairs
    feature_count = max(0, len(_read_csv(folder / "linux_feature_columns.csv")))
    return {
        "release": release,
        "release_label": RELEASE_LABELS.get(release, release),
        "folder": str(folder),
        "feature_count": feature_count,
        "n_configurations": _int(h, "n_configurations"),
        "cost_cv": _float(h, "cv_cost"),
        "cost_p90_over_p10": _float(h, "p90_over_p10"),
        "proxy_spearman": _float(proxy_all, "spearman_n_train_cost"),
        "proxy_median_ratio": _float(proxy_all, "median_calibration_ratio"),
        "rank_top1_agreement": sum(_int(row, "top1_agreement") for row in rank_rows) / len(rank_rows),
        "rank_top1_flips": sum(1 for row in rank_rows if not _int(row, "top1_agreement")),
        "rank_mean_kendall_tau": sum(_float(row, "kendall_tau") for row in rank_rows) / len(rank_rows),
        "pareto_count_n": len(count_pairs),
        "pareto_empirical_n": len(empirical_pairs),
        "pareto_overlap_n": len(count_pairs & empirical_pairs),
        "pareto_jaccard": len(count_pairs & empirical_pairs) / len(union) if union else 1.0,
        "best_mre_pair": f"{best_mre['strategy']}_{best_mre['level']}",
        "best_mre": _float(best_mre, "median_mre"),
        "best_mre_pct_cost": _float(best_mre, "median_pct_cost"),
        "best_joint_pair": f"{best_joint['strategy']}_{best_joint['level']}",
        "best_joint_mre": _float(best_joint, "median_mre"),
        "best_joint_pct_cost": _float(best_joint, "median_pct_cost"),
    }


def _plot_release_metrics(rows: list[dict[str, Any]], output: Path) -> None:
    labels = [row["release_label"] for row in rows]
    x = np.arange(len(rows))
    fig, axes = plt.subplots(2, 2, figsize=(11.5, 7.6))
    specs = [
        ("cost_cv", "Cost CV", "#4C78A8"),
        ("proxy_median_ratio", "Median %cost / %n", "#F58518"),
        ("best_mre", "Best deployable MRE", "#54A24B"),
        ("pareto_jaccard", "Pareto Jaccard", "#E45756"),
    ]
    for ax, (key, ylabel, color) in zip(axes.flat, specs):
        ax.bar(x, [_float(row, key) for row in rows], color=color)
        ax.set_xticks(x)
        ax.set_xticklabels(labels, rotation=30, ha="right")
        ax.set_ylabel(ylabel)
        ax.grid(axis="y", color="#dddddd", linewidth=0.8)
        ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def _plot_strategy_mre(strategy_rows: list[dict[str, Any]], output: Path) -> None:
    deployable = [row for row in strategy_rows if row.get("strategy") not in {"cheapOracle", "expensiveOracle"}]
    strategies = sorted({str(row["strategy"]) for row in deployable})
    releases = [RELEASE_LABELS[r] for r in RELEASES]
    fig, ax = plt.subplots(figsize=(10.5, 5.3))
    for strategy in strategies:
        values = []
        for release in RELEASES:
            rows = [row for row in deployable if row["release"] == release and row["strategy"] == strategy]
            values.append(float(np.median([_float(row, "median_mre") for row in rows])) if rows else float("nan"))
        ax.plot(releases, values, marker="o", linewidth=1.8, label=strategy)
    ax.set_ylabel("Median MRE across budgets")
    ax.set_xlabel("Linux release")
    ax.grid(axis="y", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncol=2)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def _write_report(path: Path, rows: list[dict[str, Any]], hypothesis_summary: list[dict[str, Any]]) -> None:
    best = min(rows, key=lambda row: _float(row, "best_mre"))
    worst_pareto = min(rows, key=lambda row: _float(row, "pareto_jaccard"))
    by_h = {row["hypothesis"]: row for row in hypothesis_summary}
    lines = [
        "# Linux HGBT all-feature cross-release report",
        "",
        "## Scope",
        "",
        "This report summarizes the strong-learner Linux batch: `sk-hgbt-log`, all post-pruning feature columns, and approximately 1k/5k/10k generated training budgets across seven Linux releases.",
        "",
        "The older Linux report remains the reproducibility-oriented baseline. This report is the strong-default learner view for the learner-sensitivity question.",
        "",
        "## Main Findings",
        "",
        f"- Best observed deployable MRE is `{_fmt(best['best_mre'])}` on `{best['release_label']}` with `{best['best_mre_pair']}` at `{_fmt(best['best_mre_pct_cost'])}` empirical cost fraction.",
        f"- Cost heterogeneity remains high in every release: CV ranges `{_fmt(min(_float(row, 'cost_cv') for row in rows))}`-`{_fmt(max(_float(row, 'cost_cv') for row in rows))}`.",
        f"- Count-cost calibration is close at the aggregate level: median `%cost/%n` ranges `{_fmt(min(_float(row, 'proxy_median_ratio') for row in rows))}`-`{_fmt(max(_float(row, 'proxy_median_ratio') for row in rows))}`.",
        f"- Decision-level Pareto disagreement remains visible: worst release is `{worst_pareto['release_label']}` with Jaccard `{_fmt(worst_pareto['pareto_jaccard'])}`.",
        "",
        "![Cross-release metrics](fig_linux_hgbt_release_metrics.png)",
        "",
        "![Strategy MRE by release](fig_linux_hgbt_strategy_mre.png)",
        "",
        "## Release Summary",
        "",
        "| Release | Features | Configs | Cost CV | Proxy ratio | Top-1 agreement | Pareto Jaccard | Best MRE pair | Best MRE |",
        "|---|---:|---:|---:|---:|---:|---:|---|---:|",
    ]
    for row in rows:
        lines.append(
            f"| `{row['release_label']}` | {row['feature_count']} | {row['n_configurations']} | "
            f"{_fmt(row['cost_cv'])} | {_fmt(row['proxy_median_ratio'])} | "
            f"{_fmt(row['rank_top1_agreement'])} | {_fmt(row['pareto_jaccard'])} | "
            f"`{row['best_mre_pair']}` | {_fmt(row['best_mre'])} |"
        )
    lines.extend(["", "## Hypothesis Summary", "", "| Hypothesis | Verdict | Supports | Refutes | Inconclusive |", "|---|---|---:|---:|---:|"])
    for h in ("H1a", "H1b", "H2a", "H2b", "H2c", "H3a", "H3b", "H4a", "H4b"):
        row = by_h.get(h)
        if not row:
            continue
        lines.append(
            f"| `{h}` | {row['global_verdict']} | {row['supports']} | {row['refutes']} | {row['inconclusive']} |"
        )
    lines.extend(
        [
            "",
            "## Output Files",
            "",
            "- `release_summary.csv`: one row per Linux release.",
            "- `all_strategy_summary.csv`, `all_records.csv`, `all_rq*_*.csv`: concatenated per-release artifacts.",
            "- `hypothesis_tests.csv` and `hypothesis_summary.csv`: H1a-H4b tests over release scopes.",
            "- `fig_linux_hgbt_release_metrics.png` and `fig_linux_hgbt_strategy_mre.png`: cross-release figures.",
            "",
        ]
    )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir) if args.output_dir else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    all_records: list[dict[str, Any]] = []
    all_heterogeneity: list[dict[str, Any]] = []
    all_strategy: list[dict[str, Any]] = []
    all_proxy: list[dict[str, Any]] = []
    all_ranks: list[dict[str, Any]] = []
    all_pareto: list[dict[str, Any]] = []
    all_hypotheses: list[dict[str, Any]] = []
    release_rows: list[dict[str, Any]] = []

    for release in RELEASES:
        folder = input_dir / f"linux{release}_vmlinux"
        if not (folder / "records.csv").exists():
            raise SystemExit(f"Missing Linux release artifacts: {folder}")
        records = _coerce_records(_read_csv(folder / "records.csv"), release)
        heterogeneity = _coerce_heterogeneity(_read_csv(folder / "rq1_cost_heterogeneity.csv"), release)
        strategy = _coerce_numeric_rows(_read_csv(folder / "strategy_summary.csv"), release)
        proxy = _coerce_numeric_rows(_read_csv(folder / "rq2_proxy_summary.csv"), release)
        ranks = _coerce_numeric_rows(_read_csv(folder / "rq3_rank_stability.csv"), release)
        pareto = _coerce_numeric_rows(_read_csv(folder / "rq4_pareto.csv"), release)

        scope = RELEASE_LABELS.get(release, release)
        h_rows = evaluate_per_context_hypotheses(
            scope_value=scope,
            records=records,
            heterogeneity=heterogeneity,
            rank_rows=ranks,
            pareto_rows=pareto,
            cost_values=None,
        )
        for row in h_rows:
            row["release"] = release
            row["family"] = "LINUX"
            row["learner"] = "sk-hgbt-log"
            row["feature_set"] = "all_features"
        write_csv(folder / "hypothesis_tests.csv", h_rows)

        release_rows.append(
            _release_summary(
                release=release,
                folder=folder,
                heterogeneity=heterogeneity,
                strategy_rows=strategy,
                proxy_rows=proxy,
                rank_rows=ranks,
                pareto_rows=pareto,
            )
        )
        all_records.extend(records)
        all_heterogeneity.extend(heterogeneity)
        all_strategy.extend(strategy)
        all_proxy.extend(proxy)
        all_ranks.extend(ranks)
        all_pareto.extend(pareto)
        all_hypotheses.extend(h_rows)

    write_csv(output_dir / "all_records.csv", all_records)
    write_csv(output_dir / "all_rq1_cost_heterogeneity.csv", all_heterogeneity)
    write_csv(output_dir / "all_strategy_summary.csv", all_strategy)
    write_csv(output_dir / "all_rq2_proxy_summary.csv", all_proxy)
    write_csv(output_dir / "all_rq3_rank_stability.csv", all_ranks)
    write_csv(output_dir / "all_rq4_pareto.csv", all_pareto)
    write_csv(output_dir / "release_summary.csv", release_rows)
    write_csv(output_dir / "hypothesis_tests.csv", all_hypotheses)
    hypothesis_summary = aggregate_verdicts(all_hypotheses)
    write_csv(output_dir / "hypothesis_summary.csv", hypothesis_summary)
    _plot_release_metrics(release_rows, output_dir / "fig_linux_hgbt_release_metrics.png")
    _plot_strategy_mre(all_strategy, output_dir / "fig_linux_hgbt_strategy_mre.png")
    _write_report(output_dir / "linux_hgbt_allfeatures_report.md", release_rows, hypothesis_summary)
    print(f"Wrote Linux HGBT summary outputs to {output_dir}")


if __name__ == "__main__":
    main()
