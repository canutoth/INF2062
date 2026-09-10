"""RQ6 — representation in development teams (Likert).

Specification 07. Diverging stacked-bar chart of the 4-point agreement that
development teams include each of five demographic groups.

Run from `scripts/RQ6/`.
"""

import os
import warnings

import matplotlib

matplotlib.use("Agg")  # headless / autonomous execution

import matplotlib.pyplot as plt
import numpy as np  # noqa: F401  (imported by the upstream script)
import pandas as pd
from matplotlib.patches import Patch

warnings.filterwarnings("ignore")

DATA_PATH = "../../data/data_teams.csv"
OUTPUT_DIR = "../../results/RQ6"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "team-level.png")

likert_cols = ["Race/Ethnicity", "Gender/Sexuality", "Neurodivergency", "Disability", "Elderly"]

COLORS = {1: "#d90000", 2: "#fc7e7e", 3: "#a6d96a", 4: "#1a9641"}
LABELS = {
    1: "Strongly Disagree",
    2: "Disagree",
    3: "Agree",
    4: "Strongly Agree",
}


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    likert_counts = df[likert_cols].apply(lambda x: x.value_counts(normalize=True)).fillna(0)
    likert_perc = (likert_counts.reindex(index=[1, 2, 3, 4]).fillna(0) * 100).T

    neg = -likert_perc[[1, 2]]
    pos = likert_perc[[3, 4]]

    fig, ax = plt.subplots(figsize=(10, 7))

    left = pd.Series(0.0, index=likert_perc.index)
    for col in [2, 1]:
        ax.barh(likert_perc.index, neg[col], left=left, color=COLORS[col], height=0.6)
        left = left + neg[col]

    left = pd.Series(0.0, index=likert_perc.index)
    for col in [3, 4]:
        ax.barh(likert_perc.index, pos[col], left=left, color=COLORS[col], height=0.6)
        left = left + pos[col]

    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("% of Respondents")
    ax.set_title("Diverging Stacked-Bar Chart of Likert Responses")

    handles = [Patch(facecolor=COLORS[k], label=LABELS[k]) for k in [1, 2, 3, 4]]
    ax.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, -0.1),
        ncol=4,
        fontsize=12,
    )

    ax.tick_params(axis="both", labelsize=12)
    ax.margins(x=0.01, y=0.05)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
    plt.show()

    print(likert_perc.round(1).to_string())
    print(f"Figure written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
