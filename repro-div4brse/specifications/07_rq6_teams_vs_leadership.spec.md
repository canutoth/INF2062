# Specification 07 — RQ6: Representation in **development teams vs. leadership roles**

Scripts: `scripts/RQ6/teams.py`, `scripts/RQ6/leaders.py`
Orchestrator flag: `--rq6`
Output directory: `results/RQ6/`

Two near-identical scripts: one for team-level inclusion, one for leadership-level
encouragement. Each renders a diverging stacked-bar chart of 4-point Likert
agreement across five demographic groups.

## 1. Input
| Script | File | Output |
|---|---|---|
| `teams.py` | `data/data_teams.csv` | `results/RQ6/team-level.png` |
| `leaders.py` | `data/data_leadership.csv` | `results/RQ6/leadership_level.png` |

Both files: 220 rows, `ID` + Likert columns (integer **1–4**, some cells blank)
`['Race/Ethnicity', 'Gender/Sexuality', 'Neurodivergency', 'Disability', 'Elderly']`.
Scale: 1 = Strongly Disagree, 2 = Disagree, 3 = Agree, 4 = Strongly Agree.

## 2. Processing
1. `likert_counts = df[likert_cols].apply(lambda x: x.value_counts(normalize=True)).fillna(0)`.
2. `reindex(index=[1,2,3,4])`, `* 100`, transpose → rows = questions, cols = 1..4.
3. `neg = -likert_perc[[1, 2]]` (negative side), `pos = likert_perc[[3, 4]]` (positive side).

## 3. Plot (identical spec for both)
- `fig, ax = plt.subplots(figsize=(10,7))`.
- Colors: `1:"#d90000"`, `2:"#fc7e7e"`, `3:"#a6d96a"`, `4:"#1a9641"`.
- Negative stack: `ax.barh` for `col` in `[2, 1]`, `left` accumulates `neg[col]`, `height=0.6`.
- Positive stack: `ax.barh` for `col` in `[3, 4]`, `left` accumulates `pos[col]`, `height=0.6`.
- `ax.axvline(0, color='black', linewidth=0.8)`; xlabel `"% of Respondents"`;
  title `"Diverging Stacked-Bar Chart of Likert Responses"`.
- Legend from `Patch` handles (Strongly Disagree / Disagree / Agree / Strongly Agree),
  `loc='upper center'`, `bbox_to_anchor=(0.5, -0.1)`, `ncol=4`, fontsize 12.
- Tick label size 12 both axes; `ax.margins(x=0.01, y=0.05)`; `ax.invert_yaxis()`
  (first question on top). `tight_layout()`.
- Save `dpi=300`, `bbox_inches='tight'`, then `plt.show()`.

## 4. Libraries
`pandas`, `numpy`, `matplotlib` (`matplotlib.patches.Patch`), `os`. No stats, no seed.
Run from `scripts/RQ6/` (`../../` paths).
