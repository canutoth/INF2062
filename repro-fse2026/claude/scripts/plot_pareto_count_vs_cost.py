#!/usr/bin/env python3
"""Count-cost vs measured-cost Pareto frontier for one system/scenario, as TWO panels.
Left = sample-count view (n, MRE) with the count-efficient frontier; right = measured-cost
view (cost, MRE) with the cost-efficient frontier. The contrast (a sparse count frontier vs
a rich cost frontier) shows the trade-off space the count view collapses."""
from __future__ import annotations
import argparse, csv, os, tempfile
from pathlib import Path
import numpy as np
_c = Path(tempfile.gettempdir()) / "cost_sampling_cache"; (_c / "mpl").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_c / "mpl"))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from matplotlib.lines import Line2D

ROOT = Path(__file__).resolve().parents[1]
SC_COLORS = {"random": "#4C78A8", "balanced": "#F58518", "diversity": "#54A24B",
             "pairwise": "#B279A2", "pilotCost": "#E45756",
             "solverBased": "#E45756", "distBased": "#54A24B",
             "divDistBased": "#F58518", "henard": "#B279A2"}


def pareto(x, e):
    k = np.ones(len(x), bool)
    for i in range(len(x)):
        for j in range(len(x)):
            if i != j and x[j] <= x[i] and e[j] <= e[i] and (x[j] < x[i] or e[j] < e[i]):
                k[i] = False; break
    return k


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--scenario", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--title", default=None)
    a = ap.parse_args()
    rows = [r for r in csv.DictReader(open(a.source))
            if r["target_context"] == a.scenario and r["strategy"] not in ("cheapOracle", "expensiveOracle")]
    strat = np.array([r["strategy"] for r in rows])
    n = np.array([float(r["n"]) for r in rows])
    cost = np.array([100 * float(r["median_pct_cost"]) for r in rows])
    mre = np.array([100 * float(r["median_mre"]) for r in rows])
    cnt = pareto(n, mre)
    cst = pareto(cost, mre)

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(9.8, 4.3), sharey=True)

    def panel(ax, x, eff, xlabel, subtitle, pct=False):
        ax.scatter(x[~eff], mre[~eff], s=28, color="#CFD3DA", alpha=0.75, edgecolor="white",
                   linewidth=0.4, zorder=2)
        order = np.argsort(x[eff])
        ax.plot(x[eff][order], mre[eff][order], color="#7a8089", lw=1.5, zorder=3)
        for i in np.where(eff)[0]:
            ax.scatter(x[i], mre[i], s=100, color=SC_COLORS.get(strat[i], "#444"),
                       edgecolor="#1c1c1c", linewidth=1.5, zorder=5)
        ax.set_xscale("log")
        if pct:
            ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}%"))
        ax.set_xlabel(xlabel, fontsize=10)
        ax.set_title(subtitle, fontsize=10.5, fontweight="bold", pad=6)
        ax.grid(color="#e6e6e6", lw=0.7, which="both"); ax.set_axisbelow(True)

    panel(axL, n, cnt, "Sample count $n$ (log scale)", f"Count view: {cnt.sum()} efficient designs")
    panel(axR, cost, cst, "Measured cost (% of campaign, log scale)",
          f"Measured-cost view: {cst.sum()} efficient designs", pct=True)
    axL.set_ylabel("Median MRE (%)", fontsize=10)
    axL.text(0.03, 0.04, "lower-left = better", transform=axL.transAxes, fontsize=8, color="#888", style="italic")

    present = [s for s in SC_COLORS if s in set(strat)]
    # de-dup color labels (twins/replication share colors but not names that co-occur)
    seen, leg = set(), []
    for s in present:
        if s in set(strat):
            leg.append(Line2D([0], [0], marker="o", color="w", markerfacecolor=SC_COLORS[s], markersize=8, label=s))
    axR.legend(handles=leg, loc="upper right", fontsize=8, framealpha=0.95)
    if a.title:
        fig.suptitle(a.title, fontsize=11, y=0.99)
    fig.subplots_adjust(left=0.075, right=0.985, top=0.86, bottom=0.135, wspace=0.06)
    Path(a.output).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(a.output, dpi=210); plt.close(fig)
    print(f"Wrote {a.output}  (count-eff {cnt.sum()}, cost-eff {cst.sum()}, "
          f"missed {(cst & ~cnt).sum()}, Jaccard {(cnt & cst).sum() / max((cnt | cst).sum(), 1):.2f})")


if __name__ == "__main__":
    main()
