# Specification 08 — RQ7: Self-awareness of unconscious bias

Script: `scripts/RQ7/coding_bias.py`
Orchestrator flag: `--rq7`
Output directory: `results/RQ7/`

Visualizes the qualitative coding of answers to the survey question on whether the
respondent recognizes any bias in their own interpretation of words / questions /
experiences (column id.46 of `analysis_i&d_up.csv`).

## 1. Input
**None read at runtime.** The coded counts are hard-coded in the script as a nested
dict (category → subcategory → count). Reproduce this table verbatim:

| Category | Subcategory | n |
|---|---|---|
| Uncertainty | Unsure | 8 |
| Uncertainty | Unconscious | 3 |
| Denial | Not Recognized | 21 |
| Denial | Avoided | 2 |
| Recognition | Anti-diversity | 4 |
| Recognition | General Awareness | 8 |
| Recognition | Gender | 12 |
| Recognition | Racial | 10 |
| Recognition | LGBT | 4 |
| Recognition | Disability | 2 |
| Recognition | Age | 1 |
| Recognition | Religious | 2 |
| Recognition | Political | 6 |
| Recognition | Regional | 2 |
| Personal Experience | Work Environment | 6 |
| Personal Experience | Upbringing | 1 |
| Out of scope | Out of scope | 5 |

## 2. Processing
Flatten the dict to a DataFrame (`Category`, `Subcategory`, `Quantity`); map a colour per category:
`Uncertainty:#1f77b4`, `Denial:#ff7f0e`, `Recognition:#2ca02c`,
`Personal Experience:#d62728`, `Out of scope:#9467bd`.

## 3. Plot (`coding-bias.png`)
- `fig, ax = plt.subplots(figsize=(4,10))`.
- `ax.barh(df['Subcategory'], df['Quantity'], color=df['Color'])` — insertion order,
  first subcategory at the bottom.
- `ax.margins(y=0.01)`; ylabel `"Subcategories"` (14), xlabel `"Quantity"` (14); tick size 12.
- Legend from square `Line2D` markers, title `"Categories of Bias"`, `loc='upper right'`,
  fontsize 11 / title 13, framed, `borderpad=0.5`.
- `tight_layout()`; save `results/RQ7/coding-bias.png`, `dpi=300`, `bbox_inches='tight'`, then `plt.show()`.

## 4. Libraries
`matplotlib`, `pandas`, `os`. No stats, no seed, fully deterministic.
