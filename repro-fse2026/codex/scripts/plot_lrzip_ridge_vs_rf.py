#!/usr/bin/env python3
"""Side-by-side ridge vs RF for the lrzip running example (Fig 1/2 data).
Same generated samples, different learner. Shows the measured-cost 'sampling cost'
view: MRE (%) vs measured cost (% of full campaign), highlighting the two figure
points — diversity@n128 (small n) and pilotCost@n256 (larger n, but cheaper under
cost). Auto-scales the y-axis per panel (RF's MRE range differs from ridge's)."""
from __future__ import annotations
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
SOURCES = [
    ("ridge-log", ROOT / "artifacts/twins_generated_representative_100s/lrzip/strategy_summary.csv"),
    ("sk-rf-log", ROOT / "artifacts/twins_rf_lrzip/strategy_summary.csv"),
]
OUT = ROOT / "607058f5f5131dcd1dbd783d/pic/results/lrzip_cost_only_ridge_vs_rf.png"
TARGET, COST_CTX = "lrzip__cost_performance__target_performance", "lrzip::performance"
ORACLES = {"cheapOracle", "expensiveOracle"}


def read(src: Path):
    rows = []
    for r in csv.DictReader(src.open(newline="", encoding="utf-8")):
        if r["target_context"] != TARGET or r["cost_context"] != COST_CTX or r["strategy"] in ORACLES:
            continue
        rows.append({"label": f"{r['strategy']}_{r['level']}", "n": int(float(r["n"])),
                     "mre": 100 * float(r["median_mre"]), "cost": 100 * float(r["median_pct_cost"])})
    return rows


def find(rows, label):
    return next((r for r in rows if r["label"] == label), None)


def panel(ax, rows, learner):
    for r in rows:
        ax.scatter(r["cost"], r["mre"], s=26, color="#B8BDC5", alpha=0.65, edgecolor="white", linewidth=0.4, zorder=2)
    lo, hi = find(rows, "diversity_n128"), find(rows, "pilotCost_n256")
    if lo and hi:
        ax.annotate("", xy=(hi["cost"], hi["mre"]), xytext=(lo["cost"], lo["mre"]),
                    arrowprops={"arrowstyle": "->", "color": "#555", "lw": 1.15}, zorder=4)
        ax.scatter(lo["cost"], lo["mre"], s=110, color="#E4572E", edgecolor="black", linewidth=0.9, zorder=5)
        ax.scatter(hi["cost"], hi["mre"], s=120, marker="s", color="#2C7FB8", edgecolor="black", linewidth=0.9, zorder=6)
        ax.annotate(f"diversity\n$n=128$\ncost={lo['cost']:.1f}%", xy=(lo["cost"], lo["mre"]), xytext=(8, 10),
                    textcoords="offset points", fontsize=8, color="#7A2414", zorder=7)
        ax.annotate(f"pilotCost\n$n=256$\ncost={hi['cost']:.1f}%", xy=(hi["cost"], hi["mre"]), xytext=(8, -6),
                    textcoords="offset points", fontsize=8, color="#174C72", zorder=7)
    mres = [r["mre"] for r in rows]
    pad = max(2.0, 0.08 * (max(mres) - min(mres)))
    ax.set_ylim(min(mres) - pad, max(mres) + pad)
    ax.set_xlim(left=0)
    ax.set_title(f"{learner}", fontsize=10.5, fontweight="bold", pad=6)
    ax.set_xlabel("Measured cost (% of full campaign)")
    ax.grid(True, color="#E3E3E3", linewidth=0.6); ax.set_axisbelow(True)


def main():
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.7))
    for ax, (learner, src) in zip(axes, SOURCES):
        if not src.exists():
            ax.text(0.5, 0.5, f"{learner}\n(no data: {src.name})", ha="center", va="center"); continue
        panel(ax, read(src), learner)
    axes[0].set_ylabel("MRE (%)")
    fig.suptitle("lrzip running example — sampling cost view (target = performance), same samples, two learners",
                 fontsize=10, y=0.99)
    fig.subplots_adjust(left=0.08, right=0.985, top=0.86, bottom=0.155, wspace=0.18)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200); plt.close(fig)
    print(OUT)


if __name__ == "__main__":
    main()
