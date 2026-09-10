# RQ2 / RQ3 — Cost-vs-count: key findings & paper impact

**Purpose:** the results note for updating the ICSE-2027 paper *"Sample Size Is Not Sampling
Cost"* — what we found, why it matters, and where it goes in the paper. **Revised 2026-06-27.**
Supporting detail: `learner_sensitivity_summary.md`, `kw_reanalysis_report.md`, `flip_vs_kw.md`,
`significance_decisions.md`.

---

## Executive summary — the take-away messages

1. **Cost re-ranks the "best sampler."** Re-running ICSE19/ICPE20's own Kruskal–Wallis test
   under measured cost instead of sample size changes the set of statistically tied-best
   samplers in **43–55% of comparisons in every family** — all KW-significant.
   *Impact:* the field's published best-sampler verdicts (their Tables) do not survive a cost lens.
2. **The change is learner-robust.** It holds under ridge, random forest, and CART (43–62%).
   *Impact:* neutralizes the "learning-algorithm sensitivity" reviewer threat.
3. **Who wins flips, and `random` is over-rated by count.** The single-best sampler flips under
   cost in 2 of 6 families; `random` is the count-era darling most deflated by cost; the
   **cost-aware sampler `pilotCost` gains and even wins.** (Systematic table below.)
   *Impact:* practitioners should **include a cost-aware sampler and budget by cost**.
3b. **Even the smartest sampler can fail.** On Linux (hardest system), simple **coverage /
   random / balanced win; active-learning and diversity lose**, and they are *uncalibrated*.
   *Impact:* reinforces "random is a strong baseline"; cautions against fancy samplers.
4. **The efficient choice-set changes too.** The measured-cost Pareto-efficient set robustly
   differs from the count one in **73–100% of scenarios** (bootstrap p_differ ≥ .95).
   *Impact:* the menu of efficient (strategy, budget) options a practitioner compares is almost
   always different under cost.
5. **The single-winner "flip" is mostly noise.** Report it honestly; do not lead with it.

The spine tying RQ1→RQ2/RQ3: equal sample size ≠ equal measured cost (the size→cost map is
*strategy-dependent*, RQ1), so at equal budget cheap samplers buy more data and the ranking moves.

---

## Finding 1 — Cost re-ranks the best samplers (KW), every family, robustly

KW top-group change % (the headline), and the learner-robustness check:

| family | **KW top-group change** | KW-significant | learner-robust (RF / CART) |
|---|---|---|---|
| REPLICATION-ICSE19 | **43%** | 100% | 52% / 43% |
| REPLICATION-ICPE20 (x264) | **55%** | 100% | 61% / 59% |
| ENERGY | **47%** | 78% | 62% / 52% |
| WORKLOAD | **50%** | 74% | 47% / 50% |
| LCBENCH *(external validation)* | **50%** | 79% | 50% / 43% |
| LINUX | **100%** | 100% | (HGBT, full features) |

*Impact / paper:* this is the new RQ2/RQ3 headline — defensible because it reuses the reviewers'
own test, speaks to the whole strategy set, is significant, **and survives a learner change**.

---

## Finding 2 — Who wins, who's over-/under-credited (systematic per-family)

For each family, the single-best sampler under **count** vs **cost**, plus the sampler that
**loses** the most tied-best membership under cost (over-credited by count) and the one that
**gains** the most (under-credited by count):

| family | champion: **count → cost** | over-credited (loses) | under-credited (gains) |
|---|---|---|---|
| ICSE19  | random → random | `divDistBased` (−4) | `distBased` (+2) |
| x264    | random → random | `random` (−11), `solverBased` (−7) | `distBased` (+6) |
| ENERGY  | random → random | `balanced` (−22) | **`pilotCost`** (+6) |
| WORKLOAD | random → **`pilotCost`** ⚑flip | `random` (−112) | **`pilotCost`** (+42) |
| LCBENCH | random → **`balanced`** ⚑flip | `random` (−21) | `balanced` (+39) |
| LINUX   | **`coverage` → `coverage`** | `balanced` (−9) | `uncertainty` (+1)* |

\*Linux's story is the *accuracy ranking*, not top-group flux: by MRE, `coverage ≈ random ≈
balanced` (≈7–8% at 20%) ≫ **`uncertainty` (active learning, ~9–18% — worst deployable)** ≫
`diversity` (broken). Champion = coverage in all three corrected releases.

**Four cross-family patterns (cite these):**
1. **The single champion flips under cost in 2 of 6 families** — WORKLOAD `random→pilotCost`,
   LCBENCH `random→balanced`. Elsewhere the champion holds but its margin shrinks. So even
   "who is #1" is not always cost-invariant.
2. **`random` is the count-era favourite the cost lens deflates** — champion by count in most
   families, yet the biggest top-group loser (x264 −11, workload −112, lcbench −21).
3. **The cost-aware sampler `pilotCost` gains under cost** in the generated families and *wins*
   WORKLOAD — direct evidence that **cost-aware acquisition pays off**. (Construct-validity note
   in §Robustness: the headline does not depend on it.)
4. **Mechanism invariant:** the sampler that is *accurate but pricey per configuration* loses
   under cost; the *cheaper-per-cost* one gains. The protagonist differs — solver-based t-wise
   (x264), `random`/`balanced` (others), and on Linux the "smart" feature-aware samplers
   (active learning, diversity) which are *both* uncalibrated *and* worse.

*Impact / paper:* (a) **researchers** assessing samplers at fixed *size* systematically mis-rank
the field — over-crediting interaction-rich/active samplers and under-crediting cheap ones;
(b) **practitioners** should include a cost-aware sampler and budget by cost, and should not
assume `random` is inferior — by count it looks worse than it is.

---

## Finding 3 — Concrete reversals (named, citable examples)

**ICPE20 (x264):** solver-based t-wise sampling is the count-best in **12 of 17 inputs at level
t1** and is **dethroned in 9 of those 12** under measured time — losing to diversified-distance
(`x264_0/_4/_6/_16`), `random` (`x264_2/_5/_12/_15`), or `henard` (`x264_14`). Best-in:
solverBased **12→5**, divDistBased **7→14**. (It picks slow-to-encode interaction-rich configs.)

**ICSE19:** the flagship `divDistBased` tied-best membership **5→1** (LLVM t3→random, lrzip
t2→distBased, BerkeleyDBC t3→random); `random` stays best in 11/21 cells under both lenses.

*Impact / paper:* drop-in named examples for the RQ2/RQ3 results section.

---

## Finding 4 — The Pareto-efficient choice-set robustly differs

The measured-cost efficient set of (strategy, budget) combos differs from the count-cost set,
reproducibly under bootstrap (p_differ ≥ .95): **ENERGY 80%, LCBENCH 89%, WORKLOAD 73%, ICSE19
6/7, x264 17/17, LINUX 100%**; median Jaccard 0.60–0.65. *Impact:* the decision-level claim —
the efficient menu a practitioner would compare is almost always different under cost; robust,
λ-free, and stronger than the single-winner flip.

---

## Finding 5 — Linux: simple/calibrated samplers win; smart ones fail

On Linux (largest, hardest system; corrected to full features + HGBT, MRE ~7–8% at 20%):
- **Champion = `coverage`** (all 3 releases), `random`/`balanced` tied just behind.
- **`uncertainty` (active learning) is the WORST deployable sampler** at every level; `diversity`
  is broken.
- **Cost-effect strongest: KW top-group change 100%, Pareto p_differ 1.0.**
- **RQ1 calibration:** `random`/`balanced`/`coverage` are **calibrated** (cost/size ≈1.0×); the
  feature-aware "smart" samplers are **uncalibrated** — `diversity` over-spends (1.4×),
  `uncertainty` under-spends (0.57×). (Core RQ1 — size is a poor cost proxy for smart samplers —
  holds and strengthens; cost values = vmlinux size, learner-independent.)

*Impact / paper:* a clean, defensible exhibit — even the "smart" active-learning sampler fails on
the hardest system; the simple, *calibrated* samplers win and cost still re-ranks the field.
*(Methodological note: Linux requires the full 9,645-feature option space, not a top-512 subset,
and a gradient-boosting learner; earlier truncated-feature Linux numbers are superseded.)*

---

## Finding 6 — Top-1 flip is mostly noise (secondary)

The single best (strategy, budget) combo changes often (538/1,666 in the original audit), but
under a median-decision bootstrap most flips are within noise; the robust ones concentrate where
target≠cost (x264 asymmetric) or cost is heavy-tailed (energy). Mostly noise under all learners.
*Impact:* keep as a decision-level illustration *after* KW + Pareto; do not lead with it.

---

## Robustness (threats, addressed)

- **Learning-algorithm sensitivity — PASSED.** KW change holds across ridge/RF/CART (43–62%),
  Pareto robust under all three, flip noise under all three — even where a learner fits less well.
  (`learner_sensitivity_summary.md`.)
- **Construct validity (candidate set) — PASSED.** `pilotCost`'s gain is partly circular, so it is
  **not load-bearing**: the 43–55% headline holds on the 3 families with *no* cost-aware sampler
  (replications + Linux), and where pilotCost is present only ≤8–13% of changes hinge on it.
- **Accuracy gate.** Always check median MRE before trusting a comparison (both pipelines emit it).
  Sane fits (most families <15%) give trustworthy rankings; lrzip ~49% / kanzi ~80% are inherently
  hard. *Linux needs full features + HGBT to reach a sane ~7%* (else ~30%, ranking is noise).

---

## Paper retrofit plan

- **T1 — ADD the cost-controlled KW comparison as the RQ2/RQ3 headline** (43–55%, learner-robust).
  `4-study_design.tex` (~l.53) + `5-results.tex`. Numbers: Finding 1; named examples: Finding 3.
- **T2 — ADD the systematic per-family table (Finding 2)** — champions, over/under-credited, the
  four patterns. This is the substantive "decision impact" result.
- **T3 — STRENGTHEN Pareto with bootstrap robustness (Finding 4)**; `5-results.tex:213–219`.
- **T4 — WRITE the Linux exhibit per Finding 5** (coverage wins, active learning loses, RQ1
  calibration). Replace any active-learning-champion text.
- **T5 — DEMOTE the top-1 flip (Finding 6)**; `5-results.tex:208–228`, `9-conclusion.tex`.
- **T6 — ADD a learner-sensitivity sentence/appendix row** (effect holds across ridge/RF/CART).
- Figure 4 (exastencils) stays cut.

---

## Reproducibility & files (compact)

**Env:** `.venv-linux/bin/python` (python 3.14.3, scikit-learn 1.8.0, numpy 2.4.4, scipy 1.17.1).
**Learners** (each `-log`/`-raw`): `ridge` = custom closed-form, alpha=1.0; `sk-rf` =
RandomForest(200 trees, max_features="sqrt"→use None on Linux, n_jobs=-1); `cart` = custom tree
(depth 6); `sk-hgbt` = HistGradientBoosting(max_iter 300) — Linux only. **Params:** seeds 30
(learner-sweep 10), bootstrap 1000, eval-cap 6000 (Linux 4000), λ=[0.1,0.25,0.5,1,2,4,10].

**Regenerate:**
```bash
# KW + flip + Pareto, per family/learner:
scripts/kw_cost_vs_size.py --mode {icse19,x264,twins,workload,lcbench} --learner {ridge-log,sk-rf-log,cart-log} --all-metrics --out artifacts/lsens_<fam>_<lr>.csv
scripts/stream_b_others.sh                 # the full ridge/RF/CART sweep
# Linux (corrected — full features + HGBT):
scripts/significance_linux.py --top-k-features 0 --learner sk-hgbt-log --releases 420 508 500 504 --runs-stoch 15 --runs-other 10 --eval-cap 4000 --out-prefix artifacts/significance_linux_hgbtfull
```

**Key data:** `kw_cost_vs_size_<fam>.csv`, `significance_pareto_<fam>.csv`,
`significance_flips_<fam>.csv`, `lsens_<fam>_{ridge,rf,cart}{,_flip,_pareto}.csv`,
`significance_linux_hgbtfull_*` (corrected Linux). Reports: `learner_sensitivity_summary.md`,
`kw_reanalysis_report.md`, `significance_consolidated.md`. Decisions/caveats:
`significance_decisions.md` (incl. C1 median-decision bootstrap, C12 construct validity,
C13 MRE-tail, C16 Linux feature-truncation [resolved]).
