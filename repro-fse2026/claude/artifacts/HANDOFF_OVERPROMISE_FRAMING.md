# Handoff: stop overpromising "cheaper AND more accurate" — claim cost-effectiveness

**For:** an agent editing the paper. **Scope:** small, surgical wording fixes. Do NOT
re-run experiments or change numbers. **Goal:** the paper must claim
**cost-effectiveness**, not universal strict dominance.

## The principle (what the paper may and may not claim)
- **Claim (general, defensible):** for a given measured budget, a cost-aware sampler
  reaches **better accuracy** — equivalently, the same accuracy for **less cost**. The
  efficient (Pareto) frontier moves, and the published *recommendation* can change.
- **Do NOT claim (overpromise):** that cost-aware sampling is generally **both cheaper
  and more accurate** at the same sample size. That strict dominance happens in
  *specific* cases (the lrzip running example is a real one) but is not the thesis.

## Why (evidence basis — R1#3)
The reviewer-style robustness analysis shows that when the cost-controlled KW top group
changes, the samplers involved are **statistically tied** in raw accuracy: the
equal-budget MRE gap is modest (a few points; ~3.3pp on Linux, near-0 cross-view) and
the top-1 best-sampler flips are near-ties. The large, robust signal is in **set
membership + eviction** (the source study's recommended sampler is evicted in **29–41%**
of replication comparisons) and in **cost / Pareto** (RQ1's 16.5× same-$n$ gaps, Jaccard
0.37), **not** in free accuracy gains. So a "cheaper and more accurate" headline would
overreach exactly where a reviewer can check.

## Call to action — specific edits (current → replacement)

1. **Abstract** (`main.tex`, ~l.136). Current:
   > "...cost-aware samplers the count view cannot see, **which can be cheaper and more
   > accurate at once**."
   Replace the bolded clause with cost-effectiveness:
   > "...cost-aware samplers the count view cannot see, **which reach better accuracy at
   > the same measured budget**."

2. **Intro contribution bullet** (`1-introduction.tex`, ~l.177). Current:
   > "...\texttt{pilotCost}... is on several systems **at once the cheapest \emph{and} the
   > most accurate choice**."
   Replace with:
   > "...\texttt{pilotCost}... is on several systems **the most cost-effective choice
   > (better accuracy at equal measured cost)**."

3. **Intro thesis-motivation sentence** (`1-introduction.tex`, ~l.116). Current:
   > "**This strict dominance (cheaper \emph{and} more accurate at the same sample size)**
   > is why our question is not only whether $n$ correlates with cost in aggregate, but
   > whether $n$ is a valid cost axis..."
   Reframe to motivate by cost-effectiveness, and demote the dominance to the example:
   > "**In this instance the cost-aware sample is even strictly dominant (cheaper and more
   > accurate); in general the point is weaker but still decisive — at a fixed budget the
   > cost-aware choice is more cost-effective.** This is why our question is not only
   > whether $n$ correlates with cost in aggregate, but whether $n$ is a valid cost axis..."

4. **Fig 1 running example — lead with the COST gap, demote the accuracy edge.** The robust,
   defensible content is the same-$n$ **16.5× cost gap** and **cost-effectiveness** (pilotCost
   reaches *comparable* accuracy for far less measured budget). The accuracy edge (pilotCost
   51.6% vs diversity 60.6% MRE) is a **near-tie** at $n{=}16$ (per R1#3, within noise), so do
   NOT present it as dominance.
   - `1-introduction.tex` ~l.94–98: drop "strictly dominates diversity on both cost and error";
     keep the cost facts, reframe the accuracy line as "and, in this instance, even slightly
     more accurate" (incidental, scoped).
   - Fig 1 caption ("the cheapest is also the most accurate"): reframe to "...spends 16.5×
     less to reach comparable accuracy" (cost-effectiveness), drop the accuracy-dominance.
   - `5-results.tex` ~l.106–113 ("sharpest local failure"): keep the cost gap, soften "the
     cheaper choice can also be the better one" to a scoped, near-tie statement.
   Note: lrzip cost (runtime) and target (energy) are ~0.99 correlated, so this example does
   NOT illustrate target/cost decoupling — that is fine and is not the point; the point is the
   cost gap. Reserve "target differs from acquisition cost" language for x264 (time vs size).

5. **KEEP (already correct, anti-overpromise):** `5-results.tex` ~l.353 "the scientific
   message is not that one sampler dominates in all settings...". This is the desired tone;
   mirror it elsewhere.

## Vocabulary to use / avoid
- Prefer: "cost-effective", "better accuracy at the same (measured) budget", "same
  accuracy for less cost", "moves the efficient frontier", "changes the recommendation".
- Avoid as *general* claims: "cheaper and more accurate", "strictly dominates", "wins on
  both" (fine only when explicitly scoped to the lrzip example).

## Acceptance check
After editing, grep `more accurate|cheaper and|strictly dominate|dominates|cheapest`
across `main.tex 1-introduction.tex 5-results.tex 9-conclusion.tex`; every surviving hit
must be either (a) scoped to the lrzip running example, or (b) an explicit
*cost-effectiveness* statement. No general "both accuracy and cost" promise should remain.
