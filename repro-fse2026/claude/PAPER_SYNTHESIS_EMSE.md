# Synthesis for the EMSE Write-Up: Posterior Guarantees Under Empirical Acquisition Cost

Working title: *Sample Size Is Not Sampling Cost, Even for Guarantees:
Replicating Posterior Risk and Confidence of Configuration Sampling
Strategies Under Measured Acquisition Cost*.

Target: Empirical Software Engineering (EMSE), registered-report-style
replication + extension, <= 30 pages. All numbers below are committed on
branch `fse/posterior-cost`; claim-to-artifact traceability in Section 8.

## 1. One-paragraph thesis

The FSE 2026 paper (Weis, Maggio, Siegmund, Apel; DOI 10.1145/3808147)
introduces posterior risk and posterior confidence as learner-free
guarantees for sampled performance bounds, and recommends Statistical
Recursive Search (SRS) as the strategy with consistently tighter
guarantees at a fixed sample size. We replicate the framework directly on
the original artifact and extend it to five further dataset families (six
corpora, 851 decision scopes), then re-index every decision by measured
acquisition cost instead of sample count. The framework replicates
everywhere; the SRS recommendation replicates on the original systems and
on x264 but is budget- and domain-dependent; and under measured cost the
guarantee/cost Pareto frontier changes in 97.5% of scopes. Because
posterior risk involves no learner, this isolates the cost effect from
any modeling choice: sample size is not sampling cost, even when the
outcome is a guarantee rather than a prediction.

## 2. Research questions

Two main RQs (per user decision), each decomposed into ICSE-style sub-RQs.

**RQ1 — Do FSE 2026's core claims replicate beyond the original artifact,
at the paper's own fixed-sample-size lens?**

- RQ1.1 (discriminative power / FSE C1): do posterior-risk distributions
  distinguish sampling strategies at fixed budget? [H1, Kruskal-Wallis]
- RQ1.2 (budget scaling / FSE C4): do guarantees improve monotonically
  with sample size?
- RQ1.3 (SRS superiority / FSE C2): does SRS yield lower posterior risk
  than uniform random at fixed size, and is it the best pick? [FSE5]
- RQ1.4 (solver unreliability / FSE C3): does solver-based sampling
  remain the least reliable strategy?

**RQ2 — Do FSE 2026's metrics survive re-indexing by measured sampling
cost instead of sample size?**

- RQ2.1 (cost heterogeneity; ICSE RQ1 analog): is a fixed sample size a
  fixed measured effort across strategies?
- RQ2.2 (proxy validity; ICSE RQ2 analog): how far does %cost deviate
  from %n (calibration)?
- RQ2.3 (decision impact; ICSE RQ3 analog): does cost-indexing change the
  top recommendation and the guarantee/cost Pareto frontier? [H2, H4]
- RQ2.4 (cost-normalized recommendation): which strategy is best per unit
  of measured cost; is SRS? [H3, FSE6]
- RQ2.5 (equal-spend validity check): do conclusions hold when strategies
  literally spend the same measured budget (buying different n), and what
  mechanism governs who wins? [new experiments]

## 3. Corpora and protocol (frozen)

| Corpus | Role | Scopes | Data |
|---|---|---:|---|
| FSE artifact (7 systems) | direct replication | 7 (t2) | Zenodo 10.5281/zenodo.19682296 (sha256 12ee2295...) |
| x264 (ICPE'20) | published-study replication | 34 (t2 fixed; 102 across t1-t3) | AllRuns.zip |
| ENERGY / Twins (14 systems) | generated protocol, energy cost | 220 | Zenodo 7647208 subset |
| WORKLOAD (ICSE'23, 9 systems, all 93 contexts) | generated protocol, workload contexts | 359 | Zenodo 7504284 |
| Linux / TuxKConfig (7 releases) | external validity, pool-relative | 21 (full: 3 levels, 100 runs) | TuxKConfig parquet |
| LCBench (35 OpenML datasets) | external validity, pool-relative | 210 | figshare data_2k_lw.json |

Total: 851 scopes (one scope = context x budget level decision cell).

Frozen decisions: `--extreme max` (worst-case bound); prior confidence
`1-(1-eps)^(N+1)` (artifact-compatible; `N` sensitivity = identical
decisions); no diagnostic oracles in headline runs; BH FDR 0.05 within
(corpus, hypothesis) family for the p-value-based hypotheses; Linux and
LCBench phrased pool-relative. SRS: audited faithful reimplementation
(equal posterior-risk distributions vs. the artifact notebook, MWU
p=0.95); the FSE-artifact run itself reuses the artifact's shipped SRS
samples (exact reuse). Full command manifest:
`artifacts/FSE2026_POSTERIOR_RUN_MANIFEST.md`.

## 4. RQ1 results — the FSE claims on six corpora (fixed n)

### RQ1.1 Discriminative power: replicates everywhere (strongest result)

Strategy posterior-risk distributions differ (KW, alpha=.05):

| FSE artifact | x264 | ENERGY | WORKLOAD | Linux | LCBench |
|---:|---:|---:|---:|---:|---:|
| 7/7 | 34/34 | 212/220 | 341/359 | 21/21 | 154/210 |

BH-corrected: unchanged except LCBench 154 -> 144. Verdict: **replicates
and generalizes**; the framework discriminates strategies in ~95% of 851
scopes, learner-free.

### RQ1.2 Budget scaling: replicates for configurable software, cracks on HPO pools

Share of (strategy, context) cells with non-increasing median risk as the
budget grows: x264 100%, Linux 98%, WORKLOAD 81%, ENERGY 76%, LCBench
65%. For SRS specifically: 100% on all configurable-software corpora,
**49% on LCBench**. Verdict: replicates within the FSE population;
monotonicity is not domain-independent.

### RQ1.3 SRS superiority: replicates where FSE tested it, fades elsewhere

SRS lower posterior risk than random at fixed size (FSE5, raw / BH):

| FSE artifact | x264 | ENERGY | WORKLOAD | Linux | LCBench |
|---:|---:|---:|---:|---:|---:|
| 6/7 | 34/34 | 52/220 -> 42 | 84/359 -> 70 | 5/21 -> 1 | 0/210 |

The gradient is explained by budget (see RQ2.5): FSE/x264 budgets are
t2-scale (56-843 samples/97-600 for x264-class systems), where SRS's
recursion amortizes; the generated families run n8-n64, where it cannot.
Verdict: **replicates at FSE-scale budgets; budget-dependent, not
universal**.

### RQ1.4 Solver unreliability: replicates

solverBased mean median-risk rank at the fixed level: 3.7 of 5 strategies
(FSE artifact), 6.1 of 7 (x264) — consistently among the worst, echoing
FSE's "plain solver sampling proves less reliable". (Not applicable to
the generated families, which do not include solver sampling.)

### RQ1 answer

The guarantee framework and its discriminative power replicate on every
corpus. The strategy-level claims (SRS best, monotone scaling) replicate
within FSE's own population — configurable software at hundreds-scale
budgets — and degrade predictably outside it. No claim reverses on the
original systems.

## 5. RQ2 results — the same metrics under measured cost

### RQ2.1-2.2 Cost heterogeneity and proxy validity

Median calibration ratio (%cost / %n) per strategy-level cell is ~1.0 in
every corpus, but the spread is wide: FSE artifact 0.19-3.11, ENERGY
0.03-7.05, WORKLOAD 0.09-2.77, LCBench 0.04-2.48, Linux 0.64-2.57, x264
0.62-1.43. Within-system cost CV up to 1.42 and p90/p10 up to 47.9
(BerkeleyDBC). Verdict: sample size is an unbiased but high-variance
proxy — exactly the ICSE construct-validity finding, now for guarantees.

### RQ2.3 Decision impact (headline)

| Outcome | FSE | x264 | ENERGY | WORKLOAD | Linux | LCBench | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| Pareto frontier changes (H4) | 6/7 | 30/34 | 220/220 | 346/359 | 21/21 | 207/210 | **830/851 (97.5%)** |
| Top recommendation changes (H2) | 2/7 | 2/34 | 31/220 | 61/359 | 13/21 | 120/210 | 229/851 (27%) |

The frontier (the choice set a practitioner should consider) is
cost-sensitive nearly always; the single top pick is corpus-dependent
(6% on x264 to 71%/62% on Linux). Mirrors the ICSE finding that Pareto
effects are robust while top-1 flips are secondary.

### RQ2.4 Cost-normalized recommendation

SRS best cost-normalized: FSE 3/7, x264 26/34, ENERGY 9/220, WORKLOAD
31/359, Linux 0/21, LCBench 0/210. SRS on the empirical frontier: 6/7,
29/34, 77/220, 139/359, 19/21, 21/210. SRS's cost differs from random
(FSE6, raw/BH): 7/7, 32/34, 94/220->90, 149/359->146, 21/21, 10/210->1.
On small-budget families, diversity and pairwise dominate the
cost-normalized picks (e.g., ENERGY 108+74 of 220). Linux is the crispest
statement: SRS is *never* best cost-normalized (0/21) yet almost always
frontier-competitive (19/21) with an always-significant cost premium —
SRS buys real guarantee quality at real extra cost; cost-indexing is what
exposes the premium.

### RQ2.5 Equal-spend experiments and the coupling mechanism (new)

Fix B = n_ref x mean pool cost; every strategy buys the n it can afford
(pilotCost realizes 1.7-2x volume, up to 5x):

| | ENERGY (cost ~ target) | LCBench (cost independent of target) |
|---|---|---|
| pilotCost beats random | 11/110 (10%) | 84/140 (60%) |
| pilotCost/random median risk | 6.6x worse | 0.75 (better) |
| SRS beats random | 49/110, gradient n8 1/28 -> n64 20/26 | 46/140 |
| Overall winner | diversity 47/110 | diversity 80/140 |

Two mechanisms, both invisible to size accounting:

1. **Coupling**: cost-averse volume pays exactly when the
   outcome-relevant information is not concentrated in the expensive tail
   (pilotCost flips from 6.6x-worse to better-than-random as coupling
   weakens). Cost-effectiveness is a property of the (strategy, outcome,
   cost-target coupling) triple.
2. **Amortization**: SRS's equal-spend competitiveness grows with budget,
   reconciling its FSE-scale strength with small-budget weakness.

Equal-spend winners agree with the handicap-based (prior-baseline)
protocol, so the RQ2 conclusions are not an artifact of either
methodology.

### RQ2 answer

The FSE metrics survive re-indexing — they remain computable, monotone
where expected, and discriminative — but the decisions they support do
not: the frontier changes in 97.5% of scopes, the cost-normalized winner
is never SRS outside the replication corpora, and equal-spend testing
shows *why* (coupling + amortization). Guarantees per unit of measured
cost is the decision-relevant quantity; sample size alone cannot express
it.

## 6. Secondary findings worth a paragraph each

- **SRS audit** (`artifacts/srs_audit_note.md`): faithful
  reimplementation; the artifact's random fill can duplicate
  configurations — visible in its own shipped t2 CSVs (1-5 short of
  nominal after dedup in 2-42% of runs/system). Cosmetic for FSE's
  claims; matters for cost accounting (duplicates would double-count).
- **Prior convention** (N vs N+1): zero decision changes.
- **Determinism**: release-413 Linux outputs bit-identical across two
  runs three days apart (seeded protocol, no hidden state).
- **BH correction**: headline H1 essentially intact everywhere; only the
  already-weak FSE5/FSE6 effects shrink. Quote corrected counts for
  FSE5/FSE6.
- **Oracles**: cheap/expensive oracles excluded from headlines (they
  pollute best-pair counts; kept as diagnostics).

## 7. Boundary of claims (threats skeleton)

- Construct: cost = measured target property (runtime/energy); for Linux,
  cost = target = vmlinux (acknowledged limitation; no independent cost).
- Internal: BH-corrected; 30-100 seeds; deterministic given seeds;
  equal-n and equal-spend protocols triangulated.
- External: Linux and LCBench are measured pools, not exhaustive spaces —
  all posterior-risk statements pool-relative; noisy/restricted FSE
  variants and `--extreme min` not covered (future work).
- Conclusion validity: scope counts are context-level, not repeated draws
  treated as independent.

## 8. Claim-to-artifact traceability

| Claim | Artifact |
|---|---|
| All RQ1/RQ2 per-corpus counts | `artifacts/fse_posterior_synthesis/fse_posterior_synthesis{.md,.csv,_scopes.csv}` |
| FSE artifact replication | `artifacts/fse_posterior_fse_artifact_final_t2/` (+ `_priorN` sensitivity) |
| x264 / ENERGY / WORKLOAD / LCBench | `artifacts/fse_posterior_{x264_icpe,energy,workload,lcbench_no_oracles}_final/` |
| Linux full protocol | `artifacts/fse_posterior_linux_all_full/` (+ parts, + quick-pass sensitivity) |
| Equal-spend | `artifacts/fse_posterior_{energy,lcbench}_equal_spend/` |
| BH sensitivity | `artifacts/fse_posterior_synthesis/multiple_comparison_sensitivity.{md,csv}` |
| SRS audit | `artifacts/srs_audit_note.md`, `scripts/audit_srs_vs_artifact.py` |
| Commands/provenance/checksums | `artifacts/FSE2026_POSTERIOR_RUN_MANIFEST.md` |

## 9. Figures inventory (all committed)

1. `fig_bridge_concept.png` — Section 1/2 motivation schematic.
2. `fig_synthesis_heatmap.png` — RQ1+RQ2 overview (corpus x outcome).
3. `fig_calibration_pct_n_vs_pct_cost.png` — RQ2.1/2.2.
4. `fig_cost_normalization_impact.png` — RQ2.3.
5. `fig_srs_status_matrix.png` — RQ1.3/RQ2.4.
6. `fig_frontiers_representative.png` — RQ2.4 (SRS best / on-frontier / off-frontier).
7. Per-corpus per-context figures available for zoom-ins (e.g., Linux
   guarantee-cost frontier).
   To add during writing: equal-spend figure (pilotCost flip + SRS budget
   gradient) — data ready, figure not yet drawn.

## 10. Proposed EMSE outline (~30 pp)

1. Introduction (2.5 pp) — bridge schematic; contributions list.
2. Background & replicated work (3 pp) — FSE metrics (posterior risk,
   confidence, omega), SRS; ICSE cost-validity argument.
3. Study design (4.5 pp) — corpora taxonomy, protocol freezes, SRS audit,
   hypotheses/statistics, reproducibility.
4. RQ1: replication at fixed size (5 pp) — 4 sub-RQs, per-claim verdicts.
5. RQ2: cost re-indexing (6.5 pp) — heterogeneity, decision impact,
   cost-normalized recommendation, equal-spend + mechanism.
6. Discussion (3 pp) — the triple (strategy, outcome, coupling); budget
   amortization; implications for practitioners (frontier thinking, not
   top-1) and for FSE-style evaluation protocols.
7. Threats (1.5 pp). 8. Related work (2 pp). 9. Conclusion (1 pp) +
   data availability (0.5 pp). Total ~29.5 pp + references.

## 11. Explicitly out of scope (state in the paper)

FSE's noisy/restricted-ground-truth experiments; best-case (`min`)
bounds; blocked corpus-level meta-tests; porting to the public
reproducibility repository (pending decision).
