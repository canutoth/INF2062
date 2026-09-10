# Flip vs Kruskal–Wallis: what each measures, why they differ, and which to lead with

Date: 2026-06-24. Captures the conceptual distinction worked out in discussion,
and the resulting framing decision. Companions: `kw_reanalysis_report.md`,
`significance_decisions.md`.

## TL;DR — the decision

**Lead the cost-vs-count story with the Kruskal–Wallis (KW) sampler comparison.**
It is the more defensible metric: it reuses the *existing* ICSE19/ICPE20
analysis, it is about the **whole set of sampling strategies**, and the
differences it detects are statistically significant. The **top-1 flip** (the
current RQ2 "538/1,666") may be *reported*, but it is **not the headline
metric** — it watches only the single winning combination and is mostly within
noise. The **Pareto-efficient set / top-group** is also important and should be
reported as the choice-set view (broader than top-1, more robust).

Priority: **KW top-group (primary) ≳ Pareto/choice-set (important) > top-1 flip (secondary)**.

## The two analyses, defined

### KW sampler comparison (the original studies' method, re-run under cost)
- **Question:** *given equal effort, which sampling strategy is most accurate?*
- ICSE19/ICPE20 answer it at fixed **sample size** (t-wise level) using a
  **Kruskal–Wallis** test on prediction-error distributions over ~100 seeds
  (`PerformKruskalWallis.R` → their Tables 2–8).
- We change **one thing**: hold **measured cost** fixed instead of size, and
  re-run the same test. Cost is the **constraint**, not a term added to error.
- Robust: the samplers genuinely differ (KW p<.05 in ~100% of replication
  comparisons). It is about **all** strategies, not one pick.

### Top-1 flip (the current RQ2 decision audit)
- **Question:** *which single `(strategy, budget)` plan is the best accuracy–cost
  buy, and does that one plan change when cost is priced as measured rather than
  counted?*
- Recommendation = `argmin_{strategy,size} J`, `J = minmax(MRE) + λ·minmax(cost)`.
  A flip = the argmin combo differs between count-cost and measured-cost.
- Cost is **inside** the objective. It watches **only the gold-medalist** — not
  the rest of the ranking, not whether #1 significantly beats #2, not ties.
- Fragile: top-1 vs top-2 are usually a near-tie in J, so a small change in cost
  pricing swaps them — a photo-finish recorded as a "flip." Bootstrap shows the
  top-1 flips are **mostly within noise**; the significant ones concentrate where
  cost is heavy-tailed or target≠cost.

### Pareto / choice-set (broader than top-1, the natural middle)
- The set of non-dominated `(strategy, budget)` combinations. The paper already
  reports a "Pareto front changed" count (≈209/238 ctx). The KW **top-group**
  (Dunn) is the accuracy-side analog: the set of strategies statistically tied
  for best. Auditing whether this **set** changes is more robust than the single
  winner and is the recommended decision-level measure.

## Why cost changes the verdict even though MRE is unchanged (the key mechanism)

For a fixed (strategy, size), MRE is a fixed number — re-pricing cost does not
touch it. The verdict changes because the **cost-controlled comparison does not
hold size fixed**: at an equal measured **budget**, a *cheap* sampler can afford
to measure **more** configurations (→ lower error) while an *expensive* sampler
affords **fewer** (→ higher error). So different MRE values enter the comparison
(each strategy at the largest sample it can *afford*), and the ranking moves.

Technically: equal sample size ≠ equal measured cost, because `C_s(t)` differs
across strategies at the same size *t* (strategy/cost bias — this is RQ1). The
size→cost map is strategy-dependent, so re-indexing by cost is a **non-uniform
permutation** of operating points, not an affine reparametrization → ranking not
preserved. `solverBased` (picks expensive configs) repeatedly loses to
`random`/`divDistBased` at equal budget. This is RQ1 propagating into the
sampler-comparison verdict.

## Dunn / top-group

KW is an **omnibus** test ("not all strategies are equal") and does not say
*which* differ. **Dunn's** test is the standard post-hoc: pairwise comparisons on
the shared KW ranks, `z_ij = (R̄_i−R̄_j)/sqrt(σ²(1/n_i+1/n_j))`, tie-corrected,
Holm-adjusted. **Top-group** = best (min median error) plus every strategy *not
significantly worse* than it — the "statistically tied for best" set the original
Tables report. `group_changed` = this set differs between size- and cost-control.

## What each shows (side by side)

| | top-1 flip | KW (+Dunn top-group) |
|---|---|---|
| object | single winning (strategy, budget) | whole set of strategies / the tied-best set |
| cost is… | inside the objective (a term) | a constraint (held fixed) |
| nature | deployment decision (best buy) | scientific accuracy comparison |
| statistics | fragile near-tie → mostly noise | distributional test → significant |
| grounded in prior work | no (our framing) | yes (ICSE19/ICPE20 Tables 2–8) |

ICSE19 makes the divergence concrete: top-1 flip → 7 changes, ~1 robust (looks
benign); KW → best changes 33%, **top-group changes 43%**, all KW-significant
(cost clearly matters). Different questions; both true; KW is the stronger.

## Results so far

| family | KW best-change | KW top-group change | top-1 flip (mean): on-avg / significant |
|---|---|---|---|
| ICSE19 | 33% | **43%** | 6/7 on-avg, 1 sig |
| ICPE20 x264 | 41% | **55%** | 39/86 on-avg, 9 sig |
| ENERGY (gen.) | 16% | **47%** | 100/152 on-avg, 17 sig |
| LCBENCH | — (pending KW) | — | 21/62 on-avg, 1 sig |
| WORKLOAD / LINUX | pending | pending | running / pending |

## Rationale for the decision (user, 2026-06-24)

KW is easier to defend: it is built on existing, peer-reviewed analyses
(ICSE19 + ICPE20), it speaks to the *whole* set of sampling strategies rather
than one winner, and its differences are significant. Top-1 flip is reportable
but not the main metric. The Pareto-efficient set is also important and belongs
in the decision-level reporting.
