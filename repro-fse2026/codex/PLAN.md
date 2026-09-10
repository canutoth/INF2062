Below is a **self-contained research brief + experimental plan** that you can give to a co-author or coding agent. It assumes the new positioning we converged on: the paper does **not** claim that cost-aware sampling is new; it claims that prior work often **abstracts acquisition cost as sample size**, and that this abstraction deserves empirical validation.

---

# Research brief: empirical cost models for sampling-based performance prediction

## 1. Motivation

Performance prediction of configurable systems usually relies on measuring a subset of configurations, training a model, and generalizing to the remaining configuration space. Since measuring all configurations is often infeasible, sampling strategies are evaluated by how well they trade prediction accuracy against measurement effort.

Prior work has already recognized that sampling should be cost-aware. In particular, Sarkar et al. introduced a composite sampling cost that balances measurement effort and prediction error, and they compare progressive and projective sampling under this objective. Their cost model starts with training-measurement cost, testing-measurement cost, model-building cost, and prediction-error cost; it is then simplified to a count-based formula where training and testing effort are represented by (2n), assuming equal-sized train/test sets and a unit cost per measured configuration. 

The key assumption we want to examine is therefore not whether **cost matters**—that is already established—but whether **sample size is a valid proxy for empirical measurement cost**. In practice, configurations can have heterogeneous measurement times: some x264 configurations may take longer to encode, some compression configurations may run slower, and some workloads may amplify these differences. Thus, two sampling strategies selecting the same number of configurations may induce different measurement costs if they select different kinds of configurations. Your draft already makes this point explicitly: smaller samples do not necessarily translate proportionally into lower computational measurement time, and this may threaten conclusions drawn from size-based cost abstractions. 

The paper’s central research goal should be:

> **To empirically characterize when sample size is a valid proxy for measurement cost, when it is miscalibrated, and whether replacing count-based cost with empirical measurement time changes conclusions about sampling strategies.**

This framing is robust: if empirical cost differs substantially from (n), the paper shows a threat to prior conclusions; if empirical cost closely follows (n), the paper validates a common abstraction and identifies when it is safe.

---

# 2. Positioning with respect to related work

## What prior work already covers

Sarkar et al. already study **cost-efficient sampling**. They adapt progressive and projective sampling to configurable-system performance prediction, introduce a composite sampling cost, and evaluate cost efficiency across six systems. Their contribution is about dynamically determining an “optimal” sample size and comparing adaptive sampling strategies under a cost model. 

Other configurable-system studies evaluate sampling strategies mainly by prediction accuracy and sample size. The draft notes that systematic reviews report many evaluation metrics, including MRE and related accuracy metrics, while sample size is often used as the operational notion of measurement effort. 

The ICPE 2020-style direction in your draft already points toward the right gap: previous work often assumes a relation between sample size and computational measurement cost, but this relation may be questionable because sampling strategies may pick configurations that are more or less costly to measure. 

## What this paper should claim

The safe novelty statement is:

> Existing literature either optimizes sample-count-based effort or studies context/input sensitivity, but it does not systematically test whether sample size is a calibrated proxy for empirical acquisition time, nor whether strategy conclusions change when replacing count-based cost with measured training cost.

Even more precise:

> We revisit the measurement-effort term itself. Whereas prior cost models often represent acquisition effort by the number of measured configurations, we compute empirical training measurement cost from the configurations actually selected by each strategy.

## Important conceptual difference from ASE 2015

ASE 2015 includes both training and testing measurement effort in its cost model. For our study, the cost controlled by a sampling+learning strategy is the **training sample** it chooses to measure. The evaluation/test set belongs to the experimental protocol and should not be counted as part of the strategy’s acquisition cost.

So the proposed model is:

[
TrainCost(r, s, n) = \sum_{c \in S_{r,s,n}} measurementTime(c)
]

where (S_{r,s,n}) is the training set selected by strategy (s), in run (r), at training size (n).

The test/validation set is used only to compute MRE.

---

# 3. Core assumptions to make explicit

1. **Sampling controls training, not testing.**
   A sampling strategy selects configurations to measure for training. The validation/test set is fixed and used for evaluation only.

2. **Measurement cost can be approximated from existing benchmark data.**
   If a dataset contains per-configuration execution time, elapsed time, encoding time, or similar, the empirical cost of measuring a sample is the sum of those costs over the selected training configurations.

3. **Model-building time is secondary.**
   Following prior work, model-building time can be ignored or reported separately because the dominant cost is usually measurement. Sarkar et al. make a similar simplification for CART, arguing that model-building cost is computationally insignificant compared with other cost factors. 

4. **Negative results are meaningful.**
   If (n) is highly correlated and well calibrated with empirical cost, then size-based cost is empirically justified for that context. If not, size-based cost models may mislead.

5. **Cost validity is context-dependent.**
   The validity of (n) as a cost proxy may depend on system, workload/input, performance property, and sampling strategy.

---

# 4. Research questions

## RQ1 — Empirical cost heterogeneity

**RQ1. At fixed training sample size (n), how much does empirical measurement cost vary across configurations and sampling strategies?**

### Motivation

Prior work often assumes that all configurations have equal acquisition cost. Under that assumption, every strategy selecting (n) configurations has the same measurement effort. RQ1 tests this directly by holding (n) fixed and comparing the empirical cost of the selected configurations.

### Hypotheses

* **H1a:** Per-configuration measurement cost is heterogeneous within a system.
* **H1b:** At fixed (n), some sampling strategies induce higher or lower empirical training costs than others.
* **Null:** At fixed (n), strategy choice has no meaningful effect on empirical training cost.

### Variables

* Independent variables: system, sampling strategy (s), training size (n), run (r), workload/input, performance property.
* Dependent variable: (TrainCost(r,s,n)).
* Secondary variables: per-configuration measurement-time distribution, coefficient of variation, cost overhead vs. random.

### Analysis

For each system and (n):

* report median and IQR of (TrainCost) per strategy;
* compare strategies with Kruskal–Wallis and pairwise Mann–Whitney U tests;
* report effect sizes, e.g., Vargha–Delaney (\hat{A}_{12});
* report practical overhead relative to random:

[
Overhead(s,n)=\frac{median(TrainCost(s,n))}{median(TrainCost(Random,n))}
]

### Interpretation

* If strategies differ significantly at fixed (n), then “cost = sample size” hides strategy-induced cost bias.
* If strategies do not differ, this suggests that for this system/sample-size range, (n) dominates cost.

---

## RQ2 — Validity of sample size as a cost proxy

**RQ2. To what extent is training sample size (n) a valid proxy for empirical training measurement cost, in terms of correlation, calibration, and strategy-specific bias?**

### Motivation

Even if cost grows with (n), it may not grow proportionally. A strategy using 20% of configurations might consume 10%, 20%, or 40% of full measurement time. RQ2 tests whether (n) is not only rank-correlated with cost, but also calibrated.

### Hypotheses

* **H2a:** (n) is positively correlated with empirical training cost.
* **H2b:** The relationship is not always calibrated: (%TrainCost / %n \neq 1).
* **H2c:** Calibration may differ by system, strategy, input, and property.

### Metrics

Correlation:

[
\rho(n, TrainCost)
]

Calibration ratio:

[
Ratio(r,s,n)=
\frac{TrainCost(r,s,n) / FullCost}
{n / |C|}
]

where (FullCost) is the total measurement cost over all configurations and (|C|) is the number of valid configurations.

Strategy-specific bias:

[
Bias(s)=median(Ratio(s,n)) - 1
]

### Analysis

* Spearman correlation between (n) and (TrainCost).
* Linear/log-linear regression of (TrainCost) on (n).
* Median and IQR of (%TrainCost/%n).
* Ratio plots: (%n) on x-axis, (%TrainCost) on y-axis, with the (y=x) line.
* Per-strategy and per-system calibration summaries.

### Interpretation

* High correlation + ratio close to 1: size is a good proxy.
* High correlation + ratio far from 1: size ranks cost but miscalibrates budgets.
* Low/moderate correlation: size is unreliable as a cost proxy.
* Strategy-specific ratios: some strategies systematically select cheaper or costlier configurations.

---

## RQ3 — Robustness of conclusions to the cost model

**RQ3. Do strategy rankings under accuracy–cost tradeoffs change when empirical training cost replaces count-based cost?**

### Motivation

Even if (n) is correlated with cost, conclusions may change when strategies are ranked by accuracy plus empirical measurement time rather than accuracy plus sample size. This directly tests the scientific consequence of the cost abstraction.

### Hypotheses

* **H3a:** Rankings under count-based cost and empirical-cost models sometimes diverge.
* **H3b:** Divergence is stronger when per-configuration cost heterogeneity is high or when strategies select cost-biased regions of the configuration space.
* **Null:** Rankings remain stable across cost models.

### Cost models

Use two comparable objectives.

Count-based:

[
J^{size}_{\lambda}(s,n)=norm(MRE(s,n)) + \lambda \cdot norm(n)
]

Empirical-time-based:

[
J^{time}_{\lambda}(s,n)=norm(MRE(s,n)) + \lambda \cdot norm(TrainCost(s,n))
]

Use min–max normalization per system/context to avoid scale effects.

### (\lambda) sweep

Do not rely only on (\lambda=1). Use:

[
\lambda \in {0.1, 0.25, 0.5, 1, 2, 4, 10}
]

### Analysis

For each system/context:

* rank strategies or strategy-size pairs by (J^{size}*{\lambda}) and (J^{time}*{\lambda});
* compute top-1 agreement;
* compute top-k agreement;
* compute Kendall’s (\tau);
* compute mean rank difference;
* identify rank flips.

### Interpretation

* If rankings change, size-based conclusions may be sensitive to the cost abstraction.
* If rankings do not change, the size-based abstraction is robust in that context.

---

## RQ4 — Pareto-efficient sampling under empirical cost

**RQ4. Which ((strategy,n)) pairs are Pareto-efficient under empirical training cost, and how different is the empirical-cost Pareto frontier from the count-based frontier?**

### Motivation

Scalar objectives require choosing (\lambda). RQ4 avoids relying entirely on one tradeoff parameter by studying the two-dimensional MRE–cost plane.

A pair ((s,n)) is Pareto-efficient under empirical cost if there is no other pair ((s',n')) such that:

[
MRE(s',n') \leq MRE(s,n)
]

and

[
TrainCost(s',n') \leq TrainCost(s,n)
]

with at least one strict improvement.

### Hypotheses

* **H4a:** Some strategies/sample-size pairs are dominated once empirical cost is considered.
* **H4b:** The empirical-cost Pareto frontier differs from the count-based frontier in at least some systems/contexts.
* **Null:** Empirical and count-based Pareto frontiers are identical or nearly identical.

### Analysis

Compute two frontiers:

* count-based frontier: ((n, MRE));
* empirical-cost frontier: ((TrainCost, MRE)).

Report:

* number of Pareto-efficient pairs;
* frontier overlap;
* pairs that appear only on the empirical frontier;
* pairs that disappear when empirical cost is used;
* hypervolume difference if desired;
* “knee” points.

### Interpretation

RQ4 is decision-oriented. It tells practitioners which choices are not obviously wasteful, independently of a specific (\lambda).

---

## RQ5 — Context sensitivity

**RQ5. When do RQ1–RQ4 effects appear or disappear across systems, inputs, and non-functional properties?**

### Motivation

Context sensitivity itself is not novel, but the context sensitivity of **cost-model validity** is the relevant question. Your draft’s x264 design is ideal here: x264 is widely used, has 1,152 configurations, and the draft already considers 17 input videos and two properties: encoding time and output size. 

### Hypotheses

* **H5a:** The validity of (n) as a cost proxy depends on input/workload.
* **H5b:** The effect differs between predicting execution time and output size.
* **H5c:** Strategy rankings and Pareto frontiers are less stable under empirical cost than under count-based cost.

### Analysis

For each input/property:

* repeat RQ1–RQ4;
* compute Kendall’s (W) or average Kendall’s (\tau) for ranking stability;
* compute frontier overlap across inputs;
* summarize contexts where size-based cost is safe vs unsafe.

---

# 5. Experimental design

## 5.1 Units of analysis

The main experimental unit should be:

[
(system, input, property, strategy, n, run)
]

For each unit, compute:

* selected training configurations;
* empirical training cost;
* prediction MRE;
* count-based cost;
* composite rankings;
* Pareto status.

---

## 5.2 Datasets

### Tier 1 — Mandatory: x264 / ICPE 2020-style revisit

Revisit the x264 study because it is a canonical benchmark and your draft already frames it as the most used case study, with 17 videos and two measured properties: encoding time and encoded size. 

For x264:

* configurations: 1,152;
* options: 16, according to both ASE 2015 and your draft;
* inputs: 17 videos;
* properties:

  * encoding time;
  * output size.

Important design choice:

* When predicting **time**, the target is encoding time and the empirical cost can also be encoding time. This is realistic: measuring a training configuration costs the same phenomenon being predicted.
* When predicting **size**, the target is output size, but the empirical cost should still be encoding/elapsed time, because measuring output size requires running the encoder. This distinction is crucial and should be emphasized.

### Tier 2 — Broader replication systems

Use the systems already listed in your draft’s Table 2 if artifacts are available:

* 7Z — compression time;
* BDB-C — response time;
* DUNE — solving time;
* HIPAcc — solving time;
* JavaGC — time;
* LLVM — compilation time;
* LRZIP — compression time;
* POLLY — runtime;
* VP9 — encoding time;
* x264 — encoding time.

Your draft indicates these systems were selected by filtering literature artifacts that provide both a variability model and valid-configuration performance measurements, and that the experiment uses six sampling strategies from Kaltenecker et al. 

### Tier 3 — Optional robustness datasets

Add datasets only if they provide:

* complete configuration table;
* measured performance property;
* per-configuration measurement cost or a proxy for it;
* feature model or valid-configuration constraints;
* enough configurations for sampling.

Candidate domains:

* compression tools;
* video encoders;
* compilers;
* database systems;
* cloud configuration benchmarks if per-configuration acquisition time exists.

---

# 6. Sampling strategies

Use two protocols, because not all datasets expose the same sampling
artifacts:

* **Precomputed-sampling protocol** for Tier 1A and Tier 2A, where the
  artifacts already contain strategy/size samples. Here we reuse the native
  strategy labels and sample sizes.
* **Generated-sampling protocol** for Tier 1B, Tier 2B, Green
  Configuration/TwinsOrFalseFriends, and similar datasets. Here we generate a
  common set of strategies and budget levels from the measured configuration
  universe.

## A. Literature strategies

Replicate the six strategies from the ICPE 2020 draft / Kaltenecker-style setup:

1. Uniform random sampling.
2. Solver-based sampling.
3. Randomized solver-based sampling.
4. t-wise sampling.
5. Distance-based sampling.
6. Diversified distance-based sampling.

The draft already describes these families: random, solver-based, randomized solver-based, coverage/t-wise, distance-based, and diversified distance-based. 

## B. Simple additional baselines

Add simple baselines for interpretability:

1. **Uniform Random**
   Must always be included.

2. **Cost-oblivious diversity**
   k-center or maximin over feature space.

3. **Feature-frequency stratified**
   Ensures selected/deselected features are represented.

4. **Cheap-first oracle**
   Selects configurations with lowest known measurement cost. This is not deployable without prior measurements, but useful as a lower-bound reference.

5. **Expensive-first oracle**
   Selects highest-cost configurations. Useful as an upper-bound stress test.

6. **Cost-aware pilot strategy**
   Use a small pilot sample to estimate cost predictors, then sample configurations that balance diversity/informativeness and predicted measurement cost. This can be marked as exploratory or future-facing.

The oracle baselines are important for diagnosing the space: if cheap-first and expensive-first frontiers differ greatly, then there is meaningful cost heterogeneity even if the literature strategies do not exploit it.

## C. Recommended generated-sampling suite

For datasets without precomputed sampling traces, use a compact suite that is
implementable from CSV configuration tables alone and defensible across
systems:

1. **Uniform random**: primary baseline; 100 seeds per `(system, context, n)`.
2. **Feature-balanced random**: stratify or greedily balance option/value
   frequencies; keeps interpretability and avoids purely lucky random
   coverage.
3. **Cost-oblivious diversity**: greedy maximin/k-center in normalized
   configuration space; approximates distance-based sampling without needing
   the original strategy implementation.
4. **Greedy t-wise coverage**: greedily cover option-value pairs, then triples
   where feasible. If the measured universe is too sparse, use pairwise only
   and report coverage achieved.
5. **Cost-aware pilot diversity**: measure a small random pilot, learn a
   simple cost model from configuration features, then select diverse
   configurations among predicted low-cost regions. Count the pilot in
   `TrainCost`; otherwise the method gets a hidden free pass.

Use **cheap-first** and **expensive-first** as diagnostic oracles, not as
primary deployable strategies. They are useful to bound how much empirical
cost can vary at fixed `n`, but their use of the true cost labels must be
explicitly marked as oracle access.

This generated suite gives a clean comparison:

* random answers "what happens with no structure?";
* feature-balanced and t-wise answer "what happens with coverage?";
* diversity answers "what happens with geometry?";
* pilot-cost-aware answers "can empirical cost be reduced without oracle
  labels?";
* cheap/expensive oracles answer "how large is the possible cost effect?".

---

# 7. Sample sizes

Use a range of (n), not just t-wise sizes.

For generated-sampling datasets, define the budget grid from the measured
configuration universe size `N`:

* primary fraction grid: 1%, 2%, 5%, 10%, 20%, 30%;
* reliability floor: include absolute sizes 8, 16, 32 when the percentage
  grid would otherwise produce very small samples;
* optional large-system anchors: 64, 128, 256 when they fall inside the
  30% cap;
* small-system rule: keep at least 100 held-out configurations when possible;
  if `N < 200`, stop at 30% and report the limited test-set size.

Implementation rule:

`n_grid(N) = sorted(unique(ceil(p*N) for p in P) ∪ A)`, with
`P={0.01,0.02,0.05,0.10,0.20,0.30}` and
`A={8,16,32,64,128,256}`, then filter to `8 <= n <= min(0.30N, 256)` except
for very small systems where `n=8` is retained if it is below the cap.

For cross-system plots, use `%n = n/N` on the x-axis or facet by budget band.
Do not compare absolute `n=64` for a 180-configuration system and a
68,000-configuration system as if they were equivalent experimental effort.

For t-wise strategies:

* use natural t-wise sample sets for (t=1,2,3);
* record their actual (n);
* include them as strategy-size pairs.

For comparability:

* evaluate all strategies at common (n) values when possible;
* separately analyze native strategy sizes when strategies naturally produce fixed-size samples.
* never aggregate precomputed and generated protocols in one undifferentiated
  ranking table. Use separate panels or a protocol column.

---

# 8. Learning algorithms

Use one main learner and at least one robustness learner.

Main learner:

* Stepwise multiple linear regression if replicating Kaltenecker/Pereira-style studies; your draft says the ICPE 2020 design uses stepwise multiple linear regression and MRE. 

Robustness learners:

* CART, because ASE 2015 uses CART and argues it is fast and accurate for this domain. 
* Random forest or ExtraTrees as an optional non-linear learner.
* Ridge/Lasso linear regression for reproducibility and speed.

Primary results should use the literature-aligned learner; robustness appendix can test sensitivity to the learner.

---

# 9. Evaluation protocol

## Training/test separation

For each run:

1. Generate/select a training sample (S_{r,s,n}).
2. Train the model using only configuration options as features.
3. Evaluate on a fixed validation set (C_{test}) or on all non-training configurations if feasible.
4. Compute MRE.

Do **not** include validation/test measurement cost in (TrainCost). Validation measurements are part of the benchmark artifact and experimental protocol, not part of the sampling strategy’s acquisition cost.

## Features and forbidden columns

When predicting a property, all measured performance columns must be excluded from training features.

Example for x264 video datasets:

* If target is `time`, exclude `time`, `size`, and any other measured runtime/throughput columns.
* If target is `size`, exclude `size`, `usertime`, `systemtime`, `elapsedtime`, `cpu`, `frames`, `fps`, `kbs`, `etime`, etc.
* Use configuration options only.

## Number of runs

Use:

* 100 independent runs for stochastic strategies, matching the draft’s intended setup;
* deterministic strategies can be repeated only if they depend on random seeds or tie-breaking;
* report seed handling.

Your draft explicitly mentions 100 independent runs per strategy/system/sample-size/context to reduce randomness. 

---

# 10. Metrics

## Accuracy

Mean Relative Error:

[
MRE =
\frac{1}{|C|}
\sum_{c \in C}
\frac{|measured_c - predicted_c|}
{measured_c}
]

This is already the metric used in your draft. 

Also consider:

* MdRE;
* MAE or MAPE if useful;
* but keep MRE primary for comparability.

## Empirical training cost

[
TrainCost(r,s,n)=\sum_{c \in S_{r,s,n}} measurementTime(c)
]

For x264:

* if target is encoding time: measurementTime = encoding time;
* if target is output size: measurementTime = encoding elapsed/user time, not size.

## Count-based cost

[
SizeCost(r,s,n)=n
]

Use (n), not (n+m), because we focus on training acquisition cost.

## Normalized costs

[
TrainCostPct = \frac{TrainCost}{FullMeasurementCost}
]

[
SizePct = \frac{n}{|C|}
]

[
CalibrationRatio = \frac{TrainCostPct}{SizePct}
]

## Composite objective

[
J^{time}_{\lambda}=norm(MRE)+\lambda \cdot norm(TrainCost)
]

[
J^{size}_{\lambda}=norm(MRE)+\lambda \cdot norm(n)
]

## Pareto metrics

* Pareto membership;
* frontier size;
* frontier overlap between empirical and count-based;
* dominated pairs;
* hypervolume if desired.

---

# 11. Statistical analysis

## RQ1

* Kruskal–Wallis per system/context/(n).
* Pairwise Mann–Whitney U vs Random.
* Vargha–Delaney (\hat{A}_{12}).
* Practical thresholds:

  * <5% overhead: negligible;
  * 5–15%: small;
  * 15–30%: moderate;
  * > 30%: substantial.

## RQ2

* Spearman correlation (n) vs (TrainCost).
* Calibration ratio distribution.
* Regression slope/intercept of (TrainCostPct \sim SizePct).
* Strategy-specific calibration bias.

## RQ3

* Rank strategies or ((s,n)) pairs under (J^{size}) and (J^{time}).
* Compute Kendall’s (\tau), top-1 agreement, top-3 agreement, mean rank difference.
* Sweep (\lambda).

## RQ4

* Compute Pareto frontiers under count cost and empirical cost.
* Compare overlap.
* Identify pairs that change Pareto status.

## RQ5

* Repeat all analyses per input/property.
* Compute rank stability across contexts.
* Compute frontier stability across contexts.
* Report context clusters where size-based cost is safe or unsafe.

---

# 12. Expected result patterns and how to interpret them

## Pattern A: (n) is valid everywhere

* RQ1: no strategy-induced cost differences.
* RQ2: high correlation and ratio close to 1.
* RQ3: rankings unchanged.
* RQ4: frontiers identical.

Interpretation:

> The size-based abstraction is empirically justified for these systems and measurement conditions.

This is still a valid contribution because prior work assumed rather than tested it.

## Pattern B: (n) is correlated but miscalibrated

* RQ2: high (\rho), but ratio not close to 1.

Interpretation:

> (n) ranks cost approximately correctly but misestimates measurement budgets.

## Pattern C: strategy-induced cost bias

* RQ1: strategies differ at fixed (n).

Interpretation:

> Which configurations are selected matters, not only how many.

## Pattern D: rankings/frontiers change

* RQ3/RQ4: empirical cost changes best strategy or Pareto-efficient set.

Interpretation:

> Size-based conclusions can be sensitive to the cost abstraction.

## Pattern E: effects only for x264 inputs/properties

* RQ5: some videos/properties show effects, others do not.

Interpretation:

> Cost-model validity is context-dependent; x264 should not be treated as a single universal benchmark point.

---

# 13. Minimal implementation plan for a coding agent

## Inputs

For each dataset:

* configuration table;
* target property column(s);
* measurement-cost column;
* list of configuration-option columns;
* optional feature model / constraints;
* input/workload identifier if applicable.

## Pipeline

1. Load dataset.
2. Validate columns:

   * remove measured performance columns from features;
   * encode categorical options;
   * identify target and measurement cost.
3. Generate samples for each strategy, (n), run.
4. Compute (TrainCost).
5. Train model.
6. Evaluate MRE on fixed validation set.
7. Store row:

```text
system,input,property,strategy,n,run,
TrainCost,TrainCostPct,SizePct,MRE,
CalibrationRatio
```

8. Aggregate:

   * medians/IQRs;
   * statistical tests;
   * correlations;
   * rankings for lambda sweep;
   * Pareto fronts.

## Output artifacts

* `results_raw.csv`
* `results_aggregated.csv`
* `rq1_cost_heterogeneity.csv`
* `rq2_size_cost_calibration.csv`
* `rq3_rank_comparison.csv`
* `rq4_pareto_fronts.csv`
* `rq5_context_sensitivity.csv`
* plots:

  * cost distributions by strategy;
  * `%n` vs `%TrainCost`;
  * MRE vs TrainCost scatter;
  * ranking bump charts;
  * Pareto frontiers;
  * heatmaps across x264 inputs/properties.

---

# 14. Suggested paper structure

1. **Introduction**

   * Performance prediction needs sampling.
   * Cost-aware sampling exists.
   * But cost is often abstracted as sample size.
   * We empirically test that abstraction.

2. **Background**

   * Configurable systems.
   * Sampling strategies.
   * Cost-efficient sampling.
   * ASE 2015 and size-based acquisition cost.
   * ICPE 2020 / x264 motivation.

3. **Cost model**

   * Define training empirical cost.
   * Separate training acquisition cost from evaluation cost.
   * Define count-based baseline.
   * Define composite objectives and Pareto view.

4. **Research questions**

   * RQ1–RQ5.

5. **Experimental design**

   * Datasets.
   * Strategies.
   * Learners.
   * Metrics.
   * Statistical methods.

6. **Results**

   * One subsection per RQ.

7. **Discussion**

   * When is (n) safe?
   * When does empirical cost matter?
   * Practical diagnostic: pilot estimate of cost heterogeneity.

8. **Threats**

   * Existing datasets already measured all configurations.
   * Cost proxy depends on benchmark stability.
   * Model choice.
   * Sampling implementation quality.
   * Generalizability.

9. **Related work**

   * Cost-aware sampling.
   * Learning configuration spaces.
   * Input/workload sensitivity.
   * Multi-objective model evaluation.

10. **Conclusion**

* Empirical validation or refutation of size-based cost abstraction.

---

# 15. One-sentence contribution list

You can give the coding agent / co-author this as the target contribution:

1. We define **empirical training measurement cost** for sampling-based performance prediction.
2. We test whether **sample size is correlated and calibrated** with empirical cost.
3. We compare strategy rankings under **count-based** and **measured-property** cost models.
4. We identify **Pareto-efficient strategy/sample-size pairs** in the MRE–cost plane.
5. We study whether these conclusions are stable across **systems, x264 inputs, and non-functional properties**.

This is the cleanest, most defensible version of the paper.

---

# 16. Addendum (after extended dataset/literature scouting)

This addendum supersedes parts of §5.2 and §6 in light of the extended
research report (`deep-research-report-extended.md`). It does **not** change
the RQs — only the dataset selection, the cost-extraction recipes, the
generalization of `cost(c)` beyond wall-clock time, and a richer related-
work positioning that the paper now reflects.

## 16.0 Generalizing cost beyond measurement time

Throughout sections §1--§15 of this plan, `measurementTime(c)` is the
operational stand-in for per-configuration acquisition cost. The paper
adopts a **more general** formulation: `cost(c)` is a measured quantitative
property used as the budget axis of the sampling comparison. Wall-clock
measurement time is the canonical instance, but `cost(c)` can also be
instantiated with:

* wall-clock measurement time (default);
* cumulative output size, when storage is the binding constraint
  (e.g., an x264 transcoding service with a disk budget, or compiled
  binaries in a build farm);
* energy / integrated power, on battery-bound or power-constrained
  hardware;
* inverse throughput or another clearly oriented throughput-derived quantity,
  when throughput is the operational budget of interest;
* bandwidth or I/O volume, when measurement traffic is the bottleneck.

Mathematically nothing changes: `TrainCost`, the calibration ratio, and
the Pareto comparison are unchanged. The operational interpretation
changes. Read every "measurement time" below as "cost(c) instantiated as
wall-clock time"; replicating the empirical findings under storage- or
energy-bound `cost(c)` is a natural follow-up and is flagged as future
work in the discussion.

For reporting, distinguish the **raw property** from the **oriented cost
axis**. Time, size, memory, and energy are naturally lower-is-better and can
be summed directly. Throughput is higher-is-better, so a lower-is-better
budget axis should use a monotone transformation such as `1/throughput`
unless a figure explicitly uses a benefit axis. The prediction target can
remain raw throughput; only the cost axis needs orientation.

## 16.1 Revised dataset tiers

### Tier 1A — x264 / ICPE 2020 artifact (unchanged)

* 1,152 configurations × 17 videos × 2 properties (encoding time, output size).
* Source: ICPE 2020 artifact (`https://github.com/jualvespereira/ICPE2020`).
* Asymmetric case (predicting size while paying encoding time) is the
  cleanest illustration of `target ≠ cost` and remains the headline
  example for RQ5.

### Tier 1B — x264 on YouTube UGC corpus (new)

* 201 configurations × 1,397 user-generated videos.
* Source: Zenodo record `3928253`.
* Important: this configuration space does **not** match the ICPE 2020
  x264 configuration space. Therefore, do **not** reuse the ICPE 2020
  precomputed sample sets or compare strategy labels as if they selected from
  the same universe.
* Use: input-sensitivity stress test for RQ5 under a generated-sampling
  protocol. Expect the largest per-input variation in the calibration ratio.
  Inspect schema before use (the retrieved metadata did not expose all
  columns); confirm there is an elapsed-time column before counting it as
  `measurementTime(c, video)`.
* Reporting implication: present Tier 1B as "same subject system family,
  different configuration universe and generated sampling protocol", not as a
  direct continuation of the ICPE 2020 sampling-strategy comparison.

### Tier 2A — Kaltenecker corpus (unchanged)

* 9 systems: 7Z, BDB-C, DUNE, HIPAcc, JavaGC, LLVM, LRZIP, POLLY, VP9
  (plus x264).
* Use the measured property reported in the original artifact as
  `measurementTime(c)`.

### Tier 2B — Workload-impact ICSE 2023 package (new, primary expansion)

* 9 systems: jump3r, kanzi, dconvert, h2, batik, xz, lrzip, x264, z3.
* 25,258 measured configurations; 248,700 configuration-workload rows;
  6–13 workloads per system; documented protocol (median over 5 repetitions,
  except H2 which is throughput-based).
* Source: Zenodo `7658046`; companion repo
  `AI-4-SE/workload_coverage_companion`.
* Archive inspection (`artifact_excluding_raw_coverage.zip`) shows reusable
  measured data, but not Kaltenecker/ICPE-style strategy traces:
  * `dashboard/resources/<system>/sample.csv`: one measured configuration
    sample per system.
  * `dashboard/resources/<system>/measurements.csv`: performance label per
    configuration and workload.
  * `experiment_setup/<system>/*sample.csv`: sampled configurations used to
    generate scripts; these can be larger than the dashboard sample because
    some configurations did not execute successfully.
  * `experiment_setup/<system>/feature_model/` or `feature_models/`: DIMACS
    and XML feature models for reconstructing valid configuration constraints.
  * `experiment_setup/<system>/run_scripts/` or `tasks/`: command traces for
    measurement execution, not traces of which sampling strategy selected each
    configuration.
* Use:
  * Primary support for the workload-sensitivity dimension of RQ5.
  * Treat the measured configurations as the available universe and generate
    new sampling runs inside that universe. This is a different protocol from
    Tier 1A and Tier 2A, where strategy/size samples are already available.
  * Cost extraction: for runtime systems, when raw repetitions are not in the
    published files, approximate `acquisitionCost(c, w) ≈ 5 ×
    median_runtime(c, w)` and label results as approximated.
  * Keep H2, but mark it as throughput-based. If throughput is used as the
    target, predict the raw throughput value. If throughput is used as the
    cost axis, orient it first, e.g. `cost(c,w)=1/throughput(c,w)`, so the
    Pareto comparison still uses a lower-is-better cost convention.

### Tier 2C — Green Configuration / TwinsOrFalseFriends (new, cost-property expansion)

* 14 systems: 7z, Apache, HSQLDB, LLVM, MongoDB, PostgreSQL, VP8, brotli,
  exastencils, jump3r, kanzi, lrzip, nginx, x264.
* Source: Zenodo `7544891`, companion repository
  `AI-4-SE/TwinsOrFalseFriends`.
* Archive inspection shows `data/<system>/measurements.csv` for every system,
  with configuration columns plus `performance` and `energy`, and
  `data/<system>/FeatureModel.xml` for all 14 systems. Three systems
  (`brotli`, `lrzip`, `x264`) additionally expose function-level
  `measurements_ml.csv` and profiled-configuration files.
* There are no precomputed sample sets or sampling-strategy traces in the
  archive. Treat it like Tier 1B/2B: generate a common sampling-strategy and
  budget grid over the measured configuration universe.
* Use:
  * Primary support for energy as a cost and/or prediction target.
  * Natural 2x2 matrix where available: `performance` cost/target and
    `energy` cost/target. If `performance` is throughput for a system,
    orient the cost axis before computing `TrainCost`.
  * Strong discussion hook for Simpson's paradox: the original paper reports
    that global performance-energy correlation can break or reverse on
    subsets of configurations. This is directly aligned with avoiding
    aggregate cost-target conclusions.

### Tier 2D — Input-aware Performance Models (new, breadth expansion)

* 8 systems: gcc, ImageMagick, lingeling, nodeJS, poppler, SQLite, x264, xz.
* 1,941,075 measurements across multiple inputs and target properties.
* Source: GitHub `simula-vias/input-aware-performance-models`.
* Use:
  * Primary support for the property-sensitivity dimension of RQ5.
  * Cost extraction: `TrainCost(s, n, input) = sum over c in S(time(c, input))`.
    Always condition on input; never aggregate cost across inputs.
  * For non-time targets (binary size, bitrate, SAT conflicts), use the
    elapsed-time column as `measurementTime`, not the target.

### Tier 3 — Robustness add-ons (new)

* **Performance Evolution** (Kaltenecker et al.): 190 releases of 12
  systems. Use to test whether RQ1–RQ3 conclusions hold across software
  versions.

### Possibility, not priority (this paper)

* **LCBench**: 2,000 configurations × 35 datasets × 50 epochs, with
  per-epoch runtime logged. Genuinely interesting as a cross-domain
  validation of the calibration question — sample size vs.\ summed
  per-epoch runtime is the same shape of question as `n` vs.
  `TrainCost`. Deprioritized for this paper because:
  (i) it is not a configurable software system in the SPL sense and would
  dilute the focus; (ii) we already have enough configurable-systems
  breadth in Tier 1A, 1B, 2A, 2B, 2C, 2D and 3 to support the main claim.
  Mark as future work in §VI of the paper.
* **NAS-Bench-201**: 15,625 architectures × 3 image datasets, with
  latency and per-trial info. Same considerations as LCBench. Useful
  for ranking-stability analyses (RQ3) but secondary to the
  configurable-systems claim. Mark as future work.

### Datasets explicitly out of scope

* **JHipster performance-trade-offs**: dropped. The acquisition cost is
  dominated by orchestration overhead (build, idle, warm-up, monitoring),
  so the cost construct becomes the deployment workflow rather than the
  sampling strategy's choice of configurations. There is no clean
  per-configuration `cost(c)` signal to leverage. Generalizing
  `TrainCost` to full-stack systems is a separate paper.
* **CPM** (classic 6-system corpus): retrieved metadata confirms labels
  but not raw timing protocol; baseline only.
* **JHipster v3.6.1 build/test dataset**: not a performance-regression
  dataset in our sense.
* **Surrogate-based ML/HPO benchmarks** (JAHS-Bench-201, YAHPO Gym,
  surrogate sub-benchmarks of HPOBench): out of scope because runtimes
  are surrogate-emulated and would weaken any empirical cost claim.

## 16.2 Per-dataset cost-extraction recipes (overrides §5.2)

| Dataset | `measurementTime(c)` extraction | Approximation flag |
|---|---|---|
| ICPE 2020 x264 | published encoding/elapsed time per config × video | none (direct) |
| YouTube UGC x264 | elapsed time column per (config, video) — verify column exists; generated samples because the configuration space differs from ICPE 2020 | depends on schema |
| Kaltenecker (7Z, BDB-C, …) | published time-valued property | none |
| Workload-impact ICSE 2023 | runtime labels directly; throughput labels via an oriented transformation such as `1/throughput`; one measured configuration sample per system; generate samples within that measured universe | yes if raw repetitions are absent |
| Green Configuration / Twins | `performance` and `energy` columns from `data/<system>/measurements.csv`; generated samples over measured configurations; orient throughput-like performance before using it as a cost axis | no for published aggregate labels; repetition-level acquisition cost unconfirmed |
| Input-aware models | published elapsed-time column, conditioned on input | none if column present |
| Performance Evolution | published `measurements.csv` per release | repetition protocol unconfirmed |

When a dataset only exposes one aggregated runtime column and no
repetition count, treat it as a known underestimate of true acquisition
cost and report results so labelled. Never silently substitute one property
for another: if energy, size, memory, or throughput is the cost axis, declare
that scenario explicitly and orient the axis before computing Pareto fronts.

## 16.3 Measurement-protocol pitfalls (new section)

These belong in the threats-to-validity discussion and have been reflected
in §VII of the paper:

1. **Aggregated label ≠ acquisition effort.** A median over 5 runs costs
   ≥ 5× the median, plus warm-up. Only k×median when k is documented;
   otherwise call it an underestimate.
2. **Target ≠ cost.** Size, bitrate, throughput, energy are not
   acquisition-time quantities, but they can be legitimate cost properties
   if the paper explicitly defines the scenario. Do not mix them with
   elapsed-time acquisition cost in the same aggregate.
3. **Orientation matters.** Time, size, memory, and energy are naturally
   lower-is-better; throughput is higher-is-better. For a common
   lower-is-better cost axis, use an oriented transformation such as
   `1/throughput`, or label the figure as a benefit-axis analysis.
4. **Local vs.\ global proxies.** TwinsOrFalseFriends shows that a global
   energy↔runtime correlation can break on subsets. By analogy, a global
   `n` ↔ `TrainCost` correlation may still hide local mis-calibration —
   so RQ2 must look at distributions, not just aggregates.
5. **Stability matters too.** Some published datasets enforce a
   coefficient-of-variation threshold across repetitions
   (e.g., 5–10 measurements until CV < 10\%); ours should report stability
   per system/input as a quality signal.
6. **Full-stack acquisition is out of scope.** Datasets whose acquisition
   cost is dominated by orchestration overhead (build, warm-up, idle,
   monitoring) are excluded — see §16.1. For acquisition-time scenarios, the
   cost construct is the wall-clock cost of *running configuration `c` to
   obtain its label*, not the cost of the system's deployment workflow. For
   non-time scenarios, the cost construct is the explicitly named measured
   property, such as energy or output size.

## 16.4 Related-work positioning (revised)

The paper's positioning now operates on three axes rather than two:

1. **Configurable-systems performance-prediction lineage** (Sarkar 2015,
   Westermann 2012, Siegmund 2012/2015, Guo 2013, Kaltenecker 2019,
   Pereira 2020/SLR): operationalizes effort as count. This is what we
   test against.
2. **Cost-aware sampling and active learning in ML** (Settles–Craven–
   Friedland 2008 with *real annotation costs*; Weiss & Tian 2008; Last
   2009; Margineantu; Beygelzimer et al.\ COAL; Arora et al.; Herde et
   al.\ survey; Contardo et al.): has known for ~20 years that count is
   not cost when instances are heterogeneous. Our paper is the
   configurable-systems analogue. We do **not** claim novelty for the
   heterogeneous-cost framing in general; we claim novelty for the
   configurable-systems test of it.
3. **Cost-aware regression** (Torgo & Ribeiro): asymmetric prediction-
   error utility, not acquisition cost. Cite to head off the
   "cost-aware-regression already exists" reviewer reflex; explicitly
   distinguish.

The honest novelty statement is therefore:
> The configurable-systems performance-prediction literature has continued
> to use count-based proxies even though ML active learning has known for
> nearly two decades that this fails when instance costs are
> heterogeneous. We are the first to test, in configurable systems and
> across systems, inputs, and properties, whether sample size is a
> calibrated proxy for empirical measurement time and whether replacing
> counts with measured time changes scientific conclusions.

## 16.5 Bib entries to add

The paper currently flags the following with `\red{}`. They must be added
before submission:

* Settles, Craven, Friedland — *Active Learning with Real Annotation
  Costs* (NIPS workshop 2008).
* Weiss & Tian — *Maximizing Classifier Utility When There Are Data
  Acquisition and Modeling Costs* (DMKD 2008).
* Last — *Improving Data Mining Utility with Projective Sampling* (KDD
  2009).
* Margineantu — *Active Cost-Sensitive Learning*.
* Beygelzimer, Langford, Lifschitz, Sloan, Zhang — *COAL*.
* Torgo & Ribeiro — *Utility-based Regression*.
* Arora, Nyberg, Rose — *Estimating Annotation Cost for Active Learning*.
* Herde et al.\ — survey on cost types in active learning.
* Contardo et al.\ — *Sequential Cost-Sensitive Feature Acquisition*.
* Lesoil et al.\ — *Input Sensitivity* (JSS 2023) and *Input-aware models*
  (JSS 2024).
* Mühlbauer et al.\ — *Analyzing the Impact of Workloads...* (ICSE 2023).
* Lesoil et al.\ — x264 YouTube UGC dataset (Zenodo 3928253).
* Kaltenecker et al.\ — *Performance Evolution* dataset.
* Weber et al.\ — *Twins or False Friends?* (Green Configuration).

## 16.6 Notes — Pareto evaluation guidance

Keep track of the methodological role of:

* **Li, Chen, Yao — _How to Evaluate Solutions in Pareto-based Search-Based
  Software Engineering? A Critical Review and Methodological Guidance_ (TSE).**

Why it matters for this paper:

* It supports the claim that Pareto evaluation should match the **actual
  decision question**, not default to generic indicators.
* This strengthens our choice to use **top-1 flips, frontier membership
  change, Jaccard overlap, and front-exclusive pairs** when comparing
  count-based cost vs empirical measured cost.
* Our question is **choice-set stability under two cost models on the same
  finite candidate pool**, not optimizer quality on an unknown Pareto front.

Implications for the draft:

* In **related work**, use Li et al.\ to position our Pareto analysis as
  methodological alignment, not just another multi-objective citation.
* In **study design**, explicitly justify why we do **not** lead with
  hypervolume or knee-point language.
* In **discussion**, push the reporting recommendation that Pareto-style
  claims should expose the metric, the implied preference model, and the
  artifact fields needed to recompute the fronts.

Reviewer-defense note:

* If challenged on why we use Jaccard/frontier membership instead of generic
  Pareto indicators, the answer is: **because the paper studies whether the
  recommended non-dominated strategy--budget set changes when the cost axis
  changes**, and those measures answer that question directly.

## 16.7 Notes — Tao Chen configurable-systems line

Most relevant Chen papers for this draft fall into two groups.

Performance learning:

* Gong and Chen — *Does Configuration Encoding Matter in Learning Software
  Performance?* (MSR 2022).
* Gong and Chen — *Predicting Configuration Performance in Multiple
  Environments with Sequential Meta-learning* (FSE 2024).
* Gong and Chen — *Deep Configuration Performance Learning: A Systematic
  Survey and Taxonomy* (TOSEM survey track, 2024).
* Xiang, Gong, Chen — *Dually Hierarchical Drift Adaptation for Online
  Configuration Performance Learning* (ICSE 2026).

Configuration tuning / expensive-measurement line:

* Chen and Li — *Multi-Objectivizing Software Configuration Tuning* (FSE
  2021).
* Chen, Li — *MMO: Meta Multi-Objectivization for Software Configuration
  Tuning* (journal extension).
* Chen and Li — *Do Performance Aspirations Matter for Guiding Software
  Configuration Tuning?* (TOSEM 2023).
* Chen and Li — *Adapting Multi-objectivized Software Configuration Tuning*
  (FSE 2024).
* Ye, Chen, Li — *Distilled Lifelong Self-Adaptation for Configurable
  Systems* (ICSE 2025).
* Ye et al. — *Revealing Domain-Spatiality Patterns for Configuration
  Tuning* (TOSEM 2026).

How they interact with our argument:

* The **tuning** papers are the most exposed to our sample-size vs
  sample-cost critique because they explicitly reason in terms of expensive
  measurements, count-based budgets, numbers of evaluations, or speedups.
* The likely effect is **qualification rather than refutation**:
  optimization mechanisms may still be valid, but resource-efficiency claims
  remain count-budget claims unless empirical acquisition cost is validated.
* The **performance-learning** papers are more mixed:
  encoding-study cost is mainly **model training time**, which is orthogonal
  to our acquisition-cost question; SeMPL and DHDA are more exposed only when
  they interpret data efficiency or speedup through count-based sample growth.
* The survey paper is mainly useful as a **mapping source**: it can help
  document what the subfield usually reports, and whether true measured
  acquisition cost is almost never treated as the primary budget axis.

## 16.8 Notes — Deep Research prompt template

Use the following prompt when asking a deep-research agent to scan the
configurable-systems literature against our sample-size vs empirical-cost
argument.

Prompt:

> I am writing a research paper on **sampling-based performance prediction for
> configurable systems**. The core claim of the paper is:
> 
> * In this literature, **sample size** (number of measured configurations,
>   number of evaluations, budget in counts) is often treated as if it were a
>   valid proxy for **measured acquisition cost**.
> * Our results suggest a more precise conclusion: sample size is often useful
>   for **ordering effort**, but it is **not automatically a valid resource
>   budget** unless checked against empirical measured cost.
> * When count-based cost and measured acquisition cost diverge, some published
>   conclusions can change, including the top recommended
>   strategy--budget combination and the set of Pareto-efficient
>   strategy--budget combinations.
> 
> Our paper asks five questions:
> 
> 1. **RQ1 -- Cost heterogeneity.** Do configurations and sampling strategies
>    differ in measured acquisition cost at fixed sample size?
> 2. **RQ2 -- Budget calibration.** Does sample size agree with measured
>    training budget?
> 3. **RQ3 -- Top-combination stability.** Does the best accuracy--cost
>    strategy--budget combination change when measured cost replaces sample
>    size?
> 4. **RQ4 -- Pareto-front stability.** Do the non-dominated
>    accuracy--cost strategy--budget combinations change when measured cost
>    replaces sample size?
> 5. **RQ5 -- Context sensitivity.** Do the answers above depend on workload,
>    input, target property, cost dimension, release, or system family?
> 
> The broader scientific question is therefore:
> 
> * **Which prior papers in configurable systems make efficiency or
>   resource-budget claims that may be unstable if sample count is not a
>   calibrated proxy for true measured cost?**
> 
> Investigate papers on configurable systems from 2018--2026, with emphasis on
> performance prediction, sampling, configuration tuning, transfer/meta-learning,
> online adaptation, workload-aware modeling, and Tao Chen's publication line.
>
> Use only **primary sources**: publisher pages, official PDFs, authors'
> arXiv preprints, and artifact/code repositories explicitly linked by the
> paper. Use secondary sources only to locate the primary source.
>
> Treat the following as **anchor references already relevant to our draft**.
> Use them as starting points, and then expand outward to nearby work:
> 
> * Li, Chen, Yao. *How to Evaluate Solutions in Pareto-based Search-Based
>   Software Engineering? A Critical Review and Methodological Guidance.*
>   IEEE TSE 2020. DOI: 10.1109/TSE.2020.3036108.
> * Chen, Li. *Multi-Objectivizing Software Configuration Tuning (for a Single
>   Performance Concern).* ESEC/FSE 2021. DOI: 10.1145/3468264.3468555.
> * Gong, Chen. *Does Configuration Encoding Matter in Learning Software
>   Performance?* MSR 2022. DOI: 10.1145/3524842.3528431.
> * Chen, Li. *Do Performance Aspirations Matter for Guiding Software
>   Configuration Tuning?* TOSEM 2023. DOI: 10.1145/3571853.
> * Chen, Li. *Adapting Multi-objectivized Software Configuration Tuning.*
>   FSE 2024. DOI: 10.1145/3643751.
> * Gong, Chen. *Predicting Configuration Performance in Multiple Environments
>   with Sequential Meta-learning.* FSE 2024; if no stable publisher DOI is
>   available, use arXiv:2402.03183 plus venue metadata.
> * Gong, Chen. *Deep Configuration Performance Learning: A Systematic Survey
>   and Taxonomy.* TOSEM survey track 2024; if no stable publisher DOI is
>   available, use arXiv:2403.03322 plus venue metadata.
> * Ye, Chen, Li. *Distilled Lifelong Self-Adaptation for Configurable
>   Systems.* ICSE 2025; if no stable publisher DOI is available, use
>   arXiv:2501.00840 plus venue metadata.
> * Xiang, Gong, Chen. *Dually Hierarchical Drift Adaptation for Online
>   Configuration Performance Learning.* ICSE 2026. DOI:
>   10.1145/3744916.3764542.
> * Ye, Liang, Jiang, Li, Chen. *Revealing Domain-Spatiality Patterns for
>   Configuration Tuning: Domain Knowledge Meets Fitness Landscapes.* TOSEM
>   2026. DOI: 10.1145/3803859.
> * Also track the journal-extension line around:
>   *MMO: Meta Multi-Objectivization for Software Configuration Tuning*,
>   currently safely citable as arXiv:2112.07303 unless a final publisher DOI
>   is found.
>
> Our intended use of this review is not merely to collect related work. We
> want to classify each paper according to whether our paper would:
> 
> * **leave it essentially untouched**;
> * **qualify its efficiency/resource claims**;
> * **materially weaken a headline claim**; or
> * **suggest a stronger re-evaluation is needed**.
>
> For each paper, extract:
>
> 1. Full citation, venue, year, DOI or arXiv identifier, and URL.
> 2. Problem type: performance prediction / tuning / transfer learning / online
>    learning / self-adaptation / survey.
> 3. What resource is treated as scarce, optimized, or budgeted?
> 4. Whether the paper mentions **true measured cost**:
>    wall-clock benchmarking time, runtime, CPU/GPU time, money, energy,
>    measurement-hours, or adaptation latency.
> 5. Whether effort is instead proxied by **sample size**:
>    number of evaluations, number of measurements, training set size, search
>    budget, or fixed count budget.
> 6. If both appear, which one is used in the **main claims, tables, and
>    figures**?
> 7. Whether the paper discusses only training/model-building cost, only
>    acquisition/measurement cost, or both.
> 8. Whether the paper makes speedup/resource-efficiency claims and, if so,
>    what exact denominator/resource is being sped up.
> 9. Whether the paper's **main scientific contribution** is about:
>    optimization quality, prediction quality, budget efficiency, adaptation
>    latency, modeling cost, acquisition cost, or a combination.
> 10. Whether the paper would be threatened by our work if sample count and
>     empirical acquisition cost diverge.
> 11. Threat level: **none / low / medium / high**.
> 12. A short justification for the threat level.
> 13. Whether our paper would mostly:
>     confirm / qualify / partially weaken / strongly challenge the paper's
>     claims.
> 14. Exact supporting evidence: page/section/table/figure references, plus
>     short quotes for the cost definition, budget definition, and main
>     efficiency claim.
> 15. A one-paragraph analyst note explaining, in plain language, why this
>     paper is or is not exposed to the sample-size-vs-measured-cost issue.
>
> Use this threat rubric:
>
> * **None**: no efficiency claim depends on a cost proxy, or the paper already
>   measures the relevant resource directly.
> * **Low**: sample count is reported, but not central to the paper's headline
>   scientific claim.
> * **Medium**: count-based budgets are central, but the main conclusion is
>   still mostly about quality/accuracy rather than efficiency.
> * **High**: the paper's main efficiency, speedup, or resource-saving claims
>   materially depend on number of measurements/evaluations as the budget axis.
>
> Use this interpretation guidance when assigning threat:
>
> * Papers on **configuration tuning** are usually the most exposed when they
>   claim better efficiency under a count-based budget.
> * Papers on **performance prediction** are less exposed when their main claim
>   is accuracy, but they become exposed if they also claim "data efficiency",
>   "speedup", or reduced measurement effort using counts only.
> * Papers about **training/model-building cost** are adjacent but not direct
>   targets of our argument, unless they blur model-training cost with data
>   acquisition cost.
> * **Survey papers** should be mined both for references and for evidence of
>   what the field usually reports as its cost axis.
>
> Output:
>
> * A table with columns:
>   citation | venue/year | task | scarce resource | true measured cost? |
>   sample-size proxy? | training-cost vs acquisition-cost | threatened by our
>   work? | severity | confirm/qualify/challenge | evidence.
> * A narrative synthesis describing:
>   (a) common evaluation patterns in the literature;
>   (b) which subareas are most exposed to our critique;
>   (c) which papers are really about model-building cost rather than
>   acquisition cost;
>   (d) where our paper merely qualifies prior claims versus where it could
>   materially weaken them.
> * A final shortlist of papers we should cite in our draft, grouped into:
>   direct neighbors, methodological references, and survey/mapping papers.
> * A short final section called **Implications for our draft** that gives
>   concrete writing advice:
>   which papers should appear in related work, which belong in discussion,
>   which should be framed as complementary rather than contradictory, and which
>   require especially careful wording about "efficiency", "budget", or
>   "speedup".
>
> Special rules:
>
> * Distinguish measured **acquisition cost** from **model-training cost**.
> * Distinguish **optimization quality claims** from **efficiency-budget
>   claims**.
> * If the paper says "speedup", identify precisely what is faster.
> * Prefer exact page/figure/table references over paraphrase.
> * If a final DOI is unavailable, say so explicitly and fall back to
>   arXiv-plus-accepted-venue metadata.
> * Do not silently assume that "number of measurements" and "measurement cost"
>   are interchangeable.
> * When in doubt, explicitly state whether the paper's cost variable is
>   **count**, **time**, **energy**, **money**, or **mixed/unclear**.

## 16.9 Notes — largest-n can be cheaper under measured cost

This is a sharper version of the sample-size proxy failure than the fixed-`n`
examples.

The fixed-`n` argument says:

* if two strategies both sample `n` configurations, count cost treats them as
  equally expensive;
* measured acquisition cost can still differ strongly because they select
  different regions of the configuration space.

The largest-`n` inversion says something stronger:

* even a strategy--budget combination with the largest available `n` can be
  cheaper in measured acquisition cost than another strategy with fewer
  configurations;
* in some cases it is also more accurate, so the smaller sample is neither
  cheaper nor better once measured cost is charged.

Primary-artifact scan, excluding oracle strategies:

* Found `132` cases where a largest-`n` row is not the most expensive measured
  row and is more accurate than at least one smaller-`n` row that costs more.
* Best paper-friendly lrzip example:
  * family: `ENERGY`;
  * artifact: `artifacts/twins_generated_representative_100s/lrzip/strategy_summary.csv`;
  * context: `target=lrzip__cost_performance__target_performance`,
    `cost=lrzip::performance`;
  * larger sample: `pilotCost_n256`, `n=256`, MRE `41.11%`, measured cost
    `0.658%` of the full campaign;
  * smaller sample: `diversity_n128`, `n=128`, MRE `42.77%`, measured cost
    `3.297%` of the full campaign;
  * reading: `pilotCost_n256` uses twice as many configurations, but is
    `5.0x` cheaper and `1.65` MRE percentage points more accurate.
* Generated figure:
  `607058f5f5131dcd1dbd783d/pic/results/lrzip_high_n_cheaper_counterexample.png`
  from `scripts/plot_lrzip_high_n_counterexample.py`.

Suggested wording:

> Sample size often orders effort in aggregate, but it does not define the
> acquisition budget for a specific sampling strategy. In lrzip, a
> `pilotCost` sample with `n=256` configurations is both cheaper and more
> accurate than a `diversity` sample with `n=128`. Thus, the count proxy can
> not only miscalibrate budgets at fixed `n`; it can locally order two
> strategy--budget choices in the wrong direction.
