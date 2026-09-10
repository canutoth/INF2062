# Reproduction — *Diversity, Equity, and Inclusion in Software Engineering: Perceptions from Professionals in Brazil*

Executable reproduction of the JSERD/SEBR study, generated from the
specifications in [`specifications/`](specifications/) (Specs 00–08).

Upstream: <https://github.com/aisepucrio/JSERD-Diversity4BRSE> (Zenodo DOI
`10.5281/zenodo.21850292`). Sample: 220 tech professionals in Brazil.

## Layout

```text
data/        raw + coded inputs (unchanged)
scripts/     analysis code, one directory per module
results/     generated figures / tables, one directory per module
```

## Environment

Python 3.11+ with the pinned dependencies:

```bash
python3.11 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
```

Verified on CPython 3.11.15 with pandas 1.5.3, numpy 1.26.4, matplotlib 3.7.3,
seaborn 0.13.2, statsmodels 0.15.0, scipy 1.17.1, upsetplot 0.9.0.

## Running

```bash
cd scripts && python main.py --all
```

Individual modules: `--characterization`, `--rq1` … `--rq7`; `--quiet`/`-q`
suppresses per-script output. `main.py` runs each script from its own directory,
so the `../../data/` and `../../results/` relative paths resolve. Every script
can also be run directly from its own directory; `RQ3/sintonia.py` and
`RQ4/logistic_regression.py` resolve paths from `__file__` and run from anywhere.

A full run produces **47 files** across the eight `results/` directories, exactly
matching the output inventory in Spec 00 §6.

## Reproducibility

- All scripts set `matplotlib.use("Agg")` and `warnings.filterwarnings("ignore")`
  so the pipeline runs silently and headlessly with no human intervention.
- Seeding (Spec 00 §3, a reproduction override of the unseeded upstream):
  `RQ1/diversitycloud.py` and `RQ2/discriminationcloud.py` set
  `np.random.seed(42)` and `WordCloud(random_state=42)`; `RQ3/sintonia.py` sets
  `np.random.seed(42)`. Every other script is deterministic and sets no seed.
- **Verified**: three consecutive `main.py --all` runs produce byte-identical
  output for all 47 files.

## Deviations from upstream, and why

Spec 00 §5.1 and Spec 06 §2 document two upstream bugs and permit either
reproducing or fixing them. The choices made here:

1. **`main.py` missing comma — FIXED.** Upstream writes `'RQ3/sintonia.py'` and
   `'RQ3/stats_tests.py'` on adjacent lines with no comma, so Python
   concatenates them into the single bogus path `'RQ3/sintonia.pyRQ3/stats_tests.py'`;
   `stats_tests.py` therefore never runs through the orchestrator and the
   concatenated entry fails the file-exists check. Fixed here so `--rq3` runs all
   three RQ3 scripts and `--all` generates the complete `results/RQ3/` inventory.
   The mislabeled upstream argparse help strings are likewise corrected to match
   the authoritative `SCRIPTS` table.

2. **RQ5 overlapping Q28 figures — REPRODUCED AS-IS.** `RQ5/intersection.py`
   does not clear the figure between the four Q28 `countplot` calls, so
   `bar_q28_gen/se/race/dis.png` are each drawn over the previous axes: the
   legend of `bar_q28_dis.png` accumulates all four identity dimensions
   (Man/Woman/Heterosexual/LGBTQ+/White/Non-white/No/Yes) under a single
   "Disabled" title. Spec 06 §2 says to reproduce this unless the reproduction
   brief asks for the fix, and it does not. **These four figures are therefore
   faithful to upstream but not individually interpretable.** The one-line fix,
   if you want it, is a `plt.figure()` before each `countplot` call in
   `q28_bar_charts()`.

3. **`sintonia_mixed_model.csv` rounded to 4 decimals.** `BinomialBayesMixedGLM.fit_vb()`
   accepts no seed and its BFGS step leaves float noise of order 1e-7 between
   runs that the global `np.random.seed(42)` cannot remove — enough to change the
   file's bytes, never enough to change a reported digit. Rounding to 4 decimals
   (standard precision for odds ratios and p-values, ~1000× above the noise)
   makes the artifact byte-reproducible. The estimate is stable at
   OR = 1.3277, 95% CI [0.9191, 1.9180], p = .131.

## Modules

| Flag | Question | Spec | Scripts |
|---|---|---|---|
| `--characterization` | Demographic & professional profile | 01 | `characterization.py` |
| `--rq1` | How practitioners define diversity & inclusion | 02 | `coding_inclusion_diversity.py`, `diversitycloud.py` |
| `--rq2` | How practitioners define prejudice & discrimination | 03 | `coding_discrimination_prejudice.py`, `discriminationcloud.py` |
| `--rq3` | Perceived recurrence by demographic profile | 04 | `profile.py`, `sintonia.py`, `stats_tests.py` |
| `--rq4` | Perceived recurrence by organizational setting | 05 | `company.py`, `logistic_regression.py` |
| `--rq5` | Recognize, narrate, silence (Q28/Q29) | 06 | `intersection.py` |
| `--rq6` | Representation in teams vs. leadership | 07 | `teams.py`, `leaders.py` |
| `--rq7` | Self-awareness of unconscious bias | 08 | `coding_bias.py` |

Note that `RQ7/coding_bias.py` reads no file at runtime: per Spec 08 §1 the coded
counts are hard-coded in the script.

## Headline results reproduced

- **Sexism** is the most-perceived type overall (74.1% of respondents), rising to
  95.2% among women vs. 70.3% among men — χ²(1) = 11.22, *p* < .001, OR ≈ 8.43
  (`results/RQ3/stats_gender_sexism.txt`).
- Adjusted for the full predictor set, women have 15.60× the odds of perceiving
  sexism as recurrent (95% CI [1.88, 129.80], *p* = .011)
  (`results/RQ4/odds_ratios_sexism.csv`).
- The pooled in-group ("sintonia") effect across sexism / ableism / homophobia /
  racism is positive but not significant: OR = 1.33, 95% CI [0.92, 1.92], *p* = .131.
- 78/220 respondents answered yes to Q28; of those, 42 narrated in the third
  person and only 17 in the first person — the *recognize / narrate / silence*
  gradient (`results/RQ5/heatmap29_dis.png`).
