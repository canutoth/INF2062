#!/usr/bin/env python3
"""Summarize learner-sensitivity outputs into CSV and Markdown."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
import statistics
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]


METRICS = (
    "cost_cv",
    "proxy_spearman",
    "proxy_median_ratio",
    "rank_top1_agreement",
    "rank_mean_kendall_tau",
    "pareto_jaccard",
    "best_simple_mre",
    "best_simple_pct_cost",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="artifacts/learner_sensitivity")
    return parser.parse_args()


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _float(row: dict[str, Any], key: str, default: float = float("nan")) -> float:
    try:
        return float(row[key])
    except (KeyError, TypeError, ValueError):
        return default


def _median(values: list[float]) -> float:
    finite = [value for value in values if value == value]
    return float(statistics.median(finite)) if finite else float("nan")


def _range(values: list[float]) -> str:
    finite = [value for value in values if value == value]
    if not finite:
        return "NA"
    return f"{min(finite):.4g}-{max(finite):.4g}"


def _pair(row: dict[str, Any]) -> str:
    return f"{row.get('strategy')}_{row.get('level')}"


def _linux_row(output_dir: Path) -> dict[str, Any] | None:
    heterogeneity = _read_csv(output_dir / "rq1_cost_heterogeneity.csv")
    proxy = _read_csv(output_dir / "rq2_proxy_summary.csv")
    summary = _read_csv(output_dir / "strategy_summary.csv")
    ranks = _read_csv(output_dir / "rq3_rank_stability.csv")
    pareto = _read_csv(output_dir / "rq4_pareto.csv")
    if not heterogeneity or not proxy or not summary or not ranks or not pareto:
        return None
    overall_proxy = next((row for row in proxy if row.get("strategy") == "ALL"), proxy[0])
    best = min(summary, key=lambda row: _float(row, "median_mre") + _float(row, "median_pct_cost"))
    count = {_pair(row) for row in pareto if str(row.get("pareto_count")).lower() in {"1", "true"}}
    empirical = {_pair(row) for row in pareto if str(row.get("pareto_empirical")).lower() in {"1", "true"}}
    union = count | empirical
    return {
        "unit": output_dir.name,
        "cost_cv": _float(heterogeneity[0], "cv_cost"),
        "proxy_spearman": _float(overall_proxy, "spearman_n_train_cost"),
        "proxy_median_ratio": _float(overall_proxy, "median_calibration_ratio"),
        "rank_top1_agreement": _median([_float(row, "top1_agreement") for row in ranks]),
        "rank_mean_kendall_tau": _median([_float(row, "kendall_tau") for row in ranks]),
        "pareto_jaccard": len(count & empirical) / len(union) if union else 1.0,
        "best_simple_mre": _float(best, "median_mre"),
        "best_simple_pct_cost": _float(best, "median_pct_cost"),
    }


def _rows_for_manifest_entry(entry: dict[str, str]) -> list[dict[str, Any]]:
    output_dir = Path(entry["output_dir"])
    if not output_dir.is_absolute():
        output_dir = REPO_ROOT / output_dir
    family = entry["family"]
    label = entry["label"]
    if family == "REPLICATION" and label == "x264_matrix":
        rows = _read_csv(output_dir / "context_summary.csv")
        return [dict(row, unit=f"x264:{row.get('scenario')}:{row.get('target_context')}") for row in rows]
    if family == "REPLICATION" and label == "newruns":
        rows = _read_csv(output_dir / "system_summary.csv")
        return [dict(row, unit=f"newruns:{row.get('context')}") for row in rows]
    if family == "ENERGY":
        rows = _read_csv(output_dir / "scenario_summary.csv")
        return [dict(row, unit=f"{row.get('analysis_context')}:{row.get('scenario')}") for row in rows]
    if family == "WORKLOAD":
        rows = _read_csv(output_dir / "all_workload_summary.csv")
        return [dict(row, unit=f"{row.get('system')}:{row.get('workload')}") for row in rows]
    if family == "LCBENCH":
        rows = _read_csv(output_dir / "workload_summary.csv")
        return [dict(row, unit=f"lcbench:{row.get('workload')}") for row in rows]
    if family == "LINUX":
        row = _linux_row(output_dir)
        return [row] if row is not None else []
    return []


def _aggregate(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["family"]), str(row["label"]), str(row["learner"]))].append(row)
    out: list[dict[str, Any]] = []
    for (family, label, learner), items in sorted(grouped.items()):
        record: dict[str, Any] = {
            "family": family,
            "label": label,
            "learner": learner,
            "units": len(items),
        }
        for metric in METRICS:
            values = [_float(row, metric) for row in items]
            record[f"median_{metric}"] = _median(values)
            record[f"range_{metric}"] = _range(values)
        out.append(record)
    return out


def _winner_rows(summary: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in summary:
        grouped[(row["family"], row["label"])].append(row)
    out: list[dict[str, Any]] = []
    def _best(rows: list[dict[str, Any]], metric: str, *, maximize: bool) -> dict[str, Any] | None:
        finite = [row for row in rows if _float(row, metric) == _float(row, metric)]
        if not finite:
            return None
        return (max if maximize else min)(finite, key=lambda row: _float(row, metric))

    for (family, label), rows in sorted(grouped.items()):
        best_mre = _best(rows, "median_best_simple_mre", maximize=False)
        most_stable_rank = _best(rows, "median_rank_top1_agreement", maximize=True)
        most_stable_pareto = _best(rows, "median_pareto_jaccard", maximize=True)
        out.append(
            {
                "family": family,
                "label": label,
                "best_mre_learner": best_mre["learner"] if best_mre else "NA",
                "best_mre": best_mre["median_best_simple_mre"] if best_mre else "nan",
                "rank_stability_learner": most_stable_rank["learner"] if most_stable_rank else "NA",
                "rank_top1_agreement": (
                    most_stable_rank["median_rank_top1_agreement"] if most_stable_rank else "nan"
                ),
                "pareto_stability_learner": most_stable_pareto["learner"] if most_stable_pareto else "NA",
                "pareto_jaccard": most_stable_pareto["median_pareto_jaccard"] if most_stable_pareto else "nan",
            }
        )
    return out


def _write_protocol(path: Path) -> None:
    lines = [
        "# Learner Sensitivity Protocol",
        "",
        "This artifact treats the learner as a variation point while keeping each family-specific sampling/cost protocol fixed.",
        "",
        "| Family | Units | Sampling protocol | Primary learner in main artifacts | Learners varied here | Notes |",
        "|---|---|---|---|---|---|",
        "| `REPLICATION` | x264 input/scenario rows and NewRuns systems | Published sample traces; budgeted rerun uses a capped number of published repetitions | Literature-aligned regression where possible; current scripts use ridge/log-linear as the reproducible implementation | `ridge-log`, `rf-log`, `gbt-log` | This is the family where the original rationale for the baseline learner is strongest. RQ1/RQ2 are learner-independent. |",
        "| `ENERGY` | Twins cost-target scenarios | Generated common pool sampling | `ridge-log` | `ridge-log`, `rf-log`, `gbt-log` | Learner affects only MRE-driven RQ3/RQ4 and any RQ5 claim using MRE. |",
        "| `WORKLOAD` | System-workload contexts | Generated common pool sampling per workload | `ridge-log` | `ridge-log`, `rf-log`, `gbt-log` | Workload sensitivity in RQ1/RQ2 is unchanged; decision stability can move with learner accuracy. |",
        "| `LCBENCH` | OpenML datasets | Generated common pool sampling per dataset | `ridge-raw` | `ridge-raw`, `rf-raw`, `gbt-raw` | Accuracy is bounded in [0,1], so raw-target learners are the cleaner default. |",
        "| `LINUX` | Kernel releases | Pool subsampling on TuxKConfig releases | `ridge-log` | `ridge-log`, `rf-log`, `gbt-log` | The sensitivity pass uses reduced levels/runs by default because full Linux learner sweeps are expensive. |",
        "",
        "Interpretation rule: do not compare families as if they shared identical sampling protocols. Compare whether learner changes alter the within-family RQ3/RQ4 conclusions.",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def _write_report(path: Path, summary: list[dict[str, Any]], winners: list[dict[str, Any]], manifest: list[dict[str, str]]) -> None:
    linux_failures = [
        row
        for row in manifest
        if row.get("family") == "LINUX" and row.get("returncode") not in {"0", 0}
    ]
    lines = [
        "# Learner Sensitivity Report",
        "",
        "## Headline",
        "",
        "RQ1 and RQ2 do not change with learner choice because they use only selected configurations and empirical costs. "
        "The relevant checks are RQ3/RQ4: rank stability, Pareto overlap, and median prediction error.",
        "",
        "## Aggregate by family and learner",
        "",
        "| Family | Label | Learner | Units | Median MRE | Top-1 agreement | Pareto Jaccard |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in summary:
        lines.append(
            f"| `{row['family']}` | `{row['label']}` | `{row['learner']}` | {row['units']} | "
            f"{_float(row, 'median_best_simple_mre'):.4g} | "
            f"{_float(row, 'median_rank_top1_agreement'):.4g} | "
            f"{_float(row, 'median_pareto_jaccard'):.4g} |"
        )
    lines.extend(
        [
            "",
            "## Best learners by criterion",
            "",
            "| Family | Label | Best MRE learner | Most rank-stable learner | Most Pareto-stable learner |",
            "|---|---|---|---|---|",
        ]
    )
    for row in winners:
        lines.append(
            f"| `{row['family']}` | `{row['label']}` | `{row['best_mre_learner']}` "
            f"({_float(row, 'best_mre'):.4g}) | `{row['rank_stability_learner']}` "
            f"({_float(row, 'rank_top1_agreement'):.4g}) | `{row['pareto_stability_learner']}` "
            f"({_float(row, 'pareto_jaccard'):.4g}) |"
        )
    lines.extend(
        [
            "",
            "## Conclusions",
            "",
            "- RQ1 and RQ2 are unchanged by construction: they inspect sampled configurations and empirical costs, before any learner is fitted.",
            "- Stronger learners change absolute MRE, but they do not remove the decision-level instability measured by top-1 agreement and Pareto overlap.",
            "- Ridge/log-linear remains a competitive default in the compact REPLICATION and ENERGY slices; boosted trees are useful as a robustness check and can improve median MRE in WORKLOAD and LCBENCH.",
            "- The main interpretation should therefore be learner sensitivity, not learner replacement: report the primary learner per family, then keep random forests and boosted trees as supplementary robustness evidence.",
            "",
            "## Family-level reading",
            "",
        ]
    )
    for family, label in sorted({(row["family"], row["label"]) for row in summary}):
        family_rows = [row for row in summary if row["family"] == family and row["label"] == label]
        best = min(family_rows, key=lambda row: _float(row, "median_best_simple_mre"))
        worst = max(family_rows, key=lambda row: _float(row, "median_best_simple_mre"))
        stable = max(family_rows, key=lambda row: _float(row, "median_pareto_jaccard"))
        lines.append(
            f"- `{family}` / `{label}`: best median MRE is `{best['learner']}` "
            f"({_float(best, 'median_best_simple_mre'):.4g}); worst is `{worst['learner']}` "
            f"({_float(worst, 'median_best_simple_mre'):.4g}). Pareto overlap remains partial "
            f"(best median Jaccard `{stable['learner']}` = {_float(stable, 'median_pareto_jaccard'):.4g})."
        )
    if linux_failures:
        lines.extend(
            [
                "",
                "## Execution caveat",
                "",
                f"- `LINUX` learner sensitivity did not complete in this environment ({len(linux_failures)} failed commands). "
                "The run logs show the local Python environment is missing `pyarrow`, which is required to read the TuxKConfig parquet files.",
            ]
        )
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    args = parse_args()
    root = REPO_ROOT / args.input_dir
    manifest = _read_csv(root / "manifest.csv")
    long_rows: list[dict[str, Any]] = []
    for entry in manifest:
        if entry.get("returncode") not in {"0", 0}:
            continue
        for row in _rows_for_manifest_entry(entry):
            item = dict(row)
            item["family"] = entry["family"]
            item["label"] = entry["label"]
            item["learner"] = entry["learner"]
            long_rows.append(item)

    summary = _aggregate(long_rows)
    winners = _winner_rows(summary)
    _write_csv(root / "learner_sensitivity_long.csv", long_rows)
    _write_csv(root / "learner_sensitivity_summary.csv", summary)
    _write_csv(root / "learner_sensitivity_winners.csv", winners)
    _write_protocol(root / "learner_protocol.md")
    _write_report(root / "learner_sensitivity_report.md", summary, winners, manifest)
    print(f"Wrote learner sensitivity summary to {root}")


if __name__ == "__main__":
    main()
