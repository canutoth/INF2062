# RQ2 flip-significance study — decisions & caveats (canonical record)

Status: 2026-06-24. This records every methodological decision and caveat in the
significance analysis of RQ2 "the recommendation changes" flips, so the analysis
is reproducible and auditable. Companion files: `significance_methods.md`
(parameters), `memory/reference_data_sources_repro.md` (data sources).

---

## 0. The question

The paper's RQ2 reports that the top strategy–budget recommendation **changes**
in 538/1,666 context–weight decisions when measured cost replaces count cost.
Are those flips **statistically robust**, or are many of them within noise (the
median is a near-tie that the cost model tips)? This started from doubting that
Figure 4 (exastencils target↔cost asymmetry) communicated "how much" the switch
matters.

---

## 1. Decisions about the *estimand* (what we test)

**D1. Median-decision bootstrap, not single-run.** The paper's decisions are
medians (later: also mean) over runs. The significance question is "is the
**reported aggregate flip** stable under resampling," NOT "would a single run
flip." Each bootstrap replicate resamples (a) held-out evaluation configs and
(b) the runs of each cell, recomputes the aggregate MRE/cost per cell,
recomputes the count- and measured-cost winners **over all candidates**, and
checks whether the same (count-winner → measured-winner) flip recurs.
*Caveat C1: our first implementation drew single runs; it understated robustness
badly (e.g. x264_12 asymmetric flips read as noise vs p=1.00 under the correct
median-decision bootstrap). The single-run results were discarded.*

**D2. Resampling axis = test set + runs, not seeds alone.** `pairwise` and
`diversity` are **deterministic by construction** (one sample, fixed seed-0 RNG,
`generated_sampling.py:705`), so seed-resampling is undefined for them. MRE is a
mean of per-config relative errors over the held-out population
(`analysis.py:86`), so we bootstrap the **evaluation configurations** — a uniform
uncertainty axis for deterministic and stochastic strategies alike.
*Caveat C2: deterministic strategies get only the eval-set axis (no run
resampling), so their robustness reflects evaluation uncertainty only.*

**D3. Aggregation = report BOTH mean and median.**
- **Median** matches the existing pipeline (`strategy_summary` uses
  `median_mre`, `median_pct_cost`) and is robust to unlucky heavy-tail runs.
- **Mean** is the **primary** lens: it is the expected-behavior estimand ("on
  average, using this strategy, does measured cost flip the recommendation?")
  and the faithful cost statistic — expected budget = `n × mean ≫ n × median`
  under right skew, so **median cost understates the acquisition burden**.
*Caveat C3: mean is outlier-sensitive. Where mean and median disagree, the flip
is driven by a few heavy-cost runs; under the heavy-tailed-cost thesis those are
real acquisition events, but we disclose every such disagreement rather than
hide it.*

**D4. Two-tier reporting on `p_reproduce`** (fraction of replicates reproducing
the flip):
- **flips-on-average**: `p > 0.5` — in expectation the recommendation flips.
- **significant**: `p ≥ 0.95` — and reliably so.
*Caveat C4: `p` is reported continuously, so both thresholds are adjustable; 0.95
is a convention, not a hard truth.*

**D5. Flip criterion is a conjunction:** a replicate "reproduces the flip" only
if the count side still prefers the count-winner AND the measured side prefers
the measured-winner. Both must hold for the recommendation to actually differ.

---

## 2. Decisions about *scope & parameters*

**D6. Families:** ENERGY (TwinsOrFalseFriends, 14 systems), REPLICATION-ICSE19
(7 systems, NewRuns), REPLICATION-ICPE20 (x264, 17 inputs × 4 combos, AllRuns),
WORKLOAD (93 contexts), LCBENCH (35 datasets), LINUX (7 releases).
*Caveat C5: LCBench is flagged out-of-core-scope in `feedback_dataset_scope`
(ML/HPO, external validation), but the user kept it inside the 1,666 audit — a
scope-consistency tension to resolve in the writeup.*
*Caveat C6 (status): ENERGY + ICSE19 + ICPE20 are run. WORKLOAD / LCBENCH /
LINUX adapters are pending (different loaders; LCBench needs the external
`data_2k_lw.json`).*

**D7. seeds = 30** for generated families (significance comes from the test-set
bootstrap, so 30 suffices, ~3× cheaper than the 100-seed exploratory batch).
Replication families use the archives' real repeated runs (~100/cell).

**D8. bootstrap B = 1000.**

**D9. eval-cap = 6000** held-out configs (fixed random holdout per scenario) to
bound time/memory on large systems (exastencils 86k, LLVM 65k, 7z 69k configs).
*Caveat C7: this approximates full-population MRE; negligible for n≪N and uniform
across candidates (cancels in the ranking), but it is a cap, not the full pop.*
*Caveat C8: the median-decision bootstrap evaluates each run on the full holdout
without masking that run's own ~n training configs; n≪6000 and the bias is
uniform across cells, so it cancels in the argmin.*

**D10. learner = ridge-log, alpha = 1.0** (matches the figure and primary
batches).

**D11. candidates = ordinary strategies only.** Generated:
{random, balanced, diversity, pairwise, pilotCost}. Replication archives:
{distBased, divDistBased, henard, random, solverBased} × {t1, t2, t3}. Diagnostic
oracles (cheap/expensive) excluded, matching the paper.

**D12. weights λ = [0.1, 0.25, 0.5, 1, 2, 4, 10].** Winner = argmin
`J = minmax(MRE) + λ·minmax(cost)`, identical to `analysis.rank_stability`.

**D13. Four cost/target combos per system:** symmetric (cost=target) and
asymmetric (cost≠target). ENERGY headline numbers align to the cost=performance
scenarios (matches the paper's 196 energy decisions).
*Caveat C9: the cost_energy combos charge energy as the acquisition cost — the
"charge-the-target" framing the paper cautions against; included for
completeness and reported separately.*

**D14. revision pins:** brotli = 1.0.7, PostgreSQL = 11.2 (match the paper's
revision-specific systems; other twins systems have no revision column).

---

## 3. Decisions about the *paper* (Figure 4)

**D15. Cut Figure 4** (`energy_target_cost_asymmetry_exastencils.png`) and fold
the target↔cost point into RQ2 prose tied to the generalizable evidence (the
24/28 performance–energy scenarios and the x264 asymmetry). Done in
`5-results.tex`. Rationale: it dramatized a single, *atypical* system.
*Caveat C10: exastencils is the extreme outlier — most fragile (decisiveness
0.8% of score range) and most-flipping (6/7 weights). The original figure's
"asymmetry" reads as general but is not; the symmetric time/time case flips at
least as often across systems.*

**D16. Framing:** lead RQ2 impact with the flip + its sharpness; strict
dominance is the exceptional case (the robust core), never frame a family as
"safe." (See `feedback_rq2_framing`.) The significance work supports this: the
asymmetric/heavy-tailed flips reproduce; symmetric ones don't.

---

## 4. Key results so far (median-decision bootstrap)

- **REPLICATION-ICSE19** (7 sys): 8 flips, **1 robust** (lrzip solverBased
  t1→t2: larger sample 86% cheaper AND 77% more accurate — an *inversion*, the
  high-n-cheaper figure). The trade-off flips stay within noise. Mean lifts the
  median p from 0.52 → 0.78.
- **REPLICATION-ICPE20** (x264, median): 60 flips, 9 robust.
  **Asymmetric (target≠cost): median p = 0.66 (flips on average), 9/46 robust.
  Symmetric (target=cost): median p = 0.29 (does NOT flip on average), 0 robust.**
  This is the Figure-4 asymmetry, statistically grounded.
- **ENERGY**: single-run pass found robust flips concentrated in jump3r/x264
  (heavy-tailed cost); median-decision re-run pending consolidation.

Overarching pattern (the two-axis story): flips reproduce where **target≠cost**
or **cost is heavy-tailed**; they are within noise where target=cost and cost
spread is moderate (the proxy's validated regime). Strict-dominance and
"soft failures" (trade-offs whose accuracy edge is itself within noise)
concentrate in the former.

*Caveat C11: replication families use precomputed real samples (~100 runs);
generated families use the 30-seed generated protocol — robustness power differs
by family, so cross-family p comparisons are indicative, not exact.*

---

## 5. Reproduction

Energy: `scripts/significance_flips.py` (twins archive). Replications:
`scripts/significance_flips_archive.py` (ICSE19) and `scripts/significance_flips_x264.py`
(ICPE20). Shared core: `scripts/sig_core.py` (`median_decision_flips`, with
`agg='median'|'mean'`). Energy data: Zenodo 7647208 / GitHub
`AI-4-SE/TwinsOrFalseFriends`. Reproduction of the stored 100-seed artifacts was
verified: deterministic strategies match exactly; stochastic within seed noise.

---

## 6. Later caveats (added 2026-06-26)

**C12 (construct validity — candidate-set composition).** The set of compared
samplers is a construct. That the cost-aware sampler `pilotCost` gains under cost
(and wins WORKLOAD) is partly built in — a cost-efficient strategy is expected to
rank well under cost-controlled evaluation. Mitigation (in-data): the 43–55%
top-group change holds on the **3/6 families with NO cost-aware sampler**
(both replications + Linux); where `pilotCost` is present only ≤9–13% of changes
hinge on it. Report it as a consistency check, not primary evidence. Gold-standard
test: `kw_cost_vs_size.py --exclude pilotCost` (option now exists). Full discussion
in `HANDOFF_RQ2_COST_SIGNIFICANCE.md` §9/§11.

**C13 (metric choice — MRE under-weights the expensive tail).** MRE = mean of
|y−ŷ|/|y|; the 1/|y| normalization down-weights large-target configs. When cost
correlates with target magnitude — definitional on Linux (cost≡target≡size),
partial in time/energy — the expensive tail coincides with MRE's blind spot, so a
cost-avoiding strategy is doubly favoured (cheaper AND its tail errors forgiven).
MRE's bias is identical per (strategy,level) cell, so it does NOT mechanically
create the count-vs-cost difference, but it can inflate its magnitude and decide
the cost-view winner (metric-relative). Mitigations: replications inherit MRE from
ICSE19/ICPE20 (we change only the effort axis); log-target learner makes MRE
natural; the effect also appears where cost≠target. Recommended test: recompute KW
under mean-absolute-error / RMSE / top-decile-cost-weighted error (needs eval to
store absolute error + target magnitude; not yet run). Full discussion in
`HANDOFF_RQ2_COST_SIGNIFICANCE.md` §9 (C13) and §12.

**C14 (learner mismatch — supersedes/qualifies D10).** D10 said "learner =
ridge-log ... matches the figure and primary batches." Per the paper's
learner-sensitivity appendix the PER-FAMILY primary learners are: ENERGY/WORKLOAD
ridge/log-linear, LCBENCH ridge/raw (the significance re-analysis MATCHES these),
replications "original regression" (ridge-log approximates), and **LINUX =
all-feature sklearn HGBT (mismatch)**. The Linux significance (KW/Pareto/flip,
active-learning-is-#1, exclude-AL, cost-at-size) is all under ridge-log, not the
paper's primary HGBT. The cost-EFFECT magnitude is likely learner-robust
(appendix: RQ1/RQ2 learner-independent) but the STRATEGY-IDENTITY claims (esp.
"active learning is the Linux champion") are learner-dependent and must be
re-validated with `significance_linux.py --learner sk-hgbt-log` before going in the
paper. Top-priority action; see `HANDOFF_RQ2_COST_SIGNIFICANCE.md` §9 (C14) / §12.
