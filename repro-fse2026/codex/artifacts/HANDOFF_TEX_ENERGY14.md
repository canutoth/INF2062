# Handoff to the .tex-editing agent — ENERGY 14-system reconciliation (2026-06-30)

From the coordinating/data agent. **The data side is complete and consistent; the
items below are `.tex` actions only.** No re-run is needed.

## ENERGY is now 14 systems — authoritative numbers
Source: `artifacts/kw_robust_largestn_energy_all14.csv` (largest-n policy, full
candidate set incl. pilotCost, ridge-log, membership-bootstrap 1000).
- **N = 112** (14 systems × 8 budget levels), 14 contexts: 7z, Apache, HSQLDB,
  LLVM, MongoDB, PostgreSQL, VP8, brotli, exastencils, jump3r, kanzi, lrzip,
  nginx, x264.
- **top-group Δ = 50%** (56/112)
- **robust Δ = 26%** (29/112); reproduces 52% of changed
- **evicted = 17%** (19/112)
- **KW-sig both views = 83%** (93/112)
- minerr policy (sensitivity) = 52% (58/112)
- equal-budget MRE gap on changed comparisons ≈ 0

## Pareto/Jaccard: ALREADY 14-system — DO NOT recompute or change
`artifacts/significance_pareto_energy.csv` is **56 scenarios = 14 systems × 4
cost–target combos** → **80% (45/56), median Jaccard 0.65**. The Table III ENERGY
Pareto cell (80% / 0.65) is already correct for 14 systems. The caption count
`ENERGY 112/56` is correct (112 KW, 56 Pareto, both 14-system).

The earlier mismatch was only that KW was 9-system (47%) while Pareto was already
14-system (80%). With KW corrected to 14-system (50%), the whole ENERGY row is now
internally consistent.

## `.tex` items to apply / verify
1. **RQ2 headline** (`5-results.tex`): ENERGY should read **56/112 (50%)**.
   NOTE: the coordinating agent already changed this from `35/74` — please verify
   it stuck and reconcile if you also edited it.
2. **Table III ENERGY row**: `50% & 26% & 17% & 80% & 0.65` — already updated; verify.
3. **Bootstrap-framing prose**: energy reproduce range is now **29–52%**
   ("a third to a half") — already updated; verify.
4. **Threats Strategy-panel paragraph** (`7-threats.tex`): full-panel reads
   "47/46/42%" but energy is now **50%** → should be **"50/46/42%"**. Also confirm
   the pilotCost-**excluded** "54% energy" is computed on the same **14** systems
   (apples-to-apples vs 50%); if that 54% is 9-system, recompute or note it.
5. **Threats punctuation**: remove the em-dash in `47/46/42\%---undiminished` and
   the semicolon in `we introduce; \texttt{pilotCost}` (global no-em-dash /
   no-semicolon rule).
6. **Page limit**: the expanded Strategy-panel paragraph put main text ~0.2 page
   over 10. Trim a redundant spot (e.g., the intro lrzip deep-dive or the RQ3
   brotli paragraph) to land back at 10 main pages + refs.

## Headline ranges are UNCHANGED by energy 47→50
top-group **38–55%** (non-Linux) / **100%** Linux; robust **12–93%**; evicted
**11–41%**; KW-sig both **74–100%**; Pareto **73–100%**. All still hold with
energy at 50%. No range edits needed.
