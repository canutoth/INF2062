#!/usr/bin/env python3
"""Plot selected mechanisms where measured cost changes Pareto decisions."""

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


COLORS = {
    "background": "#B8BDC5",
    "front": "#111111",
    "count": "#E4572E",
    "measured": "#2C7FB8",
}

CASES = [
    {
        "title": "Same sample count, 34x cost gap",
        "subtitle": "brotli: pilot_n8 -> cheap_n8",
        "path": "artifacts/twins_generated_representative_100s/brotli_1_0_7/strategy_summary.csv",
        "target": "brotli__cost_performance__target_performance",
        "cost": "brotli::performance",
        "count_winner": "pilotCost_n8",
        "measured_winner": "cheapOracle_n8",
        "cost_weight": "10",
        "ratio": 34.3,
    },
    {
        "title": "Similar MRE, 15x cost gap",
        "subtitle": "kanzi large: pilot_n8 -> cheap_n8",
        "path": "artifacts/strong_learner_overnight/workload/sk-hgbt-log/kanzi/strategy_summary.csv",
        "target": "kanzi__workload_large__cost_time__target_time",
        "cost": "kanzi__workload_large::time",
        "count_winner": "pilotCost_n8",
        "measured_winner": "cheapOracle_n8",
        "cost_weight": "10",
        "ratio": 14.9,
    },
    {
        "title": "More samples, lower cost",
        "subtitle": "LCBench jasmine: expensive_n8 -> cheap_n16",
        "path": "artifacts/lcbench_data_2k_lw/strategy_summary.csv",
        "target": "lcbench__workload_jasmine__cost_time_total__target_final_val_accuracy",
        "cost": "lcbench__workload_jasmine::time_total",
        "count_winner": "expensiveOracle_n8",
        "measured_winner": "cheapOracle_n16",
        "cost_weight": "10",
        "ratio": 8.3,
    },
    {
        "title": "Same count budget, 3.5x cost gap",
        "subtitle": "lrzip: divDist_t2 -> solver_t2",
        "path": "artifacts/newruns_systems/lrzip/strategy_summary.csv",
        "target": "lrzip",
        "cost": "lrzip",
        "count_winner": "divDistBased_t2",
        "measured_winner": "solverBased_t2",
        "cost_weight": "1",
        "ratio": 3.5,
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        default="607058f5f5131dcd1dbd783d/pic/results/fig_measured_cost_pattern_gallery.png",
    )
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


def _read_rows(case: dict[str, Any]) -> list[dict[str, float | str]]:
    path = REPO_ROOT / str(case["path"])
    rows: list[dict[str, float | str]] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            parsed = {key: _coerce(value) for key, value in row.items()}
            if parsed["target_context"] != case["target"] or parsed["cost_context"] != case["cost"]:
                continue
            rows.append(
                {
                    "label": f"{parsed['strategy']}_{parsed['level']}",
                    "measured_cost": 100.0 * float(parsed["median_pct_cost"]),
                    "mre": 100.0 * float(parsed["median_mre"]),
                }
            )
    if not rows:
        raise SystemExit(f"No rows found for {case['subtitle']}")
    return rows


def _pareto_indices(cost: np.ndarray, error: np.ndarray) -> list[int]:
    front: list[int] = []
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


def _clean_label(label: str) -> str:
    return (
        label.replace("pilotCost", "pilot")
        .replace("cheapOracle", "cheap")
        .replace("expensiveOracle", "expensive")
        .replace("solverBased", "solver")
        .replace("divDistBased", "divDist")
    )


def _case_limits(
    cost: np.ndarray,
    error: np.ndarray,
    front: list[int],
    count_idx: int,
    measured_idx: int,
) -> tuple[tuple[float, float], tuple[float, float], int]:
    important = sorted(set(front + [count_idx, measured_idx]))
    y_values = error[important]
    y_min = max(0.0, float(np.min(y_values)) - max(0.4, 0.18 * float(np.ptp(y_values))))
    y_max = float(np.max(y_values)) + max(0.4, 0.30 * float(np.ptp(y_values)))
    if y_max - y_min < 1.8:
        y_min = max(0.0, y_min - 0.8)
        y_max += 0.8

    x_values = cost[important]
    x_min = max(0.0, float(np.min(x_values)) - max(0.03, 0.08 * float(np.ptp(x_values))))
    x_max = float(np.max(x_values)) + max(0.05, 0.18 * float(np.ptp(x_values)))

    visible = (cost >= x_min) & (cost <= x_max) & (error >= y_min) & (error <= y_max)
    omitted = int(len(cost) - np.sum(visible))
    return (x_min, x_max), (y_min, y_max), omitted


def _label_offset(y: float, y_limits: tuple[float, float], preferred: tuple[int, int]) -> tuple[tuple[int, int], str]:
    y_min, y_max = y_limits
    span = y_max - y_min
    if y < y_min + 0.22 * span:
        return (7, 10), "bottom"
    if y > y_max - 0.18 * span:
        return (7, -12), "top"
    return preferred, "top" if preferred[1] < 0 else "bottom"


def _plot_case(ax: plt.Axes, case: dict[str, Any]) -> None:
    rows = _read_rows(case)
    labels = [str(row["label"]) for row in rows]
    cost = np.array([float(row["measured_cost"]) for row in rows], dtype=float)
    error = np.array([float(row["mre"]) for row in rows], dtype=float)
    front = _pareto_indices(cost, error)
    count_idx = labels.index(str(case["count_winner"]))
    measured_idx = labels.index(str(case["measured_winner"]))
    x_limits, y_limits, omitted = _case_limits(cost, error, front, count_idx, measured_idx)

    visible = (
        (cost >= x_limits[0])
        & (cost <= x_limits[1])
        & (error >= y_limits[0])
        & (error <= y_limits[1])
    )
    ax.scatter(
        cost[visible],
        error[visible],
        s=18,
        color=COLORS["background"],
        edgecolor="white",
        linewidth=0.35,
        alpha=0.72,
        zorder=1,
    )

    front_visible = [idx for idx in front if visible[idx]]
    if len(front_visible) > 1:
        ordered = sorted(front_visible, key=lambda idx: cost[idx])
        ax.plot(cost[ordered], error[ordered], color=COLORS["front"], linewidth=1.0, zorder=2)

    for idx, color, text, preferred in [
        (count_idx, COLORS["count"], f"count: {_clean_label(labels[count_idx])}", (7, -12)),
        (
            measured_idx,
            COLORS["measured"],
            f"measured: {_clean_label(labels[measured_idx])}",
            (7, 10),
        ),
    ]:
        ax.scatter(
            cost[idx],
            error[idx],
            s=50,
            color=color,
            edgecolor="black",
            linewidth=0.9,
            zorder=4,
        )
        offset, va = _label_offset(error[idx], y_limits, preferred)
        ax.annotate(
            text,
            (cost[idx], error[idx]),
            xytext=offset,
            textcoords="offset points",
            fontsize=6.2,
            ha="left",
            va=va,
            bbox={"boxstyle": "round,pad=0.1", "fc": "white", "ec": "none", "alpha": 0.84},
            zorder=5,
        )

    ax.set_xlim(*x_limits)
    ax.set_ylim(*y_limits)
    ax.set_title(
        f"{case['title']}\n{case['subtitle']}; cost weight {case['cost_weight']}; {case['ratio']:.1f}x",
        fontsize=6.9,
    )
    ax.grid(True, color="#E2E2E2", linewidth=0.55)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=6)
    if omitted:
        ax.text(
            0.985,
            0.025,
            f"{omitted} dominated/off-window omitted",
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            fontsize=5.6,
            color="#666666",
        )


def main() -> None:
    args = parse_args()
    fig, axes = plt.subplots(2, 2, figsize=(7.2, 5.15))
    for ax, case in zip(axes.ravel(), CASES):
        _plot_case(ax, case)

    for ax in axes[:, 0]:
        ax.set_ylabel("MRE (%)", fontsize=7)
    for ax in axes[-1, :]:
        ax.set_xlabel("Measured cost (% of full cost)", fontsize=7)

    fig.suptitle("Four mechanisms where measured cost changes the Pareto assessment", fontsize=10, y=0.992)
    fig.subplots_adjust(left=0.07, right=0.995, bottom=0.075, top=0.90, hspace=0.45, wspace=0.13)
    output = REPO_ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=240)
    plt.close(fig)
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
