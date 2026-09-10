# Linux Learner Sensitivity: Augmented Budgets

This run tests whether the high Linux MRE mainly comes from too-small training ratios.

Command:

```bash
.venv-linux/bin/python scripts/run_learner_sensitivity.py \
  --output-dir artifacts/learner_sensitivity_linux_topk512_augmented \
  --families linux \
  --linux-top-k-features 512 \
  --linux-levels 0.01,0.02,0.05,0.10,0.20 \
  --linux-diversity-runs 0 \
  --linux-uncertainty-runs 0 \
  --linux-coverage-runs 0 \
  --continue-on-error
```

The run keeps the matched light protocol used for the Linux feature-sensitivity check and adds 10% and 20% budgets.

## Outputs

- `learner_sensitivity_report.md`: aggregate learner report.
- `learner_sensitivity_summary.csv`: aggregate by release and learner.
- `learner_sensitivity_winners.csv`: best learner by criterion.
- `linux_budget_level_summary.csv`: random/balanced median MRE by release, learner, and budget.
- `linux_budget_level_best_random_balanced.csv`: best of random/balanced per release, learner, and budget.

## Result

Increasing the budget helps ridge/log-linear on every Linux release, but it does not bring Linux below 10% MRE. At 20% training ratio, the best learner is still `ridge-log` on all seven releases, with median MRE between 0.208 and 0.341.

This means the earlier ~30% Linux MRE is partly a training-budget issue, but not only that. Linux remains a harder target under the current feature representation and learner setup.

