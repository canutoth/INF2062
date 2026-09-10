# Linux: corrected numbers + paper edit list (2026-06-28 night)

## What happened
The paper's Linux numbers come from a **crippled run** (`significance_linux_kw.csv`,
512-feature ridge, ~30% MRE where the ranking is noise). The **corrected** run
(full features + sk-hgbt-log, MRE ~7% at the 20% budget) gives a *much stronger*
and qualitatively different result. Overnight orchestration (`scripts/overnight_linux.sh`,
bg job) waits for the in-flight HGBT job, builds the missing release 507, and
aggregates all 7 releases into `artifacts/significance_linux_hgbtfull_*`.

## Corrected numbers (PRELIMINARY — from 5/7 cached releases {415,420,500,504,508}; final 7/7 pending)
| metric | OLD (in paper now) | CORRECTED |
|---|---|---|
| KW top-group change | 49% (17/35) | **100%** (25/25 prelim; expect ~35/35) |
| KW best-sampler change | 26% (9/35) | **~28%** (7/25 prelim) |
| KW both-significant | 100% | 100% |
| Pareto robustly differs | 4/7 | **7/7** (5/5 prelim) |
| median Jaccard | 0.67 | **~0.38** (0.31–0.56) |
| MRE @20% budget | ~30% (noise) | **~7%** (sane) |

## Key implication — REVERSES the "Linux is the safe exception" framing
Even though target = cost = vmlinux size, strategy-level cost bias (diversity
1.24–1.52× its count share; uncertainty/AL erratic) makes the top group reshuffle
**every** comparison. Linux is now the **strongest** cost-effect family, not the
exception. This also changes the cross-family ranges:
- Pareto range was **57–100%** (Linux=57% was the floor) → becomes **73–100%** (workload 73% new floor).
- KW range 43–55% gains a 100% outlier (Linux); report Linux separately or widen to "43–55%, 100% on Linux".

## Exact edits (file:line → change) — DO AFTER final 7/7 aggregate lands
1. `5-results.tex:182` tab:rq-metrics Linux row `$26\%$ & $49\%$ & $100\%$ & $57\%$ & $0.67$`
   → `$28\%$ & $100\%$ & $100\%$ & $100\%$ & $0.38$` (use FINAL numbers).
2. `5-results.tex:170` Range row Pareto `$57$--$100\%$` → `$73$--$100\%$`; KW range note Linux=100%.
3. `5-results.tex:142` "$17/35$ \StudyLinux comparisons ($49\%$)" → corrected (e.g. "$35/35$, $100\%$").
4. `5-results.tex:219–222` the "Linux is the exception … differs on only $4/7$ … KW changes $49\%$ …
   ranking lens more sensitive" paragraph → **REFRAME**: Linux is the strongest case; both lenses
   max out (KW 100%, Pareto 100%) because strategy cost-bias survives even target=cost. ⚑ USER-REVIEW.
5. Check also: RQ2 finding box ranges (line ~270), `7-threats.tex:29` ("Linux 0.29"),
   abstract/intro/conclusion any "57–100%" or "Linux exception" phrasing.
6. `tab:decision-summary` Linux row regime is already "Changed every release" — consistent, keep.

## Sanity
Old `significance_linux_kw.csv` is the buggy artifact; corrected is `*_hgbtfull_kw.csv`
(7 releases × 5 levels = 35 comps when complete). Preview used `--reuse-cells` (no refit).
