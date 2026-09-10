import os
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from upsetplot import UpSet, from_memberships

CSV_PATH = os.path.join("..", "..", "data", "q28_q29.csv")
OUT_DIR = os.path.join("..", "..", "results", "RQ5")

IDENTITY_COLUMNS = ["Disabled", "Gender", "Race", "Seniority", "Sexuality"]
DISCOURSE_ORDER = [
    "no_recognition",
    "recognized_no_narrative",
    "third_person",
    "first_person",
]

LABEL_MAP = {
    "Gender: Woman": "Women",
    "Gender: Man": "Men",
    "Race: White": "White",
    "Race: Non-white": "Non-white",
    "Disabled: No": "Not disabled",
    "Disabled: Yes": "Disabled",
    "Sexuality: Heterosexual": "Heterosexual",
    "Sexuality: LGBTQ+": "LGBTQ+",
    "Seniority: Intern": "Intern",
    "Seniority: Junior": "Junior",
    "Seniority: Mid-level": "Mid-level",
    "Seniority: Senior": "Senior",
}

os.makedirs(OUT_DIR, exist_ok=True)

df = pd.read_csv(CSV_PATH)

# Q28 bar charts, by identity (figure is intentionally NOT cleared between calls).
q28_config = {
    "Gender": ("bar_q28_gen.png", 300),
    "Sexuality": ("bar_q28_se.png", None),
    "Race": ("bar_q28_race.png", None),
    "Disabled": ("bar_q28_dis.png", 300),
}
for identity, (out_name, dpi) in q28_config.items():
    sub = df[df[identity] != "Others/I don't know"]
    sns.countplot(data=sub, x="28", stat="percent", hue=identity)
    plt.gca().set_xlabel("28")
    plt.savefig(
        os.path.join(OUT_DIR, out_name),
        bbox_inches="tight",
        dpi=dpi,
    )

# Discourse-strategy derivation.
df["28"] = df["28"].str.lower()
df["29"] = df["29"].astype(str).str.lower()


def discourse_strategy(row):
    if row["28"] == "no":
        return "no_recognition"
    if row["28"] == "yes" and row["29"] in {"none", "nan"}:
        return "recognized_no_narrative"
    if row["28"] == "yes" and row["report_type"] == "3S":
        return "third_person"
    if row["28"] == "yes" and row["report_type"] == "1S":
        return "first_person"
    return np.nan


df["discourse_strategy"] = df.apply(discourse_strategy, axis=1)

sns.countplot(df, x="28", stat="percent", hue="discourse_strategy")
plt.gca().set_xlabel("28")
plt.savefig(os.path.join(OUT_DIR, "bar_discourse.png"), bbox_inches="tight")

# Discourse strategy x identity heatmap.
melted = df.melt(
    id_vars=["discourse_strategy"],
    value_vars=IDENTITY_COLUMNS,
    var_name="identity_dimension",
    value_name="identity_group",
)
melted = melted[melted["identity_group"] != "Others/I don't know"]
melted["identity_label"] = (
    melted["identity_dimension"] + ": " + melted["identity_group"]
)

contingency = pd.crosstab(
    melted["identity_label"], melted["discourse_strategy"], normalize="index"
)
contingency = contingency.reindex(columns=DISCOURSE_ORDER)
contingency.index = [LABEL_MAP.get(lbl, lbl) for lbl in contingency.index]

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(
    contingency * 100,
    annot=True,
    fmt=".1f",
    cmap="Reds",
    vmax=80,
    cbar_kws={"label": "% of responses"},
    ax=ax,
)
ax.set_xlabel("")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "heatmap29_dis.png"), bbox_inches="tight")
plt.show()

# Report-category analysis.
df_clean = df.copy()
df_clean["report_category_clean"] = (
    df_clean["report_category"].fillna("").astype(str).str.lower().str.strip()
)
df_clean = df_clean[df_clean["report_category_clean"] != ""]
df_clean["report_category_list"] = df_clean["report_category_clean"].apply(
    lambda s: [tag.strip() for tag in s.split(",") if tag.strip()]
)

category_counter = Counter()
for tags in df_clean["report_category_list"]:
    category_counter.update(tags)
total_occurrences = sum(category_counter.values())
tag_order = sorted(category_counter.keys())
percentages = [category_counter[tag] / total_occurrences * 100 for tag in tag_order]

fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(tag_order, percentages)
ax.set_ylabel("Percentage (%)")
ax.set_title("Distribution of Discrimination Categories")
ax.tick_params(axis="x", rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "barplot_cat.png"), bbox_inches="tight")
plt.close(fig)

# Category x identity heatmap.
exploded = df_clean.explode("report_category_list")
melted_cat = exploded.melt(
    id_vars=["report_category_list"],
    value_vars=IDENTITY_COLUMNS,
    var_name="identity_dimension",
    value_name="identity_group",
)
melted_cat = melted_cat[melted_cat["identity_group"].notna()]
melted_cat = melted_cat[melted_cat["identity_group"] != "Others/I don't know"]
melted_cat["identity_label"] = (
    melted_cat["identity_dimension"] + ": " + melted_cat["identity_group"]
)

cat_contingency = pd.crosstab(
    melted_cat["identity_label"],
    melted_cat["report_category_list"],
    normalize="index",
)
cat_contingency.index = [
    LABEL_MAP.get(lbl, lbl) for lbl in cat_contingency.index
]

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(
    cat_contingency * 100,
    annot=True,
    fmt=".1f",
    cmap="Reds",
    vmax=80,
    cbar_kws={"label": "% of responses"},
    ax=ax,
)
ax.set_xlabel("")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "heatmap29_cat.png"), bbox_inches="tight")
plt.show()

# UpSet plot of report-category intersections.
upset_data = from_memberships(df_clean["report_category_list"])
upset_data.index = pd.MultiIndex.from_tuples(
    [tuple(bool(v) for v in membership) for membership in upset_data.index],
    names=upset_data.index.names,
)
upset = UpSet(
    upset_data,
    subset_size="count",
    show_counts=True,
    facecolor="tab:blue",
    sort_by="cardinality",
)
upset.plot()
plt.suptitle("Intersections Between Report Categories", fontweight="bold", y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig(os.path.join(OUT_DIR, "useplot_cat2.png"), bbox_inches="tight")
plt.show()