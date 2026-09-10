# Overnight handoff — ICSE 2027 review-response (deadline July 1 2026, ~14:00 Paris / 23:59 AoE June 30)

Context: three reviews synthesized into a prioritized plan. User approved direction, then went to sleep
authorizing intensive overnight compute. This note = state at handoff so work resumes cleanly.

## Decisions locked with the user
1. **Linux: DEMOTE, do not delete.** Keep it, but move the headline acquisition-cost claim onto the
   five true acquisition-cost families; present Linux as a clearly-labeled *resource-budget stress
   test* with R2's framing: size ≡ cost ⇒ the 100% result proves **strategy-induced selection bias
   alone breaks the count proxy** (no target≠cost asymmetry needed). Strongest spin, keeps the
   sturdiest robust evidence (Linux robust KW 97%, Pareto 100%).
2. **pilotCost/oracles ablation: GREEN-LIT** (unanimous reviewer ask). Computing now.
3. **KW vs Pareto framing:** keep KW reuse as the *method* backbone (R2: "single best methodological
   decision"), but lead the *headline numbers* with the robust lenses — Pareto p_differ 73–100%,
   strict-dominations 57/538, eviction 29–41% — and show KW top-group∆ next to its bootstrap-robust
   subset honestly. Consistent with prior memory (KW lead) reconciled: KW = credibility, Pareto = headline %.

## Overnight jobs (all backgrounded; bai09tqgg completion = everything done)
- **bpayzs4dr** — `scripts/overnight_ablation.sh` → `artifacts/ablation/`. ABLATED (`--exclude
  pilotCost cheapOracle expensiveOracle`) KW/Pareto/flip for energy, workload, lcbench:
  Phase1 largest-n+bootstrap+all-metrics(ridge); Phase2 minerr(ridge); Phase3 largest-n(sk-rf).
- **bai09tqgg** — `scripts/overnight_reversal_chained.sh` → `artifacts/reversal/`. Waits for the
  ablation DONE marker, then computes non-monotone reversal rate (icse19,x264,energy,workload,lcbench).
- **b9w3zb9ht** — bibliography URL HTTP-resolvability check (reference integrity).
- NOTE: a *prior* `overnight_kw_corrected.sh` CART phase (PID ~1363) was still finishing — separate
  output files (`artifacts/corrected/kw_*_cart-log_*`), no conflict.

## Done overnight (safe, unattended)
- `main.tex:34` → `\usepackage[hidelinks]{hyperref}` (kills the red/green link boxes; desk-reject risk).
- Fixed dead DOI `10.1145/3744916.3764542` (confirmed 404) for `xiang2026dhda` in BOTH `ml.bib`
  (source) and `main.bbl` (generated) → arXiv:2507.08730 / https://arxiv.org/abs/2507.08730.
- **Reference-integrity sweep (15 URLs in main.bbl):** all resolve. arXiv=200, IEEE TSE=202, ACM
  10.1145/*=403 — the 403 is dl.acm.org bot-blocking curl AFTER doi.org successfully resolved+
  redirected (a fake DOI 404s at the doi.org step, as the fixed one did), so the ACM DOIs are valid.
  The lone true 404 was the one fixed. RECOMMEND a quick human browser spot-check of the 2025/26 ACM
  DOIs (3702986, 3803859, 3643743, 3643751) for camera-ready peace of mind, but no fabrication found.

## Baselines to compare the ablation against (FULL candidate set, already in artifacts/corrected/)
| family   | n   | KW top-group change | robust(≥.95) | samplers (full)            |
|----------|-----|---------------------|--------------|----------------------------|
| ENERGY   | 74  | 35/74 = 47%         | 13           | balanced, pilotCost, random|
| WORKLOAD | 846 | 389/846 = 46%       | 178          | balanced, pilotCost, random|
| LCBENCH  | 350 | 146/350 = 42%       | 42           | balanced, pilotCost, random|
Ablated candidate set = {balanced, random} (cost-blind). Smoke test (2 energy systems): full 53% →
ablated 23% top-group change, eviction 15% → **effect survives without the cost-aware sampler.**

### ABLATION RESULTS (authoritative, recomputed from the _ABL.csv files)
| family   | FULL incl pilotCost | **ABLATED {balanced,random}** | evict | Pareto≥.95 ablated |
|----------|---------------------|-------------------------------|-------|--------------------|
| ENERGY   | 47% (35/74)         | **54% (35/65)**, robust 7/35  | 17%   | 6/9 = 67%          |
| WORKLOAD | 46% (389/846)       | **52% (393/753)**, robust 103/393 | 17% | 58/93 = 62%      |
| LCBENCH  | 42% (146/350)       | *re-running (was killed)*     | —     | —                  |
KEY MESSAGE for §VII: the cost re-ranking is **NOT a pilotCost/oracle artifact** — with only cost-
blind random/balanced it persists (slightly strengthens: 54%/52% vs 47%/46%) and Pareto divergence
stays high (67%/62% vs 80%/73% full). Eviction steady at 17%. Read headline % as "fully present",
not a strict delta (candidate set 2 vs 3 samplers, denom shifts).

### LCBENCH ablated (completed on resume) + REVERSAL — INTEGRATED INTO PAPER
- LCBENCH ablated: KW top-group **32%** (100/315) vs full 42%; evict 3%; Pareto **71%** (25/35).
  So the trio: ENERGY 47→54, WORKLOAD 46→52 (strengthen), LCBENCH 42→32 (attenuate but persists).
- ENERGY reversal: within-strategy **0.6%**, cross-strategy **14.2%** (237/1668), **89%** of contexts;
  archives icse19 0.8% / x264 0% → reversal is a heavy-tailed-cost phenomenon, near-absent on homogeneous.
- **EDITS MADE (user-authorized):**
  - `7-threats.tex` Strategy-panel para → quantified ablation (32–54% KW, evict ≤17%, Pareto 62–71%,
    full-panel 47/46/42), honest that lcbench attenuates.
  - `5-results.tex` RQ1 body (after budget-calibration para) → cross-strategy reversal 14%/89% vs ≤0.8% archives.
  - `5-results.tex` RQ1 answer box → tightened with the 14% \StudyEnergy figure.
- ⚠️ **COORDINATION RISK:** my ablation/edits use **9-system** energy (full 47%, matching current paper).
  If the other agent switches energy headline to **14-system** (full 50%), the §VII energy ablation row
  (47→54) must be recomputed at 14 systems for consistency — ~15 min: `--mode twins --target-prop energy
  --systems 7z Apache HSQLDB LLVM MongoDB PostgreSQL VP8 brotli exastencils jump3r kanzi lrzip nginx x264
  --exclude pilotCost cheapOracle expensiveOracle`. Decide 9 vs 14 FIRST, then lock both.
- NOT YET COMPILED — user must run latexmk to confirm ≤10 pages + clean build.

### SESSION-2 EDITS APPLIED (I now own all .tex; other agent stood down via HANDOFF_TEX_ENERGY14.md)
Authoritative 14-sys energy: full KW 50% / Pareto 80%; **ablated KW 59%** (58/98), evict 22%, Pareto 71%;
**reversal cross-strategy 11%** (264/2472), 79% of contexts (11/14), within 0.5%.
Applied (all obey global no-em-dash / no-semicolon rule; verified clean):
1. `7-threats.tex` §VII ablation → energy full 50 (was 47), ablated 59 (was 9-sys 54), evict up to 22%,
   Pareto 62–71%; honest "stronger on energy+workload, attenuated on lcbench".
2. `5-results.tex` RQ1 reversal → 11% / 79% contexts (was 9-sys 14%/89%); em-dash removed.
3. `3-cost_model.tex` → LINUX DEMOTE reframe: vmlinux size = resource-budget proxy (not acquisition
   cost); size≡cost ⇒ strategy-bias-alone framing; rest acquisition claim on the 5 families.
4. `4-study_design.tex` + `5-results.tex` → "deployable" budget rule softened to "retrospective,
   cost-indexed evaluation device".
5. "seven releases" → "six releases" (data-confirmed: 6 = linux415/420/500/504/507/508) in
   `5-results.tex` + abstract.
Earlier session: hidelinks, DOI 404→arXiv (ml.bib + main.bbl), full URL sweep (all resolve).

### FLAGGED FOR USER / COMPILE STEP (I cannot do these reliably)
- **Page limit ~0.2 over** (handoff #6) + my cost-model reframe adds ~6 lines → trim needed. Can only be
  measured by `latexmk`. Candidates: intro lrzip deep-dive, RQ3 brotli paragraph. USER decides at compile.
- **MRE figure units** (Fig 1 / Fig 4 mixing decimals vs %): needs figure regeneration, not a text edit.
  Body MRE values are decimals consistently.
- **Artifact anon URL** at `9-conclusion.tex:33` (only real placeholder in a compiled file).
- **Novelty-vs-mutation-testing paragraph + HPO cites** (R2): additive, DEFERRED given page pressure —
  fold 1–2 sentences into `8-related_work.tex` only if space allows after the trim.
- **Cost-semantics TABLE** (R1/R2/R3): skipped for space; the §III prose reframe covers the construct.
- **J_λ normalization spec** (R2 P2): "within-context scale" still vague; minor.

### DECISION: ENERGY = 14-system (user, confirmed). Paper RQ2 ALREADY 14-system!
The in-paper RQ2/Table `tab:rq-metrics` already uses 14-system energy: **KW 50% (56/112), robust 26%,
evict 17%, Pareto 80% (45/56), Jaccard 0.65** (5-results.tex:128,164,180,215). So my earlier §VII
edit was WRONG (used 9-system 47% full / 54% ablated). FIX PENDING on batch `bibo4zj3j`
(scripts/energy14_recompute.sh): 14-sys full (confirm 50% + Pareto), 14-sys ABLATED, 14-sys reversal.
- §VII to become: energy full **50** (not 47), ablated = 14-sys figure (TBD), Pareto/evict ranges from
  14-sys ablated. Workload 46 / LCBench 42 stay; ablated 52 / 32 stay (those were already 14-sys? NO —
  workload/lcbench ablated were the standard sets, consistent with paper). Verify workload/lcbench
  denominators match paper (workload KW 46%, lcbench 42%) — they do (Table lines 181-182).
- RQ1 reversal "14%" (9-sys) → 14-sys figure (TBD from reversal_energy14.csv).
- FILE OWNERSHIP (user-confirmed): I own 7-threats.tex + 5-results.tex; other agent owns
  main.tex/abstract/Table II(=tab:rq-metrics is physically in 5-results.tex though — COORDINATE)/3-cost_model.tex.
  NOTE: tab:rq-metrics lives in MY 5-results.tex but is "Table II" — already 14-sys-correct, do not edit.

### KILL/RESUME (batch bpayzs4dr killed ~11:06, likely machine sleep)
DONE before kill: energy + workload ablated Phase-1. Missing: lcbench ablated, reversal, minerr/RF
phases. RESUME job = `scripts/overnight_resume.sh` (bg bki0r1dvi), priority order: lcbench ablated →
energy reversal → other reversals → minerr → RF. If killed again, the two CORE items finish first.

## Reversal early signal (archive families, already computed)
icse19 cross-strategy larger-yet-cheaper 0.8% (1/7 ctx); x264 0.0%. Near-zero on homogeneous-cost
archives = HONEST nuance ("proxy safest under homogeneous cost"). Expect real signal in ENERGY
(heavy-tailed). within-strategy ≈0 everywhere (a strategy's own size orders its own cost).

## Morning plan (in order)
1. Parse `artifacts/ablation/run.log` → build the per-family FULL-vs-ABLATED table (KW top-group∆ +
   robust + eviction + Pareto p_differ). Task #3.
2. Retrofit: ablation numbers into `7-threats.tex:~32` (construct-validity para) + RQ2 results; state
   prominently the effect holds on replications+Linux (no cost-aware sampler at all).
3. Reversal numbers into RQ1 (report within vs cross; concentrate claim on heavy-tailed families).
4. Remaining P0: artifact anon URL+README (NEEDS USER — anon.4open.science/Zenodo); complete sparse
   refs [4]/[5]/julianasurvey venue details; confirm main text ≤ p10 after edits.
5. P1 writing: Linux reframe paragraph + cost-semantics table; MRE unit normalization (% everywhere);
   reconcile counts (energy denominator, seven-releases/30/6-6, five-non-Linux).
