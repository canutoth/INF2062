# Conclusion: FSE-Style Posterior Guarantees on Linux/TuxKConfig

## Applicability

Linux/TuxKConfig is applicable as an external-validity extension of the FSE 2026 posterior-risk study, with an important scope restriction: the available Linux data are large measured pools, not exhaustive full configuration spaces. The posterior risk and posterior confidence values therefore quantify risk relative to the measured TuxKConfig pool.

This is still useful for the paper's revisit: it tests whether the FSE-style recommendation changes when posterior guarantees are normalized by empirical acquisition cost on a substantially different family of configurable systems.

## Quick-Pass Evidence

The quick pass covers seven Linux releases: `413`, `415`, `420`, `500`, `504`, `507`, and `508`, using two budget fractions, `0.01` and `0.02`, with generated SRS samples.

Main observations:

- Strategy posterior-risk distributions differ in `11/14` release-level scopes.
- SRS is the best empirical-cost-normalized recommendation in `3/14` scopes.
- SRS appears on the empirical cost/confidence Pareto frontier in `8/14` scopes.
- Cost-normalization changes the top recommendation in `9/14` scopes.
- Cost-normalization changes the confidence Pareto frontier in `14/14` scopes.
- SRS has lower posterior risk than random in `1/14` scopes.
- SRS empirical acquisition cost differs from random in `5/14` scopes.

## Takeaway

For Linux measured pools, SRS does not remain the dominant recommendation once posterior guarantees are normalized by empirical acquisition cost. It is often a reasonable Pareto-front candidate, and its posterior risk improves monotonically with budget in all seven releases, but diversity sampling is more often the empirical-cost-normalized winner in this quick pass.

The high-level interpretation is: SRS can still find strong bounds, but Linux changes the cost story. If the goal is "best guarantee for a fixed number of samples," SRS may remain attractive. If the goal is "best guarantee for the actual acquisition cost spent," it is no longer safe to recommend SRS universally.

## Recommended Framing

Use Linux as `REPLICATION-LINUX-POOL` or `EXTERNAL-VALIDITY-LINUX`, not as a direct full-space replication of the FSE artifact. The direct FSE-style claim should be phrased as:

> On measured Linux/TuxKConfig pools, FSE-style posterior risk and confidence can be computed and compared across sampling strategies, but the guarantee is pool-relative rather than configuration-space-complete.

## Artifacts

- Aggregate report: `artifacts/fse_posterior_linux_all_quick/fse_posterior_linux_report.md`
- Release summary: `artifacts/fse_posterior_linux_all_quick/posterior_linux_release_summary.csv`
- Budget trends: `artifacts/fse_posterior_linux_all_quick/posterior_linux_budget_trends.csv`
- Per-release reports and figures: `artifacts/fse_posterior_linux_all_quick/linux*_vmlinux/`

