# FSE 2026 Posterior Guarantees Under Empirical Acquisition Cost

## Scope

This note summarizes the reproduction/replication experiment around the FSE
2026 posterior-risk framework, but from our cost-aware perspective.

The original FSE paper evaluates sampling strategies with a fixed sample-size
budget. Here, we keep the FSE posterior outcomes:

- posterior risk;
- posterior confidence;
- integrated confidence discrepancy.

But we reinterpret the decision question as:

> Does Statistical Recursive Search remain the best recommendation once its
> posterior guarantees are normalized by empirical acquisition cost rather than
> only by sample size?

The experiment uses the FSE artifact data for seven systems:

- `7z`
- `BerkeleyDBC`
- `Dune`
- `Hipacc`
- `JavaGC`
- `LLVM`
- `Polly`

and five representative strategies at the fixed `t2` budget:

- `random`
- `solverBased`
- `divDistBased`
- `twise`
- `SRSSampling`

The detailed results are in:

- `fse_posterior_systems_report.md`
- `posterior_system_summary.csv`
- `posterior_hypothesis_tests.csv`
- per-system reports and figures under each system directory.

## Main Conclusion

SRS remains a strong strategy, but it is not a universal best recommendation
once posterior guarantees are normalized by empirical acquisition cost.

Across the seven systems:

- SRS is the best empirical-cost-normalized recommendation in `3/7` systems.
- SRS appears on the empirical cost/confidence Pareto frontier in `6/7` systems.
- Cost normalization changes the top integrated-confidence recommendation in
  `2/7` systems.
- The empirical-cost confidence Pareto frontier differs from the count-cost
  frontier in `6/7` systems.
- SRS has lower posterior risk than random sampling in `6/7` systems, but its
  empirical acquisition cost also differs from random in `7/7` systems.

So, the right interpretation is not:

> SRS is always best.

It is:

> SRS is often a very good and Pareto-relevant strategy, but cost-aware
> posterior analysis can recommend another strategy depending on the system.

## High-Level Explanation

The FSE paper asks whether the worst performance observed in a sample is really
close to the true worst case. It introduces posterior risk and posterior
confidence to answer that question.

Our cost-aware reproduction asks a slightly different practical question:

> If two strategies measure the same number of configurations, did they really
> spend the same measurement budget?

The answer is no.

Some configurations are cheap to measure and others are expensive. A strategy
can look excellent under a sample-size budget because it finds strong bounds
with `N` configurations, but if those `N` configurations are expensive to
measure, the cost/guarantee tradeoff changes.

In lay terms: counting samples is like counting the number of errands, while
empirical acquisition cost is the time each errand actually takes. Ten errands
can take ten minutes or three hours. A sampling strategy should not be judged
only by how many errands it performs.

## RQ1: Empirical Cost Heterogeneity

**Question.** Do configurations and strategies differ in empirical cost at
fixed sample size?

**Answer.** Yes.

The FSE systems show substantial per-configuration cost heterogeneity. Cost CV
ranges from `0.072` on `LLVM` to `1.42` on `BerkeleyDBC`; the `p90/p10` ratio
reaches `47.9` on `BerkeleyDBC`.

Even when every strategy uses the same nominal `t2` sample size, strategies can
select systematically cheaper or costlier regions of the configuration space.
For example, the calibration ratio `%cost/%n` ranges from `0.186` to `3.112` on
`BerkeleyDBC`.

**Take-away.** Fixed sample size is not fixed empirical effort.

## RQ2: Sample Size As Cost Proxy

**Question.** Does sample size agree with the measured acquisition budget?

**Answer.** Only as a coarse approximation.

Because this FSE reproduction focuses on a fixed `t2` budget, RQ2 is mostly a
calibration question rather than a correlation question across many sample
sizes. Median `%cost/%n` is often near one, but the strategy-specific spread is
large on several systems:

- `BerkeleyDBC`: `0.186` to `3.112`
- `7z`: `0.628` to `1.716`
- `JavaGC`: `0.625` to `1.704`
- `Polly`: `0.719` to `1.016`

This means that a count budget can understate or overstate the actual empirical
measurement effort.

**Take-away.** Sample size is a useful design axis, but it is not a calibrated
cost model.

## RQ3: Recommendation Robustness

**Question.** Do strategy recommendations change when empirical acquisition
cost replaces sample-size cost?

**Answer.** Yes, in some systems.

The top integrated-confidence recommendation changes in `2/7` systems:

| System | Best by sample-size baseline | Best by empirical-cost baseline |
|---|---|---|
| `7z` | `SRSSampling_t2` | `twise_t2` |
| `BerkeleyDBC` | `SRSSampling_t2` | `random_t2` |

Across all seven systems, the best empirical-cost-normalized strategy is:

| Strategy-level pair | Systems |
|---|---:|
| `SRSSampling_t2` | `3/7` |
| `divDistBased_t2` | `2/7` |
| `twise_t2` | `1/7` |
| `random_t2` | `1/7` |

**Take-away.** SRS remains competitive, but empirical cost changes the
recommendation often enough that sample size alone is not a safe decision
criterion.

## RQ4: Pareto-Efficient Choices

**Question.** Does the set of Pareto-efficient strategies change under
empirical cost?

**Answer.** Strong yes.

The empirical-cost confidence Pareto frontier differs from the count-cost
frontier in `6/7` systems. Only `LLVM` has the same count-cost and
empirical-cost confidence front.

This is stronger than merely changing a scalar ranking. The Pareto frontier is
the shortlist of strategies that are not obviously dominated in the
cost/guarantee plane. If the frontier changes, the set of defensible choices
changes.

**Take-away.** Empirical acquisition cost changes the decision surface, not
just the numeric score.

## RQ5: Cross-System Sensitivity

**Question.** Does the validity of the cost-normalized conclusion depend on the
system?

**Answer.** Yes.

The best empirical-cost-normalized strategy differs by system:

| System | Best empirical-cost-normalized strategy |
|---|---|
| `7z` | `twise_t2` |
| `BerkeleyDBC` | `random_t2` |
| `Dune` | `SRSSampling_t2` |
| `Hipacc` | `divDistBased_t2` |
| `JavaGC` | `SRSSampling_t2` |
| `LLVM` | `divDistBased_t2` |
| `Polly` | `SRSSampling_t2` |

SRS is therefore not dominated or irrelevant; it is often excellent. But the
winner depends on the performance landscape and the cost distribution of the
system.

**Take-away.** Cost-aware posterior guarantees are system-sensitive. The FSE
framework is useful precisely because it exposes this sensitivity.

## Relationship To The FSE Paper

The FSE paper's main claim is that posterior risk and posterior confidence
provide actionable guarantees for sampling strategies, and that SRS often gives
stronger posterior guarantees than alternatives at the same sample-size budget.

Our reproduction supports the usefulness of the posterior-risk framework, but
adds an important qualification:

> A strategy that is best at fixed sample size is not necessarily best at fixed
> empirical acquisition cost.

This does not invalidate the FSE framework. It extends its practical use. The
same posterior-risk and posterior-confidence measures can be combined with an
empirical acquisition-cost axis to produce a more realistic
cost/guarantee analysis.

## Practical Recommendation

For practitioners:

- Use posterior risk/confidence instead of relying only on the observed
  sampled maximum or minimum.
- Do not compare sampling strategies only at equal sample size.
- Report empirical acquisition cost alongside sample size.
- Treat SRS as a strong default candidate, but verify whether it remains
  Pareto-efficient under the actual measurement-cost distribution of the
  target system.

For researchers:

- The FSE paper is a good replication target for the `REPLICATION-FSE26`
  family.
- Posterior risk/confidence can replace MRE for a bound-estimation family of
  experiments.
- The key extension is to normalize posterior guarantees by empirical
  acquisition cost.
- The important research question becomes not only "which strategy gives the
  best posterior guarantees at sample size N?", but "which strategy gives the
  best posterior guarantees per unit of empirical acquisition cost?"
