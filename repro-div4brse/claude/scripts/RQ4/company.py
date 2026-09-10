"""RQ4 Script A — perceived discrimination types by organizational setting.

Specification 05 §A. Same shape as RQ3 `profile.py`, but the profile dimensions
are the work model, the sector and the company size.

Run from `scripts/RQ4/`.
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
OUTPUT_DIR = "../../results/RQ4"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "company.png")

# Column indexes in the raw Google-Forms export (Spec 00 §4).
COL_WORKMODEL = 11
COL_SECTOR = 15
COL_COMPANYSIZE = 16
COL_DISC = 39

SPLIT_PATTERN = r",\s(?=\w+\s?\()"

DISC_MAP = {
    "Etarismo": "Ageism",
    "Machismo": "Sexism",
    "Homofobia": "Homophobia",
    "Racismo": "Racism",
    "Elitismo": "Elitism",
    "Capacitismo": "Ableism",
}

WORKMODEL_MAP = {"presencial": "On-site", "remoto": "Remote", "hibrido": "Hybrid"}
SECTOR_MAP = {
    "setor público": "Public",
    "setor privado": "Private",
    "organização não governamental": "Non-profit / NGO",
    "organização sem fins lucrativos": "Non-profit / NGO",
    "startup": "Startup",
}
COMPANYSIZE_MAP = {
    "até 9": "Small company",
    "até 9 funcionários": "Small company",
    "de 10 a 49": "Small company",
    "de 50 a 99": "Small company",
    "de 100 a 499": "Big company",
    "de 500 a 999": "Big company",
    "mais de 1000": "Big company",
}
OTHERS = "Others"

COL_ORDER = ["Ableism", "Ageism", "Elitism", "Homophobia", "Racism", "Sexism"]
ROW_ORDER = [
    "Big company", "Small company",
    "On-site", "Remote", "Hybrid",
    "Public", "Private", "Non-profit / NGO",
    "Total (overall)",
]
TOTAL_LABEL = "Total (overall)"


def norm(value):
    return str(value).strip().lower()


def mapear_discriminacao(value):
    tipo = str(value).split("(")[0].strip()
    return DISC_MAP.get(tipo)


def load_columns():
    df = pd.read_csv(DATA_PATH)
    cols = {
        "WorkModel": df.columns[COL_WORKMODEL],
        "Sector": df.columns[COL_SECTOR],
        "CompanySize": df.columns[COL_COMPANYSIZE],
        "Disc": df.columns[COL_DISC],
    }
    sub = df[list(cols.values())].dropna()
    sub.columns = list(cols.keys())
    return sub


def add_org_columns(df):
    df = df.copy()
    df["WorkModel Agg"] = df["WorkModel"].map(lambda v: WORKMODEL_MAP.get(norm(v), OTHERS))
    df["Sector Agg"] = df["Sector"].map(lambda v: SECTOR_MAP.get(norm(v), OTHERS))
    df["CompanySize Agg"] = df["CompanySize"].map(lambda v: COMPANYSIZE_MAP.get(norm(v), OTHERS))
    return df


def build_denominators(df_resp):
    totals = {}
    for column in ["WorkModel Agg", "Sector Agg", "CompanySize Agg"]:
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
    df = add_org_columns(df)
    df["Discriminação Label"] = df["Disc List"].map(mapear_discriminacao)
    df = df.dropna(subset=["Discriminação Label"])

    slices = []
    for column in ["WorkModel Agg", "Sector Agg", "CompanySize Agg"]:
        part = df[[column, "Discriminação Label"]].dropna()
        part.columns = ["Perfil", "Discriminação Label"]
        slices.append(part)

    total_slice = df[["Discriminação Label"]].copy()
    total_slice["Perfil"] = TOTAL_LABEL
    slices.append(total_slice[["Perfil", "Discriminação Label"]])

    long_df = pd.concat(slices, ignore_index=True)

    # Denominators from a fresh, un-exploded read of the same CSV.
    df_resp = add_org_columns(load_columns())
    total_por_perfil = build_denominators(df_resp)

    counts = long_df.groupby(["Perfil", "Discriminação Label"]).size().reset_index(name="count")
    counts["total"] = counts["Perfil"].map(total_por_perfil)
    counts["percent"] = counts["count"] / counts["total"] * 100

    matrix = counts.pivot_table(
        index="Perfil", columns="Discriminação Label", values="percent", fill_value=0
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

    print("Respondents per organizational group:")
    for group in ROW_ORDER:
        print(f"  {group}: {total_por_perfil.get(group, 0)}")
    print()
    print(matrix.round(1).to_string())
    print(f"Figure written to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
