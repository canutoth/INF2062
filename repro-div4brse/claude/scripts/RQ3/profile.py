"""RQ3 Script A — perceived discrimination types by demographic profile.

Specification 04 §A. Reads `data/analysis_i&d_up.csv`, explodes the multi-select
"types of discrimination you believe are most recurrent in software development"
field (column index 39) and renders a profile x discrimination-type heatmap of
the percentage of respondents in each group who selected each type.

Run from `scripts/RQ3/`.
"""

import os
import re
import warnings

import matplotlib

matplotlib.use("Agg")  # headless / autonomous execution

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

warnings.filterwarnings("ignore")

DATA_PATH = "../../data/analysis_i&d_up.csv"
OUTPUT_DIR = "../../results/RQ3"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "profile.png")

# Column indexes in the raw Google-Forms export (Spec 00 §4).
COL_GENDER = 5
COL_SEXUALITY = 6
COL_RACE = 7
COL_PCD = 8
COL_SENIORITY = 13
COL_DISC = 39

# Each selected item is formatted "<Tipo> (exemplo: ...)"; items are separated by
# a comma followed by the next "<Word> (" — commas inside the examples must not
# split the list.
SPLIT_PATTERN = r",\s(?=\w+\s?\()"

GENDER_MAP = {
    "homem cisgênero": "Men",
    "homem trans": "Men",
    "mulher cisgênero": "Women",
    "mulher trans": "Women",
}
SEXUALITY_MAP = {
    "heterossexual": "Heterosexual",
    "homossexual": "LGBTQ+",
    "bissexual": "LGBTQ+",
    "pansexual": "LGBTQ+",
}
RACE_MAP = {
    "branco(a)": "White",
    "preto(a)": "PoC",
    "pardo(a)": "PoC",
    "indígena": "PoC",
}
SENIORITY_MAP = {
    "estagiário": "Intern",
    "júnior (até 5 anos)": "Junior",
    "pleno (6 a 9 anos)": "Mid-level",
    "sênior (10+ anos)": "Senior",
}
DISC_MAP = {
    "Etarismo": "Ageism",
    "Machismo": "Sexism",
    "Homofobia": "Homophobia",
    "Racismo": "Racism",
    "Elitismo": "Elitism",
    "Capacitismo": "Ableism",
}

COL_ORDER = ["Ableism", "Ageism", "Elitism", "Homophobia", "Racism", "Sexism"]
ROW_ORDER = [
    "Women", "Men", "Heterosexual", "LGBTQ+", "White", "PoC",
    "Intern", "Junior", "Mid-level", "Senior",
    "Not disabled", "Disabled", "Total (overall)",
]
TOTAL_LABEL = "Total (overall)"


def norm(value):
    return str(value).strip().lower()


def map_pcd(value):
    """`profile.py` resolves the ambiguous/other answers to `Disabled`."""
    v = norm(value)
    if v.startswith("sim"):
        return "Disabled"
    if "não" in v:
        return "Not disabled"
    return "Disabled"


def map_discrimination(value):
    tipo = str(value).split("(")[0].strip()
    return DISC_MAP.get(tipo)


def load_columns():
    df = pd.read_csv(DATA_PATH)
    cols = {
        "Gender": df.columns[COL_GENDER],
        "Sexuality": df.columns[COL_SEXUALITY],
        "Race": df.columns[COL_RACE],
        "PCD": df.columns[COL_PCD],
        "Seniority": df.columns[COL_SENIORITY],
        "Disc": df.columns[COL_DISC],
    }
    sub = df[list(cols.values())].dropna()
    sub.columns = list(cols.keys())
    return sub


def add_profile_columns(df):
    df = df.copy()
    df["Gender Agg"] = df["Gender"].map(lambda v: GENDER_MAP.get(norm(v)))
    df["Sexuality Agg"] = df["Sexuality"].map(lambda v: SEXUALITY_MAP.get(norm(v)))
    df["Race Agg"] = df["Race"].map(lambda v: RACE_MAP.get(norm(v)))
    df["Seniority Agg"] = df["Seniority"].map(lambda v: SENIORITY_MAP.get(norm(v)))
    df["PCD Agg"] = df["PCD"].map(map_pcd)
    return df


def build_denominators(df_resp):
    """Respondent-level group sizes, computed on the un-exploded table."""
    totals = {}
    for column in ["Gender Agg", "Sexuality Agg", "Race Agg", "Seniority Agg", "PCD Agg"]:
        for group, n in df_resp[column].dropna().value_counts().items():
            totals[group] = int(n)
    totals[TOTAL_LABEL] = len(df_resp)
    return totals


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = load_columns()
    df["Disc List"] = df["Disc"].map(lambda v: re.split(SPLIT_PATTERN, str(v)))
    df = df.explode("Disc List")
    df["Disc List"] = df["Disc List"].str.strip()
    df = add_profile_columns(df)
    df["Disc Label"] = df["Disc List"].map(map_discrimination)
    df = df.dropna(subset=["Disc Label"])

    # Long (Profile, Disc Label) table: one slice per profile dimension + total.
    slices = []
    for column in ["Gender Agg", "Sexuality Agg", "Race Agg", "Seniority Agg", "PCD Agg"]:
        part = df[[column, "Disc Label"]].dropna()
        part.columns = ["Profile", "Disc Label"]
        slices.append(part)

    total_slice = df[["Disc Label"]].copy()
    total_slice["Profile"] = TOTAL_LABEL
    slices.append(total_slice[["Profile", "Disc Label"]])

    long_df = pd.concat(slices, ignore_index=True)

    # Denominators from a fresh, un-exploded read of the same CSV.
    df_resp = add_profile_columns(load_columns())
    total_por_profile = build_denominators(df_resp)

    counts = long_df.groupby(["Profile", "Disc Label"]).size().reset_index(name="count")
    counts["total"] = counts["Profile"].map(total_por_profile)
    counts["percent"] = counts["count"] / counts["total"] * 100

    matrix = counts.pivot_table(
        index="Profile", columns="Disc Label", values="percent", fill_value=0
    )
    matrix = matrix.reindex(index=ROW_ORDER, columns=COL_ORDER)

    plt.figure(figsize=(10, 7))
    ax = sns.heatmap(
        matrix,
        annot=True,
        fmt=".1f",
        cmap="Reds",
        linewidths=0.5,
        annot_kws={"size": 14},
        cbar_kws={"label": "% of respondents"},
    )
    ax.set_xlabel("")
    ax.set_ylabel("")
    plt.xticks(rotation=0)
    ax.tick_params(axis="both", labelsize=12)
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
    plt.show()

    print("Respondents per profile group:")
    for group in ROW_ORDER:
        print(f"  {group}: {total_por_profile.get(group, 0)}")
    print()
    print(matrix.round(1).to_string())
    print(f"Figure written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
