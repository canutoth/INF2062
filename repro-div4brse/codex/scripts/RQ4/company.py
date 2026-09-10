import os
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

CSV_PATH = os.path.join("..", "..", "data", "analysis_i&d_up.csv")
OUT_DIR = os.path.join("..", "..", "results", "RQ4")

COLUMN_ORDER = ["Ableism", "Ageism", "Elitism", "Homophobia", "Racism", "Sexism"]
ROW_ORDER = [
    "Big company",
    "Small company",
    "On-site",
    "Remote",
    "Hybrid",
    "Public",
    "Private",
    "Non-profit / NGO",
    "Total (overall)",
]

os.makedirs(OUT_DIR, exist_ok=True)


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


def map_work_model(v):
    text = str(v).strip().lower()
    if "presencial" in text:
        return "On-site"
    if "remoto" in text:
        return "Remote"
    if "hibrido" in text or "híbrido" in text:
        return "Hybrid"
    return "Others"


def map_sector(v):
    text = str(v).strip().lower()
    if "público" in text:
        return "Public"
    if "privado" in text:
        return "Private"
    if "governamental" in text or "lucrativos" in text:
        return "Non-profit / NGO"
    if "startup" in text:
        return "Startup"
    return "Others"


def map_company_size(v):
    text = str(v).strip().lower()
    small = ["até 9", "de 10 a 49", "de 50 a 99"]
    big = ["de 100 a 499", "de 500 a 999", "mais de 1000"]
    for token in small:
        if token in text:
            return "Small company"
    for token in big:
        if token in text:
            return "Big company"
    return "Others"


raw = pd.read_csv(CSV_PATH)
dfr = raw.iloc[:, [11, 15, 16, 39]].copy()
dfr.columns = ["work_model", "sector", "company_size", "disc"]
dfr = dfr.dropna()

dfr["Perfil"] = dfr["work_model"].apply(map_work_model)
dfr["Sector"] = dfr["sector"].apply(map_sector)
dfr["Size"] = dfr["company_size"].apply(map_company_size)

exploded = dfr.assign(
    disc_list=dfr["disc"].apply(lambda v: re.split(r",\s(?=\w+\s?\()", str(v)))
).explode("disc_list")
exploded["disc_list"] = exploded["disc_list"].str.strip()
exploded["Discriminação Label"] = exploded["disc_list"].apply(map_discrimination_type)

slices = []
for dim_col in ["Perfil", "Sector", "Size"]:
    sub = exploded[["Discriminação Label", dim_col]].dropna()
    sub = sub.rename(columns={dim_col: "Perfil"})
    slices.append(sub)

total_slice = exploded[["Discriminação Label"]].dropna()
total_slice = total_slice.assign(Perfil="Total (overall)")
slices.append(total_slice)

long_df = pd.concat(slices, ignore_index=True)
type_per_profile = long_df.groupby(["Perfil", "Discriminação Label"]).size()

denominators = {}
for dim_col in ["Perfil", "Sector", "Size"]:
    for group, count in dfr[dim_col].value_counts().items():
        denominators[group] = count
denominators["Total (overall)"] = len(dfr)

counts_df = type_per_profile.rename("count").reset_index()
counts_df["den"] = counts_df["Perfil"].map(denominators)
counts_df["percent"] = counts_df["count"] / counts_df["den"] * 100

matrix = counts_df.pivot(index="Perfil", columns="Discriminação Label", values="percent")
matrix = matrix.reindex(index=ROW_ORDER, columns=COLUMN_ORDER)

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
plt.savefig(os.path.join(OUT_DIR, "company.png"), dpi=300, bbox_inches="tight")
plt.show()