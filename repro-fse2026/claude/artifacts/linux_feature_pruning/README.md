# Linux Feature Pruning Diagnostics

This artifact documents the feature pruning used before fitting Linux learners.

## What Is Mandatory

The forbidden columns are still excluded. They include the target (`vmlinux`), compressed-size variants, `active_options`, and `cid`. Keeping them would leak target/cost-derived information or row identity into the learner.

## What Is Mild

Rare-option pruning removes options whose minority class has fewer than 50 configurations. This removed only 37 to 295 options per release, leaving 9,172 to 11,415 option columns before duplicate removal.

Exact duplicate removal is information-preserving: if two option columns have identical values over the full release pool, only the first representative is kept. The duplicate mappings are in `linux*_duplicate_groups_all_remaining.csv`.

## What Was Aggressive

The previous `--top-k-features 512` cap was the aggressive step. After rare-option and duplicate pruning, the full retained feature sets contain 8,760 to 10,935 columns. The 512 cap selected only 512 columns by marginal target effect, then duplicate removal left 489 to 497 columns.

## Matched Light Comparison

To isolate feature selection from sampler differences, two matched Linux learner passes were run with:

- levels `0.01,0.02,0.05`
- random and balanced stochastic sampling only, 10 runs per level
- cheap/expensive oracle samples
- diversity, uncertainty, and coverage disabled

The matched outputs are:

- `../learner_sensitivity_linux_topk512_light`
- `../learner_sensitivity_linux_allfeatures_light`

Result: with all post-rare/post-duplicate features, `ridge-log` has the best median MRE on all 7 Linux releases. With the matched 512-feature cap, `ridge-log` wins 6 of 7 releases and `rf-log` narrowly wins Linux 5.04. Absolute MRE changes, so the feature cap should be documented as an efficiency choice, but the Linux learner conclusion is robust: all-feature RF/GBT do not overtake ridge.

