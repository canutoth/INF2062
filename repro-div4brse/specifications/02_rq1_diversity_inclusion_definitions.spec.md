# Specification 02 — RQ1: How practitioners define *diversity & inclusion*

Scripts: `scripts/RQ1/coding_inclusion_diversity.py`, `scripts/RQ1/diversitycloud.py`
Orchestrator flag: `--rq1`
Output directory: `results/RQ1/`

RQ1 characterizes participants' open-text answers to *"O que você entende por
diversidade e inclusão?"* along two coded axes and as a word cloud.

---

## Part A — Coded-category bar chart (`coding_inclusion_diversity.py`)

### A.1 Input
- `data/coding_inclusion_diversity.csv`.
- Uses **column index 2** (`T` codes — *type* of definition) and **column index 3**
  (`C` codes — *content* of definition). Other columns ignored.
- Each cell may hold multiple comma-separated codes (e.g. `"C1, C3"`); blank cells dropped.

### A.2 Processing
1. `t_col = df.iloc[:,2].dropna()`, `c_col = df.iloc[:,3].dropna()`.
2. `count_tags`: split each cell on `,`, `strip()` each token, `value_counts()` over all tokens.
3. `all_counts = concat(t_counts, c_counts).sort_index()` (alphabetical by code).
4. Map codes to labels via `label_map`, then plot.

### A.3 Code → label map
| Code | Label | | Code | Label |
|---|---|---|---|---|
| T1 | Defines diversity only | | C1 | Demographic representation |
| T2 | Defines inclusion only | | C2 | Cognitive or experiential diversity |
| T3 | Defines diversity and inclusion separately | | C3 | Equal opportunity / equity |
| T4 | Defines diversity and inclusion complementarly | | C4 | Belonging and respect |
| T5 | Generic or vague definition | | C5 | Participation and voice |
| T6 | Blank/Out of context | | C6 | Organizational practices or policies |
| | | | C7 | Justice or anti-discrimination framing |
| | | | C8 | Meritocracy / skills-first framing |
| | | | C9 | Instrumental or business outcomes |
| | | | C10 | Hate Comments |

### A.4 Plot
- Horizontal bar chart, `figsize=(12,6)`, categories in `sort_index()` order (after label mapping).
- Bar color: `tab:blue` for `T*` categories, `tab:red` for `C*` categories
  (the upstream color list-comprehension is convoluted but resolves to this intent).
- Value label at the end of each bar (`int(width)`, fontsize 12, left-aligned).
- Legend (upper right, large): blue = "Type of Definition (T)", red = "Content of Definition (C)".
- Tick label size 14 on both axes. `tight_layout()`.
- Save: `results/RQ1/coding_inclusion_diversity.png`, `dpi=300`, `bbox_inches='tight'`. Then `plt.show()`.

---

## Part B — Word cloud (`diversitycloud.py`)

### B.1 Input
- `data/diversity_cloud.csv`; text = `" ".join(df.iloc[:,1].dropna().astype(str))` (column index 1).

### B.2 Processing / config
- Stopwords: `wordcloud.STOPWORDS` **plus** the custom list:
  `a, an, and, the, to, of, in, for, on, with, is, it, this, that, we, i, you, they,
  github, code, project, use, using, without, someone, based, people, person, etc, act, action`.
- `WordCloud(width=1200, height=900, background_color="white",
  stopwords=stopwords, random_state=42)`. Also set `np.random.seed(42)` after
  imports (Spec 00 §3).

### B.3 Plot / output
- `plt.imshow(wc)`, `plt.axis("off")`, `plt.tight_layout(pad=0)`.
- Save: `results/RQ1/diversitycloud.png`, `dpi=300`, `bbox_inches='tight'`. Then `plt.show()`.
- With `random_state=42` the layout is deterministic; upstream (unseeded) differs
  only in pixel placement.

## Libraries
`pandas`, `numpy` (seed), `matplotlib` (`matplotlib.patches.Patch`), `wordcloud`,
`os`. No stats.
