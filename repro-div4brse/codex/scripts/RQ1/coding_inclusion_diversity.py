import os

import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Patch

CSV_PATH = os.path.join("..", "..", "data", "coding_inclusion_diversity.csv")
OUT_DIR = os.path.join("..", "..", "results", "RQ1")

LABEL_MAP = {
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
    os.path.join(OUT_DIR, "coding_inclusion_diversity.png"),
    dpi=300,
    bbox_inches="tight",
)
plt.show()