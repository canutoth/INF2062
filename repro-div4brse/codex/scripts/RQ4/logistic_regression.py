import os
import re
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "..", "data", "analysis_i&d_up.csv")
OUT_DIR = os.path.join(SCRIPT_DIR, "..", "..", "results", "RQ4")

DEMOGRAPHIC_COLS = [5, 6, 7, 8, 11, 13, 15, 16]
DISC_COL = 39
DISC_ORDER = ["Sexism", "Racism", "Homophobia", "Ableism", "Ageism", "Elitism"]
PREDICTOR_ORDER = [
    "Gender_Women",
    "LGBTQ+",
    "Race",
    "Disability",
    "CompanySize_Big",
    "Seniority_Junior",
    "Seniority_Mid-level",
    "Seniority_Senior",
    "WorkModel_Remote",
    "WorkModel_Hybrid",
    "Sector_Private",
    "Sector_Startup",
    "Sector_Non-profit / NGO",
]
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
    "Sector_Non-profit / NGO": "Sector: Non-profit",
}

os.makedirs(OUT_DIR, exist_ok=True)


def map_gender(v):
    mapping = {
        "homem cisgênero": "Men",
        "homem trans": "Men",
        "mulher cisgênero": "Women",
        "mulher trans": "Women",
    }
    return mapping.get(str(v).strip().lower(), np.nan)


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
        return "Non-profit / NGO"
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


def make_dummies(series, prefix, reference):
    dummies = pd.get_dummies(series, prefix=prefix, dtype=int)
    drop_col = f"{prefix}_{reference}"
    if drop_col in dummies.columns:
        dummies = dummies.drop(columns=[drop_col])
    return dummies


def sig_stars(p):
    if p < 0.001:
        return "***"
    if p < 0.01:
        return "**"
    if p < 0.05:
        return "*"
    return ""


def fit_model(y, X):
    try:
        res = sm.Logit(y, X).fit(disp=0, maxiter=100)
        converged = getattr(res, "mle_retvals", {}).get("converged", True)
        if not converged:
            raise RuntimeError("non-convergence")
    except Exception:
        res = sm.Logit(y, X).fit_regularized(disp=0, maxiter=200, L1_wt=0.0)
    return res


def plot_forest(ax, or_table, x_min, x_max, title):
    y = np.arange(len(or_table))
    ax.axvline(1, color="red", linestyle="--", linewidth=1)
    ax.errorbar(
        or_table["OR"],
        y,
        xerr=[
            or_table["OR"] - or_table["CI_lower"],
            or_table["CI_upper"] - or_table["OR"],
        ],
        fmt="o",
        color="#2c3e50",
        capsize=3,
    )
    ax.set_yticks(y)
    ax.set_yticklabels(or_table.index)
    ax.invert_yaxis()
    ax.set_xscale("log")
    ax.set_xlim(x_min, x_max)
    ax.set_title(title)


def main():
    raw = pd.read_csv(DATA_PATH)
    df = raw.iloc[:, DEMOGRAPHIC_COLS + [DISC_COL]].copy()
    df.columns = [
        "gender",
        "sexuality",
        "race",
        "disability",
        "work_model",
        "seniority",
        "sector",
        "company_size",
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

    predictors = pd.DataFrame(index=df.index)
    predictors["Gender_Women"] = df["gender"].apply(map_gender).map({"Women": 1, "Men": 0}).astype(float)
    predictors["LGBTQ+"] = df["sexuality"].apply(map_sexuality_id).astype(float)
    predictors["Race"] = df["race"].apply(map_race_id).astype(float)
    predictors["Disability"] = df["disability"].apply(map_disability).astype(float)
    predictors["CompanySize_Big"] = df["company_size"].apply(map_company_size).map({"Big": 1, "Small": 0}).astype(float)

    seniority = df["seniority"].apply(map_seniority)
    work_model = df["work_model"].apply(map_work_model)
    sector = df["sector"].apply(map_sector)

    predictors = pd.concat(
        [
            predictors,
            make_dummies(seniority, "Seniority", "Intern"),
            make_dummies(work_model, "WorkModel", "On-site"),
            make_dummies(sector, "Sector", "Public"),
        ],
        axis=1,
    )
    predictors = predictors[PREDICTOR_ORDER]

    tags = df["disc"].apply(lambda v: re.split(r",\s(?=\w+\s?\()", str(v)))
    types = tags.apply(lambda lst: [map_discrimination_type(t) for t in lst])
    disc_binary = pd.DataFrame(0, index=df.index, columns=DISC_ORDER, dtype=int)
    for t in DISC_ORDER:
        disc_binary[t] = [1 if t in row_types else 0 for row_types in types]

    model_df = predictors.join(disc_binary, how="inner")
    n_before = len(model_df)
    model_df = model_df.dropna(subset=PREDICTOR_ORDER)
    n_after = len(model_df)
    print(
        f"Respondents before dropna: {n_before}; after dropna: {n_after} "
        f"(rows_dropped={n_before - n_after})"
    )

    fitted = []
    for disc_type in DISC_ORDER:
        if disc_type not in model_df.columns:
            print(f"Warning: column {disc_type} absent; skipping.")
            continue
        events = int(model_df[disc_type].sum())
        if events < 5:
            print(f"Warning: {disc_type} has only {events} events (< 5); skipping.")
            continue

        y = model_df[disc_type].astype(int)
        X = sm.add_constant(model_df[PREDICTOR_ORDER])

        try:
            res = fit_model(y, X)
        except Exception as exc:
            print(f"Warning: {disc_type} model failed ({exc}); skipping.")
            continue

        try:
            conf = np.asarray(res.conf_int())
        except Exception:
            conf = np.column_stack(
                [res.params - 1.96 * res.bse, res.params + 1.96 * res.bse]
            )

        mask = res.params.index != "const"
        or_table = pd.DataFrame(
            {
                "OR": np.exp(res.params[mask]),
                "CI_lower": np.exp(conf[mask, 0]),
                "CI_upper": np.exp(conf[mask, 1]),
                "p": res.pvalues[mask],
            }
        )
        or_table["sig"] = or_table["p"].apply(sig_stars)
        or_table.index = [
            DISPLAY_LABELS[name] for name in res.params.index[mask]
        ]
        or_table.index.name = "Predictor"

        print(f"\n=== {disc_type} ===")
        print(or_table.to_string())
        mcfadden = 1 - res.llf / res.llnull if res.llnull else np.nan
        print(f"McFadden R² = {mcfadden:.4f}")
        print(f"Log-likelihood = {res.llf:.2f}")
        try:
            print(f"LLR p-value = {res.llr_pvalue:.4f}")
        except Exception:
            print("LLR p-value = N/A")

        or_table.to_csv(os.path.join(OUT_DIR, f"odds_ratios_{disc_type}.csv"))

        fitted.append((disc_type, or_table))

    if not fitted:
        return

    all_rows = []
    for disc_type, or_table in fitted:
        table = or_table.copy()
        table.insert(0, "Discrimination", disc_type)
        all_rows.append(table)
    pd.concat(all_rows).to_csv(os.path.join(OUT_DIR, "odds_ratios_all.csv"))

    all_lower = [table["CI_lower"].min() for _, table in fitted]
    all_upper = [table["CI_upper"].max() for _, table in fitted]
    x_min = max(min(all_lower), 0.05)
    x_max = max(all_upper) * 1.15

    for disc_type, or_table in fitted:
        fig, ax = plt.subplots(figsize=(8, 5))
        plot_forest(ax, or_table, x_min, x_max, disc_type)
        ax.set_xlabel("Odds Ratio (log scale)")
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR, f"forest_plot_{disc_type}.png"), dpi=300)
        plt.close(fig)

    fig, axes = plt.subplots(2, 3, figsize=(18, 10))
    axes = axes.flatten()
    for i, (disc_type, or_table) in enumerate(fitted):
        plot_forest(axes[i], or_table, x_min, x_max, disc_type)
    for j in range(len(fitted), len(axes)):
        axes[j].axis("off")
    fig.suptitle(
        "Adjusted Odds Ratios — Logistic Regression per Discrimination Type",
        fontsize=16,
    )
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, "forest_plot_all.png"), dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()