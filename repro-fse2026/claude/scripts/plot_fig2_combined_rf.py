#!/usr/bin/env python3
"""Fig 2 (single panel): per-configuration cost heterogeneity across energy systems.
Each row is a system; the box is the per-config performance cost normalized by that
system's median (IQR box, min/max whiskers, log x), with CV and p90/p10 made
explicit. Learner- and seed-independent (drawn from the rq1 cost quantiles), so it
illustrates RQ1 without resting on any model fit. The seed-fragile count->cost
transition panel was removed; those recommendation changes are quantified, with
significance, in Table~\\ref{tab:rq-metrics}.
Overwrites pic/results/fig_cost_distribution_regimes.png (drop-in replacement)."""
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
RFBASE = ROOT / "artifacts/learner_sensitivity_compact/energy/rf-log"
OUT = ROOT / "607058f5f5131dcd1dbd783d/pic/results/fig_cost_distribution_regimes.png"
# (label, rf-dir) — same dir holds rq1_cost_heterogeneity.csv (per-config cost quantiles)
SYS = [("PostgreSQL", "PostgreSQL_11_2"), ("exastencils", "exastencils"), ("7z", "7z"),
       ("lrzip", "lrzip"), ("brotli", "brotli_1_0_7")]


def cost_box(rfdir):
    """Per-config cost box (normalized by median) + CV and p90/p10, from the rq1 quantiles."""
    rows = list(csv.DictReader(open(RFBASE / rfdir / "rq1_cost_heterogeneity.csv")))
    r = [x for x in rows if "cost_performance__target_performance" in x["target_context"]][0]
    med = float(r["median_cost"])
    box = {"med": 1.0, "q1": float(r["q1_cost"]) / med, "q3": float(r["q3_cost"]) / med,
           "whislo": float(r["min_cost"]) / med, "whishi": float(r["max_cost"]) / med, "fliers": []}
    return box, float(r["cv_cost"]), float(r["p90_over_p10"])


def main():
    data = []
    for label, rfdir in SYS:
        box, cv, p9010 = cost_box(rfdir)
        data.append((label, box, cv, p9010))
    data.sort(key=lambda d: d[3])  # tight -> wide by p90/p10
    n = len(data); pos = list(range(n, 0, -1))

    fig, ax = plt.subplots(figsize=(3.5, 2.95))  # native ~ single column: no downscaling
    bp = ax.bxp([d[1] for d in data], positions=pos, vert=False, widths=0.5,
                patch_artist=True, showfliers=False,
                medianprops={"color": "#333", "lw": 1.1}, whiskerprops={"color": "#888"},
                capprops={"color": "#888"}, boxprops={"edgecolor": "#888"})
    for patch in bp["boxes"]:
        patch.set_facecolor("#D6E2EF"); patch.set_alpha(0.9)
    ax.axvline(1.0, color="#bbb", ls="--", lw=0.8, zorder=1)
    tr = ax.get_yaxis_transform()  # x in axes frac, y in data
    for i, p in enumerate(pos):
        _, _, cv, p9010 = data[i]
        ax.text(0.03, p + 0.36, f"CV {cv:.2f} · $p_{{90}}/p_{{10}}${p9010:.0f}$\\times$",
                transform=tr, fontsize=7.0, color="#555", va="center")
    ax.set_xscale("log")
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v:g}×"))
    ax.set_xlabel("Per-config cost / system median (log)", fontsize=8.5)
    ax.set_yticks(pos); ax.set_yticklabels([d[0] for d in data], fontsize=8.5)
    ax.tick_params(axis="x", labelsize=7.5)
    ax.set_ylim(0.4, n + 0.85); ax.set_xlim(0.08, 320)
    ax.set_title("Per-configuration cost heterogeneity", fontsize=9, fontweight="bold")
    ax.grid(axis="x", color="#ececec", lw=0.6, which="both"); ax.set_axisbelow(True)
    fig.subplots_adjust(left=0.22, right=0.97, top=0.9, bottom=0.16)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=220); plt.close(fig)
    print(f"Wrote {OUT}")
    for label, box, cv, p9010 in data:
        print(f"  {label:12s} CV={cv:4.2f}  p90/p10={p9010:6.1f}x  "
              f"range [{box['whislo']:.2f}x, {box['whishi']:.1f}x] of median")


if __name__ == "__main__":
    main()
