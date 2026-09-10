"""Participant characterization — Specification 01.

One bar chart per demographic / professional attribute of the 220-participant
sample. Values in `data/participant-characterization.csv` are already English
categorical labels, so no cleaning, mapping or NA handling is applied.

Run from `scripts/participant_characterization/`.
"""

import os
import warnings

import matplotlib

matplotlib.use("Agg")  # headless / autonomous execution

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns  # noqa: F401  (imported by the upstream script)

warnings.filterwarnings("ignore")

DATA_PATH = "../../data/participant-characterization.csv"
OUTPUT_DIR = "../../results/participant_characterization"

PALETTE = [
    "#4285F4",
    "#EA4335",
    "#FBBC04",
    "#34A853",
    "#FF6D01",
    "#46BDC6",
    "#7BAAF7",
    "#F07B72",
]

TOTAL_PARTICIPANTS = 220


def reorder_categories(counts):
    """Push any "Others" / "don't know" label to the end, keeping count order."""
    normal, others = [], []
    for label in counts.index:
        if "Others" in str(label) or "don't know" in str(label):
            others.append(label)
        else:
            normal.append(label)
    return counts.reindex(normal + others)


def plot_column(column, counts, percentages):
    n_bars = len(counts)
    colors = [PALETTE[i % len(PALETTE)] for i in range(n_bars)]

    fig, ax = plt.subplots(figsize=(max(8, n_bars * 1.2), 6))
    ax.set_axisbelow(True)
    ax.grid(axis="y", linestyle="--", alpha=0.3)

    positions = range(n_bars)
    bars = ax.bar(positions, counts.values, width=0.6, color=colors)

    for bar, count, pct in zip(bars, counts.values, percentages.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{count}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=12,
        )

    ax.set_xticks([])
    ax.set_ylabel("Number of Participants", fontsize=14)
    ax.set_ylim(0, TOTAL_PARTICIPANTS)

    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=color, edgecolor="black")
        for color in colors
    ]
    ax.legend(
        handles,
        [str(label) for label in counts.index],
        loc="upper right",
        fontsize=16,
        frameon=True,
        fancybox=True,
        shadow=True,
    )

    plt.tight_layout()

    filename = column.replace("/", "-").replace(" ", "_").lower() + ".png"
    plt.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300, bbox_inches="tight")
    plt.close()
    return filename


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    columns = [c for c in df.columns if c != "ID"]

    print(f"Participants: {len(df)}")
    for column in columns:
        counts = df[column].value_counts()
        counts = reorder_categories(counts)
        percentages = counts / TOTAL_PARTICIPANTS * 100
        filename = plot_column(column, counts, percentages)
        print(f"  {column}: {len(counts)} categories -> {filename}")

    print(f"Figures written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
