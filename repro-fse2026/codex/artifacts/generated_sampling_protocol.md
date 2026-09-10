# Generated-Sampling Protocol Notes

This note covers datasets that do not provide precomputed sample sets by
strategy, seed, or `t` level. They should not be mixed silently with the
precomputed ICPE/Kaltenecker protocol.

## Scope

Use this protocol for:

| Dataset | Reusable data | Sampling traces? | Protocol |
|---|---|---|---|
| x264 YouTube UGC | measured configurations and video labels, after schema verification | no ICPE-compatible traces | generated |
| Workload-impact ICSE 2023 | `sample.csv`, `measurements.csv`, feature models, run scripts/tasks | no strategy/seed/size traces found | generated |
| Green Configuration / TwinsOrFalseFriends | `data/<system>/measurements.csv` and `FeatureModel.xml` | no sample traces found | generated |

For Workload-impact H2, keep the system. Its measured property is throughput.
Predict raw throughput when throughput is the target. If throughput is used as
the cost axis, orient it first, for example with `cost = 1 / throughput`, so the
Pareto analysis keeps a lower-is-better cost convention.

## TwinsOrFalseFriends Inventory

Zenodo record: <https://zenodo.org/records/7544891>

The archive contains 14 systems with `performance` and `energy` columns:

| System | Rows | Unique configs | Extra structure |
|---|---:|---:|---|
| 7z | 68,640 | 68,640 | single revision |
| Apache | 13,440 | 640 | 21 revisions, also `cpu` and `fixed-energy` |
| HSQLDB | 864 | 864 | single revision |
| LLVM | 65,536 | 65,536 | single revision |
| MongoDB | 6,840 | 6,840 | single revision |
| PostgreSQL | 19,008 | 864 | 22 revisions |
| VP8 | 41,040 | 2,736 | 15 revisions |
| brotli | 2,160 | 180 | 12 revisions, function-level data |
| exastencils | 86,058 | 86,058 | single revision |
| jump3r | 4,296 | 4,296 | one workload column value |
| kanzi | 3,202 | 3,202 | one workload column value |
| lrzip | 5,184 | 5,184 | function-level data |
| nginx | 4,416 | 4,416 | single revision |
| x264 | 4,608 | 4,608 | function-level data |

This dataset is a strong cost-property expansion because it supports a 2x2
matrix: `performance` cost/target and `energy` cost/target. It is also useful
for the Simpson's-paradox threat because the original paper reports that a
global performance-energy relation can break on configuration subsets.

## Strategy Suite

Primary generated strategies:

1. Uniform random: 100 seeds per system/context/budget.
2. Feature-balanced random: balance option/value frequencies.
3. Cost-oblivious diversity: greedy maximin or k-center in normalized
   configuration space.
4. Greedy t-wise coverage: pairwise by default; triples where feasible.
5. Cost-aware pilot diversity: measure a small pilot, learn a simple cost
   predictor, then choose diverse low predicted-cost configurations.

Diagnostic oracles:

1. Cheap-first: select lowest true cost.
2. Expensive-first: select highest true cost.

The oracles are not deployable strategies; they bound the possible impact of
cost heterogeneity.

## Budget Grid

Let `N` be the measured configuration universe.

Use percentage budgets as the main cross-system axis:

`1%, 2%, 5%, 10%, 20%, 30%`

Add absolute anchors when they are meaningful:

`8, 16, 32, 64, 128, 256`

Implementation:

`n_grid(N) = sorted(unique(ceil(p*N) for p in P) union A)`

with `P={0.01,0.02,0.05,0.10,0.20,0.30}` and
`A={8,16,32,64,128,256}`, filtered to
`8 <= n <= min(0.30N, 256)`. For very small systems, retain `n=8` if possible
and report the limited test size.

For cross-system figures, plot `%n = n/N` rather than raw `n`.

## Reporting Rule

Do not aggregate across:

1. precomputed vs generated protocols;
2. cost properties;
3. prediction targets;
4. lower-is-better vs higher-is-better orientations.

For RQ1/RQ2, group by cost property. For RQ3/RQ4, facet by
`cost property x target property`.

For TwinsOrFalseFriends generated batches, the current post-processing scripts
are:

```bash
python3 scripts/run_twins_hypotheses.py --input-dir artifacts/twins_generated_quick
python3 scripts/summarize_twins_generated_batch.py --input-dir artifacts/twins_generated_quick
```

The first script writes formal H1--H4 verdicts. The second rewrites the batch
Markdown report with explicit RQ answers and scenario-faceted figures.
`plot_twins_explanatory_bias.py` writes mechanism figures. Keep the run-level
`fig_explain_cost_error_*.png` plots, but also generate aggregated alternatives:
`fig_explain_strategy_budget_path_*.png` has one median point per
strategy/budget, and `fig_explain_fixed_n8_*.png` fixes the budget for direct
same-`n` strategy comparisons.

For stronger representative Twins evidence, use:

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

Use `--exclude-oracles` for paper figures that compare actionable strategies
only. The generated files receive a `_deployable` suffix.
