import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

CSV_PATH = os.path.join("..", "..", "data", "analysis_i&d_up.csv")
OUT_DIR = os.path.join("..", "..", "results", "RQ3")

COLUMN_ORDER = ["Ableism", "Ageism", "Elitism", "Homophobia", "Racism", "Sexism"]
ROW_ORDER = [
    "Women",
    "Men",
    "Heterosexual",
    "LGBTQ+",
    "White",
    "PoC",
    "Intern",
    "Junior",
    "Mid-level",
    "Senior",
    "Not disabled",
    "Disabled",
    "Total (overall)",
]

os.makedirs(OUT_DIR, exist_ok=True)


def map_gender(v):
    mapping = {
        "homem cisgênero": "Men",
        "homem trans": "Men",
        "mulher cisgênero": "Women",
        "mulher trans": "Women",
    }
    return mapping.get(str(v).strip().lower(), np.nan)


def map_sexuality(v):
    mapping = {
        "heterossexual": "Heterosexual",
        "homossexual": "LGBTQ+",
        "bissexual": "LGBTQ+",
        "pansexual": "LGBTQ+",
    }
    return mapping.get(str(v).strip().lower(), np.nan)


def map_race(v):
    mapping = {
        "branco(a)": "White",
        "preto(a)": "PoC",
        "pardo(a)": "PoC",
        "indígena": "PoC",
    }
    return mapping.get(str(v).strip().lower(), np.nan)


def map_seniority(v):
    mapping = {
        "estagiário": "Intern",
        "júnior (até 5 anos)": "Junior",
        "pleno (6 a 9 anos)": "Mid-level",
        "sênior (10+ anos)": "Senior",
    }
    return mapping.get(str(v).strip().lower(), np.nan)


def map_pcd(v):
    text = str(v).strip().lower()
    if text.startswith("sim"):
        return "Disabled"
    if "não" in text or "nao" in text:
        return "Not disabled"
    return "Disabled"


def map_discrimination_type(v):
    mapping = {
        "etarismo": "Ageism",
        "machismo": "Sexism",
        "homofobia": "Homophobia",
        "racismo": "Racism",
        "elitismo": "Elitism",
        "capacitismo": "Ableism",
    }
    return mapping.get(str(v).split("(")[0].strip().lower(), np.nan)


raw = pd.read_csv(CSV_PATH)
dfr = raw.iloc[:, [5, 6, 7, 8, 13, 39]].copy()
dfr.columns = ["gender", "sexuality", "race", "pcd", "seniority", "disc"]
dfr = dfr.dropna()

dfr["Gender Agg"] = dfr["gender"].map(map_gender)
dfr["Sexuality Agg"] = dfr["sexuality"].map(map_sexuality)
dfr["Race Agg"] = dfr["race"].map(map_race)
dfr["Seniority Agg"] = dfr["seniority"].map(map_seniority)
dfr["PCD"] = dfr["pcd"].apply(map_pcd)

exploded = dfr.assign(
    disc_list=dfr["disc"].apply(lambda v: re.split(r",\s(?=\w+\s?\()", str(v)))
).explode("disc_list")
exploded["disc_list"] = exploded["disc_list"].str.strip()
exploded["Disc Label"] = exploded["disc_list"].apply(map_discrimination_type)

slices = []
for dim_col in ["Gender Agg", "Sexuality Agg", "Race Agg", "Seniority Agg", "PCD"]:
    sub = exploded[["Disc Label", dim_col]].dropna()
    sub = sub.rename(columns={dim_col: "Profile"})
    slices.append(sub)

total_slice = exploded[["Disc Label"]].dropna()
total_slice = total_slice.assign(Profile="Total (overall)")
slices.append(total_slice)

long_df = pd.concat(slices, ignore_index=True)
type_per_profile = long_df.groupby(["Profile", "Disc Label"]).size()

denominators = {}
for dim_col in ["Gender Agg", "Sexuality Agg", "Race Agg", "Seniority Agg", "PCD"]:
    counts = dfr[dim_col].value_counts()
    for group, count in counts.items():
        denominators[group] = count
denominators["Total (overall)"] = len(dfr)

counts_df = type_per_profile.rename("count").reset_index()
counts_df["den"] = counts_df["Profile"].map(denominators)
counts_df["percent"] = counts_df["count"] / counts_df["den"] * 100

matrix = counts_df.pivot(index="Profile", columns="Disc Label", values="percent")
matrix = matrix.reindex(columns=COLUMN_ORDER).reindex(index=ROW_ORDER).fillna(0)

fig, ax = plt.subplots(figsize=(10, 7))
sns.heatmap(
    matrix,
    annot=True,
    fmt=".1f",
    cmap="Reds",
    linewidths=0.5,
    annot_kws={"size": 14},
    cbar_kws={"label": "% of respondents"},
    ax=ax,
)
ax.tick_params(axis="x", rotation=0, labelsize=12)
ax.tick_params(axis="y", labelsize=12)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "profile.png"), dpi=300, bbox_inches="tight")
plt.show()