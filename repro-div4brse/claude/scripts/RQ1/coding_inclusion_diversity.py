"""RQ1 Part A — coded categories of the diversity & inclusion definitions.

Specification 02 §A. Reads `data/coding_inclusion_diversity.csv`, counts the
`T` codes (column index 2, type of definition) and the `C` codes (column index
3, content of definition) and renders them as one horizontal bar chart.

Run from `scripts/RQ1/`.
"""

import os
import warnings

import matplotlib

matplotlib.use("Agg")  # headless / autonomous execution

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

warnings.filterwarnings("ignore")

DATA_PATH = "../../data/coding_inclusion_diversity.csv"
OUTPUT_DIR = "../../results/RQ1"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "coding_inclusion_diversity.png")

label_map = {
    "T1": "Defines diversity only",
    "T2": "Defines inclusion only",
    "T3": "Defines diversity and inclusion separately",
    "T4": "Defines diversity and inclusion complementarly",
    "T5": "Generic or vague definition",
    "T6": "Blank/Out of context",
    "C1": "Demographic representation",
    "C2": "Cognitive or experiential diversity",
    "C3": "Equal opportunity / equity",
    "C4": "Belonging and respect",
    "C5": "Participation and voice",
    "C6": "Organizational practices or policies",
    "C7": "Justice or anti-discrimination framing",
    "C8": "Meritocracy / skills-first framing",
    "C9": "Instrumental or business outcomes",
    "C10": "Hate Comments",
}


def count_tags(series):
    """Split every cell on ',', strip each token and count all tokens."""
    tags = []
    for cell in series:
        for token in str(cell).split(","):
            token = token.strip()
            if token:
                tags.append(token)
    return pd.Series(tags).value_counts()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    t_col = df.iloc[:, 2].dropna()
    c_col = df.iloc[:, 3].dropna()

    t_counts = count_tags(t_col)
    c_counts = count_tags(c_col)
    all_counts = pd.concat([t_counts, c_counts]).sort_index()

    codes = list(all_counts.index)
    colors = ["tab:blue" if str(code).startswith("T") else "tab:red" for code in codes]
    labels = [label_map.get(code, code) for code in codes]

    fig, ax = plt.subplots(figsize=(12, 6))
    bars = ax.barh(labels, all_counts.values, color=colors)

    for bar in bars:
        width = bar.get_width()
        ax.text(
            width,
            bar.get_y() + bar.get_height() / 2,
            f"{int(width)}",
            va="center",
            ha="left",
            fontsize=12,
        )

    handles = [
        Patch(facecolor="tab:blue", label="Type of Definition (T)"),
        Patch(facecolor="tab:red", label="Content of Definition (C)"),
    ]
    ax.legend(handles=handles, loc="upper right", fontsize="large")

    ax.tick_params(axis="both", labelsize=14)
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
    plt.show()

    print(all_counts.rename(index=label_map).to_string())
    print(f"Figure written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
