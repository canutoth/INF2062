#!/usr/bin/env python3
"""Conceptual bridge figure: FSE posterior guarantees x empirical cost.

Schematic (synthetic curves, no measured data): panel A shows the FSE 2026
lens (guarantees per sample count), panel B our ICSE lens (sample count is
not measured cost), and panel C the combination (guarantees per measured
cost), where the equal-budget recommendation can flip.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

BLUE = "#2a78d6"   # guided strategy (SRS-like)
AQUA = "#1baf7a"   # uniform random
INK = "#44433c"
NEUTRAL = "#6b6a63"
GRID = "#e5e4dc"

OUT = Path("artifacts/fse_posterior_synthesis/fig_bridge_concept.png")

GAIN_GUIDED = 1.0
GAIN_RANDOM = 0.55
COST_GUIDED = 2.6   # cost units per sampled configuration
COST_RANDOM = 1.05


def confidence(n: np.ndarray | float, gain: float) -> np.ndarray | float:
    """Stylized integrated posterior confidence, saturating in n."""

    return 1.0 - np.exp(-gain * np.asarray(n, dtype=float) / 18.0)


def main() -> None:
    n = np.linspace(4, 100, 200)
    marks = np.array([10, 25, 50, 90])

    conf_guided = confidence(n, GAIN_GUIDED)
    conf_random = confidence(n, GAIN_RANDOM)
    cost_guided = COST_GUIDED * n
    cost_random = COST_RANDOM * n

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 3.9))

    ax = axes[0]
    ax.plot(n, conf_guided, color=BLUE, linewidth=2)
    ax.plot(n, conf_random, color=AQUA, linewidth=2)
    ax.scatter(marks, confidence(marks, GAIN_GUIDED), s=28, color=BLUE, zorder=3)
    ax.scatter(marks, confidence(marks, GAIN_RANDOM), s=28, color=AQUA, zorder=3)
    ax.text(58, 1.005, "guided (SRS-like)", color=BLUE, fontsize=9, fontweight="bold",
            ha="center", va="bottom")
    ax.text(72, 0.68, "uniform random", color=AQUA, fontsize=9, fontweight="bold",
            ha="center", va="top")
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("sample count n", fontsize=9)
    ax.set_ylabel("posterior confidence in the bound", fontsize=9)
    ax.set_title("A. FSE 2026 lens: guarantees per count\n(guided wins at every fixed n)",
                 fontsize=9.5, loc="left")

    ax = axes[1]
    ax.plot(n, n, color=NEUTRAL, linewidth=1.0, linestyle="--")
    ax.plot(n, cost_random, color=AQUA, linewidth=2)
    ax.plot(n, cost_guided, color=BLUE, linewidth=2)
    ax.annotate("count = cost", (92, 92), xytext=(4, -13),
                textcoords="offset points", color=NEUTRAL, fontsize=8)
    ax.annotate("guided picks costlier\nconfigurations", (55, COST_GUIDED * 55),
                xytext=(-8, 4), textcoords="offset points", color=BLUE, fontsize=9,
                fontweight="bold", ha="right")
    ax.annotate("uniform random", (76, COST_RANDOM * 76), xytext=(4, 8),
                textcoords="offset points", color=AQUA, fontsize=9, fontweight="bold")
    ax.set_xlabel("sample count n", fontsize=9)
    ax.set_ylabel("measured acquisition cost", fontsize=9)
    ax.set_title("B. Our ICSE lens: count is not cost\n(same n, different measured effort)",
                 fontsize=9.5, loc="left")

    ax = axes[2]
    ax.plot(cost_guided, conf_guided, color=BLUE, linewidth=2)
    ax.plot(cost_random, conf_random, color=AQUA, linewidth=2)
    budget = 60.0
    ax.axvline(budget, color=INK, linewidth=1.0, linestyle=":")
    ax.annotate("equal measured budget", (budget, 0.06), xytext=(-11, 0),
                textcoords="offset points", color=INK, fontsize=8, rotation=90, va="bottom")
    conf_guided_at = float(confidence(budget / COST_GUIDED, GAIN_GUIDED))
    conf_random_at = float(confidence(budget / COST_RANDOM, GAIN_RANDOM))
    ax.scatter([budget], [conf_guided_at], s=48, color=BLUE, zorder=3)
    ax.scatter([budget], [conf_random_at], s=48, color=AQUA, zorder=3)
    ax.annotate("random now wins\nat equal spend", (budget, conf_random_at), xytext=(10, 0.97),
                textcoords="data", color=AQUA, fontsize=9, fontweight="bold",
                ha="left", va="top",
                arrowprops={"arrowstyle": "-", "color": AQUA, "linewidth": 0.8, "shrinkB": 4})
    ax.annotate("guided, at the\nsame spend", (budget, conf_guided_at), xytext=(95, 0.52),
                textcoords="data", color=BLUE, fontsize=9, fontweight="bold",
                ha="left", va="top",
                arrowprops={"arrowstyle": "-", "color": BLUE, "linewidth": 0.8, "shrinkB": 4})
    ax.set_ylim(0, 1.05)
    ax.set_xlim(0, 190)
    ax.set_xlabel("measured acquisition cost", fontsize=9)
    ax.set_ylabel("posterior confidence in the bound", fontsize=9)
    ax.set_title("C. The bridge: guarantees per measured cost\n(the recommendation is cost-dependent)",
                 fontsize=9.5, loc="left")

    handles = [
        plt.Line2D([], [], color=BLUE, linewidth=2, label="guided (SRS-like)"),
        plt.Line2D([], [], color=AQUA, linewidth=2, label="uniform random"),
    ]
    fig.legend(handles=handles, frameon=False, fontsize=9, loc="upper center",
               ncol=2, bbox_to_anchor=(0.5, 0.04))
    for ax in axes:
        ax.tick_params(labelsize=8)
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(color=GRID, linewidth=0.7)
        ax.set_axisbelow(True)
    fig.suptitle("Schematic: combining FSE 2026 posterior guarantees with measured acquisition cost",
                 fontsize=11, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0.06, 1, 0.93))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=200, bbox_inches="tight")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
