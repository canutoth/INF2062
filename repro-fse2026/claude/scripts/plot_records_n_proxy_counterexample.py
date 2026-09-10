#!/usr/bin/env python3
"""Plot a run-level fixed-n counterexample from records.csv."""

from __future__ import annotations

import argparse
import csv
import math
import os
from pathlib import Path
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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--records", default="artifacts/twins_generated_representative_100s/jump3r/records.csv")
    parser.add_argument("--cost", default="performance")
    parser.add_argument("--target", default="energy")
    parser.add_argument("--level", default="n128")
    parser.add_argument("--cheap-strategy", default="pilotCost")
    parser.add_argument("--cheap-run", default="62")
    parser.add_argument("--expensive-strategy", default="random")
    parser.add_argument("--expensive-run", default="32")
    parser.add_argument("--label", default="Twins/jump3r")
    parser.add_argument("--title", default="Twins/jump3r: fixed n=128, same MRE, 12.5x cost gap")
    parser.add_argument("--cost-label", default="performance")
    parser.add_argument("--target-label", default="energy")
    parser.add_argument(
        "--output",
        default=(
            "artifacts/paper_figures/twins_jump3r_runlevel_n_proxy_counterexample/"
            "jump3r_fixed_n128_runlevel_cost_gap_performance_cost_energy_target.png"
        ),
    )
    return parser.parse_args()


def _read_csv(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"Missing records table: {path}")
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _float(row: dict[str, Any], key: str) -> float:
    try:
        return float(row[key])
    except (KeyError, TypeError, ValueError):
        return float("nan")


def _run_id(row: dict[str, Any]) -> str:
    value = row.get("run", "")
    try:
        return str(int(float(value)))
    except (TypeError, ValueError):
        return str(value)


def _selected_rows(args: argparse.Namespace) -> list[dict[str, Any]]:
    rows = [
        row
        for row in _read_csv(Path(args.records))
        if row.get("cost_property") == args.cost
        and row.get("target_property") == args.target
        and row.get("level") == args.level
        and row.get("strategy") in STRATEGY_ORDER
        and _float(row, "pct_cost") > 0
        and math.isfinite(_float(row, "mre"))
    ]
    if not rows:
        raise SystemExit(f"No rows found for {args.cost}:{args.target} {args.level} in {args.records}")
    return rows


def _find_run(rows: list[dict[str, Any]], strategy: str, run: str) -> dict[str, Any]:
    for row in rows:
        if row.get("strategy") == strategy and _run_id(row) == str(run):
            return row
    raise SystemExit(f"Could not find {strategy} run {run}")


def _percent_ticks(xmin: float, xmax: float) -> list[float]:
    candidates = [0.01, 0.02, 0.03, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]
    return [value for value in candidates if xmin <= value <= xmax]


def plot(args: argparse.Namespace) -> None:
    rows = _selected_rows(args)
    cheap = _find_run(rows, args.cheap_strategy, args.cheap_run)
    expensive = _find_run(rows, args.expensive_strategy, args.expensive_run)

    cheap_cost = 100 * _float(cheap, "pct_cost")
    expensive_cost = 100 * _float(expensive, "pct_cost")
    cheap_mre = _float(cheap, "mre")
    expensive_mre = _float(expensive, "mre")
    cost_ratio = max(cheap_cost, expensive_cost) / min(cheap_cost, expensive_cost)
    mre_delta = abs(expensive_mre - cheap_mre)
    mre_rel = mre_delta / max(min(abs(cheap_mre), abs(expensive_mre)), 1e-12)
    n_value = args.level[1:] if args.level.startswith("n") else args.level

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9.0, 5.4))
    for strategy in STRATEGY_ORDER:
        strategy_rows = [row for row in rows if row.get("strategy") == strategy]
        if not strategy_rows:
            continue
        xs = [100 * _float(row, "pct_cost") for row in strategy_rows]
        ys = [_float(row, "mre") for row in strategy_rows]
        ax.scatter(
            xs,
            ys,
            s=34 if len(strategy_rows) > 1 else 72,
            color=STRATEGY_COLORS.get(strategy, "#666666"),
            alpha=0.24 if len(strategy_rows) > 1 else 0.75,
            edgecolors="none",
            label=strategy,
            zorder=2,
        )

    for row, label, offset in [
        (cheap, f"{args.cheap_strategy} run {args.cheap_run}", (8, -18)),
        (expensive, f"{args.expensive_strategy} run {args.expensive_run}", (8, 10)),
    ]:
        strategy = row["strategy"]
        x = 100 * _float(row, "pct_cost")
        y = _float(row, "mre")
        ax.scatter(
            [x],
            [y],
            s=150,
            color=STRATEGY_COLORS.get(strategy, "#666666"),
            edgecolors="#111111",
            linewidths=1.2,
            zorder=5,
        )
        ax.annotate(
            label,
            (x, y),
            xytext=offset,
            textcoords="offset points",
            fontsize=9,
            color=STRATEGY_COLORS.get(strategy, "#333333"),
            zorder=6,
        )

    y_arrow = max(cheap_mre, expensive_mre) + 0.055
    ax.annotate(
        "",
        xy=(expensive_cost, y_arrow),
        xytext=(cheap_cost, y_arrow),
        arrowprops={"arrowstyle": "<->", "color": "#333333", "linewidth": 1.4},
    )
    ax.text(
        math.sqrt(cheap_cost * expensive_cost),
        y_arrow + 0.011,
        f"{cost_ratio:.1f}x measured cost\nsame n={n_value}; MRE delta={mre_delta:.4f}",
        ha="center",
        va="bottom",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.95},
    )

    ax.text(
        0.02,
        0.97,
        (
            f"Highlighted runs use the same sample size: n={n_value}.\n"
            f"{args.cheap_strategy} run {args.cheap_run}: cost={cheap_cost:.4f}%, MRE={cheap_mre:.4f}\n"
            f"{args.expensive_strategy} run {args.expensive_run}: cost={expensive_cost:.4f}%, MRE={expensive_mre:.4f}\n"
            f"Relative MRE difference={100 * mre_rel:.1f}%"
        ),
        transform=ax.transAxes,
        ha="left",
        va="top",
        fontsize=9,
        bbox={"facecolor": "white", "edgecolor": "#cccccc", "alpha": 0.95},
    )

    xs_all = [100 * _float(row, "pct_cost") for row in rows]
    ys_all = [_float(row, "mre") for row in rows]
    xmin = min(xs_all) * 0.7
    xmax = max(xs_all) * 1.45
    ax.set_xscale("log")
    ax.set_xlim(xmin, xmax)
    ax.set_xticks(_percent_ticks(xmin, xmax))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda value, _pos: f"{value:g}%"))
    ax.set_ylim(max(0.0, min(ys_all) - 0.035), max(max(ys_all) + 0.055, y_arrow + 0.06))
    ax.set_xlabel(f"Measured sample cost (% of full {args.cost_label} cost, log scale)")
    ax.set_ylabel(f"MRE predicting {args.target_label}")
    ax.set_title(args.title)
    ax.grid(color="#dddddd", linewidth=0.8, which="both")
    ax.set_axisbelow(True)
    ax.legend(frameon=False, ncols=5, fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(output, dpi=220)
    plt.close(fig)
    print(f"Wrote {output}")


def main() -> None:
    plot(parse_args())


if __name__ == "__main__":
    main()
