# Cost-vs-count significance — consolidated results (all families, three metrics)

Date: 2026-06-25. Single source of truth tying the three RQ2 metrics together.
Framing (settled): **KW sampler comparison leads; Pareto choice-set is the robust
decision-level metric; top-1 flip is secondary (mostly noise).** See
`flip_vs_kw.md`, `kw_reanalysis_report.md`, `significance_decisions.md`.

## The three metrics

- **KW (sampler comparison)** — reuse ICSE19/ICPE20's Kruskal–Wallis test on
  error over ~100 seeds, comparing strategies at equal **measured cost** vs equal
  **size**. Report: best-sampler change, and Dunn **top-group** (tied-best set)
  change. *Significant; grounded in prior work; about the whole strategy set.*
- **Pareto choice-set** — does the measured-cost Pareto-efficient set of
  (strategy, budget) combos robustly differ from the count-cost set (bootstrap
  p_differ ≥ .95)? *The robust decision-level metric.*
- **Top-1 flip** — does the single best (strategy, budget) combo change, and does
  it survive a median/mean-decision bootstrap? *Mostly within noise.*

## Consolidated table

| family | KW best-change | **KW top-group change** | **Pareto robustly differs** (median Jaccard) | top-1 flip sig / total (median agg) |
|---|---|---|---|---|
| REPLICATION-ICSE19 | 33% | **43%** | **6/7** (0.38–0.8) | 1 / 8 |
| REPLICATION-ICPE20 (x264) | 41% | **55%** | **17/17** (0.33) | 9 / 60 |
| ENERGY | 16%* | **47%** | **45/56 = 80%** (0.65) | 16 / 138 |
| LCBENCH | 31% | **50%** | **31/35 = 89%** (0.62) | 1 / 66 |
| WORKLOAD | 33% | **50%** | **68/93 = 73%** (0.60) | 1 / 135 |
| LINUX | 26% | **49%** | **3–4/7** (0.67–0.83) | 0 / 10 |

Flip column = significant (p_reproduce≥.95) / total point-estimate flips at
**median** aggregation (recomputed 2026-06-25). The CSVs also hold **mean**-agg
rows (`agg` column); mean is the primary estimand (D3) and lifts the
flips-on-average counts. Numbers verified against the CSVs; see
`HANDOFF_RQ2_COST_SIGNIFICANCE.md` §2.

\* ENERGY best-change is low because only 3 stochastic generated samplers enter
KW (pairwise/diversity are deterministic, excluded); its top-group still moves 47%.

## Reading

1. **KW top-group changes in ~43–55% of comparisons in EVERY family** (ICSE19 43,
   x264 55, energy 47, workload 50, LCBench 50, **Linux 49**) — the set of
   statistically-recommendable samplers is *not* preserved under a cost lens,
   ~half the time, significantly. This is the headline, and it now holds across
   all six families including Linux.
2. **The Pareto choice-set robustly differs in ~73–100% of scenarios** across
   replications + energy + LCBench + workload — the measured-cost efficient
   frontier is almost always different from the count one, and it reproduces under
   bootstrap. This is the robust decision-level claim, and it holds even in ICSE19
   where the top-1 flip is noise (6/7). **The one documented exception is Linux
   (3–4/7, seed-sensitive)**: its target=cost=vmlinux storage size, so cost and
   count are tightly coupled and the *frontier* often does not move even though the
   *sampler ranking* (KW) still does — the mechanism's lower bound, not a failure.
   See the full Linux deep-dive in `HANDOFF_RQ2_COST_SIGNIFICANCE.md` §10.
3. **Top-1 flip is mostly noise** (0–16 significant per family at median agg); the
   significant ones concentrate in heavy-tailed (ENERGY/jump3r) or asymmetric
   (x264) settings — exactly where KW and Pareto move most. Demoted, reported
   honestly.

Mechanism (why cost changes the verdict though MRE is fixed): equal sample size
≠ equal measured cost (samplers differ in what they spend per config — RQ1), so
at equal budget cheap samplers buy more data and the comparison/frontier shifts.

## Data files
- KW: `kw_cost_vs_size_{icse19,icpe20,energy,workload,lcbench}.csv`, `significance_linux_kw.csv`
- Pareto: `significance_pareto_{energy,lcbench,workload}.csv`, `significance_linux_pareto.csv`
- Flip: `significance_flips_{energy,workload,lcbench,replication_icse19,replication_icpe20}.csv`, `significance_linux_flips.csv`
- Reproduce: `scripts/{kw_cost_vs_size,significance_flips*,significance_pareto_gen,significance_linux}.py`,
  shared core `scripts/sig_core.py`. Full retrofit guide: `HANDOFF_RQ2_COST_SIGNIFICANCE.md`.

## Status
COMPLETE — all six families × three metrics are computed (2026-06-25). The pattern
is stable: KW top-group changes 43–55% in every family; Pareto robustly differs
73–100% (Linux 3–4/7, the storage-bound exception, seed-sensitive — canonical
seed-0 re-run in flight); flip mostly noise.
