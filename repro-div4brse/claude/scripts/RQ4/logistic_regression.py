"""RQ4 Script B — adjusted odds ratios per discrimination type.

Specification 05 §B. One multivariable logistic regression per discrimination
type, adjusting for gender, sexuality, race, disability, company size,
seniority, work model and sector.

Paths are resolved from `__file__`, so this script runs from anywhere.
"""

import os
import re
import warnings

import matplotlib

matplotlib.use("Agg")  # headless / autonomous execution

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "..", "data", "analysis_i&d_up.csv")
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "results", "RQ4")

# Column indexes in the raw Google-Forms export (Spec 00 §4).
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
DISC_ORDER = ["Sexism", "Racism", "Homophobia", "Ableism", "Ageism", "Elitism"]
MIN_EVENTS = 5

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

SENIORITY_LEVELS = ["Intern", "Junior", "Mid-level", "Senior"]
SENIORITY_REF = "Intern"
WORKMODEL_LEVELS = ["On-site", "Remote", "Hybrid"]
WORKMODEL_REF = "On-site"
SECTOR_LEVELS = ["Public", "Private", "Startup", "Non-profit"]
SECTOR_REF = "Public"

DISPLAY_LABELS = {
    "Gender_Women": "Gender: Women",
    "LGBTQ+": "LGBTQ+: Yes",
    "Race": "Race: PoC",
    "Disability": "Disabled",
    "CompanySize_Big": "Company: Big",
    "Seniority_Junior": "Seniority: Junior",
    "Seniority_Mid-level": "Seniority: Mid-level",
    "Seniority_Senior": "Seniority: Senior",
    "WorkModel_Remote": "Work Model: Remote",
    "WorkModel_Hybrid": "Work Model: Hybrid",
    "Sector_Private": "Sector: Private",
    "Sector_Startup": "Sector: Startup",
    "Sector_Non-profit": "Sector: Non-profit",
}


def norm(value):
    return str(value).strip().lower()


def map_disability(value):
    v = norm(value)
    if v.startswith("sim"):
        return 1.0
    if "não" in v:
        return 0.0
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


def dummies(series, levels, reference, prefix):
    out = pd.DataFrame(index=series.index)
    for level in levels:
        if level == reference:
            continue
        out[f"{prefix}_{level}"] = (series == level).astype(int)
    return out


def load_predictors():
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
    }
    sub = df[list(cols.values())].copy()
    sub.columns = list(cols.keys())

    demographic_cols = [
        "Gender_raw", "Sexuality_raw", "Race_raw", "PCD_raw", "Education_raw",
        "WorkModel_raw", "Seniority_raw", "Sector_raw",
    ]
    sub = sub.dropna(subset=demographic_cols)

    gender = sub["Gender_raw"].map(lambda v: GENDER_MAP.get(norm(v)))
    seniority = sub["Seniority_raw"].map(lambda v: SENIORITY_MAP.get(norm(v)))
    workmodel = sub["WorkModel_raw"].map(lambda v: WORKMODEL_MAP.get(norm(v)))
    sector = sub["Sector_raw"].map(lambda v: SECTOR_MAP.get(norm(v)))
    company_size = sub["CompanySize_raw"].map(lambda v: COMPANYSIZE_MAP.get(norm(v)))

    predictors = pd.DataFrame(index=sub.index)
    predictors["Gender_Women"] = gender.map({"Women": 1.0, "Men": 0.0})
    predictors["LGBTQ+"] = sub["Sexuality_raw"].map(lambda v: SEXUALITY_MAP.get(norm(v)))
    predictors["Race"] = sub["Race_raw"].map(lambda v: RACE_MAP.get(norm(v)))
    predictors["Disability"] = sub["PCD_raw"].map(map_disability)
    predictors["CompanySize_Big"] = company_size.map({"Big": 1.0, "Small": 0.0})

    predictors = predictors.join(dummies(seniority, SENIORITY_LEVELS, SENIORITY_REF, "Seniority"))
    predictors = predictors.join(dummies(workmodel, WORKMODEL_LEVELS, WORKMODEL_REF, "WorkModel"))
    predictors = predictors.join(dummies(sector, SECTOR_LEVELS, SECTOR_REF, "Sector"))
    return predictors, sub["Disc_raw"]


def build_disc_binary(disc_raw):
    exploded = pd.DataFrame({"Disc_raw": disc_raw})
    exploded["DiscType"] = exploded["Disc_raw"].map(
        lambda v: [t.strip() for t in re.split(SPLIT_PATTERN, str(v))]
    )
    exploded = exploded.explode("DiscType")
    exploded["DiscType"] = exploded["DiscType"].map(map_discrimination)
    exploded = exploded.dropna(subset=["DiscType"])

    disc_binary = pd.crosstab(exploded.index, exploded["DiscType"])
    disc_binary = (disc_binary > 0).astype(int)
    disc_binary = disc_binary.reindex(disc_raw.index, fill_value=0)
    for disc_type in DISC_ORDER:
        if disc_type not in disc_binary.columns:
            disc_binary[disc_type] = 0
    return disc_binary[DISC_ORDER]


def fit_logit(y, X):
    try:
        return sm.Logit(y, X).fit(disp=0, maxiter=100)
    except Exception as exc:
        print(f"  Unregularized fit failed ({exc}); retrying regularized.")
    try:
        return sm.Logit(y, X).fit_regularized(disp=0, maxiter=200, L1_wt=0.0)
    except Exception as exc:
        print(f"  Regularized fit failed as well ({exc}); skipping.")
        return None


def or_table(result, predictors):
    params = result.params.drop("const", errors="ignore")
    conf = result.conf_int().drop("const", errors="ignore")
    pvalues = result.pvalues.drop("const", errors="ignore")

    table = pd.DataFrame(
        {
            "OR": np.exp(params),
            "CI_lower": np.exp(conf[0]),
            "CI_upper": np.exp(conf[1]),
            "p": pvalues,
        }
    )
    table["sig"] = table["p"].map(significance)
    table.index = [DISPLAY_LABELS.get(name, name) for name in table.index]
    table.index.name = "Predictor"
    return table


def forest_plot(table, title, path, x_min, x_max):
    fig, ax = plt.subplots(figsize=(8, 5))
    y = np.arange(len(table))
    lower = (table["OR"] - table["CI_lower"]).clip(lower=0)
    upper = (table["CI_upper"] - table["OR"]).clip(lower=0)

    ax.errorbar(
        table["OR"], y, xerr=[lower, upper], fmt="o", color="#2c3e50", capsize=3, linestyle="none"
    )
    ax.axvline(1, color="red", linestyle="--", linewidth=1)
    ax.set_xscale("log")
    ax.set_xlim(x_min, x_max)
    ax.set_yticks(y)
    ax.set_yticklabels(table.index)
    ax.invert_yaxis()
    ax.set_xlabel("Adjusted Odds Ratio (log scale)")
    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=300, bbox_inches="tight")
    plt.close()


def forest_panel(ax, table, title, x_min, x_max):
    y = np.arange(len(table))
    lower = (table["OR"] - table["CI_lower"]).clip(lower=0)
    upper = (table["CI_upper"] - table["OR"]).clip(lower=0)
    ax.errorbar(
        table["OR"], y, xerr=[lower, upper], fmt="o", color="#2c3e50", capsize=3, linestyle="none"
    )
    ax.axvline(1, color="red", linestyle="--", linewidth=1)
    ax.set_xscale("log")
    ax.set_xlim(x_min, x_max)
    ax.set_yticks(y)
    ax.set_yticklabels(table.index)
    ax.invert_yaxis()
    ax.set_title(title)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    predictors, disc_raw = load_predictors()
    disc_binary = build_disc_binary(disc_raw)
    model_df = predictors.join(disc_binary, how="inner")

    PREDICTORS = [c for c in predictors.columns]

    before = len(model_df)
    model_df = model_df.dropna(subset=PREDICTORS)
    print(f"Rows dropped by dropna on predictors: {before - len(model_df)}")
    print(f"Respondents in the models: {len(model_df)}")
    print(f"Predictors ({len(PREDICTORS)}): {', '.join(PREDICTORS)}")

    tables = {}
    for disc_type in DISC_ORDER:
        print()
        print("=" * 72)
        print(f"Logistic regression — {disc_type}")
        print("=" * 72)

        if disc_type not in model_df.columns:
            print(f"  Column '{disc_type}' absent; skipping.")
            continue

        y = model_df[disc_type].astype(int)
        events = int(y.sum())
        if events < MIN_EVENTS:
            print(f"  WARNING: only {events} events (< {MIN_EVENTS}); skipping.")
            continue

        X = sm.add_constant(model_df[PREDICTORS].astype(float))
        result = fit_logit(y, X)
        if result is None:
            continue

        table = or_table(result, PREDICTORS)
        tables[disc_type] = table

        print(f"  Events: {events}/{len(y)}")
        print(table.round(4).to_string())
        try:
            print(f"  McFadden R2: {result.prsquared:.4f}")
            print(f"  Log-likelihood: {result.llf:.4f}")
            print(f"  LLR p-value: {result.llr_pvalue:.6f}")
        except Exception:
            print("  Pseudo-R2 / LLR not available for this fit.")

        table.to_csv(os.path.join(OUTPUT_DIR, f"odds_ratios_{disc_type.lower()}.csv"))

    if not tables:
        print("No model was fitted; no plots written.")
        return

    combined = pd.concat(
        [t.assign(Discrimination=name) for name, t in tables.items()]
    )
    combined = combined[["Discrimination", "OR", "CI_lower", "CI_upper", "p", "sig"]]
    combined.to_csv(os.path.join(OUTPUT_DIR, "odds_ratios_all.csv"))

    # Shared log x-axis across every discrimination type.
    x_min = max(min(t["CI_lower"].min() for t in tables.values()), 0.05)
    x_max = max(t["CI_upper"].max() for t in tables.values()) * 1.15

    for disc_type, table in tables.items():
        forest_plot(
            table,
            f"Adjusted Odds Ratios — {disc_type}",
            os.path.join(OUTPUT_DIR, f"forest_plot_{disc_type.lower()}.png"),
            x_min,
            x_max,
        )

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    flat = axes.flatten()
    for ax, (disc_type, table) in zip(flat, tables.items()):
        forest_panel(ax, table, disc_type, x_min, x_max)
    for ax in flat[len(tables):]:
        ax.set_visible(False)
    fig.suptitle(
        "Adjusted Odds Ratios — Logistic Regression per Discrimination Type",
        fontsize=16,
    )
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "forest_plot_all.png"), dpi=300, bbox_inches="tight")
    plt.close()

    print()
    print(f"Outputs written to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
