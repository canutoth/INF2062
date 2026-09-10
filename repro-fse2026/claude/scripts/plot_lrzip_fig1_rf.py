#!/usr/bin/env python3
"""Reframed Figure-1 running-example panel under RF (random forest).
lrzip 0.631, fixed n=16, predict energy / pay runtime cost. Under a strong learner
the cost-aware sampler pilotCost is BOTH the cheapest AND the most accurate — it
strictly dominates every other strategy. Folds the old Fig-2 strict-win into Fig 1."""
from __future__ import annotations
import csv, os, tempfile
from pathlib import Path
_c = Path(tempfile.gettempdir()) / "cost_sampling_cache"; (_c / "mpl").mkdir(parents=True, exist_ok=True)
os.environ.setdefault("MPLCONFIGDIR", str(_c / "mpl"))
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "artifacts/twins_rf_lrzip/strategy_summary.csv"
OUT = ROOT / "607058f5f5131dcd1dbd783d/pic/results/lrzip_fig1_rf_strictwin.png"
SCEN, LEVEL = "lrzip__cost_performance__target_energy", 16
COLORS = {"random": "#4C78A8", "balanced": "#F58518", "diversity": "#54A24B",
          "pairwise": "#B279A2", "pilotCost": "#E45756"}
OFF = {"random": (8, 6), "balanced": (8, -12), "diversity": (9, 4),
       "pairwise": (8, -12), "pilotCost": (10, 4)}


def main():
    pts = {}
    for r in csv.DictReader(SRC.open()):
        if r["target_context"] == SCEN and int(float(r["n"])) == LEVEL and r["strategy"] in COLORS:
            pts[r["strategy"]] = (100 * float(r["median_pct_cost"]), float(r["median_mre"]))
    pc, dv = pts["pilotCost"], pts["diversity"]
    ratio = dv[0] / pc[0]

    fig, ax = plt.subplots(figsize=(5.2, 3.7))
    for s, (x, y) in pts.items():
        win = s == "pilotCost"
        ax.scatter([x], [y], s=170 if win else 95, color=COLORS[s], edgecolors="#111",
                   linewidths=1.6 if win else 0.7, zorder=5)
        ax.annotate(s, (x, y), xytext=OFF.get(s, (7, 6)), textcoords="offset points",
                    fontsize=9, fontweight="bold" if win else "normal", color=COLORS[s], zorder=6)
    # (clean scatter: no arrows, no claim boxes — the reading lives in the caption/text)
    ax.set_xscale("log")
    xs = [x for x, _ in pts.values()]
    ax.set_xlim(min(xs) * 0.5, max(xs) * 1.9)
    ax.set_xticks([0.03, 0.05, 0.1, 0.2, 0.5])
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}%"))
    ys = [y for _, y in pts.values()]
    ax.set_ylim(min(ys) - 0.05, max(ys) + 0.08)
    ax.set_xlabel("Measured cost (% of full runtime campaign, log scale)", fontsize=9.5)
    ax.set_ylabel("Median MRE predicting energy (fraction)", fontsize=9.5)
    ax.set_title("lrzip 0.631, $n{=}16$, predicting energy (random forest)",
                 fontsize=10.5, fontweight="bold")
    ax.grid(color="#dddddd", linewidth=0.8, which="both"); ax.set_axisbelow(True)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=220); plt.close(fig)
    print(f"Wrote {OUT}")
    print(f"pilotCost cost={pc[0]:.3f}% MRE={pc[1]:.2f}  |  diversity cost={dv[0]:.3f}% MRE={dv[1]:.2f}  ({ratio:.1f}x)")


if __name__ == "__main__":
    main()
