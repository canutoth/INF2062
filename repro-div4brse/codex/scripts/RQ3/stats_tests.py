import os
import re
from itertools import combinations

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, fisher_exact, norm

CSV_PATH = os.path.join("..", "..", "data", "analysis_i&d_up.csv")
OUT_DIR = os.path.join("..", "..", "results", "RQ3")

DISC_ORDER = ["Ageism", "Elitism", "Homophobia", "Racism", "Sexism", "Ableism"]
dimensions = ["Gender", "Sexuality", "Race", "Seniority", "Disabled status"]
DISC_COL = 39
Z_975 = norm.ppf(0.975)

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


def map_disabled_status(v):
    text = str(v).strip().lower()
    if text.startswith("sim"):
        return "Disabled"
    if "não" in text or "nao" in text:
        return "Not disabled"
    return None


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


def load_respondent_level():
    raw = pd.read_csv(CSV_PATH)
    df = raw.iloc[:, [5, 6, 7, 8, 13, DISC_COL]].copy()
    df.columns = ["gender", "sexuality", "race", "disability", "seniority", "disc"]

    df["Gender"] = df["gender"].apply(map_gender)
    df["Sexuality"] = df["sexuality"].apply(map_sexuality)
    df["Race"] = df["race"].apply(map_race)
    df["Seniority"] = df["seniority"].apply(map_seniority)
    df["Disabled status"] = df["disability"].apply(map_disabled_status)

    tags_per_respondent = df["disc"].apply(
        lambda v: [map_discrimination_type(t) for t in re.split(r",\s(?=\w+\s?\()", str(v))]
    )
    for t in DISC_ORDER:
        df[t] = [t in tags for tags in tags_per_respondent]

    profile_cols = dimensions.copy()
    keep = profile_cols + DISC_ORDER
    df[keep] = df[keep].replace("", np.nan)
    df = df.dropna(subset=["Gender"]).reset_index(drop=True)
    return df[keep]


def analyze_2x2(table):
    table = np.asarray(table, dtype=float)
    chi2, p, dof, expected = chi2_contingency(table, correction=False)
    _, p_yates, _, _ = chi2_contingency(table, correction=True)
    fisher_p = fisher_exact(table)[1]
    note = ""
    if (table == 0).any():
        note = "Haldane-Anscombe adjustment (+0.5) applied"
        table = table + 0.5
    a, b = table[0]
    c, d = table[1]
    if a * d > 0 and b * c >= 0:
        log_or = np.log(a * d / (b * c))
        se = np.sqrt(1 / a + 1 / b + 1 / c + 1 / d)
        odds_ratio = np.exp(log_or)
        ci_low = np.exp(log_or - Z_975 * se)
        ci_high = np.exp(log_or + Z_975 * se)
    else:
        odds_ratio = np.nan
        ci_low = np.nan
        ci_high = np.nan
    return {
        "chi2": chi2,
        "dof": dof,
        "p": p,
        "p_yates": p_yates,
        "fisher_p": fisher_p,
        "odds_ratio": odds_ratio,
        "ci_low": ci_low,
        "ci_high": ci_high,
        "expected_min": expected.min(),
        "note": note,
    }


def fmt_p(p):
    if p < 0.001:
        return "p < .001"
    return f"p = {p:.3f}".replace("0.", ".", 1)


def apa_result(chi2, dof, p, ci_low, ci_high, odds_ratio):
    return (
        f"χ²({dof}) = {chi2:.2f}, {fmt_p(p)}, "
        f"95% CI [{ci_low:.2f}, {ci_high:.2f}], OR ≈ {odds_ratio:.2f}"
    )


def main():
    respondents = load_respondent_level()

    # Headline: Gender x Sexism, Women first.
    gender = respondents["Gender"]
    sexism = respondents["Sexism"]
    women_yes = int(((gender == "Women") & sexism).sum())
    women_no = int(((gender == "Women") & ~sexism).sum())
    men_yes = int(((gender == "Men") & sexism).sum())
    men_no = int(((gender == "Men") & ~sexism).sum())
    headline_table = [[women_yes, women_no], [men_yes, men_no]]
    hr = analyze_2x2(headline_table)
    headline = apa_result(hr["chi2"], hr["dof"], hr["p"], hr["ci_low"], hr["ci_high"], hr["odds_ratio"])
    fisher_line = (
        f"Fisher exact p = {hr['fisher_p']:.3f}"
        if hr["fisher_p"] >= 0.001
        else "Fisher exact p < .001"
    )
    yates_line = (
        f"Yates-corrected p = {hr['p_yates']:.3f}"
        if hr["p_yates"] >= 0.001
        else "Yates-corrected p < .001"
    )
    title = "Gender x Sexism: recurrence of perceived sexism"
    print(title)
    print(headline)
    print(fisher_line)
    print(yates_line)
    print(f"Minimum expected frequency = {hr['expected_min']:.2f}")

    txt_path = os.path.join(OUT_DIR, "stats_gender_sexism.txt")
    with open(txt_path, "w") as f:
        f.write(title + "\n")
        f.write(headline + "\n")
        f.write(fisher_line + "\n")

    # All pairwise comparisons.
    rows = []
    for dim in dimensions:
        groups = sorted(respondents[dim].dropna().unique().tolist())
        for group_a, group_b in combinations(groups, 2):
            sub = respondents[respondents[dim].isin([group_a, group_b])]
            for disc_type in DISC_ORDER:
                a_mask = sub[dim] == group_a
                b_mask = sub[dim] == group_b
                a_yes = int((a_mask & sub[disc_type]).sum())
                a_no = int((a_mask & ~sub[disc_type]).sum())
                b_yes = int((b_mask & sub[disc_type]).sum())
                b_no = int((b_mask & ~sub[disc_type]).sum())
                n_a = a_yes + a_no
                n_b = b_yes + b_no
                pct_a = a_yes / n_a * 100 if n_a else np.nan
                pct_b = b_yes / n_b * 100 if n_b else np.nan
                res = analyze_2x2([[a_yes, a_no], [b_yes, b_no]])
                rows.append(
                    {
                        "dimension": dim,
                        "group_a": group_a,
                        "group_b": group_b,
                        "discrimination": disc_type,
                        "n_a": n_a,
                        "%a_report": pct_a,
                        "n_b": n_b,
                        "%b_report": pct_b,
                        "chi2": res["chi2"],
                        "dof": res["dof"],
                        "p": res["p"],
                        "p_fisher": res["fisher_p"],
                        "odds_ratio": res["odds_ratio"],
                        "ci_low": res["ci_low"],
                        "ci_high": res["ci_high"],
                        "min_expected": res["expected_min"],
                    }
                )

    pairwise = pd.DataFrame(rows)
    pairwise.to_csv(os.path.join(OUT_DIR, "pairwise_stats.csv"), index=False)
    print(pairwise.to_string())
    print(
        "\nCaveat: multiple-comparison correction (e.g. Bonferroni/Holm) "
        "should be applied when interpreting these non-planned pairwise tests."
    )


if __name__ == "__main__":
    main()