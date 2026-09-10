# Specification 03 — RQ2: How practitioners define *prejudice & discrimination*

Scripts: `scripts/RQ2/coding_discrimination_prejudice.py`, `scripts/RQ2/discriminationcloud.py`
Orchestrator flag: `--rq2`
Output directory: `results/RQ2/`

Structurally identical to RQ1 (Spec 02) but over the answer to *"O que você entende
por discriminação e preconceito?"* with a different code vocabulary.

---

## Part A — Coded-category bar chart (`coding_discrimination_prejudice.py`)

### A.1 Input
- `data/coding_discrimination_prejudice.csv`; **column index 2** = `T` codes, **column index 3** = `C` codes (comma-separated allowed), NA dropped.

### A.2 Processing
Identical to Spec 02 §A.2: `count_tags` (split on `,`, strip, `value_counts`),
`concat(t_counts, c_counts).sort_index()`, then label mapping.

### A.3 Code → label map
| Code | Label | | Code | Label |
|---|---|---|---|---|
| T1 | Defines prejudice only | | C1 | Prior judgment or stereotyping |
| T2 | Defines discrimination only | | C2 | Bias or personal preference |
| T3 | Defines prejudice and discrimination separately | | C3 | Unequal or unfair treatment |
| T4 | Defines prejudice and discrimination complementarly | | C4 | Exclusion or denial of opportunities |
| T5 | Generic or vague definition | | C5 | Harassment, humiliation, or microaggressions |
| T6 | Blank/Out of context | | C6 | Targeted groups or social dimensions |
| | | | C7 | Structural or systemic factors |
| | | | C8 | Equality, fairness, or rights framing |
| | | | C9 | Intent versus impact or moral judgment |
| | | | C10 | Meritocracy or skills-first framing |
| | | | C11 | Reverse discrimination or anti-DEI framing |

### A.4 Plot
Same spec as Spec 02 §A.4: `figsize=(12,6)` horizontal bars, `tab:blue` for `T*` /
`tab:red` for `C*`, end-of-bar value labels (fontsize 12), legend "Type of
Definition (T)" / "Content of Definition (C)", tick size 14.
Save: `results/RQ2/coding_discrimination_prejudice.png`, `dpi=300`, `bbox_inches='tight'`, then `plt.show()`.

---

## Part B — Word cloud (`discriminationcloud.py`)

- Input: `data/discrimination_cloud.csv`; text = column index 1, `dropna`, joined by spaces.
- Stopwords: `STOPWORDS` + the **same** custom list as Spec 02 §B.2.
- `WordCloud(width=1200, height=900, background_color="white",
  stopwords=stopwords, random_state=42)`. Also set `np.random.seed(42)` after
  imports (Spec 00 §3). Layout is deterministic with the seed.
- `imshow` / `axis("off")` / `tight_layout(pad=0)`.
- Save: `results/RQ2/discriminationcloud.png`, `dpi=300`, `bbox_inches='tight'`, then `plt.show()`.

## Libraries
`pandas`, `numpy` (seed), `matplotlib` (`matplotlib.patches.Patch`), `wordcloud`, `os`.
