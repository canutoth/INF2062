# Figure & framing revision roadmap (2026-06-28)

Per the review: declutter the figures (interpretation belongs in captions/text), update
ridge-based panels to RF, split the over-loaded Pareto figure, and elevate the
"cost-aware sampling" framing.
Numbered items, each with: what changes, data/scripts, the new caption draft, and open
decisions. Recommended execution order at the end.

> **STATUS (2026-06-28): all four items DONE.** Item 1 — Fig 1 decluttered &
> re-rendered (`lrzip_fig1_rf_strictwin.png`); intro + results prose consistent
> (pilotCost 0.034% vs diversity 0.567%, 16.5×, also more accurate). Item 2 —
> combined Fig 2 rebuilt from the per-config cost quantiles in
> `learner_sensitivity_compact/energy/rf-log/<sys>/rq1_cost_heterogeneity.csv`
> (no `/tmp` zip needed): left = cost-spread boxes (tight→wide), right = RF
> count→measured-cost transitions; `5-results.tex` caption + paragraph updated
> to the RF transitions (7z/lrzip → pilotCost). Item 3 — LLVM Pareto split into
> 2 panels (`pareto_llvm_rf.png`), `fig:llvm-choiceset` added. Item 4 — naming /
> emphasis POSTPONED by design (see PAPER_REVISION_SYNTHESIS §6). Paper compiles
> clean: no undefined refs, no missing figures.

---

## ITEM 1 — Figure 1 (lrzip running example): declutter, richer reading

**File:** `scripts/plot_lrzip_fig1_rf.py` → `pic/results/lrzip_fig1_rf_strictwin.png`.
**Data (RF, cost=performance / target=energy, n=16) — all 5 deployable strategies:**

| strategy | measured cost | MRE |
|---|---|---|
| **pilotCost** | **0.034%** | **51.6%** |
| pairwise | 0.252% | 55.4% |
| diversity | 0.567% | 60.6% |
| random | 0.275% | 75.4% |
| balanced | 0.310% | 74.1% |

**Changes to the FIGURE (remove the editorializing; keep it a clean scatter):**
- ❌ Remove the **arrow** pilotCost↔diversity (it implies that pair is the only story).
- ❌ Remove the in-figure **title claim** "cost-aware sampling is cheaper AND more accurate"
  → neutral title, e.g. *"lrzip 0.631, n=16, predicting energy (random forest)"*.
- ❌ Remove the **"pilotCost dominates: 16.5× cheaper…" box**.
- ✅ Keep: 5 colored, labelled points in (measured cost [log], MRE); a light *"lower-left =
  better"* axis hint is fine. Maybe keep the pilotCost marker slightly larger.

**Interpretation moves to the CAPTION/text — and it is richer than pilotCost-vs-diversity:**
1. **pilotCost dominates everything** (cheapest 0.034%, lowest MRE 51.6%).
2. **pilotCost vs pairwise** (the pair you flagged): MRE nearly equal (51.6 vs 55.4) but
   pilotCost is ~**7× cheaper** (0.034 vs 0.252) — same accuracy, far less budget.
3. **pairwise dominates diversity**: pairwise is *both* more accurate (55.4 vs 60.6) *and*
   cheaper (0.252 vs 0.567).
4. **random/balanced are not that bad**: less accurate (74–75%) but **cheaper than
   diversity** (0.28–0.31% vs 0.567%) — count would rank them by error alone and miss this.
5. The pilotCost-vs-diversity **16.5× cost gap with lower error** is the sharpest single
   instance, but it is one of several cost-revealed orderings.

**DRAFT caption (Fig 1 right panel):**
> *Right: all five strategies use n=16 (so count prices them alike), yet measured runtime
> cost reorders them (random forest). Cost-aware pilotCost dominates — cheapest and most
> accurate; it matches pairwise's error at ~7× lower cost, and is 16.5× cheaper than
> diversity while more accurate. pairwise itself dominates diversity (cheaper and more
> accurate), and even random/balanced — weaker on error — are cheaper than diversity. Sample
> count sees none of this ordering.*

**Open decision:** neutral title wording; whether to keep a faint "better ↙" hint.

---

## ITEM 2 — Figure 2 (`fig_cost_distribution_regimes.png`): right panel → RF  *(heaviest)*

**What it is:** left panel = per-config cost spread (CV, p90/p10) — *learner-independent,
stays*. Right panel = count-cost winner → measured-cost winner **transitions** for
representative systems across the CV spectrum (ridge): currently PostgreSQL (unchanged),
x264 (`diversity→pairwise`), lrzip (`divDist→solver`), brotli (pilotCost budget change).

**RF recompute (equal weight, cost=perf/target=perf) — already differs:**
- PostgreSQL: `random@9 → random@9` (**unchanged** — still the tight/validated extreme ✅).
- brotli: `pilotCost@8 → balanced@9` (**changed**; under ridge it was a pilotCost budget shift).
- lrzip: `pilotCost@8 → pilotCost@64` (**budget change within pilotCost**).
- x264: needs the twins-energy x264 RF summary (the existing x264 RF is the *replication*
  matrix) — generate `run_twins_generated.py --system x264 --learner sk-rf-log` (≈3 min).

**Open issues / decisions:**
- The original figure mixes scenarios/strategy sets (e.g. lrzip `divDist→solver` are
  *replication* t-wise strategies, not twins) — so I must first pin down, per panel entry,
  **which system + scenario + strategy family + budget grid** the figure used. The generator
  script is not cleanly named; candidates incl. `run_system_report.py`. **Decision: locate
  the generator, or rebuild a small right-panel generator** from the RF strategy_summaries
  (cleaner and reproducible). Recommend rebuild.
- The **descriptive text** (`5-results.tex` ~l.27–33: "diversity→pairwise … divDist→solver …
  budget change inside pilotCost") **will change** under RF and must be rewritten to match
  the recomputed transitions.
- Pick the representative systems to span the CV axis (keep PostgreSQL as the unchanged
  extreme; choose 2–3 with progressively wider spread that *change* under RF).

**Effort:** locate/rebuild generator + generate x264 twins RF + recompute 3–4 transitions +
rewrite the figure text. The left panel is untouched.

---

## ITEM 3 — Figure 3 (LLVM Pareto): split into count panel + cost panel

**File:** `scripts/plot_pareto_count_vs_cost.py` → currently one over-loaded panel.
**Change:** two side-by-side panels, **shared y-axis (MRE)**:
- **LEFT — count view:** x = sample count n; mark the **count-cost Pareto frontier** (the 3
  efficient designs) + connect; grey = dominated. "lower-left = better."
- **RIGHT — measured-cost view:** x = measured cost (log); mark the **measured-cost Pareto
  frontier** (the 10 efficient designs) + connect.
- Color points by strategy; one shared legend. The visual contrast — a *sparse* count
  frontier (3) vs a *rich* cost frontier (10) — is the whole point.

**DRAFT caption (Fig 3):**
> *Measured cost exposes a trade-off frontier the count view collapses (LLVM, random forest).
> Left (sample count): only 3 strategy–budget designs are count-efficient. Right (measured
> cost): 10 are cost-efficient — count discards 7 designs that are cheaper-or-equally-accurate
> as "dominated," because it prices every same-size sample alike (Jaccard 0.30). The learner
> fits well (2.2% best MRE), so this is a genuine choice-set divergence, not a fitting
> artifact. Lower-left is better in both panels.*

**Open decision:** x-axis of the left panel — raw n, or n as % of |C| (for comparability)?
Recommend raw n with a log scale to match the right panel's shape.

---

## ITEM 4 — Naming & framing: "cost-aware sampling" as a contribution/opening

**Point (yours):** `pilotCost` is one instance; the general idea is **cost-aware sampling**.
A strong opening/motivation: **count-based evaluation kept cost-aware samplers off the radar
— over-appreciating basic samplers and under-appreciating cost-aware ones. Pricing
acquisition cost lets their qualities show.** This reframes the paper from purely "a threat
to validity" to *also* "an enabler": it lets the community recognize and adopt samplers that
pay off under cost.

**Actions:**
- Add a framing block to `PAPER_REVISION_SYNTHESIS.md` (opening/motivation angle + the
  enabler framing).
- **Naming:** in the paper, refer to it as **"cost-aware sampling (instantiated here as
  pilotCost)"** rather than just `pilotCost`; consider a cleaner generic name (e.g.
  "cost-pilot" / "budget-aware sampling"). *Decision: keep `pilotCost` as the concrete name
  but introduce the general term once and use it in high-level claims.*
- Tie to the evidence: pilotCost gains under cost in every generated family and *wins*
  workload; honestly note it is partly self-fulfilling (it is designed to be cheap), but the
  cost effect does not depend on it (holds on the 3 cost-blind families). The contribution is
  **"measured cost makes cost-aware sampling visible and adoptable."**

---

## Recommended execution order
1. **Item 1 (Fig 1 declutter + caption)** — data ready, low risk.
2. **Item 3 (Fig 3 split)** — data ready (LLVM), low risk.
3. **Item 4 (framing/naming)** — text only.
4. **Item 2 (Fig 2 RF)** — heaviest; do last. Sub-steps: locate/rebuild generator → generate
   x264 twins RF → recompute transitions → regenerate right panel → rewrite Fig 2 text.

## Open decisions to confirm before I execute
- **Fig 2:** rebuild a small right-panel generator (recommended) vs hunt for the original?
- **Fig 2:** which 3–4 representative systems (keep PostgreSQL unchanged + which RF-changing ones)?
- **Fig 1:** neutral title wording; keep a faint "better ↙" hint?
- **Naming:** keep `pilotCost` + introduce "cost-aware sampling" as the general term (my default)?
- **Fig 3 left panel:** raw n vs n-as-% on the x-axis (my default: raw n, log).
