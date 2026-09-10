# Review response — consolidated "strong" paper

**Deliverable:** `cost-sampling-STRONG-consolidated.pdf` (main repo root).
**Source:** git worktree `/Users/mathieuacher/SANDBOX/csm-strong`, branch `variant/strong`,
paper dir `607058f5f5131dcd1dbd783d/`. Builds with `latexmk -pdf main.tex`.

**Layout:** main text fills a genuine 10 pages; references begin at the very
bottom of page 10 and run onto page 11 (page 10 is ~90 % content, *not* a lost
page). Zero undefined citations/references. No overfull boxes > 20 pt.

This paper consolidates the three review-addressing variants into one: it takes
the **decision** variant as base (master cross-family table, all universal
fixes) and grafts the **audit** variant's boxed *Cost-Proxy Audit* and the
**validity** variant's construct-validity framing — i.e. all three centerpieces
the review actually asks for.

## Highest-priority items

| # | Review ask | Status | Where |
|---|------------|--------|-------|
| 1 | Page limit ≤ 10 pp main text | ✅ | 10 full content pages, refs on 10(bottom)–11 |
| 2 | Move the literature gap into the Introduction | ✅ | Intro ¶3 "The gap is not the absence of a better sampler; it is the absence of a validity check for the effort axis itself." |
| 3 | Master "what changes when count→cost" table | ✅ | Table II (`tab:master`), one-screen cross-family summary; replaces the dense Fig. 3 gallery |
| 4 | Move 538/1666 earlier | ✅ | Abstract, contribution bullet #1, **and** RQ2 opening sentence |
| 5 | Acquisition vs. resource cost (Linux) | ✅ | Cost model: Linux named a "resource-budget extension" (storage-bound `vmlinux` size) |
| 6 | Separate deployable strategies from oracles | ✅ | Method sentence in cost model; protocol note; "deployable strategies only" in every results caption + both new tables; oracles defined as diagnostic in Background. Remaining figures contain **no** oracle labels (old `cheap_n8` gallery removed) |
| 7 | Define the normalized objective exactly | ✅ | Cost model: "min–max normalization of MRE and the cost term over the **deployable** strategy–budget combinations within the same system–input–target context … conclusions are stable under rank normalization" |
| 8 | Sharper contribution bullets | ✅ | 4 bullets: decision impact (538/1666), six families, construct-validity mechanism, named **Cost-Proxy Audit** |

## Title / abstract / figures / discussion / related work / artifact

- **Title** → "When Sample Size Misprices Sampling Cost in Configurable-System Performance Prediction."
- **Abstract** rewritten around the mispricing message + 538/1666 + measured-cost validation.
- **Figures:** kept Fig. 1 (same-size 16.5× gap running example) and Fig. 2 (larger-but-cheaper inversion); replaced the dense 4-panel mechanism gallery with Table II; kept the target–cost asymmetry figure (Fig. 3). RQ-answer boxes kept short.
- **Discussion** kept the four messages (under-specified claims / three cost claims; cost-aware sampling is an opportunity; heterogeneity × strategy bias; lightweight audit) and adds a boxed **Cost-Proxy Audit**, a worked "audit in action" (LLVM passes, lrzip fails), and an explicit "construct-validity result, not a new metric" framing.
- **Related work:** "Counting effort versus measuring acquisition cost" is the 2nd paragraph (gap up front).
- **Artifact** paragraph present (Study Design): selected configs, seeds, measured targets/costs, scripts to recompute TrainCost, Ratio, flips, Pareto fronts.

## Added rigor (also fills the page budget with substance, not padding)

- **Table III** — REPLICATION-ICSE19 per-system numbers (CV, p90/p10, Ratio, flips, Pareto), grounding the running example (lrzip) and the three regimes.
- **Table IV** — LINUX per-release strategy-specific Ratio (random ≈ 1, diversity 1.24–1.52×, uncertainty < 1): the clearest mechanism evidence.
- **Table V** — x264 four cost–target scenarios (flips, agreement, Jaccard), tied to the asymmetry figure.

## Author actions still open (not paper edits)

- Confirm venue/DOI for 3 camera-ready refs: `ye2026domland` (TOSEM 2026), `xiang2026dhda` (ICSE 2026), `ye2025dlisa` ("Accepted at ICSE 2025" — update note to final proceedings). All have DOIs/URLs; none fabricated.
- Pick ICSE area (review suggests Requirements & Modeling, alt. Analytics).
- Freeze title/abstract for the mandatory abstract deadline; decide on the generative-AI disclosure per ICSE policy.
