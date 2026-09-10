# Linux Learner Sensitivity: All Features, Light Protocol

This run removes the `--top-k-features 512` cap and keeps all Linux options after mandatory forbidden-column removal, rare-option pruning, and exact duplicate removal.

Command:

```bash
.venv-linux/bin/python scripts/run_learner_sensitivity.py \
  --output-dir artifacts/learner_sensitivity_linux_allfeatures_light \
  --families linux \
  --linux-top-k-features 0 \
  --linux-diversity-runs 0 \
  --linux-uncertainty-runs 0 \
  --linux-coverage-runs 0 \
  --continue-on-error
```

This is a matched light protocol for feature-selection sensitivity. It intentionally disables diversity, uncertainty, and coverage because those samplers are feature-space-heavy and would make the no-top-k run much more expensive.

All 21 jobs completed successfully. `ridge-log` is the best-MRE learner on all 7 Linux releases.

