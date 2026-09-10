"""RQ3 Script B — the "sintonia" (in-group) mixed-effects model.

Specification 04 §B. Tests whether belonging to a targeted group raises the odds
of perceiving the matching type of discrimination as recurrent, using a Bayesian
binomial mixed GLM with a random intercept per respondent.

Paths are resolved from `__file__`, so this script runs from anywhere.
"""

import os
import re
import traceback
import warnings

import matplotlib

matplotlib.use("Agg")  # headless / autonomous execution

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM

warnings.filterwarnings("ignore")

np.random.seed(42)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "..", "data", "analysis_i&d_up.csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "results", "RQ3")

# Column indexes in the raw Google-Forms export (Spec 00 §4).
COL_AGE = 3
COL_GENDER = 5
COL_SEXUALITY = 6
COL_RACE = 7
COL_PCD = 8
COL_EDUCATION = 10
COL_WORKMODEL = 11
COL_SENIORITY = 13
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

DISC_ORDER = ["Sexism", "Ableism", "Homophobia", "Racism"]

# Which respondents are "in group" for each discrimination type.
IN_GROUP_MAP = {
    "Sexism": lambda d: (d["Gender"] == "Women").astype(int),
    "Ableism": lambda d: (d["Disability"] == 1).astype(int),
    "Homophobia": lambda d: (d["LGBTQ+"] == 1).astype(int),
    "Racism": lambda d: (d["Race"] == 1).astype(int),
}

GENDER_MAP = {
    "homem cisgênero": "Men",
    "homem trans": "Men",
    "mulher cisgênero": "Women",
    "mulher trans": "Women",
}
SEXUALITY_MAP = {
    "heterossexual": 0,
    "homossexual": 1,
    "bissexual": 1,
    "pansexual": 1,
}
RACE_MAP = {"branco(a)": 0, "preto(a)": 1, "pardo(a)": 1, "indígena": 1}
SENIORITY_MAP = {
    "estagiário": "Intern",
    "júnior (até 5 anos)": "Junior",
    "pleno (6 a 9 anos)": "Mid-level",
    "sênior (10+ anos)": "Senior",
}
WORKMODEL_MAP = {"presencial": "On-site", "remoto": "Remote", "hibrido": "Hybrid"}
SECTOR_MAP = {
    "setor público": "Public",
    "setor privado": "Private",
    "organização não governamental": "Non-profit",
    "organização sem fins lucrativos": "Non-profit",
    "startup": "Startup",
}
COMPANYSIZE_MAP = {
    "até 9": "Small",
    "até 9 funcionários": "Small",
    "de 10 a 49": "Small",
    "de 50 a 99": "Small",
    "de 100 a 499": "Big",
    "de 500 a 999": "Big",
    "mais de 1000": "Big",
}


def norm(value):
    return str(value).strip().lower()


def map_disability(value):
    """`sintonia.py` leaves the ambiguous/other answers as NaN."""
    v = norm(value)
    if v.startswith("sim"):
        return 1.0
    if "não" in v:
        return 0.0
    return np.nan


def parse_age(value):
    v = norm(value).replace("anos", "").strip()
    try:
        return int(v)
    except ValueError:
        return np.nan


def map_discrimination(value):
    tipo = str(value).split("(")[0].strip()
    return DISC_MAP.get(tipo)


def significance(p):
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return ""


def load_data():
    df = pd.read_csv(DATA_PATH)
    cols = {
        "Gender_raw": df.columns[COL_GENDER],
        "Sexuality_raw": df.columns[COL_SEXUALITY],
        "Race_raw": df.columns[COL_RACE],
        "PCD_raw": df.columns[COL_PCD],
        "Education_raw": df.columns[COL_EDUCATION],
        "WorkModel_raw": df.columns[COL_WORKMODEL],
        "Seniority_raw": df.columns[COL_SENIORITY],
        "Sector_raw": df.columns[COL_SECTOR],
        "CompanySize_raw": df.columns[COL_COMPANYSIZE],
        "Disc_raw": df.columns[COL_DISC],
        "Age_raw": df.columns[COL_AGE],
    }
    sub = df[list(cols.values())].copy()
    sub.columns = list(cols.keys())

    demographic_cols = [
        "Gender_raw", "Sexuality_raw", "Race_raw", "PCD_raw", "Education_raw",
        "WorkModel_raw", "Seniority_raw", "Sector_raw",
    ]
    sub = sub.dropna(subset=demographic_cols)

    sub["Gender"] = sub["Gender_raw"].map(lambda v: GENDER_MAP.get(norm(v)))
    sub["LGBTQ+"] = sub["Sexuality_raw"].map(lambda v: SEXUALITY_MAP.get(norm(v)))
    sub["Race"] = sub["Race_raw"].map(lambda v: RACE_MAP.get(norm(v)))
    sub["Disability"] = sub["PCD_raw"].map(map_disability)
    sub["Seniority"] = sub["Seniority_raw"].map(lambda v: SENIORITY_MAP.get(norm(v)))
    sub["Age"] = sub["Age_raw"].map(parse_age)
    sub["WorkModel"] = sub["WorkModel_raw"].map(lambda v: WORKMODEL_MAP.get(norm(v)))
    sub["Sector"] = sub["Sector_raw"].map(lambda v: SECTOR_MAP.get(norm(v)))
    sub["CompanySize"] = sub["CompanySize_raw"].map(lambda v: COMPANYSIZE_MAP.get(norm(v)))
    return sub


def build_disc_binary(sub):
    exploded = sub[["Disc_raw"]].copy()
    exploded["DiscType"] = exploded["Disc_raw"].map(
        lambda v: [t.strip() for t in re.split(SPLIT_PATTERN, str(v))]
    )
    exploded = exploded.explode("DiscType")
    exploded["DiscType"] = exploded["DiscType"].map(map_discrimination)
    exploded = exploded.dropna(subset=["DiscType"])

    disc_binary = pd.crosstab(exploded.index, exploded["DiscType"])
    disc_binary = (disc_binary > 0).astype(int)
    # Respondents who selected no listed type keep an all-zero row.
    disc_binary = disc_binary.reindex(sub.index, fill_value=0)
    for disc_type in DISC_ORDER:
        if disc_type not in disc_binary.columns:
            disc_binary[disc_type] = 0
    return disc_binary[DISC_ORDER]


def build_long_df(model_df):
    frames = []
    for disc_type in DISC_ORDER:
        part = pd.DataFrame(
            {
                "respondent_id": range(len(model_df)),
                "disc_type": disc_type,
                "perceives": model_df[disc_type].astype(int).values,
                "in_group": IN_GROUP_MAP[disc_type](model_df).values,
            }
        )
        frames.append(part)
    return pd.concat(frames, ignore_index=True)


def fit_model(long_df):
    try:
        model = BinomialBayesMixedGLM.from_formula(
            "perceives ~ in_group",
            {"re": "0 + C(respondent_id)"},
            data=long_df,
            vcp_p=1,
            fe_p=2,
        )
        return model.fit_vb()
    except Exception:
        traceback.print_exc()
        return None


def extract_effect(result):
    names = list(result.model.exog_names)
    idx = next(i for i, name in enumerate(names) if "in_group" in name)
    coef = float(result.fe_mean[idx])
    sd = float(result.fe_sd[idx])
    odds_ratio = np.exp(coef)
    ci_lower = np.exp(coef - 1.96 * sd)
    ci_upper = np.exp(coef + 1.96 * sd)
    z = coef / sd
    p = 2 * stats.norm.sf(abs(z))
    return {
        "Parameter": "in_group",
        "OR": odds_ratio,
        "CI_lower": ci_lower,
        "CI_upper": ci_upper,
        "p": p,
        "sig": significance(p),
        "random_intercept_sd": float(np.exp(result.vcp_mean[0])),
    }


def breakdown(model_df):
    rows = []
    for disc_type in DISC_ORDER:
        in_group = IN_GROUP_MAP[disc_type](model_df).astype(bool)
        perceives = model_df[disc_type].astype(int)
        n_in = int(in_group.sum())
        pct_in = perceives[in_group].mean() * 100 if n_in else np.nan
        n_out = int((~in_group).sum())
        pct_out = perceives[~in_group].mean() * 100 if n_out else np.nan

        a = perceives[in_group].sum()
        b = n_in - a
        c = perceives[~in_group].sum()
        d = n_out - c
        if 0 in (a, b, c, d):
            raw_or = ((a + 0.5) * (d + 0.5)) / ((b + 0.5) * (c + 0.5))
        else:
            raw_or = (a * d) / (b * c)

        rows.append(
            {
                "disc_type": disc_type,
                "in_group_n": n_in,
                "in_group_pct": pct_in,
                "out_group_pct": pct_out,
                "raw_OR": raw_or,
            }
        )
    return pd.DataFrame(rows)


def forest_plot(effect, path):
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.errorbar(
        [effect["OR"]],
        [0],
        xerr=[[effect["OR"] - effect["CI_lower"]], [effect["CI_upper"] - effect["OR"]]],
        fmt="o",
        color="#2c3e50",
        capsize=4,
    )
    ax.axvline(1, color="red", linestyle="--", linewidth=1)
    ax.set_xscale("log")
    ax.set_yticks([0])
    ax.set_yticklabels(["In-group"])
    ax.set_xlabel("Odds Ratio (log scale)")
    ax.set_title("Sintonia effect")
    ax.annotate(
        f"OR = {effect['OR']:.2f}\n"
        f"95% CI [{effect['CI_lower']:.2f}, {effect['CI_upper']:.2f}]\n"
        f"p = {effect['p']:.4f} {effect['sig']}",
        xy=(0.02, 0.05),
        xycoords="axes fraction",
        fontsize=8,
        va="bottom",
    )
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def bar_chart(table, path):
    x = np.arange(len(table))
    width = 0.38

    fig, ax = plt.subplots(figsize=(6, 5))
    bars_in = ax.bar(x - width / 2, table["in_group_pct"], width, label="In-Group", color="tab:blue")
    bars_out = ax.bar(x + width / 2, table["out_group_pct"], width, label="Out-Group", color="tab:red")

    for bars in (bars_in, bars_out):
        for bar in bars:
            height = bar.get_height()
            if np.isfinite(height):
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height,
                    f"{height:.1f}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                )

    ax.set_xticks(x)
    ax.set_xticklabels(table["disc_type"])
    ax.set_ylabel("% Respondents Reporting")
    ax.set_ylim(0, 105)
    ax.legend()
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    sub = load_data()
    disc_binary = build_disc_binary(sub)

    demographics = sub[
        ["Gender", "LGBTQ+", "Race", "Disability", "Seniority", "Age", "WorkModel",
         "Sector", "CompanySize"]
    ]
    model_df = demographics.join(disc_binary, how="inner")

    before = len(model_df)
    model_df = model_df.dropna(
        subset=["Gender", "LGBTQ+", "Race", "Disability", "CompanySize"]
    )
    print(f"Rows dropped by dropna on model predictors: {before - len(model_df)}")
    print(f"Respondents in the model: {len(model_df)}")

    long_df = build_long_df(model_df.reset_index(drop=True))
    print(f"Long-format rows: {len(long_df)} ({len(model_df)} respondents x {len(DISC_ORDER)} types)")

    result = fit_model(long_df)
    if result is None:
        print("Model fit failed; no outputs written.")
        return None

    print()
    print(result.summary())

    effect = extract_effect(result)
    print()
    print(
        f"In-group effect: OR = {effect['OR']:.3f} "
        f"(95% CI {effect['CI_lower']:.3f}-{effect['CI_upper']:.3f}), "
        f"p = {effect['p']:.4f} {effect['sig']}"
    )
    print(f"Random-intercept SD: {effect['random_intercept_sd']:.3f}")

    # `fit_vb()` takes no seed; its BFGS step leaves float noise of order 1e-7
    # between runs that `np.random.seed(42)` cannot remove. Rounding to 4 decimals
    # (standard reporting precision for ORs and p-values, ~1000x above that noise)
    # makes the artifact byte-reproducible.
    effect_row = pd.DataFrame([effect])
    numeric = ["OR", "CI_lower", "CI_upper", "p", "random_intercept_sd"]
    effect_row[numeric] = effect_row[numeric].round(4)
    effect_row.to_csv(os.path.join(OUTPUT_DIR, "sintonia_mixed_model.csv"), index=False)

    table = breakdown(model_df)
    print()
    print(table.round(2).to_string(index=False))

    forest_plot(effect, os.path.join(OUTPUT_DIR, "sintonia_forest_plot.png"))
    bar_chart(table, os.path.join(OUTPUT_DIR, "sintonia_bar_chart.png"))

    print(f"Outputs written to {OUTPUT_DIR}")
    return result


if __name__ == "__main__":
    main()
