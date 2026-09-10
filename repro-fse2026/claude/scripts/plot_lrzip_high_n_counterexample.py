#!/usr/bin/env python3
"""Plot an lrzip case where larger n is cheaper under measured cost."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "artifacts/twins_generated_representative_100s/lrzip/strategy_summary.csv"
OUTPUT = (
    ROOT
    / "607058f5f5131dcd1dbd783d/pic/results/lrzip_high_n_cheaper_counterexample.png"
)
TARGET = "lrzip__cost_performance__target_performance"
COST_CONTEXT = "lrzip::performance"
ORACLES = {"cheapOracle", "expensiveOracle"}


def clean(strategy: str) -> str:
    return (
        strategy.replace("pilotCost", "pilot")
        .replace("solverBased", "solver")
        .replace("divDistBased", "divDist")
        .replace("distBased", "dist")
    )


def read_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        for raw in csv.DictReader(handle):
            if raw["target_context"] != TARGET or raw["cost_context"] != COST_CONTEXT:
                continue
            if raw["strategy"] in ORACLES:
                continue
            rows.append(
                {
                    "strategy": clean(raw["strategy"]),
                    "label": f"{clean(raw['strategy'])}_{raw['level']}",
                    "n": int(float(raw["n"])),
                    "mre": 100.0 * float(raw["median_mre"]),
                    "cost": 100.0 * float(raw["median_pct_cost"]),
                }
            )
    if not rows:
        raise SystemExit(f"No rows found in {SOURCE}")
    return rows


def row_by_label(rows: list[dict[str, object]], label: str) -> dict[str, object]:
    for row in rows:
        if row["label"] == label:
            return row
    raise SystemExit(f"Missing row {label}")


def draw_panel(
    ax: plt.Axes,
    rows: list[dict[str, object]],
    x_key: str,
    x_label: str,
    title: str,
    selected: tuple[dict[str, object], dict[str, object]],
) -> None:
    for row in rows:
        ax.scatter(
            float(row[x_key]),
            float(row["mre"]),
            s=28,
            color="#B8BDC5",
            alpha=0.68,
            edgecolor="white",
            linewidth=0.45,
            zorder=2,
        )
    low_n, high_n = selected
    ax.scatter(
        float(low_n[x_key]),
        float(low_n["mre"]),
        s=110,
        color="#E4572E",
        edgecolor="black",
        linewidth=0.9,
        zorder=5,
    )
    ax.scatter(
        float(high_n[x_key]),
        float(high_n["mre"]),
        s=120,
        marker="s",
        color="#2C7FB8",
        edgecolor="black",
        linewidth=0.9,
        zorder=6,
    )
    ax.annotate(
        "",
        xy=(float(high_n[x_key]), float(high_n["mre"])),
        xytext=(float(low_n[x_key]), float(low_n["mre"])),
        arrowprops={"arrowstyle": "->", "color": "#555555", "lw": 1.15},
        zorder=4,
    )
    ax.annotate(
        "diversity\n$n=128$",
        xy=(float(low_n[x_key]), float(low_n["mre"])),
        xytext=(-8, 10),
        textcoords="offset points",
        ha="right",
        va="bottom",
        fontsize=8.5,
        color="#7A2414",
        zorder=7,
    )
    ax.annotate(
        "pilotCost\n$n=256$",
        xy=(float(high_n[x_key]), float(high_n["mre"])),
        xytext=(-8, -8) if x_key == "n" else (8, -8),
        textcoords="offset points",
        ha="right" if x_key == "n" else "left",
        va="top",
        fontsize=8.5,
        color="#174C72",
        zorder=7,
    )
    ax.set_title(title, fontsize=10.5, fontweight="bold", pad=7)
    ax.set_xlabel(x_label)
    ax.set_ylabel("MRE (%)")
    ax.grid(True, color="#E3E3E3", linewidth=0.65)
    ax.set_axisbelow(True)


def main() -> None:
    rows = read_rows()
    low_n = row_by_label(rows, "diversity_n128")
    high_n = row_by_label(rows, "pilot_n256")

    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.45), sharey=True)
    draw_panel(
        axes[0],
        rows,
        "n",
        "Sample count $n$",
        "Sampling size (count)",
        (low_n, high_n),
    )
    draw_panel(
        axes[1],
        rows,
        "cost",
        "Measured cost (% of full campaign)",
        "Sampling cost",
        (low_n, high_n),
    )
    axes[1].set_ylabel("")
    axes[0].set_xlim(0, 275)
    axes[1].set_xlim(0, 5.8)
    axes[0].set_ylim(36, 68)

    fig.subplots_adjust(left=0.085, right=0.99, top=0.90, bottom=0.17, wspace=0.10)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT, dpi=220)
    plt.close(fig)
    print(OUTPUT)

    # Standalone single-panel "Sampling cost" view (the only panel the paper
    # keeps: the count axis is redundant because the n's are printed on the
    # two highlighted points).
    fig_single, ax_single = plt.subplots(figsize=(4.9, 3.55))
    draw_panel(
        ax_single,
        rows,
        "cost",
        "Measured cost (% of full campaign)",
        "Sampling cost (target = performance)",
        (low_n, high_n),
    )
    ax_single.set_xlim(0, 5.8)
    ax_single.set_ylim(36, 68)
    fig_single.subplots_adjust(left=0.155, right=0.97, top=0.90, bottom=0.155)
    single_output = OUTPUT.parent / "lrzip_high_n_cost_only.png"
    fig_single.savefig(single_output, dpi=220)
    plt.close(fig_single)
    print(single_output)


if __name__ == "__main__":
    main()
