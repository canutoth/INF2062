import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

CSV_PATH = os.path.join("..", "..", "data", "participant-characterization.csv")
OUT_DIR = os.path.join("..", "..", "results", "participant_characterization")
N_PARTICIPANTS = 220

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

os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH)
columns = [c for c in df.columns if c != "ID"]


def reorder_with_others_last(counts):
    counts = counts.copy()
    is_other = (
        counts.index.astype(str).str.contains("Others|don't know", case=False, regex=True)
    )
    if not is_other.any():
        return counts
    head = counts[~is_other]
    tail = counts[is_other]
    return pd.concat([head, tail])


def plot_column(col):
    counts = reorder_with_others_last(df[col].value_counts())
    n_bars = len(counts)
    colors = [PALETTE[i % len(PALETTE)] for i in range(n_bars)]

    fig, ax = plt.subplots(figsize=(max(8, n_bars * 1.2), 6))
    ax.bar(range(n_bars), counts.values, width=0.6, color=colors)

    ax.set_xticks([])
    ax.set_ylim(0, 220)
    ax.set_ylabel("Number of Participants", fontsize=14)

    for i, (label, count) in enumerate(counts.items()):
        pct = count / N_PARTICIPANTS * 100
        ax.text(
            i,
            count + 2,
            f"{count}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight="bold",
        )

    handles = [
        plt.Rectangle((0, 0), 1, 1, facecolor=c, edgecolor="black") for c in colors
    ]
    ax.legend(
        handles,
        [str(l) for l in counts.index],
        loc="upper right",
        fontsize=16,
        frameon=True,
        fancybox=True,
        shadow=True,
    )

    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    plt.tight_layout()
    out_name = col.replace("/", "-").replace(" ", "_").lower() + ".png"
    out_path = os.path.join(OUT_DIR, out_name)
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close(fig)


for col in columns:
    plot_column(col)