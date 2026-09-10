# Roadmap: FSE 2026 Posterior Guarantees Under Empirical Acquisition Cost

This document is a self-contained execution roadmap for agents who need to run,
audit, or extend the experiments around FSE-style posterior risk/confidence and
empirical acquisition cost.

It should be executed together with the public ICSE reproducibility repository:

- <https://github.com/acherm/cost-sampling-icse2027>

That repository is the main reusable backbone for dataset provenance, public
commands, committed result tables, figure inputs, and the six-family taxonomy of
the submitted ICSE paper. A shallow inspection on 2026-07-02 used commit
`d5dde2b` (`Rewrite RQ3 predict-failure report as a clean public supplementary
note`).

The companion status report is:

- `FSE2026_POSTERIOR_COST_REPLICATION_REPORT.md`

Reference paper:

- FSE 2026 paper under study: `WMS+26.pdf`, originally provided as an
  attachment at `/Users/mathieuacher/Downloads/WMS+26.pdf`.
- Preferred in-repository location: `references/WMS+26.pdf`.
- If the PDF is not present in `references/`, copy or move the attached PDF into
  that location before running paper-alignment or SRS-audit tasks. On macOS,
  direct command-line reads from `Downloads` may be blocked by privacy controls,
  so moving the file into the workspace manually may be required.

This roadmap is intentionally operational: it defines the research objective,
datasets, metrics, hypotheses, commands, expected artifacts, quality checks,
and open TODOs.

## 1. Research Objective

The FSE 2026 paper evaluates sampling strategies for performance-bound
estimation using:

- posterior risk;
- posterior confidence;
- integrated confidence discrepancy;
- Statistical Recursive Search, abbreviated SRS.

The core cost-aware question is:

> Does SRS remain the best recommendation once posterior guarantees are
> normalized by empirical acquisition cost rather than by sample size?

This is a replication-plus-extension:

1. Replicate FSE-style posterior-risk analysis on the original FSE systems.
2. Revisit the same framework on our datasets.
3. Replace "sample size as cost" by measured empirical acquisition cost.
4. Check whether the strategy recommendation or Pareto frontier changes.

The intended final contribution is not "FSE 2026 is wrong." The intended
contribution is:

> Posterior risk/confidence is a useful guarantee framework, but strategy
> recommendations become dataset- and cost-dependent once empirical acquisition
> cost is used instead of sample count.

## 2. Repository Backbones To Reuse

There are two relevant code bases:

1. This working repository, `cost-sampling-matters`, which currently contains
   the ongoing FSE-posterior experiments and existing generated artifacts.
2. The public ICSE reproducibility repository,
   `acherm/cost-sampling-icse2027`, which should be treated as the clean
   public data/protocol backbone.

Agents should prefer the public repo for stable dataset-family names, data
provenance, traceability, and paper-result context. Agents should use this
working repo for the current FSE-posterior reports unless the user asks to port
them into the public repo.

Key public-repo documentation:

- `README.md`
  - paper thesis;
  - six public dataset families;
  - headline count-vs-cost results;
  - setup instructions.
- `data/README.md`
  - public data provenance;
  - download commands;
  - expected raw-data locations;
  - bundled curated energy subset.
- `docs/TRACEABILITY.md`
  - paper claim to script to data to artifact mapping;
  - exact commands for the ICSE count-vs-cost study;
  - gotchas about Linux, generated families, and artifact schemas.
- `artifacts/dataset_family_framing.md`
  - taxonomy and narrative roles for `REPLICATION`, `ENERGY`, `WORKLOAD`,
    `LCBENCH`, and `LINUX`.

## 3. Current Posterior Entry Points

Core implementation:

- `cost_sampling/posterior.py`
  - posterior risk;
  - posterior confidence;
  - prior confidence;
  - integrated posterior confidence;
  - integrated confidence discrepancy.
- `cost_sampling/srs.py`
  - code-native SRS implementation;
  - recursive selection;
  - Welch t-test;
  - random fill to reach the requested sample size, matching the FSE footnote.

Experiment scripts:

- `scripts/run_fse_posterior.py`
  - generic one-context runner.
- `scripts/run_fse_posterior_batch.py`
  - original FSE artifact systems.
- `scripts/run_fse_posterior_x264_batch.py`
  - REPLICATION-ICPE/x264.
- `scripts/run_fse_posterior_linux_batch.py`
  - Linux/TuxKConfig measured pools.
- `scripts/run_fse_posterior_lcbench_batch.py`
  - LCBench measured pools.

Public ICSE count-vs-cost engines to leverage:

- `scripts/kw_cost_vs_size.py`
  - main Kruskal-Wallis, Pareto, and flip engine for non-Linux families:
    `--mode {icse19,x264,twins,workload,lcbench}`.
- `scripts/significance_linux.py`
  - Linux/TuxKConfig significance engine.
- `scripts/sig_core.py`
  - shared median-decision bootstrap and Pareto choice-set logic.
- `scripts/run_twins_generated.py`
  - generated-sampling protocol for the ENERGY/Twins family.
- `scripts/run_workload_generated.py`
  - generated-sampling protocol for the WORKLOAD family.
- `cost_sampling/generated_sampling.py`
  - reusable generated-sampling helpers for LCBench and generated families.
- `cost_sampling/pool_samplers.py`
  - shared pool-based sampling strategies.

Existing current result directories:

- `artifacts/fse_posterior_fse_artifact_all/`
- `artifacts/fse_posterior_x264_icpe/`
- `artifacts/fse_posterior_linux_all_quick/`
- `artifacts/fse_posterior_lcbench_no_oracles/`

## 4. Data Inputs And Layout

### 4.1 Public ICSE Repository Layout

The public repo uses the following data layout:

- `data/raw/`
  - git-ignored location for full upstream raw data.
- `data/curated/energy/twins_energy_subset.zip`
  - committed 19 MB curated ENERGY subset that reproduces paper figures
    offline.
- `artifacts/`
  - committed result tables and figure inputs for the ICSE paper.
- `figures/`
  - regenerated paper figures.

Preferred public-repo raw paths:

- `data/raw/NewRuns.zip`
- `data/raw/AllRuns.zip`
- `data/raw/twins_main.zip`
- `data/raw/workload_artifact.zip`
- `data/raw/lcbench/data_2k_lw.json`
- `data/raw/linux/tuxkconfig_<release>.parquet`

### 4.2 Inputs Present In This Working Repository

The current working repository has these local inputs:

- `ICPE-rawdata/AllRuns.zip`
- `ICPE-rawdata/NewRuns.zip`
- `ICPE-rawdata/linux/tuxkconfig_413.parquet`
- `ICPE-rawdata/linux/tuxkconfig_415.parquet`
- `ICPE-rawdata/linux/tuxkconfig_420.parquet`
- `ICPE-rawdata/linux/tuxkconfig_500.parquet`
- `ICPE-rawdata/linux/tuxkconfig_504.parquet`
- `ICPE-rawdata/linux/tuxkconfig_507.parquet`
- `ICPE-rawdata/linux/tuxkconfig_508.parquet`

If an agent works in the public repo, either copy/symlink these files into
`data/raw/` or pass explicit `--zip` / `--json` paths where supported.

Current posterior scripts still have some legacy defaults, notably
`ICPE-rawdata/...` for x264/Linux. Before final public integration, either:

- pass explicit paths where the script supports them;
- create compatibility symlinks;
- or patch the posterior runner to use public-repo `data/raw/...` paths.

### 4.3 External Inputs Required

The following inputs may need to be supplied by the agent or user:

- Original FSE 2026 artifact root, containing the FSE sampling data.
- LCBench lightweight JSON if not already available:
  - public-repo preferred path: `data/raw/lcbench/data_2k_lw.json`;
  - legacy current default: `/private/tmp/lcbench/data_2k_lw.json`.

Do not assume those external inputs are version-stable. Record their source,
checksum if possible, and local path in each run manifest.

## 5. Terminology And Scope Rules

Use these labels consistently:

- `RELATED-FSE26`
  - original FSE posterior-risk paper and artifact;
  - methodological source for posterior guarantees and SRS.
- `REPLICATION-FSE26`
  - original FSE artifact systems;
  - closest direct replication.
- `REPLICATION`
  - public ICSE family grouping published sampling replications;
  - includes Kaltenecker/NewRuns and x264/ICPE.
- `REPLICATION-ICSE19`
  - Kaltenecker/NewRuns corpus.
- `REPLICATION-ICPE20-x264`
  - x264 corpus from the ICPE 2020 artifact.
- `ENERGY`
  - Twins/Twins-or-False-Friends family;
  - changes the meaning of acquisition cost, e.g. energy rather than runtime.
- `WORKLOAD`
  - workload-impact family;
  - tests workload/input sensitivity within configurable software systems.
- `LCBENCH`
  - external validation on hyperparameter-configuration measured pools.
- `LINUX`
  - large-scale TuxKConfig stress test.
- `EXTERNAL-VALIDITY-LINUX-POOL`
  - Linux/TuxKConfig measured pools;
  - not exhaustive full Linux configuration spaces.
- `EXTERNAL-VALIDITY-LCBENCH`
  - LCBench measured hyperparameter pools;
  - cross-domain methodological stress test.

Important wording:

- For FSE artifact systems, posterior risk can be described relative to the
  available complete configuration universe if the artifact contains the full
  measured universe for that system.
- For Linux and LCBench, use "pool-relative posterior risk" or
  "reference-relative posterior risk." Do not claim exhaustive configuration
  risk for these datasets.

Recommended narrative inherited from the public ICSE repo:

1. `REPLICATION`: same published sampling studies, different cost model.
2. `ENERGY`: same sampling question, different notion of cost.
3. `WORKLOAD`: same configurable system, changing workload/input context.
4. `LCBENCH`: same count-vs-cost question, outside pure configurable software.
5. `LINUX`: same thesis, extreme configuration-space scale.
6. `RELATED-FSE26`: same posterior-guarantee outcome, now crossed with measured
   acquisition cost.

## 6. Metrics To Compute

For a target performance vector over a reference universe `V` and a sampled set
`S`, compute the sampled bound:

- max-bound case: `max(target[S])`;
- min-bound case: `min(target[S])`.

Posterior risk:

- max-bound case: fraction of configurations in `V` with target value larger
  than the sampled bound;
- min-bound case: fraction of configurations in `V` with target value smaller
  than the sampled bound.

Posterior confidence:

- empirical CDF over repeated-sample posterior risks;
- for each accepted risk threshold `epsilon`, confidence is the fraction of
  repeated samples whose posterior risk is at most `epsilon`.

Integrated posterior confidence:

- exact integral of the empirical CDF over epsilon in `[0, 1]`;
- implemented as `1 - mean(posterior_risk)`.

Prior confidence:

- current default follows the FSE artifact notebook:
  - `1 - (1 - epsilon) ** (N + 1)`
- sensitivity should also be run with the simplified paper equation:
  - `1 - (1 - epsilon) ** N`

Integrated confidence discrepancy:

- `omega = posterior_area - prior_area`.

Cost quantities:

- `pct_n = sample_size / reference_universe_size`;
- `pct_cost = sum(cost[S]) / sum(cost[V])`;
- `calibration_ratio = pct_cost / pct_n`;
- `effective_n_by_cost = pct_cost * reference_universe_size`.

Cost-normalized posterior confidence:

- use `effective_n_by_cost` as the prior baseline sample size when asking
  whether a strategy gives better guarantees than expected for the empirical
  cost spent.

Pareto decisions:

- count-cost frontier: use sample size or `pct_n` as the cost axis;
- empirical-cost frontier: use `pct_cost` as the cost axis;
- compare the two frontiers with Jaccard overlap and changed-frontier flags.

## 7. Core Hypotheses

Use a small, stable hypothesis set. Current scripts use FSE-style hypothesis
labels; for paper writing, these can be renamed.

Recommended hypothesis family:

- H1: posterior-risk distributions differ among strategies at fixed budget.
- H2: empirical-cost normalization changes the top recommendation.
- H3: SRS is the best empirical-cost-normalized recommendation.
- H4: empirical-cost normalization changes the Pareto frontier.
- H5: SRS has lower posterior risk than random sampling.
- H6: SRS has different empirical acquisition cost than random sampling.

Recommended tests:

- H1: Kruskal-Wallis across strategies.
- Pairwise strategy comparisons: Mann-Whitney U.
- Effect size: Vargha-Delaney A12 or another rank-based effect size.
- Multiple-comparison correction: decide before final reruns.
- Corpus-level synthesis: use blocked tests or context-level counts, not raw
  repeated samples as independent systems.

## 8. Global Protocol Decisions To Freeze Before Final Runs

Before paper-grade reruns, freeze these decisions:

1. Prior confidence convention:
   - default artifact-compatible `N + 1`;
   - sensitivity with `N`.
2. Strategy set per corpus.
3. Budget levels per corpus.
4. Number of repeated runs or seeds.
5. Target orientation:
   - most performance-bound settings use `--extreme max`;
   - accuracy-like targets may also use `max` if "best accuracy" is the bound.
6. Cost column per corpus.
7. Whether generated diagnostic oracle strategies are included or excluded.
8. Multiple-comparison correction policy.
9. Which generated artifacts should be committed.
10. Whether final reruns are executed in:
   - this working repository; or
   - the public `acherm/cost-sampling-icse2027` repository.
11. How posterior results are integrated with the public repo:
   - as a branch/PR adding the FSE-posterior extension;
   - as separate supplementary artifacts;
   - or as an internal pre-paper exploration only.

## 9. Phase 0: Environment And Cleanliness

Start every experimental session with:

```bash
pwd
git status --short
python3 --version
```

Do not revert or delete unrelated user changes. Generated artifacts can be
large; ask before committing them unless the user explicitly requested it.

Recommended sanity imports:

```bash
python3 - <<'PY'
import numpy, pandas
print("numpy", numpy.__version__)
print("pandas", pandas.__version__)
PY
```

If dependencies are missing, inspect the repository setup first. Do not install
new packages without approval if network access is required.

If the public ICSE repository is not already present, clone it:

```bash
git clone https://github.com/acherm/cost-sampling-icse2027.git
cd cost-sampling-icse2027
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

Then read:

```bash
sed -n '1,220p' README.md
sed -n '1,260p' data/README.md
sed -n '1,320p' docs/TRACEABILITY.md
sed -n '1,260p' artifacts/dataset_family_framing.md
```

Do not blindly copy artifacts between repositories. Prefer rerunning final
commands in the target repository and keeping a manifest with the command, git
commit, input paths, and output directory.

## 10. Phase 1: SRS Audit

Goal:

- verify that `cost_sampling/srs.py` faithfully matches the FSE artifact
  behavior relevant to our experiments.

Tasks:

1. Locate the official FSE SRS implementation, likely named
   `SRS-sampling.ipynb` or similar.
2. Save the artifact source path and version in the run notes.
3. Compare defaults:
   - step sample size;
   - Welch t-test;
   - p-value threshold;
   - target orientation;
   - recursion stop behavior;
   - random fill behavior.
4. Add or run small tests for:
   - exact sample size returned;
   - deterministic seed behavior;
   - fill-to-budget behavior;
   - no duplicate indices;
   - `max` and `min` orientation.

Suggested smoke check:

```bash
python3 - <<'PY'
import numpy as np
from cost_sampling.srs import srs_indices

rng = np.random.default_rng(0)
X = rng.integers(0, 2, size=(200, 12))
y = X[:, 0] * 10 + X[:, 1] * 3 + rng.normal(size=200)
idx = srs_indices(X, y, 32, rng=123)
print(len(idx), len(set(idx)), idx[:10].tolist())
assert len(idx) == 32
assert len(set(idx)) == 32
PY
```

Deliverable:

- short note in the final report saying whether SRS is:
  - exact artifact reuse;
  - faithful reimplementation;
  - approximate adaptation requiring caveats.

## 11. Phase 2: Direct FSE Artifact Replication

Goal:

- reproduce FSE posterior-risk analysis on the original FSE systems;
- add empirical acquisition cost as the second decision axis.

Input:

- external FSE artifact root, represented below as `$FSE_ROOT`.

Fixed-budget command:

```bash
python3 scripts/run_fse_posterior_batch.py \
  --fse-root "$FSE_ROOT" \
  --output-dir artifacts/fse_posterior_fse_artifact_final_t2 \
  --contexts ALL \
  --strategies random,solverBased,divDistBased,twise,SRSSampling \
  --levels t2 \
  --max-runs 100 \
  --extreme max \
  --prior-offset 1
```

Optional prior-equation sensitivity:

```bash
python3 scripts/run_fse_posterior_batch.py \
  --fse-root "$FSE_ROOT" \
  --output-dir artifacts/fse_posterior_fse_artifact_final_t2_priorN \
  --contexts ALL \
  --strategies random,solverBased,divDistBased,twise,SRSSampling \
  --levels t2 \
  --max-runs 100 \
  --extreme max \
  --prior-offset 0
```

If the artifact exposes multiple levels and budget-scaling is needed:

```bash
python3 scripts/run_fse_posterior_batch.py \
  --fse-root "$FSE_ROOT" \
  --output-dir artifacts/fse_posterior_fse_artifact_final_all_levels \
  --contexts ALL \
  --strategies random,solverBased,divDistBased,twise,SRSSampling \
  --levels ALL \
  --max-runs 100 \
  --extreme max \
  --prior-offset 1
```

Expected outputs:

- `fse_posterior_systems_report.md`
- `posterior_system_summary.csv`
- `posterior_strategy_summary.csv`
- `posterior_hypothesis_summary.csv`
- `posterior_hypothesis_tests.csv`
- per-system folders with figures and CSVs.

Required checks:

- Are all seven FSE systems present?
- Are all expected strategies present?
- Does SRS have exactly the fixed requested sample size?
- Does the result reproduce the previous current finding:
  - SRS best empirical-cost-normalized in about `3/7`;
  - SRS on empirical Pareto frontier in about `6/7`;
  - empirical frontier changes in about `6/7`.

## 12. Phase 3: REPLICATION/x264

Goal:

- run FSE posterior-risk metrics on the x264 corpus;
- test whether SRS and posterior guarantees transfer;
- test whether cost-normalized decisions differ from sample-size decisions.

Input:

- public repo preferred path: `data/raw/AllRuns.zip`;
- legacy working-repo path: `ICPE-rawdata/AllRuns.zip`.

Recommended final command:

```bash
python3 scripts/run_fse_posterior_x264_batch.py \
  --runs-zip data/raw/AllRuns.zip \
  --output-dir artifacts/fse_posterior_x264_icpe_final \
  --contexts 0-16 \
  --target-props time,size \
  --cost-prop time \
  --strategies random,solverBased,divDistBased,twise,distBased,henard \
  --levels t1,t2,t3 \
  --fixed-level t2 \
  --max-runs 100 \
  --srs-seeds 100 \
  --extreme max \
  --prior-offset 1
```

Optional sensitivity where each target uses its own acquisition cost:

```bash
python3 scripts/run_fse_posterior_x264_batch.py \
  --runs-zip data/raw/AllRuns.zip \
  --output-dir artifacts/fse_posterior_x264_icpe_final_cost_same \
  --contexts 0-16 \
  --target-props time,size \
  --cost-prop same \
  --strategies random,solverBased,divDistBased,twise,distBased,henard \
  --levels t1,t2,t3 \
  --fixed-level t2 \
  --max-runs 100 \
  --srs-seeds 100 \
  --extreme max \
  --prior-offset 1
```

Expected outputs:

- `fse_posterior_x264_icpe_report.md`
- `posterior_x264_context_summary.csv`
- `posterior_x264_budget_trends.csv`
- `posterior_strategy_summary.csv`
- `posterior_hypothesis_summary.csv`
- per-context reports and figures.

Required checks:

- Expect 34 fixed-level target contexts:
  - 17 inputs x 2 target properties.
- Previous current result:
  - strategy posterior-risk distributions differ in `34/34`;
  - SRS best cost-normalized in about `26/34`;
  - SRS on empirical Pareto frontier in about `29/34`;
  - empirical frontier changes in about `30/34`.

Interpretation target:

- x264 is likely the strongest positive SRS replication.
- The cost-aware result is still important because Pareto frontiers change even
  when the top recommendation is stable.

## 13. Phase 4: ENERGY And WORKLOAD Posterior Extension

Goal:

- extend the FSE-posterior outcome to two public ICSE generated-sampling
  families that were not covered by the first roadmap draft;
- reuse the public repo's existing generated-sampling engines instead of
  inventing a second protocol.

Why this phase matters:

- `ENERGY` checks whether posterior guarantees per acquisition cost behave
  differently when cost means energy or another measured property, not just
  runtime.
- `WORKLOAD` checks whether posterior guarantees and SRS/cost tradeoffs are
  sensitive to workload/input context inside configurable software systems.

Existing public-repo assets to reuse:

- `scripts/kw_cost_vs_size.py --mode twins`
- `scripts/kw_cost_vs_size.py --mode workload`
- `scripts/run_twins_generated.py`
- `scripts/run_workload_generated.py`
- `cost_sampling/generated_sampling.py`
- `cost_sampling/pool_samplers.py`
- `artifacts/generated_sampling_protocol.md`
- `data/curated/energy/twins_energy_subset.zip`

Current gap:

- There is no dedicated `scripts/run_fse_posterior_twins_batch.py`.
- There is no dedicated `scripts/run_fse_posterior_workload_batch.py`.

Implementation task:

1. Factor reusable posterior logic from `scripts/run_fse_posterior.py` and the
   existing batch scripts.
2. Reuse generated-sampling data loaders and sample builders from the public
   ICSE repo.
3. Add two thin wrappers:
   - `scripts/run_fse_posterior_twins_batch.py`;
   - `scripts/run_fse_posterior_workload_batch.py`.
4. Keep output schemas parallel to the existing posterior scripts:
   - `posterior_strategy_summary.csv`;
   - `posterior_hypothesis_summary.csv`;
   - `posterior_hypothesis_tests.csv`;
   - family/context summary CSV;
   - per-context figures and reports.

Suggested ENERGY smoke target:

```bash
python3 scripts/run_fse_posterior_twins_batch.py \
  --zip data/curated/energy/twins_energy_subset.zip \
  --systems brotli lrzip \
  --target-props energy,performance \
  --cost-props energy,performance \
  --levels n8,n16,n32 \
  --seeds 30 \
  --srs-seeds 30 \
  --output-dir artifacts/fse_posterior_energy_smoke \
  --extreme max \
  --prior-offset 1
```

Suggested ENERGY final target, if runtime permits:

```bash
python3 scripts/run_fse_posterior_twins_batch.py \
  --zip data/curated/energy/twins_energy_subset.zip \
  --systems 7z Apache HSQLDB LLVM MongoDB PostgreSQL VP8 brotli exastencils \
            jump3r kanzi lrzip nginx x264 \
  --target-props energy,performance \
  --cost-props energy,performance \
  --levels n8,n16,n32,n64 \
  --seeds 100 \
  --srs-seeds 100 \
  --output-dir artifacts/fse_posterior_energy_final \
  --extreme max \
  --prior-offset 1
```

Suggested WORKLOAD smoke target:

```bash
python3 scripts/run_fse_posterior_workload_batch.py \
  --zip data/raw/workload_artifact.zip \
  --systems xz \
  --workload-limit 3 \
  --levels n8,n16,n32 \
  --seeds 30 \
  --srs-seeds 30 \
  --output-dir artifacts/fse_posterior_workload_smoke \
  --extreme max \
  --prior-offset 1
```

Suggested WORKLOAD final target:

```bash
python3 scripts/run_fse_posterior_workload_batch.py \
  --zip data/raw/workload_artifact.zip \
  --systems ALL \
  --workloads ALL \
  --levels n8,n16,n32,n64 \
  --seeds 100 \
  --srs-seeds 100 \
  --output-dir artifacts/fse_posterior_workload_final \
  --extreme max \
  --prior-offset 1
```

The command names above are target commands. If the wrappers do not exist yet,
creating them is part of this phase.

Required checks:

- Confirm generated samplers match the public ICSE generated-sampling protocol.
- Confirm whether target orientation should be `max` or `min` per property.
- Confirm that cost and target columns are not accidentally conflated.
- Report ENERGY and WORKLOAD separately, following the public repo's taxonomy.

Interpretation target:

- If posterior-risk results align with the ICSE count-vs-cost findings, then
  posterior guarantees become another outcome supporting "sample size is not
  sampling cost."
- If they diverge, document the boundary condition: posterior-bound quality may
  respond differently from prediction-error quality.

## 14. Phase 5: Linux/TuxKConfig Measured Pools

Goal:

- test FSE-style posterior risk on a large, structurally different
  configurable-system family;
- report results as pool-relative posterior risk.

Inputs:

- public repo preferred path: `data/raw/linux/tuxkconfig_*.parquet`;
- legacy posterior-runner path: `ICPE-rawdata/linux/tuxkconfig_*.parquet`.

The current `scripts/run_fse_posterior_linux_batch.py` uses a hardcoded
`ICPE-rawdata/linux/...` release map. For final public-repo execution, either
patch that map to `data/raw/linux/...` or create a compatibility symlink:

```bash
mkdir -p ICPE-rawdata
ln -s ../data/raw/linux ICPE-rawdata/linux
```

Quick-pass command:

```bash
python3 scripts/run_fse_posterior_linux_batch.py \
  --releases ALL \
  --output-dir artifacts/fse_posterior_linux_all_quick_final \
  --target-column vmlinux \
  --levels 0.01,0.02 \
  --stochastic-runs 30 \
  --diversity-runs 5 \
  --uncertainty-runs 5 \
  --coverage-runs 5 \
  --srs-seeds 30 \
  --top-k-features 512 \
  --extreme max \
  --prior-offset 1 \
  --quick
```

Fuller command if time budget allows:

```bash
python3 scripts/run_fse_posterior_linux_batch.py \
  --releases ALL \
  --output-dir artifacts/fse_posterior_linux_all_full \
  --target-column vmlinux \
  --levels 0.01,0.02,0.05 \
  --stochastic-runs 100 \
  --diversity-runs 20 \
  --uncertainty-runs 20 \
  --coverage-runs 20 \
  --srs-seeds 100 \
  --top-k-features 512 \
  --extreme max \
  --prior-offset 1
```

Expected outputs:

- `fse_posterior_linux_report.md`
- `fse_posterior_linux_conclusion.md`
- `posterior_linux_release_summary.csv`
- `posterior_linux_budget_trends.csv`
- `posterior_strategy_summary.csv`
- `posterior_hypothesis_summary.csv`
- per-release reports and figures.

Required checks:

- Confirm all seven releases are present:
  - `413`, `415`, `420`, `500`, `504`, `507`, `508`.
- Confirm result scope is described as measured-pool relative.
- Previous quick-pass result:
  - strategy posterior-risk distributions differ in `11/14`;
  - SRS best cost-normalized in about `3/14`;
  - SRS on empirical Pareto frontier in about `8/14`;
  - empirical frontier changes in `14/14`.

Interpretation target:

- Linux weakens the universal SRS recommendation.
- This does not invalidate posterior risk; it shows the recommendation is
  sensitive to system family and empirical acquisition cost.

## 15. Phase 6: LCBench Measured Pools

Goal:

- use LCBench as a cross-domain stress test for the FSE posterior framework;
- determine whether posterior-risk strategy recommendations survive empirical
  runtime normalization.

Input:

- public repo preferred path: `data/raw/lcbench/data_2k_lw.json`;
- legacy working path: `/private/tmp/lcbench/data_2k_lw.json`.

Main no-oracle command:

```bash
python3 scripts/run_fse_posterior_lcbench_batch.py \
  --json data/raw/lcbench/data_2k_lw.json \
  --datasets ALL \
  --output-dir artifacts/fse_posterior_lcbench_no_oracles_final \
  --target-column final_val_accuracy \
  --cost-column time_total \
  --runtime-mode last \
  --max-budget 64 \
  --seeds 30 \
  --srs-seeds 30 \
  --no-oracles \
  --extreme max \
  --prior-offset 1
```

Optional diagnostic run with oracle strategies:

```bash
python3 scripts/run_fse_posterior_lcbench_batch.py \
  --json data/raw/lcbench/data_2k_lw.json \
  --datasets ALL \
  --output-dir artifacts/fse_posterior_lcbench_with_oracles_diagnostic \
  --target-column final_val_accuracy \
  --cost-column time_total \
  --runtime-mode last \
  --max-budget 64 \
  --seeds 30 \
  --srs-seeds 30 \
  --extreme max \
  --prior-offset 1
```

Expected outputs:

- `fse_posterior_lcbench_report.md`
- `fse_posterior_lcbench_conclusion.md`
- `posterior_lcbench_dataset_summary.csv`
- `posterior_lcbench_budget_trends.csv`
- `posterior_strategy_summary.csv`
- `posterior_hypothesis_summary.csv`
- per-dataset reports and figures.

Required checks:

- Expect 35 datasets and 210 dataset-budget scopes:
  - 35 datasets x 6 budgets.
- Previous no-oracle result:
  - strategy posterior-risk distributions differ in `155/210`;
  - SRS best cost-normalized in `0/210`;
  - SRS on empirical Pareto frontier in about `20/210`;
  - empirical top recommendation changes in about `119/210`;
  - empirical frontier changes in about `207/210`.

Interpretation target:

- LCBench does not refute the FSE framework.
- LCBench strongly challenges broad, domain-independent SRS recommendation.
- Phrase all claims as reference-relative measured-pool posterior risk.

## 16. Phase 7: Cross-Corpus Synthesis

Goal:

- turn per-corpus outputs into one coherent table and a small number of
  paper-ready figures.

Create a synthesis table with columns:

- corpus;
- number of systems, contexts, or scopes;
- strategy-risk distributions differ;
- SRS best empirical-cost-normalized;
- SRS on empirical Pareto frontier;
- top recommendation changed by cost;
- Pareto frontier changed by cost;
- SRS lower risk than random;
- SRS cost different from random;
- direct replication or external-validity status.

Use current numbers as a sanity target:

| Corpus | Scopes | Risk distributions differ | SRS best cost-normalized | SRS on empirical Pareto | Top changes | Frontier changes |
|---|---:|---:|---:|---:|---:|---:|
| FSE artifact | 7 | TBD or per-system | 3/7 | 6/7 | 2/7 | 6/7 |
| x264 | 34 | 34/34 | 26/34 | 29/34 | 2/34 | 30/34 |
| ENERGY | TBD | TBD | TBD | TBD | TBD | TBD |
| WORKLOAD | TBD | TBD | TBD | TBD | TBD | TBD |
| Linux quick | 14 | 11/14 | 3/14 | 8/14 | 9/14 | 14/14 |
| LCBench | 210 | 155/210 | 0/210 | 20/210 | 119/210 | 207/210 |

Recommended synthesis figures:

1. Corpus-level heatmap:
   - rows: corpus;
   - columns: H1 to H6;
   - cells: support rate.
2. SRS status matrix:
   - rows: corpus/scopes;
   - columns: best, Pareto, lower risk than random, cost differs.
3. Cost-normalization impact plot:
   - changed top recommendation;
   - changed Pareto frontier.
4. Three representative guarantee-cost frontiers:
   - SRS best;
   - SRS Pareto but not best;
   - SRS not Pareto.
5. Calibration plot:
   - `pct_n` versus `pct_cost`;
   - line `y = x`;
   - color by strategy.

## 17. Phase 8: Paper-Ready Claims

Candidate claim A:

> FSE-style posterior risk and confidence can be reproduced and extended across
> multiple measured reference universes.

Candidate claim B:

> Empirical acquisition cost changes the strategy decision surface. The Pareto
> frontier changes far more often than the top scalar recommendation alone.

Candidate claim C:

> SRS remains strong on the original FSE-style configurable-system setting and
> on x264, but it is not a universal empirical-cost-normalized recommendation.

Candidate claim D:

> Linux and LCBench are external-validity stress tests: they preserve the
> usefulness of posterior risk while revealing boundary conditions for SRS.

Candidate claim E:

> ENERGY and WORKLOAD determine whether the posterior-guarantee version of the
> question behaves like the ICSE prediction-error version when the cost property
> or workload context changes.

Avoid:

- "LCBench refutes FSE 2026."
- "SRS is bad."
- "Posterior risk is invalid on Linux."
- "Measured-pool posterior risk is the same as exhaustive configuration-space
  posterior risk."

Prefer:

- "SRS recommendation is dataset- and cost-dependent."
- "Posterior risk remains valid relative to the measured reference universe."
- "Sample size is an incomplete cost abstraction for posterior guarantees."

## 18. Deliverable Checklist

For each corpus, deliver:

- source repository and git commit;
- aggregate Markdown report;
- aggregate CSV summary;
- hypothesis summary CSV;
- hypothesis tests CSV;
- per-context or per-system reports;
- key figures;
- command manifest;
- short caveat note about scope and data completeness.

For the whole study, deliver:

- one synthesis Markdown;
- one synthesis CSV;
- paper-level figures;
- final TODO list;
- reproduction commands;
- data provenance notes.

## 19. Agent Handoff Rules

When another agent takes over:

1. Start by reading this roadmap and
   `FSE2026_POSTERIOR_COST_REPLICATION_REPORT.md`.
2. Also read, in the public ICSE repo:
   - `README.md`;
   - `data/README.md`;
   - `docs/TRACEABILITY.md`;
   - `artifacts/dataset_family_framing.md`.
3. Check `git status --short` in whichever repository is being edited.
4. Decide and state whether the task is being done in:
   - `cost-sampling-matters`; or
   - `acherm/cost-sampling-icse2027`.
5. Do not overwrite existing artifact directories unless explicitly asked.
   Use a new suffix such as `_final`, `_rerun`, or a dated name.
6. Record every command that produces final results.
7. Keep direct replication claims separate from external-validity claims.
8. Use pool-relative language for Linux and LCBench.
9. Do not commit large generated artifacts without user approval.
10. If a run fails because external data are missing, report the missing path
   and the expected input format.

## 20. Immediate Next Actions

Highest-priority next actions:

1. Decide whether the next execution target is this working repo or the public
   `acherm/cost-sampling-icse2027` repo.
2. Audit SRS against the FSE artifact implementation.
3. Freeze prior-confidence convention and run `prior-offset` sensitivity.
4. Rerun the direct FSE artifact experiment with a clean final output path.
5. Rerun x264 final protocol using the public repo's `data/raw/AllRuns.zip`
   layout where possible.
6. Implement or port posterior wrappers for `ENERGY` and `WORKLOAD` by reusing
   the public repo's generated-sampling code.
7. Decide whether Linux quick pass is enough or whether a fuller Linux run is
   needed.
8. Ensure LCBench JSON provenance is documented and rerun the no-oracle final
   protocol.
9. Build the cross-corpus synthesis table and figures.
10. Write the final interpretation around "posterior guarantees per empirical
   acquisition cost."
