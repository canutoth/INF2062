# FSE 2026 Posterior Guarantees Under Empirical Acquisition Cost

Status as of 2026-07-02.

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

| Corpus | Scope | Key result | Current interpretation |
|---|---:|---|---|
| Original FSE artifact systems | 7 systems | SRS best empirical-cost-normalized in 3/7; SRS on empirical Pareto frontier in 6/7; cost normalization changes the top recommendation in 2/7; Pareto frontier changes in 6/7. | Direct FSE-style replication supports posterior guarantees and keeps SRS competitive, but not universally best under measured cost. |
| REPLICATION-ICPE/x264 | 34 target contexts | Strategy posterior-risk distributions differ in 34/34; SRS best cost-normalized in 26/34; SRS on empirical Pareto frontier in 29/34; cost normalization changes the top recommendation in 2/34 and frontier in 30/34. | Strong external replication for SRS, while still showing that cost-aware frontiers change. |
| Linux/TuxKConfig | 7 releases x 2 budget levels = 14 scopes | Strategy posterior-risk distributions differ in 11/14; SRS best cost-normalized in 3/14; SRS on empirical Pareto frontier in 8/14; cost normalization changes top recommendation in 9/14 and frontier in 14/14. | Pool-relative posterior risk is valid, but Linux weakens any universal SRS recommendation. |
| LCBench | 35 datasets x 6 budget levels = 210 scopes | Strategy posterior-risk distributions differ in 155/210; SRS best cost-normalized in 0/210; SRS on empirical Pareto frontier in 20/210; cost normalization changes top recommendation in 119/210 and frontier in 207/210. | Strong external-validity stress test: the posterior-risk metric transfers, but the SRS recommendation does not. |

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

### Linux/TuxKConfig

Artifacts:

- `artifacts/fse_posterior_linux_all_quick/fse_posterior_linux_report.md`
- `artifacts/fse_posterior_linux_all_quick/fse_posterior_linux_conclusion.md`
- `artifacts/fse_posterior_linux_all_quick/posterior_linux_release_summary.csv`
- per-release reports and figures under `artifacts/fse_posterior_linux_all_quick/linux*_vmlinux/`

Scope:

- seven Linux releases: `413`, `415`, `420`, `500`, `504`, `507`, `508`;
- two quick-pass budget fractions: `0.01`, `0.02`;
- generated SRS samples;
- target: `vmlinux`;
- posterior risk is computed relative to the measured TuxKConfig pool, not the complete Linux configuration universe.

Current headline:

- Strategy posterior-risk distributions differ in `11/14` release-level scopes.
- SRS is best empirical-cost-normalized in `3/14` scopes.
- SRS appears on the empirical cost/confidence Pareto frontier in `8/14` scopes.
- Cost normalization changes the top recommendation in `9/14` scopes.
- Cost normalization changes the confidence Pareto frontier in `14/14` scopes.
- SRS has lower posterior risk than random in `1/14` scopes.
- SRS empirical acquisition cost differs from random in `5/14` scopes.

Interpretation:

Linux is not a direct exhaustive-space replication. It is an external-validity measured-pool study. Within that scope, posterior risk is valid but pool-relative. SRS is not the dominant empirical-cost-normalized recommendation.

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

Current status:

- We have a code-native SRS implementation aligned with the FSE artifact notebook behavior.
- It includes the paper-footnote behavior of filling the sample with random configurations when recursion stops early.

Needed:

- Record the exact FSE artifact source used for SRS.
- Compare our implementation against the official notebook on small controlled examples.
- Confirm whether the released FSE artifact has all strategy traces or only enough data to regenerate some of them.

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

Needed:

- Finalize the exact hypothesis family.
- Decide correction policy for multiple comparisons.
- Report effect sizes consistently.
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

### Protocol Freeze

- Define the exact corpus list and labels:
  - `REPLICATION-FSE26`;
  - `REPLICATION-ICPE-x264`;
  - `EXTERNAL-VALIDITY-LINUX-POOL`;
  - `EXTERNAL-VALIDITY-LCBENCH`;
  - remaining families from the submitted paper if retained.
- Freeze target/cost columns for each corpus.
- Freeze budget levels and seed counts.
- Freeze whether the prior confidence convention is `N` or `N + 1`.

### SRS Audit

- Locate and archive the exact FSE artifact implementation of SRS.
- Compare our `cost_sampling/srs.py` against the artifact notebook.
- Add a small regression test for:
  - exact requested sample size;
  - random fill after early stop;
  - stable behavior under fixed seed;
  - max-bound and min-bound orientation.

### Full Reruns

- Rerun the original FSE artifact systems with the frozen protocol.
- Rerun x264 with fixed final seeds and all selected levels.
- Rerun Linux beyond the quick pass if time permits:
  - more levels;
  - more stochastic runs;
  - possibly all releases and selected target/cost variants.
- Rerun LCBench with frozen no-oracle strategy set and final cost convention.

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

### Figures

Keep per-context figures, but add paper-level synthesis figures:

- SRS win/Pareto matrix by corpus.
- Recommendation-change rate by corpus.
- Pareto-frontier change rate by corpus.
- Sample-size versus empirical-cost calibration plot.
- Guarantee/cost frontier examples:
  - one where SRS remains best;
  - one where SRS is Pareto but not best;
  - one where SRS is not competitive.
- A conceptual figure showing the bridge:
  - FSE posterior guarantee axis;
  - our empirical acquisition cost axis;
  - resulting cost/guarantee decision surface.

### Writing

- Use the direct FSE artifact as the anchor replication.
- Present x264 as the main configurable-system external replication.
- Present Linux and LCBench as external-validity stress tests.
- Be explicit that Linux and LCBench posterior risk is pool-relative.
- Avoid claiming that LCBench refutes FSE. It refutes only a broad, domain-independent SRS recommendation.

### Reproducibility

- Add a top-level command list or Makefile target for each corpus.
- Store run manifests with:
  - command;
  - git commit;
  - seed count;
  - source data path;
  - strategy set;
  - budget levels.
- Move any required non-repo temporary data, such as LCBench JSON, into a documented acquisition step or durable artifact location.

## Current Bottom Line

The work so far is promising and coherent.

The strongest defensible message is:

> We can reproduce the FSE posterior-risk framework and use it as a replacement outcome for our sample-size-versus-cost protocol. The posterior-risk metric generalizes, but the SRS recommendation is cost- and dataset-dependent. Therefore, sample size alone is not a sufficient basis for comparing strategies when the practical goal is posterior performance-bound guarantees per unit of empirical acquisition cost.

