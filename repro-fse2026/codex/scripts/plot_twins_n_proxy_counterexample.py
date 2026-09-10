#!/usr/bin/env python3
"""Plot a fixed-n counterexample where sample size hides measured cost."""

from __future__ import annotations

import argparse
import csv
import math
import os
from pathlib import Path
import sys
import tempfile
from typing import Any


_cache_root = Path(tempfile.gettempdir()) / "cost_sampling_cache"
(_cache_root / "matplotlib").mkdir(parents=True, exist_ok=True)
(_cache_root / "fontconfig").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_cache_root / "matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(_cache_root / "fontconfig"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


STRATEGY_ORDER = ["random", "balanced", "diversity", "pairwise", "pilotCost"]
STRATEGY_COLORS = {
    "random": "#4C78A8",
    "balanced": "#F58518",
    "diversity": "#54A24B",
    "pairwise": "#B279A2",
    "pilotCost": "#E45756",
}
LABEL_OFFSETS = {
    "random": (6, 8),
    "balanced": (6, -11),
    "diversity": (6, -10),
    "pairwise": (8, 9),
    "pilotCost": (8, 8),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", default="artifacts/twins_generated_representative_100s")
    parser.add_argument("--system-folder", default="lrzip")
    parser.add_argument("--workload", default=None, help="Optional workload filter for aggregate strategy tables.")
    parser.add_argument("--label", default=None, help="Human-readable label for the plot title.")
    parser.add_argument("--title", default=None, help="Optional full plot title.")
    parser.add_argument("--cost-label", default=None, help="Human-readable cost-axis label.")
    parser.add_argument("--target-label", default=None, help="Human-readable target label.")
    parser.add_argument("--compact", action="store_true", help="Use a shorter paper layout.")
    parser.add_argument("--side-panel", action="store_true", help="Use dimensions suitable for a two-panel LaTeX figure.")
    parser.add_argument("--hide-summary-box", action="store_true", help="Do not draw the in-plot numeric summary box.")
    parser.add_argument("--no-title", action="store_true", help="Do not draw an axes title.")
    parser.add_argument("--cost", default="performance")
    parser.add_argument("--target", default="energy")
    parser.add_argument("--level", default="n16")
    parser.add_argument("--cheap-strategy", default="pilotCost")
    parser.add_argument("--expensive-strategy", default="diversity")
    parser.add_argument(
        "--output",
        default=(
            "artifacts/paper_figures/twins_lrzip_n_proxy_counterexample/"
            "lrzip_fixed_n16_empirical_cost_gap_performance_cost_energy_target.png"
        ),
    )
    return parser.parse_args()


def _read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"Missing input table: {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _float(row: dict[str, Any], key: str) -> float:
    try:
        return float(row[key])
    except (KeyError, TypeError, ValueError):
        return float("nan")


def _strategy_rows(args: argparse.Namespace) -> list[dict[str, Any]]:
    path = Path(args.input_dir) / args.system_folder / "strategy_summary.csv"
    rows = [
        row
        for row in _read_csv(path)
        if row.get("cost_property") == args.cost
        and row.get("target_property") == args.target
        and row.get("level") == args.level
        and row.get("strategy") in STRATEGY_ORDER
        and (args.workload is None or row.get("workload") == args.workload)
    ]
    if not rows:
        raise SystemExit(f"No rows found for {args.system_folder} {args.cost}:{args.target} {args.level}")
    return sorted(rows, key=lambda row: STRATEGY_ORDER.index(row["strategy"]))


def _fmt(value: float, digits: int = 3) -> str:
    if not math.isfinite(value):
        return "--"
    return f"{value:.{digits}g}"


def plot(args: argparse.Namespace) -> None:
    rows = _strategy_rows(args)
    by_strategy = {row["strategy"]: row for row in rows}
    cheap = by_strategy.get(args.cheap_strategy)
    expensive = by_strategy.get(args.expensive_strategy)
    if cheap is None or expensive is None:
        raise SystemExit("Counterexample strategies not present in selected rows")

    cheap_cost = 100 * _float(cheap, "median_pct_cost")
    expensive_cost = 100 * _float(expensive, "median_pct_cost")
    cheap_mre = _float(cheap, "median_mre")
    expensive_mre = _float(expensive, "median_mre")
    cost_ratio = expensive_cost / cheap_cost
    mre_delta = abs(expensive_mre - cheap_mre)
    mre_rel = mre_delta / max(min(abs(cheap_mre), abs(expensive_mre)), 1e-12)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    label = args.label or args.workload or args.system_folder.rstrip("/.")

    if args.side_panel:
        figsize = (4.9, 3.45)
        label_font = 8
        tick_font = 7
        annotation_font = 7
        marker_scale = 0.62
    else:
        figsize = (9.0, 4.35 if args.compact else 5.4)
        label_font = 11
        tick_font = 10
        annotation_font = 9
        marker_scale = 1.0

    fig, ax = plt.subplots(figsize=figsize)
    for row in rows:
        strategy = row["strategy"]
        x = 100 * _float(row, "median_pct_cost")
        y = _float(row, "median_mre")
        marker_size = (110 if strategy in {args.cheap_strategy, args.expensive_strategy} else 80) * marker_scale
        edge_width = 1.4 if strategy in {args.cheap_strategy, args.expensive_strategy} else 0.6
        ax.scatter(
            [x],
            [y],
            s=marker_size,
            color=STRATEGY_COLORS.get(strategy, "#666666"),
            edgecolors="#111111",
            linewidths=edge_width,
            zorder=4,
        )
        ax.annotate(
            strategy,
            (x, y),
            xytext=LABEL_OFFSETS.get(strategy, (7, 6)),
            textcoords="offset points",
            fontsize=annotation_font,
            color=STRATEGY_COLORS.get(strategy, "#333333"),
            zorder=5,
        )

    n_value = args.level[1:] if args.level.startswith("n") else args.level
    ys_for_layout = [_float(row, "median_mre") for row in rows if math.isfinite(_float(row, "median_mre"))]
    y_span = max(ys_for_layout) - min(ys_for_layout) if ys_for_layout else 0.0
    y_arrow = max(cheap_mre, expensive_mre) + max(0.02, 0.35 * y_span)
    ax.annotate(
        "",
        xy=(expensive_cost, y_arrow),
        xytext=(cheap_cost, y_arrow),
        arrowprops={"arrowstyle": "<->", "color": "#333333", "linewidth": 1.4},
    )
    ax.text(
        math.sqrt(cheap_cost * expensive_cost),
        y_arrow + 0.018,
        f"{cost_ratio:.1f}x measured cost\nsame n={n_value}; MRE delta={mre_delta:.4f}",
        ha="center",
        va="bottom",
        fontsize=annotation_font,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.95},
    )

    if not args.hide_summary_box:
        ax.text(
            0.02,
            0.97,
            (
                f"All points use the same sample size: n={n_value}.\n"
                f"{args.cheap_strategy}: cost={cheap_cost:.4f}%, MRE={cheap_mre:.3f}\n"
                f"{args.expensive_strategy}: cost={expensive_cost:.4f}%, MRE={expensive_mre:.3f}\n"
                f"Relative MRE difference={100 * mre_rel:.1f}%"
            ),
            transform=ax.transAxes,
            ha="left",
            va="top",
            fontsize=annotation_font,
            bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.95},
        )

    ax.set_xscale("log")
    xs = [100 * _float(row, "median_pct_cost") for row in rows if _float(row, "median_pct_cost") > 0]
    ys = ys_for_layout
    xmin = min(xs) * 0.55
    xmax = max(xs) * 1.75
    ax.set_xlim(xmin, xmax)
    tick_candidates = [0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.5, 1.0]
    ax.set_xticks([value for value in tick_candidates if xmin <= value <= xmax])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _pos: f"{value:g}%"))
    bottom_pad = max(0.01, 0.45 * (y_span or max(ys)))
    top_pad = max(0.025, 0.55 * (y_span or max(ys)))
    ax.set_ylim(max(0.0, min(ys) - bottom_pad), y_arrow + top_pad)
    cost_label = args.cost_label or args.cost
    target_label = args.target_label or args.target
    if args.side_panel:
        ax.set_xlabel(f"Measured cost (% full {cost_label}, log scale)", fontsize=label_font)
        ax.set_ylabel(f"Median MRE ({target_label})", fontsize=label_font)
    else:
        ax.set_xlabel(f"Median measured cost (% of full {cost_label} cost, log scale)", fontsize=label_font)
        ax.set_ylabel(f"Median MRE predicting {target_label}", fontsize=label_font)
    ax.tick_params(axis="both", labelsize=tick_font)
    if not args.no_title:
        ax.set_title(args.title or f"{label}: fixed n={n_value}, similar MRE, different measured cost")
    ax.grid(color="#dddddd", linewidth=0.8, which="both")
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(output, dpi=220)
    plt.close(fig)

    print(f"Wrote {output}")


def main() -> None:
    plot(parse_args())


if __name__ == "__main__":
    main()
