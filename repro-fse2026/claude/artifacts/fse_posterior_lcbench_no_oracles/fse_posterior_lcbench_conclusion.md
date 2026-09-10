# Conclusion: FSE-Style Posterior Guarantees on LCBench

## Applicability

LCBench is applicable as an external-validity dataset for the FSE posterior-risk framework, provided the claim is scoped as reference-relative posterior risk. Each OpenML dataset is one measured reference universe, and each hyperparameter configuration is a sampled object.

This is not a software-product-line/configurable-software replication. It is a cross-domain check of the same methodological question: do posterior-risk and posterior-confidence recommendations change when normalized by empirical acquisition cost rather than sample size?

## Main Run

The main recommendation run excludes diagnostic cheap/expensive oracles and covers all `35` LCBench datasets, with `2,000` configurations per dataset and budget levels `n8`, `n16`, `n20`, `n32`, `n40`, and `n64`.

Target: `final_val_accuracy`.

Cost: `time_total`, derived from the runtime learning curve.

Main observations:

- Strategy posterior-risk distributions differ in `155/210` dataset-budget scopes.
- SRS is the best empirical-cost-normalized recommendation in `0/210` scopes.
- SRS appears on the empirical cost/confidence Pareto frontier in `20/210` scopes.
- Cost-normalization changes the top recommendation in `119/210` scopes.
- Cost-normalization changes the confidence Pareto frontier in `207/210` scopes.
- SRS has lower posterior risk than random in `0/210` scopes.
- SRS empirical acquisition cost differs from random in `12/210` scopes.

## Takeaway

For LCBench, SRS is not supported as the best recommendation once posterior guarantees are normalized by empirical runtime cost. This result is stronger than the Linux measured-pool finding: in the no-oracle LCBench run, SRS is never the empirical-cost-normalized winner.

The high-level interpretation is that the FSE posterior-risk framework transfers cleanly to LCBench, but the FSE strategy recommendation does not. LCBench behaves as a useful external-validity stress test: the metric remains meaningful, while the preferred strategy becomes domain- and cost-dependent.

## Recommended Framing

Use LCBench as `EXTERNAL-VALIDITY-LCBENCH`, not as a direct FSE replication and not as another configurable-software system family. A precise claim is:

> On measured LCBench hyperparameter pools, FSE-style posterior risk and confidence can be computed per OpenML dataset, but empirical-cost normalization changes the strategy recommendation and does not support SRS as the dominant choice.

## Artifacts

- Main no-oracle report: `artifacts/fse_posterior_lcbench_no_oracles/fse_posterior_lcbench_report.md`
- Dataset summary: `artifacts/fse_posterior_lcbench_no_oracles/posterior_lcbench_dataset_summary.csv`
- Budget trends: `artifacts/fse_posterior_lcbench_no_oracles/posterior_lcbench_budget_trends.csv`
- Diagnostic oracle-inclusive report: `artifacts/fse_posterior_lcbench/fse_posterior_lcbench_report.md`
- Per-dataset reports and figures: `artifacts/fse_posterior_lcbench_no_oracles/lcbench_*/`

