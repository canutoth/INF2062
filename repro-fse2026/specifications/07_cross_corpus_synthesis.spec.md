# Specification 07 — Phase 7: Cross-Corpus Synthesis & Paper-Ready Claims

Inputs: the per-corpus outputs from Specs 02–06.
Outputs: `artifacts/fse_posterior_synthesis/` — one synthesis Markdown, one
synthesis CSV, and the paper-level figures.

See Spec 00 §6 (metrics), §7 (hypotheses), §12 (deliverables).

---

## 1. Goal

Turn per-corpus outputs into one coherent table and a small number of
paper-ready figures.

## 2. Synthesis table

One row per corpus, columns:

- corpus;
- number of systems / contexts / scopes;
- strategy-risk distributions differ (H1);
- SRS best empirical-cost-normalized (H3);
- SRS on empirical Pareto frontier;
- top recommendation changed by cost (H2);
- Pareto frontier changed by cost (H4);
- SRS lower risk than random (H5);
- SRS cost different from random (H6);
- direct-replication vs. external-validity status.

### 2.1 Sanity target (current numbers — must land close after final reruns)

| Corpus | Scopes | Risk distributions differ | SRS best cost-normalized | SRS on empirical Pareto | Top changes | Frontier changes |
|---|---:|---:|---:|---:|---:|---:|
| FSE artifact | 7 | TBD or per-system | 3/7 | 6/7 | 2/7 | 6/7 |
| x264 | 34 | 34/34 | 26/34 | 29/34 | 2/34 | 30/34 |
| ENERGY | TBD | TBD | TBD | TBD | TBD | TBD |
| WORKLOAD | TBD | TBD | TBD | TBD | TBD | TBD |
| Linux quick | 14 | 11/14 | 3/14 | 8/14 | 9/14 | 14/14 |
| LCBench | 210 | 155/210 | 0/210 | 20/210 | 119/210 | 207/210 |

## 3. Synthesis figures

1. **Corpus-level heatmap** — rows: corpus; columns: H1–H6; cells: support rate.
2. **SRS status matrix** — rows: corpus/scopes; columns: best, Pareto, lower risk
   than random, cost differs.
3. **Cost-normalization impact plot** — changed top recommendation; changed
   Pareto frontier.
4. **Three representative guarantee-cost frontiers** — SRS best; SRS Pareto but
   not best; SRS not Pareto.
5. **Calibration plot** — `pct_n` vs `pct_cost`; line `y = x`; color by strategy.

## 4. Paper-ready claims

| ID | Claim |
|---|---|
| A | FSE-style posterior risk and confidence can be reproduced and extended across multiple measured reference universes. |
| B | Empirical acquisition cost changes the strategy decision surface. The Pareto frontier changes far more often than the top scalar recommendation alone. |
| C | SRS stays strong on the original FSE-style configurable-system setting and on x264, but it is not a universal empirical-cost-normalized recommendation. |
| D | Linux and LCBench are external-validity stress tests: they preserve the usefulness of posterior risk while revealing SRS boundary conditions. |
| E | ENERGY and WORKLOAD determine whether the posterior-guarantee version of the question behaves like the ICSE prediction-error version when the cost property or workload context changes. |

**Avoid:** "LCBench refutes FSE 2026." / "SRS is bad." / "Posterior risk is
invalid on Linux." / "Measured-pool posterior risk is the same as exhaustive
configuration-space posterior risk."

**Prefer:** "SRS recommendation is dataset- and cost-dependent." / "Posterior
risk remains valid relative to the measured reference universe." / "Sample size
is an incomplete cost abstraction for posterior guarantees."

## 5. Deliverables (whole study)

- one synthesis Markdown;
- one synthesis CSV;
- paper-level figures (§3);
- final TODO list;
- reproduction commands;
- data provenance notes.

## 6. Libraries

`numpy`, `pandas`, `matplotlib`, `seaborn` (heatmaps). No new dependencies.
