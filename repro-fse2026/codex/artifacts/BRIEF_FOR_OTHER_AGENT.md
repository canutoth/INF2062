# Brief for the framing agent — Linux DEMOTE reframe (+ consistency guardrails)

**Decision (locked with the author): keep Linux, demote it — do NOT delete.** Linux is the
sturdiest robust evidence in the paper (KW top-group change 100%, robust 93%, Pareto differs 100%);
deleting it to dodge a framing objection would remove the strongest pillar of the robust headline.
The objection ("vmlinux size isn't acquisition cost") is answered by *reframing in one paragraph +
a cost-semantics table*, not by cutting data. All three reviewers asked for demote/reframe; none asked
to delete.

## The core move: size ≡ cost ⇒ strategy bias ALONE breaks the proxy
For Linux the prediction *target* (uncompressed image size) IS the cost axis, so there is **no
target–cost asymmetry** to exploit. That makes Linux the most favorable case for the count proxy —
and the fact that measured cost STILL re-ranks the recommendable samplers on every release proves a
mechanism no other family isolates: **strategy-induced selection bias, by itself, is sufficient to
break sample count as a budget.** This is a *stronger* story than the other families, not a weaker one.

## Drop-in framing paragraph (adapt as needed — §III cost model and/or RQ3 Linux exhibit)
> For Linux we predict the uncompressed kernel image size and treat that same size as the measured
> cost. This is deliberately the most favorable case for the count proxy: the prediction target and
> the paid resource coincide, so no target–cost asymmetry is available to exploit. A real budget still
> exists—shippable image bytes are a hard constraint for embedded and over-the-air deployment—but we
> do not claim image size measures label-\emph{acquisition} effort, and our headline acquisition-cost
> results rest on the five families where the cost is acquisition cost. Linux instead isolates a single
> mechanism: even when target and cost coincide, strategy-induced selection bias alone re-ranks the
> statistically recommendable samplers (Kruskal--Wallis top group changes on all releases, robust on
> 93\%; the Pareto-efficient set differs on every release). The simple, calibrated samplers
> (\texttt{random}, \texttt{balanced}, \texttt{coverage}) win, while the feature-aware ``smart''
> samplers (\texttt{diversity}, active learning) are both miscalibrated in cost and worse in accuracy.
> Strategy bias, not heterogeneous targets, is enough to invalidate sample count as a budget.

## Cost-semantics table to add near §III (R1/R2/R3 all asked for this)
Columns: Family | Prediction target | Measured cost axis | Cost interpretation | In the acquisition-cost claim?
- ICSE19 → performance | runtime | measurement time | **yes**
- x264 → time or size | encode time / output size | measurement time / resource target | **partly**
- ENERGY → energy/perf | time or energy | measurement resource | **yes (caveat)**
- WORKLOAD → performance | wall time / throughput | measurement time | **yes**
- LCBENCH → accuracy | training runtime | training/eval time | **yes**
- LINUX → image size | vmlinux size | resource/deployment budget | **no — resource-budget stress test**
Then change "measured acquisition cost" → "measured cost (usually acquisition cost; for Linux a
resource-budget proxy)" in the abstract/intro/§III.

## Consistency guardrails (so we don't desync)
- **Energy = 14-system everywhere: KW 50%, Pareto 80%.** Abstract/intro must use 50%, not 47%.
- **"38–55% across five non-Linux families" is consistent** (ICSE19 38, x264 55, energy 50, workload
  46, lcbench 42) — verify the abstract uses exactly this.
- **MRE → percent everywhere.** You take `main.tex` figure captions + appendix; I take `5-results.tex`.
- **Budget rule:** soften "deployable from measured costs alone" → "retrospective, cost-indexed
  evaluation device" in `4-study_design.tex:56`. I soften the matching phrase in `5-results.tex:121`.
- **Hands off (mine):** `7-threats.tex`, `5-results.tex`. In particular `tab:rq-metrics` ("Table II")
  lives in my file and is already 14-system-correct — do not edit its numbers; I'll dash the "evicted"
  column for the generated rows (R3).
- **Yours:** `main.tex`/abstract, `1-introduction.tex`, `3-cost_model.tex`, `4-study_design.tex`,
  `8-related_work.tex` (novelty-vs-mutation-testing paragraph + HPO citations).
