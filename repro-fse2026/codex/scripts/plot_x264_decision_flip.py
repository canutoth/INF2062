#!/usr/bin/env python3
"""Plot a focused x264 Pareto view explaining a count/measured-cost flip."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import sys
from typing import Any

import numpy as np


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset

plt.rcParams.update(
    {
        "font.size": 8,
        "axes.titlesize": 9,
        "axes.labelsize": 8,
        "xtick.labelsize": 7,
        "ytick.labelsize": 7,
    }
)


DEFAULT_SELECTION = ["henard_t1", "solverBased_t1", "random_t1", "divDistBased_t1"]
DISPLAY_LABELS = {
    "henard_t1": "Henard\nt1",
    "solverBased_t1": "Solver\nt1",
    "random_t1": "Random\nt1",
    "divDistBased_t1": "Diversity\nt1",
}
COLORS = {
    "henard_t1": "#4C78A8",
    "solverBased_t1": "#F58518",
    "random_t1": "#54A24B",
    "divDistBased_t1": "#B279A2",
    "background": "#B8BDC5",
    "front": "#111111",
}
LABEL_OFFSETS = {
    "henard_t1": (7, 11),
    "solverBased_t1": (8, -13),
    "random_t1": (8, -3),
    "divDistBased_t1": (8, 11),
}
ZOOM_PAIR = ("henard_t1", "solverBased_t1")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="artifacts/x264_matrix/strategy_summary.csv")
    parser.add_argument("--output", default="artifacts/x264_matrix/fig_x264_decision_flip_time_size.png")
    parser.add_argument("--scenario", default="cost_time__target_size")
    parser.add_argument("--context", default="x264_size_14")
    parser.add_argument("--lambda-value", type=float, default=10.0)
    parser.add_argument("--selection", default=",".join(DEFAULT_SELECTION))
    return parser.parse_args()


def _coerce(value: str) -> Any:
    if value == "":
        return None
    try:
        if any(char in value for char in ".eE"):
            return float(value)
        return int(value)
    except ValueError:
        return value


def _read_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return [{key: _coerce(value) for key, value in row.items()} for row in csv.DictReader(handle)]


def _display_context(context: str) -> str:
    prefix = "x264_size_"
    if context.startswith(prefix):
        return f"x264 input {context[len(prefix):]}"
    return context.replace("_", " ")


def _pareto_indices(cost: np.ndarray, error: np.ndarray) -> list[int]:
    front = []
    for i in range(len(cost)):
        dominated = False
        for j in range(len(cost)):
            if i == j:
                continue
            no_worse = cost[j] <= cost[i] and error[j] <= error[i]
            strictly_better = cost[j] < cost[i] or error[j] < error[i]
            if no_worse and strictly_better:
                dominated = True
                break
        if not dominated:
            front.append(i)
    return front


def _plot_panel(
    ax: plt.Axes,
    cost: np.ndarray,
    error: np.ndarray,
    labels: list[str],
    selected: list[str],
    title: str,
    xlabel: str,
) -> None:
    front = _pareto_indices(cost, error)
    front_set = set(front)
    selected_set = set(selected)
    selected_indices = [idx for idx, label in enumerate(labels) if label in selected_set]
    background_indices = [idx for idx, label in enumerate(labels) if label not in selected_set]

    ax.scatter(
        cost[background_indices],
        error[background_indices],
        s=32,
        color=COLORS["background"],
        edgecolor="white",
        linewidth=0.5,
        alpha=0.72,
        zorder=1,
    )

    if len(front) > 1:
        ordered = sorted(front, key=lambda idx: cost[idx])
        ax.plot(
            cost[ordered],
            error[ordered],
            color=COLORS["front"],
            linewidth=1.2,
            zorder=2,
        )

    for pos in selected_indices:
        label = labels[pos]
        on_front = pos in front_set
        ax.scatter(
            cost[pos],
            error[pos],
            s=78 if on_front else 58,
            color=COLORS.get(label, "#666666"),
            edgecolor=COLORS["front"] if on_front else "white",
            linewidth=1.4 if on_front else 0.8,
            zorder=3,
        )
        ax.annotate(
            DISPLAY_LABELS.get(label, label.replace("_", "\n")).replace("\n", " "),
            (cost[pos], error[pos]),
            xytext=LABEL_OFFSETS.get(label, (5, 4)),
            textcoords="offset points",
            fontsize=7,
            ha="left",
            va="center",
            bbox={"boxstyle": "round,pad=0.12", "fc": "white", "ec": "none", "alpha": 0.78},
        )

    x_span = float(np.max(cost) - np.min(cost))
    x_pad = 0.18 if x_span == 0 else max(0.06, 0.28 * x_span)
    y_span = float(np.max(error) - np.min(error))
    y_pad = max(0.12, 0.14 * y_span)
    ax.set_xlim(float(np.min(cost)) - x_pad, float(np.max(cost)) + x_pad)
    ax.set_ylim(float(np.min(error)) - y_pad, float(np.max(error)) + y_pad)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.grid(True, color="#E2E2E2", linewidth=0.8)
    ax.set_axisbelow(True)
    _add_pair_zoom(ax, cost, error, labels, front_set)


def _add_pair_zoom(
    ax: plt.Axes,
    cost: np.ndarray,
    error: np.ndarray,
    labels: list[str],
    front_set: set[int],
) -> None:
    pair_indices = [labels.index(label) for label in ZOOM_PAIR if label in labels]
    if len(pair_indices) != len(ZOOM_PAIR):
        return

    x_values = cost[pair_indices]
    y_values = error[pair_indices]
    x_span = float(np.max(x_values) - np.min(x_values))
    x_pad = 0.2 if x_span == 0 else max(0.24, 0.55 * x_span)
    y_pad = 0.16
    xlim = (float(np.min(x_values) - x_pad), float(np.max(x_values) + x_pad))
    ylim = (float(np.min(y_values) - y_pad), float(np.max(y_values) + y_pad))

    axins = inset_axes(ax, width="43%", height="40%", loc="upper right", borderpad=0.8)
    visible = [
        idx
        for idx in range(len(labels))
        if xlim[0] <= cost[idx] <= xlim[1] and ylim[0] <= error[idx] <= ylim[1]
    ]
    background = [idx for idx in visible if idx not in pair_indices]
    if background:
        axins.scatter(
            cost[background],
            error[background],
            s=14,
            color=COLORS["background"],
            edgecolor="white",
            linewidth=0.4,
            alpha=0.7,
            zorder=1,
        )

    pair_front = [idx for idx in pair_indices if idx in front_set]
    if len(pair_front) == 2:
        ordered = sorted(pair_front, key=lambda idx: cost[idx])
        axins.plot(cost[ordered], error[ordered], color=COLORS["front"], linewidth=0.9, zorder=2)

    for idx in pair_indices:
        label = labels[idx]
        on_front = idx in front_set
        axins.scatter(
            cost[idx],
            error[idx],
            s=42,
            color=COLORS.get(label, "#666666"),
            edgecolor=COLORS["front"] if on_front else "#777777",
            linewidth=1.0 if on_front else 0.6,
            zorder=3,
        )

    henard_idx, solver_idx = pair_indices
    axins.annotate(
        "Henard t1",
        (cost[henard_idx], error[henard_idx]),
        xytext=(4, 7),
        textcoords="offset points",
        fontsize=5.6,
        ha="left",
        va="bottom",
        bbox={"boxstyle": "round,pad=0.08", "fc": "white", "ec": "none", "alpha": 0.82},
    )
    axins.annotate(
        "Solver t1",
        (cost[solver_idx], error[solver_idx]),
        xytext=(4, -8),
        textcoords="offset points",
        fontsize=5.6,
        ha="left",
        va="top",
        bbox={"boxstyle": "round,pad=0.08", "fc": "white", "ec": "none", "alpha": 0.82},
    )

    axins.set_xlim(*xlim)
    axins.set_ylim(*ylim)
    axins.set_title("Henard/Solver zoom", fontsize=6, pad=1.5)
    axins.grid(True, color="#E6E6E6", linewidth=0.5)
    axins.tick_params(labelsize=5, length=2, pad=1)
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="#6F6F6F", linewidth=0.6)


def main() -> None:
    args = parse_args()
    rows = [
        row
        for row in _read_rows(Path(args.input))
        if row.get("scenario") == args.scenario and row.get("target_context") == args.context
    ]
    if not rows:
        raise SystemExit(f"No rows found for scenario={args.scenario} context={args.context}")

    labels = [f"{row['strategy']}_{row['level']}" for row in rows]
    selected = [label.strip() for label in args.selection.split(",") if label.strip()]
    missing = [label for label in selected if label not in labels]
    if missing:
        raise SystemExit(f"Missing selected labels: {', '.join(missing)}")

    mre = np.array([float(row["median_mre"]) for row in rows], dtype=float)
    count_cost = np.array([float(row["pct_n"]) for row in rows], dtype=float)
    measured_cost = np.array([float(row["median_pct_cost"]) for row in rows], dtype=float)
    all_mre = 100 * mre
    all_count = 100 * count_cost
    all_measured = 100 * measured_cost

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.1), sharey=True)
    _plot_panel(
        axes[0],
        all_count,
        all_mre,
        labels,
        selected,
        "Count cost view\nSolver dominates labelled t1 choices",
        "Count cost (% configurations)",
    )
    _plot_panel(
        axes[1],
        all_measured,
        all_mre,
        labels,
        selected,
        "Measured cost view\nHenard and Solver trade off",
        "Measured time cost (% full time)",
    )
    axes[0].set_ylabel("MRE (%)")
    fig.suptitle(
        f"{_display_context(args.context)}, cost=time, target=size; four labelled t1 choices in full local context",
        y=0.985,
        fontsize=10,
    )
    fig.subplots_adjust(left=0.075, right=0.99, bottom=0.17, top=0.76, wspace=0.06)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220)
    plt.close(fig)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
