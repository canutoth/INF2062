#!/usr/bin/env python3
"""Fig 2 right panel, rebuilt: count-cost winner -> measured-cost winner transition
per representative system, under random forest (equal-weight decision). Each row is a
system; the open marker is the count-cost recommendation, the filled marker (colored by
its strategy) is the measured-cost recommendation, at their measured costs (x, log).
PostgreSQL is the tight-cost control (no movement); the others change under measured cost,
with cost-aware pilotCost emerging on several."""
from __future__ import annotations
import csv, os, tempfile
from pathlib import Path
import numpy as np
_c = Path(tempfile.gettempdir()) / "cost_sampling_cache"; (_c / "mpl").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_c / "mpl"))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "artifacts/learner_sensitivity_compact/energy/rf-log"
OUT = ROOT / "607058f5f5131dcd1dbd783d/pic/results/fig2_transitions_rf.png"
COLORS = {"random": "#4C78A8", "balanced": "#F58518", "diversity": "#54A24B",
          "pairwise": "#B279A2", "pilotCost": "#E45756"}
# (label, dir) top->bottom; PostgreSQL control first, then changing ones across the spread
SYSTEMS = [("PostgreSQL", "PostgreSQL_11_2"), ("exastencils", "exastencils"),
           ("brotli", "brotli_1_0_7"), ("7z", "7z"), ("lrzip", "lrzip")]


def mm(a):
    a = np.asarray(a, float); r = max(a.max() - a.min(), 1e-12); return (a - a.min()) / r


def winners(d, lam=1.0):
    rows = [r for r in csv.DictReader(open(BASE / d / "strategy_summary.csv"))
            if r["strategy"] not in ("cheapOracle", "expensiveOracle")]
    sc = [s for s in {r["target_context"] for r in rows} if "cost_performance__target_performance" in s][0]
    rows = [r for r in rows if r["target_context"] == sc]
    strat = [r["strategy"] for r in rows]
    n = np.array([int(float(r["n"])) for r in rows])
    c = np.array([100 * float(r["median_pct_cost"]) for r in rows])
    m = np.array([100 * float(r["median_mre"]) for r in rows])
    ic = int((mm(m) + lam * mm(n)).argmin()); im = int((mm(m) + lam * mm(c)).argmin())
    return (strat[ic], int(n[ic]), c[ic]), (strat[im], int(n[im]), c[im])


def main():
    fig, ax = plt.subplots(figsize=(7.0, 3.6))
    yticks, ylabels = [], []
    for row, (label, d) in enumerate(SYSTEMS):
        y = len(SYSTEMS) - row
        (cs, cn, cc), (ms, mn, mc) = winners(d)
        changed = (cs, cn) != (ms, mn)
        if changed:
            ax.annotate("", xy=(mc, y), xytext=(cc, y),
                        arrowprops={"arrowstyle": "-|>", "color": "#555", "lw": 1.5}, zorder=2)
        ax.scatter([cc], [y], s=70, facecolors="white", edgecolors="#444", linewidths=1.4, zorder=4)
        ax.scatter([mc], [y], s=130, color=COLORS.get(ms, "#444"), edgecolors="#1c1c1c", linewidths=1.4, zorder=5)
        # labels: count-winner (left/grey), cost-winner (right/colored)
        ax.annotate(f"{cs}@{cn}", (cc, y), xytext=(0, 9), textcoords="offset points",
                    ha="center", fontsize=7.5, color="#666", zorder=6)
        ax.annotate(f"{ms}@{mn}" if changed else "(unchanged)", (mc, y), xytext=(0, -15), textcoords="offset points",
                    ha="center", fontsize=7.5, fontweight="bold" if changed else "normal",
                    color=COLORS.get(ms, "#666") if changed else "#999", zorder=6)
        yticks.append(y); ylabels.append(label)
    ax.set_yticks(yticks); ax.set_yticklabels(ylabels, fontsize=9.5)
    ax.set_ylim(0.4, len(SYSTEMS) + 0.7)
    ax.set_xscale("log")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}%"))
    ax.set_xlabel("Measured acquisition cost (% of full campaign, log scale)", fontsize=9.5)
    ax.set_title("Count-cost → measured-cost recommendation (random forest, equal weight)",
                 fontsize=10, fontweight="bold")
    ax.grid(axis="x", color="#e6e6e6", lw=0.7, which="both"); ax.set_axisbelow(True)
    from matplotlib.lines import Line2D
    ax.legend(handles=[Line2D([0], [0], marker="o", color="w", markerfacecolor="white",
                              markeredgecolor="#444", markersize=8, label="count-cost winner"),
                       Line2D([0], [0], marker="o", color="w", markerfacecolor="#888",
                              markeredgecolor="#1c1c1c", markersize=9, label="measured-cost winner")],
              loc="lower right", fontsize=7.5, framealpha=0.95)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=220); plt.close(fig)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
