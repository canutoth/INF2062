"""RQ7 — self-awareness of unconscious bias.

Specification 08. Visualizes the qualitative coding of the answers to "do you
recognize any bias in your interpretation of the words, questions or
experiences mentioned?" (column index 46 of `analysis_i&d_up.csv`).

The coded counts are hard-coded below: this script reads no file at runtime.

Run from `scripts/RQ7/`.
"""

import os
import warnings

import matplotlib

matplotlib.use("Agg")  # headless / autonomous execution

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.lines import Line2D

warnings.filterwarnings("ignore")

OUTPUT_DIR = "../../results/RQ7"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "coding-bias.png")

data = {
    "Uncertainty": {
        "Unsure": 8,
        "Unconscious": 3,
    },
    "Denial": {
        "Not Recognized": 21,
        "Avoided": 2,
    },
    "Recognition": {
        "Anti-diversity": 4,
        "General Awareness": 8,
        "Gender": 12,
        "Racial": 10,
        "LGBT": 4,
        "Disability": 2,
        "Age": 1,
        "Religious": 2,
        "Political": 6,
        "Regional": 2,
    },
    "Personal Experience": {
        "Work Environment": 6,
        "Upbringing": 1,
    },
    "Out of scope": {
        "Out of scope": 5,
    },
}

colors = {
    "Uncertainty": "#1f77b4",
    "Denial": "#ff7f0e",
    "Recognition": "#2ca02c",
    "Personal Experience": "#d62728",
    "Out of scope": "#9467bd",
}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    rows = []
    for category, subcategories in data.items():
        for subcategory, quantity in subcategories.items():
            rows.append(
                {
                    "Category": category,
                    "Subcategory": subcategory,
                    "Quantity": quantity,
                }
            )
    df = pd.DataFrame(rows)
    df["Color"] = df["Category"].map(colors)

    fig, ax = plt.subplots(figsize=(4, 10))
    ax.barh(df["Subcategory"], df["Quantity"], color=df["Color"])
    ax.margins(y=0.01)
    ax.set_ylabel("Subcategories", fontsize=14)
    ax.set_xlabel("Quantity", fontsize=14)
    ax.tick_params(axis="both", labelsize=12)

    handles = [
        Line2D([0], [0], marker="s", color="w", markerfacecolor=color, markersize=12, label=category)
        for category, color in colors.items()
    ]
    legend = ax.legend(
        handles=handles,
        title="Categories of Bias",
        loc="upper right",
        fontsize=11,
        frameon=True,
        borderpad=0.5,
    )
    legend.get_title().set_fontsize(13)

    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
    plt.show()

    print(df[["Category", "Subcategory", "Quantity"]].to_string(index=False))
    print(f"Total coded answers: {df['Quantity'].sum()}")
    print(f"Figure written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
