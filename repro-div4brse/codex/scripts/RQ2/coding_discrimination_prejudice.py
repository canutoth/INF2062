import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

CSV_PATH = os.path.join("..", "..", "data", "coding_discrimination_prejudice.csv")
OUT_DIR = os.path.join("..", "..", "results", "RQ2")

LABEL_MAP = {
    "T1": "Defines prejudice only",
    "T2": "Defines discrimination only",
    "T3": "Defines prejudice and discrimination separately",
    "T4": "Defines prejudice and discrimination complementarly",
    "T5": "Generic or vague definition",
    "T6": "Blank/Out of context",
    "C1": "Prior judgment or stereotyping",
    "C2": "Bias or personal preference",
    "C3": "Unequal or unfair treatment",
    "C4": "Exclusion or denial of opportunities",
    "C5": "Harassment, humiliation, or microaggressions",
    "C6": "Targeted groups or social dimensions",
    "C7": "Structural or systemic factors",
    "C8": "Equality, fairness, or rights framing",
    "C9": "Intent versus impact or moral judgment",
    "C10": "Meritocracy or skills-first framing",
    "C11": "Reverse discrimination or anti-DEI framing",
}

os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH)
t_col = df.iloc[:, 2].dropna()
c_col = df.iloc[:, 3].dropna()


def count_tags(series):
    counts = {}
    for cell in series:
        for token in str(cell).split(","):
            token = token.strip()
            if token:
                counts[token] = counts.get(token, 0) + 1
    return pd.Series(counts)


t_counts = count_tags(t_col)
c_counts = count_tags(c_col)
all_counts = pd.concat([t_counts, c_counts]).sort_index()

codes = all_counts.index.tolist()
labels = [LABEL_MAP.get(code, code) for code in codes]
values = [int(v) for v in all_counts.values]
colors = ["tab:blue" if str(code).startswith("T") else "tab:red" for code in codes]

fig, ax = plt.subplots(figsize=(12, 6))
y = range(len(codes))
ax.barh(y, values, color=colors)
ax.set_yticks(list(y))
ax.set_yticklabels(labels, fontsize=14)
ax.tick_params(axis="x", labelsize=14)

for i, v in enumerate(values):
    ax.text(v, i, str(v), fontsize=12, va="center", ha="left")

ax.set_xlim(0, max(values) * 1.08 + 2)

ax.legend(
    handles=[Patch(facecolor="tab:blue"), Patch(facecolor="tab:red")],
    labels=["Type of Definition (T)", "Content of Definition (C)"],
    loc="upper right",
)

plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "coding_discrimination_prejudice.png"),
    dpi=300,
    bbox_inches="tight",
)
plt.show()