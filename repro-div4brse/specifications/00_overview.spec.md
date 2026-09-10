# Specification 00 — Study Overview & Reproduction Environment

## 1. Study

**Title:** *Diversity, Equity, and Inclusion in Software Engineering: Perceptions from Professionals in Brazil* (JSERD / SEBR).

**Design:** Cross-sectional online survey of tech professionals in Brazil. The
anonymized/coded datasets used by the analysis scripts describe **220 participants**.
The raw survey export (`analysis_i&d_up.csv`) holds additional partial/incomplete
responses; RQ3 and RQ4 scripts drop them with `dropna` on the required columns.

**Upstream repository:** `https://github.com/aisepucrio/JSERD-Diversity4BRSE`
(Zenodo DOI `10.5281/zenodo.21850292`).

The project is organized by **Research Question (RQ1–RQ7)** plus a participant
characterization module. Each analysis script is self-contained: it reads a raw file
from `data/`, does its own cleaning/mapping, and writes figures/tables to
`results/<module>/`. **There is no shared data-preparation / master-merge step.**

| Module | Question | Spec |
|---|---|---|
| `participant_characterization` | Demographic & professional profile of the sample | `01_participant_characterization.spec.md` |
| RQ1 | How practitioners **define diversity & inclusion** | `02_rq1_diversity_inclusion_definitions.spec.md` |
| RQ2 | How practitioners **define prejudice & discrimination** | `03_rq2_prejudice_discrimination_definitions.spec.md` |
| RQ3 | Perceived recurrence of discrimination **by demographic profile** (+ "sintonia"/in-group effect, pairwise tests) | `04_rq3_perceptions_by_profile.spec.md` |
| RQ4 | Perceived recurrence of discrimination **by organizational setting** (size, sector, work model) + adjusted logistic regression | `05_rq4_perceptions_by_organization.spec.md` |
| RQ5 | Workplace discrimination: **Recognize, Narrate, Silence** (Q28/Q29 discourse strategies, intersectional) | `06_rq5_recognize_narrate_silence.spec.md` |
| RQ6 | Representation in **development teams vs. leadership roles** (Likert) | `07_rq6_teams_vs_leadership.spec.md` |
| RQ7 | **Self-awareness of unconscious bias** (qualitative coding) | `08_rq7_unconscious_bias.spec.md` |

## 2. Repository layout to reproduce

```text
├── data/                              # raw + coded inputs (see §4)
├── survey/                            # questionnaire & consent forms (PT/EN) — not processed
├── scripts/
│   ├── main.py                        # CLI orchestrator
│   ├── requirements.txt
│   ├── participant_characterization/
│   │   └── characterization.py
│   ├── RQ1/  coding_inclusion_diversity.py   diversitycloud.py
│   ├── RQ2/  coding_discrimination_prejudice.py   discriminationcloud.py
│   ├── RQ3/  profile.py   sintonia.py   stats_tests.py
│   ├── RQ4/  company.py   logistic_regression.py
│   ├── RQ5/  intersection.py
│   ├── RQ6/  teams.py   leaders.py
│   └── RQ7/  coding_bias.py
└── results/                           # generated figures / tables (one folder per module)
```

## 3. Environment & constraints

- **Language:** Python 3.11+.
- **Dependencies** (`scripts/requirements.txt`, versions pinned as in upstream):
  ```
  pandas<2.0
  numpy>=1.23
  matplotlib==3.7.3
  seaborn
  upsetplot==0.9.0
  wordcloud
  statsmodels>=0.14
  scipy>=1.11
  ```
  No NLTK. No `scikit-posthocs`. No `openpyxl` requirement (scripts read the
  `.csv` variants, never the `.xlsx` ones).
- **Path convention:** every script assumes it is executed **from its own
  directory** and reaches data with the relative prefix `../../data/`, writing to
  `../../results/<module>/`. `sintonia.py` and `logistic_regression.py` instead
  resolve paths from `__file__` (`SCRIPT_DIR/../../...`) and can run from anywhere.
- Scripts call `plt.show()`; under a non-interactive backend this is a no-op.
- `sintonia.py` and `logistic_regression.py` set `warnings.filterwarnings("ignore")`.
- **Seeding (reproduction override of the upstream, which sets no seed):** the
  three scripts with stochastic elements set `np.random.seed(42)` immediately
  after imports, and pass an explicit constructor seed where one exists:
  - RQ1 `diversitycloud.py`, RQ2 `discriminationcloud.py` — `WordCloud(random_state=42)`;
  - RQ3 `sintonia.py` — `np.random.seed(42)`; `BinomialBayesMixedGLM.fit_vb()`
    has no seed argument, but the global seed plus the fixed input row order make
    the variational fit deterministic in practice.

  All other scripts are fully deterministic and set no seed. With `seed = 42` the
  figures and estimates are reproducible on a fixed library set; upstream
  (unseeded) differs only in wordcloud pixel layout and 3rd-decimal variational
  estimates.
- Each script creates its output directory with `os.makedirs(..., exist_ok=True)`.

## 4. Input data dictionary (`data/`)

| File | Rows | Shape / key columns | Consumed by |
|---|---|---|---|
| `participant-characterization.csv` | 220 | `ID` (`#P01`…`#P220`), `Region`, `Gender`, `Sexuality`, `Race`, `Disabled`, `Education`, `Work Model`, `Seniority`, `Industry Sector`, `Company size` — already in English, categorical | characterization |
| `coding_inclusion_diversity.csv` | 220 (one per participant; quoted free-text fields contain embedded newlines, so the raw line count is higher) | col0 `ID`, col1 free-text answer, **col2 = `T` code(s)**, **col3 = `C` code(s)** (comma-separated), col4 human-readable type, col5 explanation | RQ1 `coding_inclusion_diversity.py` |
| `coding_discrimination_prejudice.csv` | 220 (embedded newlines as above) | same shape as above; different code vocabulary | RQ2 `coding_discrimination_prejudice.py` |
| `diversity_cloud.csv` | 220 (embedded newlines) | `ID`, free-text "O que você entende por diversidade e inclusão?" (col1 used) | RQ1 `diversitycloud.py` |
| `discrimination_cloud.csv` | 220 (embedded newlines) | `ID`, free-text "O que você entende por discriminação e preconceito?" (col1 used) | RQ2 `discriminationcloud.py` |
| `data_teams.csv` | 220 | `ID` + 5 Likert (1–4) cols: `Race/Ethnicity`, `Gender/Sexuality`, `Neurodivergency`, `Disability`, `Elderly` — agreement that dev **teams** include each group | RQ6 `teams.py` |
| `data_leadership.csv` | 220 | same 5 Likert cols — agreement that **leadership** is encouraged for each group | RQ6 `leaders.py` |
| `q28_q29.csv` | 220 (one per participant; embedded newlines in `29`) | `ID`, `Region`, `Gender`, `Sexuality`, `Race`, `Disabled`, `Seniority`, `28` (Yes/No — witnessed differential treatment), `29` (free text), `report_type` (`1S` first-person / `3S` third-person / `N/A`), `report_category` (comma-separated discrimination labels) | RQ5 `intersection.py` |
| `analysis_i&d_up.csv` | full raw Google-Forms export (more responses than the 220 coded participants; scripts drop incomplete rows via `dropna`) | Full Google-Forms export, **Portuguese column headers**. Key columns by header string: idade (age), região, gênero (id.5), orientação sexual (id.6, trailing spaces), autodeclaração raça (id.7), deficiência (id.8), educação (id.10), modelo de trabalho (id.11), senioridade (id.13, trailing spaces), setor (id.15), tamanho da empresa (id.16), Likert team/leadership blocks (id.25–34), **"Qual(is) dos tipos de discriminação... mais recorrentes..."** (id.39), definitions D&I (id.41), definitions discr./prec. (id.42), bias self-recognition (id.46) | RQ3 (`profile.py`, `sintonia.py`, `stats_tests.py`), RQ4 (`company.py`, `logistic_regression.py`) |
| `analysis_i&d_up.xlsx` | — | Excel mirror of the above; **not read by any script** | — |
| `q28_q29` / coding `.xlsx`, `coding_discursive_answers.xlsx` | — | Excel companions; **not read by any script** | — |

### 4.1 Portuguese → English category mappings (used across RQ3 & RQ4)

- **Gender** (`identidade de gênero`): `homem cisgênero`/`homem trans` → `Men`;
  `mulher cisgênero`/`mulher trans` → `Women`. Anything else → unmapped (dropped).
- **Sexuality**: `heterossexual` → `Heterosexual`; `homossexual`/`bissexual`/`pansexual` → `LGBTQ+`.
- **Race** (`autodeclaração`): `branco(a)` → `White`; `preto(a)`/`pardo(a)`/`indígena` → `PoC`.
- **Disability** (`Você é uma pessoa com deficiência?`): starts with `sim` → `Disabled`/1;
  contains `não` → `Not disabled`/0. (`profile.py` treats the ambiguous/other case as `Disabled`;
  `sintonia.py`/`logistic_regression.py` treat it as `NaN`.)
- **Seniority**: `estagiário` → `Intern`; `júnior (até 5 anos)` → `Junior`;
  `pleno (6 a 9 anos)` → `Mid-level`; `sênior (10+ anos)` → `Senior`.
- **Work model**: `presencial` → `On-site`; `remoto` → `Remote`; `hibrido` → `Hybrid`.
- **Sector**: `setor público` → `Public`; `setor privado` → `Private`;
  `organização não governamental`/`organização sem fins lucrativos` → `Non-profit` (`company.py`: `Non-profit / NGO`);
  `startup` → `Startup`.
- **Company size**: `até 9`, `de 10 a 49`, `de 50 a 99` → `Small`;
  `de 100 a 499`, `de 500 a 999`, `mais de 1000` → `Big`.
- **Discrimination type** (multi-select field id.39, each item formatted
  `"<Tipo> (explby...)"`, items separated by the regex `,\s(?=\w+\s?\()`):
  `Etarismo` → `Ageism`, `Machismo` → `Sexism`, `Homofobia` → `Homophobia`,
  `Racismo` → `Racism`, `Elitismo` → `Elitism`, `Capacitismo` → `Ableism`.

## 5. Orchestrator (`scripts/main.py`)

CLI wrapper that `subprocess`-runs each script from its own directory.

Flags: `--all`, `--characterization`, `--rq1` … `--rq7`, `--quiet/-q`.
`--all` runs, in order: characterization → RQ1 → RQ2 → RQ3 → RQ4 → RQ5 → RQ6 → RQ7.

Per-module script lists:

| Flag | Scripts run |
|---|---|
| `--characterization` | `participant_characterization/characterization.py` |
| `--rq1` | `RQ1/coding_inclusion_diversity.py`, `RQ1/diversitycloud.py` |
| `--rq2` | `RQ2/coding_discrimination_prejudice.py`, `RQ2/discriminationcloud.py` |
| `--rq3` | `RQ3/profile.py`, `RQ3/sintonia.py`, `RQ3/stats_tests.py` |
| `--rq4` | `RQ4/company.py`, `RQ4/logistic_regression.py` |
| `--rq5` | `RQ5/intersection.py` |
| `--rq6` | `RQ6/teams.py`, `RQ6/leaders.py` |
| `--rq7` | `RQ7/coding_bias.py` |

### 5.1 Known discrepancies in the current upstream `main.py` (reproduce as-is, or fix and note)

1. **Missing comma** in the `rq3` list: `'RQ3/sintonia.py'` and `'RQ3/stats_tests.py'`
   are written on adjacent lines with no comma, so Python concatenates them into the
   single bogus path `'RQ3/sintonia.pyRQ3/stats_tests.py'`. Effect: via the
   orchestrator, `stats_tests.py` never runs and the concatenated entry fails the
   `full_path.exists()` check. Running `python RQ3/stats_tests.py` directly works.
2. The `argparse` **help strings are mislabeled** (e.g. `--rq1` help says "bias
   recognition"). The `SCRIPTS` dict and the README table are authoritative; the
   help text is not.

## 6. Output inventory (`results/`)

| Folder | Files produced by scripts |
|---|---|
| `participant_characterization/` | `region.png`, `gender.png`, `sexuality.png`, `race.png`, `disabled.png`, `education.png`, `work_model.png`, `seniority.png`, `industry_sector.png`, `company_size.png` (one PNG per non-`ID` column, filename = lowercased column, `/`→`-`, space→`_`). *Note:* `participant_characterization_graphics.pdf` and `participant_characterization_table.pdf` also exist upstream but are **not generated by `characterization.py`**. |
| `RQ1/` | `coding_inclusion_diversity.png`, `diversitycloud.png` |
| `RQ2/` | `coding_discrimination_prejudice.png`, `discriminationcloud.png` |
| `RQ3/` | `profile.png`, `pairwise_stats.csv`, `stats_gender_sexism.txt`, `sintonia_mixed_model.csv`, `sintonia_forest_plot.png`, `sintonia_bar_chart.png` |
| `RQ4/` | `company.png`, `odds_ratios_<type>.csv` (×6: sexism, racism, homophobia, ableism, ageism, elitism — subject to min-events filter), `odds_ratios_all.csv`, `forest_plot_<type>.png` (×6), `forest_plot_all.png` |
| `RQ5/` | `bar_q28_gen.png`, `bar_q28_se.png`, `bar_q28_race.png`, `bar_q28_dis.png`, `bar_discourse.png`, `heatmap29_dis.png`, `heatmap29_cat.png`, `useplot_cat2.png` (script also emits `barplot_cat.png`, not committed upstream) |
| `RQ6/` | `team-level.png`, `leadership_level.png` |
| `RQ7/` | `coding-bias.png` |
