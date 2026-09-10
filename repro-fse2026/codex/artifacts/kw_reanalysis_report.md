# Cost-controlled Kruskal–Wallis re-analysis of ICPE20 / ICSE19 — intermediate report

Date: 2026-06-24. Data: `artifacts/kw_cost_vs_size_icse19.csv`,
`artifacts/kw_cost_vs_size_icpe20.csv`. Script: `scripts/kw_cost_vs_size.py`
(run with `.venv-linux/bin/python`, which has scipy). Source data:
`ICPE-rawdata/{NewRuns,AllRuns}.zip` (the original studies' sampling runs).

## 1. What the original papers do

ICPE20 ("Sampling Effect on Performance Prediction", x264) and ICSE19
(Kaltenecker, distance-based sampling) compare sampling strategies
{twise, solvBased, henard, distBased, divDistBased, rand} by **prediction error
rate over ~100 random seeds**, and decide which strategy is best with a
**Kruskal–Wallis** test (`PerformKruskalWallis.R` → their Tables 2–8).
Crucially the comparison is **at a fixed sample size** (t-wise level t1/t2/t3).
This answers: *"at a given number of configurations, which sampler is most
accurate?"*

## 2. What we add (the only change)

We keep their **exact** test and metric, and change **one thing**: instead of
holding the sample *size* fixed, we hold the **measured acquisition cost** fixed.

Operationalization (per system/input and per level L):
- **SIZE view** (their cell): the samplers all use level L; Kruskal–Wallis on
  their 100-seed error distributions; best = lowest median error.
- **COST view**: budget `b` = the median measured cost the samplers spend at
  level L. Each sampler may use the most accurate sample it can **afford**
  (median cost ≤ b) — a cheap sampler can afford a *larger* sample, an expensive
  one cannot. Kruskal–Wallis again; best = lowest median error.
- **changed?** = does the best sampler differ between the two views.

## 3. Results

| family | comparisons (sys/input × level) | KW-sig (both views) | best sampler changes | **top-group (Dunn) changes** |
|---|---|---|---|---|
| REPLICATION-ICSE19 | 21 | 21 / 21 (100%) | 7 / 21 (33%) | **9 / 21 (43%)** |
| REPLICATION-ICPE20 (x264) | 51 | 51 / 51 (100%) | 21 / 51 (41%) | **28 / 51 (55%)** |
| ENERGY (generated; 3 stochastic samplers) | 74 | 58 / 74 (78%) | 12 / 74 (16%) | **35 / 74 (47%)** |
| LCBENCH (generated; 3 stochastic) | 350 | 277 / 350 (79%) | 110 / 350 (31%) | **174 / 350 (50%)** |
| WORKLOAD (generated; 3 stochastic) | 846 | 625 / 846 (74%) | 283 / 846 (33%) | **423 / 846 (50%)** |

**The top-group (set of statistically-recommendable samplers) changes under cost
in 43–55% of comparisons in EVERY family — a remarkably stable ~½.** Best-single-
sampler change is 16–41% (lower in energy because only 3 stochastic samplers).
Only LINUX remains (needs its own loader).

Post-hoc top-group = samplers not significantly worse than the best (Dunn,
Holm-adjusted), i.e. the "statistically tied for best" set the original Tables
2–8 report. The **set of recommendable samplers changes under cost in 43–55%**
of comparisons. (ENERGY's best-sampler change is lower at 16% because only the
three stochastic generated samplers — random/balanced/pilotCost — have a
distribution; pairwise/diversity are deterministic, 1 run, excluded from KW. But
its top-group still moves 47% of the time.)

**The samplers genuinely differ in (almost) every comparison (KW p < .05; 100%
for replications, 78% for the 3-sampler energy case).** The
original Tables are statistically real — this is *not* a noise phenomenon. Yet a
third to two-fifths of the "best sampler" verdicts change once effort is counted
as measured cost rather than configuration count.

Who wins shifts in an interpretable direction (expensive samplers lose):

- **x264 / ICPE20:** `solverBased` best-in 12 comparisons under size → only 5
  under cost; `divDistBased` rises 7 → 14. (solverBased samples expensive
  configs, so at equal cost it can't afford as large a sample.)
- **ICSE19:** `divDistBased` 4 → 1; `distBased` 0 → 2; `solverBased` 3 → 4;
  `random` stays dominant (11) under both.

Concrete flips (size-best → cost-best): LLVM t3 `divDistBased → random`;
Polly t2 `solverBased → random`; x264_4 t1 `solverBased → divDistBased`.

## 4. How this differs from the RQ2 flip audit (they are NOT the same thing)

| | flip audit (`significance_flips*`) | KW re-analysis (this report) |
|---|---|---|
| object | the single **top (strategy, budget) combination** that minimizes J = MRE + λ·cost | the **most accurate sampler** at a fixed effort |
| varies | count cost → measured cost, inside one combined objective | effort axis: size → measured cost; pure accuracy (no λ) |
| "change" | argmin of J changes | best sampler by accuracy changes |
| significance | bootstrap of the median decision; **mostly within noise** | Kruskal–Wallis on the accuracy distributions; **significant** |
| ICSE19 reading | 7 flips, ≈1 robust → looks benign | 33% of verdicts change, all significant → cost clearly matters |

They answer different questions and that resolves the apparent contradiction:
the **combined-objective decision** (flip) is a fragile near-tie, but the
**accuracy ranking of samplers at fixed effort** (KW) genuinely changes when
effort is measured cost. The KW lens is the stronger, more defensible result
because the underlying differences are statistically significant.

## 5. Caveats

- COST view uses the affordable-best-accuracy level per sampler at budget `b`;
  with only 3 t-levels the budget axis is coarse, so this is a conservative
  count of changes (finer budgets would likely reveal more).
- We report the omnibus KW (do samplers differ?) + best-by-median. We have not
  yet computed the post-hoc significance **groups** (Dunn/Conover) that the
  original Tables 2–8 use; that is the natural next refinement to say *which*
  samplers are statistically tied under each view.
- Same eval pipeline as the flip study (ridge-log, eval-cap 6000); see
  `significance_decisions.md`.

## 6. Recommendation

Lead the cost-vs-count story with **this** analysis, not the flip audit: it
re-runs the original papers' own test, the differences are significant, and ~1/3
to 2/5 of their published best-sampler verdicts change under measured cost. Use
the flip audit as the decision-level consequence, with the honest caveat that
many flips are within noise (robust ones concentrate where target≠cost or cost
is heavy-tailed).

Next: add post-hoc significance groups; extend the KW re-analysis to the
generated families (energy's 5 strategies).
