import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch

CSV_PATH = os.path.join("..", "..", "data", "data_teams.csv")
OUT_PATH = os.path.join("..", "..", "results", "RQ6", "team-level.png")

LIKERT_COLS = [
    "Race/Ethnicity",
    "Gender/Sexuality",
    "Neurodivergency",
    "Disability",
    "Elderly",
]
COLORS = {1: "#d90000", 2: "#fc7e7e", 3: "#a6d96a", 4: "#1a9641"}
LEGEND_LABELS = ["Strongly Disagree", "Disagree", "Agree", "Strongly Agree"]

os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

df = pd.read_csv(CSV_PATH)

likert_counts = (
    df[LIKERT_COLS].apply(lambda x: x.value_counts(normalize=True)).fillna(0)
)
likert_perc = likert_counts.reindex(index=[1, 2, 3, 4]).fillna(0) * 100
likert_perc = likert_perc.T

neg = -likert_perc[[1, 2]]
pos = likert_perc[[3, 4]]

fig, ax = plt.subplots(figsize=(10, 7))

y = np.arange(len(likert_perc))
height = 0.6

left = np.zeros(len(likert_perc))
for col in [2, 1]:
    ax.barh(y, neg[col].values, left=left, height=height, color=COLORS[col])
    left = left + neg[col].values

left = np.zeros(len(likert_perc))
for col in [3, 4]:
    ax.barh(y, pos[col].values, left=left, height=height, color=COLORS[col])
    left = left + pos[col].values

ax.axvline(0, color="black", linewidth=0.8)
ax.set_yticks(y)
ax.set_yticklabels(likert_perc.index)
ax.set_xlabel("% of Respondents")
ax.set_title("Diverging Stacked-Bar Chart of Likert Responses")

handles = [
    Patch(facecolor=COLORS[scale]) for scale in [1, 2, 3, 4]
]
ax.legend(
    handles,
    LEGEND_LABELS,
    loc="upper center",
    bbox_to_anchor=(0.5, -0.1),
    ncol=4,
    fontsize=12,
)

ax.tick_params(axis="both", labelsize=12)
ax.margins(x=0.01, y=0.05)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=300, bbox_inches="tight")
plt.show()