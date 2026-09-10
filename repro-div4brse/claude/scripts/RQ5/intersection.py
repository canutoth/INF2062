"""RQ5 — workplace discrimination: Recognize, Narrate, Silence.

Specification 06. Derives the discourse strategy participants use when asked
whether they witnessed or experienced differential treatment (Q28, Yes/No) and,
if so, to describe it (Q29, free text), and crosses it with their intersecting
identities.

Run from `scripts/RQ5/`.

NOTE (Spec 06 §2): the upstream script does not clear the figure between the
four Q28 `countplot` calls, so each of `bar_q28_gen/se/race/dis.png` is drawn
over the previous axes. That behaviour is reproduced verbatim here.
"""

import os
import warnings
from collections import Counter

import matplotlib

matplotlib.use("Agg")  # headless / autonomous execution

import matplotlib.pyplot as plt
import numpy as np  # noqa: F401  (imported by the upstream script)
import pandas as pd
import seaborn as sns
from upsetplot import UpSet, from_memberships

warnings.filterwarnings("ignore")

DATA_PATH = "../../data/q28_q29.csv"
OUTPUT_DIR = "../../results/RQ5"

EXCLUDED = "Others/I don't know"

identity_columns = ["Disabled", "Gender", "Race", "Seniority", "Sexuality"]

DISCOURSE_ORDER = [
    "no_recognition",
    "recognized_no_narrative",
    "third_person",
    "first_person",
]

label_map = {
    "Gender: Woman": "Women",
    "Gender: Man": "Men",
    "Race: Non-white": "Non-white",
    "Race: White": "White",
    "Disabled: No": "Not disabled",
    "Disabled: Yes": "Disabled",
    "Sexuality: LGBTQ+": "LGBTQ+",
    "Sexuality: Heterosexual": "Heterosexual",
    "Seniority: Intern": "Intern",
    "Seniority: Junior": "Junior",
    "Seniority: Mid-level": "Mid-level",
    "Seniority: Senior": "Senior",
}


def out(name):
    return os.path.join(OUTPUT_DIR, name)


def discourse_strategy(row):
    if row["28"] == "no":
        return "no_recognition"
    if row["28"] == "yes":
        if row["29"] in {"none", "nan"}:
            return "recognized_no_narrative"
        if row["report_type"] == "3S":
            return "third_person"
        if row["report_type"] == "1S":
            return "first_person"
    return np.nan


def q28_bar_charts(df):
    """Percent of Yes/No answers to Q28 by identity (see the NOTE above)."""
    sns.countplot(data=df[df["Gender"] != EXCLUDED], x="28", stat="percent", hue="Gender")
    plt.savefig(out("bar_q28_gen.png"), dpi=300, bbox_inches="tight")

    sns.countplot(data=df[df["Sexuality"] != EXCLUDED], x="28", stat="percent", hue="Sexuality")
    plt.savefig(out("bar_q28_se.png"), bbox_inches="tight")

    sns.countplot(data=df[df["Race"] != EXCLUDED], x="28", stat="percent", hue="Race")
    plt.savefig(out("bar_q28_race.png"), bbox_inches="tight")

    sns.countplot(data=df[df["Disabled"] != EXCLUDED], x="28", stat="percent", hue="Disabled")
    plt.savefig(out("bar_q28_dis.png"), dpi=300, bbox_inches="tight")


def identity_long(df, value_columns):
    long_df = df.melt(
        id_vars=value_columns,
        value_vars=identity_columns,
        var_name="identity_dimension",
        value_name="identity_group",
    )
    long_df = long_df.dropna(subset=["identity_group"])
    long_df = long_df[long_df["identity_group"] != EXCLUDED]
    long_df["identity_label"] = (
        long_df["identity_dimension"] + ": " + long_df["identity_group"].astype(str)
    )
    return long_df


def heatmap(contingency, path):
    plt.figure(figsize=(10, 6))
    ax = sns.heatmap(
        contingency * 100,
        annot=True,
        fmt=".1f",
        cmap="Reds",
        vmax=80,
        cbar_kws={"label": "% of responses"},
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.show()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)
    print(f"Rows: {len(df)}")

    # --- Q28 bar charts (percent, by identity) -------------------------------
    q28_bar_charts(df)

    # --- Discourse strategy --------------------------------------------------
    df["28"] = df["28"].str.lower()
    df["29"] = df["29"].astype(str).str.lower()
    df["discourse_strategy"] = df.apply(discourse_strategy, axis=1)

    print()
    print("Discourse strategy distribution:")
    print(df["discourse_strategy"].value_counts(dropna=False).to_string())

    sns.countplot(df, x="28", stat="percent", hue="discourse_strategy")
    plt.savefig(out("bar_discourse.png"), bbox_inches="tight")

    # --- Discourse strategy x identity heatmap -------------------------------
    long_df = identity_long(df, ["discourse_strategy"])
    contingency = pd.crosstab(
        long_df["identity_label"], long_df["discourse_strategy"], normalize="index"
    )
    contingency = contingency.reindex(columns=DISCOURSE_ORDER, fill_value=0)
    contingency.index = [label_map.get(i, i) for i in contingency.index]
    print()
    print((contingency * 100).round(1).to_string())
    heatmap(contingency, out("heatmap29_dis.png"))

    # --- Report categories ---------------------------------------------------
    df["report_category_clean"] = (
        df["report_category"].fillna("").astype(str).str.lower().str.strip()
    )
    df_clean = df[df["report_category_clean"] != ""].copy()
    df_clean["report_category_list"] = df_clean["report_category_clean"].map(
        lambda v: [t for t in v.split(", ") if t]
    )
    print()
    print(f"Responses with a report category: {len(df_clean)}")

    flattened = [tag for tags in df_clean["report_category_list"] for tag in tags]
    counter = Counter(flattened)
    total = sum(counter.values())
    categories = list(counter.keys())
    percentages = [counter[c] / total * 100 for c in categories]

    print("Category distribution (% of occurrences):")
    for category, pct in zip(categories, percentages):
        print(f"  {category}: {counter[category]} ({pct:.1f}%)")

    plt.figure(figsize=(8, 5))
    plt.bar(categories, percentages)
    plt.ylabel("Percentage (%)")
    plt.title("Distribution of Discrimination Categories")
    plt.xticks(rotation=45, ha="right")
    plt.savefig(out("barplot_cat.png"), bbox_inches="tight")

    # Category x identity heatmap
    exploded = df_clean.explode("report_category_list")
    long_cat = identity_long(exploded, ["report_category_list"])
    long_cat = long_cat.dropna(subset=["report_category_list"])
    contingency_cat = pd.crosstab(
        long_cat["identity_label"], long_cat["report_category_list"], normalize="index"
    )
    contingency_cat.index = [label_map.get(i, i) for i in contingency_cat.index]
    print()
    print((contingency_cat * 100).round(1).to_string())
    heatmap(contingency_cat, out("heatmap29_cat.png"))

    # --- UpSet plot ----------------------------------------------------------
    data = from_memberships(df_clean["report_category_list"])
    data.index = pd.MultiIndex.from_tuples(
        [tuple(bool(v) for v in idx) for idx in data.index],
        names=list(data.index.names),
    )
    upset = UpSet(
        data,
        subset_size="count",
        show_counts=True,
        facecolor="tab:blue",
        sort_by="cardinality",
    )
    upset.plot()
    plt.suptitle("Intersections Between Report Categories", fontweight="bold", y=0.98)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig(out("useplot_cat2.png"), bbox_inches="tight")
    plt.show()

    print()
    print(f"Outputs written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
