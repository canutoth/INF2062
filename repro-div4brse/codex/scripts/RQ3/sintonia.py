import os
import re
import traceback
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import norm
from statsmodels.genmod.bayes_mixed_glm import BinomialBayesMixedGLM

np.random.seed(42)
warnings.filterwarnings("ignore")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "..", "data", "analysis_i&d_up.csv")
OUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "results", "RQ3")

DEMOGRAPHIC_COLS = [5, 6, 7, 8, 11, 13, 15, 16]
AGE_COL = 3
DISC_COL = 39
DISC_ORDER = ["Sexism", "Ableism", "Homophobia", "Racism"]

os.makedirs(OUT_DIR, exist_ok=True)


def map_gender(v):
    mapping = {
        "homem cisgênero": "Men",
        "homem trans": "Men",
        "mulher cisgênero": "Women",
        "mulher trans": "Women",
    }
    result = mapping.get(str(v).strip().lower(), np.nan)
    return result


def map_sexuality_id(v):
    text = str(v).strip().lower()
    if text == "heterossexual":
        return 0
    if text in ("homossexual", "bissexual", "pansexual"):
        return 1
    return np.nan


def map_race_id(v):
    text = str(v).strip().lower()
    if text == "branco(a)":
        return 0
    if text in ("preto(a)", "pardo(a)", "indígena"):
        return 1
    return np.nan


def map_disability(v):
    text = str(v).strip().lower()
    if text.startswith("sim"):
        return 1
    if "não" in text or "nao" in text:
        return 0
    return np.nan


def map_seniority(v):
    mapping = {
        "estagiário": "Intern",
        "júnior (até 5 anos)": "Junior",
        "pleno (6 a 9 anos)": "Mid-level",
        "sênior (10+ anos)": "Senior",
    }
    return mapping.get(str(v).strip().lower(), np.nan)


def parse_age(v):
    text = str(v).strip().lower().replace("anos", "").strip()
    try:
        return int(float(text))
    except ValueError:
        return np.nan


def map_work_model(v):
    text = str(v).strip().lower()
    if "presencial" in text:
        return "On-site"
    if "remoto" in text:
        return "Remote"
    if "hibrido" in text or "híbrido" in text:
        return "Hybrid"
    return np.nan


def map_sector(v):
    text = str(v).strip().lower()
    if "público" in text:
        return "Public"
    if "privado" in text:
        return "Private"
    if "governamental" in text or "lucrativos" in text:
        return "Non-profit"
    if "startup" in text:
        return "Startup"
    return np.nan


def map_company_size(v):
    text = str(v).strip().lower()
    small = ["até 9", "de 10 a 49", "de 50 a 99"]
    big = ["de 100 a 499", "de 500 a 999", "mais de 1000"]
    for token in small:
        if token in text:
            return "Small"
    for token in big:
        if token in text:
            return "Big"
    return np.nan


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


def derive_demographics(df):
    df = df.copy()
    df["Gender"] = df["gender"].apply(map_gender)
    df["LGBTQ+"] = df["sexuality"].apply(map_sexuality_id).astype(float)
    df["Race"] = df["race"].apply(map_race_id).astype(float)
    df["Disability"] = df["disability"].apply(map_disability).astype(float)
    df["Seniority"] = df["seniority"].apply(map_seniority)
    df["Age"] = df["age"].apply(parse_age)
    df["WorkModel"] = df["work_model"].apply(map_work_model)
    df["Sector"] = df["sector"].apply(map_sector)
    df["CompanySize"] = df["company_size"].apply(map_company_size)
    return df


def build_disc_binary(df):
    items = df["disc"].apply(lambda v: re.split(r",\s(?=\w+\s?\()", str(v)))
    types = items.apply(
        lambda lst: [map_discrimination_type(x) for x in lst]
    )
    disc_binary = pd.DataFrame(0, index=df.index, columns=DISC_ORDER, dtype=int)
    for t in DISC_ORDER:
        disc_binary[t] = [1 if t in row_types else 0 for row_types in types]
    return disc_binary


def in_group_flag(model_df, disc_type):
    if disc_type == "Sexism":
        return (model_df["Gender"] == "Women").astype(int)
    if disc_type == "Ableism":
        return model_df["Disability"].astype(int)
    if disc_type == "Homophobia":
        return model_df["LGBTQ+"].astype(int)
    if disc_type == "Racism":
        return model_df["Race"].astype(int)
    return np.nan


def sig_stars(p):
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return ""


def main():
    raw = pd.read_csv(DATA_PATH)
    df = raw.iloc[:, DEMOGRAPHIC_COLS + [AGE_COL, DISC_COL]].copy()
    df.columns = [
        "gender",
        "sexuality",
        "race",
        "disability",
        "work_model",
        "seniority",
        "sector",
        "company_size",
        "age",
        "disc",
    ]
    df = df.dropna(
        subset=[
            "gender",
            "sexuality",
            "race",
            "disability",
            "work_model",
            "seniority",
            "sector",
            "company_size",
        ]
    )

    demog = derive_demographics(df)
    disc_binary = build_disc_binary(df)

    model_df = demog.join(disc_binary, how="inner")
    n_before = len(model_df)
    model_df = model_df.dropna(
        subset=["Gender", "LGBTQ+", "Race", "Disability", "CompanySize"]
    )
    n_after = len(model_df)
    print(f"Respondents before dropna: {n_before}; after dropna: {n_after} "
          f"(rows_dropped={n_before - n_after})")

    long_rows = []
    n_respondents = len(model_df)
    for t in DISC_ORDER:
        sub = pd.DataFrame(
            {
                "respondent_id": np.arange(n_respondents),
                "perceives": model_df[t].astype(int),
                "disc_type": t,
                "in_group": in_group_flag(model_df, t),
            },
            index=model_df.index,
        )
        long_rows.append(sub)
    long_df = pd.concat(long_rows, ignore_index=True)

    breakdown = []
    for t in DISC_ORDER:
        sub = long_df[long_df["disc_type"] == t]
        in_group = sub["in_group"] == 1
        in_n = int(in_group.sum())
        out_n = int((~in_group).sum())
        in_pct = sub.loc[in_group, "perceives"].mean() * 100 if in_n else np.nan
        out_pct = sub.loc[~in_group, "perceives"].mean() * 100 if out_n else np.nan
        in_yes = int((in_group & (sub["perceives"] == 1)).sum())
        in_no = int((in_group & (sub["perceives"] == 0)).sum())
        out_yes = int((~in_group & (sub["perceives"] == 1)).sum())
        out_no = int((~in_group & (sub["perceives"] == 0)).sum())
        table = [[in_yes, in_no], [out_yes, out_no]]
        if min(table[0] + table[1]) == 0:
            table = [[c + 0.5 for c in row] for row in table]
        a, b = table[0]
        c_, d = table[1]
        raw_or = (a * d) / (b * c_) if b * c_ else np.nan
        breakdown.append(
            {
                "type": t,
                "in_n": in_n,
                "in_pct": in_pct,
                "out_n": out_n,
                "out_pct": out_pct,
                "raw_or": raw_or,
            }
        )
        print(
            f"{t}: in-group n={in_n} ({in_pct:.1f}%), "
            f"out-group n={out_n} ({out_pct:.1f}%), raw OR={raw_or:.2f}"
        )

    try:
        model = BinomialBayesMixedGLM.from_formula(
            "perceives ~ in_group",
            {"re": "0 + C(respondent_id)"},
            data=long_df,
            vcp_p=1,
            fe_p=2,
        )
        result = model.fit_vb()
    except Exception:
        traceback.print_exc()
        return None

    print(result.summary())

    coef = result.fe_mean[1]
    sd = result.fe_sd[1]
    or_value = float(np.exp(coef))
    ci_low = float(np.exp(coef - 1.96 * sd))
    ci_high = float(np.exp(coef + 1.96 * sd))
    z = coef / sd
    p = 2.0 * norm.sf(abs(z))
    random_intercept_sd = float(np.exp(result.vcp_mean[0]))

    out_row = {
        "Parameter": "in_group",
        "OR": or_value,
        "CI_lower": ci_low,
        "CI_upper": ci_high,
        "p": p,
        "sig": sig_stars(p),
        "random_intercept_sd": random_intercept_sd,
    }
    pd.DataFrame([out_row]).to_csv(
        os.path.join(OUT_DIR, "sintonia_mixed_model.csv"), index=False
    )

    fig, ax = plt.subplots(figsize=(3, 3))
    ax.axvline(1, color="red", linestyle="--", linewidth=1)
    ax.set_xscale("log")
    ax.errorbar(
        [or_value],
        [0],
        xerr=[[or_value - ci_low], [ci_high - or_value]],
        fmt="o",
        color="#2c3e50",
        capsize=4,
    )
    ax.set_yticks([])
    ax.set_xlim(max(ci_low * 0.8, 0.05), ci_high * 1.2)
    ax.set_xlabel("Odds Ratio (log scale)")
    ax.annotate(
        f"OR = {or_value:.2f}\n95% CI [{ci_low:.2f}, {ci_high:.2f}]\np = {p:.3f}",
        xy=(or_value, 0),
        xytext=(or_value * 1.1, 0.6),
        fontsize=8,
    )
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "sintonia_forest_plot.png"), dpi=300)
    plt.close(fig)

    types = [b["type"] for b in breakdown]
    in_pcts = [b["in_pct"] for b in breakdown]
    out_pcts = [b["out_pct"] for b in breakdown]
    x = np.arange(len(types))
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(x - 0.2, in_pcts, width=0.4, color="tab:blue", label="In-Group")
    ax.bar(x + 0.2, out_pcts, width=0.4, color="tab:red", label="Out-Group")
    ax.set_xticks(x)
    ax.set_xticklabels(types)
    ax.set_ylim(0, 105)
    ax.set_ylabel("% Respondents Reporting")
    for i in range(len(types)):
        ax.text(x[i] - 0.2, (in_pcts[i] or 0) + 1.5, f"{in_pcts[i]:.1f}",
                ha="center", va="bottom", fontsize=9)
        ax.text(x[i] + 0.2, (out_pcts[i] or 0) + 1.5, f"{out_pcts[i]:.1f}",
                ha="center", va="bottom", fontsize=9)
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "sintonia_bar_chart.png"), dpi=300)
    plt.close(fig)

    return out_row


if __name__ == "__main__":
    main()