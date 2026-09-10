# Specification 05 — RQ4: Perceived recurrence of discrimination **by organizational setting**

Scripts: `scripts/RQ4/company.py`, `scripts/RQ4/logistic_regression.py`
Orchestrator flag: `--rq4`
Output directory: `results/RQ4/`

Both scripts read `data/analysis_i&d_up.csv`, reuse Spec 00 §4.1 mappings, and use
the same discrimination multi-select field (id.39) as the outcome.

---

## Script A — `company.py` : organization-profile × discrimination-type heatmap

Same shape as RQ3 `profile.py` but the profile dimensions are organizational.

### A.1 Processing
1. Keep columns: work model (id.11), sector (id.15), company size (id.16),
   discrimination (id.39); `dropna()`.
2. `explode` discrimination list; `strip()`; map each item → English label
   (`mapear_discriminacao`).
3. Map the 3 org columns (lowercase/strip):
   - work model → On-site / Remote / Hybrid, unmapped → `Others`.
   - sector → Public / Private / `Non-profit / NGO` / Startup, unmapped → `Others`.
   - size → `Small company` / `Big company`, unmapped → `Others`.
4. Stack `(Perfil, Discriminação Label)` rows for model, sector, size, plus a
   `Total (overall)` slice.
5. **Denominators** recomputed from a fresh un-exploded read: per distinct value of
   each org column, `#respondents`; `Total (overall)` = `len(df_resp)`.
6. `groupby([Perfil, Label]).size()`; `percent = count / denominator * 100`; pivot.

### A.2 Plot (`company.png`)
- Column order `["Ableism","Ageism","Elitism","Homophobia","Racism","Sexism"]`.
- Row order `["Big company","Small company","On-site","Remote","Hybrid","Public",
  "Private","Non-profit / NGO","Total (overall)"]` (rows not present → NaN).
- `sns.heatmap`, `figsize=(10,7)`, `annot=True`, `fmt=".1f"`, `cmap="Reds"`,
  `linewidths=.5`, `annot_kws={'size':14}`, cbar label `"% of respondents"`,
  x-ticks horizontal, tick size 12. `tight_layout()`.
- Save `results/RQ4/company.png`, `dpi=300`, `bbox_inches='tight'`, then `plt.show()`.

---

## Script B — `logistic_regression.py` : adjusted odds ratios per discrimination type

### B.1 Data prep
1. Keep the 8 demographic cols + discrimination (id.39); `dropna` on the 8 demographic cols.
2. Derive predictors:
   - `Gender` (Men/Women) → `Gender_Women` (1/0).
   - `LGBTQ+` (1/0), `Race` (PoC=1/White=0),
     `Disability` (1 if `sim*`, 0 if `não`, else NaN).
   - `CompanySize` (Small/Big) → `CompanySize_Big` (1/0).
   - Dummy sets (reference dropped): `Seniority` (ref **Intern**),
     `WorkModel` (ref **On-site**), `Sector` (ref **Public**); all cast to int.
3. Explode discrimination → per-respondent binary matrix `disc_binary`; inner-join to predictors.
4. `PREDICTORS` = `Gender_Women, LGBTQ+, Race, Disability, CompanySize_Big` +
   seniority dummies + workmodel dummies + sector dummies.
   `dropna(subset=PREDICTORS)` (reports rows dropped, e.g. non-binary / prefer-not-to-say).

### B.2 Model loop
For each `disc_type` in `DISC_ORDER = ["Sexism","Racism","Homophobia","Ableism","Ageism","Elitism"]`:
- Skip if the column is absent or `events < 5` (print a warning).
- `y = model_df[disc_type]` (int); `X = sm.add_constant(model_df[PREDICTORS])`.
- Fit `sm.Logit(y, X).fit(disp=0, maxiter=100)`; on failure retry
  `fit_regularized(disp=0, maxiter=200, L1_wt=0.0)`; on second failure skip.
- Build OR table (drop `const`): `OR = exp(param)`, CI = `exp(conf_int)`, `p`, sig stars.
  Rename predictors to display labels (`Gender: Women`, `LGBTQ+: Yes`, `Race: PoC`,
  `Disabled`, `Company: Big`, `Seniority: Junior/Mid-level/Senior`,
  `Work Model: Remote/Hybrid`, `Sector: Private/Startup/Non-profit`).
- Console: per-model table + `McFadden R²`, log-likelihood, LLR p-value.

### B.3 Outputs
- `results/RQ4/odds_ratios_<type>.csv` per fitted type (index `Predictor`;
  cols `OR, CI_lower, CI_upper, p, sig`).
- `results/RQ4/odds_ratios_all.csv` — concatenation with a leading `Discrimination` column.
- `results/RQ4/forest_plot_<type>.png` per type — horizontal forest plot, **shared
  log x-axis** across all types (`x_min = max(min CI_lower, 0.05)`,
  `x_max = max CI_upper · 1.15`), markers `o` colour `#2c3e50`, dashed red line at
  OR=1, y-axis inverted, `figsize=(8,5)`, `dpi=300`.
- `results/RQ4/forest_plot_all.png` — combined 2×3 grid (`figsize=(18,10)`), suptitle
  *"Adjusted Odds Ratios — Logistic Regression per Discrimination Type"*, unused cells hidden, `dpi=300`.

## Libraries (RQ4)
`pandas`, `numpy`, `matplotlib`, `seaborn` (company.py), `statsmodels.api`, `re`, `os`, `warnings`.
`logistic_regression.py` resolves paths from `__file__`; `company.py` uses `../../` (run from `scripts/RQ4/`).
