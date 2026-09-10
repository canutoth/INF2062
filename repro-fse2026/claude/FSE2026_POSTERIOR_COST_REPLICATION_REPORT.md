# FSE 2026 Posterior Guarantees Under Empirical Acquisition Cost

Status as of 2026-07-03. Final reruns executed on branch `fse/posterior-cost`
(worktree `csm-fse-posterior`); commands, provenance, and verification in
`artifacts/FSE2026_POSTERIOR_RUN_MANIFEST.md`; cross-corpus rollup in
`artifacts/fse_posterior_synthesis/`.

## Executive Summary

This line of work connects two papers:

1. The FSE 2026 paper on posterior risk, posterior confidence, integrated confidence discrepancy, and Statistical Recursive Search (SRS) for performance-bound sampling.
2. Our submitted paper, "Sample Size Is Not Sampling Cost", which argues that fixed sample size is not necessarily fixed empirical acquisition cost.

The central question is:

> Does SRS remain the best recommendation once posterior guarantees are normalized by empirical acquisition cost rather than by sample size?

The current answer is nuanced:

- The FSE posterior-risk framework transfers well. Posterior risk/confidence can be computed on the original FSE systems, x264, Linux measured pools, and LCBench measured pools.
- SRS remains strong in the direct FSE-artifact setting and especially on x264.
- SRS does not remain a universal best recommendation once empirical acquisition cost is considered.
- Linux and LCBench are strong external-validity stress tests: they support the posterior-risk framework but weaken the generality of the SRS recommendation.
- The ENERGY (Twins, 14 systems) and WORKLOAD (ICSE'23, 9 systems / 93 contexts) generated-protocol families now confirm the same pattern at small budgets (n8-n64): posterior-risk distributions discriminate strategies in ~95% of scopes, the empirical-cost Pareto frontier changes in 96-100% of scopes, and SRS is best cost-normalized in under 10% of scopes (diversity/pairwise dominate there).
- The cleanest high-level claim is not "FSE is wrong"; it is "the FSE guarantee framework becomes more realistic when combined with measured acquisition cost, and the preferred strategy is then dataset-dependent."

## Basic Motivation

The FSE 2026 paper asks whether the observed worst-case performance in a finite sample is trustworthy. It introduces posterior risk and posterior confidence as a way to quantify the remaining probability that unseen configurations violate the sampled performance bound.

Our submitted paper asks a different construct-validity question:

> Is sample size a good proxy for the effort required to acquire performance data?

The natural bridge is to replace the prediction-error outcome used in our submitted paper, such as MRE, with FSE-style posterior guarantees:

- old outcome: prediction error, such as MRE;
- new outcome: posterior risk, posterior confidence, and integrated confidence discrepancy;
- old question: is sample size a good proxy for prediction-study cost?
- new question: is sample size a good proxy for the cost of obtaining posterior performance-bound guarantees?

In lay terms: FSE tells us how confident we are that a sampled bound is safe; our cost work asks whether two strategies that sample the same number of configurations actually paid the same measurement cost. Combining the two asks which strategy gives the best guarantee for the cost actually spent.

## What Has Been Achieved

### Implemented Core Metrics

The repository now contains a reusable FSE-style posterior guarantee implementation:

- `cost_sampling/posterior.py`
  - posterior risk;
  - posterior confidence;
  - prior confidence;
  - integrated posterior confidence;
  - integrated confidence discrepancy;
  - confidence-curve rows for plotting.

The implementation follows the FSE artifact convention for the prior-confidence exponent offset by default:

```text
prior confidence = 1 - (1 - epsilon) ** (N + 1)
```

The code also allows the simplified `N` exponent form by changing the offset.

### Implemented SRS

The repository now contains:

- `cost_sampling/srs.py`

This is a code-native adaptation of the FSE artifact's `SRS-sampling.ipynb` behavior:

- recursive search;
- batch step size of 25 by default;
- Welch t-test with `p < 0.05` by default;
- final random fill if recursion stops before the requested sample size.

The last point is important because it matches the FSE paper footnote:

> SRS is supplemented with random configurations if needed so every strategy reaches the predetermined sample size.

This implementation should still be treated as "aligned but not yet audited line-by-line" until we compare it against the official artifact output on controlled examples.

### Implemented Experiment Entry Points

The following scripts now support FSE-style posterior experiments:

- `scripts/run_fse_posterior.py`
  - one context/system;
  - posterior records;
  - summaries;
  - hypothesis tests;
  - Pareto frontiers;
  - figures.
- `scripts/run_fse_posterior_batch.py`
  - original FSE artifact systems.
- `scripts/run_fse_posterior_x264_batch.py`
  - REPLICATION-ICPE/x264.
- `scripts/run_fse_posterior_linux_batch.py`
  - Linux/TuxKConfig measured pools.
- `scripts/run_fse_posterior_lcbench_batch.py`
  - LCBench measured pools.

Generated figure families include:

- posterior risk by strategy;
- posterior/prior confidence discrepancy;
- integrated confidence discrepancy;
- guarantee-cost Pareto/frontier plots.

## Current Results

These results should be treated as current working evidence. They need protocol realignment before becoming paper-ready claims.

### Summary Table

Final-rerun numbers (2026-07-03; `artifacts/fse_posterior_*_final*`,
machine-readable rollup in
`artifacts/fse_posterior_synthesis/fse_posterior_synthesis.csv`):

| Corpus | Scope | Key result | Current interpretation |
|---|---:|---|---|
| Original FSE artifact systems | 7 systems | Posterior-risk distributions differ in 7/7; SRS best empirical-cost-normalized in 3/7; SRS on empirical Pareto frontier in 6/7; cost normalization changes the top recommendation in 2/7; Pareto frontier changes in 6/7. | Direct FSE-style replication supports posterior guarantees and keeps SRS competitive, but not universally best under measured cost. |
| REPLICATION-ICPE/x264 | 34 target contexts | Strategy posterior-risk distributions differ in 34/34; SRS best cost-normalized in 26/34; SRS on empirical Pareto frontier in 29/34; cost normalization changes the top recommendation in 2/34 and frontier in 30/34. | Strong external replication for SRS, while still showing that cost-aware frontiers change. |
| ENERGY (Twins) | 14 systems x {energy,performance} cost x {energy,performance} target x n8-n64 = 220 scopes | Distributions differ in 212/220; SRS best cost-normalized in 9/220; SRS on empirical Pareto frontier in 77/220; top changes in 31/220; frontier changes in 220/220; diversity/pairwise dominate cost-normalized picks. | Posterior guarantees per cost behave like the ICSE prediction-error outcome when cost means energy: the frontier is always cost-sensitive and SRS is not the small-budget recommendation. |
| WORKLOAD (ICSE'23) | 9 systems x 93 workload contexts x n8-n64 = 359 scopes | Distributions differ in 341/359; SRS best cost-normalized in 31/359; SRS on empirical Pareto frontier in 139/359; top changes in 61/359; frontier changes in 346/359. | Workload context shifts posterior-guarantee decisions the same way it shifts prediction-error decisions; SRS is occasionally competitive but not the default. |
| Linux/TuxKConfig | 7 releases x 3 budget levels = 21 scopes (full protocol: 100 stochastic runs, 100 SRS seeds, levels 1/2/5%) | Strategy posterior-risk distributions differ in 21/21; SRS best cost-normalized in 0/21; SRS on empirical Pareto frontier in 19/21; SRS cost differs from random in 21/21; cost normalization changes top recommendation in 13/21 and frontier in 21/21. | Pool-relative posterior risk is valid; at full statistical power SRS is never the cost-normalized winner on Linux, though it is almost always frontier-competitive. |
| LCBench | 35 datasets x 6 budget levels = 210 scopes | Strategy posterior-risk distributions differ in 154/210; SRS best cost-normalized in 0/210; SRS on empirical Pareto frontier in 21/210; cost normalization changes top recommendation in 120/210 and frontier in 207/210. | Strong external-validity stress test: the posterior-risk metric transfers, but the SRS recommendation does not. |

Across all six corpora that is 851 decision scopes; the empirical-cost
confidence Pareto frontier differs from the count-based frontier in 830/851
(97.5%) of them.

The quick-pass Linux run (2 levels, 30 stochastic runs; 14 scopes) is kept
in `artifacts/fse_posterior_linux_all_quick_final/` as a protocol
sensitivity: the fuller protocol strengthens rather than changes the
conclusions (risk-differ 79% -> 100%, SRS best 14% -> 0%, frontier change
100% -> 100%), and SRS's frontier membership rises from 57% to 90% with
100 SRS seeds — the quick pass understated SRS's frontier competitiveness.

### Original FSE Artifact Systems

Artifacts:

- `artifacts/fse_posterior_fse_artifact_all/fse_posterior_systems_report.md`
- `artifacts/fse_posterior_fse_artifact_all/fse_posterior_rq_conclusions.md`
- `artifacts/fse_posterior_fse_artifact_all/posterior_system_summary.csv`
- `artifacts/fse_posterior_fse_artifact_all/posterior_hypothesis_summary.csv`

Systems analyzed:

- `7z`
- `BerkeleyDBC`
- `Dune`
- `Hipacc`
- `JavaGC`
- `LLVM`
- `Polly`

The fixed-level run uses five strategies:

- `random`
- `solverBased`
- `divDistBased`
- `twise`
- `SRSSampling`

Current headline:

- SRS is the best empirical-cost-normalized strategy in `3/7` systems.
- SRS appears on the empirical cost/confidence Pareto frontier in `6/7` systems.
- Cost normalization changes the top integrated-confidence recommendation in `2/7` systems.
- Cost normalization changes the empirical-confidence Pareto frontier in `6/7` systems.
- SRS has lower posterior risk than random in `6/7` systems, with one inconclusive case.

Interpretation:

The direct FSE-artifact revisit does not refute FSE. It supports the framework and shows SRS is often strong. The added result is that "best at fixed sample size" and "best at fixed empirical acquisition cost" are not identical decision rules.

### REPLICATION-ICPE/x264

Artifacts:

- `artifacts/fse_posterior_x264_icpe/fse_posterior_x264_icpe_report.md`
- `artifacts/fse_posterior_x264_icpe/posterior_x264_context_summary.csv`
- `artifacts/fse_posterior_x264_icpe/posterior_hypothesis_summary.csv`
- per-context reports and figures under `artifacts/fse_posterior_x264_icpe/x264_*`

Scope:

- target properties: `time` and `size`;
- empirical acquisition cost: `time`;
- 17 input contexts per target, 34 contexts total;
- levels: `t1`, `t2`, `t3`;
- fixed-level summary: `t2`;
- generated SRS with 100 seeds per context/level.

Current headline:

- Strategy posterior-risk distributions differ in `34/34` target contexts.
- SRS is best empirical-cost-normalized in `26/34` contexts.
- SRS appears on the empirical cost/confidence Pareto frontier in `29/34` contexts.
- Cost normalization changes the top recommendation in `2/34` contexts.
- Cost normalization changes the confidence Pareto frontier in `30/34` contexts.
- SRS has lower posterior risk than random in `34/34` contexts.
- SRS empirical acquisition cost differs from random in `33/34` contexts.

Interpretation:

x264 is currently the strongest positive external replication for SRS. It also confirms our cost-validity concern: even when the top winner rarely changes, the set of Pareto-defensible choices changes in most contexts.

### ENERGY (Twins/TwinsOrFalseFriends)

Run 2026-07-03 via the new `scripts/run_fse_posterior_twins_batch.py`
(generated-sampling protocol from the public ICSE repo; strategies random,
balanced, pilotCost, diversity, pairwise + code-native SRS; 100 stochastic
seeds; budgets n8-n64 clamped by the protocol grid; no oracles).

Artifacts:

- `artifacts/fse_posterior_energy_final/fse_posterior_energy_report.md`
- `artifacts/fse_posterior_energy_final/posterior_energy_scenario_summary.csv`
- per-scenario folders `twins_<system>__cost_<c>__target_<t>/`

Result (14 systems x 4 cost/target combinations x up to 4 budgets = 220
scopes, no skips): distributions differ in 212/220; empirical-cost frontier
changes in 220/220; top recommendation changes in 31/220; SRS best
cost-normalized in 9/220 and on the empirical frontier in 77/220;
diversity (108/220) and pairwise (74/220) dominate best cost-normalized
picks.

Interpretation:

Changing the meaning of cost (energy versus runtime) does not rescue sample
count as a cost proxy: every scope's guarantee/cost frontier is
cost-sensitive. At n8-n64 budgets SRS is rarely the cost-normalized winner;
its strength in the FSE artifact and x264 settings comes with the much
larger t2-style budgets there.

### ENERGY equal-measured-spend sensitivity

The equal-n protocol handles cost via a prior-based handicap; an obvious
objection is that cheap strategies should instead be allowed to spend the
same measured budget and buy more configurations. The equal-spend
experiment (`scripts/run_energy_equal_spend.py`, checkpointed per
scenario; outputs in `artifacts/fse_posterior_energy_equal_spend/`) grants
exactly that: per scope, B = n_ref x mean pool cost, and every strategy
buys the sample size B affords (binary search per seed, protocol cap =
censoring, 12/110 pilotCost cap hits).

Results over 110 scopes (14 systems x {energy, performance} x n8-n64):

- pilotCost realizes a 2.05x median volume advantage (up to ~5x on
  cost-heterogeneous systems such as 7z and Apache) and still beats random
  in only 11/110 scopes; its median max-bound risk stays 6.6x worse than
  random's. Volume cannot substitute for the expensive tail it avoids:
  cost-effectiveness for prediction does not transfer to worst-case
  guarantees.
- SRS beats random at equal spend in 49/110 scopes overall, with a strong
  budget gradient: 1/28 at n8, 8/28 at n16, 20/28 at n32, 20/26 at n64.
  This reconciles the corpora: SRS's recursion needs budget to amortize,
  which is why it dominates at FSE/x264 t2 budgets (hundreds of samples)
  and underperforms at the generated families' small budgets.
- Equal-spend winners: diversity 47/110, pairwise 28/110, balanced and SRS
  14/110 each, random 4/110, pilotCost 3/110 — consistent with the
  handicap-based analysis, so the two methodologies agree.

The LCBench companion run (`scripts/run_lcbench_equal_spend.py`,
`artifacts/fse_posterior_lcbench_equal_spend/`, 140 scopes) tests the
mechanism's falsifiable prediction at the other end of the coupling
spectrum: with cost = training runtime and target = validation accuracy
(weakly coupled), pilotCost's equal-spend verdict flips — it beats random
in 84/140 scopes (60%) with a median risk ratio of 0.75, i.e. better than
random, from a 1.66x volume advantage. Cost-aware volume pays exactly
when the outcome-relevant information is not concentrated in the
expensive tail. diversity remains the overall equal-spend winner
(80/140), so the practical default is unchanged; the flip is the
mechanism evidence. Together the two runs ground the claim that
cost-effectiveness is a property of the (strategy, outcome, cost-target
coupling) triple, not of the strategy alone.

Run 2026-07-03 via the new `scripts/run_fse_posterior_workload_batch.py`
(same generated protocol; measured `time` column as both bound target and
acquisition cost, `throughput` with inverse orientation for h2).

Artifacts:

- `artifacts/fse_posterior_workload_final/fse_posterior_workload_report.md`
- `artifacts/fse_posterior_workload_final/posterior_workload_context_summary.csv`
- per-context folders `workload_<system>__<workload>/`

Result (9 systems, all 93 workload contexts of the study, 359 scopes, no
skips): distributions differ in 341/359; frontier changes in 346/359; top
recommendation changes in 61/359; SRS best cost-normalized in 31/359 and on
the empirical frontier in 139/359; pairwise (155/359) and diversity
(108/359) lead the cost-normalized picks.

Interpretation:

Workload context behaves for posterior guarantees the way it behaves for
prediction error in the submitted ICSE paper: the guarantee-per-cost
decision surface is workload-dependent, and the same system can prefer
different strategies on different inputs.

### Linux/TuxKConfig

Artifacts (full protocol, 2026-07-06):

- `artifacts/fse_posterior_linux_all_full/fse_posterior_linux_report.md`
- `artifacts/fse_posterior_linux_all_full/posterior_linux_release_summary.csv`
- per-release reports and figures under
  `artifacts/fse_posterior_linux_full_parts/r<release>/`
- quick-pass sensitivity retained in
  `artifacts/fse_posterior_linux_all_quick_final/`

Scope:

- seven Linux releases: `413`, `415`, `420`, `500`, `504`, `507`, `508`;
- three budget fractions: `0.01`, `0.02`, `0.05`;
- 100 stochastic runs, 20 runs per deterministic family, 100 SRS seeds;
- target: `vmlinux`;
- posterior risk is computed relative to the measured TuxKConfig pool, not the complete Linux configuration universe.

Current headline (21 release-level scopes):

- Strategy posterior-risk distributions differ in `21/21` scopes.
- SRS is best empirical-cost-normalized in `0/21` scopes.
- SRS appears on the empirical cost/confidence Pareto frontier in `19/21` scopes.
- Cost normalization changes the top recommendation in `13/21` scopes.
- Cost normalization changes the confidence Pareto frontier in `21/21` scopes.
- SRS has lower posterior risk than random in `5/21` scopes.
- SRS empirical acquisition cost differs from random in `21/21` scopes.

Interpretation:

Linux is not a direct exhaustive-space replication. It is an external-validity measured-pool study. Within that scope, posterior risk is valid but pool-relative. At full statistical power SRS is never the cost-normalized winner, but it is frontier-competitive in 90% of scopes: on Linux, SRS buys real guarantee quality at a real cost premium, and the premium is what cost normalization exposes. The quick pass (fewer runs/seeds) had understated both effects.

### LCBench

Artifacts:

- `artifacts/fse_posterior_lcbench_no_oracles/fse_posterior_lcbench_report.md`
- `artifacts/fse_posterior_lcbench_no_oracles/fse_posterior_lcbench_conclusion.md`
- `artifacts/fse_posterior_lcbench_no_oracles/posterior_lcbench_dataset_summary.csv`
- per-dataset reports and figures under `artifacts/fse_posterior_lcbench_no_oracles/lcbench_*`

Scope:

- 35 OpenML datasets;
- 2,000 measured configurations per dataset;
- target: `final_val_accuracy`;
- cost: `time_total`;
- budget levels: `n8`, `n16`, `n20`, `n32`, `n40`, `n64`;
- no diagnostic cheap/expensive oracles in the main run;
- generated SRS with 30 seeds per dataset/level.

Current headline:

- Strategy posterior-risk distributions differ in `155/210` dataset-budget scopes.
- SRS is best empirical-cost-normalized in `0/210` scopes.
- SRS appears on the empirical cost/confidence Pareto frontier in `20/210` scopes.
- Cost normalization changes the top recommendation in `119/210` scopes.
- Cost normalization changes the confidence Pareto frontier in `207/210` scopes.
- SRS has lower posterior risk than random in `0/210` scopes.
- SRS empirical acquisition cost differs from random in `12/210` scopes.

Interpretation:

LCBench should be framed as `EXTERNAL-VALIDITY-LCBENCH`, not as configurable-software replication. It does not refute the FSE posterior-risk framework. It does challenge any broad reading that SRS is generally the best recommendation beyond the original domain and cost model.

## Current Answers To The Revisited RQs

### RQ1: Do posterior-risk distributions distinguish sampling strategies?

Yes, generally.

- FSE artifact: strategy differences are visible across the seven systems.
- x264: differences in `34/34` target contexts.
- Linux: differences in `11/14` measured-pool scopes.
- LCBench: differences in `155/210` scopes.

Take-away:

Posterior risk is a useful outcome. It is sensitive enough to separate strategies across domains.

### RQ2: Do guarantees improve with sample size?

Mostly yes where budget scaling was evaluated.

x264 shows the cleanest result: for SRS, posterior risk is non-increasing in `34/34` contexts and integrated posterior confidence is non-decreasing in `34/34` contexts.

Linux also shows monotonic SRS posterior-risk improvement in the quick pass, but the cost-normalized winner still varies.

Take-away:

More samples generally improve posterior guarantees, but this does not imply that sample size is a calibrated cost model.

### RQ3: Is SRS still the best recommendation?

Sometimes, not universally.

- FSE artifact: SRS best empirical-cost-normalized in `3/7`.
- x264: SRS best in `26/34`.
- Linux: SRS best in `3/14`.
- LCBench: SRS best in `0/210`.

Take-away:

SRS remains a serious candidate, especially in the original FSE-style configurable-system setting and x264. It should not be recommended universally without a cost-aware check.

### RQ4: Does empirical acquisition cost change the decision frontier?

Yes, strongly.

- FSE artifact: frontier changes in `6/7`.
- x264: frontier changes in `30/34`.
- Linux: frontier changes in `14/14`.
- LCBench: frontier changes in `207/210`.

Take-away:

This is one of the strongest current findings. Even when the top scalar winner does not change, the Pareto set of defensible cost/guarantee choices often changes.

### RQ5: Is sample size a good proxy for posterior-guarantee acquisition cost?

Only coarsely.

Sample size is useful as a design variable, but it hides strategy-specific and dataset-specific acquisition cost. A fixed number of sampled configurations can correspond to substantially different empirical effort.

Take-away:

The FSE-style protocol becomes more actionable when posterior risk/confidence are plotted and ranked against measured acquisition cost, not only against sample count.

## Important Caveats And Realignment Needs

### Direct Replication Versus External Validity

The original FSE artifact systems are the closest direct replication.

x264 is a configurable-system external replication.

Linux and LCBench are measured-pool studies:

- Linux: measured TuxKConfig pools, not exhaustive Linux configuration spaces.
- LCBench: hyperparameter optimization pools, not software-product-line configuration spaces.

For these two, posterior risk should be phrased as reference-relative or pool-relative posterior risk.

### SRS Implementation Provenance

Audited 2026-07-02 against the official `SRS-sampling.ipynb`
(Zenodo 10.5281/zenodo.19682296); full verdict in
`artifacts/srs_audit_note.md`, harness in `scripts/audit_srs_vs_artifact.py`:

- `cost_sampling/srs.py` is a faithful reimplementation: all protocol
  constants match (step 25, two-sided Welch p<0.05, max orientation,
  random fill, budget clamp), and posterior-risk distributions of the two
  implementations are statistically indistinguishable (Mann-Whitney p=0.95
  over 40 seeds on a synthetic system).
- Two documented deviations, both conservative for cost analysis: our
  sampler never returns duplicate configurations (the artifact's random
  fill can, and its shipped SRS t2 CSVs are indeed 1-5 configs short of the
  nominal size in 2-42% of runs per system), and RNG streams differ so
  samples are statistically rather than bitwise equivalent.
- The released artifact ships full sample traces for
  random/solverBased/divDistBased/twise/SRSSampling at t2 (100 runs per
  system), plus noisy/restricted diagnostic variants; the Phase 2 rerun
  uses the artifact's own SRS traces (exact reuse), while
  x264/ENERGY/WORKLOAD/Linux/LCBench use the audited code-native sampler.

### Metric Alignment

The current code follows the FSE artifact's `N + 1` prior-confidence exponent by default. The paper text may present the simplified `N` form.

Needed:

- Decide which convention to report.
- Run a sensitivity check for `prior-offset=0` versus `prior-offset=1`.
- Make all reports explicit about the convention.

### Cost Alignment

Different corpora expose different cost notions:

- FSE artifact systems: empirical performance values are also used as the acquisition-cost axis in the current revisit.
- x264: target can be `time` or `size`, while acquisition cost is currently `time`.
- Linux: target is `vmlinux`; cost-column choices require careful documentation.
- LCBench: target is validation accuracy; acquisition cost is `time_total`.

Needed:

- Freeze a single cost protocol per dataset.
- Add a sensitivity table where multiple plausible cost definitions exist.

### Statistical Testing Alignment

Current scripts produce hypothesis summaries and tests, including nonparametric comparisons.

Multiple-comparison policy (decided 2026-07-06): Benjamini-Hochberg at FDR
0.05 within each (corpus, hypothesis) family, applied to the p-value-based
hypotheses (FSE1 Kruskal-Wallis, FSE5/FSE6 Mann-Whitney); FSE2/3/4 are
decision rules without significance tests. Sensitivity
(`scripts/mcc_sensitivity.py`,
`artifacts/fse_posterior_synthesis/multiple_comparison_sensitivity.md`):
FSE1 survives essentially intact in every corpus (FSE artifact 7/7, x264
102/102, ENERGY 212/212, WORKLOAD 341/341, Linux 21/21, LCBench 154 ->
144), and the losses concentrate in the secondary SRS-vs-random effects
where they were already weak (ENERGY FSE5 52 -> 42, WORKLOAD FSE5 84 ->
70, Linux FSE5 5 -> 1, LCBench FSE6 10 -> 1). Headline claims are
FDR-robust; corrected counts are the ones to quote for FSE5/FSE6.

Still open:

- Treat repeated samples as repeated stochastic draws, not independent systems.
- Add corpus-level blocked tests where appropriate, especially for x264, Linux, and LCBench.

## Suggested Paper Framing

The clean framing is:

> We replicate and extend FSE 2026's posterior-risk framework under measured acquisition cost.

Possible research questions:

1. Can FSE-style posterior risk and posterior confidence be reproduced on the original artifact systems?
2. Do these posterior guarantees generalize to our six dataset families?
3. Does SRS remain the recommended strategy once guarantees are normalized by empirical acquisition cost?
4. Does replacing sample size by measured cost change the top recommendation or Pareto-efficient strategy set?
5. Under which dataset/cost conditions is sample size a safe or unsafe proxy for posterior-bound guarantees?

The expected contribution is not a simple contradiction of FSE 2026. It is a cost-aware refinement:

> Posterior risk is a useful guarantee metric, but the guarantee/cost tradeoff depends on empirical acquisition cost. SRS is often strong, but its recommendation is not universal.

## Next Steps / TODO

### Protocol Freeze — DONE (2026-07-03)

Frozen decisions are recorded in `artifacts/FSE2026_POSTERIOR_RUN_MANIFEST.md`:
six corpora (FSE artifact, x264, ENERGY, WORKLOAD, Linux pools, LCBench),
`--extreme max`, prior `N+1` (with an `N` sensitivity run showing identical
headline decisions), no-oracle headline runs, per-corpus target/cost columns
and budget grids as listed there.

### SRS Audit — DONE (2026-07-02)

See `artifacts/srs_audit_note.md` and `scripts/audit_srs_vs_artifact.py`
(smoke checks: exact size, fill, determinism, orientation; behavioral
equivalence vs the artifact notebook).

### Full Reruns — DONE (2026-07-06)

- FSE artifact final t2 rerun + prior-N sensitivity: match previous results
  exactly.
- x264 final (t1-t3, 100 runs, 100 SRS seeds): matches previous results.
- ENERGY final: 14 systems, 220 scopes. WORKLOAD final: 93 contexts,
  359 scopes.
- LCBench no-oracle final: matches previous results within seed noise.
- Linux full protocol (levels 1/2/5%, 100 stochastic runs, 100 SRS seeds):
  completed 2026-07-06 via the resumable per-release sweep
  (`scripts/run_linux_full_parts.sh` + `scripts/merge_linux_full_parts.py`,
  five OS-kill/resume cycles on a memory-starved machine); results in
  `artifacts/fse_posterior_linux_all_full/`, per-release parts in
  `artifacts/fse_posterior_linux_full_parts/`.

### Hypothesis Testing

- Define a small hypothesis set, for example:
  - H1: posterior-risk distributions differ among strategies;
  - H2: SRS has lower posterior risk than random;
  - H3: SRS acquisition cost differs from random;
  - H4: empirical-cost normalization changes the top recommendation;
  - H5: empirical-cost normalization changes the Pareto frontier.
- Use nonparametric tests and effect sizes at context level.
- Add blocked corpus-level tests:
  - by system for FSE;
  - by input/target for x264;
  - by release for Linux;
  - by OpenML dataset for LCBench.
- Decide and document multiple-comparison correction.

### Figures — mostly DONE (2026-07-03)

`scripts/build_fse_posterior_synthesis.py` now emits, under
`artifacts/fse_posterior_synthesis/`:

- corpus-by-outcome heatmap (`fig_synthesis_heatmap.png`);
- SRS status matrix (`fig_srs_status_matrix.png`);
- recommendation-change and frontier-change rates
  (`fig_cost_normalization_impact.png`);
- guarantee/cost frontier examples: SRS best (x264), SRS Pareto-not-best
  (7z), SRS off-frontier (LCBench) (`fig_frontiers_representative.png`);
- sample-size versus empirical-cost calibration small-multiples
  (`fig_calibration_pct_n_vs_pct_cost.png`).

Still open: the conceptual bridge figure (FSE guarantee axis x empirical
cost axis) for the paper introduction.

### Writing

- Use the direct FSE artifact as the anchor replication.
- Present x264 as the main configurable-system external replication.
- Present Linux and LCBench as external-validity stress tests.
- Be explicit that Linux and LCBench posterior risk is pool-relative.
- Avoid claiming that LCBench refutes FSE. It refutes only a broad, domain-independent SRS recommendation.

### Reproducibility — largely DONE (2026-07-03)

`artifacts/FSE2026_POSTERIOR_RUN_MANIFEST.md` records per-corpus commands,
git commit, interpreter/library versions, data provenance (with the FSE
artifact `data.zip` sha256), frozen protocol decisions, and verification
against the roadmap sanity targets.

Still open: durable local homes for the two large temporary inputs
(LCBench JSON in `/private/tmp/lcbench/`, and re-extraction of the FSE
artifact data from Zenodo when Phase 2 needs rerunning), pending disk
space on this machine.

## Current Bottom Line

The work so far is promising and coherent.

The strongest defensible message is:

> We can reproduce the FSE posterior-risk framework and use it as a replacement outcome for our sample-size-versus-cost protocol. The posterior-risk metric generalizes, but the SRS recommendation is cost- and dataset-dependent. Therefore, sample size alone is not a sufficient basis for comparing strategies when the practical goal is posterior performance-bound guarantees per unit of empirical acquisition cost.

