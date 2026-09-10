#!/usr/bin/env python3
"""Summarize a completed workload-impact generated-sampling batch run."""

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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-dir",
        default="artifacts/workload_batch_overnight",
        help="Batch root containing per-system workload outputs.",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Report path; defaults to <input-dir>/workload_batch_report.md",
    )
    return parser.parse_args()


def _read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


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


def _finite(values: list[float]) -> list[float]:
    return [value for value in values if math.isfinite(value)]


def _range(values: list[float]) -> tuple[float, float]:
    values = _finite(values)
    if not values:
        return float("nan"), float("nan")
    return min(values), max(values)


def _median(values: list[float]) -> float:
    values = _finite(values)
    return float(np.median(values)) if values else float("nan")


def _plot_range_chart(
    rows: list[dict[str, Any]],
    *,
    lo_key: str,
    hi_key: str,
    xlabel: str,
    title: str,
    output: Path,
    sort_by: str | None = None,
) -> None:
    if not rows:
        return
    ordered = rows
    if sort_by:
        ordered = sorted(rows, key=lambda row: _float(row, sort_by), reverse=True)
    labels = [str(row["system"]) for row in ordered]
    y = np.arange(len(labels))
    lo = [_float(row, lo_key) for row in ordered]
    hi = [_float(row, hi_key) for row in ordered]

    fig, ax = plt.subplots(figsize=(8.8, max(4.5, 0.45 * len(labels) + 1.2)))
    for idx, (a, b) in enumerate(zip(lo, hi)):
        ax.plot([a, b], [idx, idx], color="#4C78A8", linewidth=6, solid_capstyle="round")
        ax.scatter([a, b], [idx, idx], color="#1f3b57", s=20, zorder=3)
    ax.set_yticks(y)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel(xlabel)
    ax.set_title(title)
    ax.grid(axis="x", color="#dddddd", linewidth=0.8)
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def _plot_dual_metric_ranges(rows: list[dict[str, Any]], output: Path) -> None:
    if not rows:
        return
    ordered = sorted(rows, key=lambda row: _float(row, "rank_top1_agreement_min"))
    labels = [str(row["system"]) for row in ordered]
    y = np.arange(len(labels))
    top1_lo = [_float(row, "rank_top1_agreement_min") for row in ordered]
    top1_hi = [_float(row, "rank_top1_agreement_max") for row in ordered]
    jac_lo = [_float(row, "pareto_jaccard_min") for row in ordered]
    jac_hi = [_float(row, "pareto_jaccard_max") for row in ordered]

    fig, axes = plt.subplots(1, 2, figsize=(11.0, max(4.8, 0.45 * len(labels) + 1.2)), sharey=True)
    for ax, lo, hi, title, color in [
        (axes[0], top1_lo, top1_hi, "Top-1 agreement range across workloads", "#4C78A8"),
        (axes[1], jac_lo, jac_hi, "Pareto Jaccard range across workloads", "#F58518"),
    ]:
        for idx, (a, b) in enumerate(zip(lo, hi)):
            ax.plot([a, b], [idx, idx], color=color, linewidth=6, solid_capstyle="round")
            ax.scatter([a, b], [idx, idx], color="#333333", s=20, zorder=3)
        ax.set_xlim(-0.02, 1.02)
        ax.set_title(title)
        ax.grid(axis="x", color="#dddddd", linewidth=0.8)
        ax.set_axisbelow(True)
    axes[0].set_yticks(y)
    axes[0].set_yticklabels(labels)
    axes[0].invert_yaxis()
    axes[1].tick_params(labelleft=False)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)


def _summarize_system(
    system: str,
    workload_rows: list[dict[str, Any]],
    h5_rows: list[dict[str, Any]],
    manifest_row: dict[str, Any] | None,
) -> dict[str, Any]:
    cost_cv = [_float(row, "cost_cv") for row in workload_rows]
    rho = [_float(row, "proxy_spearman") for row in workload_rows]
    ratio = [_float(row, "proxy_median_ratio") for row in workload_rows]
    top1 = [_float(row, "rank_top1_agreement") for row in workload_rows]
    flips = [_int(row, "rank_top1_flips") for row in workload_rows]
    tau = [_float(row, "rank_mean_kendall_tau") for row in workload_rows]
    jac = [_float(row, "pareto_jaccard") for row in workload_rows]

    worst_proxy = min(workload_rows, key=lambda row: _float(row, "proxy_spearman"))
    worst_top1 = min(workload_rows, key=lambda row: _float(row, "rank_top1_agreement"))
    highest_cv = max(workload_rows, key=lambda row: _float(row, "cost_cv"))
    h5 = h5_rows[0] if h5_rows else {}

    cv_lo, cv_hi = _range(cost_cv)
    rho_lo, rho_hi = _range(rho)
    ratio_lo, ratio_hi = _range(ratio)
    top1_lo, top1_hi = _range(top1)
    tau_lo, tau_hi = _range(tau)
    jac_lo, jac_hi = _range(jac)

    return {
        "system": system,
        "target_column": workload_rows[0].get("target_property", ""),
        "cost_column": workload_rows[0].get("cost_property", ""),
        "n_workloads": len(workload_rows),
        "n_configurations": _int(workload_rows[0], "n_configurations"),
        "seeds": _int(workload_rows[0], "seeds"),
        "cost_cv_min": cv_lo,
        "cost_cv_max": cv_hi,
        "proxy_spearman_min": rho_lo,
        "proxy_spearman_max": rho_hi,
        "proxy_median_ratio_min": ratio_lo,
        "proxy_median_ratio_max": ratio_hi,
        "rank_top1_agreement_min": top1_lo,
        "rank_top1_agreement_max": top1_hi,
        "rank_top1_flips_max": max(flips) if flips else 0,
        "rank_mean_kendall_tau_min": tau_lo,
        "rank_mean_kendall_tau_max": tau_hi,
        "pareto_jaccard_min": jac_lo,
        "pareto_jaccard_max": jac_hi,
        "median_cost_cv": _median(cost_cv),
        "median_proxy_spearman": _median(rho),
        "median_proxy_ratio": _median(ratio),
        "median_top1_agreement": _median(top1),
        "median_pareto_jaccard": _median(jac),
        "highest_cv_workload": highest_cv.get("workload", ""),
        "highest_cv_value": _float(highest_cv, "cost_cv"),
        "worst_proxy_workload": worst_proxy.get("workload", ""),
        "worst_proxy_value": _float(worst_proxy, "proxy_spearman"),
        "least_stable_workload": worst_top1.get("workload", ""),
        "least_stable_top1_agreement": _float(worst_top1, "rank_top1_agreement"),
        "least_stable_flips": _int(worst_top1, "rank_top1_flips"),
        "h5a_verdict": h5.get("verdict", ""),
        "h5a_p_value": _float(h5, "p_value"),
        "h5a_ratio_spread": _float(h5, "effect_value"),
        "returncode": _int(manifest_row or {}, "returncode"),
        "elapsed_seconds": _float(manifest_row or {}, "elapsed_seconds"),
    }


def _write_report(
    path: Path,
    *,
    input_dir: Path,
    system_rows: list[dict[str, Any]],
) -> None:
    lines = [
        "# Workload-impact cross-system report",
        "",
        f"Input batch: `{input_dir}`.",
        "",
    ]
    total_workloads = sum(_int(row, "n_workloads") for row in system_rows)
    runtime_systems = sum(1 for row in system_rows if row.get("target_column") == "time")
    throughput_systems = sum(1 for row in system_rows if row.get("target_column") == "throughput")
    lines.extend(
        [
            "## Scope",
            "",
            f"Systems covered: `{len(system_rows)}`. Workload contexts covered: `{total_workloads}`.",
            "",
            f"Target/cost setup: `{runtime_systems}` runtime systems plus `{throughput_systems}` throughput-oriented system (`h2`, with cost = `1/throughput`).",
            "",
        ]
    )

    highest_cv = max(system_rows, key=lambda row: _float(row, "cost_cv_max"))
    weakest_proxy = min(system_rows, key=lambda row: _float(row, "proxy_spearman_min"))
    least_stable = min(system_rows, key=lambda row: _float(row, "rank_top1_agreement_min"))
    worst_pareto = min(system_rows, key=lambda row: _float(row, "pareto_jaccard_min"))
    supported_h5a = sum(1 for row in system_rows if row.get("h5a_verdict") == "supports")

    lines.extend(
        [
            "## Readout",
            "",
            f"Highest observed cost heterogeneity: `{highest_cv['system']}` with workload-level CV up to `{_fmt(highest_cv['cost_cv_max'])}`.",
            "",
            f"Weakest count-cost proxy: `{weakest_proxy['system']}` with workload-level Spearman rho down to `{_fmt(weakest_proxy['proxy_spearman_min'])}`.",
            "",
            f"Least stable top-1 decisions: `{least_stable['system']}` with workload-level agreement as low as `{_fmt(least_stable['rank_top1_agreement_min'])}`.",
            "",
            f"Strongest Pareto disagreement: `{worst_pareto['system']}` with workload-level Jaccard down to `{_fmt(worst_pareto['pareto_jaccard_min'])}`.",
            "",
            f"H5a workload sensitivity is supported in `{supported_h5a} / {len(system_rows)}` systems.",
            "",
        ]
    )

    lines.extend(
        [
            "## Systems",
            "",
            "| System | Workloads | Cost CV range | Spearman rho range | Median %cost/%n range | Top-1 agreement range | Pareto Jaccard range | H5a |",
            "|---|---:|---:|---:|---:|---:|---:|---|",
        ]
    )
    for row in sorted(system_rows, key=lambda item: item["system"]):
        lines.append(
            f"| `{row['system']}` | {row['n_workloads']} | "
            f"{_fmt(row['cost_cv_min'])}-{_fmt(row['cost_cv_max'])} | "
            f"{_fmt(row['proxy_spearman_min'])}-{_fmt(row['proxy_spearman_max'])} | "
            f"{_fmt(row['proxy_median_ratio_min'])}-{_fmt(row['proxy_median_ratio_max'])} | "
            f"{_fmt(row['rank_top1_agreement_min'])}-{_fmt(row['rank_top1_agreement_max'])} | "
            f"{_fmt(row['pareto_jaccard_min'])}-{_fmt(row['pareto_jaccard_max'])} | "
            f"`{row['h5a_verdict']}` |"
        )

    lines.extend(
        [
            "",
            "## Files",
            "",
            "- `all_workload_summary.csv`: concatenated workload rows from every system.",
            "- `system_summary.csv`: one row per system with workload ranges and H5a verdicts.",
            "- `fig_cost_cv_range_by_system.png`: cost heterogeneity range by system.",
            "- `fig_rq2_proxy_spearman_range_by_system.png`: sample-size ordering quality by system.",
            "- `fig_rq2_median_calibration_range_by_system.png`: calibration range by system.",
            "- `fig_rq3_rq4_decision_range_by_system.png`: top-1 agreement and Pareto Jaccard ranges by system.",
            "",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    args = parse_args()
    input_dir = REPO_ROOT / args.input_dir
    output = Path(args.output) if args.output else input_dir / "workload_batch_report.md"

    manifest_rows = _read_csv(input_dir / "batch_manifest.csv")
    manifest_index = {row["system"]: row for row in manifest_rows if row.get("system")}
    system_rows: list[dict[str, Any]] = []
    all_workloads: list[dict[str, Any]] = []

    for path in sorted(input_dir.iterdir()):
        if not path.is_dir():
            continue
        workload_rows = _read_csv(path / "workload_summary.csv")
        if not workload_rows:
            continue
        h5_rows = _read_csv(path / "h5_workload_sensitivity.csv")
        all_workloads.extend(workload_rows)
        system_rows.append(_summarize_system(path.name, workload_rows, h5_rows, manifest_index.get(path.name)))

    system_rows.sort(key=lambda row: row["system"])
    _write_csv(input_dir / "all_workload_summary.csv", all_workloads)
    _write_csv(input_dir / "system_summary.csv", system_rows)

    _plot_range_chart(
        system_rows,
        lo_key="cost_cv_min",
        hi_key="cost_cv_max",
        xlabel="Cost CV range across workloads",
        title="RQ1: cost heterogeneity range by system",
        output=input_dir / "fig_cost_cv_range_by_system.png",
        sort_by="cost_cv_max",
    )
    _plot_range_chart(
        system_rows,
        lo_key="proxy_spearman_min",
        hi_key="proxy_spearman_max",
        xlabel="Spearman rho(n, TrainCost) range across workloads",
        title="RQ2: sample-size ordering quality by system",
        output=input_dir / "fig_rq2_proxy_spearman_range_by_system.png",
        sort_by="proxy_spearman_min",
    )
    _plot_range_chart(
        system_rows,
        lo_key="proxy_median_ratio_min",
        hi_key="proxy_median_ratio_max",
        xlabel="Median %TrainCost / %n range across workloads",
        title="RQ2: calibration range by system",
        output=input_dir / "fig_rq2_median_calibration_range_by_system.png",
        sort_by="proxy_median_ratio_min",
    )
    _plot_dual_metric_ranges(system_rows, input_dir / "fig_rq3_rq4_decision_range_by_system.png")
    _write_report(output, input_dir=input_dir, system_rows=system_rows)


if __name__ == "__main__":
    main()
