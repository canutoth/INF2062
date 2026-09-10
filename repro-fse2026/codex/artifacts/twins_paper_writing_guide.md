# Paper-Writing Guide: TwinsOrFalseFriends Generated-Sampling Tier

## What This Experiment Is

This tier evaluates the sampling-cost RQs on the Green Configuration / TwinsOrFalseFriends dataset. It is different from the ICPE x264 and Kaltenecker/NewRuns tiers because TwinsOrFalseFriends provides measured configuration tables but no precomputed sampling traces. We therefore use the generated-sampling protocol: sample configurations from the measured universe with a common strategy suite and budget grid, then compute empirical acquisition cost as the sum of the selected configurations' measured property values.

Dataset source: Zenodo `7544891`, companion archive `AI-4-SE/TwinsOrFalseFriends`. The local archive used here is `/private/tmp/TwinsOrFalseFriends-ICSE2023.zip`.

Systems covered in the broad pass: `7z`, `Apache`, `brotli`, `exastencils`, `HSQLDB`, `jump3r`, `kanzi`, `LLVM`, `lrzip`, `MongoDB`, `nginx`, `PostgreSQL`, `VP8`, and `x264`.

Measured properties: `performance` and `energy`. Both can be used as the acquisition-cost axis and as the prediction target, giving four scenarios:

- cost=`performance`, target=`performance`
- cost=`performance`, target=`energy`
- cost=`energy`, target=`performance`
- cost=`energy`, target=`energy`

RQ1 and RQ2 are reported by cost property. RQ3 and RQ4 are reported by cost-target scenario.

## Experimental Protocol

Sampling strategies:

- `random`: uniform random baseline.
- `balanced`: feature-balanced random sampling.
- `diversity`: cost-oblivious diversity over the feature space.
- `pairwise`: greedy pairwise option-value coverage.
- `pilotCost`: pilot-based cost-aware diversity.
- `cheapOracle` and `expensiveOracle`: diagnostic lower/upper bounds using true cost labels. Do not describe these as deployable strategies.

Budget grid:

- Percentage anchors and absolute anchors from `artifacts/generated_sampling_protocol.md`.
- The quick batch used max budget `32` for speed.
- Focused example runs used larger grids up to `256` where feasible.

Learner:

- Current main learner is `ridge-log`: ridge regression on log-transformed targets.
- The infrastructure also supports `ridge-raw`, `cart-log`, and `cart-raw`.
- Treat learner choice as a robustness dimension for RQ3/RQ4. RQ1/RQ2 are cost-axis questions and do not depend on the learner except through generated sample reuse.

Broad-batch command used for the current exploratory results:

```bash
python3 scripts/run_twins_batch.py --seeds 3 --max-budget 32 --max-rows 5000 --output-dir artifacts/twins_generated_quick --continue-on-error
python3 scripts/run_twins_hypotheses.py --input-dir artifacts/twins_generated_quick
python3 scripts/summarize_twins_generated_batch.py --input-dir artifacts/twins_generated_quick
```

Stronger representative run now available:

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

Use `twins_generated_representative_100s/` as the stronger Twins evidence:
seven selected systems, 100 stochastic seeds, no row caps, and max budget 256.
Use `twins_generated_quick/` for broad 14-system triage only.
The deployable-only brotli plotting command excludes `cheapOracle` and
`expensiveOracle`, which makes the fixed-`n=8` strategy comparison suitable for
paper figures about actionable sampling strategies.

Focused examples already available:

```bash
python3 scripts/run_twins_generated.py --system HSQLDB --seeds 20 --output-dir artifacts/twins_HSQLDB_generated
python3 scripts/run_twins_generated.py --system brotli --where revision=1.0.7 --seeds 20 --output-dir artifacts/twins_brotli_1_0_7_generated
python3 scripts/run_twins_generated.py --system PostgreSQL --where revision=9.6.3 --seeds 20 --output-dir artifacts/twins_PostgreSQL_9_6_3_generated
```

Formal hypothesis reports have also been computed for these focused folders:

- `artifacts/twins_HSQLDB_generated/twins_hypothesis_report.md`
- `artifacts/twins_brotli_1_0_7_generated/twins_hypothesis_report.md`
- `artifacts/twins_PostgreSQL_9_6_3_generated/twins_hypothesis_report.md`

## Where To Find The Results

Main broad-batch report:

- `artifacts/twins_generated_representative_100s/twins_generated_batch_report.md`
- `artifacts/twins_generated_representative_100s/twins_hypothesis_report.md`
- `artifacts/twins_generated_quick/twins_generated_batch_report.md`

Formal hypothesis report:

- `artifacts/twins_generated_quick/twins_hypothesis_report.md`

Main CSV tables:

- `artifacts/twins_generated_quick/scenario_summary.csv`: one row per system and cost-target scenario.
- `artifacts/twins_generated_quick/hypothesis_tests.csv`: one row per H1--H4 test scope.
- `artifacts/twins_generated_quick/hypothesis_summary.csv`: support/refute/inconclusive counts.
- `artifacts/twins_generated_quick/strategy_calibration_summary.csv`: per-strategy bootstrap calibration summary.
- Per-system `records.csv`, `strategy_summary.csv`, `rq1_cost_heterogeneity.csv`, `rq2_proxy_summary.csv`, `rq3_rank_stability.csv`, and `rq4_pareto.csv` live under `artifacts/twins_generated_quick/<system>/`.

Best broad-batch figures:

- `artifacts/paper_figures/twins_brotli_pairwise_n8/`: curated paper-facing copy of the brotli explanatory figures, including caption and provenance notes.
- `artifacts/paper_figures/twins_jump3r_runlevel_n_proxy_counterexample/`: run-level fixed-`n=128` witness with about 17.5% MRE and a 12.5x empirical-cost gap.
- `artifacts/paper_figures/twins_lrzip_n_proxy_counterexample/`: fixed-`n=16` counterexample showing nearly identical MRE but a 16.5x empirical-cost gap.
- `artifacts/twins_generated_representative_100s/fig_cost_cv_range_by_system.png`
- `artifacts/twins_generated_representative_100s/fig_rq2_proxy_spearman_by_system_cost.png`
- `artifacts/twins_generated_representative_100s/fig_rq2_median_calibration_by_system_cost.png`
- `artifacts/twins_generated_representative_100s/fig_rq3_top1_agreement_heatmap.png`
- `artifacts/twins_generated_representative_100s/fig_rq4_pareto_jaccard_heatmap.png`
- `artifacts/twins_generated_representative_100s/fig_twins_hypothesis_verdicts.png`
- `artifacts/twins_generated_representative_100s/fig_explain_strategy_calibration_heatmap.png`
- `artifacts/twins_generated_representative_100s/<system>/fig_explain_cost_error_*.png`
- `artifacts/twins_generated_representative_100s/<system>/fig_explain_strategy_budget_path_*.png`
- `artifacts/twins_generated_representative_100s/<system>/fig_explain_fixed_n8_*.png`
- `artifacts/twins_generated_representative_100s/brotli_1_0_7/fig_explain_fixed_n8_cost_performance__target_energy_deployable.png`
- `artifacts/twins_generated_quick/fig_cost_cv_range_by_system.png`: RQ1 heterogeneity.
- `artifacts/twins_generated_quick/fig_rq2_proxy_spearman_by_system_cost.png`: RQ2 rank-proxy validity.
- `artifacts/twins_generated_quick/fig_rq2_median_calibration_by_system_cost.png`: RQ2 calibration.
- `artifacts/twins_generated_quick/fig_rq3_top1_agreement_heatmap.png`: RQ3 scenario-faceted rank stability.
- `artifacts/twins_generated_quick/fig_rq4_pareto_jaccard_heatmap.png`: RQ4 scenario-faceted Pareto-front overlap.
- `artifacts/twins_generated_quick/fig_twins_hypothesis_verdicts.png`: formal verdict counts.

Best per-system figures:

- `fig_rq2_calibration_cost_performance.png`
- `fig_rq2_calibration_cost_energy.png`
- `fig_rq3_rank_agreement_by_scenario.png`
- `fig_rq4_pareto_jaccard_by_scenario.png`
- `fig_rq4_frontier_cost_performance__target_performance.png`
- `fig_rq4_frontier_cost_performance__target_energy.png`
- `fig_rq4_frontier_cost_energy__target_performance.png`
- `fig_rq4_frontier_cost_energy__target_energy.png`

The frontier figures are the most intuitive for RQ4 because the x-axis is empirical cost and the y-axis is MRE.

For explanatory mechanism figures, use the three views together rather than
substituting one for all purposes. `fig_explain_cost_error_*.png` keeps every
run-level point, so it shows stochastic spread but can be busy. The
`fig_explain_strategy_budget_path_*.png` view aggregates to one point per
strategy/budget and is better for showing how a strategy moves as `n` grows.
The `fig_explain_fixed_n8_*.png` view fixes `n` and is best when the paper
needs a direct same-budget strategy comparison. The brotli deployable-only
fixed-`n=8` figure is the clearest current example: `pairwise` is much more
costly and much less accurate than `random`, `balanced`, and `pilotCost` for
cost=`performance`, target=`energy`.

## RQ Answers From The Current Broad Pass

Representative 100-seed run:

RQ1: empirical acquisition cost is heterogeneous in the selected systems. Cost CV spans `0.05751` to `7.104` across 14 system-cost contexts. H1a is supported in `11/14` contexts, and H1b is supported in `14/14`, giving stronger evidence that strategies induce different empirical costs at fixed `n`.

RQ2: sample size is consistently rank-correlated with empirical cost, but calibration remains strategy-dependent. H2a is supported in `14/14` contexts and H2c in `14/14`. H2b is mixed: only `4/14` contexts have aggregate median calibration clearly away from 1, so the stronger message is not that `n` is always badly calibrated, but that strategy-specific bias survives even when the aggregate median looks calibrated.

RQ3: empirical cost changes cost-sensitive strategy rankings in `24/28` selected-system scenarios. The cross-scenario H3b correlation is stronger than in the quick batch: Spearman rho `0.719`.

RQ4: empirical-cost Pareto frontiers differ from count-cost frontiers in `28/28` selected-system scenarios. This remains the clearest decision-level result.

Quick 14-system triage batch:

RQ1: empirical acquisition cost is heterogeneous, but not uniformly so. Cost CV spans `0.05751` to `7.104` across 28 system-cost contexts. H1a is supported in `23/28` contexts. The strongest cases are `jump3r`, `lrzip`, `kanzi`, and `brotli`; the clearest contrasts are `PostgreSQL`, `LLVM`, and `MongoDB`.

RQ1 caveat: H1b is inconclusive in the quick batch because three seeds underpower fixed-n Kruskal-Wallis tests. The effect sizes are often large, so this should be rerun with more seeds before making a formal strategy-effect claim for Twins.

RQ2: sample size is a useful ordering proxy but not a calibrated cost model. Spearman rho spans `0.413` to `0.9735`, and H2a is supported in `28/28` contexts. H2b is supported in only `5/28` contexts and refuted in `15/28`, meaning aggregate median calibration is often close to 1. However, H2c is supported in `27/28` contexts, so strategy-specific calibration remains necessary.

RQ3: empirical cost often changes cost-sensitive strategy rankings. H3a is supported in `54/56` cost-target scenarios. H3b is supported across scenarios with Spearman rho `0.657` between cost CV and top-1 flip count.

RQ4: empirical-cost Pareto frontiers differ from count-cost frontiers in every broad-pass scenario. H4a and H4b are supported in `56/56` scenarios. This is currently the strongest decision-level result for Twins.

## Suggested Paper Use

Use Twins as the generated-protocol and cost-property expansion, not as a direct aggregate with x264 ICPE or NewRuns. A safe paragraph is:

> TwinsOrFalseFriends extends the study to a setting without precomputed sampling traces and to two measured properties, performance and energy. We therefore generate a common sampling panel over the measured configuration universe and evaluate the four cost-target scenarios separately. The broad pass shows that sample size remains positively correlated with acquisition cost, but strategy-specific calibration and decision-level frontiers still change when empirical cost replaces count cost.

Use `jump3r`, `brotli`, or `lrzip` as high-heterogeneity examples. Use `PostgreSQL` or `LLVM` as low-heterogeneity contrasts. Use `x264` or `HSQLDB` from this tier when you want a system that is easy to connect back to earlier paper sections.

## Caveats To State

- The `twins_generated_quick/` folder is exploratory: 3 seeds, max budget 32, and 5000-row caps for `7z`, `exastencils`, `LLVM`, `lrzip`, and `MongoDB`.
- H1b should not be claimed as formally supported from the quick batch.
- Diagnostic oracles are bounds, not deployable strategies.
- Generated-protocol results should not be silently aggregated with precomputed-sampling results.
- If `performance` is throughput for a system, orient it before using it as cost, for example `cost=1/performance`.

## Final-Run Recommendation

For paper-grade Twins evidence, rerun selected representatives with at least 100 seeds and no row cap where feasible:

- high heterogeneity: `jump3r`, `brotli`, `lrzip`
- low heterogeneity contrast: `PostgreSQL`, `LLVM`
- moderate familiar case: `HSQLDB` or `x264`

After rerunning, apply:

```bash
python3 scripts/run_twins_hypotheses.py --input-dir <final-output-dir>
python3 scripts/summarize_twins_generated_batch.py --input-dir <final-output-dir>
```

Use the summarizer when `<final-output-dir>` is a batch folder with
`system_summary.csv`. For a single-system folder, run the hypothesis script and
use the system's own generated report.
