"""RQ3 Script C — frequentist 2x2 tests on the profile x discrimination table.

Specification 04 §C. Pearson and Yates-corrected chi-square, Fisher exact test
and odds ratios with 95% CIs, for the headline Gender x Sexism contrast and for
every unordered group pair on every profile dimension.

Run from `scripts/RQ3/` (`python stats_tests.py`). Note Spec 00 §5.1: the
upstream `main.py` never reaches this script.
"""

import os
import re
import warnings
from itertools import combinations

import numpy as np
import pandas as pd
from scipy import stats

warnings.filterwarnings("ignore")

DATA_PATH = "../../data/analysis_i&d_up.csv"
OUTPUT_DIR = "../../results/RQ3"

# Column indexes in the raw Google-Forms export (Spec 00 §4).
COL_GENDER = 5
COL_SEXUALITY = 6
COL_RACE = 7
COL_PCD = 8
COL_SENIORITY = 13
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
DISC_ORDER = ["Ageism", "Elitism", "Homophobia", "Racism", "Sexism", "Ableism"]

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

DIMENSIONS = ["Gender", "Sexuality", "Race", "Seniority", "Disabled status"]


def norm(value):
    return str(value).strip().lower()


def map_disabled(value):
    v = norm(value)
    if v.startswith("sim"):
        return "Disabled"
    if "não" in v:
        return "Not disabled"
    return None


def selected_types(value):
    types = set()
    for item in re.split(SPLIT_PATTERN, str(value)):
        tipo = item.split("(")[0].strip()
        if tipo in DISC_MAP:
            types.add(DISC_MAP[tipo])
    return types


def load_respondent_level():
    """One row per respondent: profile dimensions + one boolean per disc type."""
    raw = pd.read_csv(DATA_PATH)

    df = pd.DataFrame(index=raw.index)
    df["Gender"] = raw.iloc[:, COL_GENDER].map(lambda v: GENDER_MAP.get(norm(v)))
    df["Sexuality"] = raw.iloc[:, COL_SEXUALITY].map(lambda v: SEXUALITY_MAP.get(norm(v)))
    df["Race"] = raw.iloc[:, COL_RACE].map(lambda v: RACE_MAP.get(norm(v)))
    df["Seniority"] = raw.iloc[:, COL_SENIORITY].map(lambda v: SENIORITY_MAP.get(norm(v)))
    df["Disabled status"] = raw.iloc[:, COL_PCD].map(map_disabled)

    picks = raw.iloc[:, COL_DISC].map(selected_types)
    for disc_type in DISC_ORDER:
        df[disc_type] = picks.map(lambda s, t=disc_type: t in s)

    df[DIMENSIONS + DISC_ORDER] = df[DIMENSIONS + DISC_ORDER].replace("", np.nan)
    df = df.dropna(subset=["Gender"]).reset_index(drop=True)
    return df


def analyze_2x2(table):
    """`table = [[g1 yes, g1 no], [g2 yes, g2 no]]`."""
    table = np.asarray(table, dtype=float)
    note = ""

    chi2, p, dof, expected = stats.chi2_contingency(table, correction=False)
    _, p_yates, _, _ = stats.chi2_contingency(table, correction=True)
    _, fisher_p = stats.fisher_exact(table)

    counts = table.copy()
    if (counts == 0).any():
        counts = counts + 0.5
        note = "Haldane-Anscombe correction (+0.5 to every cell)"

    odds_ratio = (counts[0, 0] * counts[1, 1]) / (counts[0, 1] * counts[1, 0])
    log_or = np.log(odds_ratio)
    se = np.sqrt((1 / counts).sum())
    z = stats.norm.ppf(0.975)
    ci_low = float(np.exp(log_or - z * se))
    ci_high = float(np.exp(log_or + z * se))

    return {
        "chi2": float(chi2),
        "dof": int(dof),
        "p": float(p),
        "p_yates": float(p_yates),
        "fisher_p": float(fisher_p),
        "odds_ratio": float(odds_ratio),
        "ci_low": ci_low,
        "ci_high": ci_high,
        "expected_min": float(expected.min()),
        "note": note,
    }


def fmt_p(p, threshold=0.001):
    if p < threshold:
        return "p < .001"
    return "p = " + f"{p:.3f}".lstrip("0")


def apa_result(res):
    return (
        f"chi2({res['dof']}) = {res['chi2']:.2f}, {fmt_p(res['p'])}, "
        f"95% CI [{res['ci_low']:.2f}, {res['ci_high']:.2f}], "
        f"OR ~ {res['odds_ratio']:.2f}"
    )


def build_table(df, dimension, group_a, group_b, disc_type):
    rows = []
    for group in (group_a, group_b):
        subset = df[df[dimension] == group]
        yes = int(subset[disc_type].sum())
        rows.append([yes, len(subset) - yes])
    return rows


def headline_gender_sexism(df):
    print("=" * 72)
    print("Headline test — Gender x Sexism (Women first)")
    print("=" * 72)

    table = build_table(df, "Gender", "Women", "Men", "Sexism")
    res = analyze_2x2(table)

    n_women = table[0][0] + table[0][1]
    n_men = table[1][0] + table[1][1]
    pct_women = table[0][0] / n_women * 100 if n_women else float("nan")
    pct_men = table[1][0] / n_men * 100 if n_men else float("nan")

    apa = apa_result(res)
    fisher_line = f"Fisher exact: {fmt_p(res['fisher_p'])}"

    print(f"Women: {table[0][0]}/{n_women} ({pct_women:.1f}%) report Sexism")
    print(f"Men:   {table[1][0]}/{n_men} ({pct_men:.1f}%) report Sexism")
    print(apa)
    print(fisher_line)
    print(f"Yates-corrected: {fmt_p(res['p_yates'])}")
    print(f"Minimum expected frequency: {res['expected_min']:.2f}")
    if res["note"]:
        print(f"Note: {res['note']}")

    path = os.path.join(OUTPUT_DIR, "stats_gender_sexism.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("Gender x Sexism — perceived recurrence of sexism in software development\n")
        fh.write(apa + "\n")
        fh.write(fisher_line + "\n")
    print(f"Written: {path}")
    return res


def all_pairwise(df):
    print()
    print("=" * 72)
    print("All pairwise 2x2 tests")
    print("=" * 72)

    rows = []
    for dimension in DIMENSIONS:
        groups = [g for g in df[dimension].dropna().unique()]
        groups = sorted(groups)
        for group_a, group_b in combinations(groups, 2):
            for disc_type in DISC_ORDER:
                table = build_table(df, dimension, group_a, group_b, disc_type)
                n_a = table[0][0] + table[0][1]
                n_b = table[1][0] + table[1][1]
                if n_a == 0 or n_b == 0:
                    continue
                res = analyze_2x2(table)
                rows.append(
                    {
                        "dimension": dimension,
                        "group_a": group_a,
                        "group_b": group_b,
                        "discrimination": disc_type,
                        "n_a": n_a,
                        "pct_a_report": table[0][0] / n_a * 100,
                        "n_b": n_b,
                        "pct_b_report": table[1][0] / n_b * 100,
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

    results = pd.DataFrame(rows)
    path = os.path.join(OUTPUT_DIR, "pairwise_stats.csv")
    results.to_csv(path, index=False)

    with pd.option_context("display.max_rows", None, "display.width", 220):
        print(results.round(4).to_string(index=False))
    print(f"Written: {path}")
    print()
    print(
        "CAVEAT: only the Gender x Sexism contrast is a planned comparison. The "
        "remaining tests are exploratory and a multiple-comparison correction "
        "(Bonferroni or Holm) should be applied before interpreting their p-values."
    )
    return results


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    df = load_respondent_level()
    print(f"Respondents in the respondent-level table: {len(df)}")
    headline_gender_sexism(df)
    all_pairwise(df)


if __name__ == "__main__":
    main()
