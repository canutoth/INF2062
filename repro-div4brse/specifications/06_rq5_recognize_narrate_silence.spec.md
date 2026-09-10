# Specification 06 — RQ5: Workplace discrimination — *Recognize, Narrate, Silence*

Script: `scripts/RQ5/intersection.py`
Orchestrator flag: `--rq5`
Output directory: `results/RQ5/`

Analyzes the discourse strategy participants use when asked whether they
witnessed/experienced differential treatment (Q28, Yes/No) and, if yes, to
describe it (Q29, free text), broken down by intersecting identities.

## 1. Input
`data/q28_q29.csv` (220 rows; `29` free-text may contain embedded newlines). Columns:
`ID, Region, Gender, Sexuality, Race, Disabled, Seniority, 28, 29, report_type, report_category`.
- `28` ∈ {Yes, No}; `29` free text or `none`/`N/A`.
- `report_type` ∈ {`1S` (first-person), `3S` (third-person), `N/A`}.
- `report_category` = comma-separated discrimination labels (e.g. `"Ableism, Sexism"`) or `N/A`.
- The literal string `"Others/I don't know"` marks the excluded identity bucket.

## 2. Q28 bar charts (percent, by identity)
For each of Gender / Sexuality / Race / Disabled: filter out rows whose value is
`"Others/I don't know"`, then `sns.countplot(data=…, x='28', stat="percent", hue=<identity>)`.

| Output | dpi | notes |
|---|---|---|
| `results/RQ5/bar_q28_gen.png` | 300 | `bbox_inches='tight'` |
| `results/RQ5/bar_q28_se.png` | default | `bbox_inches="tight"` |
| `results/RQ5/bar_q28_race.png` | default | `bbox_inches="tight"` |
| `results/RQ5/bar_q28_dis.png` | 300 | `bbox_inches='tight'` |

> Upstream does **not** clear the figure between these `countplot` calls, so each
> plot is drawn over the previous axes. Reproduce as-is unless the reproduction
> brief asks for the fix (`plt.figure()` / `plt.clf()` before each).

## 3. Discourse-strategy derivation
1. `df['28'] = df['28'].str.lower()`; `df['29'] = df['29'].astype(str).str.lower()`.
2. `discourse_strategy(row)`:
   - `28 == 'no'` → `no_recognition`
   - `28 == 'yes'` and `29 in {'none','nan'}` → `recognized_no_narrative`
   - `28 == 'yes'` and `report_type == '3S'` → `third_person`
   - `28 == 'yes'` and `report_type == '1S'` → `first_person`
   - else → `NaN`
3. `bar_discourse.png`: `sns.countplot(df, x='28', stat="percent", hue="discourse_strategy")`,
   `bbox_inches="tight"`.

## 4. Discourse strategy × identity heatmap (`heatmap29_dis.png`)
- `identity_columns = ['Disabled','Gender','Race','Seniority','Sexuality']`.
- `melt` to long (`identity_dimension`, `identity_group`); drop `identity_group == "Others/I don't know"`.
- `identity_label = dimension + ": " + group`.
- `pd.crosstab(identity_label, discourse_strategy, normalize='index')`, reindexed to
  column order `['no_recognition','recognized_no_narrative','third_person','first_person']`.
- Relabel index via `label_map` (`Gender: Woman`→`Women`, `Race: Non-white`→`Non-white`,
  `Disabled: No`→`Not disabled`, etc.).
- `sns.heatmap(contingency*100, annot=True, fmt=".1f", cmap="Reds", vmax=80,
  cbar_kws={"label": "% of responses"})`, `figsize=(10,6)`, blank axis labels,
  `tight_layout()`. Save `bbox_inches="tight"`, then `plt.show()`.

## 5. Report-category analysis
1. `report_category_clean` = `report_category` → fillna('') → str → lower → strip.
2. `df_clean` = rows with non-empty clean category; `report_category_list` = split on `", "`, drop empties.
3. **Category distribution bar** (`Counter` over flattened tags → % of total occurrences):
   `plt.bar`, `figsize=(8,5)`, ylabel `"Percentage (%)"`, x-ticks 45° right, title
   *"Distribution of Discrimination Categories"*. Save `results/RQ5/barplot_cat.png`
   (`bbox_inches="tight"`). *Not committed upstream — regenerated on run.*
4. **Category × identity heatmap** (`heatmap29_cat.png`): `explode` `report_category_list`,
   `melt` over the same `identity_columns`, drop NaN + `"Others/I don't know"`,
   `crosstab(..., normalize='index')`, relabel, `sns.heatmap(*100, annot, fmt=".1f",
   cmap="Reds", vmax=80)`, `figsize=(10,6)`, `bbox_inches="tight"`, `plt.show()`.
5. **UpSet plot** (`useplot_cat2.png`): `from_memberships(df_clean['report_category_list'])`,
   coerce the MultiIndex to tuples of `bool`, `UpSet(data, subset_size="count",
   show_counts=True, facecolor="tab:blue", sort_by="cardinality")`, `.plot()`,
   suptitle *"Intersections Between Report Categories"* (bold, `y=0.98`),
   `tight_layout(rect=[0,0,1,0.95])`, save `bbox_inches="tight"`, `plt.show()`.

## 6. Libraries
`pandas`, `numpy`, `matplotlib`, `seaborn`, `upsetplot` (`from_memberships`, `UpSet`),
`collections.Counter`, `os`. Run from `scripts/RQ5/` (`../../` paths). No seed; UpSet /
countplot ordering is deterministic given the data.
