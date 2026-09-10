#!/usr/bin/env python3
"""Run FSE-style posterior guarantee/cost analysis across systems."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import replace
import math
from pathlib import Path
import sys
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = Path(__file__).resolve().parent
for path in (REPO_ROOT, SCRIPT_DIR):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from cost_sampling.analysis import level_sort_key, strategy_sort_key, write_csv
from cost_sampling.fse_artifact import load_fse_directory_dataset

from run_fse_posterior import (
    _fmt,
    _parse_set,
    confidence_curves,
    posterior_hypothesis_summary,
    posterior_hypothesis_tests,
    posterior_pareto,
    posterior_records,
    posterior_summary,
    write_figures,
    write_report,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fse-root",
        required=True,
        help="Extracted FSE 2026 artifact root, data/, or data/sampling/ directory.",
    )
    parser.add_argument("--output-dir", default="artifacts/fse_posterior_fse_artifact_all")
    parser.add_argument("--contexts", default="ALL", help="Comma-separated systems, or ALL.")
    parser.add_argument(
        "--strategies",
        default="random,solverBased,divDistBased,twise,SRSSampling",
        help="Comma-separated strategies. Default covers the FSE paper's five representative strategies.",
    )
    parser.add_argument("--levels", default="t2", help="Comma-separated levels; default mirrors the paper's t2 fixed budget.")
    parser.add_argument("--max-runs", type=int, default=100)
    parser.add_argument("--performance-name", default="Performance")
    parser.add_argument("--extreme", choices=("max", "min"), default="max")
    parser.add_argument("--prior-offset", type=int, default=1)
    parser.add_argument("--epsilon-points", type=int, default=151)
    parser.add_argument("--plot-epsilon-max", type=float, default=0.15)
    return parser.parse_args()


def _sampling_root(root: str | Path) -> Path:
    path = Path(root)
    for candidate in (path / "data" / "sampling", path / "sampling", path):
        if candidate.exists() and any(child.is_dir() for child in candidate.iterdir()):
            return candidate
    raise FileNotFoundError(f"Cannot find FSE sampling root under {root}")


def _contexts(root: str | Path, raw: str) -> list[str]:
    if raw.strip().upper() != "ALL":
        return [part.strip() for part in raw.split(",") if part.strip()]
    sampling_root = _sampling_root(root)
    return sorted([child.name for child in sampling_root.iterdir() if child.is_dir()])


def _median(values: list[float]) -> float:
    return float(np.median(np.asarray(values, dtype=float)))


def _frontier_label(row: dict[str, Any]) -> str:
    return f"{row['strategy']}_{row['level']}"


def _pareto_jaccard(pareto_rows: list[dict[str, Any]], key: str) -> float:
    count_front = {_frontier_label(row) for row in pareto_rows if row[f"pareto_count_cost_{key}"]}
    empirical_front = {_frontier_label(row) for row in pareto_rows if row[f"pareto_empirical_cost_{key}"]}
    union = count_front | empirical_front
    return len(count_front & empirical_front) / len(union) if union else 1.0


def summarize_system(
    dataset: Any,
    summary: list[dict[str, Any]],
    pareto: list[dict[str, Any]],
    hypotheses: list[dict[str, Any]],
) -> dict[str, Any]:
    values = np.asarray(dataset.cost_values, dtype=float)
    mean = float(np.mean(values))
    cv = float(np.std(values, ddof=1) / mean) if mean else float("nan")
    p10, p90 = np.percentile(values, [10, 90])
    ratio_by_pair = {
        _frontier_label(row): float(row["median_calibration_ratio"])
        for row in summary
    }
    best_risk = min(summary, key=lambda row: row["median_posterior_risk"])
    best_size = max(summary, key=lambda row: row["omega_size_baseline"])
    best_cost = max(summary, key=lambda row: row["omega_cost_baseline"])
    srs = next((row for row in summary if row["strategy"] == "SRSSampling"), None)
    srs_pareto = next((row for row in pareto if row["strategy"] == "SRSSampling"), None)
    fse2 = next((row for row in hypotheses if row["hypothesis"] == "FSE2"), None)
    fse3 = next((row for row in hypotheses if row["hypothesis"] == "FSE3"), None)
    fse4 = next((row for row in hypotheses if row["hypothesis"] == "FSE4"), None)
    fse5 = next((row for row in hypotheses if row["hypothesis"] == "FSE5"), None)
    fse6 = next((row for row in hypotheses if row["hypothesis"] == "FSE6"), None)
    count_front = [_frontier_label(row) for row in pareto if row["pareto_count_cost_confidence"]]
    empirical_front = [_frontier_label(row) for row in pareto if row["pareto_empirical_cost_confidence"]]
    return {
        "context": dataset.context,
        "n_configurations": len(dataset.y),
        "strategies": ",".join(sorted({row["strategy"] for row in summary}, key=strategy_sort_key)),
        "levels": ",".join(sorted({row["level"] for row in summary}, key=level_sort_key)),
        "cost_cv": cv,
        "cost_p90_over_p10": float(p90 / p10) if p10 else float("nan"),
        "median_calibration_ratio": _median([float(row["median_calibration_ratio"]) for row in summary]),
        "min_calibration_ratio": min(ratio_by_pair.values()),
        "max_calibration_ratio": max(ratio_by_pair.values()),
        "best_risk_pair": _frontier_label(best_risk),
        "best_risk": float(best_risk["median_posterior_risk"]),
        "best_size_pair": _frontier_label(best_size),
        "best_cost_pair": _frontier_label(best_cost),
        "best_cost_omega": float(best_cost["omega_cost_baseline"]),
        "cost_normalization_changed_top": int(bool(fse2 and fse2["verdict"] == "supports")),
        "srs_risk": float(srs["median_posterior_risk"]) if srs else float("nan"),
        "srs_pct_cost": float(srs["median_pct_cost"]) if srs else float("nan"),
        "srs_omega_cost": float(srs["omega_cost_baseline"]) if srs else float("nan"),
        "srs_best_cost_normalized": int(bool(fse3 and fse3["verdict"] == "supports")),
        "srs_on_empirical_confidence_frontier": int(bool(srs_pareto and srs_pareto["pareto_empirical_cost_confidence"])),
        "srs_vs_random_risk_verdict": fse5["verdict"] if fse5 else "",
        "srs_vs_random_cost_verdict": fse6["verdict"] if fse6 else "",
        "confidence_pareto_jaccard": float(fse4["statistic_value"]) if fse4 else _pareto_jaccard(pareto, "confidence"),
        "confidence_pareto_changed": int(bool(fse4 and fse4["verdict"] == "supports")),
        "count_confidence_front": ",".join(count_front),
        "empirical_confidence_front": ",".join(empirical_front),
    }


def _counts(rows: list[dict[str, Any]], key: str) -> Counter[str]:
    return Counter(str(row[key]) for row in rows)


def write_batch_report(
    output: Path,
    *,
    system_rows: list[dict[str, Any]],
    hypothesis_rows: list[dict[str, Any]],
    contexts: list[str],
    strategies: set[str] | None,
    levels: set[str] | None,
) -> None:
    best_cost_counts = _counts(system_rows, "best_cost_pair")
    changed_top = sum(int(row["cost_normalization_changed_top"]) for row in system_rows)
    changed_front = sum(int(row["confidence_pareto_changed"]) for row in system_rows)
    srs_best = sum(int(row["srs_best_cost_normalized"]) for row in system_rows)
    srs_front = sum(int(row["srs_on_empirical_confidence_frontier"]) for row in system_rows)
    n_systems = len(system_rows)
    strategy_text = ",".join(sorted(strategies, key=strategy_sort_key)) if strategies is not None else "ALL"
    level_text = ",".join(sorted(levels, key=level_sort_key)) if levels is not None else "ALL"

    lines = [
        "# FSE-style posterior cross-system cost-normalization report",
        "",
        "## Scope",
        "",
        "This is the FSE posterior-risk/posterior-confidence experiment mapped onto the paper's RQ1-RQ5 protocol. "
        "Posterior risk/confidence replaces MRE as the outcome for ranking and Pareto decisions.",
        "",
        f"Systems: {', '.join(contexts)}.",
        f"Strategies: `{strategy_text}`. Levels: `{level_text}`.",
        "",
        "## Headline",
        "",
        f"Cost-normalization changed the top integrated-confidence recommendation in {changed_top}/{n_systems} systems. "
        f"The empirical confidence Pareto frontier changed in {changed_front}/{n_systems} systems.",
        "",
        f"SRS was the single best empirical-cost-normalized recommendation in {srs_best}/{n_systems} systems and "
        f"appeared on the empirical cost/confidence Pareto frontier in {srs_front}/{n_systems} systems.",
        "",
        "Best empirical-cost-normalized pairs by system:",
        "",
    ]
    for pair, count in best_cost_counts.most_common():
        lines.append(f"- `{pair}`: {count}/{n_systems}")

    lines.extend(
        [
            "",
            "## RQ1: Empirical Cost Heterogeneity",
            "",
            "| System | #configs | Cost CV | p90/p10 | Calibration range |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for row in system_rows:
        lines.append(
            f"| `{row['context']}` | {row['n_configurations']} | {_fmt(row['cost_cv'])} | "
            f"{_fmt(row['cost_p90_over_p10'])} | "
            f"{_fmt(row['min_calibration_ratio'])}-{_fmt(row['max_calibration_ratio'])} |"
        )

    lines.extend(
        [
            "",
            "Take-away: fixed sample size is not fixed empirical effort. The same t2 budget can select "
            "substantially cheaper or costlier configurations depending on the system and strategy.",
            "",
            "## RQ2: Sample Size As Cost Proxy",
            "",
            "| System | Median %cost/%n | Min %cost/%n | Max %cost/%n |",
            "|---|---:|---:|---:|",
        ]
    )
    for row in system_rows:
        lines.append(
            f"| `{row['context']}` | {_fmt(row['median_calibration_ratio'])} | "
            f"{_fmt(row['min_calibration_ratio'])} | {_fmt(row['max_calibration_ratio'])} |"
        )

    lines.extend(
        [
            "",
            "Take-away: in this fixed-budget FSE run, RQ2 is mainly about calibration rather than "
            "correlation across many n values. The count budget is useful for experiment design, but it "
            "does not represent the actual acquisition budget equally across strategies.",
            "",
            "## RQ3: Cost-Normalized Recommendation",
            "",
            "| System | Best by size baseline | Best by empirical-cost baseline | Changed? | SRS best? |",
            "|---|---|---|---:|---:|",
        ]
    )
    for row in system_rows:
        lines.append(
            f"| `{row['context']}` | `{row['best_size_pair']}` | `{row['best_cost_pair']}` | "
            f"{row['cost_normalization_changed_top']} | {row['srs_best_cost_normalized']} |"
        )

    lines.extend(
        [
            "",
            "Take-away: posterior guarantees can change the recommendation once empirical cost is used. "
            "SRS often remains competitive, but it is not a universal cost-normalized winner.",
            "",
            "## RQ4: Pareto-Efficient Choices",
            "",
            "| System | Jaccard | Count confidence front | Empirical confidence front | SRS on empirical front? |",
            "|---|---:|---|---|---:|",
        ]
    )
    for row in system_rows:
        lines.append(
            f"| `{row['context']}` | {_fmt(row['confidence_pareto_jaccard'])} | "
            f"`{row['count_confidence_front']}` | `{row['empirical_confidence_front']}` | "
            f"{row['srs_on_empirical_confidence_frontier']} |"
        )

    lines.extend(
        [
            "",
            "Take-away: the empirical-cost Pareto front is often not the same front as the count-cost front. "
            "This is the clearest decision-level evidence that sample size hides cost/guarantee tradeoffs.",
            "",
            "## RQ5: Cross-System Sensitivity",
            "",
            "| System | Best risk pair | Best cost pair | SRS risk | SRS %cost | SRS-vs-random risk | SRS-vs-random cost |",
            "|---|---|---|---:|---:|---|---|",
        ]
    )
    for row in system_rows:
        lines.append(
            f"| `{row['context']}` | `{row['best_risk_pair']}` | `{row['best_cost_pair']}` | "
            f"{_fmt(row['srs_risk'])} | {_fmt(row['srs_pct_cost'])} | "
            f"`{row['srs_vs_random_risk_verdict']}` | `{row['srs_vs_random_cost_verdict']}` |"
        )

    lines.extend(
        [
            "",
            "Take-away: the answer is system-dependent. The FSE posterior framework is useful because it "
            "makes this variability visible: a strategy may be excellent for low posterior risk yet lose "
            "when the empirical cost of acquiring its configurations is included.",
            "",
            "## Hypothesis Verdict Counts",
            "",
            "| Hypothesis | Supports | Refutes | Inconclusive |",
            "|---|---:|---:|---:|",
        ]
    )
    verdicts: dict[str, Counter[str]] = {}
    for row in hypothesis_rows:
        verdicts.setdefault(row["hypothesis"], Counter())[row["verdict"]] += 1
    for hypothesis in sorted(verdicts):
        counts = verdicts[hypothesis]
        lines.append(
            f"| `{hypothesis}` | {counts.get('supports', 0)} | "
            f"{counts.get('refutes', 0)} | {counts.get('inconclusive', 0)} |"
        )

    lines.extend(
        [
            "",
            "## Per-System Reports",
            "",
        ]
    )
    for row in system_rows:
        context = row["context"]
        lines.append(f"- [`{context}`]({context}/{context}_fse_posterior_report.md)")

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    contexts = _contexts(args.fse_root, args.contexts)
    strategies = _parse_set(args.strategies)
    levels = _parse_set(args.levels)

    all_records: list[dict[str, Any]] = []
    all_summary: list[dict[str, Any]] = []
    all_curves: list[dict[str, Any]] = []
    all_pareto: list[dict[str, Any]] = []
    all_hypotheses: list[dict[str, Any]] = []
    all_hypothesis_summaries: list[dict[str, Any]] = []
    system_rows: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []

    for context in contexts:
        try:
            dataset = load_fse_directory_dataset(
                args.fse_root,
                context,
                max_runs=args.max_runs,
                strategies=strategies,
                levels=levels,
                performance_name=args.performance_name,
            )
            dataset = replace(dataset, samples=list(dataset.samples))
            records = posterior_records(dataset, dataset.samples, extreme=args.extreme)
            summary = posterior_summary(records, n_configurations=len(dataset.y), prior_offset=args.prior_offset)
            curves = confidence_curves(records, epsilon_points=args.epsilon_points, prior_offset=args.prior_offset)
            pareto = posterior_pareto(summary)
            hypotheses = posterior_hypothesis_tests(records, summary, pareto, context=context)
            hypothesis_summary = posterior_hypothesis_summary(hypotheses)
            context_dir = output_dir / context
            context_dir.mkdir(parents=True, exist_ok=True)
            figures = write_figures(
                context_dir,
                records=records,
                summary=summary,
                curves=curves,
                pareto=pareto,
                epsilon_max=args.plot_epsilon_max,
            )
            write_csv(context_dir / "posterior_records.csv", records)
            write_csv(context_dir / "posterior_strategy_summary.csv", summary)
            write_csv(context_dir / "posterior_confidence_curves.csv", curves)
            write_csv(context_dir / "posterior_pareto.csv", pareto)
            write_csv(context_dir / "posterior_hypothesis_tests.csv", hypotheses)
            write_csv(context_dir / "posterior_hypothesis_summary.csv", hypothesis_summary)
            write_report(
                context_dir / f"{context}_fse_posterior_report.md",
                context=context,
                n_configurations=len(dataset.y),
                summary=summary,
                pareto=pareto,
                hypotheses=hypotheses,
                figures=figures,
                include_srs=False,
                prior_offset=args.prior_offset,
                extreme=args.extreme,
            )
            all_records.extend(records)
            all_summary.extend(summary)
            all_curves.extend(curves)
            all_pareto.extend(pareto)
            all_hypotheses.extend(hypotheses)
            all_hypothesis_summaries.extend(dict(row, context=context) for row in hypothesis_summary)
            system_rows.append(summarize_system(dataset, summary, pareto, hypotheses))
        except Exception as exc:  # noqa: BLE001 - batch should report all skipped systems.
            skipped.append({"context": context, "error": str(exc)})

    system_rows.sort(key=lambda row: row["context"])
    write_csv(output_dir / "posterior_records.csv", all_records)
    write_csv(output_dir / "posterior_strategy_summary.csv", all_summary)
    write_csv(output_dir / "posterior_confidence_curves.csv", all_curves)
    write_csv(output_dir / "posterior_pareto.csv", all_pareto)
    write_csv(output_dir / "posterior_hypothesis_tests.csv", all_hypotheses)
    write_csv(output_dir / "posterior_hypothesis_summary.csv", all_hypothesis_summaries)
    write_csv(output_dir / "posterior_system_summary.csv", system_rows)
    write_csv(output_dir / "skipped_contexts.csv", skipped)
    write_batch_report(
        output_dir / "fse_posterior_systems_report.md",
        system_rows=system_rows,
        hypothesis_rows=all_hypotheses,
        contexts=[row["context"] for row in system_rows],
        strategies=strategies,
        levels=levels,
    )
    print(f"Wrote FSE-style posterior cross-system outputs to {output_dir}")
    if skipped:
        print(f"Skipped {len(skipped)} contexts; see skipped_contexts.csv")


if __name__ == "__main__":
    main()
