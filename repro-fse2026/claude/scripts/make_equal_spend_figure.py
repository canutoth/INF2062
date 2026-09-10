#!/usr/bin/env python3
"""Equal-spend figure for the EMSE paper: coupling flip + budget gradient.

Panel A: share of scopes where pilotCost beats uniform random at equal
measured spend, ENERGY (strong cost-target coupling) vs LCBench (weak),
annotated with the median pilotCost/random risk ratio.
Panel B: share of scopes where SRS beats random at equal spend, by budget
level, per family.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BLUE = "#2a78d6"   # ENERGY
AQUA = "#1baf7a"   # LCBench
INK = "#44433c"
GRID = "#e5e4dc"

ENERGY = "artifacts/fse_posterior_energy_equal_spend/equal_spend_scope_summary.csv"
LCBENCH = "artifacts/fse_posterior_lcbench_equal_spend/equal_spend_scope_summary.csv"
OUT = Path("paper-emse/figures/fig_equal_spend.png")
LEVELS = ["n8", "n16", "n32", "n64"]


def main() -> None:
    energy = pd.read_csv(ENERGY)
    lcbench = pd.read_csv(LCBENCH)

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 3.6))

    ax = axes[0]
    rates = []
    ratios = []
    for df in (energy, lcbench):
        rates.append(df.pilotCost_beats_random.mean())
        ratios.append((df.pilotCost_risk / df.random_risk).median())
    x = np.arange(2)
    bars = ax.bar(x, rates, width=0.55, color=[BLUE, AQUA])
    for xi, bar, ratio, df in zip(x, bars, ratios, (energy, lcbench)):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.03,
                f"{bar.get_height():.0%} of {len(df)} scopes\nmedian risk ratio {ratio:.2f}x",
                ha="center", fontsize=8.5, color=INK)
    ax.set_xticks(x, ["ENERGY\n(cost ~ target)", "LCBench\n(cost independent of target)"], fontsize=9)
    ax.set_ylim(0, 0.92)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    ax.set_ylabel("pilotCost beats random at equal spend", fontsize=9)
    ax.set_title("A. Cost-aware volume pays only under weak coupling", fontsize=9.5, loc="left")

    ax = axes[1]
    for df, label, color in ((energy, "ENERGY", BLUE), (lcbench, "LCBench", AQUA)):
        shares = [df[df.ref_level == lvl].srs_beats_random.mean() for lvl in LEVELS]
        ax.plot(range(len(LEVELS)), shares, marker="o", color=color, linewidth=2, markersize=6, label=label)
    ax.set_xticks(range(len(LEVELS)), LEVELS, fontsize=9)
    ax.set_ylim(0, 0.92)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    ax.set_xlabel("budget level (reference sample size)", fontsize=9)
    ax.set_ylabel("SRS beats random at equal spend", fontsize=9)
    ax.set_title("B. SRS's equal-spend advantage needs budget to amortize", fontsize=9.5, loc="left")
    ax.legend(frameon=False, fontsize=9, loc="upper left")

    for ax in axes:
        ax.tick_params(labelsize=8)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="y", color=GRID, linewidth=0.7)
        ax.set_axisbelow(True)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches="tight")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
