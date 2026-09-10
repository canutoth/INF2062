#!/usr/bin/env python3
"""Key-systems frontier figure for the EMSE paper.

Two clean guarantee/cost frontier panels (one budget level each, headline
strategies only): Linux 4.13 at the 2% level and the lrzip energy/energy
scenario at n64. Reuses the synthesis module's frontier panel and
entity-stable palette.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_fse_posterior_synthesis import NEUTRAL, STRATEGY_COLORS, _frontier_panel

PANELS = [
    (
        "artifacts/fse_posterior_linux_all_full/linux413_vmlinux/posterior_pareto.csv",
        "n01851",
        "Linux 4.13, kernel-size bound (2% level, n=1,851)",
    ),
    (
        "artifacts/fse_posterior_energy_final/twins_lrzip_cost_energy_target_energy/posterior_pareto.csv",
        "n64",
        "lrzip, energy bound and energy cost (n=64)",
    ),
]
OUT = Path("paper-emse/figures/fig_key_systems.png")


def main() -> None:
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.0))
    for ax, (path, level, title) in zip(axes, PANELS):
        pareto = pd.read_csv(path)
        pareto = pareto[~pareto.strategy.astype(str).str.contains("Oracle")]
        _frontier_panel(ax, pareto, level=level, title=title)
        strategies = sorted(pareto[pareto["level"] == level]["strategy"].unique())
        handles = [
            plt.Line2D([], [], marker="o", linestyle="", color=STRATEGY_COLORS.get(s, NEUTRAL),
                       label=s, markersize=6)
            for s in strategies
        ]
        ax.legend(handles=handles, frameon=False, fontsize=7.5, loc="lower right", ncol=2)
    axes[0].set_ylabel("integrated posterior confidence", fontsize=8)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches="tight")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
