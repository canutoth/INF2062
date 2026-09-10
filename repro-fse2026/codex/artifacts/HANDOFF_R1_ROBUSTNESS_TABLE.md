# Handoff: integrate R1 robustness (bootstrap + eviction + effect size) into Table III + RQ2

**For:** an agent editing `5-results.tex`. All numbers below are final
(minerr policy = canonical, matches the published 43–55%; B=1000 seed bootstrap).
Sources: `artifacts/kw_robust_minerr_{icse19,x264,energy,workload,lcbench}.csv` and the
Linux 6-release aggregate (`significance_linux_hgbtfull_cells_*.pkl`, 413 dropped).

## Final per-family numbers
| Family | top-group Δ | robust Δ (≥.95) | % of changes robust | evicted | Pareto differs | med. Jaccard | eq-budget MRE gap |
|---|---|---|---|---|---|---|---|
| REPLICATION-ICSE19 | 43% (9/21) | 29% (6/21) | 67% | 29% (6/21) | 86% (6/7) | 0.50 | 3.9pp |
| REPLICATION-ICPE20 (x264) | 55% (28/51) | 55% (28/51) | 100% | 41% (21/51) | 100% (17/17) | 0.33 | 0.7pp |
| ENERGY | 47% (35/74) | 18% (13/74) | 37% | 11% (8/74) | 80% (45/56) | 0.65 | 1.6pp |
| WORKLOAD | 50% (423/846) | 23% (195/846) | 46% | 15% (127/846) | 73% (68/93) | 0.60 | 0.9pp |
| LCBENCH | 50% (174/350) | 16% (56/350) | 32% | 13% (45/350) | 89% (31/35) | 0.62 | 0.2pp |
| LINUX (6 rel.) | 100% (30/30) | 97% (29/30) | 97% | 23% (7/30) | 100% (6/6) | 0.38 | 3.3pp |

Ranges: top-group Δ 43–55% (100% Linux); robust Δ 16–55% (97% Linux); evicted 11–41%;
eq-budget gap 0.2–3.9pp. Omnibus KW both-significant 74–100% (unchanged).

## Recommended Table III (`tab:rq-metrics`) edit
The current KW block is `best sampler | top group | both sig.`. **Replace** with
`top group Δ | robust Δ | evicted` (drop the top-1 "best sampler" column — it is the
least meaningful lens — and move "both sig. 74–100%" to the caption). Keep the Pareto
block `differs | med. Jaccard`. New header/rows:

```
& \multicolumn{3}{c}{Kruskal--Wallis sampler test} & \multicolumn{2}{c}{Pareto choice set} \\
Family & top-group $\Delta$ & robust $\Delta$ & evicted & differs & med.\ Jaccard \\
REPLICATION-ICSE19  & $43\%$  & $29\%$ & $29\%$ & $86\%$  & $0.50$ \\
x264                & $55\%$  & $55\%$ & $41\%$ & $100\%$ & $0.33$ \\
ENERGY              & $47\%$  & $18\%$ & $11\%$ & $80\%$  & $0.65$ \\
WORKLOAD            & $50\%$  & $23\%$ & $15\%$ & $73\%$  & $0.60$ \\
LCBENCH             & $50\%$  & $16\%$ & $13\%$ & $89\%$  & $0.62$ \\
LINUX               & $100\%$ & $97\%$ & $23\%$ & $100\%$ & $0.38$ \\
```
Caption additions: define *robust Δ* = the top-group change reproduces in ≥95% of
seed-bootstrap resamples (B=1000); *evicted* = the source study's recommended sampler
drops out of the cost-controlled top group; omnibus KW significant in both views in
74–100%; equal-budget MRE gap 0.2–3.9pp (small where samplers are near-ties).

## RQ2 prose to add (after the KW headline paragraph)
> To check that these top-group changes are not single-draw artifacts, we bootstrap the
> membership change itself (resample each sampler's per-seed errors, recompute both Dunn
> top groups, B=1000). The change is highly reproducible on the families that ground the
> published-verdict claim — every x264 change, 97% on Linux, 67% on REPLICATION-ICSE19 —
> but only about a third of the generated-family changes reproduce (32–46% on
> ENERGY/WORKLOAD/LCBENCH), where the tied-best samplers are near-ties (equal-budget MRE
> gaps of 0.2–1.6pp). The recommendation-level number is sharper: the source study's
> recommended sampler is *evicted* from the cost-controlled top group in 29–41% of
> replication comparisons. Practically, cost control does not buy large accuracy at a
> fixed budget (the best samplers are close); it changes which sampler is recommendable
> and what reaching that accuracy costs, with the robust decision-level signal carried by
> the Pareto choice set.

## Framing guardrails (consistency with the overpromise handoff)
- This is cost-effectiveness + recommendation-validity, NOT free accuracy. Do not let the
  robust/eviction numbers be read as "much better predictions."
- Be explicit that ENERGY/LCBENCH top-group changes are largely reseeding noise; the
  load-bearing KW evidence is the replications + Linux. The generated families' robust
  signal is Pareto, not KW.
- The honest tempering strengthens credibility (directly answers reviewer R1#1–#3).
