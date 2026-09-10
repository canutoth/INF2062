#!/usr/bin/env python3
"""Pedagogical 'choice-set flip' figure: one decision-space panel (measured cost vs
MRE) where every strategy-budget design is colored by its membership in the two
efficient menus. The count menu = {both, dropped}; the measured-cost menu =
{both, added}. Jaccard = |both| / |union|. Makes the set flip and the Jaccard the
whole point (vs the old two-panel scatter that showed reordering)."""
from __future__ import annotations
import csv, os, tempfile
from pathlib import Path
import numpy as np
_c = Path(tempfile.gettempdir()) / "cost_sampling_cache"; (_c / "mpl").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_c / "mpl"))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "artifacts/twins_rf_lrzip/strategy_summary.csv"
SCEN = "lrzip__cost_performance__target_energy"
OUT = ROOT / "607058f5f5131dcd1dbd783d/pic/results/choiceset_flip_lrzip.png"


def pareto(x, e):
    k = np.ones(len(x), bool)
    for i in range(len(x)):
        for j in range(len(x)):
            if i != j and x[j] <= x[i] and e[j] <= e[i] and (x[j] < x[i] or e[j] < e[i]):
                k[i] = False; break
    return k


def main():
    rows = [r for r in csv.DictReader(open(SRC))
            if r["target_context"] == SCEN and r["strategy"] not in ("cheapOracle", "expensiveOracle")]
    n = np.array([float(r["n"]) for r in rows])
    cost = np.array([100 * float(r["median_pct_cost"]) for r in rows])
    mre = np.array([float(r["median_mre"]) for r in rows])
    cnt = pareto(n, mre); cst = pareto(cost, mre)
    both = cnt & cst; added = cst & ~cnt; dropped = cnt & ~cst; neither = ~cnt & ~cst
    j = both.sum() / (cnt | cst).sum()

    fig, ax = plt.subplots(figsize=(4.6, 3.7))
    # measured-cost Pareto frontier (the menu a practitioner would compare)
    eff = np.where(cst)[0][np.argsort(cost[cst])]
    ax.plot(cost[eff], mre[eff], color="#9aa0a6", lw=1.3, zorder=2)
    ax.scatter(cost[neither], mre[neither], s=26, color="#d7d9dd", edgecolor="white", lw=0.4, zorder=3)
    ax.scatter(cost[dropped], mre[dropped], s=95, facecolors="none", edgecolors="#4C78A8",
               linewidths=1.8, zorder=6, marker="s")
    ax.scatter(cost[both], mre[both], s=80, color="#54A24B", edgecolor="#1c1c1c", lw=0.7, zorder=5)
    ax.scatter(cost[added], mre[added], s=95, color="#E45756", edgecolor="#1c1c1c", lw=0.7,
               marker="D", zorder=7)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}%"))
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_xlabel("Measured acquisition cost (% of campaign, log)", fontsize=8.5)
    ax.set_ylabel("Median MRE (fraction, log)", fontsize=8.5)
    ax.tick_params(labelsize=7.5)
    ax.set_title("Choice-set flip under measured cost (lrzip)", fontsize=9.5, fontweight="bold")
    ax.grid(color="#ededed", lw=0.6, which="both"); ax.set_axisbelow(True)

    leg = [Line2D([0], [0], marker="o", color="w", markerfacecolor="#54A24B", markeredgecolor="#1c1c1c",
                  markersize=8, label=f"efficient under both ({both.sum()})"),
           Line2D([0], [0], marker="D", color="w", markerfacecolor="#E45756", markeredgecolor="#1c1c1c",
                  markersize=8, label=f"added by measured cost ({added.sum()})"),
           Line2D([0], [0], marker="s", color="w", markerfacecolor="none", markeredgecolor="#4C78A8",
                  markersize=8, markeredgewidth=1.6, label=f"dropped by measured cost ({dropped.sum()})"),
           Line2D([0], [0], marker="o", color="w", markerfacecolor="#d7d9dd", markeredgecolor="white",
                  markersize=7, label=f"dominated in both ({neither.sum()})")]
    ax.legend(handles=leg, loc="lower left", fontsize=7.0, framealpha=0.96, borderpad=0.5,
              handletextpad=0.4)
    ax.text(0.975, 0.95,
            f"count menu: {cnt.sum()}   cost menu: {cst.sum()}\n"
            f"shared: {both.sum()}   Jaccard = {both.sum()}/{(cnt|cst).sum()} = {j:.2f}\n"
            f"the count view discards {added.sum()} cost-efficient designs",
            transform=ax.transAxes, ha="right", va="top", fontsize=7.2,
            bbox={"facecolor": "white", "edgecolor": "#ccc", "alpha": 0.95})
    fig.subplots_adjust(left=0.13, right=0.97, top=0.9, bottom=0.13)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=230); plt.close(fig)
    print(f"Wrote {OUT}")
    print(f"  both={both.sum()} added={added.sum()} dropped={dropped.sum()} neither={neither.sum()} Jaccard={j:.2f}")


if __name__ == "__main__":
    main()
