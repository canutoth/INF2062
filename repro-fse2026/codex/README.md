# Empirical Sampling-Cost Experiments

This repository now contains a small Python proof-of-concept infrastructure for
the RQs in `PLAN.md`.  The first runnable case is `x264_time_0`, using the
sampled configuration CSVs inside `ICPE-rawdata/AllRuns.zip`.

## Run the proof of concept

```bash
python3 scripts/run_poc.py --context x264_time_0
```

The script depends only on `numpy` and `matplotlib`, which are already available
in the current environment.  It does not unpack the large archives; it reads the
needed CSV files directly from the zip.

## What it produces

By default, outputs are written to `artifacts/poc_x264_time_0/`:

- `records.csv`: one row per `(context, run, strategy, level)` with `n`,
  empirical training cost, calibration ratio, and MRE.
- `rq1_cost_heterogeneity.csv`: per-configuration cost distribution summary.
- `strategy_summary.csv`: median/IQR cost, calibration, MRE, and overhead
  relative to random at the same sample level.
- `rq2_proxy_summary.csv`: Spearman correlation and calibration bias summaries.
- `rq3_rank_stability.csv`: count-cost vs empirical-cost rank agreement for the
  lambda sweep from `PLAN.md`.
- `rq4_pareto.csv`: count-based and empirical-cost Pareto labels.
- `fig_*.png`: first figures for RQ1-RQ4.
- `summary.md`: short human-readable snapshot of the run.

## Current modeling choices

For time contexts, empirical acquisition cost is the sampled row's `Performance`
value. In `x264_time_0`, this is both the prediction target and the cost of
measuring a configuration, which matches the Tier 1 time-property case in
`PLAN.md`. For size contexts, the target remains `x264_size_i` performance, but
cost is joined from the matching `x264_time_i` context.

The learner is a lightweight ridge/log-linear model implemented with `numpy`.
This is intentionally simple and reproducible.

## Run the x264 size batch

```bash
python3 scripts/run_x264_size_batch.py
```

This analyzes `x264_size_0` through `x264_size_16`, using the matching
`x264_time_i` context as empirical acquisition cost. Aggregate outputs are
written to `artifacts/x264_size_all/`, including `x264_size_report.md`,
`context_summary.csv`, RQ-level CSV files, and aggregate figures.

For a single size context, `scripts/run_poc.py` infers the matching time-cost
context automatically:

```bash
python3 scripts/run_poc.py --context x264_size_0
```

## Run the x264 time batch

```bash
python3 scripts/run_x264_time_batch.py
```

This analyzes `x264_time_0` through `x264_time_16`, using time as both the
prediction target and empirical acquisition cost. Aggregate outputs are written
to `artifacts/x264_time_all/`, including `x264_time_report.md`.

## Run the full 2x2 matrix

```bash
python3 scripts/run_x264_matrix.py
```

This evaluates all four combinations of cost property and prediction target:
time/time, time/size, size/time, and size/size. It writes
`artifacts/x264_matrix/x264_matrix_report.md`, where RQ1/RQ2 are grouped by cost
property and RQ3/RQ4 are reported per cost-target scenario.

## Run a non-x264 system

```bash
python3 scripts/run_system_report.py --context BerkeleyDBC
```

This uses `ICPE-rawdata/NewRuns.zip`, whose non-x264 systems expose sampled
configuration CSVs. The default example writes
`artifacts/BerkeleyDBC_performance/BerkeleyDBC_performance_report.md`.

Unlike x264, these systems expose a single `Performance` property in the sampled
CSVs, so the report is a single diagonal scenario:
`cost=performance, target=performance`. It is not a full time/size matrix, but
it exercises the same RQ1-RQ4 infrastructure on another configurable system.

Other compatible contexts include `7z`, `Dune`, `LLVM`, `lrzip`, `Polly`,
`Hipacc`, and `x264`.

## Run the NewRuns non-x264 batch

```bash
python3 scripts/run_newruns_batch.py
```

This systematizes the same single-property analysis for the NewRuns systems that
expose sampled configuration CSVs: `7z`, `BerkeleyDBC`, `Dune`, `Hipacc`,
`LLVM`, `Polly`, and `lrzip`. It writes a cross-system report to
`artifacts/newruns_systems/newruns_systems_report.md`, plus one per-system
report and RQ-level CSV files under `artifacts/newruns_systems/<system>/`.

## Run FSE-style posterior guarantee analysis

```bash
python3 scripts/run_fse_posterior.py --context LLVM --levels t2 --include-srs
```

This computes the FSE 2026 posterior-risk/posterior-confidence view for
sampled performance bounds. In this family, posterior risk replaces MRE as the
outcome: the report compares sampling strategies by empirical acquisition cost
versus bound guarantees. Outputs are written to
`artifacts/fse_posterior_<context>/`:

- `posterior_records.csv`: one row per sample with observed bound, posterior
  risk, sample size, empirical cost, and effective cost-normalized `n`.
- `posterior_strategy_summary.csv`: per-strategy/level risk quantiles,
  integrated posterior confidence, and confidence discrepancy against both
  sample-size and empirical-cost baselines.
- `posterior_confidence_curves.csv`: posterior/prior confidence curves.
- `posterior_pareto.csv`: count-cost and empirical-cost Pareto labels for
  risk and integrated confidence.
- `posterior_hypothesis_tests.csv`: FSE-style tests for strategy effects,
  SRS-vs-random behavior, and whether cost-normalization changes the
  recommendation or Pareto frontier.
- `fig_*.png`: posterior risk, confidence discrepancy, cost/confidence
  frontier, and integrated-confidence discrepancy plots.

With `--include-srs`, the script generates Statistical Recursive Search samples
using the FSE artifact defaults: recursive step size `25`, Welch's t-test, and
random fill to the requested sample size.

After extracting the FSE 2026 artifact's `data.zip`, the same runner can read
the paper's `data/sampling/<system>/...` layout directly:

```bash
python3 scripts/run_fse_posterior.py --fse-root /path/to/extracted/data/sampling --context LLVM --levels t2 --strategies random,solverBased,divDistBased,twise,SRSSampling
```

For the cross-system reproduction, run:

```bash
python3 scripts/run_fse_posterior_batch.py --fse-root /path/to/extracted/data/sampling
```

This writes per-system reports and a cross-system RQ-style summary to
`artifacts/fse_posterior_fse_artifact_all/`.

To revisit the FSE posterior-risk experiments on the ICPE x264 corpus, run:

```bash
python3 scripts/run_fse_posterior_x264_batch.py --contexts 0-16 --target-props time,size
```

This uses the existing ICPE sampling traces, generates SRS samples, treats
`x264_time_i` as empirical acquisition cost by default, and writes the
cross-input report to `artifacts/fse_posterior_x264_icpe/`.

To revisit the same questions on Linux/TuxKConfig measured pools, run:

```bash
.venv/bin/python scripts/run_fse_posterior_linux_batch.py --releases 508 --quick
```

This uses the local parquet files under `ICPE-rawdata/linux/`, the existing
Linux sampling strategies, and generated SRS samples. The interpretation is
different from the FSE artifact and x264: Linux is treated as a large measured
pool, not an exhaustive full configuration space, so posterior risk/confidence
hold relative to the measured TuxKConfig pool. For a broader pass:

```bash
.venv/bin/python scripts/run_fse_posterior_linux_batch.py --releases 415,420,500,504,507,508 --quick
```

`413` is also supported, but it is substantially larger than the other local
parquets and should be run as a heavier job. Outputs are written to
`artifacts/fse_posterior_linux/` by default, with per-release reports, CSVs, and
the same posterior-risk/confidence figures as the other FSE-style runners.

LCBench can also be used as a non-configurable-software external validation
family. Each OpenML dataset is treated as one measured reference pool, and each
hyperparameter configuration is the sampled object:

```bash
.venv/bin/python scripts/run_fse_posterior_lcbench_batch.py --json /private/tmp/lcbench/data_2k_lw.json --quick --no-oracles
```

The raw JSON is not stored in this repository; the expected file is
`data_2k_lw.json` from the LCBench lightweight archive. This runner computes
reference-relative posterior risk over the measured LCBench pools, generates
SRS samples, and compares posterior confidence under sample-size and empirical
runtime-cost normalization. Use `--no-oracles` for the deployable-strategy
recommendation; omit it only for diagnostic oracle-inclusive reports. Outputs are written to
`artifacts/fse_posterior_lcbench/` by default.

## Run the generated-sampling protocol

```bash
python3 scripts/run_twins_generated.py --system HSQLDB --seeds 20
```

This uses the TwinsOrFalseFriends Zenodo archive and generates a common
sampling strategy/budget grid because that dataset does not provide
precomputed sampling traces. The default HSQLDB run evaluates the four
`performance/energy` cost-target scenarios and writes
`artifacts/twins_HSQLDB_generated/HSQLDB_generated_report.md`.

Revision-scoped examples:

```bash
python3 scripts/run_twins_generated.py --system brotli --where revision=1.0.7 --seeds 20 --output-dir artifacts/twins_brotli_1_0_7_generated
python3 scripts/run_twins_generated.py --system PostgreSQL --where revision=9.6.3 --seeds 20 --output-dir artifacts/twins_PostgreSQL_9_6_3_generated
```

For paper-scale stochastic replication, increase `--seeds` to `100`. If a
performance column is throughput and you want to use it as cost, pass an
orientation override such as:

```bash
python3 scripts/run_twins_generated.py --system HSQLDB --cost-orientation performance=inverse
```

To run a broad exploratory pass over all TwinsOrFalseFriends systems:

```bash
python3 scripts/run_twins_batch.py --seeds 3 --max-budget 32 --max-rows 5000 --output-dir artifacts/twins_generated_quick
python3 scripts/run_twins_hypotheses.py --input-dir artifacts/twins_generated_quick
python3 scripts/summarize_twins_generated_batch.py --input-dir artifacts/twins_generated_quick
```

This writes `artifacts/twins_generated_quick/twins_generated_batch_report.md`.
It also writes `twins_hypothesis_report.md`, `hypothesis_tests.csv`,
`hypothesis_summary.csv`, and scenario-faceted RQ figures. The batch is
intended for coverage and triage; rerun selected systems without row caps and
with more seeds for final paper evidence. See
`artifacts/twins_paper_writing_guide.md` for the current paper-writing map.

For a stronger representative pass:

```bash
python3 scripts/run_twins_batch.py \
  --systems HSQLDB,brotli,jump3r,lrzip,MongoDB,PostgreSQL,x264 \
  --seeds 100 \
  --max-budget 256 \
  --max-rows 0 \
  --output-dir artifacts/twins_generated_representative_100s \
  --continue-on-error

python3 scripts/run_twins_hypotheses.py --input-dir artifacts/twins_generated_representative_100s
python3 scripts/summarize_twins_generated_batch.py --input-dir artifacts/twins_generated_representative_100s
python3 scripts/plot_twins_explanatory_bias.py --input-dir artifacts/twins_generated_representative_100s --fixed-levels n8
python3 scripts/plot_twins_explanatory_bias.py --input-dir artifacts/twins_generated_representative_100s --systems brotli_1.0.7 --scenarios performance:energy --fixed-levels n8 --exclude-oracles
python3 scripts/summarize_twins_generated_batch.py --input-dir artifacts/twins_generated_representative_100s
```

This produces a seven-system, no-row-cap Twins run that is more appropriate
for paper evidence than the 3-seed triage batch. The explanatory plotting step
adds calibration-bias, run-level cost-distribution/MRE, strategy-budget
aggregate, and fixed-`n` comparison figures that help interpret why some
strategies are expensive without being predictive enough. The second plotting
command creates deployable-only brotli figures that exclude diagnostic oracles.
