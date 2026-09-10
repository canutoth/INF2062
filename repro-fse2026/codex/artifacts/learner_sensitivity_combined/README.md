# Combined Learner Sensitivity Summary

This directory combines:

- the compact cross-family learner pass from `artifacts/learner_sensitivity_compact`, excluding its failed Linux rows, and
- the completed Linux-only learner pass from `artifacts/learner_sensitivity`.

The combined manifest points to the original per-family output directories, so this directory contains only the merged manifest and derived summary/report files.

## Main Outputs

- `learner_sensitivity_report.md`: cross-family Markdown report.
- `learner_sensitivity_summary.csv`: median metrics by family, label, and learner.
- `learner_sensitivity_winners.csv`: best learner by criterion.
- `learner_sensitivity_long.csv`: per-unit rows used by the summary.
- `manifest.csv`: merged command manifest.

## Reading

The Linux sweep completed for all 7 releases and all 3 learners. Ridge/log-linear is the best-MRE learner on 6 of 7 Linux releases, while boosted trees most often give the highest Pareto overlap. This supports keeping ridge/log-linear as the primary Linux learner and using random forests/boosted trees as robustness checks rather than replacing the primary learner wholesale.

