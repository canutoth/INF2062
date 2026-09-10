import os

import matplotlib.pyplot as plt
import pandas as pd

OUT_DIR = os.path.join("..", "..", "results", "RQ7")

CATEGORY_COLORS = {
    "Uncertainty": "#1f77b4",
    "Denial": "#ff7f0e",
    "Recognition": "#2ca02c",
    "Personal Experience": "#d62728",
    "Out of scope": "#9467bd",
}

BIAS_TABLE = {
    "Uncertainty": {"Unsure": 8, "Unconscious": 3},
    "Denial": {"Not Recognized": 21, "Avoided": 2},
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
    "Personal Experience": {"Work Environment": 6, "Upbringing": 1},
    "Out of scope": {"Out of scope": 5},
}

os.makedirs(OUT_DIR, exist_ok=True)

rows = []
for category, subcategories in BIAS_TABLE.items():
    for subcategory, quantity in subcategories.items():
        rows.append(
            {
                "Category": category,
                "Subcategory": subcategory,
                "Quantity": quantity,
                "Color": CATEGORY_COLORS[category],
            }
        )
df = pd.DataFrame(rows)

fig, ax = plt.subplots(figsize=(4, 10))
ax.barh(df["Subcategory"], df["Quantity"], color=df["Color"])
ax.margins(y=0.01)
ax.set_ylabel("Subcategories", fontsize=14)
ax.set_xlabel("Quantity", fontsize=14)
ax.tick_params(axis="both", labelsize=12)

handles = [
    plt.Line2D(
        [0],
        [0],
        marker="s",
        color="w",
        markerfacecolor=color,
        markersize=10,
    )
    for color in CATEGORY_COLORS.values()
]
legend = ax.legend(
    handles,
    list(CATEGORY_COLORS.keys()),
    title="Categories of Bias",
    loc="upper right",
    fontsize=11,
    frameon=True,
    borderpad=0.5,
)
legend.get_title().set_fontsize(13)

plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "coding-bias.png"), dpi=300, bbox_inches="tight")
plt.show()