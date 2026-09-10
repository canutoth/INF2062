#!/usr/bin/env python3
"""Plot fixed-n strategy comparison with full cost distribution above it."""

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

from cost_sampling.generated_sampling import load_twins_table, parse_where


STRATEGY_ORDER = ["random", "balanced", "diversity", "pairwise", "pilotCost"]
STRATEGY_COLORS = {
    "random": "#4C78A8",
    "balanced": "#F58518",
    "diversity": "#54A24B",
    "pairwise": "#B279A2",
    "pilotCost": "#E45756",
}
LABEL_OFFSETS = {
    "random": (6, 7),
    "balanced": (6, -12),
    "diversity": (6, 7),
    "pairwise": (-52, -1),
    "pilotCost": (6, 7),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="artifacts/twins_generated_representative_100s")
    parser.add_argument("--system-folder", default="brotli_1_0_7")
    parser.add_argument("--system", default="brotli")
    parser.add_argument("--where", default="revision=1.0.7")
    parser.add_argument("--zip", default="/private/tmp/TwinsOrFalseFriends-ICSE2023.zip")
    parser.add_argument("--cost", default="performance")
    parser.add_argument("--target", default="energy")
    parser.add_argument("--level", default="n8")
    parser.add_argument("--title", default="brotli 1.0.7: fixed n=8 samples and performance-cost distribution")
    parser.add_argument(
        "--output",
        default=(
            "artifacts/paper_figures/twins_brotli_pairwise_n8/"
            "brotli_fixed_n8_with_performance_distribution_deployable.png"
        ),
    )
    return parser.parse_args()


def _read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"Missing CSV file: {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _float(row: dict[str, Any], key: str) -> float:
    try:
        return float(row[key])
    except (KeyError, TypeError, ValueError):
        return float("nan")


def _percentile(values: list[float], pct: float) -> float:
    finite = [value for value in values if math.isfinite(value)]
    return float(np.percentile(finite, pct)) if finite else float("nan")


def _full_cost_values(args: argparse.Namespace) -> np.ndarray:
    where = parse_where([args.where]) if args.where else {}
    table = load_twins_table(args.zip, args.system, where=where)
    return np.asarray([float(row[args.cost]) for row in table.rows], dtype=float)


def _strategy_points(args: argparse.Namespace) -> list[dict[str, Any]]:
    records_path = Path(args.input_dir) / args.system_folder / "records.csv"
    records = [
        row
        for row in _read_csv(records_path)
        if row.get("cost_property") == args.cost
        and row.get("target_property") == args.target
        and row.get("level") == args.level
        and row.get("strategy") in STRATEGY_ORDER
    ]
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in records:
        grouped.setdefault(row["strategy"], []).append(row)

    out: list[dict[str, Any]] = []
    for strategy in STRATEGY_ORDER:
        rows = grouped.get(strategy, [])
        if not rows:
            continue
        mean_cost = [_float(row, "train_cost") / max(_float(row, "n"), 1.0) for row in rows]
        pct_cost = [_float(row, "pct_cost") for row in rows]
        mre = [_float(row, "mre") for row in rows]
        out.append(
            {
                "strategy": strategy,
                "runs": len(rows),
                "x": _percentile(mean_cost, 50),
                "x_q1": _percentile(mean_cost, 25),
                "x_q3": _percentile(mean_cost, 75),
                "pct_cost": _percentile(pct_cost, 50),
                "mre": _percentile(mre, 50),
                "mre_q1": _percentile(mre, 25),
                "mre_q3": _percentile(mre, 75),
            }
        )
    return out


def plot(args: argparse.Namespace) -> None:
    values = _full_cost_values(args)
    values = values[np.isfinite(values) & (values > 0)]
    points = _strategy_points(args)
    if not points:
        raise SystemExit("No strategy points to plot")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    median_cost = float(np.median(values))
    p90_cost = float(np.percentile(values, 90))
    x_values = [point["x"] for point in points if math.isfinite(point["x"]) and point["x"] > 0]
    xmin = min(float(np.min(values)), min(x_values)) * 0.75
    xmax = max(float(np.max(values)), max(x_values)) * 1.35

    fig = plt.figure(figsize=(8.8, 6.2))
    grid = fig.add_gridspec(2, 1, height_ratios=[1.0, 3.1], hspace=0.08)
    ax_hist = fig.add_subplot(grid[0])
    ax = fig.add_subplot(grid[1], sharex=ax_hist)

    bins = np.geomspace(float(np.min(values)), float(np.max(values)), 42)
    ax_hist.hist(values, bins=bins, color="#d0d0d0", edgecolor="#ffffff")
    ax_hist.axvline(median_cost, color="#333333", linewidth=1.0)
    ax_hist.axvline(p90_cost, color="#333333", linewidth=1.0, linestyle="--")
    ax_hist.set_xscale("log")
    ax_hist.set_ylabel("configs")
    ax_hist.set_title(args.title)
    plt.setp(ax_hist.get_xticklabels(), visible=False)

    for axis in (ax_hist, ax):
        axis.axvline(median_cost, color="#333333", linewidth=1.0, alpha=0.75)
        axis.axvline(p90_cost, color="#333333", linewidth=1.0, linestyle="--", alpha=0.75)

    for point in points:
        strategy = point["strategy"]
        color = STRATEGY_COLORS.get(strategy, "#666666")
        x = point["x"]
        y = point["mre"]
        xerr = [[max(0.0, x - point["x_q1"])], [max(0.0, point["x_q3"] - x)]]
        yerr = [[max(0.0, y - point["mre_q1"])], [max(0.0, point["mre_q3"] - y)]]
        show_error = point["runs"] > 1 and all(math.isfinite(v[0]) for v in xerr + yerr)
        if show_error:
            ax.errorbar(
                [x],
                [y],
                xerr=xerr,
                yerr=yerr,
                fmt="o",
                color=color,
                ecolor=color,
                elinewidth=1.0,
                capsize=3,
                markersize=8,
                markeredgecolor="#111111",
                markeredgewidth=0.45,
                zorder=4,
            )
        else:
            ax.scatter([x], [y], s=100, color=color, edgecolors="#111111", linewidths=0.55, zorder=4)
        ax.annotate(
            strategy,
            (x, y),
            xytext=LABEL_OFFSETS.get(strategy, (6, 6)),
            textcoords="offset points",
            fontsize=8,
            color=color,
        )

    by_strategy = {point["strategy"]: point for point in points}
    pairwise = by_strategy.get("pairwise")
    pilot = by_strategy.get("pilotCost")
    if pairwise and pilot:
        ax.text(
            0.98,
            0.78,
            (
                f"fixed {args.level}; error bars: IQR over seeds\n"
                f"pairwise: {100 * pairwise['pct_cost']:.1f}% full cost, MRE={pairwise['mre']:.1f}\n"
                f"pilotCost: {100 * pilot['pct_cost']:.2f}% full cost, MRE={pilot['mre']:.2f}"
            ),
            transform=ax.transAxes,
            ha="right",
            va="top",
            fontsize=8,
            bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.95},
        )

    ax.set_xscale("log")
    ax.set_xlim(xmin, xmax)
    positive_mre = [point["mre"] for point in points if point["mre"] > 0 and math.isfinite(point["mre"])]
    if positive_mre and max(positive_mre) > 5:
        ax.set_yscale("log")
        ax.set_ylim(min(positive_mre) * 0.45, max(positive_mre) * 1.45)
    ax.set_xlabel(f"Mean sampled {args.cost} cost per selected configuration")
    ax.set_ylabel(f"Median MRE predicting {args.target}")
    ax.grid(color="#dddddd", linewidth=0.8, which="both")
    ax.set_axisbelow(True)
    ax.text(
        0.02,
        0.98,
        "solid line: full median cost\n dashed line: full p90 cost",
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=8,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.9},
    )

    fig.tight_layout()
    fig.savefig(output, dpi=220)
    plt.close(fig)
    print(f"Wrote {output}")


def main() -> None:
    plot(parse_args())


if __name__ == "__main__":
    main()
