# Specification 00 — Study Overview & Reproduction Environment

## 1. Study

**Paper under study:** FSE 2026 submission `WMS+26.pdf` — posterior guarantees for
performance-bound estimation from configuration samples.

- Preferred in-repository location: `references/WMS+26.pdf`.
- If the PDF is absent from `references/`, copy the attachment
  (`/Users/mathieuacher/Downloads/WMS+26.pdf`) there before running any
  paper-alignment or SRS-audit task. macOS privacy controls can block
  command-line reads from `Downloads`; move the file manually if needed.

**What the FSE paper provides (methodological source, label `RELATED-FSE26`):**

- posterior risk;
- posterior confidence;
- integrated confidence discrepancy (ICD);
- Statistical Recursive Search (**SRS**) sampling.

**This project = replication + extension.** The core cost-aware question:

> Does SRS remain the best recommendation once posterior guarantees are
> normalized by **empirical acquisition cost** rather than by **sample size**?

Steps:

1. Replicate FSE-style posterior-risk analysis on the original FSE systems.
2. Revisit the same framework on our datasets.
3. Replace "sample size as cost" with measured empirical acquisition cost.
4. Check whether the strategy recommendation or the Pareto frontier changes.

**Intended contribution** (not "FSE 2026 is wrong"):

> Posterior risk/confidence is a useful guarantee framework, but strategy
> recommendations become dataset- and cost-dependent once empirical acquisition
> cost is used instead of sample count.

## 2. Repository backbones

Two code bases are in play:

1. **Working repo** — `cost-sampling-matters` (this reproduction target). Holds
   the ongoing FSE-posterior experiments, runner scripts, and generated
   artifacts. Final FSE-posterior reports live here unless the user asks to port
   them into the public repo.
2. **Public ICSE reproducibility repo** — `acherm/cost-sampling-icse2027`
   (<https://github.com/acherm/cost-sampling-icse2027>). Treat as the clean
   public data/protocol backbone: stable dataset-family names, provenance,
   traceability, committed result tables, figure inputs, six-family taxonomy.
   Shallow inspection on 2026-07-02 used commit `d5dde2b` ("Rewrite RQ3
   predict-failure report as a clean public supplementary note").

Companion status report (working repo): `FSE2026_POSTERIOR_COST_REPLICATION_REPORT.md`.

Prefer the **public repo** for dataset-family names, provenance, traceability,
and paper-result context. Prefer the **working repo** for the current
FSE-posterior runners and reports.

Key public-repo docs to read before any run:

| Doc | Contents |
|---|---|
| `README.md` | paper thesis; six public dataset families; headline count-vs-cost results; setup |
| `data/README.md` | data provenance; download commands; expected raw-data locations; bundled curated energy subset |
| `docs/TRACEABILITY.md` | paper-claim → script → data → artifact mapping; exact commands for the ICSE count-vs-cost study; Linux / generated-family / schema gotchas |
| `artifacts/dataset_family_framing.md` | taxonomy and narrative roles for `REPLICATION`, `ENERGY`, `WORKLOAD`, `LCBENCH`, `LINUX` |

## 3. Module map (Phases → specs)

| Phase | Scope | Spec |
|---|---|---|
| 0 | Environment & cleanliness | this file, §9 |
| 1 | SRS audit vs. the FSE artifact | `01_srs_audit.spec.md` |
| 2 | Direct FSE artifact replication (+ empirical cost axis) | `02_fse_artifact_replication.spec.md` |
| 3 | `REPLICATION` / x264 corpus | `03_replication_x264.spec.md` |
| 4 | `ENERGY` and `WORKLOAD` posterior extension | `04_energy_workload_posterior.spec.md` |
| 5 | `LINUX` / TuxKConfig measured pools | `05_linux_tuxkconfig.spec.md` |
| 6 | `LCBENCH` measured pools | `06_lcbench.spec.md` |
| 7 | Cross-corpus synthesis + paper-ready claims | `07_cross_corpus_synthesis.spec.md` |

## 4. Repository layout to reproduce (working repo)

```text
├── references/WMS+26.pdf                     # FSE 2026 paper (add manually if missing)
├── cost_sampling/
│   ├── posterior.py                          # posterior risk / confidence / prior conf / integrated conf / ICD
│   ├── srs.py                                # code-native SRS: recursive selection, Welch t-test, random fill-to-budget
│   ├── generated_sampling.py                 # reusable generated-sampling helpers (LCBench + generated families)
│   └── pool_samplers.py                      # shared pool-based sampling strategies
├── scripts/
│   ├── run_fse_posterior.py                  # generic one-context runner
│   ├── run_fse_posterior_batch.py            # original FSE artifact systems
│   ├── run_fse_posterior_x264_batch.py       # REPLICATION-ICPE / x264
│   ├── run_fse_posterior_linux_batch.py      # Linux / TuxKConfig measured pools
│   ├── run_fse_posterior_lcbench_batch.py    # LCBench measured pools
│   ├── run_fse_posterior_twins_batch.py      # ENERGY / Twins  (TO CREATE — Phase 4)
│   ├── run_fse_posterior_workload_batch.py   # WORKLOAD        (TO CREATE — Phase 4)
│   ├── kw_cost_vs_size.py                    # ICSE count-vs-cost engine: --mode {icse19,x264,twins,workload,lcbench}
│   ├── significance_linux.py                 # Linux/TuxKConfig significance engine
│   ├── sig_core.py                           # shared median-decision bootstrap + Pareto choice-set logic
│   ├── run_twins_generated.py               # generated-sampling protocol, ENERGY/Twins
│   └── run_workload_generated.py            # generated-sampling protocol, WORKLOAD
├── ICPE-rawdata/                             # local inputs (see §5)
└── artifacts/                                # generated result dirs (one per corpus/run)
```

Existing result directories (do **not** overwrite — use a new suffix
`_final` / `_rerun` / dated):

- `artifacts/fse_posterior_fse_artifact_all/`
- `artifacts/fse_posterior_x264_icpe/`
- `artifacts/fse_posterior_linux_all_quick/`
- `artifacts/fse_posterior_lcbench_no_oracles/`

## 5. Data inputs and layout

### 5.1 Public ICSE repo layout

- `data/raw/` — git-ignored, full upstream raw data.
- `data/curated/energy/twins_energy_subset.zip` — committed ~19 MB curated
  ENERGY subset that reproduces paper figures offline.
- `artifacts/` — committed result tables and figure inputs for the ICSE paper.
- `figures/` — regenerated paper figures.

Preferred public-repo raw paths:

```text
data/raw/NewRuns.zip
data/raw/AllRuns.zip
data/raw/twins_main.zip
data/raw/workload_artifact.zip
data/raw/lcbench/data_2k_lw.json
data/raw/linux/tuxkconfig_<release>.parquet
```

### 5.2 Canonical data root (frozen)

**Execution target is the working repo `cost-sampling-matters` (§8 decision 10,
frozen). The canonical data root is `ICPE-rawdata/`** — the prefix the posterior
runners already default to. Every phase spec writes its input paths against this
root; do **not** pass `data/raw/...` paths.

```text
ICPE-rawdata/AllRuns.zip                                              # x264            (Spec 03)
ICPE-rawdata/NewRuns.zip                                              # REPLICATION-ICSE19 (not run this pass)
ICPE-rawdata/linux/tuxkconfig_{413,415,420,500,504,507,508}.parquet   # Linux           (Spec 05)
ICPE-rawdata/lcbench/data_2k_lw.json                                  # LCBench         (Spec 06)
ICPE-rawdata/twins_energy_subset.zip                                  # ENERGY / Twins  (Spec 04)
ICPE-rawdata/workload_artifact.zip                                    # WORKLOAD        (Spec 04)
```

`AllRuns.zip`, `NewRuns.zip` and the seven `tuxkconfig_*.parquet` files are
already present in the working repo. The LCBench JSON, the curated ENERGY subset
and the WORKLOAD artifact are external (§5.3) and must be staged under
`ICPE-rawdata/` before the corresponding phase.

If a later run is moved to the public ICSE repo, do the remap **once** as
environment setup — `ln -s ../data/raw ICPE-rawdata` (plus placing the curated
energy subset and lcbench json under it) — never as a per-command decision.
Record the repo and git commit in every run manifest.

### 5.3 External inputs (supplied by agent/user)

| Input | Canonical local path | Needed by |
|---|---|---|
| Original FSE 2026 artifact root (`$FSE_ROOT`) | passed via `--fse-root` | Specs 01, 02 |
| LCBench lightweight JSON | `ICPE-rawdata/lcbench/data_2k_lw.json` | Spec 06 |
| Curated ENERGY / Twins subset | `ICPE-rawdata/twins_energy_subset.zip` | Spec 04 |
| WORKLOAD artifact | `ICPE-rawdata/workload_artifact.zip` | Spec 04 |

External inputs are **not** assumed version-stable. Each run manifest must record
source, checksum (if available), and local path.

## 6. Metrics to compute (shared across all phases)

For a target performance vector over a reference universe `V` and a sampled set
`S`:

**Sampled bound**
- max-bound case: `max(target[S])`;
- min-bound case: `min(target[S])`.

**Posterior risk**
- max-bound: fraction of configs in `V` with target value **larger** than the sampled bound;
- min-bound: fraction of configs in `V` with target value **smaller** than the sampled bound.

**Posterior confidence**
- empirical CDF over repeated-sample posterior risks;
- for each accepted risk threshold `epsilon`, confidence = fraction of repeated
  samples whose posterior risk ≤ `epsilon`.

**Integrated posterior confidence**
- exact integral of the empirical CDF over `epsilon ∈ [0, 1]`;
- implemented as `1 - mean(posterior_risk)`.

**Prior confidence**
- default (FSE artifact notebook): `1 - (1 - epsilon) ** (N + 1)` — flag `--prior-offset 1`;
- sensitivity (simplified paper equation): `1 - (1 - epsilon) ** N` — flag `--prior-offset 0`.

**Integrated confidence discrepancy**
- `omega = posterior_area - prior_area`.

**Cost quantities**
- `pct_n = sample_size / reference_universe_size`;
- `pct_cost = sum(cost[S]) / sum(cost[V])`;
- `calibration_ratio = pct_cost / pct_n`;
- `effective_n_by_cost = pct_cost * reference_universe_size`.

**Cost-normalized posterior confidence**
- use `effective_n_by_cost` as the prior baseline sample size when asking whether
  a strategy gives better guarantees than expected for the empirical cost spent.

**Pareto decisions**
- count-cost frontier: cost axis = sample size or `pct_n`;
- empirical-cost frontier: cost axis = `pct_cost`;
- compare the two frontiers with Jaccard overlap and changed-frontier flags.

## 7. Core hypotheses

| ID | Statement | Test |
|---|---|---|
| H1 | posterior-risk distributions differ among strategies at fixed budget | Kruskal-Wallis across strategies |
| H2 | empirical-cost normalization changes the top recommendation | frontier/top-choice comparison |
| H3 | SRS is the best empirical-cost-normalized recommendation | cost-normalized ranking |
| H4 | empirical-cost normalization changes the Pareto frontier | Jaccard + changed-frontier flag |
| H5 | SRS has lower posterior risk than random sampling | Mann-Whitney U + effect size |
| H6 | SRS has different empirical acquisition cost than random sampling | Mann-Whitney U + effect size |

- Pairwise strategy comparisons: **Mann-Whitney U**.
- Effect size: **Vargha-Delaney A12** (or another rank-based effect size).
- Multiple-comparison correction: decide the policy before final reruns.
- Corpus-level synthesis: use blocked tests / context-level counts — never raw
  repeated samples as independent systems.

Current scripts use FSE-style hypothesis labels; renaming to H1–H6 for paper
writing is allowed but must be consistent across all phase outputs.

## 8. Global protocol decisions

Frozen: 1, 5, 7, 10. Frozen by the Specs 02–06 command blocks: 2, 3, 4, 6.
Still open: 8, 9, 11.

1. **Frozen.** Prior confidence `N + 1` (`--prior-offset 1`) is the headline
   convention; run the `N` sensitivity (`--prior-offset 0`) only where the phase
   spec includes a dedicated sensitivity command (Spec 02 §3.2).
2. Strategy set per corpus — per the Specs 02–06 command blocks.
3. Budget levels per corpus — per the Specs 02–06 command blocks.
4. Number of repeated runs / seeds — per the Specs 02–06 command blocks
   (smoke 30, final 100).
5. **Frozen.** `--extreme max` for every corpus (performance-bound targets and
   accuracy-as-bound targets alike).
6. Cost column per corpus — per the Specs 02–06 command blocks (x264 `time`;
   ENERGY `energy,performance`; Linux acquisition proxy; LCBench `time_total`).
7. **Frozen.** Generated diagnostic oracle strategies are excluded from headline
   results (`--no-oracles` where the runner supports it); oracle runs are
   diagnostic-only side outputs.
8. Multiple-comparison correction policy — **open**; decide before final reruns.
9. Which generated artifacts are committed — **open**; ask the user.
10. **Frozen.** Final reruns execute in the working repo `cost-sampling-matters`;
    canonical data root `ICPE-rawdata/` (§5.2).
11. How posterior results integrate with the public repo (branch/PR extension;
    separate supplementary artifacts; or internal pre-paper exploration only) —
    **open**.

## 9. Phase 0 — environment & cleanliness

Start every experimental session with:

```bash
pwd
git status --short
python3 --version
```

Sanity imports:

```bash
python3 - <<'PY'
import numpy, pandas
print("numpy", numpy.__version__)
print("pandas", pandas.__version__)
PY
```

Rules:

- Do not revert or delete unrelated user changes.
- Do not install packages requiring network access without approval; inspect the
  repo setup first.
- If the public ICSE repo is absent and needed:
  ```bash
  git clone https://github.com/acherm/cost-sampling-icse2027.git
  cd cost-sampling-icse2027
  python3 -m venv .venv
  . .venv/bin/activate
  pip install -r requirements.txt
  ```
  then read `README.md`, `data/README.md`, `docs/TRACEABILITY.md`,
  `artifacts/dataset_family_framing.md`.
- Do not blindly copy artifacts between repos. Prefer rerunning final commands in
  the target repo and keeping a manifest with: command, git commit, input paths,
  output directory.
- Generated artifacts can be large — ask before committing unless the user
  explicitly requested it.

## 10. Reproducibility constraints (SDD)

- **Language:** Python 3 (match the target repo's `requirements.txt`).
- **Seeds:** every stochastic operation is seeded. Runner scripts expose
  `--srs-seeds` / `--seeds` / `--*-runs`; pass explicit integers and record them.
  Where a script sets a global seed, use `np.random.seed(42)` unless an existing
  script fixes another value.
- **No hallucinated dependencies / metrics / data sources** beyond §6 and the
  per-phase specs.
- **Exact paths:** honour the input/output paths in each phase spec; assume
  execution from the target repository root unless the spec says otherwise.
- **Autonomous execution:** scripts run silently, suppress non-critical warnings,
  and download external resources quietly (only with approval when network is
  required).
- Output directories are created with `os.makedirs(..., exist_ok=True)`.

## 11. Terminology and scope rules

| Label | Meaning |
|---|---|
| `RELATED-FSE26` | original FSE posterior-risk paper + artifact; methodological source for posterior guarantees and SRS |
| `REPLICATION-FSE26` | original FSE artifact systems; closest direct replication |
| `REPLICATION` | public ICSE family grouping published sampling replications; includes Kaltenecker/NewRuns and x264/ICPE |
| `REPLICATION-ICSE19` | Kaltenecker / NewRuns corpus |
| `REPLICATION-ICPE20-x264` | x264 corpus from the ICPE 2020 artifact |
| `ENERGY` | Twins / Twins-or-False-Friends family; acquisition cost may mean energy rather than runtime |
| `WORKLOAD` | workload-impact family; workload/input sensitivity within configurable systems |
| `LCBENCH` | external validation on hyperparameter-configuration measured pools |
| `LINUX` | large-scale TuxKConfig stress test |
| `EXTERNAL-VALIDITY-LINUX-POOL` | Linux/TuxKConfig measured pools; not exhaustive full config spaces |
| `EXTERNAL-VALIDITY-LCBENCH` | LCBench measured hyperparameter pools; cross-domain methodological stress test |

**Wording rules:**

- FSE artifact systems: posterior risk may be described relative to the complete
  configuration universe **only if** the artifact contains the full measured
  universe for that system.
- Linux and LCBench: always use "pool-relative posterior risk" /
  "reference-relative posterior risk". Never claim exhaustive configuration risk.

**Inherited narrative (from the public ICSE repo):**

1. `REPLICATION`: same published sampling studies, different cost model.
2. `ENERGY`: same sampling question, different notion of cost.
3. `WORKLOAD`: same configurable system, changing workload/input context.
4. `LCBENCH`: same count-vs-cost question, outside pure configurable software.
5. `LINUX`: same thesis, extreme configuration-space scale.
6. `RELATED-FSE26`: same posterior-guarantee outcome, now crossed with measured
   acquisition cost.

## 12. Deliverable checklist

**Per corpus:** source repo + git commit; aggregate Markdown report; aggregate
CSV summary; hypothesis summary CSV; hypothesis tests CSV; per-context/per-system
reports; key figures; command manifest; short caveat note on scope and data
completeness.

**Whole study:** one synthesis Markdown; one synthesis CSV; paper-level figures;
final TODO list; reproduction commands; data provenance notes.

## 13. Agent handoff rules

1. Read this spec and `FSE2026_POSTERIOR_COST_REPLICATION_REPORT.md` first, then
   the four public-repo docs (§2).
2. `git status --short` in whichever repo is being edited.
3. State whether the task runs in `cost-sampling-matters` or
   `acherm/cost-sampling-icse2027`.
4. Never overwrite existing artifact directories unless explicitly asked — use a
   new suffix.
5. Record every command that produces final results.
6. Keep direct-replication claims separate from external-validity claims.
7. Use pool-relative language for Linux and LCBench.
8. Never commit large generated artifacts without user approval.
9. On a failed run due to missing external data, report the missing path and the
   expected input format.
