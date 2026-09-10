#!/usr/bin/env python3
"""Plot strategy trajectories with the full cost distribution above them."""

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


STRATEGY_ORDER = ["pilotCost", "random", "balanced", "diversity", "pairwise"]
STRATEGY_COLORS = {
    "random": "#4C78A8",
    "balanced": "#F58518",
    "diversity": "#54A24B",
    "pairwise": "#B279A2",
    "pilotCost": "#E45756",
}
LABEL_OFFSETS = {
    "pilotCost": (6, 4),
    "random": (6, 4),
    "balanced": (6, -11),
    "diversity": (6, 6),
    "pairwise": (6, 6),
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
    parser.add_argument(
        "--title",
        default="brotli 1.0.7: strategy trajectories and performance-cost distribution",
    )
    parser.add_argument(
        "--output",
        default=(
            "artifacts/paper_figures/twins_brotli_pairwise_n8/"
            "brotli_trajectory_with_performance_distribution_deployable.png"
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


def _level_n(level: str) -> int:
    return int(level[1:]) if level.startswith("n") and level[1:].isdigit() else 0


def _full_cost_values(args: argparse.Namespace) -> np.ndarray:
    where = parse_where([args.where]) if args.where else {}
    table = load_twins_table(args.zip, args.system, where=where)
    return np.asarray([float(row[args.cost]) for row in table.rows], dtype=float)


def _strategy_level_points(args: argparse.Namespace) -> list[dict[str, Any]]:
    summary_path = Path(args.input_dir) / args.system_folder / "strategy_summary.csv"
    rows = [
        row
        for row in _read_csv(summary_path)
        if row.get("cost_property") == args.cost
        and row.get("target_property") == args.target
        and row.get("strategy") in STRATEGY_ORDER
    ]
    points: list[dict[str, Any]] = []
    for row in rows:
        n = max(_float(row, "n"), 1.0)
        points.append(
            {
                "strategy": row["strategy"],
                "level": row["level"],
                "n": int(n),
                "x": _float(row, "median_train_cost") / n,
                "x_q1": _float(row, "q1_train_cost") / n,
                "x_q3": _float(row, "q3_train_cost") / n,
                "pct_cost": _float(row, "median_pct_cost"),
                "mre": _float(row, "median_mre"),
                "mre_q1": _float(row, "q1_mre"),
                "mre_q3": _float(row, "q3_mre"),
                "ratio": _float(row, "median_calibration_ratio"),
                "runs": int(float(row.get("runs", 0) or 0)),
            }
        )
    return sorted(
        points,
        key=lambda row: (
            STRATEGY_ORDER.index(row["strategy"]),
            _level_n(str(row["level"])),
        ),
    )


def _finite(values: list[float]) -> list[float]:
    return [value for value in values if math.isfinite(value)]


def _plot_errorbar(ax: plt.Axes, point: dict[str, Any], color: str, size: float) -> None:
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
            elinewidth=0.9,
            capsize=2.5,
            markersize=math.sqrt(size),
            markeredgecolor="#111111",
            markeredgewidth=0.45,
            alpha=0.95,
            zorder=4,
        )
    else:
        ax.scatter(
            [x],
            [y],
            s=size,
            color=color,
            edgecolors="#111111",
            linewidths=0.55,
            alpha=0.95,
            zorder=4,
        )


def plot(args: argparse.Namespace) -> None:
    values = _full_cost_values(args)
    values = values[np.isfinite(values) & (values > 0)]
    points = _strategy_level_points(args)
    if values.size == 0 or not points:
        raise SystemExit("No cost values or strategy points to plot")

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    median_cost = float(np.median(values))
    p90_cost = float(np.percentile(values, 90))
    x_values = [point["x"] for point in points if math.isfinite(point["x"]) and point["x"] > 0]
    xmin = min(float(np.min(values)), min(x_values)) * 0.75
    xmax = max(float(np.max(values)), max(x_values)) * 1.35

    fig = plt.figure(figsize=(9.2, 6.6))
    grid = fig.add_gridspec(2, 1, height_ratios=[1.0, 3.4], hspace=0.08)
    ax_hist = fig.add_subplot(grid[0])
    ax = fig.add_subplot(grid[1], sharex=ax_hist)

    bins = np.geomspace(float(np.min(values)), float(np.max(values)), 42)
    ax_hist.hist(values, bins=bins, color="#d0d0d0", edgecolor="#ffffff")
    ax_hist.set_xscale("log")
    ax_hist.set_ylabel("configs")
    ax_hist.set_title(args.title)
    plt.setp(ax_hist.get_xticklabels(), visible=False)

    for axis in (ax_hist, ax):
        axis.axvline(median_cost, color="#333333", linewidth=1.0, alpha=0.75)
        axis.axvline(p90_cost, color="#333333", linewidth=1.0, linestyle="--", alpha=0.75)

    for strategy in STRATEGY_ORDER:
        items = [
            point
            for point in points
            if point["strategy"] == strategy
            and math.isfinite(point["x"])
            and point["x"] > 0
            and math.isfinite(point["mre"])
            and point["mre"] > 0
        ]
        if not items:
            continue
        color = STRATEGY_COLORS.get(strategy, "#666666")
        xs = [point["x"] for point in items]
        ys = [point["mre"] for point in items]
        ax.plot(xs, ys, color=color, alpha=0.65, linewidth=1.7, zorder=2)
        for point in items:
            size = 34 + 1.7 * min(point["n"], 64)
            _plot_errorbar(ax, point, color, size)
        if strategy == "pairwise":
            for point in (items[0], items[-1]):
                ax.annotate(
                    point["level"],
                    (point["x"], point["mre"]),
                    xytext=LABEL_OFFSETS.get(strategy, (6, 4)),
                    textcoords="offset points",
                    fontsize=8,
                    color=color,
                )
            ax.annotate(
                strategy,
                (items[-1]["x"], items[-1]["mre"]),
                xytext=(8, -2),
                textcoords="offset points",
                fontsize=8,
                color=color,
                va="center",
            )

    by_strategy = {point["strategy"]: [] for point in points}
    for point in points:
        by_strategy.setdefault(point["strategy"], []).append(point)
    pairwise = sorted(by_strategy.get("pairwise", []), key=lambda row: row["n"])
    pilot = sorted(by_strategy.get("pilotCost", []), key=lambda row: row["n"])
    if pairwise and pilot:
        pair_first = pairwise[0]
        pair_last = pairwise[-1]
        pilot_first = pilot[0]
        ax.text(
            0.02,
            0.98,
            (
                "lines connect increasing n; marker size grows with n\n"
                "solid/dashed vertical lines: full median/p90 per-config cost\n"
                f"pairwise {pair_first['level']}: {100 * pair_first['pct_cost']:.1f}% full cost, "
                f"MRE={pair_first['mre']:.1f}\n"
                f"pairwise {pair_last['level']}: {100 * pair_last['pct_cost']:.1f}% full cost, "
                f"MRE={pair_last['mre']:.2f}\n"
                f"pilotCost {pilot_first['level']}: {100 * pilot_first['pct_cost']:.2f}% full cost, "
                f"MRE={pilot_first['mre']:.2f}"
            ),
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=7.5,
            bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.94},
        )

    ax.set_xscale("log")
    ax.set_xlim(xmin, xmax)
    positive_mre = _finite([point["mre"] for point in points if point["mre"] > 0])
    if positive_mre and max(positive_mre) > 5:
        ax.set_yscale("log")
        ax.set_ylim(min(positive_mre) * 0.45, max(positive_mre) * 1.55)
    ax.set_xlabel(f"Median sampled {args.cost} cost per selected configuration")
    ax.set_ylabel(f"Median MRE predicting {args.target}")
    ax.grid(color="#dddddd", linewidth=0.8, which="both")
    ax.set_axisbelow(True)
    ax.legend(
        handles=[
            plt.Line2D([0], [0], color=STRATEGY_COLORS[strategy], marker="o", label=strategy)
            for strategy in STRATEGY_ORDER
        ],
        frameon=False,
        fontsize=8,
        ncols=5,
        loc="lower center",
        bbox_to_anchor=(0.5, -0.28),
    )

    fig.tight_layout()
    fig.savefig(output, dpi=220, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {output}")


def main() -> None:
    plot(parse_args())


if __name__ == "__main__":
    main()
