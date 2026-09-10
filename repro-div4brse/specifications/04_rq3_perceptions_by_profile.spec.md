# Specification 04 — RQ3: Perceived recurrence of discrimination **by demographic profile**

Scripts: `scripts/RQ3/profile.py`, `scripts/RQ3/sintonia.py`, `scripts/RQ3/stats_tests.py`
Orchestrator flag: `--rq3` (but see Spec 00 §5.1 — `stats_tests.py` is skipped by the
buggy `main.py`; run it directly)
Output directory: `results/RQ3/`

All three scripts read `data/analysis_i&d_up.csv` and share the Portuguese column
names and the category mappings in Spec 00 §4.1. The dependent variable throughout
is the multi-select field **"Qual(is) dos tipos de discriminação você acha que são
mais recorrentes dentro da área de desenvolvimento de software?"** (column id.39),
split with the regex `,\s(?=\w+\s?\()` and each item reduced to its type via
`val.split("(")[0].strip()` → English label.

---

## Script A — `profile.py` : profile × discrimination-type heatmap

### A.1 Processing
1. Keep columns: gender, sexuality, race, PCD, seniority, discrimination(id.39); `dropna()`.
2. `explode` the discrimination list → one row per (respondent, perceived type); `strip()`.
3. Derive aggregated profile columns:
   - `Gender Agg` (Men/Women), `Sexuality Agg` (Heterosexual/LGBTQ+),
     `Race Agg` (White/PoC), `Seniority Agg` (Intern/Junior/Mid-level/Senior).
   - `PCD`: `sim*` → `Disabled`, contains `não` → `Not disabled`, **else `Disabled`**.
   - `Disc Label`: type → {Ageism, Sexism, Homophobia, Racism, Elitism, Ableism}.
4. Build a long table stacking, for each profile dimension, `(Profile, Disc Label)` rows:
   gender, sexuality, race, seniority, PCD, plus a `Total (overall)` slice.
5. **Denominators**: recompute per-group respondent counts from a fresh, *un-exploded*
   read of the same CSV (`total_por_Profile[group] = #respondents in that group`);
   `Total (overall)` = `len(df_resp)`.
6. `counts = groupby([Profile, Disc Label]).size()`; `percent = count / denominator * 100`.
7. Pivot to matrix `index=Profile`, `columns=Disc Label`, values `percent`, `fill_value=0`.

### A.2 Plot (`profile.png`)
- Column order: `["Ableism","Ageism","Elitism","Homophobia","Racism","Sexism"]`.
- Row order: `["Women","Men","Heterosexual","LGBTQ+","White","PoC","Intern","Junior",
  "Mid-level","Senior","Not disabled","Disabled","Total (overall)"]`.
- `sns.heatmap`, `figsize=(10,7)`, `annot=True`, `fmt=".1f"`, `cmap="Reds"`,
  `linewidths=.5`, `annot_kws={'size':14}`, cbar label `"% of respondents"`.
- x-ticks horizontal, both tick sizes 12. `tight_layout()`.
- Save `results/RQ3/profile.png`, `dpi=300`, `bbox_inches='tight'`, then `plt.show()`.

---

## Script B — `sintonia.py` : in-group ("sintonia") mixed-effects model

Tests whether belonging to a targeted group raises the odds of perceiving the
matching discrimination type.

### B.1 Data prep
1. Read CSV; keep the 8 demographic cols + discrimination(id.39) + age; `dropna` on
   the 8 demographic cols only.
2. Derive: `Gender` (Men/Women), `LGBTQ+` (1/0), `Race` (PoC=1/White=0),
   `Disability` (1 if `sim*`, 0 if contains `não`, else `NaN`),
   `Seniority`, `Age` (`parse_age`: strip "anos", int, else NaN),
   `WorkModel`, `Sector`, `CompanySize`.
3. Explode discrimination → `DiscType`; build a per-respondent binary matrix
   `disc_binary` (1 if that type was selected). Keep only columns in
   `DISC_ORDER = ["Sexism","Ableism","Homophobia","Racism"]`.
4. `model_df` = demographics `join` `disc_binary` (inner);
   `dropna(subset=["Gender","LGBTQ+","Race","Disability","CompanySize"])` (reports rows dropped).

### B.2 Long format + `in_group`
For each of the 4 types, stack a copy with `perceives` = that type's 0/1 flag,
`disc_type` = the label, and `in_group` from `IN_GROUP_MAP`:
- Sexism → `Gender == "Women"`
- Ableism → `Disability == 1`
- Homophobia → `LGBTQ+ == 1`
- Racism → `Race == 1` (PoC)

`respondent_id` = row index range; result ≈ N respondents × 4 rows.

### B.3 Model
- Set `np.random.seed(42)` after imports (Spec 00 §3).
- `BinomialBayesMixedGLM.from_formula("perceives ~ in_group", {"re": "0 + C(respondent_id)"},
  data=long_df, vcp_p=1, fe_p=2)`, fit with `.fit_vb()` (variational Bayes).
  `fit_vb()` takes no seed argument; the global `np.random.seed(42)` plus the
  fixed `long_df` row order make the fit deterministic in practice.
- From the `in_group` fixed effect: `OR = exp(coef)`, 95% CI `exp(coef ± 1.96·sd)`,
  `z = coef/sd`, `p = 2·norm.sf(|z|)`, significance stars (`*** <.001, ** <.01, * <.05`).
- Random-intercept SD = `exp(result.vcp_mean[0])`.
- Per-type breakdown table: in-group n, in-group %, out-group %, raw OR.

### B.4 Outputs
- `results/RQ3/sintonia_mixed_model.csv` — one row: `Parameter, OR, CI_lower, CI_upper, p, sig, random_intercept_sd`.
- `results/RQ3/sintonia_forest_plot.png` — single-marker forest plot, log x-axis,
  `figsize=(3,3)`, dashed red line at OR=1, annotation with OR/CI/p, `dpi=300`.
- `results/RQ3/sintonia_bar_chart.png` — grouped bars, per type: In-Group (`tab:blue`)
  vs Out-Group (`tab:red`) `% Respondents Reporting`, `figsize=(6,5)`, `ylim 0–105`,
  value labels, `dpi=300`.
- Console prints the model summary; on fit failure it prints a traceback and returns `None`.

---

## Script C — `stats_tests.py` : frequentist 2×2 tests (χ², Fisher, OR)

### C.1 Respondent-level table (`load_respondent_level`)
- One row per respondent. Profile dims: `Gender`, `Sexuality`, `Race`, `Seniority`
  (via the maps), plus `Disabled status` (`sim*`→Disabled, `não`→Not disabled, else None).
- For each discrimination type in
  `DISC_ORDER = ["Ageism","Elitism","Homophobia","Racism","Sexism","Ableism"]`,
  a boolean column: `True` if that `Tipo` appears in the respondent's id.39 selections.
- Replace `""`→NaN in profile+disc columns; `dropna(subset=["Gender"])`; reset index.

### C.2 `analyze_2x2(table)` — `table = [[g1 yes, g1 no], [g2 yes, g2 no]]`
- Pearson χ² (`chi2_contingency`, `correction=False`) → `chi2, p, dof, expected`.
- Yates-corrected χ² p-value (`correction=True`).
- Fisher exact p-value (`stats.fisher_exact`).
- Odds ratio + 95% CI on log scale (`z = norm.ppf(0.975)`).
  If any cell is 0, apply **Haldane–Anscombe** +0.5 to every cell and note it.
- Returns dict: `chi2, dof, p, p_yates, fisher_p, odds_ratio, ci_low, ci_high, expected_min, note`.

### C.3 Runs
1. **Headline — Gender × Sexism**: build the 2×2 with **Women first**, print APA-style
   result (`χ²(dof)=…, p…, 95% CI […], OR ≈ …`), Fisher p, Yates p, min expected freq.
   Write `results/RQ3/stats_gender_sexism.txt` (title line, APA line, Fisher line).
2. **All pairwise** — for `dimensions = ["Gender","Sexuality","Race","Seniority","Disabled status"]`,
   every unordered group pair × every type in `DISC_ORDER`: build the 2×2, run
   `analyze_2x2`, collect a row (`dimension, group_a, group_b, discrimination, n_a,
   %a_report, n_b, %b_report, chi2, dof, p, p_fisher, odds_ratio, ci_low, ci_high, min_expected`).
   Write `results/RQ3/pairwise_stats.csv`. Print the full table + a caveat that
   multiple-comparison correction (Bonferroni/Holm) should be applied to non-planned tests.

### C.4 `fmt_p` / `apa_result`
APA style: `p < .001` when below threshold, else `p = .XXX` (leading zero stripped).

---

## Libraries (RQ3)
`pandas`, `numpy`, `matplotlib`, `seaborn` (profile.py), `scipy.stats`,
`statsmodels` (`statsmodels.genmod.bayes_mixed_glm.BinomialBayesMixedGLM`), `re`, `os`,
`warnings`, `itertools.combinations`.
`sintonia.py` resolves paths from `__file__`; `profile.py` and `stats_tests.py` use
`../../` relative paths (run from `scripts/RQ3/`).
