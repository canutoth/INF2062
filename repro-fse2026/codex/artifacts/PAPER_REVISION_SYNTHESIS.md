# Paper revision synthesis — consequences of the new analyses

Date: 2026-06-28. What our analyses (flip vs KW vs Pareto; ridge vs RF vs CART;
per-family who-wins; MRE/fit; the Linux feature-truncation fix) mean for the paper:
which claims still hold, what to retract, what to add, and the high-level messages
for the abstract and conclusion. Companions: `learner_sensitivity_summary.md`,
`HANDOFF_RQ2_COST_SIGNIFICANCE.md`, `significance_decisions.md`.

---

## 0. One-paragraph TL;DR (for the abstract/conclusion)

Re-running the field's *own* best-sampler comparison (Kruskal–Wallis on prediction
error) under **measured acquisition cost** instead of **configuration count** changes
the set of statistically tied-best samplers in **43–55% of comparisons in every
configurable-systems family** — significantly, and **robustly across three learners
(ridge, random forest, CART)**. The measured-cost **Pareto-efficient choice-set**
differs from the count-cost one in **73–100% of scenarios**. The single-winner "flip"
is mostly within noise and is reported as a secondary lens. The cost lens
systematically **over-credits the strategies that select interaction-rich, expensive
configurations** (solver-based t-wise; diversified-distance; even active learning) and
**under-credits cheap/cost-aware sampling** (plain random; a cost-aware `pilotCost`
sampler that *wins* once cost is priced). The effect is **strongest on the largest,
hardest subject (Linux)**. Consequence: sampling-strategy studies that count
configurations can reach the wrong comparative conclusion; effort must be priced as
measured cost (and the learner must actually fit the data before any ranking is trusted).

---

## 1. Claims review — still right / must change / retract

### 1a. STILL CORRECT (and now stronger)
- **KW headline:** the tied-best sampler set changes 43–55% under cost in every
  configurable family, all KW-significant. ✅ Unchanged — and now shown **learner-robust**
  (RF 47–62%, CART 43–59%), which neutralizes the "you only saw this with one learner"
  objection.
- **Pareto choice-set differs 73–100%** robustly. ✅ Unchanged.
- **Flip is mostly noise** (538/1,666 nominal, but bootstrap shows near-ties). ✅ Keep
  demoted; it corroborates, does not carry.
- **Concrete reversals (ICSE19/ICPE20):** solver-based t-wise dethroned on x264 (best-in
  12→5); diversified-distance edge evaporates on ICSE19 (tied-best 5→1). ✅ Verified.
- **RQ1 (cost is heterogeneous; strategy bias is the mechanism).** ✅ Holds; the
  per-strategy calibration numbers (e.g. Linux diversity 1.2–1.5×) are confirmed.

### 1b. MUST CHANGE / UPDATE
- **Linux is NOT the weak "storage-bound exception."** The paper currently says the
  Linux choice-set "robustly differs on only 4/7 releases" and "cost tracks count
  closely" (`5-results.tex` ~l.161–166). **Under the corrected setup (full 9,645
  features + HGBT) the opposite is true:** KW top-group change **100%**, Pareto
  p_differ **1.0 on every release** (3/3 so far). Linux is the **strongest**, not the
  weakest, cost-effect family. **Rewrite this paragraph.** (Why: with a learner that
  actually fits, the feature-aware "smart" samplers become strongly cost-biased.)
- **"KW-significant in X% / the MRE numbers":** add that fit quality must be checked;
  some families/systems are inherently hard (lrzip ~49%, kanzi ~80% MRE) — that is data,
  not a bug, but the ranking is only trustworthy where the learner fits.
- **The running example (Fig 1):** reframed from "equal error, only cost differs"
  (ridge-specific) to **"cost-aware `pilotCost` is cheaper AND more accurate — strictly
  dominates"** (random forest, robust). Done in `1-introduction.tex`. Update any text
  that still says "errors are almost indistinguishable."

### 1c. RETRACT
- **"Active learning is the novel/best Linux sampler."** This was an artifact of a
  **feature-truncation bug** (the Linux loader kept only 512 of 9,645 options), which
  (i) made every learner fit at ~30% MRE — garbage — and (ii) made the feature-based
  samplers select configs in a crippled 492-dim space. **Corrected:** active learning
  (`uncertainty`) is the **worst deployable sampler** on Linux (4th of 5, every
  release); **`coverage`/`random`/`balanced` win**; `diversity` is broken. Remove any
  active-learning-champion / "first to apply active learning to Linux" claim. The
  corrected story is *better* for the thesis (simple, calibrated samplers win on the
  hardest system) and must replace it.
- **Any Linux number computed on the 492-feature / ridge setup** (old §10/§11 KW 49%,
  exclude-AL 60%, the active-learning cost-at-size). Recompute from the corrected run.

---

## 2. New insights to insist on (the value added this session)

1. **Learner-robustness is now a result, not a hope.** The cost-induced re-ranking
   holds across ridge, random forest, *and* CART (43–62% KW change; Pareto robust under
   all three) — and it holds **even where a learner fits less well** (e.g. energy RF
   22% MRE still gives 62% change). That is a *stronger* robustness statement than "use
   a good learner." Insist on it: it closes the most obvious reviewer attack.
2. **Who wins, and who is over-/under-credited (the systematic per-family result).** The
   single best sampler **flips under cost in 2 of 6 families** (workload random→
   `pilotCost`, lcbench random→`balanced`); **`random` is the count-era favourite the
   cost lens most deflates**; **the cost-aware `pilotCost` sampler gains under cost and
   *wins* workload.** Mechanism invariant: *accurate-but-pricey-per-config loses; cheap-
   per-cost gains.* This is the substantive "decision impact" — promote it to a table.
3. **Cost-aware acquisition pays off (empirically).** `pilotCost` is the only strategy
   that gains under cost in every generated family. Caveat honestly (it is partly
   circular — it is *designed* to be cheap, §construct validity), but the headline does
   not depend on it: it holds on the 3 families with **no** cost-aware sampler.
4. **Linux is the showcase, not the exception.** On the largest, hardest subject, with a
   learner that actually fits (~7% MRE): the cost effect is **maximal** (KW 100%, Pareto
   100%), the **simple/calibrated samplers win**, and the **"smart" feature-aware
   samplers (active learning, diversity) are both uncalibrated and worse** (active
   learning under-spends at 0.57×, diversity over-spends at 1.4×; random/balanced/
   coverage ≈ 1.0×). This is the strongest single exhibit in the paper.
5. **A methodological lesson worth a paragraph: check the fit before you rank.** A
   learner that does not fit (Linux at ~30% MRE under the truncated/linear setup) makes
   the sampler comparison meaningless. The right Linux setup needs the **full option
   space + gradient boosting**; random forest with default `max_features="sqrt"` and
   classic GBT both underperform HGBT there. This doubles as a reproducibility caution.
6. **Three lenses, clearly ranked.** KW top-group (primary; reuses the field's test,
   whole-strategy, significant, learner-robust) ≳ Pareto choice-set (the robust
   decision-level metric) > top-1 flip (secondary, mostly noise). Make this hierarchy
   explicit; it pre-empts "your flip is just a near-tie."

---

## 3. Abstract & conclusion — high-level messages + the numbers to use

**Thesis sentence:** *Sample size orders sampling effort but is not the cost axis;
once acquisition cost is measured, the comparative conclusions of sampling-strategy
studies change — significantly, robustly, and most of all on the hardest subjects.*

**Headline numbers to state (all verified):**
- KW tied-best set changes **43–55%** of comparisons (every configurable family), **all
  KW-significant**, and **43–62% across ridge/RF/CART** (learner-robust).
- Pareto-efficient choice-set differs robustly (bootstrap p≥.95) in **73–100%** of
  scenarios; **Linux 100%** under the corrected setup.
- Single-winner flip **538/1,666 (32%)** but mostly within noise — reported as secondary.
- On Linux: cost-effect **100%** (KW), the cheap/calibrated samplers (`coverage`,
  `random`, `balanced`) win, active learning is the **worst deployable** sampler.

**Impact — research (for the conclusion):**
- Sampling-strategy studies that report "best sampler at fixed $n$" can reach a different
  verdict once effort is priced as measured cost; the field's own Kruskal–Wallis verdicts
  move in ~half of comparisons. Effort must be reported as **measured acquisition cost**,
  not configuration count, and the **prediction model must demonstrably fit** before any
  ranking is trusted (the Linux cautionary tale).
- The effect is **not a learner artifact** (ridge/RF/CART agree) and **not a single-system
  artifact** (every family; strongest on Linux).

**Impact — practice (for the conclusion):**
- **Budget by measured cost and include a cost-aware sampler.** A simple pilot-cost
  strategy is cheaper and often more accurate, and *wins* once cost is priced; plain
  **random is a strong baseline that the count view under-rates**.
- **Do not assume "smart" samplers are best.** Interaction-rich (solver-based t-wise),
  diversity, and even active learning can be the *most* expensive and, on the hardest
  subject, the *least* accurate per unit cost.
- **Same sample size ≠ same cost:** at $n{=}16$ on lrzip, two strategies differ by
  $16.5\times$ in measured cost, and the cheap one is also more accurate.

---

## 4. Figures & tables — add / remove / rewrite

**ADD**
- **Figure 1 (reframed, RF strict-win)** — `lrzip_fig1_rf_strictwin.png`. ✅ Done.
- **LLVM Pareto choice-set figure** — `pareto_llvm_rf.png` (count certifies 3 efficient
  designs, measured cost reveals 10). ✅ Done (`fig:llvm-choiceset` in `5-results.tex`).
- **Systematic per-family table** — champion (count→cost), over-/under-credited sampler,
  for all six families. This is the decision-impact centerpiece (Finding 2 of the
  handoff). *Recommended to add.*
- **Learner-sensitivity row/table** — KW top-group change under ridge/RF/CART per family
  (one line per family); or a sentence + appendix table. *Recommended.*

**REMOVE**
- **Figure 2** (`lrzip_high_n_cost_only.png`) — folded into the reframed Figure 1. ✅ Done
  (refs repointed).
- **Figure 4** (exastencils target–cost asymmetry) — already cut; keep cut (atypical
  outlier).

**REWRITE (data ready, no new compute)**
- **§ Linux deep-dive (RQ-by-RQ):** replace the active-learning-champion narrative with
  the corrected one — `coverage`/`random`/`balanced` win, active learning worst, cost
  effect 100%, RQ1 calibration split (calibrated simple samplers vs uncalibrated smart
  ones). Linux becomes the headline exhibit.
- **§ Choice-set paragraph (`5-results.tex` ~l.161–166):** Linux is no longer the "4/7
  exception"; it robustly differs on every release (100%).
- **Any results table with per-family RQ2/RQ3/RQ4 entries:** update the Linux row to the
  corrected numbers; add a learner-sensitivity column if space allows.

---

## 5. One-line correctness ledger
| claim | status |
|---|---|
| KW 43–55% every family | ✅ correct, now learner-robust |
| Pareto 73–100% robust | ✅ correct |
| flip mostly noise | ✅ correct (secondary) |
| pilotCost / cost-aware gains | ✅ new, report cautiously |
| random over-credited by count | ✅ new |
| Linux = weak storage-bound exception (4/7) | ❌ REVERSED → strongest (100%) |
| active learning = Linux champion / novel | ❌ RETRACT → worst deployable |
| Linux numbers on 492-feat/ridge | ❌ recompute (corrected run) |
| Fig 1 "equal error, only cost differs" | ⚠️ reframed → strict dominance (RF) |

---

## 6. Framing — cost-aware sampling as an ENABLER, not only a threat (a strong opening)

A reframing worth foregrounding (possibly in the opening/motivation): the paper is not
only a *caution* ("count is an unsafe cost proxy") but an *enabler*. **Count-based
evaluation keeps cost-aware samplers off the radar** — it over-credits simple/cheap-looking
baselines and under-credits strategies whose value is in spending the budget well. Once
acquisition cost is measured, those strategies' qualities become visible and adoptable.
The evidence: a cost-aware sampler (`pilotCost`) gains under cost in every generated family
and *wins* workload; on the lrzip running example it is cheaper *and* more accurate than the
"smart" diversity sampler. So a possible opening thesis:

> *Measuring sampling cost does more than expose a validity threat — it lets the community
> see, fairly compare, and adopt cost-aware samplers that the count lens renders invisible,
> while preventing both the over-appreciation of basic samplers and the dismissal of
> cost-aware ones.*

Honest guardrail (keep): `pilotCost` is partly self-fulfilling (designed to be cheap), so
its win is reported as a demonstration, not as the load-bearing result — the cost effect
holds on the three families with no cost-aware sampler.

**OPEN DECISIONS — POSTPONED, do not resolve yet (flagged per discussion 2026-06-28):**
- **Naming.** `pilotCost` is one instance; the general concept is "cost-aware sampling."
  How to name it in the paper (keep `pilotCost`; introduce a general term such as
  "budget-aware sampling"; rename) deserves more reflection. **Decide later.**
- **Emphasis level.** How strongly to push the "enabler / cost-aware sampling is a
  contribution" angle vs keeping the threat-to-validity framing primary — also deserves
  reflection. It interacts with the contribution list and the abstract's center of gravity.
  **Decide later.**
