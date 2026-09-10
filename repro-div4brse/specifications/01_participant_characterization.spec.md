# Specification 01 — Participant Characterization

Script: `scripts/participant_characterization/characterization.py`
Orchestrator flag: `--characterization`

## 1. Purpose
Produce one bar chart per demographic/professional attribute describing the 220-participant sample.

## 2. Input
- `data/participant-characterization.csv` (read as `../../data/participant-characterization.csv`).
- 220 data rows. Columns: `ID`, `Region`, `Gender`, `Sexuality`, `Race`, `Disabled`,
  `Education`, `Work Model`, `Seniority`, `Industry Sector`, `Company size`.
- Values are already English categorical labels; **no cleaning, mapping, or NA handling** is applied.

## 3. Processing
1. Columns to analyze = every column except `ID`.
2. For each column:
   - `value_counts()` (descending by count) and matching percentages `count / 220 * 100`.
   - **Reorder** so any label containing `"Others"` or `"don't know"` is pushed to the end,
     preserving the count order of the rest.
3. No aggregation across columns; each chart is independent.

## 4. Plot spec (per column)
- Vertical bar chart, one bar per category.
- Figure width = `max(8, n_bars * 1.2)`, height = 6. Bar width 0.6.
- Palette (cycled, in order):
  `#4285F4, #EA4335, #FBBC04, #34A853, #FF6D01, #46BDC6, #7BAAF7, #F07B72`.
- X axis: ticks removed (no category labels on axis).
- Y axis: label `"Number of Participants"` (fontsize 14), fixed limits `0–220`.
- Per-bar annotation above the bar: `"{count}\n({pct:.1f}%)"`, bold, fontsize 12.
- Legend (upper right, fontsize 16, framed, fancybox, shadow): color swatch per
  category using `plt.Rectangle` handles with black edge; labels = category names.
- Dashed y-grid at alpha 0.3, drawn below bars.
- `plt.tight_layout()`.

## 5. Outputs
Directory: `results/participant_characterization/` (created if missing).

One PNG per analyzed column, `dpi=300`, `bbox_inches='tight'`, filename =
`column.replace("/", "-").replace(" ", "_").lower() + ".png"`:

`region.png`, `gender.png`, `sexuality.png`, `race.png`, `disabled.png`,
`education.png`, `work_model.png`, `seniority.png`, `industry_sector.png`,
`company_size.png`.

Figures are closed with `plt.close()` after saving (no `plt.show()`).

> The two PDFs under `results/participant_characterization/`
> (`..._graphics.pdf`, `..._table.pdf`) are **not** produced by this script and are out of scope.

## 6. Libraries
`pandas`, `matplotlib`, `seaborn` (imported; `os`). No stats.
