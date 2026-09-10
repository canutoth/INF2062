#!/usr/bin/env python3
"""RF version of the brotli fixed-n=8 distribution figure (does NOT override the
ridge figure). Top: per-configuration performance-cost distribution as a box from
the rq1 quantiles (the raw twins measurements are no longer on disk, so we draw the
quartiles+range rather than a full histogram). Bottom: each sampling strategy placed
at its mean sampled per-config cost (x, log) vs its energy-prediction MRE (y, log),
under random forest. Shows that pairwise lands near the expensive end of the cost
distribution (≈expensiveOracle) and is far worse at MRE, while pilotCost stays cheap
and accurate."""
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
REC = ROOT / "artifacts/learner_sensitivity_compact/energy/rf-log/brotli_1_0_7/records.csv"
RQ1 = ROOT / "artifacts/learner_sensitivity_compact/energy/rf-log/brotli_1_0_7/rq1_cost_heterogeneity.csv"
OUT = ROOT / "607058f5f5131dcd1dbd783d/pic/results/twins_brotli_fixed_n8_with_distribution_RF.png"
COLORS = {"random": "#4C78A8", "balanced": "#F58518", "diversity": "#54A24B",
          "pairwise": "#B279A2", "pilotCost": "#E45756",
          "cheapOracle": "#9aa0a6", "expensiveOracle": "#9aa0a6"}
ORDER = ["cheapOracle", "balanced", "pilotCost", "random", "diversity", "pairwise", "expensiveOracle"]


def strat_points():
    rows = [r for r in csv.DictReader(open(REC))
            if r.get("cost_property") == "performance" and r.get("target_property") == "energy"
            and r["level"] == "n8"]
    out = {}
    for s in ORDER:
        rr = [r for r in rows if r["strategy"] == s]
        if not rr:
            continue
        mpc = [float(r["train_cost"]) / max(float(r["n"]), 1) for r in rr]
        out[s] = {"x": float(np.median(mpc)), "mre": float(np.median([float(r["mre"]) for r in rr])),
                  "pct": float(np.median([100 * float(r["pct_cost"]) for r in rr])), "runs": len(rr)}
    return out


def cost_box():
    r = [x for x in csv.DictReader(open(RQ1)) if "cost_performance__target_energy" in x["target_context"]]
    r = (r or list(csv.DictReader(open(RQ1))))[0]
    return {"med": float(r["median_cost"]), "q1": float(r["q1_cost"]), "q3": float(r["q3_cost"]),
            "whislo": float(r["min_cost"]), "whishi": float(r["max_cost"]), "fliers": []}, int(float(r["n_configurations"]))


def main():
    pts = strat_points(); box, ncfg = cost_box()
    fig = plt.figure(figsize=(8.6, 5.6))
    grid = fig.add_gridspec(2, 1, height_ratios=[1.0, 3.2], hspace=0.07)
    axh = fig.add_subplot(grid[0]); ax = fig.add_subplot(grid[1], sharex=axh)

    # top: per-config cost distribution as a box (quartiles + min/max), log x
    bp = axh.bxp([box], positions=[0], vert=False, widths=0.6, patch_artist=True, showfliers=False,
                 medianprops={"color": "#333", "lw": 1.2}, whiskerprops={"color": "#888"},
                 capprops={"color": "#888"}, boxprops={"edgecolor": "#888"})
    bp["boxes"][0].set_facecolor("#dcdcdc")
    axh.set_yticks([]); axh.set_ylabel("configs", fontsize=9)
    axh.set_title(f"brotli 1.0.7, fixed $n{{=}}8$, predicting energy (random forest) — "
                  f"{ncfg} configs, cost $p_{{90}}/p_{{10}}{{=}}149\\times$", fontsize=10, fontweight="bold")
    plt.setp(axh.get_xticklabels(), visible=False)

    med = box["med"]
    for axis in (axh, ax):
        axis.axvline(med, color="#333", lw=1.0, alpha=0.7)

    # bottom: strategy scatter (mean per-config cost vs MRE)
    for s in ORDER:
        if s not in pts:
            continue
        p = pts[s]; oracle = s.endswith("Oracle")
        ax.scatter([p["x"]], [p["mre"]], s=150 if s in ("pairwise", "pilotCost") else 95,
                   color=COLORS[s], edgecolors="#111", linewidths=0.7,
                   marker="D" if oracle else "o", alpha=0.55 if oracle else 1.0, zorder=4)
        lab = s + (f"  ({p['runs']} seed)" if p["runs"] == 1 else "")
        right = p["x"] > 120  # pairwise, expensiveOracle hug the right edge
        ax.annotate(lab, (p["x"], p["mre"]), xytext=(-9, 7) if right else (7, 6), textcoords="offset points",
                    ha="right" if right else "left", fontsize=8, color=COLORS[s],
                    fontweight="bold" if s in ("pairwise", "pilotCost") else "normal")
    pw, pc = pts["pairwise"], pts["pilotCost"]
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(0.35, 620)
    ax.text(0.03, 0.97,
            f"pairwise: {pw['pct']:.1f}% full cost, MRE={pw['mre']:.1f}  (1 seed)\n"
            f"pilotCost: {pc['pct']:.2f}% full cost, MRE={pc['mre']:.2f}",
            transform=ax.transAxes, ha="left", va="top", fontsize=8.2,
            bbox={"facecolor": "white", "edgecolor": "#ccc", "alpha": 0.95})
    ax.text(med, ax.get_ylim()[1], " full median cost", color="#333", fontsize=7.5, va="top", ha="left", alpha=0.7)
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}"))
    ax.set_xlabel("Mean sampled performance cost per selected configuration (log)", fontsize=9.5)
    ax.set_ylabel("Median MRE predicting energy (log)", fontsize=9.5)
    ax.grid(color="#e3e3e3", lw=0.7, which="both"); ax.set_axisbelow(True)
    fig.subplots_adjust(left=0.1, right=0.98, top=0.91, bottom=0.1)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=220); plt.close(fig)
    print(f"Wrote {OUT}")
    for s in ORDER:
        if s in pts:
            print(f"  {s:16s} cost/config={pts[s]['x']:8.3f}  pct={pts[s]['pct']:6.2f}%  MRE={pts[s]['mre']:7.3f}  runs={pts[s]['runs']}")


if __name__ == "__main__":
    main()
